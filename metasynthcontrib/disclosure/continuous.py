"""Disclosure control implementations for continuous distributions."""

from metasynth.distribution.continuous import UniformDistribution
from metasynth.distribution.continuous import NormalDistribution, LogNormalDistribution
from metasynth.distribution.continuous import ExponentialDistribution
from metasynth.distribution.continuous import TruncatedNormalDistribution

from metasynthcontrib.disclosure.numerical import DisclosureNumerical
from metasynthcontrib.disclosure.base import metadist_disclosure


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
