"""Disclosure control implementations for continuous distributions."""

from metasyn.distribution.continuous import UniformDistribution
from metasyn.distribution.continuous import NormalDistribution, LogNormalDistribution
from metasyn.distribution.continuous import ExponentialDistribution
from metasyn.distribution.continuous import TruncatedNormalDistribution

from metasyncontrib.disclosure.numerical import DisclosureNumerical
from metasyncontrib.disclosure.base import metadist_disclosure


@metadist_disclosure()
class DisclosureUniform(DisclosureNumerical, UniformDistribution):
    """Uniform distribution implementation."""


@metadist_disclosure()
class DisclosureTruncatedNormal(DisclosureNumerical, TruncatedNormalDistribution):
    """Truncated normal distribution implementation."""


@metadist_disclosure()
class DisclosureNormal(DisclosureNumerical, NormalDistribution):
    """Disclosure normal distribution."""


@metadist_disclosure()
class DisclosureLogNormal(DisclosureNumerical, LogNormalDistribution):
    """Disclosure log-normal distribution."""


@metadist_disclosure()
class DisclosureExponential(DisclosureNumerical, ExponentialDistribution):
    """Disclosure exponential distribution."""
