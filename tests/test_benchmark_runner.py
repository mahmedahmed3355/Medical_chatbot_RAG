import json

from app.experiments.benchmark import (
    evaluate_retrieval,
    load_benchmark,
)


def test_load_benchmark(tmp_path):
    benchmark_path = tmp_path / "benchmark.json"

    benchmark_path.write_text(
        json.dumps(
            {
                "dataset_name": "test",
                "version": "1.0",
                "cases": [],
            }
        ),
        encoding="utf-8",
    )

    benchmark = load_benchmark(
        benchmark_path
    )

    assert benchmark["dataset_name"] == "test"


def test_evaluate_retrieval():
    benchmark = {
        "cases": [
            {
                "id": "case-1",
                "relevant_documents": [
                    "doc-1"
                ],
            },
            {
                "id": "case-2",
                "relevant_documents": [
                    "doc-2"
                ],
            },
        ]
    }

    retrieval_results = {
        "case-1": [
            "doc-1",
            "doc-3",
        ],
        "case-2": [
            "doc-3",
            "doc-2",
        ],
    }

    metrics = evaluate_retrieval(
        benchmark,
        retrieval_results,
        2,
    )

    assert metrics["hit_rate_at_k"] == 1.0
    assert metrics["recall_at_k"] == 1.0
    assert metrics["mrr"] == 0.75
