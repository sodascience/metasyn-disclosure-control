"""Disclosure control implementations for continuous distributions."""

from metasyn.distribution.continuous import (
    ExponentialDistribution,
    LogNormalDistribution,
    NormalDistribution,
    TruncatedNormalDistribution,
    UniformDistribution,
)

from metasyncontrib.disclosure.base import metadist_disclosure
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
