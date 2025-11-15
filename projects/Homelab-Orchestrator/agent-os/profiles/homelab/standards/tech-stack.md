## AI Lab Framework Coding Standards

### Technology Stack
- **Language**: Python (>=3.11)
- **Dependency Management**: Poetry
- **Database**: SQLAlchemy ORM with SQLite backend
- **Testing**: pytest with coverage reporting
- **Code Quality**: black (formatting), ruff (linting), mypy (type checking)
- **Documentation**: Markdown with structured formats
- **Project Structure**: Organized with src/, tests/, core/, data/ directories

### Code Style Guidelines
- **Formatting**: Use black with line-length 88, target-version py311+
- **Imports**: Organize with isort (stdlib → third-party → local)
- **Type Hints**: Use consistent type hints throughout codebase
- **Naming**: PascalCase for classes, snake_case for functions/variables
- **Error Handling**: Use specific exceptions, avoid bare except:
- **Logging**: Use structlog for structured logging

### Database Standards
- **ORM**: Always use SQLAlchemy models from src/infrastructure/db/models/
- **Queries**: Use SQLAlchemy ORM, not raw SQL
- **Migrations**: Update models first, then run migrations
- **Sessions**: Use SessionLocal() for database sessions
- **Legacy**: Never use src/ai_lab_framework/database.py (deprecated)

### Testing Standards
- **Framework**: pytest for all testing
- **Structure**: tests/unit/, tests/integration/, tests/e2e/
- **Coverage**: Aim for >80% test coverage
- **Fixtures**: Use pytest fixtures for test setup
- **Async**: Mark async tests with @pytest.mark.asyncio

### Security Standards
- **Credentials**: Never commit secrets or API keys
- **Validation**: Use Pydantic for data validation
- **SQL**: Use parameterized queries to prevent injection
- **Dependencies**: Regularly scan for security vulnerabilities
- **Access**: Implement proper authentication and authorization

### Documentation Standards
- **README**: Comprehensive project documentation
- **API**: Auto-generated API documentation
- **Code**: Docstrings for all public functions/classes
- **Changes**: Maintain CHANGELOG with version history
- **Architecture**: Document system design and decisions