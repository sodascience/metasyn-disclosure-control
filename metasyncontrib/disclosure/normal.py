"""Disclosure control implementations for continuous distributions."""

from metasyn.distribution.normal import (
    DiscreteNormalFitter,
    DiscreteTruncatedNormalFitter,
    LogNormalFitter,
    ContinuousNormalFitter,
    ContinuousTruncatedNormalFitter,
)

from metasyncontrib.disclosure.base import disclosure_fitter
from metasyncontrib.disclosure.numerical import DisclosureNumericalMixin


@disclosure_fitter()
class DisclosureNormal(DisclosureNumericalMixin, ContinuousNormalFitter):
    """Disclosure normal distribution."""


@disclosure_fitter()
class DisclosureLogNormal(DisclosureNumericalMixin, LogNormalFitter):
    """Disclosure log-normal distribution."""


@disclosure_fitter()
class DisclosureTruncatedNormal(DisclosureNumericalMixin, ContinuousTruncatedNormalFitter):
    """Truncated normal distribution implementation."""


@disclosure_fitter()
class DisclosureDiscreteNormal(DisclosureNumericalMixin, DiscreteNormalFitter):
    """Implementation for discrete uniform distribution."""


@disclosure_fitter()
class DisclosureDiscreteTruncatedNormal(
    DisclosureNumericalMixin, DiscreteTruncatedNormalFitter
):
    """Implementation for discrete uniform distribution."""
