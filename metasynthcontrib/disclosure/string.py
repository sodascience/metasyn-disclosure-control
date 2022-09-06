from metasynth.distribution.faker import FakerDistribution


class DisclosureFakerDistribution(FakerDistribution):
    @classmethod
    def _fit(cls, values, faker_type: str="city", locale: str="en_US", n_avg: int=10):
        return super(DisclosureFakerDistribution, cls)._fit(
            values, faker_type=faker_type, locale=locale)
