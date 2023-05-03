"""Module with the CBS implementations for discrete variables."""

from __future__ import annotations

import polars as pl

from metasynth.distribution.discrete import DiscreteUniformDistribution
from metasynth.distribution.discrete import PoissonDistribution
from metasynth.distribution.discrete import UniqueKeyDistribution

from metasynthcontrib.disclosure.numerical import DisclosureNumerical
from metasynthcontrib.disclosure.utils import micro_aggregate
from metasynthcontrib.disclosure.base import BaseDisclosure


class DisclosureDiscreteUniform(DisclosureNumerical, DiscreteUniformDistribution):
    """Implementation for discrete uniform distribution."""


class DisclosureUniqueKey(BaseDisclosure, UniqueKeyDistribution):
    """Implementation for unique key distribution."""

    @classmethod
    def _fit(cls, values: pl.Series, n_avg: int=11):
        orig_dist = super()._fit(values)
        if orig_dist.consecutive == 1:
            return cls(0, 1)
        sub_values = micro_aggregate(values, n_avg)
        return super()._fit(sub_values)


class DisclosurePoisson(DisclosureNumerical, PoissonDistribution):
    """Disclosure implementation for Poisson distribution."""
