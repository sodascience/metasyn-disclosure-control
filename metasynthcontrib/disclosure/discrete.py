"""Module with the CBS implementations for discrete variables."""

from __future__ import annotations

from typing import Sequence

import numpy as np

from metasynth.distribution.discrete import DiscreteUniformDistribution
from metasynth.distribution.discrete import PoissonDistribution
from metasynth.distribution.discrete import UniqueKeyDistribution

from metasynthcontrib.disclosure.utils import get_bounds
from metasynthcontrib.disclosure.numerical import DisclosureNumerical


class DisclosureDiscreteUniform(DisclosureNumerical, DiscreteUniformDistribution):
    """Implementation for discrete uniform distribution."""

    @classmethod
    def _fit(cls, values, n_avg: int=10):
        low, high = get_bounds(values, n_avg)
        return cls(round(low), round(high))


class DisclosureUniqueKey(UniqueKeyDistribution):
    """Implementation for unique key distribution."""

    @classmethod
    def _fit(cls, values, n_avg: int=10):
        orig_dist = super()._fit(values)
        if orig_dist.consecutive == 1:
            return cls(np.random.randint(2*n_avg+1)-n_avg, orig_dist.consecutive)
        uniform_dist = DisclosureDiscreteUniform.fit(values, n_avg=n_avg)
        return cls(uniform_dist.low, orig_dist.consecutive)  # type: ignore


class DisclosurePoissonDistribution(DisclosureNumerical, PoissonDistribution):
    @classmethod
    def _fit(cls, values: Sequence, n_avg: int=10) -> DisclosurePoissonDistribution:
        return super(DisclosurePoissonDistribution, cls)._fit(values)
