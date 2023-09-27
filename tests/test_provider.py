from pytest import mark

from metasyn.provider import get_distribution_provider
from metasyn.testutils import check_distribution, check_distribution_provider
from metasyncontrib.disclosure.privacy import DisclosurePrivacy


def test_disclosure_provider():
    check_distribution_provider("metasyn-disclosure")


@mark.parametrize(
    "distribution", get_distribution_provider("metasyn-disclosure").distributions
)
@mark.parametrize(
    "privacy_kwargs", ({}, {"n_avg": 10}, {"n_avg": 15})
)
def test_dist_validation(distribution, privacy_kwargs):
    privacy = DisclosurePrivacy(**privacy_kwargs)
    check_distribution(distribution, privacy=privacy,
                       provenance="metasyn-disclosure")
