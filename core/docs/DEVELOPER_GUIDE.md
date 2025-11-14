# AI Lab Framework - Developer Guide

## 🎯 Purpose

This guide provides comprehensive documentation for human developers working with the AI Lab Framework. It assumes you're familiar with software development concepts and focuses on practical implementation details.

## 📚 Documentation Structure

### Core Documentation
- **[FRAMEWORK_STRUCTURE.md](./core/docs/FRAMEWORK_STRUCTURE.md)** - Single Source of Truth for framework structure (AI-readable)
- **[PROJECT_CONTEXT.md](./core/docs/PROJECT_CONTEXT.md)** - Complete framework context and overview
- **[GUIDELINES.md](./core/guidelines/GUIDELINES.md)** - Detailed coding standards and practices

### Strategic Documentation
- **[VISION.md](./core/guidelines/VISION.md)** - Long-term vision and goals
- **[DECISIONS.md](./core/guidelines/DECISIONS.md)** - Architecture decisions and rationale
- **[ki-tool-guidelines.md](./core/guidelines/ki-tool-guidelines.md)** - AI tool-specific standards

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Git
- Make

### Initial Setup
```bash
# Clone and setup
git clone <repository-url>
cd ai-lab
make setup

# Verify installation
make test
```

### Creating Your First Project
```bash
# Interactive project creation
./core/tools/project-creator/bin/project-creator

# Quick project creation
./core/tools/project-creator/bin/project-creator --standard my-project

# AI/ML project
./core/tools/project-creator/bin/project-creator --type ai_ml my-ml-project
```

### AI Assistant Integration
```bash
# Check if AI tools are installed
make check-ai-tools

# Open project with AI assistant (interactive)
make ai-assistant

# Open with specific assistant
make open-with-opencode projects/my-project
make open-with-gemini projects/my-project
```

## 🏗️ Framework Architecture

### Core Principles
1. **Single Source of Truth**: All framework-relevant code lives in `core/`
2. **Consistency**: Standardized structures across all projects
3. **Modularity**: Clear separation of concerns
4. **Developer Experience**: Focus on practical usability

### Directory Structure
```
ai-lab/
├── core/                    # Framework core (all framework-relevant code)
│   ├── docs/               # Documentation
│   ├── guidelines/         # Standards and guidelines
│   ├── templates/          # Project templates (single source)
│   ├── tools/              # Framework tools
│   │   ├── project-creator/ # Project creation
│   │   ├── framework-setup/ # Framework setup
│   │   └── ai-assistant/    # AI assistant integration
│   └── scripts/            # Setup and utility scripts
├── projects/               # Your projects
├── data/work-items/        # JSON-based work items (SINGLE SOURCE OF TRUTH)
├── project-management/     # Legacy markdown work items (DEPRECATED)
└── ai-logs/               # AI interaction logs
```

## 🐳 Docker-based Development

To handle the mixed Python and Node.js environments, the framework now uses Docker Compose for a unified development setup.

### Services
- **`framework`**: A container with the Python environment and all dependencies from `pyproject.toml` installed. The entire project directory is mounted, so you can execute any script or tool from within this container.
- **`mcp-server`**: A container for the Node.js-based Model Context Protocol (MCP) server, running in development mode with file watching.

### Usage
The development environment is managed via `make` commands.

- `make dev` or `make dev-up`: Starts the Docker Compose environment in detached mode.
- `make dev-down`: Stops and removes the containers.
- `docker-compose exec framework bash`: Opens a shell inside the `framework` container to run Python tools and scripts.

## 🛠️ Development Workflow

### 1. Start the Development Environment
```bash
# This will build and start the 'framework' and 'mcp-server' containers.
make dev
```

### 2. Work with the Framework
To run Python scripts, tools, or tests, open a shell inside the `framework` container:
```bash
docker-compose exec framework bash

# Now you are inside the container, you can run framework commands
./core/tools/project-creator/bin/project-creator --help
make test
```

### 3. Stop the Development Environment
```bash
make dev-down
```

### 4. AI-Assisted Development
```bash
# Check AI tools installation
make check-ai-tools

# Open project with AI assistant
make ai-assistant

# Work with specific AI assistant
make open-with-opencode projects/your-project
make open-with-gemini projects/your-project
```

