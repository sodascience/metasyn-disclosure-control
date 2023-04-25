"""Disclosure classes for categorical variables."""

import polars as pl

from metasynth.distribution.categorical import MultinoulliDistribution
from metasynthcontrib.disclosure.base import BaseDisclosure


class DisclosureMultinoulli(BaseDisclosure, MultinoulliDistribution):
    """Disclosure variant for multinoulli distribution.

    It checks that all labels appear at least x times, and that
    there is no label with >90% of the counts.
    """

    @classmethod
    def _fit(cls, values: pl.Series, n_avg: int=11):
        dist = super(DisclosureMultinoulli, cls)._fit(values)
        labels = dist.labels[dist.probs >= n_avg/len(values)]
        probs = dist.probs[dist.probs >= n_avg/len(values)]
        if probs.max() >= 0.9:
            return cls.default_distribution()
        return cls(labels, probs)
