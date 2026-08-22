import pytest

from app.experiments.evaluation import (
    hit_rate_at_k,
    mean_reciprocal_rank,
    recall_at_k,
    reciprocal_rank,
)


def test_hit_rate_at_k_returns_one_when_relevant_found():
    score = hit_rate_at_k(
        {"doc-2"},
        ["doc-1", "doc-2"],
        2,
    )

    assert score == 1.0


def test_hit_rate_at_k_returns_zero_when_missing():
    score = hit_rate_at_k(
        {"doc-3"},
        ["doc-1", "doc-2"],
        2,
    )

    assert score == 0.0


def test_recall_at_k():
    score = recall_at_k(
        {"doc-1", "doc-2"},
        ["doc-1", "doc-3", "doc-2"],
        2,
    )

    assert score == 0.5


def test_reciprocal_rank():
    score = reciprocal_rank(
        {"doc-3"},
        ["doc-1", "doc-2", "doc-3"],
    )

    assert score == pytest.approx(1 / 3)


def test_mean_reciprocal_rank():
    score = mean_reciprocal_rank([1.0, 0.5, 0.0])

    assert score == 0.5


def test_metrics_reject_invalid_k():
    with pytest.raises(ValueError):
        hit_rate_at_k(
            {"doc-1"},
            ["doc-1"],
            0,
        )
