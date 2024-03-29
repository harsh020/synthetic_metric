import numpy as np
import pandas as pd
from scipy.stats import chisquare, ks_2samp, anderson_ksamp, f_oneway

from .base import ColumnMetricStrategy
from synmetric.utils import get_density


class CSTestColumnMetricStrategy(ColumnMetricStrategy):
    """
    Performes Chi Square test for goodness of fit.
    Computes chi squared pvalue between categorical column of
    real and synthetic data.
    """

    @staticmethod
    def compute(real_data, synthetic_data):
        """
        Function to calculate pvalue of chi squared test for a given
        categorical column from real and synthetic data.

        Args
        ----
        real_data: Union[numpy.array, pandas.Series]
                   A single dimension data from the real dataset.

        synthetic_data: Union[numpy.array, pandas.Series]
                        A single dimension data from the synthetic dataset.

        Return
        ------
        pvalue: float
                The pvalue of the chi squared test. This value lies between
                (0.0, 1.0). The greater the better.
        """
        f_exp, f_obs = get_density(real_data, synthetic_data)

        _, pvalue = chisquare(f_obs, f_exp)

        return pvalue


class KSTestColumnMetricStrategy(ColumnMetricStrategy):
    """
    Performs the two-sample Kolmogorov-Smirnov test for goodness of fit.
    Computes Kolmogorov-Smirnov's pvalue for continuous columns between
    real and synthetic data and returns 1 - pvalue.
    """

    @staticmethod
    def compute(real_data, synthetic_data):
        """
        Function to calculate pvalue of Kolmogorov-Smirnov test for a given
        continuous column from real and synthetic data.

        Args
        ----
        real_data: Union[numpy.array, pandas.Series]
                   A single dimension data from the real dataset.

        synthetic_data: Union[numpy.array, pandas.Series]
                        A single dimension data from the synthetic dataset.

        Return
        ------
        statistic: float
                The 1 - Kolmogorov-Smirnov statistic. This value lies between
                (0.0, 1.0). The greater the better.
        """
        real_data = pd.Series(real_data).fillna(0.0)
        synthetic_data = pd.Series(synthetic_data).fillna(0.0)

        statistic, _ = ks_2samp(real_data, synthetic_data)

        return 1 - statistic


class ADTestColumnMetricStrategy(ColumnMetricStrategy):
    """
    Performs the Anderson-Darling test which tests the null hypothesis that a
    sample is drawn from a population that follows a particular distribution.
    real and synthetic data and returns statistic.
    """

    @staticmethod
    def compute(real_data, synthetic_data):
        """
        Function to calculate pvalue of oneway ANOVA test for a given
        continuous column from real and synthetic data.

        Args
        ----
        real_data: Union[numpy.array, pandas.Series]
                   A single dimension data from the real dataset.

        synthetic_data: Union[numpy.array, pandas.Series]
                        A single dimension data from the synthetic dataset.

        Return
        ------
        statistic: float
                The Anderson Test test statistic.
        """
        real_data = pd.Series(real_data).fillna(0.0)
        synthetic_data = pd.Series(synthetic_data).fillna(0.0)

        statistic, _ = anderson_ksamp(real_data, synthetic_data)

        return statistic


class ANOVATestColumnMetricStrategy(ColumnMetricStrategy):
    """
    Performs the ANOVA test which tests the null hypothesis that a
    sample is drawn from a population that follows a particular distribution.
    real and synthetic data and returns statistic.
    """

    @staticmethod
    def compute(real_data, synthetic_data):
        """
        Function to calculate pvalue of oneway ANOVA test for a given
        continuous column from real and synthetic data.

        Args
        ----
        real_data: Union[numpy.array, pandas.Series]
                   A single dimension data from the real dataset.

        synthetic_data: Union[numpy.array, pandas.Series]
                        A single dimension data from the synthetic dataset.

        Return
        ------
        statistic: float
                The ANOVA test statistic.
        """
        real_data = pd.Series(real_data).fillna(0.0)
        synthetic_data = pd.Series(synthetic_data).fillna(0.0)

        statistic, _ = f_oneway(real_data, synthetic_data)

        return statistic
