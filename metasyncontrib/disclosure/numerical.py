"""Module that contains a class useful for both discrete and continuous distributions."""
from __future__ import annotations

from metasyn.distribution.base import BaseDistribution

from metasyncontrib.disclosure.utils import micro_aggregate


class DisclosureNumerical(BaseDistribution):
    """Class for numerical distributions of the disclosure kind."""

    @classmethod
    def fit(cls, series, *args, n_avg: int = 11, **kwargs) -> BaseDistribution:
        pl_series = cls._to_series(series)
        sub_series = micro_aggregate(pl_series, n_avg)
        return cls._fit(sub_series, *args, **kwargs)
