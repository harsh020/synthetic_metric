import numpy as np
import pandas as pd

from .strategy import CSTestColumnMetricStrategy
from .strategy import KSTestColumnMetricStrategy

from synmetric.utils import Dtypes
from synmetric.metric.base import BaseMetric


class StatisticalMetric(BaseMetric):
    """
    An abstract class for concrete tabular metrics. Any and all metrics
    to calculate score for tabular data needs to inherit from it.

    Attributes
    ----------
    strategy: ColumnMetricStrategy
              Defines the base class to calculate scores per columns.

    dtypes: utils.Dtypes
            Defines the datatypes to be used by the strategy, i.e, the type of
            column the column metric will work on.
    """
    def __init__(self, strategy, dtypes):
        self.strategy = strategy
        self.dtypes = dtypes

    def compute(self, real_data, synthetic_data):
        """
        Funciton to compute the score based on the strategy.

        Args
        ----
        real_data: `pandas.DataFrame`
                    The real dataset.

        synthetic_data: `pandas.DataFrame`
                         The synthetic dataset.
        """
        self._validate_data(real_data, synthetic_data)

        real, synthetic = self._select_dtypes(self.dtypes, real_data, synthetic_data)

        vals = []
        for col in real.columns:
            vals.append(self.strategy.compute(real[col], synthetic[col]))

        return np.nanmean(vals)


class CSTestMetric(StatisticalMetric):
    """
    Metric for calculating chi squares test score on given real and synthetic dataframes.
    """
    def __init__(self):
        strategy = CSTestColumnMetricStrategy
        dtypes = Dtypes.CATEGORICAL
        super().__init__(strategy, dtypes)

class KSTestMetric(StatisticalMetric):
    """
    Metric for calculating Kolmogorov-Smirnov test score on given real and synthetic dataframes.
    """
    def __init__(self):
        strategy = KSTestColumnMetricStrategy
        dtypes = Dtypes.NUMERIC
        super().__init__(strategy, dtypes)
