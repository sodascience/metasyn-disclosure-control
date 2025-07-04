"""Module that contains a class useful for both discrete and continuous distributions."""
from __future__ import annotations

from metasyn.distribution.base import BaseDistribution

from metasyncontrib.disclosure.privacy import DisclosurePrivacy
from metasyncontrib.disclosure.utils import micro_aggregate


class DisclosureNumericalMixin(BaseDistribution):
    """Mixin class to create numerical distributions of the disclosure kind."""

    @classmethod
    def fit(cls, series, privacy: DisclosurePrivacy, *args,
            **kwargs) -> BaseDistribution:
        """Fit numeric distributions with disclosure control rules in place."""
        pl_series = cls._to_series(series)
        sub_series = micro_aggregate(pl_series,
                                     min_partition_size=privacy.partition_size,
                                     max_dominance=privacy.max_dominance)
        return cls._fit(sub_series, *args, **kwargs)
