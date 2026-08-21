import json

from app.experiments import benchmark_runner


def test_load_benchmark(tmp_path):
    benchmark_path = tmp_path / "benchmark.json"

    benchmark_path.write_text(
        json.dumps(
            {
                "dataset_name": "test",
                "version": "1.0",
                "cases": [],
            }
        ),
        encoding="utf-8",
    )

    benchmark = benchmark_runner.load_benchmark(benchmark_path)

    assert benchmark["dataset_name"] == "test"


def test_evaluate_retrieval():
    benchmark = {
        "cases": [
            {
                "id": "case-1",
                "relevant_documents": ["doc-1"],
            },
            {
                "id": "case-2",
                "relevant_documents": ["doc-2"],
            },
        ]
    }

    retrieval_results = {
        "case-1": [
            "doc-1",
            "doc-3",
        ],
        "case-2": [
            "doc-3",
            "doc-2",
        ],
    }

    metrics = benchmark_runner.evaluate_retrieval(
        benchmark,
        retrieval_results,
        2,
    )

    assert metrics["hit_rate_at_k"] == 1.0
    assert metrics["recall_at_k"] == 1.0
    assert metrics["mrr"] == 0.75


def test_build_baseline_retrieval_results():
    results = benchmark_runner.build_baseline_retrieval_results()

    assert isinstance(results, dict)
    assert len(results) == 5

    assert results["case-001"] == [
        "doc-diabetes-symptoms",
        "doc-hypertension-management",
        "doc-asthma-symptoms",
    ]

    assert results["case-005"] == [
        "doc-dehydration",
        "doc-diabetes-symptoms",
        "doc-heart-health",
    ]


def test_run_benchmark_writes_results(
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
                "dataset_name": "test-benchmark",
                "version": "1.0",
                "cases": [],
            }
        ),
        encoding="utf-8",
    )

    class FakeConfig:
        seed = 42
        top_k = 3
        experiment_name = "test-experiment"

    seed_calls = []

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

    monkeypatch.setattr(
        benchmark_runner,
        "set_global_seed",
        lambda seed: seed_calls.append(seed),
    )

    monkeypatch.setattr(
        benchmark_runner,
        "load_benchmark",
        lambda path: {
            "dataset_name": "test-benchmark",
            "version": "1.0",
            "cases": [],
        },
    )

    expected_retrieval_results = {"case-test": ["doc-test"]}

    monkeypatch.setattr(
        benchmark_runner,
        "build_baseline_retrieval_results",
        lambda: expected_retrieval_results,
    )

    expected_metrics = {
        "hit_rate_at_k": 1.0,
        "recall_at_k": 1.0,
        "mrr": 1.0,
    }

    evaluation_calls = []

    def fake_evaluate(
        benchmark,
        retrieval_results,
        top_k,
    ):
        evaluation_calls.append(
            (
                benchmark,
                retrieval_results,
                top_k,
            )
        )

        return expected_metrics

    monkeypatch.setattr(
        benchmark_runner,
        "evaluate_retrieval",
        fake_evaluate,
    )

    result = benchmark_runner.run_benchmark()

    assert seed_calls == [42]

    assert evaluation_calls == [
        (
            {
                "dataset_name": "test-benchmark",
                "version": "1.0",
                "cases": [],
            },
            expected_retrieval_results,
            3,
        )
    ]

    assert result == {
        "experiment_name": "test-experiment",
        "benchmark": "test-benchmark",
        "benchmark_version": "1.0",
        "seed": 42,
        "top_k": 3,
        "metrics": expected_metrics,
    }

    assert results_path.exists()

    saved_results = json.loads(results_path.read_text(encoding="utf-8"))

    assert saved_results == result


def test_benchmark_runner_module_main_entrypoint(capsys):
    import runpy
    import sys

    module_name = "app.experiments.benchmark_runner"
    sys.modules.pop(module_name, None)

    try:
        runpy.run_module(
            module_name,
            run_name="__main__",
        )
    finally:
        sys.modules.pop(module_name, None)

    output = capsys.readouterr().out

    assert '"benchmark": "medical-rag-evaluation"' in output
    assert '"benchmark_version": "1.0"' in output
    assert '"metrics"' in output
    assert '"mrr": 0.8' in output
