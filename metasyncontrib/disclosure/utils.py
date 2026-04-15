"""Utilities for disclosure control."""

from __future__ import annotations

from typing import NamedTuple, Optional

import numpy as np
import numpy.typing as npt
import polars as pl

try:
    from numpy.core._exceptions import UFuncTypeError  # type: ignore
except ImportError:
    from numpy._core._exceptions import UFuncTypeError  # type: ignore


def _compute_dominance(block_values: npt.NDArray, reverse: bool=False):
    """Compute the dominance over a set of microaggregated values.

    Parameters
    ----------
    block_values
        The original values aggregated into bins with shape (N/partition_size, partition_size).
    reverse, optional
        Whether the dominance of the highest or lowest value is computed, by default False

    Returns
    -------
        The maximum of the dominance for all microaggregated bis.

    """
    if len(block_values) == 0:
        return 0
    if not reverse:  # dominance of highest value
        min_values = np.min(block_values, axis=1).reshape(-1, 1)
        diff_values = block_values - min_values
        same_vals = np.all(block_values == min_values, axis=1)
    else:  # Dominance of the lowest value
        max_values = np.max(block_values, axis=1).reshape(-1, 1)
        diff_values = max_values - block_values
        same_vals = np.all(block_values == max_values, axis=1)

    # If any of the bins have values that are the same, the dominance critereon has failed.
    if same_vals.any():
        # Dominance can't be more than 1, but using the number of failed bins aids the convergence.
        return 1+same_vals.mean()
    dominance = diff_values.max(axis=1) / diff_values.sum(axis=1)
    return np.max(dominance)


def _meanify(block_values):
    try:
        mean_vals = block_values.mean(axis=1)
    except UFuncTypeError:
        # Datetime detected
        # Workaround for years < 1970 that should work for Windows and Linux/OS X
        mean_vals = []
        for block in block_values:
            mean_vals.append(pl.Series(block).dt.cast_time_unit("us").mean())
        mean_vals = np.array(mean_vals)
    return mean_vals

def _create_subsample( # pylint: disable=too-many-locals
    values: pl.Series,
    n_blocks: int,
    pre_remove: int = 0,
    post_remove: int = 0,
) -> tuple[list, float]:
    """Use microaggregation on a list of values.

    Parameters
    ----------
    values:
        Values to microaggregate.
    partition_size, optional
        Partition size to be used for the microaggregation, bin size, by default 11
    pre_remove, optional
        Remove the lowest N values from the original values, by default 0
    post_remove, optional
        Remove the highest N values from the original values, by default 0

    Returns
    -------
    sub_values:
        Aggregated values
    dominance:
        Maximum of all aggregated values

    Raises
    ------
    ValueError
        If there are not enough values to create subsamples.

    """
    # Sort and arange values low-high
    sorted_values = np.sort(values)
    sorted_values = sorted_values[pre_remove : len(values) - post_remove]
    n_values = len(sorted_values)


    # Get the number of aggregation blocks and the remainder
    partition_size = n_values // n_blocks
    # n_blocks = n_values // partition_size
    leftover = n_values % partition_size
    if n_blocks < 1:
        raise ValueError("Cannot find subsample with current settings.")

    blocks_left = sorted_values[:leftover*(partition_size+1)].reshape(leftover, partition_size+1)
    blocks_right = sorted_values[leftover*(partition_size+1):].reshape(
        n_blocks-leftover, partition_size)

    # assert blocks_left.size + blocks_right.size == len(sorted_values)

    # Compute dominance both for high and low values
    dominance = max(
        _compute_dominance(blocks_left, reverse=False),
        _compute_dominance(blocks_left, reverse=True),
        _compute_dominance(blocks_right, reverse=False),
        _compute_dominance(blocks_right, reverse=True)
    )
    mean_vals = np.concatenate((_meanify(blocks_left).reshape(-1), _meanify(blocks_right).reshape(-1)))
    return mean_vals, dominance


def micro_aggregate(values: pl.Series, min_partition_size: int = 11, max_iterations: int = 1000,
                    max_dominance: float = 0.5) -> pl.Series:
    """Use micro-aggregation to make the data safe for disclosure purposes.

    Arguments:
    ---------
    values:
        Values that need to be micro-aggregated.
    min_partition_size:
        Micro-aggregate over at least this many values.
    max_iterations:
        Maximum number of iterations to find a solution that satisfies the dominance
        criterion.
    max_dominance:
        Maximum dominance that is allowed during the microaggregation.

    Returns:
    -------
    new_values:
        Aggregated values.

    """
    # Compute initial settings of parition_size, start_remove, end_remove
    assert min_partition_size > 6, ("Please use a bigger minimum bin size, or disclosure "
                                    "control will not work.")
    
    cur_settings = [len(values) // min_partition_size, 0, 0]
    sub_values, dominance = _create_subsample(values, *cur_settings)

    class Solution(NamedTuple):  # pylint: disable=missing-class-docstring
        sub_values: list
        dominance: float
        settings: list
        grad: float

    for _ in range(max_iterations):
        print(dominance, max_dominance)
        # Found a viable solution
        if dominance < max_dominance:
            break

        best_solution: Optional[Solution] = None
        # max_diff = cur_settings[0] // 2  # Maximally try changes with partition_size/2
        # Iterate over parameter to change
        for new_settings in _search_domain(*cur_settings, min_partition_size, len(values)):
        # for i_par in range(3):
            # for add_par in range(1, max_diff):
                # new_settings = [
                    # x if j_par != i_par else x + add_par for j_par, x in enumerate(cur_settings)
            # ]
            # print(new_settings)
            try:
                new_bin, new_dom = _create_subsample(values, *new_settings)
            except ValueError:
                continue

            # Find the solution with the best gradient
            grad = (dominance - new_dom)/_diff_settings(cur_settings, new_settings)
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

def _search_domain(n_partitions, pre_remove, post_remove, min_partition_size, series_size):
    delta_part = max(1, n_partitions//5)
    for part in range(n_partitions-delta_part, n_partitions+delta_part+1):
        partition_size = series_size // part
        delta_remove = max(1, partition_size // 4)
        if partition_size < min_partition_size:
            continue
        for new_pre_remove in range(pre_remove-delta_remove, pre_remove+delta_remove+1):
            if new_pre_remove < 0:
                continue
            for new_post_remove in range(post_remove-delta_remove, post_remove+delta_remove+1):
                if new_post_remove < 0:
                    continue
                if ((part, new_pre_remove, new_post_remove)
                        == (n_partitions, pre_remove, post_remove)):
                    continue
                yield part, new_pre_remove, new_post_remove

def _diff_settings(cur_settings, new_settings):
    diff = 0
    for i in range(len(cur_settings)):
        diff += abs(cur_settings[i]-new_settings[i])
    return diff
