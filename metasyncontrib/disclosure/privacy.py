"""Disclosure control privacy class."""

from __future__ import annotations

from metasyn.privacy import BasePrivacy


class DisclosurePrivacy(BasePrivacy):
    """Disclosure control privacy class that uses micro-aggregation.

    Arguments:
    ---------
    partition_size:
        Number of elements to aggregate into one bin. Higher values
        mean better protected privacy, but lower statistical accuracy.

    """

    name = "disclosure"

    def __init__(self, partition_size: int = 11):
        """Initialize the disclosure privacy object."""
        self.partition_size = partition_size

    def to_dict(self) -> dict:
        """Create a dictionary that gives the privacy type, and parameters."""
        return {"name": self.name, "parameters": {"partition_size": self.partition_size}}
