import numpy as np
import pandas as pd

from  abc import ABC, abstractmethod

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder

from synmetric.utils import Dtypes
from synmetric.metric.base import BaseMetric


class ModelMetric(BaseMetric):
    """
    Abstract base class for all model based metric.
    """
    def _get_num_cat_columns(self, real_data):
        cat_cols = list(real_data.select_dtypes(include=Dtypes.CATEGORICAL).columns)
        num_cols = list(real_data.select_dtypes(include=Dtypes.NUMERIC).columns)

        return cat_cols, num_cols

    def _preprocess_data(self, real_data, synthetic_data):
        # THINK: Since the real and synthetic data are expected to have the same
        # distribution they must share the same imputer and label encoder
        cat_imputer = SimpleImputer(strategy='most_frequent')
        num_imputer = SimpleImputer(strategy='median')

        cat_cols, num_cols = self._get_num_cat_columns(real_data)

        real_cat, real_num = real_data[cat_cols], real_data[num_cols]
        synthetic_cat, synthetic_num = synthetic_data[cat_cols], synthetic_data[num_cols]

        real_cat = cat_imputer.fit_transform(real_cat)
        real_num = num_imputer.fit_transform(real_num)

        synthetic_cat = cat_imputer.transform(synthetic_cat)
        synthetic_num = num_imputer.transform(synthetic_num)

        for i in range(real_cat.shape[-1]):
            encoder = LabelEncoder()
            real_cat[:, i] = encoder.fit_transform(real_cat[:, i])
            synthetic_cat[:, i] = encoder.transform(synthetic_cat[:, i])

        real = np.concatenate([real_cat, real_num], axis=1)
        synthetic = np.concatenate([synthetic_cat, synthetic_num], axis=1)

        return real, synthetic
