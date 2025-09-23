"""Disclosure classes for categorical variables."""

from __future__ import annotations

import polars as pl
from metasyn.distribution.categorical import MultinoulliFitter
from metasyn.util import get_var_type

from metasyncontrib.disclosure.base import disclosure_fitter
from metasyncontrib.disclosure.privacy import DisclosurePrivacy

@disclosure_fitter()
class DisclosureMultinoulli(MultinoulliFitter):
    """Disclosure variant for multinoulli distribution.

    It checks that all labels appear at least partition_size times, and that
    there is no label with >90% of the counts.
    """

    privacy: DisclosurePrivacy

    def _fit(self, series: pl.Series):
        dist = super()._fit(series)
        # Remove labels with counts < partition_size
        labels = dist.labels[dist.probs >= self.privacy.partition_size / len(series)]
        probs = dist.probs[dist.probs >= self.privacy.partition_size / len(series)]

        # If no more categories are present or the dominance criterion is not satisfied return
        # the default distribution.
        if len(probs) == 0 or probs.max() >= self.privacy.group_disclosure_threshold:
            return self.default_distribution()
        probs /= probs.sum()
        return self.distribution(labels, probs)

    def default_distribution(self, series):  # noqa: D102
        if get_var_type(series) == "discrete":
            return self.distribution([77777, 88888, 99999], [0.1, 0.2, 0.7])  # type: ignore
        return self.distribution(["A_REDACTED", "B_REDACTED", "C_REDACTED"], [0.1, 0.3, 0.6])

