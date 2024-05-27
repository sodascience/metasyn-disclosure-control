"""Module contains distribution provider for disclosure control."""

from __future__ import annotations

from metasyn.provider import BaseDistributionProvider

from metasyncontrib.disclosure.categorical import DisclosureMultinoulli
from metasyncontrib.disclosure.continuous import (
    DisclosureConstant,
    DisclosureExponential,
    DisclosureLogNormal,
    DisclosureNormal,
    DisclosureTruncatedNormal,
    DisclosureUniform,
)
from metasyncontrib.disclosure.datetime import (
    DisclosureDate,
    DisclosureDateConstant,
    DisclosureDateTime,
    DisclosureDateTimeConstant,
    DisclosureTime,
    DisclosureTimeConstant,
)
from metasyncontrib.disclosure.discrete import (
    DisclosureDiscreteConstant,
    DisclosureDiscreteNormal,
    DisclosureDiscreteTruncatedNormal,
    DisclosureDiscreteUniform,
    DisclosurePoisson,
    DisclosureUniqueKey,
)
from metasyncontrib.disclosure.na import DisclosureNA
from metasyncontrib.disclosure.string import (
    DisclosureFaker,
    DisclosureFreetext,
    DisclosureStringConstant,
    DisclosureUniqueFaker,
)


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
