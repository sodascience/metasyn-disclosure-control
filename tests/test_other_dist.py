import polars as pl
from metasynth.distribution.datetime import UniformDateDistribution
from metasynth.distribution.datetime import UniformDateTimeDistribution
from metasynth.distribution.datetime import UniformTimeDistribution
from metasynthcontrib.disclosure.datetime import DisclosureDate, DisclosureDateTime, DisclosureTime
from pytest import mark
from metasynth.distribution.categorical import MultinoulliDistribution
from metasynthcontrib.disclosure.categorical import DisclosureMultinoulli
from metasynthcontrib.disclosure.string import DisclosureFaker


@mark.parametrize(
    "class_norm,class_disc",
    [(UniformDateDistribution, DisclosureDate),
     (UniformDateTimeDistribution, DisclosureDateTime),
     (UniformTimeDistribution, DisclosureTime)]
    )
def test_datetime(class_norm, class_disc):
    dist_norm = class_norm.default_distribution()
    series = pl.Series([dist_norm.draw() for _ in range(100)])
    dist_norm = class_norm.fit(series)
    dist_disc = class_disc.fit(series)
    assert dist_norm.start < dist_disc.start
    assert dist_norm.end > dist_disc.end
    if not isinstance(dist_norm, UniformDateDistribution):
        assert dist_norm.precision == dist_disc.precision


def test_categorical():
    dist_norm = MultinoulliDistribution.default_distribution()
    series = pl.Series([dist_norm.draw() for _ in range(40)], dtype=pl.Categorical)
    dist_norm = MultinoulliDistribution.fit(series)
    dist_disc = DisclosureMultinoulli.fit(series)
    assert len(dist_norm.labels) > len(dist_disc.labels)


def test_string():
    dist = DisclosureFaker.default_distribution()
    series = pl.Series([dist.draw() for _ in range(100)])
    assert len(series)
    dist = DisclosureFaker.fit(series, n_avg=11)
    assert isinstance(dist, DisclosureFaker)
    # assert len([dist.draw() for _ in range(100)]) == 100
