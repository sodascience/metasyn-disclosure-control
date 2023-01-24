"""Module with the CBS implementations for discrete variables."""

from __future__ import annotations

import numpy as np
import polars as pl

from metasynth.distribution.discrete import DiscreteUniformDistribution
from metasynth.distribution.discrete import PoissonDistribution
from metasynth.distribution.discrete import UniqueKeyDistribution

from metasynthcontrib.disclosure.numerical import DisclosureNumerical


class DisclosureDiscreteUniform(DiscreteUniformDistribution, DisclosureNumerical):
    """Implementation for discrete uniform distribution."""


class DisclosureUniqueKey(UniqueKeyDistribution):
    """Implementation for unique key distribution."""

    @classmethod
    def _fit(cls, values: pl.Series, n_avg: int=10):
        orig_dist = super()._fit(values)
        if orig_dist.consecutive == 1:
            return cls(np.random.randint(2*n_avg+1)-n_avg, orig_dist.consecutive)
        uniform_dist = DisclosureDiscreteUniform.fit(values, n_avg=n_avg)
        return cls(uniform_dist.low, orig_dist.consecutive)  # type: ignore


class DisclosurePoisson(PoissonDistribution, DisclosureNumerical):
    """Disclosure implementation for Poisson distribution."""
