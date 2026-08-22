from app.experiments.result_pipeline import (
    build_experiment_result,
)
from app.experiments.schemas import (
    BenchmarkCase,
    BenchmarkDataset,
)


def create_benchmark() -> BenchmarkDataset:
    return BenchmarkDataset(
        dataset_name="retrieval-benchmark",
        version="1.0",
        cases=[
            BenchmarkCase(
                id="case-1",
                relevant_documents=[
                    "doc-1",
                ],
            ),
            BenchmarkCase(
                id="case-2",
                relevant_documents=[
                    "doc-2",
                    "doc-3",
                ],
            ),
        ],
    )


def create_metrics() -> dict[str, float]:
    return {
        "hit_rate_at_k": 0.5,
        "recall_at_k": 0.75,
        "mrr": 0.5,
    }


def test_build_experiment_result_returns_validated_result():
    result = build_experiment_result(
        benchmark=create_benchmark(),
        metrics=create_metrics(),
        retrieval_results={
            "case-1": [
                "wrong-doc",
            ],
            "case-2": [
                "doc-2",
            ],
        },
        experiment_id="experiment-1",
    )

    assert result.metadata.experiment_id == "experiment-1"
    assert result.metadata.benchmark_name == ("retrieval-benchmark")
    assert result.metadata.benchmark_version == "1.0"

    assert result.metrics.hit_rate_at_k == 0.5
    assert result.metrics.recall_at_k == 0.75
    assert result.metrics.mrr == 0.5


def test_build_experiment_result_summarizes_retrieval_errors():
    result = build_experiment_result(
        benchmark=create_benchmark(),
        metrics=create_metrics(),
        retrieval_results={
            "case-1": [],
            "case-2": [
                "doc-2",
            ],
        },
        experiment_id="experiment-errors",
    )

    assert result.error_summary == {
        "no_results": 1,
        "retrieval_miss": 0,
        "partial_retrieval": 1,
    }


def test_build_experiment_result_uses_empty_metadata_defaults():
    result = build_experiment_result(
        benchmark=create_benchmark(),
        metrics=create_metrics(),
        retrieval_results={
            "case-1": [
                "doc-1",
            ],
            "case-2": [
                "doc-2",
                "doc-3",
            ],
        },
        experiment_id="experiment-defaults",
    )

    assert result.metadata.configuration == {}
    assert result.metadata.reproducibility == {}


def test_build_experiment_result_preserves_metadata_configuration():
    configuration = {
        "top_k": 5,
        "embedding_model": "test-model",
    }

    reproducibility = {
        "seed": 42,
        "environment": "test",
    }

    result = build_experiment_result(
        benchmark=create_benchmark(),
        metrics=create_metrics(),
        retrieval_results={
            "case-1": [
                "doc-1",
            ],
            "case-2": [
                "doc-2",
                "doc-3",
            ],
        },
        experiment_id="experiment-configured",
        configuration=configuration,
        reproducibility=reproducibility,
    )

    assert result.metadata.configuration == configuration
    assert result.metadata.reproducibility == reproducibility


def test_build_experiment_result_validates_metrics():
    invalid_metrics = {
        "hit_rate_at_k": 1.5,
        "recall_at_k": 0.5,
        "mrr": 0.5,
    }

    try:
        build_experiment_result(
            benchmark=create_benchmark(),
            metrics=invalid_metrics,
            retrieval_results={
                "case-1": [
                    "doc-1",
                ],
                "case-2": [
                    "doc-2",
                ],
            },
            experiment_id="invalid-metrics",
        )
    except ValueError:
        pass
    else:
        raise AssertionError("Expected invalid metrics to raise ValueError")
