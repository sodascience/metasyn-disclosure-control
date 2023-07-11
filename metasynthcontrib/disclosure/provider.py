"""Module contains distribution tree for disclosure control."""

from __future__ import annotations
from metasynth.provider import BaseDistributionProvider

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


class DisclosureProvider(BaseDistributionProvider):
    """Distribution tree that contains safe distributions.

    See for more information on disclosure control:
    https://ec.europa.eu/eurostat/cros/system/files/dwb_standalone-document_output-checking-guidelines.pdf
    """

    name = "metasynth-disclosure"
    version = "1.0"
    distributions = [
        DisclosureUniform, DisclosureTruncatedNormal, DisclosureNormal,
        DisclosureLogNormal, DisclosureExponential,
        DisclosureDiscreteUniform, DisclosureUniqueKey, DisclosurePoisson,
        DisclosureMultinoulli,
        DisclosureFaker,
        DisclosureDate,
        DisclosureTime,
        DisclosureDateTime,
    ]
