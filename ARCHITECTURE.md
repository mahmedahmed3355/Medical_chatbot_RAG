
Architecture
Overview

Medical Chatbot RAG is a Python-based Retrieval-Augmented Generation application designed to provide a structured architecture for document ingestion, embedding generation, vector retrieval, language model interaction, observability, experimentation, and HTTP API delivery.

The project is organized around clear separation of responsibilities between the application entry point, reusable components, configuration, shared infrastructure, experiments, schemas, and observability.

High-Level Architecture

The primary application flow is:

Client
  |
  v
Flask Application
  |
  v
Application Layer
  |
  +--------------------------+
  |                          |
  v                          v
Retriever                Observability
  |                          |
  v                          v
Vector Store             Metrics / Logging
  |
  v
Embeddings
  |
  v
FAISS

For document ingestion:

Documents
  |
  v
PDF Loader / Data Loader
  |
  v
Embedding Model
  |
  v
Vector Store

For question processing:

User Request
  |
  v
Flask Endpoint
  |
  v
Retriever
  |
  v
FAISS Similarity Search
  |
  v
Retrieved Context
  |
  v
LLM Component
  |
  v
Generated Response
Application Layer

The application entry point is implemented in:

app/application.py

This layer is responsible for:

Creating and configuring the Flask application.
Registering HTTP routes.
Coordinating request processing.
Exposing the health endpoint.
Connecting application components.
Integrating observability and structured logging.

The application is served in the container using Gunicorn.

Components Layer

The app/components package contains the primary RAG building blocks.

Data Loader

The data loader is responsible for loading application data and preparing it for downstream processing.

PDF Loader

The PDF loader is responsible for loading PDF documents and converting them into documents suitable for the retrieval pipeline.

Embeddings

The embeddings component initializes the Hugging Face embedding model used to convert documents and queries into vector representations.

The configured model is:

sentence-transformers/all-MiniLM-L6-v2

Vector Store

The vector store component manages vector indexing and retrieval storage.

FAISS is used as the vector similarity backend.

Retriever

The retriever component is responsible for querying the vector store and returning relevant documents or context for a user request.

LLM

The LLM component encapsulates language model interaction and separates model initialization from the application layer.

Configuration Layer

The app/config package centralizes application configuration.

This separation keeps configuration concerns outside the business and retrieval components and supports consistent configuration access across the application.

Common Infrastructure

The app/common package contains shared infrastructure.

This includes:

Custom exceptions.
Application logging.
Structured logging.

These utilities provide consistent error handling and logging across the application.

Schemas

The app/schemas package defines structured application data models.

Schemas provide a clear boundary between external request data and internal application processing.

Observability

The app/observability package contains observability functionality.

Metrics are exposed through the Prometheus client integration.

Structured logging is used to record application events and request information.

The observability architecture supports:

Application
  |
  +------------------+
  |                  |
  v                  v
Structured Logs    Prometheus Metrics
Experiments

The app/experiments package contains utilities for evaluating and comparing RAG behavior.

The experiment modules include functionality related to:

Baseline evaluation.
Benchmarking.
Benchmark execution.
Result comparison.
Evaluation.
Reproducibility.

This separates experimental and evaluation concerns from the production application flow.

Testing Architecture

Tests are located in:

tests/

The project uses Pytest and pytest-cov.

The test configuration enforces a minimum coverage threshold.

The current test suite validates application behavior across the major project modules.

Container Architecture

The application container is built from:

python:3.12-slim

The runtime image:

Uses a runtime dependency lock file.
Avoids build-essential and compiler toolchains.
Uses CPU-only PyTorch.
Runs the application as a non-root user.
Exposes port 5000.
Includes a health check.
Runs Gunicorn with multiple workers and threads.

The runtime command is conceptually:

Gunicorn
  |
  v
app.application:app
  |
  v
Flask Application
CI Architecture

GitHub Actions workflows are located in:

.github/workflows/

The project includes automation for:

Continuous integration and quality checks.
Dependency security auditing.
Filesystem security scanning.
Kubernetes manifest validation.
Terraform validation and formatting.

The CI quality gate validates application quality, testing, dependency security, and infrastructure configuration.

Design Principles

The project architecture follows these principles:

Separation of concerns.
Modular RAG components.
Explicit application boundaries.
Shared infrastructure for logging and exceptions.
Independent experimentation and evaluation.
Runtime-focused container design.
Automated quality and security validation.
Repository Structure
Medical_chatbot_RAG/
├── app/
│   ├── application.py
│   ├── common/
│   ├── components/
│   ├── config/
│   ├── experiments/
│   ├── observability/
│   └── schemas/
├── tests/
├── .github/
│   └── workflows/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── requirements.lock
├── requirements-dev.txt
├── setup.py
└── ARCHITECTURE.md
Summary

The Medical Chatbot RAG architecture separates HTTP delivery, retrieval logic, embeddings, vector storage, language model interaction, observability, experimentation, configuration, and shared infrastructure into dedicated modules.

This structure supports maintainability, testability, containerized deployment, and automated validation through the project's CI workflows.

## Dependency Reproducibility

Python dependencies are defined in `pyproject.toml` and resolved into the committed `uv.lock` file.

`uv.lock` captures the resolved dependency graph used for reproducible installations. The existing requirements files remain available for the current pip-based workflow and compatibility with existing tooling.

Use the following command to install exactly the locked dependency set:

uv sync --frozen --all-groups
