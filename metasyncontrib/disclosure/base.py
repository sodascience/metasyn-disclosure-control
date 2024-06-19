"""Base class for all disclosure control distributions."""

from metasyn.distribution.base import BaseDistribution


def metadist_disclosure():
    """Decorate class to create a distribution with disclosure control.

    Returns
    -------
    cls:
        Class with the appropriate class variables.

    """

    def _wrap(cls):
        cls.provenance = "metasyn-disclosure"
        cls.privacy = "disclosure"
        return cls

    return _wrap


class DisclosureConstantMixin(BaseDistribution):
    """Mixin class to overload fit method for constant distributions."""

    @classmethod
    def fit(cls, series, *args, partition_size: int = 11, **kwargs) -> BaseDistribution:  #pylint: disable=unused-argument
        """Fit constant distributions with disclosure control rules in place."""
        # NB: dominance rule ensures that constant distribution is essentially never
        # allowed under formal disclosure control. Always return default distribution.
        return cls.default_distribution()
