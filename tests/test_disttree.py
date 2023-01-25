import polars as pl

from metasynth.disttree import get_disttree
from metasynthcontrib.disclosure.disttree import DisclosureDistributionTree
from metasynthcontrib.disclosure.continuous import DisclosureUniform
from metasynthcontrib.disclosure.discrete import DisclosureDiscreteUniform
from metasynthcontrib.disclosure.categorical import DisclosureMultinoulli
from metasynthcontrib.disclosure.string import DisclosureFaker
from metasynthcontrib.disclosure.datetime import DisclosureDate, DisclosureTime,\
    DisclosureDateTime


def _fit_series(dist_class, dist_tree):
    dist = dist_class.default_distribution()
    if dist.var_type == "category":
        series = pl.Series([dist.draw() for _ in range(100)], pl.Categorical)
    else:
        series = pl.Series([dist.draw() for _ in range(100)])
    dist_tree.fit(series, dist.var_type)


def test_dist_tree():
    dist_tree = get_disttree("disclosure", n_avg=19)
    assert isinstance(dist_tree, DisclosureDistributionTree)
    assert dist_tree.privacy_kwargs["n_avg"] == 19

    dist_tree = get_disttree(DisclosureDistributionTree)
    assert isinstance(dist_tree, DisclosureDistributionTree)
    assert dist_tree.__class__.__name__ == "DisclosureDistributionTree"
    _fit_series(DisclosureUniform, dist_tree)
    _fit_series(DisclosureDiscreteUniform, dist_tree)
    _fit_series(DisclosureMultinoulli, dist_tree)
    _fit_series(DisclosureFaker, dist_tree)
    _fit_series(DisclosureDate, dist_tree)
    _fit_series(DisclosureTime, dist_tree)
    _fit_series(DisclosureDateTime, dist_tree)
