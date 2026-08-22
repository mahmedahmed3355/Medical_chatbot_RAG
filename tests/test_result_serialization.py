import json

import pytest

from app.experiments.result_schemas import (
    ExperimentMetadata,
    ExperimentMetrics,
    ExperimentResult,
)
from app.experiments.result_serialization import (
    deserialize_experiment_result,
    load_experiment_result,
    save_experiment_result,
    serialize_experiment_result,
)


def create_experiment_result() -> ExperimentResult:
    return ExperimentResult(
        metadata=ExperimentMetadata(
            experiment_id="experiment-001",
            benchmark_name="medical-retrieval",
            benchmark_version="1.0",
            created_at="2026-08-22T00:00:00Z",
            configuration={
                "top_k": 5,
            },
            reproducibility={
                "seed": 42,
            },
        ),
        metrics=ExperimentMetrics(
            hit_rate_at_k=0.8,
            recall_at_k=0.9,
            mrr=0.85,
        ),
        error_summary={
            "no_results": 1,
            "retrieval_miss": 2,
            "partial_retrieval": 0,
        },
    )


def test_serialize_experiment_result_returns_json_compatible_record():
    result = create_experiment_result()

    record = serialize_experiment_result(
        result,
    )

    assert record["metadata"]["experiment_id"] == "experiment-001"
    assert record["metadata"]["created_at"] == "2026-08-22T00:00:00Z"
    assert record["metrics"]["hit_rate_at_k"] == 0.8
    assert record["error_summary"]["retrieval_miss"] == 2

    json.dumps(record)


def test_deserialize_experiment_result_reconstructs_valid_result():
    original = create_experiment_result()

    record = serialize_experiment_result(
        original,
    )

    reconstructed = deserialize_experiment_result(
        record,
    )

    assert reconstructed == original


def test_deserialize_experiment_result_rejects_invalid_record():
    with pytest.raises(Exception):
        deserialize_experiment_result(
            {
                "metadata": {},
            }
        )


def test_save_experiment_result_creates_parent_directories(
    tmp_path,
):
    result = create_experiment_result()

    output_path = tmp_path / "nested" / "experiments" / "result.json"

    save_experiment_result(
        result,
        output_path,
    )

    assert output_path.exists()


def test_save_experiment_result_writes_deterministic_json(
    tmp_path,
):
    result = create_experiment_result()

    output_path = tmp_path / "result.json"

    save_experiment_result(
        result,
        output_path,
    )

    content = output_path.read_text(
        encoding="utf-8",
    )

    assert content.endswith("\n")

    loaded_json = json.loads(content)

    assert loaded_json == serialize_experiment_result(
        result,
    )

    assert content.index('"error_summary"') < content.index('"metadata"')


def test_load_experiment_result_round_trip(
    tmp_path,
):
    original = create_experiment_result()

    output_path = tmp_path / "result.json"

    save_experiment_result(
        original,
        output_path,
    )

    loaded = load_experiment_result(
        output_path,
    )

    assert loaded == original


def test_load_experiment_result_rejects_non_object_json(
    tmp_path,
):
    input_path = tmp_path / "invalid.json"

    input_path.write_text(
        '["not", "an", "object"]',
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="must contain an object",
    ):
        load_experiment_result(
            input_path,
        )


def test_load_experiment_result_rejects_invalid_experiment_data(
    tmp_path,
):
    input_path = tmp_path / "invalid-result.json"

    input_path.write_text(
        json.dumps(
            {
                "metadata": {},
                "metrics": {},
                "error_summary": {},
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(Exception):
        load_experiment_result(
            input_path,
        )
