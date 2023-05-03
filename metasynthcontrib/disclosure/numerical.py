"""Module that contains a class useful for both discrete and continuous distributions."""
from __future__ import annotations
from typing import Union
from collections.abc import Sequence

import polars as pl

from metasynth.distribution.base import BaseDistribution

from metasynthcontrib.disclosure.utils import micro_aggregate
from metasynthcontrib.disclosure.base import BaseDisclosure


class DisclosureNumerical(BaseDisclosure):
    """Class for numerical distributions of the disclosure kind."""

    @classmethod
    def fit(cls, series: Union[Sequence, pl.Series], *args,
            n_avg: int=11, **kwargs) -> BaseDistribution:
        pl_series = cls._to_series(series)
        sub_series = micro_aggregate(pl_series, n_avg)
        return cls._fit(sub_series, *args, **kwargs)
