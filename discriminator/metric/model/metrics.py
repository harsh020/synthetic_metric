from abc import ABC
import numpy as np
from .base import ModelMetric
from sklearn.ensemble import RandomForestClassifier


class TrainableMetric(ABC, ModelMetric):
    """
    Base class for all metric which calculate score by training a model.

    Attributes
    ----------
    strategy: sklearn.Model, default `None`
              A classificatoini model to be trained to classify real vs synthetic
              data.
    """
    strategy = None

    @classmethod
    def compute(cls, real_data, synthetic_data, **kwargs):
        """
        Funciton to compute the score based on the strategy.

        Args
        ----
        real_data: `pandas.DataFrame`
                    The real dataset.

        synthetic_data: `pandas.DataFrame`
                         The synthetic dataset.
        """
        X_train, X_test, y_train, y_test = cls._prepare_dataset(real_data, synthetic_data)

        model = cls.strategy(**kwargs).fit(X_train, y_test)
        score = model.evaluate(X_test, y_test)

        return 1 - score


class RFCMetric(TrainableMetric):
    strategy = RandomForestClassifier
