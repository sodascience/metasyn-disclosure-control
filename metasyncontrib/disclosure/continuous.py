"""Disclosure control implementations for continuous distributions."""

from metasyn.distribution.continuous import (
    ConstantDistribution,
    ExponentialDistribution,
    LogNormalDistribution,
    NormalDistribution,
    TruncatedNormalDistribution,
    UniformDistribution,
)

from metasyncontrib.disclosure.base import DisclosureConstantMixin, metadist_disclosure
from metasyncontrib.disclosure.numerical import DisclosureNumericalMixin


@metadist_disclosure()
class DisclosureUniform(DisclosureNumericalMixin, UniformDistribution):
    """Uniform distribution implementation."""


@metadist_disclosure()
class DisclosureNormal(DisclosureNumericalMixin, NormalDistribution):
    """Disclosure normal distribution."""


@metadist_disclosure()
class DisclosureLogNormal(DisclosureNumericalMixin, LogNormalDistribution):
    """Disclosure log-normal distribution."""


@metadist_disclosure()
class DisclosureTruncatedNormal(DisclosureNumericalMixin, TruncatedNormalDistribution):
    """Truncated normal distribution implementation."""


@metadist_disclosure()
class DisclosureExponential(DisclosureNumericalMixin, ExponentialDistribution):
    """Disclosure exponential distribution."""


@metadist_disclosure()
class DisclosureConstant(DisclosureConstantMixin, ConstantDistribution):
    """Disclosure controlled ConstantDistribution."""

    @classmethod
    def default_distribution(cls):  # noqa: D102
        return cls(99999.9)
