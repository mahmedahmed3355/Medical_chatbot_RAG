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

    @property
    def top_k(self) -> int:
        return self.retrieval.top_k


def load_experiment_config(
    config_path: str | Path,
) -> ExperimentConfig:
    path = Path(config_path)

    with path.open(encoding="utf-8") as file:
        data = json.load(file)

    retrieval_data = data.get("retrieval", {})
    top_k = int(
        retrieval_data.get(
            "top_k",
            data.get("top_k", 3),
        )
    )

    evaluation_data = data.get("evaluation", {})
    metrics = tuple(
        str(metric)
        for metric in evaluation_data.get(
            "metrics",
            (
                "hit_rate",
                "precision_at_k",
            ),
        )
    )

    return ExperimentConfig(
        experiment_name=str(data["experiment_name"]),
        seed=int(data["seed"]),
        retrieval=RetrievalConfig(
            top_k=top_k,
        ),
        evaluation=EvaluationConfig(
            metrics=metrics,
        ),
    )
