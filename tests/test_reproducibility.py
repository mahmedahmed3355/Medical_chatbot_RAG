import os
import random
import sys
import types

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

def test_global_seed_sets_python_hash_seed():
    set_global_seed(123)

    assert os.environ["PYTHONHASHSEED"] == "123"

def test_global_seed_handles_import_error(monkeypatch):
    monkeypatch.setitem(
        sys.modules,
        "torch",
        None,
    )

    set_global_seed(7)

    assert os.environ["PYTHONHASHSEED"] == "7"

def test_global_seed_configures_available_torch(monkeypatch):
    calls = []

    fake_cuda = types.SimpleNamespace(
        is_available=lambda: True,
        manual_seed=lambda seed: calls.append(
            ("cuda_manual_seed", seed)
        ),
        manual_seed_all=lambda seed: calls.append(
            ("cuda_manual_seed_all", seed)
        ),
    )

    fake_cudnn = types.SimpleNamespace(
        deterministic=False,
        benchmark=True,
    )

    fake_torch = types.SimpleNamespace(
        manual_seed=lambda seed: calls.append(
            ("manual_seed", seed)
        ),
        cuda=fake_cuda,
        backends=types.SimpleNamespace(
            cudnn=fake_cudnn
        ),
    )

    monkeypatch.setitem(
        sys.modules,
        "torch",
        fake_torch,
    )

    set_global_seed(99)

    assert ("manual_seed", 99) in calls
    assert ("cuda_manual_seed", 99) in calls
    assert ("cuda_manual_seed_all", 99) in calls
    assert fake_cudnn.deterministic is True
    assert fake_cudnn.benchmark is False
