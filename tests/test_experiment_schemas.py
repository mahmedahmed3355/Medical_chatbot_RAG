import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from app.experiments.benchmark import load_benchmark
from app.experiments.schemas import BenchmarkCase, BenchmarkDataset


def test_benchmark_dataset_accepts_valid_data():
    dataset = BenchmarkDataset(
        dataset_name="medical-retrieval",
        version="1.0",
        cases=[
            BenchmarkCase(
                id="case-1",
                relevant_documents=["document-1"],
            )
        ],
    )

    assert dataset.dataset_name == "medical-retrieval"
    assert dataset.version == "1.0"
    assert len(dataset.cases) == 1
    assert dataset.cases[0].id == "case-1"


@pytest.mark.parametrize(
    ("payload", "field_name"),
    [
        (
            {
                "version": "1.0",
                "cases": [
                    {
                        "id": "case-1",
                        "relevant_documents": ["document-1"],
                    }
                ],
            },
            "dataset_name",
        ),
        (
            {
                "dataset_name": "   ",
                "version": "1.0",
                "cases": [
                    {
                        "id": "case-1",
                        "relevant_documents": ["document-1"],
                    }
                ],
            },
            "dataset_name",
        ),
        (
            {
                "dataset_name": "medical-retrieval",
                "cases": [
                    {
                        "id": "case-1",
                        "relevant_documents": ["document-1"],
                    }
                ],
            },
            "version",
        ),
        (
            {
                "dataset_name": "medical-retrieval",
                "version": "   ",
                "cases": [
                    {
                        "id": "case-1",
                        "relevant_documents": ["document-1"],
                    }
                ],
            },
            "version",
        ),
    ],
)
def test_benchmark_dataset_rejects_invalid_required_text(
    payload: dict[str, object],
    field_name: str,
):
    with pytest.raises(ValidationError) as exc_info:
        BenchmarkDataset.model_validate(payload)

    assert field_name in str(exc_info.value)


def test_benchmark_dataset_rejects_empty_cases():
    with pytest.raises(ValidationError):
        BenchmarkDataset(
            dataset_name="medical-retrieval",
            version="1.0",
            cases=[],
        )


@pytest.mark.parametrize(
    "case_id",
    [
        "",
        "   ",
    ],
)
def test_benchmark_case_rejects_blank_case_id(
    case_id: str,
):
    with pytest.raises(ValidationError):
        BenchmarkCase(
            id=case_id,
            relevant_documents=["document-1"],
        )


def test_benchmark_case_rejects_empty_relevant_documents():
    with pytest.raises(ValidationError):
        BenchmarkCase(
            id="case-1",
            relevant_documents=[],
        )


@pytest.mark.parametrize(
    "document_id",
    [
        "",
        "   ",
    ],
)
def test_benchmark_case_rejects_blank_document_identifier(
    document_id: str,
):
    with pytest.raises(ValidationError):
        BenchmarkCase(
            id="case-1",
            relevant_documents=[document_id],
        )


def test_benchmark_dataset_rejects_duplicate_case_ids():
    with pytest.raises(ValidationError):
        BenchmarkDataset(
            dataset_name="medical-retrieval",
            version="1.0",
            cases=[
                BenchmarkCase(
                    id="case-1",
                    relevant_documents=["document-1"],
                ),
                BenchmarkCase(
                    id="case-1",
                    relevant_documents=["document-2"],
                ),
            ],
        )


def test_load_benchmark_returns_validated_dataset(
    tmp_path: Path,
):
    benchmark_path = tmp_path / "benchmark.json"

    benchmark_path.write_text(
        json.dumps(
            {
                "dataset_name": "medical-retrieval",
                "version": "1.0",
                "cases": [
                    {
                        "id": "case-1",
                        "relevant_documents": ["document-1"],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    dataset = load_benchmark(
        benchmark_path,
    )

    assert isinstance(
        dataset,
        BenchmarkDataset,
    )
    assert dataset.cases[0].id == "case-1"


def test_load_benchmark_rejects_invalid_dataset(
    tmp_path: Path,
):
    benchmark_path = tmp_path / "benchmark.json"

    benchmark_path.write_text(
        json.dumps(
            {
                "dataset_name": "",
                "version": "1.0",
                "cases": [],
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValidationError):
        load_benchmark(
            benchmark_path,
        )
