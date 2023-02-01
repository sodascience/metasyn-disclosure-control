"""Module for disclosure control for string distributions."""

from metasynth.distribution.faker import FakerDistribution
from metasynthcontrib.disclosure.base import BaseDisclosureDistribution


class DisclosureFaker(BaseDisclosureDistribution, FakerDistribution):
    """Faker distribution for disclosure control."""
    @classmethod
    def _fit(cls, values, n_avg=11):
        return super(DisclosureFaker, cls)._fit(values)
