from app.experiments.error_analysis import (
    RetrievalError,
    analyze_retrieval_errors,
    serialize_retrieval_errors,
    summarize_retrieval_errors,
)
from app.experiments.schemas import (
    BenchmarkCase,
    BenchmarkDataset,
)


def make_benchmark() -> BenchmarkDataset:
    return BenchmarkDataset(
        dataset_name="test-benchmark",
        version="1.0",
        cases=[
            BenchmarkCase(
                id="hit-case",
                relevant_documents=[
                    "doc-1",
                ],
            ),
            BenchmarkCase(
                id="miss-case",
                relevant_documents=[
                    "doc-2",
                ],
            ),
            BenchmarkCase(
                id="partial-case",
                relevant_documents=[
                    "doc-3",
                    "doc-4",
                ],
            ),
        ],
    )


def test_analyze_retrieval_errors_returns_no_errors_for_hits():
    benchmark = BenchmarkDataset(
        dataset_name="perfect-benchmark",
        version="1.0",
        cases=[
            BenchmarkCase(
                id="case-1",
                relevant_documents=[
                    "doc-1",
                ],
            ),
        ],
    )

    errors = analyze_retrieval_errors(
        benchmark=benchmark,
        retrieval_results={
            "case-1": [
                "doc-1",
                "doc-2",
            ],
        },
    )

    assert errors == []


def test_analyze_retrieval_errors_detects_retrieval_miss():
    benchmark = make_benchmark()

    errors = analyze_retrieval_errors(
        benchmark=benchmark,
        retrieval_results={
            "hit-case": [
                "doc-1",
            ],
            "miss-case": [
                "wrong-doc",
            ],
            "partial-case": [
                "doc-3",
            ],
        },
    )

    assert len(errors) == 2

    retrieval_miss = next(error for error in errors if error.case_id == "miss-case")

    assert retrieval_miss.failure_type == "retrieval_miss"

    partial_retrieval = next(error for error in errors if error.case_id == "partial-case")

    assert partial_retrieval.failure_type == "partial_retrieval"
    assert partial_retrieval.relevant_documents == [
        "doc-3",
        "doc-4",
    ]
    assert partial_retrieval.retrieved_documents == [
        "doc-3",
    ]


def test_analyze_retrieval_errors_detects_missing_results():
    benchmark = BenchmarkDataset(
        dataset_name="missing-result-benchmark",
        version="1.0",
        cases=[
            BenchmarkCase(
                id="case-1",
                relevant_documents=[
                    "doc-1",
                ],
            ),
        ],
    )

    errors = analyze_retrieval_errors(
        benchmark=benchmark,
        retrieval_results={},
    )

    assert len(errors) == 1

    error = errors[0]

    assert error.case_id == "case-1"
    assert error.failure_type == "no_results"
    assert error.relevant_documents == [
        "doc-1",
    ]
    assert error.retrieved_documents == []


def test_analyze_retrieval_errors_detects_partial_retrieval():
    benchmark = make_benchmark()

    errors = analyze_retrieval_errors(
        benchmark=benchmark,
        retrieval_results={
            "hit-case": [
                "doc-1",
            ],
            "miss-case": [
                "doc-2",
            ],
            "partial-case": [
                "doc-3",
            ],
        },
    )

    assert len(errors) == 1

    error = errors[0]

    assert error.case_id == "partial-case"
    assert error.failure_type == "partial_retrieval"


def test_summarize_retrieval_errors_counts_error_types():
    errors = [
        RetrievalError(
            case_id="case-1",
            failure_type="retrieval_miss",
            relevant_documents=[
                "doc-1",
            ],
            retrieved_documents=[
                "wrong-doc",
            ],
        ),
        RetrievalError(
            case_id="case-2",
            failure_type="retrieval_miss",
            relevant_documents=[
                "doc-2",
            ],
            retrieved_documents=[],
        ),
        RetrievalError(
            case_id="case-3",
            failure_type="no_results",
            relevant_documents=[
                "doc-3",
            ],
            retrieved_documents=[],
        ),
    ]

    summary = summarize_retrieval_errors(
        errors,
    )

    assert sum(summary.values()) == 3
    assert summary == {
        "no_results": 1,
        "retrieval_miss": 2,
        "partial_retrieval": 0,
    }


def test_summarize_retrieval_errors_handles_empty_errors():
    summary = summarize_retrieval_errors(
        [],
    )

    assert sum(summary.values()) == 0
    assert summary == {
        "no_results": 0,
        "retrieval_miss": 0,
        "partial_retrieval": 0,
    }


def test_serialize_retrieval_errors_returns_serializable_records():
    errors = [
        RetrievalError(
            case_id="case-1",
            failure_type="retrieval_miss",
            relevant_documents=[
                "doc-1",
            ],
            retrieved_documents=[
                "wrong-doc",
            ],
        ),
    ]

    records = serialize_retrieval_errors(
        errors,
    )

    assert records == [
        {
            "case_id": "case-1",
            "failure_type": "retrieval_miss",
            "relevant_documents": [
                "doc-1",
            ],
            "retrieved_documents": [
                "wrong-doc",
            ],
        },
    ]


def test_serialize_retrieval_errors_handles_empty_errors():
    records = serialize_retrieval_errors(
        [],
    )

    assert records == []
