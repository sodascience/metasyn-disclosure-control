from typing import List, Type

from metasynth.disttree import BuiltinDistributionTree
from metasynth.distribution.base import BaseDistribution
# from metasynth.distribution.categorical import MultinoulliDistribution

from metasynthcontrib.disclosure.continuous import DisclosureUniform, DisclosureTruncatedNormal
from metasynthcontrib.disclosure.continuous import DisclosureNormalDistribution
from metasynthcontrib.disclosure.continuous import DisclosureLogNormalDistribution
from metasynthcontrib.disclosure.continuous import DisclosureExponentialDistribution
from metasynthcontrib.disclosure.discrete import DisclosureDiscreteUniform, DisclosureUniqueKey
from metasynthcontrib.disclosure.discrete import DisclosurePoissonDistribution
from metasynthcontrib.disclosure.string import DisclosureFakerDistribution
from metasynthcontrib.disclosure.categorical import DisclosureMultinoulliDistribution
from metasynthcontrib.disclosure.datetime import DisclosureDateDistribution
from metasynthcontrib.disclosure.datetime import DisclosureDateTimeDistribution
from metasynthcontrib.disclosure.datetime import DisclosureTimeDistribution


# TODO: currently unsafe distributions are included
class DisclosureDistributionTree(BuiltinDistributionTree):
    @property
    def continuous_distributions(self) -> List[Type[BaseDistribution]]:
        return [DisclosureUniform, DisclosureTruncatedNormal, DisclosureNormalDistribution,
                DisclosureLogNormalDistribution, DisclosureExponentialDistribution]

    @property
    def discrete_distributions(self) -> List[Type[BaseDistribution]]:
        return [DisclosureDiscreteUniform,  DisclosureUniqueKey, DisclosurePoissonDistribution]

    @property
    def categorical_distributions(self) -> List[Type[BaseDistribution]]:
        return [DisclosureMultinoulliDistribution]

    @property
    def string_distributions(self) -> List[Type[BaseDistribution]]:
        return [DisclosureFakerDistribution]

    @property
    def date_distributions(self) -> List[Type[BaseDistribution]]:
        return [DisclosureDateDistribution]

    @property
    def time_distributions(self) -> List[Type[BaseDistribution]]:
        return [DisclosureTimeDistribution]

    @property
    def datetime_distributions(self) -> List[Type[BaseDistribution]]:
        return [DisclosureDateTimeDistribution]
