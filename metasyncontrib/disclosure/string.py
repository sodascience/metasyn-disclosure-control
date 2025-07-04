"""Module for disclosure control for string distributions."""

from metasyn.distribution.string import (
    FakerDistribution,
    FreeTextDistribution,
    StringConstantDistribution,
    UniqueFakerDistribution,
)

from metasyncontrib.disclosure.base import DisclosureConstantMixin, metadist_disclosure


@metadist_disclosure()
class DisclosureFaker(FakerDistribution):
    """Faker distribution for disclosure control."""

    @classmethod
<<<<<<< HEAD
    def _fit(cls, values, faker_type: str = "city", locale: str = "en_US"):
=======
    def _fit(cls, values, faker_type: str = "city", locale: str = "en_US"):  # pylint: disable=unused-argument
>>>>>>> 8e9f47c (Update to new structure in metasyn)
        return super()._fit(values, faker_type=faker_type, locale=locale)


@metadist_disclosure()
class DisclosureUniqueFaker(UniqueFakerDistribution):
    """Faker distribution for disclosure control that produces unique values."""

    @classmethod
<<<<<<< HEAD
    def _fit(cls, values, faker_type: str = "city", locale: str = "en_US"):
=======
    def _fit(cls, values, faker_type: str = "city", locale: str = "en_US"):  # pylint: disable=unused-argument
>>>>>>> 8e9f47c (Update to new structure in metasyn)
        return super()._fit(values, faker_type=faker_type, locale=locale)


@metadist_disclosure()
class DisclosureFreetext(FreeTextDistribution):
    """Disclosure implementation of freetext distribution.

    This implementation is the same as the original.
    """

    @classmethod
<<<<<<< HEAD
    def _fit(cls, values, max_values: int = 50):
=======
    def _fit(cls, values, max_values: int = 50):  # pylint: disable=unused-argument
>>>>>>> 8e9f47c (Update to new structure in metasyn)
        return super()._fit(values, max_values=max_values)


@metadist_disclosure()
class DisclosureStringConstant(DisclosureConstantMixin, StringConstantDistribution):
    """Disclosure controlled StringConstantDistribution."""

    @classmethod
    def default_distribution(cls):  # noqa: D102
        return cls("REDACTED")
