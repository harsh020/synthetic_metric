from abc import ABC, abstractmethod

class ColumnMetricStrategy(ABC):
    """
    An abstrction of a column metric strategy.
    """

    @staticmethod
    @abstractmethod
    def compute(real_data, synthetic_data):
        raise NotImplementedError()