### 5. Daily Development
```bash
# Code quality checks (run inside the 'framework' container)
make lint          # Black, Ruff, MyPy
make test          # Run all tests
make coverage      # Test coverage report
```

### 4. Project Structure
Every project follows this structure:
```
your-project/
├── src/                    # Source code
│   ├── api/               # API endpoints
│   ├── core/              # Core functionality
│   ├── models/            # Data models
│   └── services/          # Business logic
├── tests/                  # Tests
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   └── conftest.py        # Pytest configuration
├── docs/                   # Project documentation
├── config/                 # Configuration files
├── docker-compose.yml      # Development containers
├── pyproject.toml         # Dependencies and config
└── README.md              # Project overview
```

## 📝 Coding Standards

### Python Standards
```python
# Type hints are mandatory
from typing import List, Dict, Optional

def process_data(
    items: List[Dict[str, str]],
    limit: Optional[int] = None
) -> Optional[str]:
    """Process a list of items with optional limit."""
    if limit and len(items) > limit:
        items = items[:limit]
    return items[0].get("name") if items else None

# Class naming
class DataProcessor:
    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config

    def process(self, data: Any) -> Any:
        """Process the input data."""
        pass
```

### File Naming
- **Python files**: `snake_case.py`
- **Directories**: `kebab-case`
- **Documentation**: `kebab-case.md`
- **Configuration**: `kebab-case.yaml` or `kebab-case.json`

### Git Workflow
```bash
# Feature branch
git checkout -b feature/your-feature-name

# Conventional commits
git commit -m "feat: add user authentication"
git commit -m "fix: resolve memory leak in data processing"
git commit -m "docs: update API documentation"

# Push and create PR
git push origin feature/your-feature-name
```

## 🧪 Testing Strategy

### Test Structure
```python
# tests/unit/test_data_processor.py
import pytest
from src.core.data_processor import DataProcessor

class TestDataProcessor:
    def test_process_data_success(self):
        """Test successful data processing."""
        processor = DataProcessor({"limit": 10})
        result = processor.process([{"name": "test"}])
        assert result == "test"

    def test_process_data_empty_list(self):
        """Test processing empty list."""
        processor = DataProcessor({})
        result = processor.process([])
        assert result is None
```

### Coverage Requirements
- **Minimum**: 80% line coverage
- **Target**: 90% for critical components
- **AI/ML projects**: 70% minimum (experimental code)

## 🐳 Docker & Deployment

### Development Docker
```dockerfile
# Multi-stage build
FROM python:3.11-slim as builder
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install --only=main

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY src/ ./src/
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Configuration
```bash
# .env.example (required in every project)
OPENAI_API_KEY=your_openai_key_here
DATABASE_URL=postgresql://user:pass@localhost/db
REDIS_URL=redis://localhost:6379
LOG_LEVEL=INFO
ENVIRONMENT=development
```

## 🤖 AI Assistant Integration

### Supported AI Assistants
The AI Lab Framework integrates with popular AI coding assistants:

#### 1. opencode (OpenAI-based)
- **Installation**: https://github.com/sst/opencode
- **Features**: OpenAI GPT integration, context-aware assistance
- **Usage**: `make open-with-opencode projects/your-project`

#### 2. gemini-cli (Google Gemini)
- **Installation**: `npm install -g @google/generative-ai-cli`
- **Features**: Google Gemini integration, multimodal capabilities
- **Usage**: `make open-with-gemini projects/your-project`

### AI Assistant Features
- **Automatic Context Creation**: Generates `.opencode-context.md` or `.gemini-context.md`
- **Project Validation**: Checks for AI Lab project structure
- **Framework Integration**: Provides AI Lab context and guidelines
- **Interactive Mode**: Choose assistant and project interactively

### Usage Examples
```bash
# Check if AI tools are installed
make check-ai-tools

# Interactive mode - choose assistant and project
make ai-assistant

# Direct project opening
make open-with-opencode projects/my-project
make open-with-gemini projects/my-project

