import json
from pathlib import Path

from app.experiments.benchmark import (
    evaluate_retrieval,
    load_benchmark,
)
from app.experiments.config import (
    load_experiment_config,
)
from app.experiments.reproducibility import (
    set_global_seed,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DEFAULT_CONFIG_PATH = (
    PROJECT_ROOT
    / "config"
    / "experiment.yaml"
)

DEFAULT_BENCHMARK_PATH = (
    PROJECT_ROOT
    / "data"
    / "evaluation"
    / "rag_benchmark.json"
)

DEFAULT_RESULTS_PATH = (
    PROJECT_ROOT
    / "experiments"
    / "results"
    / "rag_benchmark_baseline.json"
)


def build_baseline_retrieval_results() -> dict[str, list[str]]:
    return {
        "case-001": [
            "doc-diabetes-symptoms",
            "doc-hypertension-management",
            "doc-asthma-symptoms",
        ],
        "case-002": [
            "doc-heart-health",
            "doc-hypertension-management",
            "doc-dehydration",
        ],
        "case-003": [
            "doc-asthma-symptoms",
            "doc-heart-health",
            "doc-diabetes-symptoms",
        ],
        "case-004": [
            "doc-hypertension-management",
            "doc-heart-health",
            "doc-asthma-symptoms",
        ],
        "case-005": [
            "doc-dehydration",
            "doc-diabetes-symptoms",
            "doc-heart-health",
        ],
    }


def run_benchmark() -> dict[str, object]:
    config = load_experiment_config(
        DEFAULT_CONFIG_PATH
    )

    seed = config.seed
    top_k = config.top_k
    experiment_name = config.experiment_name

    set_global_seed(seed)

    benchmark = load_benchmark(
        DEFAULT_BENCHMARK_PATH
    )

    metrics = evaluate_retrieval(
        benchmark,
        build_baseline_retrieval_results(),
        top_k,
    )

    results: dict[str, object] = {
        "experiment_name": experiment_name,
        "benchmark": benchmark["dataset_name"],
        "benchmark_version": benchmark["version"],
        "seed": seed,
        "top_k": top_k,
        "metrics": metrics,
    }

    DEFAULT_RESULTS_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with DEFAULT_RESULTS_PATH.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            results,
            file,
            indent=2,
            sort_keys=True,
        )

    return results


if __name__ == "__main__":
    result = run_benchmark()

    print(
        json.dumps(
            result,
            indent=2,
            sort_keys=True,
        )
    )
