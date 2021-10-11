from abc import ABC
import numpy as np
from .base import ModelMetric
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


class ClassificationMetric(ModelMetric):
    """
    Base class for all metric which calculate classification score by training a model.

    Attributes
    ----------
    strategy: sklearn.Model, default `None`
              A classificatoini model to be trained to classify real vs synthetic
              data.
    """
    def __init__(self, strategy):
        self.strategy = strategy

    def _prepare_dataset(self, real, synthetic):
        """
        Function to prepare dataset to train model for all model based metrics.
        """

        real, synthetic = self._preprocess_data(real, synthetic)

        real_cls = np.ones((real_cat.shape[0]), )
        real_train_x, real_test_x, real_train_y, real_test_y = train_test_split(
            real, real_cls, test_size=0.2)

        synthetic_cls = np.zeros((synthetic_num.shape[0]), )
        synthetic_train_x, synthetic_test_x, synthetic_train_y, synthetic_test_y =  train_test_split(
            synthetic, synthetic_cls, test_size=0.2)

        X_train = np.concatenate([real_train_x, synthetic_train_x], axis=0)
        y_train = np.concatenate([real_train_y, synthetic_train_y], axis=0)

        X_test = np.concatenate([real_test_x, synthetic_test_x], axis=0)
        y_test = np.concatenate([real_test_y, synthetic_test_y], axis=0)

        return X_train, X_test, y_train, y_test


    def compute(self, real_data, synthetic_data, **kwargs):
        """
        Funciton to compute the score based on the strategy.

        Args
        ----
        real_data: `pandas.DataFrame`
                    The real dataset.

        synthetic_data: `pandas.DataFrame`
                         The synthetic dataset.
        """
        real_data, synthetic_data = self._validate_data(real_data, synthetic_data)

        X_train, X_test, y_train, y_test = self._prepare_dataset(real_data, synthetic_data)

        model = self.strategy(**kwargs).fit(X_train, y_train)
        score = model.score(X_test, y_test)

        return 1 - score


class RFCMetric(ClassificationMetric):
    def __init__(self):
        strategy = RandomForestClassifier
        super().__init__(strategy)
