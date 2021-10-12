# synmetric

A WIP python package to compute quality and privacy of synthetic data.

[![pypi package](https://img.shields.io/badge/pypi%20package-0.2dev0-green)](https://test.pypi.org/project/synmetric/)
[![license](https://img.shields.io/badge/license-MIT-blue)](https://opensource.org/licenses/MIT)

**NOTE**
- **_Please not that this is currently a work in progress package. If you find any issues feel free to report them and fix them via a PR._**
- **_The docstrings are fairly verbose so kindly look at them, if one does not understand something kindly open an issue for the same._**

## Installation
- Currently the package is not hosted on `pypy`, so one needs to build from source as - 
  - Clone this repository, and type the following in terminal
  ```sh
  $ cd synthetic_metric
  $ pip install .
  ```
  
## Types of metrics
- **Statistical Metric:** These metrics are based on goodness of fit test such as `Chi-Squared` and `2 sample Kolmogorov–Smirnov`.
- **Model Metric:** These metrics calculate score by training models.
  - **Discriminator Metric:** These are model metrics that train classification models (currently only `RandomForestClassifier` is supported) to 
    discriminate bewtween synthetic and real data. That is, they tell how hard it is for a ML model to differentiate between real and synthetic data.
  - **Privacy Metric:** These are also model metrics that use train classificaiton model and/or regression model (the type of model depends on the dtype 
    of the feature whose privacy score is to be calculated) to determine privacy score. That is, they train model on the synthetic data to predict the 
    feature whose privacy score is to be calculated, and the same model is evaluated using real data. The score gives the idea of how robust can synthetic
    data be in terms of begin predicted by a ML model. Currently, support for `RandomForestClassifier` and `RandomForestRegressor` exist.

## Usage
Usage if fairly simple, just import the required metric and call either the object or `compute` method of the object with real and synthtic data passed 
as parameters.
```python
from synmetric.metric import CSTestMetric

metric = CSTestMetric()
score = metric.compute(real_data, synthetic_data)
```

## Creating custom metric
Creating you own new metrics is easy using `synmetric`.
- To build a custom Statistical Metric, 
  1. Create a strategy which calculates the score per column using a statistical test by inherting from `ColumnMetricStrategy`.
  ```python
  # NOTE: We are using more of a direct import, for absolute import use
  # from synmetric.metric.statistical.strategy import ColumnMetricStrategy
  from synmetric.metric import ColumnMetricStrategy
  
  class CustomColumnMetricStrategy(ColumnMetricStrategy):
    @staticmethod
    def compute(real_data, custom_data):
      # write code to calculate score for single column.
      ...
  ```
  
  2. Create a metric that calculate score for a `pandas.DataFrame` by inheriting from `StatisticalMetric`.
  ```python
  from synmetric.metric import StatisticalMetric
  from synmetric.utils import Dtypes
  
  def CustomStatisticalMetric(StatisticalMetric):
    def __init__(self):
      strategy = CustomColumnMetricStrategy
      dtypes = # put the dtype that the statistical method works on i.e, `Dtypes.CATEGORICAL` or `Dtypes.NUMERIC`.
      super().__init__(strategy, dtypes)
  ```
  
  3. Use the metric
  ```python
  metric = CustomStatisticalMetric()
  metric.compute(real_data, synthetic_data) 
  # on can also use metric(real_data, synthetic_data) to get the score, as the metrics are callable.
  ```

Similarly, custom metrics for other types of metrics can also be created. Other types of metrices do not have any dependency injection requirements, so, no
need ot create strategies for them.
