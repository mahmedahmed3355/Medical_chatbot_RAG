from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = PROJECT_ROOT / ".github" / "workflows" / "ci.yml"


def read_workflow():
    return WORKFLOW_PATH.read_text(
        encoding="utf-8",
    )


def test_ci_workflow_exists():
    assert WORKFLOW_PATH.is_file()


def test_ci_runs_on_push_to_main():
    workflow = read_workflow()

    assert "push:" in workflow
    assert "branches:" in workflow
    assert "- main" in workflow


def test_ci_runs_on_pull_requests_to_main():
    workflow = read_workflow()

    assert "pull_request:" in workflow


def test_ci_checks_out_repository():
    workflow = read_workflow()

    assert "actions/checkout@v4" in workflow


def test_ci_uses_python_312():
    workflow = read_workflow()

    assert "actions/setup-python@v5" in workflow
    assert 'python-version: "3.12"' in workflow


def test_ci_installs_project_dependencies():
    workflow = read_workflow()

    assert "requirements.lock" in workflow
    assert "requirements-dev.txt" in workflow


def test_ci_runs_dependency_integrity_check():
    workflow = read_workflow()

    assert "python -m pip check" in workflow


def test_ci_runs_ruff():
    workflow = read_workflow()

    assert "make lint" in workflow


def test_ci_runs_mypy():
    workflow = read_workflow()

    assert "make type-check" in workflow


def test_ci_runs_pytest():
    workflow = read_workflow()

    assert "make test" in workflow


def test_ci_builds_application():
    workflow = read_workflow()

    assert "make build" in workflow


def test_ci_has_security_job():
    workflow = read_workflow()

    assert "security:" in workflow
    assert "python -m pip_audit" in workflow


def test_ci_validates_terraform():
    workflow = read_workflow()

    assert "terraform -chdir=terraform validate" in workflow


def test_ci_runs_checkov():
    workflow = read_workflow()

    assert "checkov==3.3.13" in workflow
    assert 'Checkov().run(["-d", "terraform", "--quiet"])' in workflow
