"""Disclosure control implementations for continuous distributions."""

from metasynth.distribution.continuous import UniformDistribution
from metasynth.distribution.continuous import NormalDistribution, LogNormalDistribution
from metasynth.distribution.continuous import ExponentialDistribution
from metasynth.distribution.continuous import TruncatedNormalDistribution

from metasynthcontrib.disclosure.numerical import DisclosureNumerical


class DisclosureUniform(UniformDistribution, DisclosureNumerical):
    """Uniform distribution implementation."""


class DisclosureTruncatedNormal(TruncatedNormalDistribution, DisclosureNumerical):
    """Truncated normal distribution implementation."""


class DisclosureNormal(NormalDistribution, DisclosureNumerical):
    """Disclosure normal distribution."""


class DisclosureLogNormal(LogNormalDistribution, DisclosureNumerical):
    """Disclosure log-normal distribution."""


class DisclosureExponential(ExponentialDistribution, DisclosureNumerical):
    """Disclosure exponential distribution."""
