"""Disclosure control implementations for continuous distributions."""
from __future__ import annotations

import datetime as dt

import polars as pl
from metasyn.distribution.uniform import (
    ContinuousUniformFitter,
    DateTimeUniformFitter,
    DateUniformFitter,
    DiscreteUniformFitter,
    TimeUniformFitter,
)

from metasyncontrib.disclosure.base import disclosure_fitter
from metasyncontrib.disclosure.numerical import DisclosureNumericalMixin
from metasyncontrib.disclosure.privacy import DisclosurePrivacy
from metasyncontrib.disclosure.utils import micro_aggregate


@disclosure_fitter()
class DisclosureContinuousUniform(DisclosureNumericalMixin, ContinuousUniformFitter):
    """Uniform distribution implementation."""


@disclosure_fitter()
class DisclosureDiscreteUniform(DisclosureNumericalMixin, DiscreteUniformFitter):
    """Implementation for discrete uniform distribution."""


@disclosure_fitter()
class DisclosureDateTime(DateTimeUniformFitter):
    """Disclosure implementation for the datetime distribution."""

    privacy: DisclosurePrivacy

    def _fit(self, series: pl.Series) -> DisclosureDateTime:
        sub_series = micro_aggregate(series, self.privacy.partition_size,
                                     max_dominance=self.privacy.max_dominance)
        return self.distribution(sub_series.min(), sub_series.max(), self._get_precision(series))


@disclosure_fitter()
class DisclosureTime(TimeUniformFitter):
    """Disclosure implementation for the time distribution."""

    privacy: DisclosurePrivacy

    def _fit(self, values: pl.Series):
        # Convert time to a datetime so that the microaggregation works
        today = dt.date(1970, 1, 1)
        dt_series = pl.Series([dt.datetime.combine(today, t) for t in values])
        dt_sub_series = micro_aggregate(dt_series, self.privacy.partition_size,
                                        max_dominance=self.privacy.max_dominance)

        # Convert back into time
        sub_series = pl.Series([dt_val.time() for dt_val in dt_sub_series])
        return self.distribution(sub_series.min(), sub_series.max(),
                                 self._get_precision(values))


@disclosure_fitter()
class DisclosureDate(DateUniformFitter):
    """Disclosure implementation for the date distribution."""

    privacy: DisclosurePrivacy

    def _fit(self, values: pl.Series) -> DisclosureDate:
        # Convert dates to datetimes
        dt_series = pl.Series([dt.datetime.combine(d, dt.time(hour=12)) for d in values])
        dt_sub_series = micro_aggregate(dt_series, self.privacy.partition_size,
                                        max_dominance=self.privacy.max_dominance)

        # Convert back into dates
        sub_series = pl.Series([dt_val.date() for dt_val in dt_sub_series])
        return self.distribution(sub_series.min(), sub_series.max())
