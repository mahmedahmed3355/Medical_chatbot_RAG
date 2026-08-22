# Operations Runbook

## Overview

This runbook describes the standard workflow for setting up, running, testing, containerizing, and validating the Medical Chatbot RAG application.

For the architectural structure of the project, see ARCHITECTURE.md.

## Prerequisites

The project requires:

- Python 3.12 or newer
- pip
- Docker for containerized execution
- Docker Compose when using the compose configuration

## Local Setup

Create and activate a virtual environment:

    python -m venv .venv
    source .venv/bin/activate

Upgrade pip:

    python -m pip install --upgrade pip

Install runtime dependencies:

    python -m pip install -r requirements.lock

Install development dependencies when running tests and quality checks:

    python -m pip install -r requirements-dev.txt

## Running the Application

The application entry point is:

    app/application.py

Run the application locally:

    python -m app.application

The containerized deployment uses Gunicorn to serve:

    app.application:app

The application listens on port 5000 in the container.

## Health Check

The application exposes:

    /health

Example:

    curl http://127.0.0.1:5000/health

A successful response should indicate that the application is healthy.

## Running Tests

Run the complete test suite:

    python -m pytest

The project test configuration is defined in pytest.ini.

Run a specific test file:

    python -m pytest tests/test_file.py

## Code Quality

Development tooling is installed from:

    requirements-dev.txt

The project includes:

- Pytest
- Coverage reporting
- Ruff
- Mypy

Run Ruff:

    python -m ruff check .

Run Mypy:

    python -m mypy app

## Docker Build

Build the application image:

    docker build -t medical-chatbot-rag:local .

The runtime image is designed to:

- Use Python 3.12 slim
- Install dependencies from requirements.lock
- Avoid build toolchains in the runtime environment
- Use CPU-only PyTorch
- Run as a non-root user
- Expose port 5000
- Include a health check

## Docker Run

Start the application:

    docker run --rm -p 5000:5000 --name medical-chatbot-rag medical-chatbot-rag:local

Check health:

    curl http://127.0.0.1:5000/health

View logs:

    docker logs medical-chatbot-rag

## Docker Compose

If docker-compose.yml is configured:

    docker compose up --build

Stop services:

    docker compose down

## Dependency Management

Runtime dependencies are locked in:

    requirements.lock

Development and quality tooling dependencies are defined in:

    requirements-dev.txt

Runtime dependency changes should be validated with the complete test suite and a Docker build before being committed.

## CI Workflows

GitHub Actions workflows are located in:

    .github/workflows/

The repository includes automation for:

- Continuous integration and quality gates
- Dependency security auditing
- Filesystem security scanning
- Kubernetes manifest validation
- Terraform validation

## Standard Validation Workflow

For application changes:

    python -m pytest

For quality validation:

    python -m ruff check .
    python -m mypy app

For container validation:

    docker build -t medical-chatbot-rag:local .
    docker run --rm -d -p 5000:5000 --name medical-chatbot-rag medical-chatbot-rag:local
    curl http://127.0.0.1:5000/health
    docker stop medical-chatbot-rag

## Troubleshooting

### Application Import Failure

Verify the project root:

    pwd

Activate the virtual environment:

    source .venv/bin/activate

Run tests through Python:

    python -m pytest

### Dependency Installation Failure

Upgrade pip:

    python -m pip install --upgrade pip

Then reinstall the required dependency set.

### Docker Health Check Failure

Inspect containers:

    docker ps -a

View logs:

    docker logs medical-chatbot-rag

Verify health:

    curl http://127.0.0.1:5000/health

### CI Failure

List recent workflow runs:

    gh run list --limit 10

Inspect a specific run:

    gh run view RUN_ID

Download failed logs:

    gh run view RUN_ID --log-failed

## Operational Checklist

Before committing:

- Confirm the working tree contains only expected changes
- Run the relevant tests
- Run quality checks when source code changes
- Review the Git diff

Before pushing:

- Confirm the latest commit
- Verify the target branch
- Push to the intended remote branch
- Confirm GitHub Actions completes successfully

## Related Documentation

- ARCHITECTURE.md for project architecture
- README.md for repository-level information
- .github/workflows/ for CI and security automation
