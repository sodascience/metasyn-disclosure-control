"""Disclosure control implementations for continuous distributions."""

from metasynth.distribution.continuous import UniformDistribution
from metasynth.distribution.continuous import TruncatedNormalDistribution

from metasynthcontrib.disclosure.utils import get_disclosure_bounds


class DisclosureUniform(UniformDistribution):
    """Uniform distribution implementation."""

    @classmethod
    def _fit(cls, values, n_avg=10):
        return cls(*get_disclosure_bounds(values, n_avg))


class DisclosureTruncatedNormal(TruncatedNormalDistribution):
    """Truncated normal distribution implementation."""

    @classmethod
    def _fit(cls, values, n_avg=10):
        cls._fit_with_bounds(values, *get_disclosure_bounds(values, n_avg=n_avg))
