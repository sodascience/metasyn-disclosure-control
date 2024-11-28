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

    def comment(self, var):
        """Comment on a specific variable in the .toml GMF file.

        Parameters
        ----------
        var
            Variable to create a comment about.

        Returns
        -------
            A string with the comment.

        """
        base_msg = (
            f"The above parameters for column '{var.name}' were generated using disclosure "
            f"control\n# with a maximum dominance of 0.5 and data aggregated into partitions of "
            f"size {self.partition_size}\n"
            f"# before any parameters of the distribution were estimated.")

        intersect_lower = set(("lower", "upper")).intersection(  # noqa: C405
            var.distribution.to_dict()["parameters"])
        if len(intersect_lower) > 0:
            base_msg = base_msg[:-1]
            base_msg += (f"\n# The parameter(s) {', '.join(intersect_lower)} were estimated by the"
                         f" average of the {self.partition_size} lowest or highest values.")

        return base_msg
