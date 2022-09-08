from typing import Sequence

from metasynth.distribution.categorical import MultinoulliDistribution


class DisclosureMultinoulliDistribution(MultinoulliDistribution):
    @classmethod
    def _fit(cls, values: Sequence[str], n_avg: int=10):
        dist = super(DisclosureMultinoulliDistribution, cls)._fit(values)
        labels = dist.labels[dist.probs >= n_avg/len(values)]
        probs = dist.probs[dist.probs >= n_avg/len(values)]
        return cls(labels, probs)
