import json
from pathlib import Path

from app.experiments.result_schemas import ExperimentResult


def serialize_experiment_result(
    result: ExperimentResult,
) -> dict[str, object]:
    """Convert an experiment result into a JSON-compatible record."""

    return result.model_dump(
        mode="json",
    )


def deserialize_experiment_result(
    record: dict[str, object],
) -> ExperimentResult:
    """Validate and reconstruct an experiment result from a record."""

    return ExperimentResult.model_validate(
        record,
    )


def save_experiment_result(
    result: ExperimentResult,
    path: str | Path,
) -> None:
    """Persist an experiment result as deterministic JSON."""

    output_path = Path(path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_text(
        json.dumps(
            serialize_experiment_result(
                result,
            ),
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def load_experiment_result(
    path: str | Path,
) -> ExperimentResult:
    """Load and validate an experiment result from JSON."""

    input_path = Path(path)

    record = json.loads(
        input_path.read_text(
            encoding="utf-8",
        )
    )

    if not isinstance(record, dict):
        raise ValueError("Experiment result JSON must contain an object")

    return deserialize_experiment_result(
        record,
    )
