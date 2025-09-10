"""Module for disclosure control for string distributions."""

from metasyn.distribution.faker import (
    FakerFitter,
    UniqueFakerFitter,
)

from metasyncontrib.disclosure.base import disclosure_fitter


@disclosure_fitter()
class DisclosureFaker(FakerFitter):
    """Faker distribution for disclosure control."""


@disclosure_fitter()
class DisclosureUniqueFaker(UniqueFakerFitter):
    """Faker distribution for disclosure control that produces unique values."""