# Open current directory
make open-with-opencode
```

### AI Context Files
The framework automatically creates context files containing:
- Project information and structure
- AI Lab Framework guidelines
- Current project status
- Development instructions

### Best Practices for AI-Assisted Development
1. **Always use AI assistant integration** - Provides proper context
2. **Review AI suggestions** - Ensure they follow AI Lab standards
3. **Update documentation** - Keep PROJECT_OVERVIEW.md current
4. **Create JSON work items** - Track AI-assisted changes in `data/work-items/`
5. **Use JSON-based project management** - Never use markdown work items (deprecated)

## 🔧 Tools and Utilities

### Interactive CLI Wrapper
For an easier way to browse and execute `make` targets, an interactive CLI wrapper is available.

```bash
# Run the interactive CLI
interactive-cli
```

This will present a menu of all available `make` targets, grouped by category. You can then select a target to execute.

### Makefile Dependency Visualization
To visualize the dependencies between the modular Makefiles, you can generate a Graphviz DOT file.

```bash
# Generate the DOT file
make visualize-deps

# To create a PNG image from the DOT file (requires Graphviz to be installed)
dot -Tpng make_dependencies.dot -o make_dependencies.png
```

### Project Creator Tool
```bash
# Interactive mode
./core/tools/project-creator/bin/project-creator

# Available project types
--standard          # Standard Python project
--ai_ml            # AI/ML project with prompt management
--api              # API-focused project
--infrastructure   # Infrastructure as Code project
```

### Framework Setup Tool
```bash
# Initial framework setup
cd core/tools/framework-setup
make setup

# Install diagram tools
make diagrams-install

# Update framework
make update
```

## 📊 Monitoring and Logging

### Structured Logging
```python
import structlog

logger = structlog.get_logger()

logger.info(
    "api_request_completed",
    user_id=user_id,
    endpoint="/api/chat",
    duration_ms=duration,
    status_code=200
)
```

### Required Metrics
Every project must track:
- Request count and response times
- Error rates and types
- Resource usage (memory, CPU)
- Business metrics (user actions, conversions)

## 🔒 Security Standards

### API Key Management
```python
# ✅ Correct - use environment variables
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is required")

# ❌ Wrong - never hardcode keys
api_key = "sk-1234567890abcdef"
```

### Input Validation
```python
from pydantic import BaseModel, validator

class UserRequest(BaseModel):
    email: str
    message: str

    @validator('email')
    def validate_email(cls, v):
        if not '@' in v:
            raise ValueError('Invalid email format')
        return v

    @validator('message')
    def validate_message(cls, v):
        if len(v) > 1000:
            raise ValueError('Message too long')
        return v
```

## 🚀 Deployment

### CI/CD Pipeline
1. **Linting**: Black, Ruff, MyPy checks
2. **Testing**: All tests with coverage
3. **Security**: Dependency and code scans
4. **Build**: Docker image creation
5. **Deploy**: Staging and production deployment

### Release Process
```bash
# Version bump
poetry version patch  # or minor/major

# Update changelog
# Edit CHANGELOG.md

# Create release
git tag -a v1.2.3 -m "Release version 1.2.3"
git push origin v1.2.3
```

## 📚 Additional Resources

### Internal Documentation
- [Framework Structure Details](./core/docs/FRAMEWORK_STRUCTURE.md)
- [Architecture Decisions](./core/guidelines/DECISIONS.md)
- [AI Tool Guidelines](./core/guidelines/ki-tool-guidelines.md)
- [Project Management Schema](./data/schemas/project_management_schema.json)
- [Work Items Database](./data/work-items/)

### External Resources
- [Python Documentation](https://docs.python.org/3/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)

## 🤝 Contributing to Framework

### Development Workflow
1. Create feature branch from `main`
2. Make changes following all standards
3. Add tests for new functionality
4. Update documentation
5. Submit pull request

### Code Review Process
- All changes require review
- Automated tests must pass
- Documentation must be updated
- Breaking changes require discussion

---

For AI-specific instructions, see [AI_GUIDE.md](./AI_GUIDE.md).
For the authoritative framework structure, see [core/docs/FRAMEWORK_STRUCTURE.md](./core/docs/FRAMEWORK_STRUCTURE.md).
