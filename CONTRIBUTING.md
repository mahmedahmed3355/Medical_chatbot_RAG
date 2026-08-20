# Contributing

Thank you for your interest in contributing to Medical RAG Chatbot.

## Development Setup

Clone the repository:

git clone https://github.com/mahmedahmed3355/Medical_chatbot_RAG.git
cd Medical_chatbot_RAG

Create and activate a virtual environment:

python3.12 -m venv .venv
source .venv/bin/activate

Install dependencies:

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt

## Branching

Create a new branch for your work:

git checkout -b feature/your-feature-name

Use clear branch names such as:

feature/add-api-endpoint
fix/vector-store-error
docs/update-readme
test/improve-coverage

## Code Quality

Before submitting changes, run:

python -m ruff check app tests
python -m pytest -q
python -m compileall -q app tests

All checks should pass before opening a pull request.

## Testing

Add or update tests when changing application behavior.

Run the full test suite:

python -m pytest -q

## Pull Requests

Before opening a pull request:

- Keep changes focused.
- Add tests for new behavior when appropriate.
- Do not commit .env files or secrets.
- Run linting and tests locally.
- Ensure the GitHub Actions CI workflow passes.
- Write a clear pull request description.

## Commit Messages

Use clear and descriptive commit messages.

Examples:

Add health endpoint tests
Fix vector store loading error
Improve Docker container security
Update CI workflow

## Reporting Bugs

When reporting a bug, include:

- A clear description of the problem.
- Steps to reproduce it.
- Expected behavior.
- Actual behavior.
- Python version.
- Operating system.
- Relevant logs or error messages.

## Security Issues

Do not report security vulnerabilities through public GitHub issues.

Please review SECURITY.md for the responsible disclosure process.
