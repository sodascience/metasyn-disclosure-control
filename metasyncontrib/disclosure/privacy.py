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

    def __init__(self, partition_size: int = 11, max_dominance: float = 0.5,
                 group_disclosure_threshold: float = 0.9):
        """Initialize the disclosure privacy object."""
        self.partition_size = partition_size
        self.max_dominance = max_dominance
        self.group_disclosure_threshold = group_disclosure_threshold

    def to_dict(self) -> dict:
        """Create a dictionary that gives the privacy type, and parameters."""
        return {"name": self.name,
                "parameters": {"partition_size": self.partition_size,
                               "max_dominance": self.max_dominance,
                               "group_disclosure_threshold": self.group_disclosure_threshold}}

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
            f"control\n# with a maximum dominance of {self.max_dominance}, data aggregated into "
            "partitions of "
            f"size {self.partition_size} and a group disclosure threshold "
            f"of {self.group_disclosure_threshold}\n"
            f"# before any parameters of the distribution were estimated.")

        intersect_lower = set(("lower", "upper")).intersection(  # noqa: C405
            var.distribution.to_dict()["parameters"])
        if len(intersect_lower) > 0:
            base_msg = base_msg[:-1]
            base_msg += (f"\n# The parameter(s) {', '.join(intersect_lower)} were estimated by the"
                         f" average of the {self.partition_size} lowest or highest values.")

        return base_msg
