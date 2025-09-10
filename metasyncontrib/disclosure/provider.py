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
from metasyncontrib.disclosure.exponential import DisclosureExponential
from metasyncontrib.disclosure.faker import (
    DisclosureFaker,
    DisclosureUniqueFaker,
)
from metasyncontrib.disclosure.freetext import DisclosureFreetext
from metasyncontrib.disclosure.na import DisclosureNA
from metasyncontrib.disclosure.normal import (
    DisclosureDiscreteNormal,
    DisclosureDiscreteTruncatedNormal,
    DisclosureLogNormal,
    DisclosureNormal,
    DisclosureTruncatedNormal,
)
from metasyncontrib.disclosure.poisson import DisclosurePoisson
from metasyncontrib.disclosure.uniform import (
    DisclosureDate,
    DisclosureDateTime,
    DisclosureDiscreteUniform,
    DisclosureTime,
    DisclosureContinuousUniform,
)
from metasyncontrib.disclosure.uniquekey import DisclosureUniqueKey


class DisclosureProvider(BaseDistributionProvider):
    """Distribution tree that contains safe distributions.

    See for more information on disclosure control:
    https://ec.europa.eu/eurostat/cros/system/files/dwb_standalone-document_output-checking-guidelines.pdf
    """

    name = "metasyn-disclosure"
    version = "1.0"
    fitters = [
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
        DisclosureContinuousUniform,
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
