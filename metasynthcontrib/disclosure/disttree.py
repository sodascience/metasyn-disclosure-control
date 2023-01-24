"""Module contains distribution tree for disclosure control."""

from typing import List, Type

from metasynth.disttree import BuiltinDistributionTree
from metasynth.distribution.base import BaseDistribution

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


# Currently unsafe distributions are included:
# DisclosureUniqueKey needs to be checked (no guidelines).
class DisclosureDistributionTree(BuiltinDistributionTree):
    """Distribution tree that contains safe distributions.

    See for more information on disclosure control:
    https://ec.europa.eu/eurostat/cros/system/files/dwb_standalone-document_output-checking-guidelines.pdf
    """

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
