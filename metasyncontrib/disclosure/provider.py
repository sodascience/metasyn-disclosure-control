"""Module contains distribution tree for disclosure control."""

from __future__ import annotations
from metasyn.provider import BaseDistributionProvider

from metasyncontrib.disclosure.continuous import DisclosureUniform, DisclosureTruncatedNormal
from metasyncontrib.disclosure.continuous import DisclosureNormal
from metasyncontrib.disclosure.continuous import DisclosureLogNormal
from metasyncontrib.disclosure.continuous import DisclosureExponential
from metasyncontrib.disclosure.discrete import DisclosureDiscreteUniform, DisclosureUniqueKey
from metasyncontrib.disclosure.discrete import DisclosurePoisson
from metasyncontrib.disclosure.string import DisclosureFaker, DisclosureUniqueFaker
from metasyncontrib.disclosure.categorical import DisclosureMultinoulli
from metasyncontrib.disclosure.datetime import DisclosureDate
from metasyncontrib.disclosure.datetime import DisclosureDateTime
from metasyncontrib.disclosure.datetime import DisclosureTime


class DisclosureProvider(BaseDistributionProvider):
    """Distribution tree that contains safe distributions.

    See for more information on disclosure control:
    https://ec.europa.eu/eurostat/cros/system/files/dwb_standalone-document_output-checking-guidelines.pdf
    """

    name = "metasyn-disclosure"
    version = "1.0"
    distributions = [
        DisclosureUniform, DisclosureTruncatedNormal, DisclosureNormal,
        DisclosureLogNormal, DisclosureExponential,
        DisclosureDiscreteUniform, DisclosureUniqueKey, DisclosurePoisson,
        DisclosureMultinoulli,
        DisclosureFaker, DisclosureUniqueFaker,
        DisclosureDate,
        DisclosureTime,
        DisclosureDateTime,
    ]
