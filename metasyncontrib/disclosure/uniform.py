"""Disclosure control implementations for continuous distributions."""
from __future__ import annotations

import datetime as dt

import polars as pl
from metasyn.distribution.uniform import (
    ContinuousUniformFitter,
    DateTimeUniformDistribution,
    DateTimeUniformFitter,
    DateUniformDistribution,
    DateUniformFitter,
    DiscreteUniformFitter,
    TimeUniformDistribution,
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
class DisclosureDateTimeUniform(DateTimeUniformFitter):
    """Disclosure implementation for the datetime distribution."""

    privacy: DisclosurePrivacy
    distribution: type[DateTimeUniformDistribution]

    def _fit(self, series: pl.Series, fit_log) -> DateTimeUniformDistribution:
        sub_series = micro_aggregate(series, fit_log, self.privacy.partition_size,
                                     max_dominance=self.privacy.max_dominance)
        fit_log.add(method="Using the first and last time stamps in the aggregated series.")
        return self.distribution(sub_series.min(), sub_series.max(), self._get_precision(series))


@disclosure_fitter()
class DisclosureTimeUniform(TimeUniformFitter):
    """Disclosure implementation for the time distribution."""

    privacy: DisclosurePrivacy
    distribution: type[TimeUniformDistribution]

    def _fit(self, values: pl.Series, fit_log) -> TimeUniformDistribution:
        # Convert time to a datetime so that the microaggregation works
        today = dt.date(1970, 1, 1)
        dt_series = pl.Series([dt.datetime.combine(today, t) for t in values])
        dt_sub_series = micro_aggregate(dt_series, fit_log, self.privacy.partition_size,
                                        max_dominance=self.privacy.max_dominance)

        # Convert back into time
        sub_series = pl.Series([dt_val.time() for dt_val in dt_sub_series])
        fit_log.add(method="Using the first and last time values in the aggregated series.")
        return self.distribution(sub_series.min(), sub_series.max(),
                                 self._get_precision(values))


@disclosure_fitter()
class DisclosureDateUniform(DateUniformFitter):
    """Disclosure implementation for the date distribution."""

    privacy: DisclosurePrivacy
    distribution: type[DateUniformDistribution]

    def _fit(self, values: pl.Series, fit_log) -> DateUniformDistribution:
        # Convert dates to datetimes
        dt_series = pl.Series([dt.datetime.combine(d, dt.time(hour=12)) for d in values])
        dt_sub_series = micro_aggregate(dt_series, fit_log, self.privacy.partition_size,
                                        max_dominance=self.privacy.max_dominance)

        # Convert back into dates
        sub_series = pl.Series([dt_val.date() for dt_val in dt_sub_series])
        fit_log.add(method="Using the first and last dates in the aggregated series.")
        return self.distribution(sub_series.min(), sub_series.max())
