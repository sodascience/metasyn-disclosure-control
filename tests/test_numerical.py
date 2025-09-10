import polars as pl
from metasyn.distribution.exponential import (
    ExponentialFitter,
)
from metasyn.distribution.normal import (
    ContinuousNormalFitter,
    ContinuousTruncatedNormalFitter,
    LogNormalFitter,
)
from metasyn.distribution.uniform import (
    ContinuousUniformFitter,
    DiscreteUniformFitter,
)
from metasyn.privacy import BasicPrivacy
from pytest import mark

from metasyncontrib.disclosure.exponential import DisclosureExponential
from metasyncontrib.disclosure.normal import (
    DisclosureLogNormal,
    DisclosureNormal,
    DisclosureTruncatedNormal,
)
from metasyncontrib.disclosure.privacy import DisclosurePrivacy
from metasyncontrib.disclosure.uniform import DisclosureContinuousUniform, DisclosureDiscreteUniform


@mark.parametrize(
    "fit_normal,fit_disclosure",
    [
        (ContinuousUniformFitter, DisclosureContinuousUniform),
        (ContinuousTruncatedNormalFitter, DisclosureTruncatedNormal),
        (ContinuousNormalFitter, DisclosureNormal),
        (LogNormalFitter, DisclosureLogNormal),
        (ExponentialFitter, DisclosureExponential),
        (DiscreteUniformFitter, DisclosureDiscreteUniform),
        # (PoissonDistribution, DisclosurePoisson)
    ],
)
def test_continuous(fit_normal, fit_disclosure):
    assert fit_normal.distribution == fit_disclosure.distribution
    dist_normal = fit_normal.distribution
    unif = dist_normal.default_distribution()
    series = pl.Series([unif.draw() for _ in range(500)])
    unif = fit_normal(BasicPrivacy()).fit(series)
    unif_disc = fit_disclosure(DisclosurePrivacy()).fit(series)
    if unif.var_type == "continuous":
        assert unif.to_dict() != unif_disc.to_dict()

    # Test with outliers
    if unif.var_type == "continuous":
        series_out = pl.Series([x for x in series] + [99999999.0])
    else:
        series_out = pl.Series([x for x in series] + [99999999])
    unif_out = fit_normal(BasicPrivacy()).fit(series_out)
    unif_disc_out = fit_disclosure(DisclosurePrivacy()).fit(series_out)
    assert unif_out.to_dict() != unif.to_dict()

    # This will fail from time to time for discrete distributions
    assert unif_disc.to_dict() == unif_disc_out.to_dict()
