from metasyn.distribution.continuous import ConstantDistribution
from metasyn.distribution.datetime import (
    DateConstantDistribution,
    DateTimeConstantDistribution,
    TimeConstantDistribution,
)
from metasyn.distribution.discrete import DiscreteConstantDistribution
from metasyn.distribution.string import StringConstantDistribution
from pytest import mark

from metasyncontrib.disclosure.continuous import DisclosureConstant
from metasyncontrib.disclosure.datetime import (
    DisclosureDateConstant,
    DisclosureDateTimeConstant,
    DisclosureTimeConstant,
)
from metasyncontrib.disclosure.discrete import DisclosureDiscreteConstant
from metasyncontrib.disclosure.string import DisclosureStringConstant


@mark.parametrize(
    "dist_builtin, dist_disclosure, value, disclosurevalue",
    [
        (ConstantDistribution, DisclosureConstant, 8.0, 99999.9),
        (DiscreteConstantDistribution, DisclosureDiscreteConstant, 8, 99999),
        (StringConstantDistribution, DisclosureStringConstant, "Secretvalue", "REDACTED"),
        (DateTimeConstantDistribution, DisclosureDateTimeConstant, "2024-02-23T12:08:38", "1970-01-01T00:00:00"),  # noqa: E501
        (TimeConstantDistribution, DisclosureTimeConstant, "12:08:38", "00:00:00"),
        (DateConstantDistribution, DisclosureDateConstant, "2024-02-23", "1970-01-01"),
    ],
)
def test_constant(dist_builtin, dist_disclosure, value, disclosurevalue):  # noqa: D103
    dist = dist_builtin(value)
    data = [dist.draw() for _ in range(21)]

    assert dist_disclosure.fit(data, partition_size=11)._param_dict().get("value") == disclosurevalue
