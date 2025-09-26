"""Disclosure control implementations for continuous distributions."""

from metasyn.distribution.exponential import ExponentialFitter

from metasyncontrib.disclosure.base import disclosure_fitter
from metasyncontrib.disclosure.numerical import DisclosureNumericalMixin


@disclosure_fitter()
class DisclosureExponential(DisclosureNumericalMixin, ExponentialFitter):
    """Disclosure exponential distribution."""
