"""Utilities for disclosure control."""

from __future__ import annotations

from collections.abc import Iterator
from typing import NamedTuple, Optional, Union

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
        return 0, 0.0
    if not reverse:  # dominance of highest value
        min_values = np.min(block_values, axis=1).reshape(-1, 1)
        diff_values = block_values - min_values
        same_vals = np.all(block_values == min_values, axis=1)
    else:  # Dominance of the lowest value
        max_values = np.max(block_values, axis=1).reshape(-1, 1)
        diff_values = max_values - block_values
        same_vals = np.all(block_values == max_values, axis=1)

    if same_vals.all():
        dominance = 0
    else:
        dominance = diff_values[~same_vals].max(axis=1) / diff_values[~same_vals].sum(axis=1)
    return np.max(dominance), same_vals.sum()


def _meanify(block_values) -> npt.NDArray:
    try:
        mean_vals = block_values.mean(axis=1)
    except UFuncTypeError:
        # Datetime detected
        # Workaround for years < 1970 that should work for Windows and Linux/OS X
        mean_vals = []
        for block in block_values:
            mean_vals.append(pl.Series(block).dt.cast_time_unit("us").mean())
    return mean_vals

def _add_dominances(*args) -> int:
    """Add results from the dominance calculations together."""
    dom = 0
    n_same = 0
    for cur_dom, cur_n_same in args:
        dom = max(dom, cur_dom)
        n_same += cur_n_same

    return dom + n_same

