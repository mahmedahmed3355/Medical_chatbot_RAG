# Medical RAG Chatbot

A medical Retrieval-Augmented Generation (RAG) chatbot built with Flask, LangChain, FAISS, Hugging Face, and Groq.

The application processes medical PDF documents, creates embeddings, stores them in a FAISS vector database, retrieves relevant context, and uses an LLM to generate concise answers.

## Features

- PDF document loading
- Text chunking with configurable chunk size and overlap
- Hugging Face embeddings
- FAISS vector store
- Retrieval-Augmented Generation
- Groq and Hugging Face LLM integration
- Flask API
- Health endpoint
- Docker support
- Gunicorn production server
- GitHub Actions CI
- Ruff linting
- Pytest test suite
- Jenkins pipeline configuration
- Environment-based configuration

## Architecture

Medical PDF Documents
        |
        v
    PDF Loader
        |
        v
   Text Splitter
        |
        v
    Embeddings
        |
        v
FAISS Vector Store
        |
        v
User Question -> Retriever -> Relevant Context
        |
        v
       LLM
        |
        v
   Final Answer

## Project Structure

.
├── app/
│   ├── common/
│   │   ├── custom_exception.py
│   │   └── logger.py
│   ├── components/
│   │   ├── data_loader.py
│   │   ├── embeddings.py
│   │   ├── llm.py
│   │   ├── pdf_loader.py
│   │   ├── retriever.py
│   │   └── vector_store.py
│   ├── config/
│   │   └── config.py
│   └── application.py
├── tests/
├── .github/
│   └── workflows/
│       └── ci.yml
├── Dockerfile
├── Jenkinsfile
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
├── ruff.toml
└── setup.py

## Requirements

- Python 3.12+
- pip
- Docker (optional)

## Installation

Clone the repository:

git clone https://github.com/mahmedahmed3355/Medical_chatbot_RAG.git
cd Medical_chatbot_RAG

Create a virtual environment:

python3.12 -m venv .venv
source .venv/bin/activate

Install dependencies:

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt

## Environment Variables

Create your local environment file:

cp .env.example .env

Configure the required values in .env.

Never commit secrets, API keys, tokens, or production credentials.

## Running the Application

python app/application.py

The application runs on port 5000.

Health endpoint:

curl http://localhost:5000/health

Expected response:

{"status":"ok"}

## Usage

### Quick Start

After installing the project dependencies, start the application from the repository root:

```bash
python -m app.application
```

The containerized deployment serves the application on port 5000.

Build the application image:

```bash
docker build -t medical-chatbot-rag:local .
```

Run the application container:

```bash
docker run --rm -p 5000:5000 --name medical-chatbot-rag medical-chatbot-rag:local
```

Verify that the application is running:

```bash
curl http://127.0.0.1:5000/health
```

For the complete operational workflow, including testing, quality checks, Docker operations, troubleshooting, and CI validation, see [RUNBOOK.md](RUNBOOK.md).

For details about the internal project structure and major components, see [ARCHITECTURE.md](ARCHITECTURE.md).

## Testing

Run the complete test suite:

python -m pytest -q

## Code Quality

Run Ruff:

python -m ruff check app tests

Compile the application:

python -m compileall -q app tests

Run all quality checks:

python -m ruff check app tests && \
python -m pytest -q && \
python -m compileall -q app tests

## Docker

Build the image:

docker build -t medical-rag-chatbot .

Run the container:

docker run -d \
  --name medical-rag-chatbot \
  -p 5000:5000 \
  --env-file .env \
  medical-rag-chatbot

Check the health endpoint:

curl http://localhost:5000/health

Check container health:

docker inspect \
  --format='Status={{.State.Status}} Health={{.State.Health.Status}}' \
  medical-rag-chatbot

The container runs using a non-root user and includes a Docker health check.

## Continuous Integration

GitHub Actions automatically runs on pushes and pull requests.

The CI pipeline performs:

- Dependency installation
- Ruff linting
- Pytest execution
- Python compilation checks

## Jenkins

The repository includes a Jenkins pipeline for container build, security scanning, image publishing, and deployment workflows.

## Security

Please review SECURITY.md for information about reporting security vulnerabilities.

## Contributing

Please review CONTRIBUTING.md before opening an issue or pull request.

## License

This project is currently provided without an explicit license.

## Maintenance and Quality

The project uses a lightweight quality gate for ongoing maintenance.

Before submitting changes, run:

python -m ruff check app tests
python -m mypy app
python -m pytest
python -m pip check

The project also includes deterministic experiment configuration and a fixed RAG evaluation benchmark for retrieval-quality validation.

## Docker Compose

Run the application with Docker Compose:

docker compose up --build

Run it in the background:

docker compose up --build -d

Check the application health endpoint:

curl -i http://localhost:5000/health

Stop the application:

docker compose down

The application is available at:

http://localhost:5000
