"""Module for disclosure control for string distributions."""

from metasynth.distribution.faker import FakerDistribution
from metasynthcontrib.disclosure.base import BaseDisclosureDistribution


class DisclosureFakerDistribution(BaseDisclosureDistribution, FakerDistribution):
    """Faker distribution for disclosure control."""
