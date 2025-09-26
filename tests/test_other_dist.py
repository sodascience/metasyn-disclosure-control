import datetime as dt

import numpy as np
import polars as pl
from metasyn.distribution.categorical import MultinoulliFitter
from metasyn.distribution.uniform import (
    DateTimeUniformFitter,
    DateUniformFitter,
    TimeUniformFitter,
)
from metasyn.privacy import BasicPrivacy
from pytest import mark

from metasyncontrib.disclosure.categorical import DisclosureMultinoulli
from metasyncontrib.disclosure.faker import DisclosureFaker
from metasyncontrib.disclosure.privacy import DisclosurePrivacy
from metasyncontrib.disclosure.uniform import DisclosureDate, DisclosureDateTime, DisclosureTime


@mark.parametrize(
    "fitter_norm,fitter_disc,input_type",
    [
        (DateUniformFitter, DisclosureDate, dt.date),
        (DateTimeUniformFitter, DisclosureDateTime, dt.datetime),
        (TimeUniformFitter, DisclosureTime, dt.time),
    ],
)
def test_datetime(fitter_norm, fitter_disc, input_type):
    dist_class = fitter_norm.distribution
    dist = dist_class.default_distribution()
    series = pl.Series([dist.draw() for _ in range(100)])
    dist_norm = fitter_norm(BasicPrivacy()).fit(series)
    dist_disc = fitter_disc(DisclosurePrivacy()).fit(series)
    assert dist_norm.lower < dist_disc.lower
    assert dist_norm.upper > dist_disc.upper
    assert isinstance(dist_norm.draw(), input_type)
    if not isinstance(dist_norm, dist_class):
        assert dist_norm.precision == dist_disc.precision


def test_categorical():
    np.random.seed(45)
    dist_norm = MultinoulliFitter.distribution.default_distribution()
    series = pl.Series([dist_norm.draw() for _ in range(40)], dtype=pl.Categorical)
    dist_norm = MultinoulliFitter(BasicPrivacy()).fit(series)
    dist_disc = DisclosureMultinoulli(DisclosurePrivacy()).fit(series)
    assert len(dist_norm.labels) > len(dist_disc.labels)


def test_string():
    dist = DisclosureFaker.distribution.default_distribution()
    series = pl.Series([dist.draw() for _ in range(100)])
    assert len(series)
    dist = DisclosureFaker(DisclosurePrivacy()).fit(series)
    assert isinstance(dist, DisclosureFaker.distribution)
    # assert len([dist.draw() for _ in range(100)]) == 100
