from collections import Counter

import numpy as np



def get_density(real, synthetic):
    real_freq, synthetic_freq = Counter(real), Counter(synthetic)

    real_density = []
    synthetic_density = []
    for key in real_freq.keys():
        real_density.append(real_freq[key] / sum(real_freq.values()))

        # TODO: Handle the case when the category does not exist in synthetic data
        synthetic_density.append(synthetic_freq[key] / sum(synthetic_freq.values()))

    return real_density, synthetic_density
