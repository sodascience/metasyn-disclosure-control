import numpy as np
from metasyn.provider import get_distribution_provider
from metasyn.testutils import check_distribution, check_distribution_provider
from pytest import mark

from metasyncontrib.disclosure.privacy import DisclosurePrivacy


def test_disclosure_provider():
    check_distribution_provider("metasyn-disclosure")


@mark.parametrize("distribution", get_distribution_provider("metasyn-disclosure").distributions)
@mark.parametrize("privacy_kwargs", ({}, {"partition_size": 10}, {"partition_size": 15}))
def test_dist_validation(distribution, privacy_kwargs):
    np.random.seed(45)
    privacy = DisclosurePrivacy(**privacy_kwargs)
    # Testing empty series will fail with a convergence error, so skip these tests.
    try:
        check_distribution(distribution, privacy=privacy, provenance="metasyn-disclosure", test_empty=False)
    except TypeError:
        check_distribution(distribution, privacy=privacy, provenance="metasyn-disclosure")
