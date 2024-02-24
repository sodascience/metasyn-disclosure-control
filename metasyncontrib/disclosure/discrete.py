"""Module with the CBS implementations for discrete variables."""

from __future__ import annotations

import polars as pl
from metasyn.distribution.discrete import (
    DiscreteNormalDistribution,
    DiscreteTruncatedNormalDistribution,
    DiscreteUniformDistribution,
    PoissonDistribution,
    UniqueKeyDistribution,
)

from metasyncontrib.disclosure.base import metadist_disclosure
from metasyncontrib.disclosure.numerical import DisclosureNumericalMixin
from metasyncontrib.disclosure.utils import micro_aggregate


@metadist_disclosure()
class DisclosureDiscreteUniform(DisclosureNumericalMixin, DiscreteUniformDistribution):
    """Implementation for discrete uniform distribution."""


@metadist_disclosure()
class DisclosureDiscreteNormal(DisclosureNumericalMixin, DiscreteNormalDistribution):
    """Implementation for discrete uniform distribution."""


@metadist_disclosure()
class DisclosureDiscreteTruncatedNormal(
    DisclosureNumericalMixin, DiscreteTruncatedNormalDistribution
):
    """Implementation for discrete uniform distribution."""


@metadist_disclosure()
class DisclosurePoisson(DisclosureNumericalMixin, PoissonDistribution):
    """Disclosure implementation for Poisson distribution."""


@metadist_disclosure()
class DisclosureUniqueKey(UniqueKeyDistribution):
    """Implementation for unique key distribution."""

    @classmethod
    def _fit(cls, values: pl.Series, n_avg: int = 11):
        orig_dist = super()._fit(values)
        if orig_dist.consecutive:
            return cls(0, True)
        sub_values = micro_aggregate(values, n_avg)
        return super()._fit(sub_values)
