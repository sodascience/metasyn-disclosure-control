"""Disclosure control implementations for continuous distributions."""

from metasynth.distribution.continuous import UniformDistribution
from metasynth.distribution.continuous import NormalDistribution, LogNormalDistribution
from metasynth.distribution.continuous import ExponentialDistribution
from metasynth.distribution.continuous import TruncatedNormalDistribution

from metasynthcontrib.disclosure.numerical import DisclosureNumerical


class DisclosureUniform(DisclosureNumerical, UniformDistribution):
    """Uniform distribution implementation."""


class DisclosureTruncatedNormal(DisclosureNumerical, TruncatedNormalDistribution):
    """Truncated normal distribution implementation."""


class DisclosureNormal(DisclosureNumerical, NormalDistribution):
    """Disclosure normal distribution."""


class DisclosureLogNormal(DisclosureNumerical, LogNormalDistribution):
    """Disclosure log-normal distribution."""


class DisclosureExponential(DisclosureNumerical, ExponentialDistribution):
    """Disclosure exponential distribution."""