def _create_subsample( # pylint: disable=too-many-locals
    values: pl.Series,
    n_blocks: int,
    pre_remove: int = 0,
    post_remove: int = 0,
) -> tuple[Union[list, npt.NDArray], float]:
    """Use microaggregation on a list of values.

    Parameters
    ----------
    values:
        Values to microaggregate.
    n_blocks
        Number of partitions to be used for the microaggregation.
    pre_remove
        Remove the lowest N values from the original values, by default 0
    post_remove
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
    leftover = n_values % partition_size
    if n_blocks < 1:
        raise ValueError("Cannot find subsample with current settings.")

    # Partition the values into two parts, one part with bins of partition_size
    # and another one with bins of size partition_size + 1.
    # This is done because the number of values is not necessarily divisable by the partition_size.
    blocks_left = sorted_values[:leftover*(partition_size+1)].reshape(leftover, partition_size+1)
    blocks_right = sorted_values[leftover*(partition_size+1):].reshape(
        n_blocks-leftover, partition_size)

    # Compute dominance both for high and low values, for both blocks.
    # Note that the dominance is only the true dominance if there are no bins for which all values
    # have the same value.
    # If there are bins for which all values are the same, the number of these bins are added to
    # the maximum dominance of all bins.
    dominance = _add_dominances(
        _compute_dominance(blocks_left, reverse=False),
        _compute_dominance(blocks_left, reverse=True),
        _compute_dominance(blocks_right, reverse=False),
        _compute_dominance(blocks_right, reverse=True)
    )
    # Get the mean of each bin
    mean_left, mean_right = _meanify(blocks_left), _meanify(blocks_right)
    try:
        mean_vals = np.concatenate((mean_left.reshape(-1), mean_right.reshape(-1)))
    except AttributeError:
        # Datetimes are given back as lists
        mean_vals = mean_left + mean_right
    return mean_vals, dominance


def micro_aggregate(values: pl.Series, fit_log, min_partition_size: int = 11,
                    max_iterations: int = 1000,  # noqa: C901
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
    cur_settings = (len(values) // min_partition_size, 0, 0)
    sub_values, dominance = _create_subsample(values, *cur_settings)
    fit_log.add(privacy=f"Using micro-aggregation with minimum partition size {min_partition_size} "
                f"and maximum dominance of {max_dominance}.")

    _, counts = np.unique(values, return_counts=True)
    new_min_partition_size = round(counts.max() / (2*max_dominance))
    if new_min_partition_size > min_partition_size:
        min_partition_size = new_min_partition_size
        cur_settings = (len(values) // new_min_partition_size, 0, 0)
        sub_values, dominance = _create_subsample(values, *cur_settings)
        fit_log.add(privacy="Detected significant numbers of duplicate values, increasing minimum "
                    f"partition size to {min_partition_size}")

    cache = set()  # A cache that stores all visited solutions.
    class Solution(NamedTuple):  # pylint: disable=missing-class-docstring
        sub_values: Union[list, npt.NDArray]
        dominance: float
        settings: tuple[int, int, int]
        grad: float

    best_solution = cur_settings
    for i_iter in range(max_iterations):  # noqa
        # Found a viable solution
        if dominance < max_dominance:
            break

        best_solution: Optional[Solution] = None
        # Iterate over the parameter space around the current best solution
        for new_settings in _search_domain(*cur_settings, min_partition_size, len(values)):  # type: ignore
            # We're searching greedily, so settings that have been tried are always worse.
            if new_settings in cache:
                continue
            try:
                new_bin, new_dom = _create_subsample(values, *new_settings)
            except ValueError:
                continue
            # Find the solution with the best gradient
            grad = (dominance - new_dom)/_diff_settings(cur_settings, new_settings)
            if new_dom >= dominance:
                cache.add(new_settings)
            if best_solution is None or best_solution.grad < grad:
                best_solution = Solution(new_bin, new_dom, new_settings, grad)
        if best_solution is None or best_solution.grad <= 0:
            raise ValueError(
                "Could not find solution satisfying dominance conditions for column"
                f" '{values.name}'."
            )
        dominance = best_solution.dominance
        cur_settings = best_solution.settings
        sub_values = best_solution.sub_values

    if dominance > max_dominance:
        raise ValueError(f"Failed to converge for column '{values.name}'")

    fit_log.add(privacy="Used microgregation with {best_solution[0]} partitions, "
                f" {best_solution[1]} lowest records removed, "
                f" {best_solution[2]} highest records removed, "
                f" and a partition size of {len(values) // best_solution[0]}.")

    # If the values are integer types, round the values to the nearest integer.
    if values.dtype in [pl.datatypes.Int64, pl.datatypes.Int32, pl.datatypes.Int32]:
        return pl.Series((np.array(sub_values) + 0.5).astype(np.int64))
    return pl.Series(sub_values)

def _search_domain(n_partitions: int, pre_remove: int, post_remove: int,
                   min_partition_size: int, series_size: int
                   ) -> Iterator[tuple[int, int, int]]:
    """Find all neighboring solutions around the current solution.

    Parameters
    ----------
    n_partitions
        Number of partitions of the current solution
    pre_remove
        Number of items to remove at the start (lowest values)
    post_remove
        Number of highest values to remove
    min_partition_size
        Minimum partition size (11 by default)
    series_size
        Size of the series for which the microaggregation is performed

    Yields
    ------
        A newly proposed solution, but not the same as the current one.

    """
    delta_part = max(3, n_partitions//5)
    for part in range(max(1, n_partitions-delta_part), n_partitions+delta_part+1):
        partition_size = series_size // part
        delta_remove = max(3, partition_size // 4)
        # Reject if partition size is too small
        if partition_size < min_partition_size:
            continue
        for new_pre_remove in range(pre_remove-delta_remove, pre_remove+delta_remove+1):
            if new_pre_remove < 0:  # Reject negative removal
                continue
            for new_post_remove in range(post_remove-delta_remove, post_remove+delta_remove+1):
                if new_post_remove < 0:  # Reject negative removel
                    continue
                if ((part, new_pre_remove, new_post_remove)  # Reject current solution
                        == (n_partitions, pre_remove, post_remove)):
                    continue
                yield part, new_pre_remove, new_post_remove

def _diff_settings(cur_settings: tuple, new_settings: tuple) -> int:
    """Get the distance between two settings. Used for the gradient."""
    diff = 0
    for i in range(len(cur_settings)):
        diff += abs(cur_settings[i]-new_settings[i])
    return diff
