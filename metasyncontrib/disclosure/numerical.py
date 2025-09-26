"""Module that contains a class useful for both discrete and continuous distributions."""
from __future__ import annotations

from metasyn.distribution.base import BaseDistribution, BaseFitter, convert_to_series

from metasyncontrib.disclosure.privacy import DisclosurePrivacy
from metasyncontrib.disclosure.utils import micro_aggregate


class DisclosureNumericalMixin(BaseFitter):
    """Mixin class to create numerical distributions of the disclosure kind."""

    privacy: DisclosurePrivacy

    def fit(self, values, *args, **kwargs) -> BaseDistribution:
        """Fit numeric distributions with disclosure control rules in place."""
        series = convert_to_series(values)
        sub_series = micro_aggregate(series,
                                     min_partition_size=self.privacy.partition_size,
                                     max_dominance=self.privacy.max_dominance)
        return self._fit(sub_series, *args, **kwargs)
