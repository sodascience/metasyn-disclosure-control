from typing import List, Type

from metasynth.disttree import BaseDistributionTree
from metasynth.distribution.base import BaseDistribution

from metasynthcontrib.disclosure.continuous import DisclosureUniform, DisclosureTruncatedNormal
from metasynthcontrib.disclosure.discrete import DisclosureDiscreteUniform, DisclosureUniqueKey


class DisclosureDistributionTree(BaseDistributionTree):
    @property
    def continuous_distributions(self) -> List[Type[BaseDistribution]]:
        return [DisclosureUniform, DisclosureTruncatedNormal]

    @property
    def discrete_distributions(self) -> List[Type[BaseDistribution]]:
        return [DisclosureDiscreteUniform,  DisclosureUniqueKey]

    @property
    def categorical_distributions(self) -> List[Type[BaseDistribution]]:
        return []

    @property
    def string_distributions(self) -> List[Type[BaseDistribution]]:
        return []

    @property
    def date_distributions(self) -> List[Type[BaseDistribution]]:
        return []

    @property
    def time_distributions(self) -> List[Type[BaseDistribution]]:
        return []

    @property
    def datetime_distributions(self) -> List[Type[BaseDistribution]]:
        return []
