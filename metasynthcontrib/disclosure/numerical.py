from typing import Sequence


from metasynth.distribution.base import BaseDistribution
from metasynthcontrib.disclosure.utils import subsample


class DisclosureNumerical(BaseDistribution):
    @classmethod
    def fit(cls, series: Sequence, n_avg: int=10) -> BaseDistribution:
        pl_series = cls._to_series(series)
        sub_series = subsample(pl_series, n_avg)
        return cls._fit(sub_series, n_avg=n_avg)
