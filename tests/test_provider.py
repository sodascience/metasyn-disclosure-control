import numpy as np
from metasyn.registry import DistributionRegistry
from metasyn.testutils import check_distribution_registry, check_fitter
from pytest import mark

from metasyncontrib.disclosure.privacy import DisclosurePrivacy


def test_disclosure_provider():
    check_distribution_registry("metasyn-disclosure")


@mark.parametrize("fitter", DistributionRegistry.parse("metasyn-disclosure").fitters)
@mark.parametrize("privacy_kwargs", ({}, {"partition_size": 10}, {"partition_size": 15}))
def test_dist_validation(fitter, privacy_kwargs):
    np.random.seed(45)
    privacy = DisclosurePrivacy(**privacy_kwargs)
    # Testing empty series will fail with a convergence error, so skip these tests.
    try:
        check_fitter(fitter, privacy=privacy, provenance="metasyn-disclosure", test_empty=False)
    except TypeError:
        check_fitter(fitter, privacy=privacy, provenance="metasyn-disclosure")
