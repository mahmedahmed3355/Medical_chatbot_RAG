import json

from app.experiments.baseline import (
    run_baseline,
    save_baseline_result,
)


def test_baseline_is_reproducible():
    first_result = run_baseline()
    second_result = run_baseline()

    assert first_result == second_result

    assert first_result["experiment_name"] == "medical-rag-baseline"
    assert first_result["seed"] == 42
    assert first_result["top_k"] == 3


def test_baseline_metrics_are_present():
    result = run_baseline()

    assert "hit_rate" in result["metrics"]
    assert "precision_at_k" in result["metrics"]

    assert result["metrics"]["hit_rate"] == 1.0
    assert result["metrics"]["precision_at_k"] > 0.0


def test_baseline_result_can_be_saved(tmp_path):
    output_path = tmp_path / "baseline-result.json"

    result = save_baseline_result(output_path)

    assert output_path.exists()

    saved_result = json.loads(
        output_path.read_text(
            encoding="utf-8"
        )
    )

    assert saved_result == result
