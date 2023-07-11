from pytest import mark

from metasynth.provider import get_distribution_provider
from metasynth.testutils import check_distribution, check_distribution_provider
from metasynthcontrib.disclosure.privacy import DisclosurePrivacy


def test_disclosure_provider():
    check_distribution_provider("metasynth-disclosure")


@mark.parametrize(
    "distribution", get_distribution_provider("metasynth-disclosure").distributions
)
@mark.parametrize(
    "privacy_kwargs", ({}, {"n_avg": 10}, {"n_avg": 15})
)
def test_dist_validation(distribution, privacy_kwargs):
    privacy = DisclosurePrivacy(**privacy_kwargs)
    check_distribution(distribution, privacy=privacy,
                       provenance="metasynth-disclosure")
