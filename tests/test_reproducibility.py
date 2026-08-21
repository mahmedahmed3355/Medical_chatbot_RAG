import random

import numpy as np

from app.experiments.reproducibility import set_global_seed


def test_global_seed_produces_reproducible_random_values():
    set_global_seed(42)

    first_python = random.random()
    first_numpy = np.random.rand()

    set_global_seed(42)

    second_python = random.random()
    second_numpy = np.random.rand()

    assert first_python == second_python
    assert first_numpy == second_numpy
