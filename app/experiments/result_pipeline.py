from datetime import datetime, timezone
from typing import Any

from app.experiments.error_analysis import (
    analyze_retrieval_errors,
    summarize_retrieval_errors,
)
from app.experiments.result_schemas import (
    ExperimentMetadata,
    ExperimentMetrics,
    ExperimentResult,
)
from app.experiments.schemas import BenchmarkDataset


def build_experiment_result(
    benchmark: BenchmarkDataset,
    metrics: dict[str, float],
    retrieval_results: dict[str, list[str]],
    experiment_id: str,
    configuration: dict[str, Any] | None = None,
    reproducibility: dict[str, Any] | None = None,
) -> ExperimentResult:
    """Build a validated experiment result from benchmark execution data."""

    errors = analyze_retrieval_errors(
        benchmark,
        retrieval_results,
    )

    error_summary = summarize_retrieval_errors(
        errors,
    )

    metadata = ExperimentMetadata(
        experiment_id=experiment_id,
        benchmark_name=benchmark.dataset_name,
        benchmark_version=benchmark.version,
        created_at=datetime.now(timezone.utc),
        configuration=configuration or {},
        reproducibility=reproducibility or {},
    )

    experiment_metrics = ExperimentMetrics(
        **metrics,
    )

    return ExperimentResult(
        metadata=metadata,
        metrics=experiment_metrics,
        error_summary=error_summary,
    )
