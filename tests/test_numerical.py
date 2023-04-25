from pytest import mark
import polars as pl

from metasynth.distribution.continuous import UniformDistribution, TruncatedNormalDistribution
from metasynth.distribution.continuous import NormalDistribution, LogNormalDistribution
from metasynth.distribution.continuous import ExponentialDistribution
from metasynthcontrib.disclosure.continuous import DisclosureUniform, DisclosureTruncatedNormal
from metasynthcontrib.disclosure.continuous import DisclosureNormal, DisclosureLogNormal
from metasynthcontrib.disclosure.continuous import DisclosureExponential
from metasynthcontrib.disclosure.discrete import DisclosureDiscreteUniform
from metasynthcontrib.disclosure.discrete import DisclosurePoisson

from metasynth.distribution.discrete import DiscreteUniformDistribution,\
    PoissonDistribution
from metasynth.distribution.base import ContinuousDistribution


@mark.parametrize(
    "dist_normal,dist_disclosure",
    [(UniformDistribution, DisclosureUniform),
     (TruncatedNormalDistribution, DisclosureTruncatedNormal),
     (NormalDistribution, DisclosureNormal),
     (LogNormalDistribution, DisclosureLogNormal),
     (ExponentialDistribution, DisclosureExponential),
     (DiscreteUniformDistribution, DisclosureDiscreteUniform),
     # (PoissonDistribution, DisclosurePoisson)
     ]
)
def test_continuous(dist_normal, dist_disclosure):
    unif = dist_normal.default_distribution()
    series = pl.Series([unif.draw() for _ in range(500)])
    unif = dist_normal.fit(series)
    unif_disc = dist_disclosure.fit(series)
    if isinstance(unif, ContinuousDistribution):
        assert unif.to_dict() != unif_disc.to_dict()

    # Test with outliers
    if isinstance(unif, ContinuousDistribution):
        series_out = pl.Series([x for x in series] + [99999999.0])
    else:
        series_out = pl.Series([x for x in series] + [99999999])
    unif_out = dist_normal.fit(series_out)
    unif_disc_out = dist_disclosure.fit(series_out)
    assert unif_out.to_dict() != unif.to_dict()

    # This will fail from time to time for discrete distributions
    assert unif_disc.to_dict() == unif_disc_out.to_dict()
