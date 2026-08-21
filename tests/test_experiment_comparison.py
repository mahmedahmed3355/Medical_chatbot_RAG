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
