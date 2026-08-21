import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RetrievalConfig:
    top_k: int


@dataclass(frozen=True)
class EvaluationConfig:
    metrics: tuple[str, ...]


@dataclass(frozen=True)
class ExperimentConfig:
    experiment_name: str
    seed: int
    retrieval: RetrievalConfig
    evaluation: EvaluationConfig


def load_experiment_config(path: str | Path) -> ExperimentConfig:
    """Load an experiment configuration from JSON."""
    config_path = Path(path)

    with config_path.open(encoding="utf-8") as file:
        data = json.load(file)

    return ExperimentConfig(
        experiment_name=data["experiment_name"],
        seed=int(data["seed"]),
        retrieval=RetrievalConfig(
            top_k=int(data["retrieval"]["top_k"]),
        ),
        evaluation=EvaluationConfig(
            metrics=tuple(data["evaluation"]["metrics"]),
        ),
    )
