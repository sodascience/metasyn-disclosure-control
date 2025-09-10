
from metasyn.distribution.poisson import PoissonFitter

from metasyncontrib.disclosure.base import disclosure_fitter
from metasyncontrib.disclosure.numerical import DisclosureNumericalMixin


@disclosure_fitter()
class DisclosurePoisson(DisclosureNumericalMixin, PoissonFitter):
    """Disclosure implementation for Poisson distribution."""

