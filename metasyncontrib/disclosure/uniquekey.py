"""Module with the CBS implementations for discrete variables."""

from __future__ import annotations

import polars as pl
from metasyn.distribution.base import VarLog
from metasyn.distribution.uniquekey import UniqueKeyDistribution, UniqueKeyFitter

from metasyncontrib.disclosure.base import disclosure_fitter
from metasyncontrib.disclosure.privacy import DisclosurePrivacy
from metasyncontrib.disclosure.utils import micro_aggregate


@disclosure_fitter()
class DisclosureUniqueKey(UniqueKeyFitter):
    """Implementation for unique key distribution.

    This implementation will for series longer than the partition size either
    a) be consecutive from 0 if the original series is consecutive or
    b) Find the minimum of the microaggregated series.
    """

    privacy: DisclosurePrivacy
    distribution: type[UniqueKeyDistribution]


    def _fit(self, series: pl.Series, fit_log) -> UniqueKeyDistribution:
        # Return the default distribution if there are not enough series to micro aggregate
        if len(series) < self.privacy.partition_size:
            fit_log.add(privacy="Using default key distribution without using the data, because the"
                        " number of items is smaller than the partition size.")
            return self.distribution.default_distribution()

        orig_dist = super()._fit(series, VarLog())
        if orig_dist.consecutive:
            fit_log.add(privacy="Detected that values are consecutive, using starting value of 0 "
                        "independent of actual data.")
            return self.distribution(0, True)
        sub_series = micro_aggregate(series, fit_log, self.privacy.partition_size,
                                     max_dominance=self.privacy.max_dominance)
        fit_log.add(method="Applying normal fit method on micro-aggregated data.")
        return super()._fit(sub_series, fit_log)

