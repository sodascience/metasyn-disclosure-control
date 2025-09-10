"""Module for disclosure control for string distributions."""

from metasyn.distribution.freetext import FreeTextFitter

from metasyncontrib.disclosure.base import disclosure_fitter


@disclosure_fitter()
class DisclosureFreetext(FreeTextFitter):
    """Disclosure implementation of freetext distribution.

    This implementation is the same as the original.
    """
