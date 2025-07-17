"""Disclosure classes for categorical variables."""

from __future__ import annotations

import polars as pl
from metasyn.distribution.categorical import MultinoulliDistribution
from metasyn.var import MetaVar

from metasyncontrib.disclosure.base import metadist_disclosure
from metasyncontrib.disclosure.privacy import DisclosurePrivacy


@metadist_disclosure()
class DisclosureMultinoulli(MultinoulliDistribution):
    """Disclosure variant for multinoulli distribution.

    It checks that all labels appear at least partition_size times, and that
    there is no label with >90% of the counts.
    """

    @classmethod
    def _fit(cls, values: pl.Series, privacy: DisclosurePrivacy):
        dist = super()._fit(values)
        # Remove labels with counts < partition_size
        labels = dist.labels[dist.probs >= privacy.partition_size / len(values)]
        probs = dist.probs[dist.probs >= privacy.partition_size / len(values)]

        # If no more categories are present or the dominance criterion is not satisfied return
        # the default distribution.
        if len(probs) == 0 or probs.max() >= privacy.group_disclosure_threshold:
            if MetaVar.get_var_type(values) == "discrete":
                return cls([77777, 88888, 99999], [0.1, 0.2, 0.7])  # type: ignore
            return cls.default_distribution()
        probs /= probs.sum()
        return cls(labels, probs)

    @classmethod
    def default_distribution(cls):  # noqa: D102
        return cls(["A_REDACTED", "B_REDACTED", "C_REDACTED"], [0.1, 0.3, 0.6])
