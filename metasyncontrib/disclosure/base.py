"""Base class for all disclosure control distributions."""

def disclosure_fitter():
    """Decorate class to create a distribution with disclosure control.

    Returns
    -------
    cls:
        Class with the appropriate class variables.

    """

    def _wrap(cls):
        cls.privacy_type = "disclosure"
        return cls

    return _wrap

