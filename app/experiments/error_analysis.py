from dataclasses import asdict, dataclass

from app.experiments.schemas import BenchmarkDataset


@dataclass(frozen=True)
class RetrievalError:
    """Structured analysis for a single retrieval benchmark case."""

    case_id: str
    failure_type: str
    relevant_documents: list[str]
    retrieved_documents: list[str]


def analyze_retrieval_errors(
    benchmark: BenchmarkDataset,
    retrieval_results: dict[str, list[str]],
) -> list[RetrievalError]:
    """Identify benchmark cases where retrieval missed relevant documents."""

    errors: list[RetrievalError] = []

    for case in benchmark.cases:
        relevant_documents = set(case.relevant_documents)

        retrieved_documents = retrieval_results.get(
            case.id,
            [],
        )

        retrieved_set = set(retrieved_documents)

        if not retrieved_documents:
            failure_type = "no_results"
        elif relevant_documents.isdisjoint(retrieved_set):
            failure_type = "retrieval_miss"
        elif not relevant_documents.issubset(retrieved_set):
            failure_type = "partial_retrieval"
        else:
            continue

        errors.append(
            RetrievalError(
                case_id=case.id,
                failure_type=failure_type,
                relevant_documents=case.relevant_documents,
                retrieved_documents=retrieved_documents,
            )
        )

    return errors


def summarize_retrieval_errors(
    errors: list[RetrievalError],
) -> dict[str, int]:
    """Return deterministic counts grouped by retrieval failure type."""

    summary: dict[str, int] = {
        "no_results": 0,
        "retrieval_miss": 0,
        "partial_retrieval": 0,
    }

    for error in errors:
        summary[error.failure_type] = (
            summary.get(
                error.failure_type,
                0,
            )
            + 1
        )

    return summary


def serialize_retrieval_errors(
    errors: list[RetrievalError],
) -> list[dict[str, object]]:
    """Convert structured retrieval errors into serializable records."""

    return [asdict(error) for error in errors]
