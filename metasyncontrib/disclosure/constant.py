"""Disclosure control implementations for continuous distributions."""

from metasyn.distribution.base import BaseDistribution, BaseFitter
from metasyn.distribution.constant import (
    ContinuousConstantFitter,
    DateConstantFitter,
    DateTimeConstantFitter,
    DiscreteConstantFitter,
    StringConstantFitter,
    TimeConstantFitter,
)

from metasyncontrib.disclosure.base import disclosure_fitter


class DisclosureConstantMixin(BaseFitter):
    """Mixin class to overload fit method for constant distributions."""

    def _fit(self, series) -> BaseDistribution:  #pylint: disable=unused-argument
        """Fit constant distributions with disclosure control rules in place."""
        # NB: dominance rule ensures that constant distribution is essentially never
        # allowed under formal disclosure control. Always return default distribution.
        return self.default_distribution()


@disclosure_fitter()
class DisclosureConstant(DisclosureConstantMixin, ContinuousConstantFitter):
    """Disclosure controlled ConstantFitter."""

    def default_distribution(self):  # noqa: D102
        return self.distribution(99999.9)


@disclosure_fitter()
class DisclosureDiscreteConstant(DisclosureConstantMixin, DiscreteConstantFitter):
    """Disclosure controlled DiscreteConstantFitter."""

    def default_distribution(self):  # noqa: D102
        return self.distribution(99999)


@disclosure_fitter()
class DisclosureStringConstant(DisclosureConstantMixin, StringConstantFitter):
    """Disclosure controlled StringConstantFitter."""

    def default_distribution(self):  # noqa: D102
        return self.distribution("REDACTED")


@disclosure_fitter()
class DisclosureDateTimeConstant(DisclosureConstantMixin, DateTimeConstantFitter):
    """Disclosure controlled DateTimeConstantFitter."""

    def default_distribution(self):  # noqa: D102
        return self.distribution("1970-01-01T00:00:00")


@disclosure_fitter()
class DisclosureTimeConstant(DisclosureConstantMixin, TimeConstantFitter):
    """Disclosure controlled TimeConstantFitter."""

    def default_distribution(self):  # noqa: D102
        return self.distribution("00:00:00")


@disclosure_fitter()
class DisclosureDateConstant(DisclosureConstantMixin, DateConstantFitter):
    """Disclosure controlled DateConstantFitter."""

    def default_distribution(self):  # noqa: D102
        return self.distribution("1970-01-01")
