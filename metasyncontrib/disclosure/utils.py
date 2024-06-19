"""Utilities for disclosure control."""

from __future__ import annotations

from typing import NamedTuple, Optional

import numpy as np
import polars as pl

try:
    from numpy.core._exceptions import UFuncTypeError  # type: ignore
except ImportError:
    from numpy._core._exceptions import UFuncTypeError  # type: ignore


def _compute_dominance(block_values, reverse=False):
    if not reverse:
        min_values = np.min(block_values, axis=1).reshape(-1, 1)
        diff_values = block_values - min_values
        same_vals = np.all(block_values == min_values, axis=1)
    else:
        max_values = np.max(block_values, axis=1).reshape(-1, 1)
        diff_values = max_values - block_values
        same_vals = np.all(block_values == max_values, axis=1)
    diff_sum = diff_values.sum(axis=1)
    dominance = diff_values[~same_vals].max(axis=1) / diff_sum[~same_vals]
    # If all values are the same, then dominance is 0.
    if len(dominance) == 0:
        return 0
    return np.max(dominance)


def _create_subsample( # pylint: disable=too-many-locals
    values,
    partition_size: int = 11,
    pre_remove: int = 0,
    post_remove: int = 0,
) -> tuple[list, float]:
    sorted_values = np.sort(values)
    sorted_values = sorted_values[pre_remove : len(values) - post_remove]
    n_values = len(sorted_values)

    n_blocks = n_values // partition_size
    if n_blocks <= 1:
        raise ValueError("Cannot find subsample with current settings.")
    min_block_size = n_values // n_blocks
    leftover = n_values - n_blocks * min_block_size
    if leftover == 1:
        sorted_values = np.delete(sorted_values, [n_values // 2])
    if leftover > 1:
        base_skip = round(n_values / (leftover + 1))
        skip_start = (n_values - base_skip * (leftover - 1) + 1) // 2
        delete_values = skip_start + base_skip * np.arange(leftover)
        sorted_values = np.delete(sorted_values, delete_values)
    assert len(sorted_values) == n_blocks * min_block_size

    block_values = sorted_values.reshape(n_blocks, min_block_size)
    dominance = max(
        _compute_dominance(block_values, reverse=False),
        _compute_dominance(block_values, reverse=True),
    )
    try:
        sub_values = block_values.mean(axis=1)
    except UFuncTypeError:
        # Datetime detected
        # Workaround for years < 1970 that should work for Windows and Linux/OS X
        sub_values = []
        for block in block_values:
            mean_time = pl.Series(block).dt.cast_time_unit("us").mean()
            sub_values.append(mean_time)
    return sub_values, dominance


def micro_aggregate(values: pl.Series, min_bin: int = 11) -> pl.Series:
    """Use micro-aggregation to make the data safe for disclosure purposes.

    Arguments:
    ---------
    values:
        Values that need to be micro-aggregated.
    min_bin:
        Micro-aggregate over at least this many values.

    Returns:
    -------
    new_values:
        Aggregated values.

    """
    assert min_bin > 6, "Please use a bigger minimum bin size, or disclosure control will not work."
    cur_settings = [min_bin, 0, 0]
    sub_values, dominance = _create_subsample(values, *cur_settings)

    class Solution(NamedTuple):  # pylint: disable=missing-class-docstring
        sub_values: list
        dominance: float
        settings: list
        grad: float

    for _ in range(1000):
        if dominance < 0.5:
            break

        best_solution: Optional[Solution] = None
        max_diff = cur_settings[0] // 2
        for i_par in range(3):
            for add_par in range(1, max_diff):
                new_settings = [
                    x if j_par != i_par else x + add_par for j_par, x in enumerate(cur_settings)
                ]
                try:
                    new_bin, new_dom = _create_subsample(values, *new_settings)
                except ValueError:
                    continue
                grad = (dominance - new_dom) / add_par

                if best_solution is None or best_solution.grad < grad:
                    best_solution = Solution(new_bin, new_dom, new_settings, grad)
        if best_solution is None:
            raise ValueError(
                "Could not find solution satisfying dominance conditions for column"
                f" '{values.name}'."
            )
        dominance = best_solution.dominance
        cur_settings = best_solution.settings
        sub_values = best_solution.sub_values

    # If the values are integer types, round the values to the nearest integer.
    if values.dtype in [pl.datatypes.Int64, pl.datatypes.Int32, pl.datatypes.Int32]:
        return pl.Series((np.array(sub_values) + 0.5).astype(np.int64))
    return pl.Series(sub_values)
