"""Base class for all disclosure control distributions."""


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
