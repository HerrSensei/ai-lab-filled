# AI Lab Framework - Agent Guidelines

## 🚨 CRITICAL REMINDERS FOR EVERY PROMPT

### Database Architecture (ALWAYS VERIFY)
- ✅ **USE**: SQLAlchemy ORM (`src/infrastructure/db/models/`)
- ❌ **AVOID**: Direct SQLite (`src/ai_lab_framework/database.py` - DEPRECATED)
- ✅ **Database**: `data/ai_lab.db` (SQLite with SQLAlchemy ORM)
- ✅ **Models**: `src/infrastructure/db/models/models.py`

### Before Any Database Operation
1. Check if using SQLAlchemy models
2. Verify imports from `infrastructure.db`
3. Never import from `ai_lab_framework.database`

### Quick Test Before Coding
```python
# ✅ This is correct
from src.infrastructure.db.database import SessionLocal
from src.infrastructure.db.models.models import WorkItem

# ❌ This is WRONG - deprecated
from src.ai_lab_framework.database import AILabDatabase  # DO NOT USE!
```

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
pytest tests/ -v              # Verbose test output
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
- Always include context in error messages and logs

### Database Operations
- **ALWAYS** use SQLAlchemy ORM models from `src/infrastructure/db/models/`
- **NEVER** use direct SQLite or the legacy `src/ai_lab_framework/database.py`
- **Migrations**: Use SQLAlchemy sessions and models
- **Queries**: Use SQLAlchemy ORM, not raw SQL
- **Schema Changes**: Update SQLAlchemy models, then run migrations

### Project Structure
- `src/` for production code, `tests/` for test code (unit/, integration/)
- `data/schemas/` for JSON schemas, `data/work-items/` for JSON work items (SSOT)
- Follow agent-os/ standards for all implementations
- Use absolute imports: `from src.infrastructure.db.models import X`

### Database Architecture
- **Primary Database**: SQLAlchemy ORM with SQLite backend
- **Database Location**: `data/ai_lab.db` (SQLite file)
- **Models**: `src/infrastructure/db/models/models.py` (SQLAlchemy models)
- **Database Module**: `src/infrastructure/db/database.py` (SQLAlchemy configuration)
- **Migration Scripts**: Use SQLAlchemy models, NOT direct SQLite
- **Legacy Module**: `src/ai_lab_framework/database.py` (DEPRECATED - do not use)

**IMPORTANT**: Always use SQLAlchemy models for database operations. The legacy SQLite module should not be used for new development.

### Dependencies & Environment
- Python >=3.11 required
- Use `poetry install` or `pip install -e .` for dependencies
- Environment variables in `.env` (copy from `.env.template`)

### Testing
- Write unit tests for all core logic, use pytest fixtures
- Test files: `test_*.py` or `*_test.py` in tests/ directories
- Aim for >80% coverage, test both happy path and error cases
- Use `pytest tests/unit/test_file.py::test_function` for single test
- Mark tests with `@pytest.mark.asyncio` for async functions
