import json
from pathlib import Path

from app.experiments.evaluation import (
    hit_rate_at_k,
    mean_reciprocal_rank,
    recall_at_k,
    reciprocal_rank,
)
from app.experiments.schemas import BenchmarkDataset


def load_benchmark(
    path: Path,
) -> BenchmarkDataset:
    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    return BenchmarkDataset.model_validate(data)


def evaluate_retrieval(
    benchmark: BenchmarkDataset,
    retrieval_results: dict[str, list[str]],
    k: int,
) -> dict[str, float]:
    hit_scores: list[float] = []
    recall_scores: list[float] = []
    reciprocal_ranks: list[float] = []

    for case in benchmark.cases:
        case_id = case.id

        relevant_documents = set(case.relevant_documents)

        retrieved_documents = retrieval_results.get(
            case_id,
            [],
        )

        hit_scores.append(
            hit_rate_at_k(
                relevant_documents,
                retrieved_documents,
                k,
            )
        )

        recall_scores.append(
            recall_at_k(
                relevant_documents,
                retrieved_documents,
                k,
            )
        )

        reciprocal_ranks.append(
            reciprocal_rank(
                relevant_documents,
                retrieved_documents,
            )
        )

    total_cases = len(benchmark.cases)

    if total_cases == 0:
        raise ValueError("Benchmark must contain at least one case")

    return {
        "hit_rate_at_k": (sum(hit_scores) / total_cases),
        "recall_at_k": (sum(recall_scores) / total_cases),
        "mrr": mean_reciprocal_rank(reciprocal_ranks),
    }
