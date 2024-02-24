"""Module for disclosure-controlled NA distribution."""
from __future__ import annotations

from metasyn.distribution.na import NADistribution

from metasyncontrib.disclosure.base import metadist_disclosure


@metadist_disclosure()
class DisclosureNA(NADistribution):
    """Disclosure version of NA distribution."""
