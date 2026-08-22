import json

from app.experiments import benchmark_runner


def test_run_benchmark_with_injected_retriever(
    monkeypatch,
    tmp_path,
):
    config_path = tmp_path / "experiment.yaml"
    benchmark_path = tmp_path / "benchmark.json"
    results_path = tmp_path / "results" / "benchmark_results.json"

    config_path.write_text(
        "placeholder",
        encoding="utf-8",
    )

    benchmark_path.write_text(
        json.dumps(
            {
                "dataset_name": "live-test-benchmark",
                "version": "1.0",
                "cases": [
                    {
                        "id": "case-1",
                        "query": "diabetes symptoms",
                        "relevant_documents": [
                            "doc-diabetes",
                        ],
                    },
                    {
                        "id": "case-2",
                        "query": "hypertension management",
                        "relevant_documents": [
                            "doc-hypertension",
                        ],
                    },
                ],
            }
        ),
        encoding="utf-8",
    )

    class FakeConfig:
        seed = 42
        top_k = 2
        experiment_name = "live-retriever-test"

    monkeypatch.setattr(
        benchmark_runner,
        "DEFAULT_CONFIG_PATH",
        config_path,
    )

    monkeypatch.setattr(
        benchmark_runner,
        "DEFAULT_BENCHMARK_PATH",
        benchmark_path,
    )

    monkeypatch.setattr(
        benchmark_runner,
        "DEFAULT_RESULTS_PATH",
        results_path,
    )

    monkeypatch.setattr(
        benchmark_runner,
        "load_experiment_config",
        lambda path: FakeConfig(),
    )

    seed_calls = []

    monkeypatch.setattr(
        benchmark_runner,
        "set_global_seed",
        lambda seed: seed_calls.append(seed),
    )

    retriever_calls = []

    def fake_retriever(case, top_k):
        retriever_calls.append(
            (
                case["id"],
                top_k,
            )
        )

        results = {
            "case-1": [
                "doc-diabetes",
                "doc-other",
            ],
            "case-2": [
                "doc-other",
                "doc-hypertension",
            ],
        }

        return results[case["id"]]

    result = benchmark_runner.run_benchmark_with_retriever(
        fake_retriever,
    )

    assert seed_calls == [42]

    assert retriever_calls == [
        ("case-1", 2),
        ("case-2", 2),
    ]

    assert result["experiment_name"] == "live-retriever-test"
    assert result["benchmark"] == "live-test-benchmark"
    assert result["benchmark_version"] == "1.0"
    assert result["seed"] == 42
    assert result["top_k"] == 2

    assert result["metrics"]["hit_rate_at_k"] == 1.0
    assert result["metrics"]["recall_at_k"] == 1.0
    assert result["metrics"]["mrr"] == 0.75

    saved = json.loads(
        results_path.read_text(
            encoding="utf-8",
        )
    )

    assert saved == result
