"""Disclosure classes for categorical variables."""

from __future__ import annotations

import numpy as np
import polars as pl
from metasyn.distribution.base import VarLog
from metasyn.distribution.categorical import MultinoulliFitter
from metasyn.util import get_var_type

from metasyncontrib.disclosure.base import disclosure_fitter
from metasyncontrib.disclosure.privacy import DisclosurePrivacy


@disclosure_fitter()
class DisclosureMultinoulli(MultinoulliFitter):
    """Disclosure variant for multinoulli distribution.

    It checks that all labels appear at least partition_size times, and that
    there is no label with >90% of the counts.
    """

    privacy: DisclosurePrivacy

    def _fit(self, series: pl.Series, fit_log: VarLog):  # noqa: C901
        dist = super()._fit(series, VarLog())
        # Remove labels with counts < partition_size
        labels = dist.labels[dist.probs >= self.privacy.partition_size / len(series)]
        probs = dist.probs[dist.probs >= self.privacy.partition_size / len(series)]

        if (dist.probs < self.privacy.partition_size / len(series)).sum() > 0:
            fit_log.add(
                privacy="Removed labels "
                + str(dist.labels[dist.probs < self.privacy.partition_size / len(series)])
                + ", because counts were less than the partion size threshold of "
                f"{self.privacy.partition_size}.")
        # If no more categories are present or the dominance criterion is not satisfied return
        # the default distribution.
        if len(probs) == 0:
            fit_log.add(privacy="Using default distribution, because after removing all categories "
                        "with counts less than the partition size no data was left to fit.")
            return self.default_distribution(series)
        if probs.max() >= self.privacy.group_disclosure_threshold:
            fit_log.add(privacy="Using default distribution, because a category is exceeding the "
                        "group disclosure threshold: "
                        f"{probs.max()} > {self.privacy.group_disclosure_threshold}")
            return self.default_distribution(series)
        n_leftover = round((1-probs.sum())*len(series))

        if n_leftover > 0:
            fit_log.add(method="After removing labels for privacy concerns, the remaining "
                        "categories are renormalized. The new probabilities are chosen so that"
                        " it cannot be deduced how many values were removed.")

        # Redistribute labels non-randomly
        # Attempt to distribute the counts as best we can
        n_dist = np.round((probs/probs.sum())*n_leftover)

        # Due to rounding, we could have a few more or less, so those are distributed differently
        n_still_leftover = n_leftover-n_dist.sum()

        # Get the difference between the optimal and current distribution
        n_diff = probs*len(series) + n_dist - (probs/probs.sum()*len(series))

        # If there are a positive number of leftovers, then the highest differential probability
        # gets one first, then the second highest differential, etc.
        if n_still_leftover > 0:
            for i_label in np.argsort(n_diff):
                n_dist[i_label] += 1
                n_still_leftover -= 1
                if n_still_leftover == 0:
                    break
        # If the number leftover is negative (distributed too many values), then do the reverse.
        elif n_still_leftover < 0:
            for i_label in reversed(np.argsort(n_diff)):
                n_dist[i_label] -= 1
                n_still_leftover += 1
                if n_still_leftover == 0:
                    break
        probs += n_dist/len(series)
        return self.distribution(labels, probs)

    def default_distribution(self, series):  # noqa: D102
        if get_var_type(series) == "discrete":
            return self.distribution([77777, 88888, 99999], [0.1, 0.2, 0.7])  # type: ignore
        return self.distribution(["A_REDACTED", "B_REDACTED", "C_REDACTED"], [0.1, 0.3, 0.6])

