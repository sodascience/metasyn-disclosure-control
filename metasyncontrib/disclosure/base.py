"""Base class for all disclosure control distributions."""

import polars as pl
from metasyn.distribution.base import BaseDistribution


def metadist_disclosure():
    """Decorate class to create a distribution with disclosure control.

    Returns
    -------
    cls:
        Class with the appropriate class variables.

    """

    def _wrap(cls):
        cls.provenance = "metasyn-disclosure"
        cls.privacy = "disclosure"
        return cls

    return _wrap


class DisclosureConstantMixin(BaseDistribution):
    """Mixin class to overload fit method for constant distributions."""

    @classmethod
    def fit(cls, series, *args, partition_size: int = 11, **kwargs) -> BaseDistribution:
        """Fit constant distributions with disclosure control rules in place."""
        pl_series: pl.Series = cls._to_series(series)

        # if unique, just get that value if it occurs at least partition_size times
        if pl_series.n_unique() == 1 and pl_series.len() >= partition_size:
            return cls._fit(pl_series, *args, **kwargs)

        if pl_series.n_unique() > 1:
            # if not unique, ensure most common value occurs at least partition_size times
            _value, count = pl_series.value_counts(sort=True).row(0)
            if count >= partition_size:
                return cls._fit(pl_series, *args, **kwargs)

        return cls.default_distribution()

