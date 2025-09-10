"""Module with the CBS implementations for discrete variables."""

from __future__ import annotations

import polars as pl
from metasyn.distribution.uniquekey import UniqueKeyFitter

from metasyncontrib.disclosure.base import disclosure_fitter
from metasyncontrib.disclosure.utils import micro_aggregate


@disclosure_fitter()
class DisclosureUniqueKey(UniqueKeyFitter):
    """Implementation for unique key distribution.

    This implementation will for series longer than the partition size either
    a) be consecutive from 0 if the original series is consecutive or
    b) Find the minimum of the microaggregated series.
    """

    def _fit(self, series: pl.Series):
        # Return the default distribution if there are not enough series to micro aggregate
        if len(series) < self.privacy.partition_size:
            return self.distribution.default_distribution()

        orig_dist = super()._fit(series)
        if orig_dist.consecutive:
            return self.distribution(0, True)
        sub_series = micro_aggregate(series, self.privacy.partition_size,
                                     max_dominance=self.privacy.max_dominance)
        return super()._fit(sub_series)

