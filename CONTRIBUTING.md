# Contributing

## Development Setup

Create and activate a virtual environment, then install the project and development dependencies.

Run:

python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt

## Quality Checks

Before submitting changes, run:

python -m ruff check app tests
python -m mypy app
python -m pytest
python -m pip check

All checks must pass before merging changes.

## Contribution Guidelines

- Keep commits small and focused.
- Add or update tests for behavioral changes.
- Preserve deterministic behavior in experiment and benchmark code.
- Avoid unrelated refactoring in feature or bug-fix commits.
- Run the full quality suite before opening a pull request.

## Experiment Changes

Changes affecting experiments or retrieval evaluation should preserve:

- reproducible configuration
- deterministic seeds where applicable
- benchmark compatibility
- documented evaluation metrics
