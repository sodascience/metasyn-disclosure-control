"""Module for disclosure-controlled NA distribution."""
from __future__ import annotations

from metasyn.distribution.na import NAFitter

from metasyncontrib.disclosure.base import disclosure_fitter


@disclosure_fitter()
class DisclosureNA(NAFitter):
    """Disclosure version of NA distribution."""
