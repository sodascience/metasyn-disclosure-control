"""Module for disclosure control for string distributions."""

from metasynth.distribution.faker import FakerDistribution
from metasynthcontrib.disclosure.base import BaseDisclosureDistribution


class DisclosureFaker(FakerDistribution, BaseDisclosureDistribution):
    """Faker distribution for disclosure control."""
