from __future__ import annotations
from typing import Sequence, Tuple, Any
import datetime as dt

import numpy as np

from metasynth.distribution.datetime import UniformDateTimeDistribution
from metasynth.distribution.datetime import UniformTimeDistribution
from metasynth.distribution.datetime import UniformDateDistribution


def average_dt(values):
    return values[0] + np.mean(values - values[0])


def get_lower_bound(sorted_values, n_avg=10):
    sub_time_zero = average_dt(sorted_values[:n_avg])
    sub_time_one = average_dt(sorted_values[n_avg:2*n_avg])
    sub_time_two = average_dt(sorted_values[2*n_avg:3*n_avg])

    alpha_zero = 2*(sub_time_one-sub_time_zero) - (sub_time_two-sub_time_one)
    delta = alpha_zero/n_avg
    return sub_time_zero - alpha_zero/2 - delta/2


def get_upper_bound(sorted_values, n_avg=10):
    sub_time_zero = average_dt(sorted_values[-n_avg:])
    sub_time_one = average_dt(sorted_values[-2*n_avg:-n_avg])
    sub_time_two = average_dt(sorted_values[-3*n_avg:-2*n_avg])

    alpha_zero = 2*(sub_time_zero-sub_time_one) - (sub_time_one-sub_time_two)
    delta = alpha_zero/n_avg
    return sub_time_zero + alpha_zero/2 + delta/2


def get_dt_bounds(series, n_avg=10) -> Tuple[Any, Any]:
    sorted_values = np.sort(series)
    return get_lower_bound(sorted_values, n_avg), get_upper_bound(sorted_values, n_avg)


class DisclosureDateTimeDistribution(UniformDateTimeDistribution):
    @classmethod
    def _fit(cls, series: Sequence, n_avg: int=10) -> DisclosureDateTimeDistribution:
        return cls(*get_dt_bounds(series, n_avg), cls._get_precision(series))


class DisclosureTimeDistribution(UniformTimeDistribution):
    @classmethod
    def _fit(cls, series: Sequence, n_avg: int=10):
        base_date = dt.date.fromisoformat("2020-01-01")
        sorted_time = np.sort(series)
        sorted_dt = np.array([dt.datetime.combine(base_date, x) for x in sorted_time])
        start, end = get_dt_bounds(sorted_dt, n_avg=n_avg)
        if start.date() < base_date:
            start_time = dt.time.fromisoformat("00:00:00.000000")
        else:
            start_time = start.time()
        if end.date() > base_date:
            end_time = dt.time.fromisoformat("23:59:59.999999")
        else:
            end_time = end.time()
        start_time, end_time
        assert start_time < end_time
        return cls(start_time, end_time, cls._get_precision(series))


class DisclosureDateDistribution(UniformDateDistribution):
    @classmethod
    def _fit(cls, series: Sequence, n_avg: int=10) -> DisclosureDateDistribution:
        return cls(*get_dt_bounds(series, n_avg))
