from abc import ABC, abstractmethod

import pandas as pd

class StatisticalMetric(ABC):
    """
    An abstrction of a column metric.
    """

    def _select_dtypes(self, includes, real, synthetic):
         real_cols = list(real.select_dtypes(includes=inclues).columns)

         return real[real_cols], synthetic[real_cols]

    def _validate_data(self, real, synthetic):
        real_cols = list(real.columns)

        try:
            return real[real_cols], synthetic[real_cols]

        except: #TODO: Remove this wide except and make it a specific one
            raise ValueError("Real and synthetic data do not match")


    @classmethod
    @abstractmethod
    def compute(cls, real_data, synthetic_data):
        raise NotImplementedError()
