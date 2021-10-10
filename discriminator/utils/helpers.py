from collections import Counter

import numpy as np



def get_density(real, synthetic):
    real_freq, synthetic_freq = Conter(real), Counter(synthetic)

    real_denstiy = []
    synthetic_density = []
    for key in real_freq.keys():
        real_denstiy.append(real_freq[key] / sum(real_freq.values()))

        # TODO: Handle the case when the category does not exist in synthetic data
        synthetic_denstiy.append(synthetic_freq[key] / sum(synthetic_freq.values()))

    return real_denstiy, synthetic_density
