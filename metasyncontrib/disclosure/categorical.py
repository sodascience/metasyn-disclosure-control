"""Disclosure classes for categorical variables."""

import polars as pl

from metasyn.distribution.categorical import MultinoulliDistribution
from metasyncontrib.disclosure.base import metadist_disclosure


@metadist_disclosure()
class DisclosureMultinoulli(MultinoulliDistribution):
    """Disclosure variant for multinoulli distribution.

    It checks that all labels appear at least x times, and that
    there is no label with >90% of the counts.
    """

    @classmethod
    def _fit(cls, values: pl.Series, n_avg: int = 11):
        dist = super(DisclosureMultinoulli, cls)._fit(values)
        labels = dist.labels[dist.probs >= n_avg/len(values)]
        probs = dist.probs[dist.probs >= n_avg/len(values)]
        if len(probs) == 0 or probs.max() >= 0.9:
            return cls.default_distribution()
        probs /= probs.sum()
        return cls(labels, probs)
