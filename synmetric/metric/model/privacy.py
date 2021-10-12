import numpy as np
from .base import ModelMetric
from synmetric.utils import Dtypes
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split

class PrivacyMetric(ModelMetric):
    """
    Base class intherited by all privacy metric classes.

    Attributes
    ----------
    clf_strategy: sklearn.Model, default `None`
                  A classification model from the sklearn library used to
                  calculate score for categorcal columns.

    reg_strategy: sklearn.Model, default `None`
                  A regression model from the sklearn library used to
                  calculate score for numerical columns.
    """
    def __init__(self, clf_strategy=None, reg_strategy=None):
        self.clf_strategy = clf_strategy
        self.reg_strategy = reg_strategy

    def _prepare_dataset(self, real_data, synthetic_data, target, dtype):
        """
        Function to prepocess and prepare dataset to be used by models to calculate
        score.
        """
        real_data = real_data.dropna(axis=0, subset=[target])
        synthetic_data = synthetic_data.dropna(axis=0, subset=[target])

        real_label = real_data[target]
        synthetic_label = synthetic_data[target]

        real_data = real_data.drop([target], axis=1)
        synthetic_data = synthetic_data.drop([target], axis=1)

        real_data, synthetic_data = self._preprocess_data(real_data, synthetic_data)

        if dtype in Dtypes.CATEGORICAL:
            encoder = LabelEncoder()
            real_label = encoder.fit_transform(real_label)
            synthetic_label = encoder.transform(synthetic_label)

        return synthetic_data, real_data, synthetic_label, real_label

    def compute(self, real_data, synthetic_data, targets=None, dtypes=None):
        """
        Funciton to calculate scores using the models provided to `clf_strategy`
        and `reg_strategy`. The models used will depend on the `dtype` of `target`.

        Args
        ----
        real_data: `pandas.DataFrame`
                    The real dataset.

        synthetic_data: `pandas.DataFrame`
                         The synthetic dataset.

        targets: list[String]. default `None`
                 List of columns whose privacy score is to be calculated. If not
                 provided privacy score for all columns will be calculated.

        dtypes: list[String]. defaullt `None`
                List of dtypes of columns in the same sequence as provided in
                `targets`. If `targets` is `None` it will automatically be
                populated for all columns.

        Returns
        -------
        socres: dict.
                A dictionary of scores (-ve coefficient of determination) for each
                target. The values of each score lies between (-1.0, 1.0).
                The higher the better, it indicates how hard it is for a model to
                derive the `real` feature provided the `synthetic` one.
        """
        real_data, synthetic_data = self._validate_data(real_data, synthetic_data)

        if targets is None:
            dt = real_data.dtypes
            targets = list(dt.index)
            dtypes = list([d.name for d in dt.values])

        scores = dict()
        for target, dtype in zip(targets, dtypes):
            X_train, X_test, y_train, y_test = self._prepare_dataset(real_data,
                                                                     synthetic_data,
                                                                     target, dtype)

            if dtype in Dtypes.CATEGORICAL:
                model = self.clf_strategy().fit(X_train, y_train)
                scores[target] = -model.score(X_test, y_test)
            else:
                model = self.reg_strategy().fit(X_train, y_train)
                scores[target] = -model.score(X_test, y_test)

        return scores


class RFPrivacyMetric(PrivacyMetric):
    """
    Privacy metric which calculates score using `RandomForestRegressor` for
    numericla targets and `RandomForestClassifier` for categorical targets.
    """
    def __init__(self):
        clf_strategy = RandomForestClassifier
        reg_strategy = RandomForestRegressor

        super().__init__(clf_strategy, reg_strategy)
