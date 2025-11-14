# AI Lab Framework - Agent Guidelines

## Build/Lint/Test Commands
```bash
# Code quality
black .                       # Format code (line-length: 88, target py311+)
ruff check .                  # Lint with ruff (isort, pyupgrade, bugbear)
ruff check --fix .            # Auto-fix lint issues
mypy .                        # Type checking (strict mode)
pre-commit run --all-files    # Run all pre-commit hooks

# Testing
pytest                        # Run all tests
pytest tests/unit/test_file.py  # Run single test file
pytest -k "test_function"     # Run specific test
pytest --cov=src              # Run with coverage
pytest -x                     # Stop on first failure
```

## Code Style Guidelines

### Imports & Formatting
- Use `isort` (via ruff) for import organization: stdlib → third-party → local
- Format with `black` (line-length: 88, target-version: py311+)
- Use type hints consistently (mypy strict mode enabled)
- Python version: >=3.11

### Naming Conventions
- Classes: `PascalCase`, Functions/variables: `snake_case`, Constants: `UPPER_SNAKE_CASE`
- Private: `_leading_underscore`, Files: `snake_case.py`

### Error Handling
- Use specific exception types, avoid bare `except:`
- Log errors with structlog, raise `HTTPException` for API errors
- Use Pydantic for data validation

### Project Structure
- `src/` for production code, `tests/` for test code (unit/, integration/)
- `data/schemas/` for JSON schemas, `data/work-items/` for JSON work items (SSOT)
- Follow agent-os/ standards for all implementations

### Testing
- Write unit tests for all core logic, use pytest fixtures
- Test files: `test_*.py` or `*_test.py` in tests/ directories
- Aim for >80% coverage, test both happy path and error cases
