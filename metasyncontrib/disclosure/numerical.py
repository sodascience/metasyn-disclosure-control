"""Module that contains a class useful for both discrete and continuous distributions."""
from __future__ import annotations

from metasyn.distribution.base import BaseDistribution, BaseFitter, VarLog, convert_to_series

from metasyncontrib.disclosure.privacy import DisclosurePrivacy
from metasyncontrib.disclosure.utils import micro_aggregate


class DisclosureNumericalMixin(BaseFitter):
    """Mixin class to create numerical distributions of the disclosure kind."""

    privacy: DisclosurePrivacy

    def fit(self, values, fit_log: VarLog | None = None) -> BaseDistribution:
        """Fit numeric distributions with disclosure control rules in place."""
        fit_log = VarLog() if fit_log is None else fit_log
        series = convert_to_series(values)
        sub_series = micro_aggregate(series,
                                     fit_log,
                                     min_partition_size=self.privacy.partition_size,
                                     max_dominance=self.privacy.max_dominance)
        fit_log.add(method="Applying normal fit method on micro-aggregated data.")
        return self._fit(sub_series, fit_log)
