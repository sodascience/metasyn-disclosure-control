import polars as pl
from metasyn.distribution.continuous import (
    ExponentialDistribution,
    LogNormalDistribution,
    NormalDistribution,
    TruncatedNormalDistribution,
    UniformDistribution,
)
from metasyn.distribution.discrete import DiscreteUniformDistribution
from pytest import mark

from metasyncontrib.disclosure.continuous import (
    DisclosureExponential,
    DisclosureLogNormal,
    DisclosureNormal,
    DisclosureTruncatedNormal,
    DisclosureUniform,
)
from metasyncontrib.disclosure.discrete import DisclosureDiscreteUniform


@mark.parametrize(
    "dist_normal,dist_disclosure",
    [
        (UniformDistribution, DisclosureUniform),
        (TruncatedNormalDistribution, DisclosureTruncatedNormal),
        (NormalDistribution, DisclosureNormal),
        (LogNormalDistribution, DisclosureLogNormal),
        (ExponentialDistribution, DisclosureExponential),
        (DiscreteUniformDistribution, DisclosureDiscreteUniform),
        # (PoissonDistribution, DisclosurePoisson)
    ],
)
def test_continuous(dist_normal, dist_disclosure):
    unif = dist_normal.default_distribution()
    series = pl.Series([unif.draw() for _ in range(500)])
    unif = dist_normal.fit(series)
    unif_disc = dist_disclosure.fit(series)
    if unif.var_type == "continuous":
        assert unif.to_dict() != unif_disc.to_dict()

    # Test with outliers
    if unif.var_type == "continuous":
        series_out = pl.Series([x for x in series] + [99999999.0])
    else:
        series_out = pl.Series([x for x in series] + [99999999])
    unif_out = dist_normal.fit(series_out)
    unif_disc_out = dist_disclosure.fit(series_out)
    assert unif_out.to_dict() != unif.to_dict()

    # This will fail from time to time for discrete distributions
    assert unif_disc.to_dict() == unif_disc_out.to_dict()
