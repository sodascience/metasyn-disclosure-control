"""Disclosure control implementations for continuous distributions."""

from metasynth.distribution.continuous import UniformDistribution,\
    NormalDistribution, LogNormalDistribution, ExponentialDistribution
from metasynth.distribution.continuous import TruncatedNormalDistribution

from metasynthcontrib.disclosure.utils import get_bounds
from metasynthcontrib.disclosure.numerical import DisclosureNumerical


class DisclosureUniform(DisclosureNumerical, UniformDistribution):
    """Uniform distribution implementation."""

    @classmethod
    def _fit(cls, values, n_avg=10):
        return cls(*get_bounds(values, n_avg))


class DisclosureTruncatedNormal(DisclosureNumerical, TruncatedNormalDistribution):
    """Truncated normal distribution implementation."""

    @classmethod
    def _fit(cls, values, n_avg=10):
        return cls._fit_with_bounds(values, *get_bounds(values, n_avg=n_avg))


class DisclosureNormalDistribution(DisclosureNumerical, NormalDistribution):
    pass


class DisclosureLogNormalDistribution(DisclosureNumerical, LogNormalDistribution):
    pass


class DisclosureExponentialDistribution(DisclosureNumerical, ExponentialDistribution):
    pass
