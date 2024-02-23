"""Module contains distribution provider for disclosure control."""

from __future__ import annotations

from metasyn.provider import BaseDistributionProvider

from metasyncontrib.disclosure.categorical import DisclosureMultinoulli
from metasyncontrib.disclosure.constant import (
    DisclosureConstant,
    DisclosureDateConstant,
    DisclosureDateTimeConstant,
    DisclosureDiscreteConstant,
    DisclosureStringConstant,
    DisclosureTimeConstant,
)
from metasyncontrib.disclosure.continuous import (
    DisclosureExponential,
    DisclosureLogNormal,
    DisclosureNormal,
    DisclosureTruncatedNormal,
    DisclosureUniform,
)
from metasyncontrib.disclosure.datetime import DisclosureDate, DisclosureDateTime, DisclosureTime
from metasyncontrib.disclosure.discrete import (
    DisclosureDiscreteNormal,
    DisclosureDiscreteTruncatedNormal,
    DisclosureDiscreteUniform,
    DisclosurePoisson,
    DisclosureUniqueKey,
)
from metasyncontrib.disclosure.faker import (
    DisclosureFaker,
    DisclosureFreetext,
    DisclosureUniqueFaker,
)
from metasyncontrib.disclosure.na import DisclosureNA


class DisclosureProvider(BaseDistributionProvider):
    """Distribution tree that contains safe distributions.

    See for more information on disclosure control:
    https://ec.europa.eu/eurostat/cros/system/files/dwb_standalone-document_output-checking-guidelines.pdf
    """

    name = "metasyn-disclosure"
    version = "1.0"
    distributions = [
        DisclosureMultinoulli,
        DisclosureConstant,
        DisclosureDateConstant,
        DisclosureDateTimeConstant,
        DisclosureDiscreteConstant,
        DisclosureStringConstant,
        DisclosureTimeConstant,
        DisclosureExponential,
        DisclosureLogNormal,
        DisclosureNormal,
        DisclosureTruncatedNormal,
        DisclosureUniform,
        DisclosureDate, 
        DisclosureDateTime, 
        DisclosureTime,
        DisclosureDiscreteNormal,
        DisclosureDiscreteTruncatedNormal,
        DisclosureDiscreteUniform,
        DisclosurePoisson,
        DisclosureUniqueKey,
        DisclosureFaker, 
        DisclosureUniqueFaker,
        DisclosureFreetext,
        DisclosureNA,
    ]
