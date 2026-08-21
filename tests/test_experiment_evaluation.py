import pytest

from app.experiments.evaluation import (
    hit_rate,
    hit_rate_at_k,
    mean_reciprocal_rank,
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
)


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

def test_hit_rate_returns_zero_for_empty_predictions():
    assert hit_rate([], ["a"]) == 0.0

def test_hit_rate_returns_zero_for_empty_expected():
    assert hit_rate([["a"]], []) == 0.0

def test_precision_at_k_returns_zero_for_empty_predictions():
    assert precision_at_k([], ["a"], 1) == 0.0

def test_precision_at_k_returns_zero_for_empty_expected():
    assert precision_at_k([["a"]], [], 1) == 0.0

def test_hit_rate_at_k_returns_one_for_relevant_document():
    assert hit_rate_at_k(
        {"doc-1"},
        ["doc-2", "doc-1"],
        2,
    ) == 1.0

def test_hit_rate_at_k_returns_zero_when_not_found():
    assert hit_rate_at_k(
        {"doc-1"},
        ["doc-2"],
        1,
    ) == 0.0

def test_hit_rate_at_k_returns_zero_for_empty_inputs():
    assert hit_rate_at_k(set(), ["doc-1"], 1) == 0.0
    assert hit_rate_at_k({"doc-1"}, [], 1) == 0.0

def test_hit_rate_at_k_rejects_invalid_k():
    with pytest.raises(
        ValueError,
        match="k must be greater than zero",
    ):
        hit_rate_at_k(
            {"doc-1"},
            ["doc-1"],
            0,
        )

def test_recall_at_k_returns_expected_fraction():
    assert recall_at_k(
        {"doc-1", "doc-2"},
        ["doc-1", "doc-3"],
        2,
    ) == 0.5

def test_recall_at_k_returns_zero_for_empty_inputs():
    assert recall_at_k(set(), ["doc-1"], 1) == 0.0
    assert recall_at_k({"doc-1"}, [], 1) == 0.0

def test_recall_at_k_rejects_invalid_k():
    with pytest.raises(
        ValueError,
        match="k must be greater than zero",
    ):
        recall_at_k(
            {"doc-1"},
            ["doc-1"],
            0,
        )

def test_reciprocal_rank_returns_first_relevant_rank():
    assert reciprocal_rank(
        {"doc-2"},
        ["doc-1", "doc-2"],
    ) == 0.5

def test_reciprocal_rank_returns_zero_for_missing_document():
    assert reciprocal_rank(
        {"doc-3"},
        ["doc-1", "doc-2"],
    ) == 0.0

def test_reciprocal_rank_returns_zero_for_empty_inputs():
    assert reciprocal_rank(
        set(),
        ["doc-1"],
    ) == 0.0

    assert reciprocal_rank(
        {"doc-1"},
        [],
    ) == 0.0

def test_mean_reciprocal_rank():
    assert mean_reciprocal_rank(
        [1.0, 0.5, 0.0],
    ) == 0.5

def test_mean_reciprocal_rank_returns_zero_for_empty_values():
    assert mean_reciprocal_rank([]) == 0.0
