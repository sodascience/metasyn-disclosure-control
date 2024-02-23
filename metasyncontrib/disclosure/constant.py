"""Module for disclosure controlled constant distributions."""
import polars as pl
from metasyn.distribution.constant import (
    ConstantDistribution,
    DiscreteConstantDistribution,
    StringConstantDistribution,
    DateTimeConstantDistribution,
    TimeConstantDistribution,
    DateConstantDistribution,
)
from metasyncontrib.disclosure.base import metadist_disclosure


def disclosure_constant(cls):
    """Override _fit method for constant distributions using this decorator."""
    def _fit(values: pl.Series, n_avg=11):
        # if unique, just get that value if it occurs at least n_avg times
        if values.n_unique() == 1 & values.len() >= n_avg:
            return cls(values.unique()[0])

        # otherwise get most common value
        val_counts = values.value_counts(sort=True)
        value = val_counts[0,0]
        count = val_counts[0,1]

        if count >= n_avg:
            return cls(value)

        return cls.default_distribution()

    setattr(cls, "_fit", _fit)
    return cls


@metadist_disclosure()
@disclosure_constant
class DisclosureConstant(ConstantDistribution):
    """Disclosure controlled ConstantDistribution."""

@metadist_disclosure()
@disclosure_constant
class DisclosureDiscreteConstant(DiscreteConstantDistribution):
    """Disclosure controlled DiscreteConstantDistribution."""

@metadist_disclosure()
@disclosure_constant
class DisclosureStringConstant(StringConstantDistribution):
    """Disclosure controlled StringConstantDistribution."""

@metadist_disclosure()
@disclosure_constant
class DisclosureDateTimeConstant(DateTimeConstantDistribution):
    """Disclosure controlled DateTimeConstantDistribution."""

@metadist_disclosure()
@disclosure_constant
class DisclosureTimeConstant(TimeConstantDistribution):
    """Disclosure controlled TimeConstantDistribution."""

@metadist_disclosure()
@disclosure_constant
class DisclosureDateConstant(DateConstantDistribution):
    """Disclosure controlled DateConstantDistribution."""
