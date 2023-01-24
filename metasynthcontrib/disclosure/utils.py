"""Utilities for disclosure control."""

import datetime as dt

import numpy as np
import polars as pl
from numpy.core._exceptions import UFuncTypeError

# def get_disclosure_bounds(values, n_avg: int=10) -> Tuple[float, float]:
#     """Get disclosure control bounds."""
#     sorted_values = np.sort(values)
#     sum_low = 0
#     sum_high = 0
#     for i_slice in range(n_avg):
#         spliced_values = sorted_values[i_slice::n_avg]
#         delta_avg = (spliced_values[-1]-spliced_values[0])/(len(spliced_values)-1)
#         delta_avg /= n_avg
#         low_est = spliced_values[0] - (i_slice+0.5)*delta_avg
#         high_est = spliced_values[-1] + (n_avg-i_slice-0.5)*delta_avg
#         sum_low += low_est
#         sum_high += high_est
#     return sum_low/n_avg, sum_high/n_avg

#
# def get_lower_bound(values, n_avg: int=10):
#     alpha_one = values[1]-values[0]
#     alpha_two = values[2]-values[1]
#     alpha_zero = 2*alpha_one - alpha_two
#     delta = alpha_zero/n_avg
#     return values[0] - alpha_zero/2 - delta/2
#
#
# def get_upper_bound(sub_values, n_avg: int=10):
#     n = len(sub_values)
#     alpha_one = sub_values[n-1]-sub_values[n-2]
#     alpha_two = sub_values[n-2]-sub_values[n-3]
#     alpha_zero = 2*alpha_one - alpha_two
#     delta = alpha_zero/n_avg
#     return sub_values[n-1] + alpha_zero/2 + delta/2
#
#
# def get_bounds(values, n_avg: int=10):
#     return get_lower_bound(values, n_avg), get_upper_bound(values, n_avg)


def create_subsample(values, n_avg: int=11, pre_remove: int=0, post_remove: int=0):
    sorted_values = np.sort(values)
    sorted_values = sorted_values[pre_remove:len(values)-post_remove]
    n_values = len(sorted_values)

    n_blocks = n_values//n_avg
    if n_blocks <= 1:
        raise ValueError("Cannot find subsample with current settings.")
    min_block_size = n_values//n_blocks
    leftover = n_values - n_blocks*min_block_size
    if leftover == 1:
        sorted_values = np.delete(sorted_values, [n_values//2])
    if leftover > 1:
        base_skip = round(n_values/(leftover+1))
        skip_start = (n_values - base_skip*(leftover-1) + 1) // 2
        delete_values = skip_start + base_skip*np.arange(leftover)
        sorted_values = np.delete(sorted_values, delete_values)
    assert len(sorted_values) == n_blocks*min_block_size

    block_values = sorted_values.reshape(n_blocks, min_block_size)
    min_values = np.min(block_values, axis=1).reshape(-1, 1)
    max_values = np.max(block_values, axis=1).reshape(-1, 1)
    diff_values = (block_values - min_values)
    dominance = diff_values.max(axis=1)/diff_values.sum(axis=1)
    diff_values_reverse = (max_values - block_values)
    dominance_reverse = diff_values_reverse.max(axis=1)/diff_values_reverse.sum(axis=1)
    dominance = np.maximum(dominance, dominance_reverse)
    try:
        sub_values = block_values.mean(axis=1)
    except UFuncTypeError:
        return [dt.datetime.utcfromtimestamp(pl.Series(sub).mean()/1e6)
                for sub in block_values], np.max(dominance)
    return sub_values, np.max(dominance)


def micro_aggregate(values, min_bin: int=11):
    cur_settings = [min_bin, 0, 0]
    sub_values, dominance = create_subsample(values, *cur_settings)
    for _ in range(1000):
        if dominance < 0.5:
            break

        best_solution = None
        max_diff = cur_settings[0]//2
        for i_par in range(3):
            for add_par in range(1, max_diff):
                new_settings = [x if j_par != i_par else x+add_par
                                for j_par, x in enumerate(cur_settings)]
                try:
                    new_bin, new_dom = create_subsample(values, *new_settings)
                except ValueError:
                    continue
                grad = (dominance-new_dom) / add_par

                if best_solution is None or best_solution["grad"] < grad:
                    best_solution = {
                        "sub_values": new_bin,
                        "dominance": new_dom,
                        "settings": new_settings,
                        "grad": grad,
                    }
        if best_solution is None:
            raise ValueError("Could not find solutution satisfying dominance conditions.")
        dominance = best_solution["dominance"]
        cur_settings = best_solution["settings"]
        sub_values = best_solution["sub_values"]

    if values.dtype in [pl.datatypes.Int64, pl.datatypes.Int32, pl.datatypes.Int32]:
        return pl.Series((sub_values+0.5).astype(np.int64))
    return pl.Series(sub_values)
