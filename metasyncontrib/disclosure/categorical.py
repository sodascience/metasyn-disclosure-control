"""Disclosure classes for categorical variables."""

from __future__ import annotations

import polars as pl
from metasyn.distribution.categorical import MultinoulliDistribution
from metasyn.var import MetaVar

from metasyncontrib.disclosure.base import metadist_disclosure


@metadist_disclosure()
class DisclosureMultinoulli(MultinoulliDistribution):
    """Disclosure variant for multinoulli distribution.

    It checks that all labels appear at least n_avg times, and that
    there is no label with >90% of the counts.
    """

    @classmethod
    def _fit(cls, values: pl.Series, n_avg: int = 11):
        dist = super()._fit(values)
        labels = dist.labels[dist.probs >= n_avg / len(values)]
        probs = dist.probs[dist.probs >= n_avg / len(values)]
        if len(probs) == 0 or probs.max() >= 0.9:
            if MetaVar.get_var_type(values) == "discrete":
                return cls([1, 2, 3], [0.1, 0.2, 0.7])
            return cls.default_distribution()
        probs /= probs.sum()
        return cls(labels, probs)
