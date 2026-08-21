import pytest

from app.experiments.comparison import (
    compare_experiments,
)


def test_compare_experiments():
    baseline = {
        "metrics": {
            "hit_rate_at_k": 0.8,
            "recall_at_k": 0.7,
            "mrr": 0.6,
        }
    }

    candidate = {
        "metrics": {
            "hit_rate_at_k": 0.9,
            "recall_at_k": 0.8,
            "mrr": 0.7,
        }
    }

    comparison = compare_experiments(
        baseline,
        candidate,
    )

    assert comparison["hit_rate_at_k"] == 0.1
    assert comparison["recall_at_k"] == 0.1
    assert comparison["mrr"] == 0.1


def test_compare_experiments_rejects_invalid_baseline_metrics():
    with pytest.raises(
        ValueError,
        match="Baseline metrics must be a mapping",
    ):
        compare_experiments(
            {"metrics": ["invalid"]},
            {"metrics": {}},
        )


def test_compare_experiments_rejects_invalid_candidate_metrics():
    with pytest.raises(
        ValueError,
        match="Candidate metrics must be a mapping",
    ):
        compare_experiments(
            {"metrics": {}},
            {"metrics": ["invalid"]},
        )


def test_compare_experiments_only_compares_common_metrics():
    comparison = compare_experiments(
        {
            "metrics": {
                "accuracy": 0.5,
                "recall": 0.4,
            }
        },
        {
            "metrics": {
                "accuracy": 0.8,
                "precision": 0.9,
            }
        },
    )

    assert comparison == {
        "accuracy": 0.3,
    }
