from metasyn.distribution.constant import (
    ContinuousConstantDistribution,
    DateConstantDistribution,
    DateTimeConstantDistribution,
    DiscreteConstantDistribution,
    StringConstantDistribution,
    TimeConstantDistribution,
)
from pytest import mark

from metasyncontrib.disclosure.constant import (
    DisclosureConstant,
    DisclosureDateConstant,
    DisclosureDateTimeConstant,
    DisclosureDiscreteConstant,
    DisclosureStringConstant,
    DisclosureTimeConstant,
)
from metasyncontrib.disclosure.privacy import DisclosurePrivacy


@mark.parametrize(
    "dist_builtin, dist_disclosure, value, disclosurevalue",
    [
        (ContinuousConstantDistribution, DisclosureConstant, 8.0, 99999.9),
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

    privacy = DisclosurePrivacy()
    assert dist_disclosure(privacy).fit(data)._param_dict().get("value") == disclosurevalue
