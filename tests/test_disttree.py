from pytest import mark

from metasynth.testutils import check_dist_type
from metasynth.disttree import get_disttree


@mark.parametrize(
    "var_type", get_disttree().all_var_types)
def test_dist_tree(var_type):
    check_dist_type("disclosure", var_type, n_avg=10)
    check_dist_type("disclosure", var_type, n_avg=15)
