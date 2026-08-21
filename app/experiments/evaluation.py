from collections.abc import Sequence


def hit_rate(
    predictions: Sequence[Sequence[str]],
    expected: Sequence[str],
) -> float:
    if not predictions or not expected:
        return 0.0

    total = min(len(predictions), len(expected))

    if total == 0:
        return 0.0

    hits = sum(
        expected_document in retrieved_documents
        for retrieved_documents, expected_document
        in zip(predictions[:total], expected[:total])
    )

    return hits / total


def precision_at_k(
    predictions: Sequence[Sequence[str]],
    expected: Sequence[str],
    k: int,
) -> float:
    if k <= 0 or not predictions or not expected:
        return 0.0

    total = min(len(predictions), len(expected))

    if total == 0:
        return 0.0

    correct = sum(
        1
        for retrieved_documents, expected_document
        in zip(predictions[:total], expected[:total])
        if expected_document in retrieved_documents[:k]
    )

    return correct / (total * k)


def hit_rate_at_k(
    relevant_documents: set[str],
    retrieved_documents: Sequence[str],
    k: int,
) -> float:
    if k <= 0:
        raise ValueError("k must be greater than zero")

    if not relevant_documents or not retrieved_documents:
        return 0.0

    retrieved_at_k = set(retrieved_documents[:k])

    return float(bool(relevant_documents & retrieved_at_k))


def recall_at_k(
    relevant_documents: set[str],
    retrieved_documents: Sequence[str],
    k: int,
) -> float:
    if k <= 0:
        raise ValueError("k must be greater than zero")

    if not relevant_documents or not retrieved_documents:
        return 0.0

    retrieved_at_k = set(retrieved_documents[:k])

    return (
        len(relevant_documents & retrieved_at_k)
        / len(relevant_documents)
    )


def reciprocal_rank(
    relevant_documents: set[str],
    retrieved_documents: Sequence[str],
) -> float:
    if not relevant_documents or not retrieved_documents:
        return 0.0

    for index, document in enumerate(
        retrieved_documents,
        start=1,
    ):
        if document in relevant_documents:
            return 1.0 / index

    return 0.0


def mean_reciprocal_rank(
    reciprocal_ranks: Sequence[float],
) -> float:
    if not reciprocal_ranks:
        return 0.0

    return sum(reciprocal_ranks) / len(reciprocal_ranks)
