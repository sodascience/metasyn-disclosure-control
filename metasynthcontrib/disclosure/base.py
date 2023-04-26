"""Base class for all disclosure control distributions."""

from metasynth.distribution.base import BaseDistribution


class BaseDisclosure(BaseDistribution):
    """Disclosure class to set privacy and provenance of distributions."""
    privacy = "disclosure"
    provenance = "disclosure"
