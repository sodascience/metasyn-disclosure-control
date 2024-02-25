import numpy as np
import polars as pl
from metasyn.distribution.categorical import MultinoulliDistribution
from metasyn.distribution.datetime import (
    DateTimeUniformDistribution,
    DateUniformDistribution,
    TimeUniformDistribution,
)
from pytest import mark

from metasyncontrib.disclosure.categorical import DisclosureMultinoulli
from metasyncontrib.disclosure.datetime import DisclosureDate, DisclosureDateTime, DisclosureTime
from metasyncontrib.disclosure.faker import DisclosureFaker


@mark.parametrize(
    "class_norm,class_disc",
    [
        (DateUniformDistribution, DisclosureDate),
        (DateTimeUniformDistribution, DisclosureDateTime),
        (TimeUniformDistribution, DisclosureTime),
    ],
)
def test_datetime(class_norm, class_disc):
    dist_norm = class_norm.default_distribution()
    series = pl.Series([dist_norm.draw() for _ in range(100)])
    dist_norm = class_norm.fit(series)
    dist_disc = class_disc.fit(series)
    assert dist_norm.lower < dist_disc.lower
    assert dist_norm.upper > dist_disc.upper
    if not isinstance(dist_norm, DateUniformDistribution):
        assert dist_norm.precision == dist_disc.precision


def test_categorical():
    np.random.seed(45)
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
