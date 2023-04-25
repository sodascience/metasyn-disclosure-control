from pytest import mark

# from metasynth.testutils import check_dist_type
from metasynth.provider import get_distribution_provider
from metasynth.testutils import check_distribution


# @mark.parametrize(
#     "var_type", get_distribution_provider().all_var_types)
# def test_dist_tree(var_type):
#     check_dist_type("disclosure", var_type, n_avg=10)
#     check_dist_type("disclosure", var_type, n_avg=15)


@mark.parametrize(
    "distribution", get_distribution_provider("disclosure").distributions
)
@mark.parametrize(
    "privacy_kwargs", ({}, {"n_avg": 10}, {"n_avg": 15})
)
def test_dist_validation(distribution, privacy_kwargs):
    check_distribution(distribution, privacy="disclosure",
                       provenance="disclosure",
                       **privacy_kwargs)
