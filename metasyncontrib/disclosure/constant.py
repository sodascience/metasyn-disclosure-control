"""Module for disclosure controlled constant distributions."""
from __future__ import annotations

import polars as pl
from metasyn.distribution.base import BaseDistribution
from metasyn.distribution.constant import (
    ConstantDistribution,
    DateConstantDistribution,
    DateTimeConstantDistribution,
    DiscreteConstantDistribution,
    StringConstantDistribution,
    TimeConstantDistribution,
)

from metasyncontrib.disclosure.base import metadist_disclosure


class DisclosureConstantMixin(BaseDistribution):
    """Mixin class to overload fit method for constant distributions."""

    @classmethod
    def fit(cls, series, *args, n_avg: int = 11, **kwargs) -> BaseDistribution:
        """Fit constant distributions with disclosure control rules in place."""
        pl_series: pl.Series = cls._to_series(series)

        # if unique, just get that value if it occurs at least n_avg times
        if pl_series.n_unique() == 1 and pl_series.len() >= n_avg:
            return cls._fit(pl_series, *args, **kwargs)
            
        if pl_series.n_unique() > 1:
            # if not unique, ensure most common value occurs at least n_avg times
            _value, count = pl_series.value_counts(sort=True).row(0)
            if count >= n_avg:
                return cls._fit(pl_series, *args, **kwargs)
        
        return cls.default_distribution()


@metadist_disclosure()
class DisclosureConstant(DisclosureConstantMixin, ConstantDistribution):
    """Disclosure controlled ConstantDistribution."""

@metadist_disclosure()
class DisclosureDiscreteConstant(DisclosureConstantMixin, DiscreteConstantDistribution):
    """Disclosure controlled DiscreteConstantDistribution."""

@metadist_disclosure()
class DisclosureStringConstant(DisclosureConstantMixin, StringConstantDistribution):
    """Disclosure controlled StringConstantDistribution."""

@metadist_disclosure()
class DisclosureDateTimeConstant(DisclosureConstantMixin, DateTimeConstantDistribution):
    """Disclosure controlled DateTimeConstantDistribution."""

@metadist_disclosure()
class DisclosureTimeConstant(DisclosureConstantMixin, TimeConstantDistribution):
    """Disclosure controlled TimeConstantDistribution."""

@metadist_disclosure()
class DisclosureDateConstant(DisclosureConstantMixin, DateConstantDistribution):
    """Disclosure controlled DateConstantDistribution."""
