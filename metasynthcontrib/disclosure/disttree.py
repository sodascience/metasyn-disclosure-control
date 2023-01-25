"""Module contains distribution tree for disclosure control."""

from typing import List, Type

from metasynth.disttree import BuiltinDistributionTree
from metasynth.distribution.base import BaseDistribution

from metasynthcontrib.disclosure.continuous import DisclosureUniform, DisclosureTruncatedNormal
from metasynthcontrib.disclosure.continuous import DisclosureNormal
from metasynthcontrib.disclosure.continuous import DisclosureLogNormal
from metasynthcontrib.disclosure.continuous import DisclosureExponential
from metasynthcontrib.disclosure.discrete import DisclosureDiscreteUniform, DisclosureUniqueKey
from metasynthcontrib.disclosure.discrete import DisclosurePoisson
from metasynthcontrib.disclosure.string import DisclosureFaker
from metasynthcontrib.disclosure.categorical import DisclosureMultinoulli
from metasynthcontrib.disclosure.datetime import DisclosureDate
from metasynthcontrib.disclosure.datetime import DisclosureDateTime
from metasynthcontrib.disclosure.datetime import DisclosureTime


# Currently unsafe distributions are included:
# DisclosureUniqueKey needs to be checked (no guidelines).
class DisclosureDistributionTree(BuiltinDistributionTree):
    """Distribution tree that contains safe distributions.

    See for more information on disclosure control:
    https://ec.europa.eu/eurostat/cros/system/files/dwb_standalone-document_output-checking-guidelines.pdf
    """

    @property
    def continuous_distributions(self) -> List[Type[BaseDistribution]]:
        return [DisclosureUniform, DisclosureTruncatedNormal, DisclosureNormal,
                DisclosureLogNormal, DisclosureExponential]

    @property
    def discrete_distributions(self) -> List[Type[BaseDistribution]]:
        return [DisclosureDiscreteUniform,  DisclosureUniqueKey, DisclosurePoisson]

    @property
    def categorical_distributions(self) -> List[Type[BaseDistribution]]:
        return [DisclosureMultinoulli]

    @property
    def string_distributions(self) -> List[Type[BaseDistribution]]:
        return [DisclosureFaker]

    @property
    def date_distributions(self) -> List[Type[BaseDistribution]]:
        return [DisclosureDate]

    @property
    def time_distributions(self) -> List[Type[BaseDistribution]]:
        return [DisclosureTime]

    @property
    def datetime_distributions(self) -> List[Type[BaseDistribution]]:
        return [DisclosureDateTime]
