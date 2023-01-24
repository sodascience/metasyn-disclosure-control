from abc import abstractmethod

import polars as pl

from metasynth.distribution.base import BaseDistribution


class BaseDisclosureDistribution(BaseDistribution):
    @classmethod
    @abstractmethod
    def _fit(cls, values: pl.Series, n_avg=11) -> BaseDistribution:
        return super(BaseDisclosureDistribution, cls)._fit(values)
