from collections.abc import Mapping


def compare_experiments(
    baseline: Mapping[str, object],
    candidate: Mapping[str, object],
) -> dict[str, float]:
    baseline_metrics = baseline.get("metrics", {})
    candidate_metrics = candidate.get("metrics", {})

    if not isinstance(baseline_metrics, Mapping):
        raise ValueError("Baseline metrics must be a mapping")

    if not isinstance(candidate_metrics, Mapping):
        raise ValueError("Candidate metrics must be a mapping")

    common_metrics = baseline_metrics.keys() & candidate_metrics.keys()

    return {
        metric: round(
            float(candidate_metrics[metric]) - float(baseline_metrics[metric]),
            10,
        )
        for metric in common_metrics
    }
