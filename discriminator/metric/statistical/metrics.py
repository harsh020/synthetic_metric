import numpy as np
import pandas as pd

from .base import StatisticalMetric
from .strategy import CSTestColumnMetricStrategy
from .strategy import KSTestColumnMetricStrategy
from rs_discriminator.utils.constants import Dtypes


class TabularMetric(ABC, StatisticalMetric):
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
    strategy = None
    dtypes = None

    @classmethod
    def compute(cls, real_data, synthetic_data):
        """
        Funciton to compute the score based on the strategy.

        Args
        ----
        real_data: `pandas.DataFrame`
                    The real dataset.

        synthetic_data: `pandas.DataFrame`
                         The synthetic dataset.
        """
        cls._validate_data(real_data, synthetic_data)

        real, synthetic = cls._select_dtypes(cls.dtypes, real_data, synthetic_data)

        vals = []
        for col in real.columns:
            vals.append(cls.column_metric.compute(real[col], synthetic[col]))

        return np.nanmean(vals)


class CSTestMetric(TabularMetric):
    """
    Metric for calculating chi squares test score on given real and synthetic dataframes.
    """
    strategy = CSTestColumnMetricStrategy
    dtypes = Dtypes.CATEGORICAL

class KSTestMetric(TabularMetric):
    """
    Metric for calculating Kolmogorov-Smirnov test score on given real and synthetic dataframes.
    """
    strategy = KSTestColumnMetricStrategy
    dtypes = Dtypes.NUMERIC
