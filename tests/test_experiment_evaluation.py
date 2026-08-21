from app.experiments.evaluation import hit_rate, precision_at_k


def test_hit_rate():
    predictions = [
        ["a", "b"],
        ["b", "c"],
        ["d", "e"],
    ]

    expected = [
        "a",
        "c",
        "x",
    ]

    assert hit_rate(predictions, expected) == 2 / 3


def test_precision_at_k():
    predictions = [
        ["a", "b", "c"],
        ["x", "y", "z"],
    ]

    expected = [
        "a",
        "y",
    ]

    assert precision_at_k(
        predictions,
        expected,
        2,
    ) == 0.5


def test_precision_at_k_returns_zero_for_invalid_k():
    assert precision_at_k(
        [["a"]],
        ["a"],
        0,
    ) == 0.0
