from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def read_project_file(relative_path):
    return (
        PROJECT_ROOT / relative_path
    ).read_text(
        encoding="utf-8",
    )


def test_dockerfile_uses_non_root_user():
    dockerfile = read_project_file("Dockerfile")

    assert "useradd" in dockerfile
    assert "USER appuser" in dockerfile


def test_dockerfile_uses_gunicorn():
    dockerfile = read_project_file("Dockerfile")

    assert "gunicorn" in dockerfile
    assert "CMD" in dockerfile


def test_application_disables_flask_debug_mode():
    application = read_project_file(
        "app/application.py"
    )

    assert "debug=False" in application


def test_application_binds_to_all_interfaces():
    application = read_project_file(
        "app/application.py"
    )

    assert 'host="0.0.0.0"' in application
    assert "port=5000" in application


def test_compose_exposes_expected_port():
    compose = read_project_file(
        "docker-compose.yml"
    )

    assert "5000:5000" in compose


def test_compose_defines_healthcheck():
    compose = read_project_file(
        "docker-compose.yml"
    )

    assert "healthcheck:" in compose
    assert "/health" in compose


def test_compose_uses_restart_policy():
    compose = read_project_file(
        "docker-compose.yml"
    )

    assert "restart: unless-stopped" in compose
