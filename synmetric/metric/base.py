from abc import ABC, abstractmethod


class BaseMetric(ABC):
    """
    An abstract class any type of metrics. Any and all metrics
     needs to inherit from it.
    """
    def __call__(self, real, synthetic, **kwargs):
        return self.compute(real, synthetic, **kwargs)

    def _select_dtypes(self, includes, real, synthetic):
         real_cols = list(real.select_dtypes(include=includes).columns)

         return real[real_cols], synthetic[real_cols]

    def _validate_data(self, real, synthetic):
        real_cols = list(real.columns)

        try:
            return real[real_cols], synthetic[real_cols]

        except: #TODO: Remove this wide except and make it a specific one
            raise ValueError("Real and synthetic data do not match")

    @abstractmethod
    def compute(self, real_data, synthetic_data):
        raise NotImplementedError()
