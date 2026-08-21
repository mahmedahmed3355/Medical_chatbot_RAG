from collections.abc import Sequence


def hit_rate(
    predictions: Sequence[Sequence[str]],
    expected: Sequence[str],
) -> float:
    """Calculate retrieval hit rate."""
    if not expected:
        return 0.0

    hits = sum(
        expected_item in predicted_items
        for predicted_items, expected_item in zip(
            predictions,
            expected,
            strict=True,
        )
    )

    return hits / len(expected)


def precision_at_k(
    predictions: Sequence[Sequence[str]],
    expected: Sequence[str],
    k: int,
) -> float:
    """Calculate mean precision@k for one relevant item per query."""
    if not expected or k <= 0:
        return 0.0

    scores = []

    for predicted_items, expected_item in zip(
        predictions,
        expected,
        strict=True,
    ):
        top_k = predicted_items[:k]

        if expected_item in top_k:
            scores.append(1.0 / len(top_k))
        else:
            scores.append(0.0)

    return sum(scores) / len(scores)
