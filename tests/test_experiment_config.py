import json

from app.experiments.config import load_experiment_config


def test_load_experiment_config(tmp_path):
    config_path = tmp_path / "experiment.json"

    config_path.write_text(
        json.dumps(
            {
                "experiment_name": "test-experiment",
                "seed": 123,
                "retrieval": {
                    "top_k": 5,
                },
                "evaluation": {
                    "metrics": [
                        "hit_rate",
                        "precision_at_k",
                    ],
                },
            }
        ),
        encoding="utf-8",
    )

    config = load_experiment_config(config_path)

    assert config.experiment_name == "test-experiment"
    assert config.seed == 123
    assert config.retrieval.top_k == 5
    assert config.evaluation.metrics == (
        "hit_rate",
        "precision_at_k",
    )
