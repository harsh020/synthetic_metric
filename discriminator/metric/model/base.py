from abc import ABC, abstractmethod

from sklearn.impute import SimpleImuter
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

class ModelMetric(ABC):
    """
    Base class for `TrainableMetric`.
    """

    def _prepare_dataset(self, real, synthetic):
        """
        Function to prepare dataset to train model for all model based metrics.
        """
        category = ['category', 'object']

        cat_cols = list(real.select_dtypes(includes=category).columns)
        num_cols = list(real.select_dtypes(excludes=category).columns)

        real_cat, real_num = real[cat_cols], real[num_cols]
        synthetic_cat, synthetic_num = synthetic[cat_cols], real[num_cols]

        real_cat = SimpleImuter(strategy='most_frequent').fit_transform(real_cat)
        real_cat = LabelEncoder().fit_transform(real_cat)
        real_num = SimpleImuter(strategy='median').fit_transform(real_num)

        real = np.cancatenate([real_cat, real_num], axis=1)
        real_cls = np.ones((real_cat.shape[0]), )
        real_train_x, real_test_x, real_train_y, real_train_y = train_test_split(
            real, real_cls, test_size=0.2)

        synthetic_cat = SimpleImuter(strategy='most_frequent').fit_transform(synthetic_cat)
        synthetic_cat = LabelEncoder().fit_transform(synthetic_cat)
        synthetic_num = SimpleImuter(strategy='median').fit_transform(synthetic_num)

        synthetic = np.concatenate([synthetic_cat, synthetic_num], axis=1)
        synthetic_cls = np.zeros((synthetic_num.shape[0]), )
        synthetic_train_x, synthetic_test_x, synthetic_train_y, synthetic_train_y =  train_test_split(
            real, real_cls, test_size=0.2)

        X_train = np.concatenate([real_train_x, synthetic_train_x], axis=0)
        y_train = np.concatenate([real_train_y, synthetic_train_y], axis=0)

        X_test = np.concatenate([real_test_x, synthetic_test_x], axis=0)
        y_test = np.concatenate([real_test_x, synthetic_test_y], axis=0)

        return X_train, X_test, y_train, y_test


    @classmethod
    @abstractmethod
    def compute(cls, real_data, synthetic_data):
        raise NotImplementedError()
