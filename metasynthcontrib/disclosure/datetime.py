from __future__ import annotations
from typing import Sequence
import datetime as dt

import polars as pl

from metasynth.distribution.datetime import UniformDateTimeDistribution
from metasynth.distribution.datetime import UniformTimeDistribution
from metasynth.distribution.datetime import UniformDateDistribution
from metasynthcontrib.disclosure.base import BaseDisclosureDistribution
from metasynthcontrib.disclosure.utils import micro_aggregate


# def average_dt(values):
#     return values[0] + (values - values[0]).mean()
#
#
# def get_lower_bound(sorted_values, n_avg=10):
#     sub_time_zero = average_dt(sorted_values[:n_avg])
#     sub_time_one = average_dt(sorted_values[n_avg:2*n_avg])
#     sub_time_two = average_dt(sorted_values[2*n_avg:3*n_avg])
#
#     alpha_zero = 2*(sub_time_one-sub_time_zero) - (sub_time_two-sub_time_one)
#     delta = alpha_zero/n_avg
#     return sub_time_zero - alpha_zero/2 - delta/2
#
#
# def get_upper_bound(sorted_values, n_avg=10):
#     sub_time_zero = average_dt(sorted_values[-n_avg:])
#     sub_time_one = average_dt(sorted_values[-2*n_avg:-n_avg])
#     sub_time_two = average_dt(sorted_values[-3*n_avg:-2*n_avg])
#
#     alpha_zero = 2*(sub_time_zero-sub_time_one) - (sub_time_one-sub_time_two)
#     delta = alpha_zero/n_avg
#     return sub_time_zero + alpha_zero/2 + delta/2
#
#
# def get_dt_bounds(series, n_avg=10) -> Tuple[Any, Any]:
#     sorted_values = np.sort(series)
#     return get_lower_bound(sorted_values, n_avg), get_upper_bound(sorted_values, n_avg)


class DisclosureDateTimeDistribution(BaseDisclosureDistribution, UniformDateTimeDistribution):
    @classmethod
    def _fit(cls, series: Sequence, n_avg: int=10) -> DisclosureDateTimeDistribution:
        sub_series = micro_aggregate(series, n_avg)
        return cls(sub_series.min(), sub_series.max(), cls._get_precision(series))


class DisclosureTimeDistribution(UniformTimeDistribution):
    @classmethod
    def _fit(cls, series: Sequence, n_avg: int=10):
        today = dt.datetime.today()
        dt_series = pl.Series([dt.datetime.combine(today, t) for t in series])
        dt_sub_series = micro_aggregate(dt_series, n_avg)
        sub_series = pl.Series([dt_val.time() for dt_val in dt_sub_series])
        return cls(sub_series.min(), sub_series.max(), cls._get_precision(series))


class DisclosureDateDistribution(UniformDateDistribution):
    @classmethod
    def _fit(cls, series: Sequence, n_avg: int=10) -> DisclosureDateDistribution:
        dt_series = pl.Series([dt.datetime.combine(d, dt.time(hour=12)) for d in series])
        dt_sub_series = micro_aggregate(dt_series, n_avg)
        sub_series = pl.Series([dt_val.date() for dt_val in dt_sub_series])
        return cls(sub_series.min(), sub_series.max())

        # min_dt, max_dt = get_dt_bounds(series, n_avg)
        # return cls(convert_numpy_datetime(min_dt).date(), convert_numpy_datetime(max_dt).date())
