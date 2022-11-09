"""Utilities for disclosure control."""

import numpy as np
import polars as pl

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

def get_lower_bound(values, n_avg: int=10):
    alpha_one = values[1]-values[0]
    alpha_two = values[2]-values[1]
    alpha_zero = 2*alpha_one - alpha_two
    delta = alpha_zero/n_avg
    return values[0] - alpha_zero/2 - delta/2


def get_upper_bound(sub_values, n_avg: int=10):
    n = len(sub_values)
    alpha_one = sub_values[n-1]-sub_values[n-2]
    alpha_two = sub_values[n-2]-sub_values[n-3]
    alpha_zero = 2*alpha_one - alpha_two
    delta = alpha_zero/n_avg
    return sub_values[n-1] + alpha_zero/2 + delta/2


def get_bounds(values, n_avg: int=10):
    return get_lower_bound(values, n_avg), get_upper_bound(values, n_avg)


def subsample(values, n_avg: int=10):
    sorted_values = np.sort(values)
    n_values = len(values)
    n_blocks = n_values//n_avg
    min_block_size = n_values//n_blocks
    leftover = n_values - n_blocks*min_block_size
    remove_points = np.zeros(n_blocks)
    remove_points[:leftover] = 1
    np.random.shuffle(remove_points)
    remove_index = np.where(remove_points)[0] + np.random.randint(0, min_block_size, size=leftover)
    sorted_values = sorted_values[np.delete(np.arange(n_values), remove_index)]
    sub_values = sorted_values.reshape(n_blocks, min_block_size).mean(axis=1)
    if values.dtype in [pl.datatypes.Int64, pl.datatypes.Int32, pl.datatypes.Int32]:
        return (sub_values+0.5).astype(np.int64)
    return sub_values
