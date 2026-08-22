from datetime import datetime

import pytest
from pydantic import ValidationError

from app.experiments.result_schemas import (
    ExperimentMetadata,
    ExperimentMetrics,
    ExperimentResult,
)


def create_valid_metadata() -> ExperimentMetadata:
    return ExperimentMetadata(
        experiment_id="experiment-001",
        benchmark_name="medical-retrieval",
        benchmark_version="1.0",
        created_at=datetime(
            2026,
            1,
            1,
        ),
        configuration={
            "k": 5,
        },
        reproducibility={
            "seed": 42,
        },
    )


def create_valid_metrics() -> ExperimentMetrics:
    return ExperimentMetrics(
        hit_rate_at_k=0.8,
        recall_at_k=0.7,
        mrr=0.6,
    )


def test_experiment_metrics_accepts_valid_values():
    metrics = create_valid_metrics()

    assert metrics.hit_rate_at_k == 0.8
    assert metrics.recall_at_k == 0.7
    assert metrics.mrr == 0.6


@pytest.mark.parametrize(
    (
        "field_name",
        "value",
    ),
    [
        (
            "hit_rate_at_k",
            -0.1,
        ),
        (
            "hit_rate_at_k",
            1.1,
        ),
        (
            "recall_at_k",
            -0.1,
        ),
        (
            "recall_at_k",
            1.1,
        ),
        (
            "mrr",
            -0.1,
        ),
        (
            "mrr",
            1.1,
        ),
    ],
)
def test_experiment_metrics_rejects_values_outside_unit_interval(
    field_name: str,
    value: float,
):
    metric_values = {
        "hit_rate_at_k": 0.8,
        "recall_at_k": 0.7,
        "mrr": 0.6,
    }

    metric_values[field_name] = value

    with pytest.raises(
        ValidationError,
    ):
        ExperimentMetrics(
            **metric_values,
        )


def test_experiment_metadata_normalizes_required_text():
    metadata = ExperimentMetadata(
        experiment_id="  experiment-001  ",
        benchmark_name="  medical-retrieval  ",
        benchmark_version="  1.0  ",
        created_at=datetime(
            2026,
            1,
            1,
        ),
    )

    assert metadata.experiment_id == "experiment-001"
    assert metadata.benchmark_name == "medical-retrieval"
    assert metadata.benchmark_version == "1.0"


@pytest.mark.parametrize(
    "field_name",
    [
        "experiment_id",
        "benchmark_name",
        "benchmark_version",
    ],
)
def test_experiment_metadata_rejects_blank_required_text(
    field_name: str,
):
    metadata_values = {
        "experiment_id": "experiment-001",
        "benchmark_name": "medical-retrieval",
        "benchmark_version": "1.0",
        "created_at": datetime(
            2026,
            1,
            1,
        ),
    }

    metadata_values[field_name] = "   "

    with pytest.raises(
        ValidationError,
    ):
        ExperimentMetadata(
            **metadata_values,
        )


def test_experiment_metadata_uses_empty_defaults():
    metadata = ExperimentMetadata(
        experiment_id="experiment-001",
        benchmark_name="medical-retrieval",
        benchmark_version="1.0",
        created_at=datetime(
            2026,
            1,
            1,
        ),
    )

    assert metadata.configuration == {}
    assert metadata.reproducibility == {}


def test_experiment_result_accepts_valid_data():
    result = ExperimentResult(
        metadata=create_valid_metadata(),
        metrics=create_valid_metrics(),
        error_summary={
            "no_results": 1,
            "retrieval_miss": 2,
            "partial_retrieval": 0,
        },
    )

    assert result.metadata.experiment_id == "experiment-001"
    assert result.metrics.hit_rate_at_k == 0.8
    assert result.error_summary == {
        "no_results": 1,
        "retrieval_miss": 2,
        "partial_retrieval": 0,
    }


def test_experiment_result_uses_empty_error_summary_by_default():
    result = ExperimentResult(
        metadata=create_valid_metadata(),
        metrics=create_valid_metrics(),
    )

    assert result.error_summary == {}


def test_experiment_result_rejects_blank_error_summary_key():
    with pytest.raises(
        ValidationError,
    ):
        ExperimentResult(
            metadata=create_valid_metadata(),
            metrics=create_valid_metrics(),
            error_summary={
                "   ": 1,
            },
        )


def test_experiment_result_rejects_negative_error_summary_count():
    with pytest.raises(
        ValidationError,
    ):
        ExperimentResult(
            metadata=create_valid_metadata(),
            metrics=create_valid_metrics(),
            error_summary={
                "retrieval_miss": -1,
            },
        )
