"""Module with the CBS implementations for discrete variables."""

from __future__ import annotations

import polars as pl
from metasyn.distribution.discrete import (
    DiscreteConstantDistribution,
    DiscreteNormalDistribution,
    DiscreteTruncatedNormalDistribution,
    DiscreteUniformDistribution,
    PoissonDistribution,
    UniqueKeyDistribution,
)

from metasyncontrib.disclosure.base import DisclosureConstantMixin, metadist_disclosure
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
    """Implementation for unique key distribution.

    This implementation will for series longer than the partition size either
    a) be consecutive from 0 if the original series is consecutive or
    b) Find the minimum of the microaggregated series.
    """

    @classmethod
    def _fit(cls, values: pl.Series, partition_size: int = 11, max_dominance: float = 0.5):
        # Return the default distribution if there are not enough values to micro aggregate
        if len(values) < partition_size:
            return cls.default_distribution()

        orig_dist = super()._fit(values)
        if orig_dist.consecutive:
            return cls(0, True)
        sub_values = micro_aggregate(values, partition_size, max_dominance=max_dominance)
        return super()._fit(sub_values)


@metadist_disclosure()
class DisclosureDiscreteConstant(DisclosureConstantMixin, DiscreteConstantDistribution):
    """Disclosure controlled DiscreteConstantDistribution."""

    @classmethod
    def default_distribution(cls):  # noqa: D102
        return cls(99999)
