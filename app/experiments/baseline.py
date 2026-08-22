import json
from pathlib import Path

from app.experiments.config import load_experiment_config
from app.experiments.evaluation import hit_rate, precision_at_k
from app.experiments.reproducibility import set_global_seed

DEFAULT_CONFIG_PATH = (
    Path(__file__).resolve().parents[2] / "config" / "experiments" / "baseline.json"
)


def run_baseline(
    config_path: str | Path = DEFAULT_CONFIG_PATH,
) -> dict[str, object]:
    """Run a deterministic baseline evaluation."""
    config = load_experiment_config(config_path)

    set_global_seed(config.seed)

    predictions = [
        ["diabetes", "hypertension", "vaccination"],
        ["hypertension", "diabetes", "vaccination"],
        ["vaccination", "diabetes", "hypertension"],
    ]

    expected = [
        "diabetes",
        "hypertension",
        "vaccination",
    ]

    metrics = {
        "hit_rate": hit_rate(predictions, expected),
        "precision_at_k": precision_at_k(
            predictions,
            expected,
            config.retrieval.top_k,
        ),
    }

    return {
        "experiment_name": config.experiment_name,
        "seed": config.seed,
        "top_k": config.retrieval.top_k,
        "metrics": metrics,
    }


def save_baseline_result(
    output_path: str | Path,
    config_path: str | Path = DEFAULT_CONFIG_PATH,
) -> dict[str, object]:
    """Run the baseline experiment and save its result as JSON."""
    result = run_baseline(config_path)

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(
            result,
            file,
            indent=2,
            sort_keys=True,
        )

    return result


if __name__ == "__main__":
    result = run_baseline()
    print(
        json.dumps(
            result,
            indent=2,
            sort_keys=True,
        )
    )
