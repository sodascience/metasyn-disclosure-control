"""Disclosure control implementations for continuous distributions."""

from metasyn.distribution.constant import (
    ContinuousConstantFitter,
    DateConstantFitter,
    DateTimeConstantFitter,
    DiscreteConstantFitter,
    StringConstantFitter,
    TimeConstantFitter,
)

from metasyncontrib.disclosure.base import disclosure_fitter


@disclosure_fitter()
class DisclosureConstant(ContinuousConstantFitter):
    """Disclosure controlled ConstantFitter."""

    def _fit(self, series):
        return self.distribution(99999.9)


@disclosure_fitter()
class DisclosureDiscreteConstant(DiscreteConstantFitter):
    """Disclosure controlled DiscreteConstantFitter."""

    def _fit(self, series):
        return self.distribution(99999)


@disclosure_fitter()
class DisclosureStringConstant(StringConstantFitter):
    """Disclosure controlled StringConstantFitter."""

    def _fit(self, series):
        return self.distribution("REDACTED")


@disclosure_fitter()
class DisclosureDateTimeConstant(DateTimeConstantFitter):
    """Disclosure controlled DateTimeConstantFitter."""

    def _fit(self, series):
        return self.distribution("1970-01-01T00:00:00")


@disclosure_fitter()
class DisclosureTimeConstant(TimeConstantFitter):
    """Disclosure controlled TimeConstantFitter."""

    def _fit(self, series):
        return self.distribution("00:00:00")


@disclosure_fitter()
class DisclosureDateConstant(DateConstantFitter):
    """Disclosure controlled DateConstantFitter."""

    def _fit(self, series):
        return self.distribution("1970-01-01")
