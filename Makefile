.PHONY: help install install-runtime install-dev build test lint format-check type-check quality security docker-build docker-run clean

PYTHON ?= python
IMAGE_NAME ?= medical-chatbot-rag
IMAGE_TAG ?= local
CONTAINER_NAME ?= medical-chatbot-rag
PORT ?= 5000

help:
	@echo "Available targets:"
	@echo "  install       Install dependencies required for build and test"
	@echo "  install-runtime Install locked runtime dependencies only"
	@echo "  install-dev   Alias for install"
	@echo "  build         Validate application sources for a clean build"
	@echo "  test          Run the complete test suite"
	@echo "  lint          Run Ruff checks"
	@echo "  format-check  Check code formatting with Ruff"
	@echo "  type-check    Run Mypy against the application"
	@echo "  quality       Run lint, format, type, and test checks"
	@echo "  security      Run pip-audit against requirements.lock"
	@echo "  docker-build  Build the Docker image"
	@echo "  docker-run    Run the Docker container"
	@echo "  clean         Remove local generated caches"

install:
	$(PYTHON) -m pip install -r requirements.lock
	$(PYTHON) -m pip install -r requirements-dev.txt

install-runtime:
	$(PYTHON) -m pip install -r requirements.lock

install-dev: install

build:
	$(PYTHON) -m compileall -q app

test:
	$(PYTHON) -m pytest -m "not live"

lint:
	$(PYTHON) -m ruff check .

format-check:
	$(PYTHON) -m ruff format --check .

type-check:
	$(PYTHON) -m mypy app

quality: lint format-check type-check test

security:
	$(PYTHON) -m pip_audit -r requirements.lock

docker-build:
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .

docker-run:
	docker run --rm -p $(PORT):5000 --name $(CONTAINER_NAME) $(IMAGE_NAME):$(IMAGE_TAG)

clean:
	rm -rf .pytest_cache .ruff_cache .mypy_cache htmlcov .coverage
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
