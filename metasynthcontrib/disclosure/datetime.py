"""Disclosure classes for date/time/datetime distributions."""

from __future__ import annotations
import datetime as dt

import polars as pl

from metasynth.distribution.datetime import UniformDateTimeDistribution
from metasynth.distribution.datetime import UniformTimeDistribution
from metasynth.distribution.datetime import UniformDateDistribution
# from metasynthcontrib.disclosure.base import BaseDisclosureDistribution
from metasynthcontrib.disclosure.utils import micro_aggregate


class DisclosureDateTime(UniformDateTimeDistribution):
    """Disclosure implementation for the datetime distribution."""

    @classmethod
    def _fit(cls, values: pl.Series, n_avg: int=11) -> DisclosureDateTime:
        sub_series = micro_aggregate(values, n_avg)
        return cls(sub_series.min(), sub_series.max(), cls._get_precision(values))


class DisclosureTime(UniformTimeDistribution):
    """Disclosure implementation for the time distribution."""

    @classmethod
    def _fit(cls, values: pl.Series, n_avg: int=11):
        # Convert time to a datetime so that the microaggregation works
        today = dt.date(1970, 1, 1)
        dt_series = pl.Series([dt.datetime.combine(today, t) for t in values])
        dt_sub_series = micro_aggregate(dt_series, n_avg)

        # Convert back into time
        sub_series = pl.Series([dt_val.time() for dt_val in dt_sub_series])
        return cls(sub_series.min(), sub_series.max(), cls._get_precision(values))


class DisclosureDate(UniformDateDistribution):
    """Disclosure implementation for the date distribution."""

    @classmethod
    def _fit(cls, values: pl.Series, n_avg: int=11) -> DisclosureDate:
        # Convert dates to datetimes
        dt_series = pl.Series([dt.datetime.combine(d, dt.time(hour=12)) for d in values])
        dt_sub_series = micro_aggregate(dt_series, n_avg)

        # Convert back into dates
        sub_series = pl.Series([dt_val.date() for dt_val in dt_sub_series])
        return cls(sub_series.min(), sub_series.max())
