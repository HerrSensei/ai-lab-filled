# AI Lab Framework - Agent Guidelines

## Build/Lint/Test Commands
```bash
# Framework setup
make setup                    # Complete environment setup
make install-tools            # Install dev tools (black, ruff, mypy, pytest, pre-commit)

# Code quality
black .                       # Format code (line-length: 88, target py311+)
ruff check .                  # Lint with ruff (isort, pyupgrade, bugbear)
ruff check --fix .            # Auto-fix lint issues
mypy .                        # Type checking (strict mode)
pre-commit run --all-files    # Run all pre-commit hooks

# Testing
make test                     # Run all framework tests (core + tools)
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
- Python version: >=3.11 (as defined in pyproject.toml)

### Naming Conventions
- Classes: `PascalCase`
- Functions/variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Private: `_leading_underscore`
- Files: `snake_case.py`

### Error Handling
- Use specific exception types, avoid bare `except:`
- Log errors with proper context using structlog
- Raise `HTTPException` for API errors with status codes
- Use Pydantic for data validation errors

### Project Structure
- `src/` for production code
- `tests/` for test code (unit/, integration/)
- `data/schemas/` for JSON schemas
- `data/work-items/` for JSON-based work items (SINGLE SOURCE OF TRUTH)
- `ideas/` for markdown documentation
- `core/` for framework tools and templates
- `projects/` for generated projects
- Follow agent-os/ standards for all implementations

### Project Management (JSON-based)
- **ALWAYS use JSON work items** in `data/work-items/` for project management
- **NEVER use markdown work items** - they are deprecated and only for archival
- **Single Source of Truth**: `data/work-items/*.json` files contain all work item data
- **Schema Compliance**: Follow `data/schemas/project_management_schema.json`
- **Status Tracking**: Use `project_management.json` for overall project status
- **Work Item Creation**: Create new work items as JSON files in `data/work-items/`
- **Dependencies**: Track dependencies using JSON `dependencies` arrays
- **Progress**: Update `actual_hours` and `status` fields in JSON files

### Operational Workflows
- Refer to `core/docs/CLI_WORKFLOWS.md` for detailed standard operating procedures and workflows for CLI-driven tasks, including session management, reporting, and development tasks.

### Documentation
- Use docstrings for all public functions/classes
- Markdown for documentation, JSON for data and project management
- Keep README.md files up-to-date
- Follow existing template patterns

### Testing
- Write unit tests for all core logic
- Use pytest fixtures for setup/teardown
- Aim for >80% coverage
- Test both happy path and error cases
- Test files: `test_*.py` or `*_test.py` in tests/ directories
- Use `make test` to run framework-wide tests
