"""Module for disclosure control for string distributions."""

from metasynth.distribution.faker import FakerDistribution
# from metasynthcontrib.disclosure.base import BaseDisclosureDistribution


class DisclosureFaker(FakerDistribution):
    """Faker distribution for disclosure control."""

    @classmethod
    def _fit(cls, values,
             faker_type: str="city",
             locale: str="en_US", n_avg=11):  # pylint: disable=unused-argument
        return super(DisclosureFaker, cls)._fit(values, faker_type=faker_type,
                                                locale=locale)
