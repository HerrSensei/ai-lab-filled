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

## Agent-OS Framework Integration

The AI Lab Framework integrates with **Agent-OS** (https://github.com/buildermethods/agent-os) - a spec-driven development system that provides structured workflows for AI agents.

### Framework Overview

Agent-OS uses a **3-layer context system**:
- **Standards** → **Product** → **Specs**
- Coding standards and patterns inform product vision
- Product vision guides specific feature specifications
- Feature specifications drive implementation details

### Available Agents

The framework includes production-ready Agent-OS agents:

#### 🤖 Agent Builder Agent (`agent-builder.md`)
**Meta-agent for creating and improving Agent-OS agents**
- Agent creation with proper YAML frontmatter and metadata
- Workflow design following Agent-OS patterns  
- Standards development and integration
- Template generation for common agent types
- Profile management and configuration

#### 🏠 Homelab Management Agent (`homelab-manager.md`)
**Infrastructure management via SSH and CLI tools**
- System monitoring (CPU, memory, disk, network)
- Service management (Docker, systemd, custom services)
- Backup automation with schedules and retention
- Update management for systems and containers
- Health checks with alerting
- Security best practices and access control

#### 📊 Project Management Agent (`project-manager.md`)
**Project, task, and team coordination**
- Project planning with scope and objectives
- Task management with dependencies and prioritization
- Progress tracking and milestone management
- Resource coordination and team assignments
- Agile methodologies (Scrum, Kanban, hybrid)
- Risk management and mitigation strategies

#### 🔒 Security & Compliance Agent (`security-compliance.md`)
**Security scanning, compliance, and incident response**
- Vulnerability scanning and security assessments
- Compliance monitoring (GDPR, SOC2, ISO27001, HIPAA)
- Access control with identity and permission management
- Incident response with classification and handling
- Risk assessment and mitigation frameworks
- Security auditing and policy enforcement

### Agent-OS Profile Structure

```
projects/Homelab-Orchestrator/agent-os/
├── config.yml                    # Agent-OS configuration
├── profiles/
│   └── homelab/
│       ├── agents/              # Agent definitions
│       │   ├── agent-builder.md
│       │   ├── homelab-manager.md
│       │   ├── project-manager.md
│       │   └── security-compliance.md
│       ├── standards/            # Coding standards
│       │   └── tech-stack.md
│       └── commands/             # Command templates
└── agents/                      # Legacy implementations
```

### Configuration

The `config.yml` defines Agent-OS behavior:
```yaml
version: 2.1.1
base_install: true
claude_code_commands: true      # Install in .claude/commands/
agent_os_commands: true         # Install in agent-os/commands/
use_claude_code_subagents: true # Use subagents delegation
standards_as_claude_code_skills: false
profile: homelab               # Default profile
```

### Using Agent-OS Agents

#### Agent Structure
Each agent follows Agent-OS standards:
- **YAML Frontmatter**: Metadata (name, description, tools, color, model)
- **Workflow References**: `{{workflows/*}}` syntax for workflow integration
- **Standards Integration**: `{{standards/*}}` syntax for compliance
- **Context Awareness**: Specific to AI Lab Framework tech stack

#### Usage Patterns
1. **Select Agent**: Choose based on task domain
2. **Execute Commands**: Use Agent-OS commands or Claude Code
3. **Follow Guidance**: Agents provide structured workflows
4. **Apply Standards**: Automatic compliance with AI Lab Framework patterns

### Implementation Status

**✅ Completed:**
- Agent Builder Agent for meta-agent capabilities
- Homelab Management Agent for infrastructure
- Project Management Agent for coordination
- Security & Compliance Agent for security
- Proper Agent-OS profile structure
- Integration with AI Lab Framework standards
- Configuration and command templates

**📋 Planned Work Items:**
- Development Workflow Agent (PROJ-336F4EE3-WI-A1478773)
- Data & Analytics Agent (PROJ-336F4EE3-WI-7E62E290)

### Agent Development Guidelines

When creating or modifying Agent-OS agents:

1. **Follow Framework Patterns**: Use established Agent-OS structure
2. **Proper YAML Frontmatter**: Include all required metadata fields
3. **Workflow Integration**: Use `{{workflows/*}}` and `{{standards/*}}` syntax
4. **Domain Expertise**: Include specialized knowledge for agent type
5. **Error Handling**: Comprehensive error recovery and guidance
6. **Tool Integration**: Specify required tools and their usage
7. **Context Awareness**: Align with AI Lab Framework patterns

### Agent-OS Development Workflow

When working with Agent-OS agents, follow this structured approach:

1. **Requirements Analysis**: Use Agent Builder Agent to analyze needs
2. **Agent Selection**: Choose appropriate agent for the domain
3. **Configuration**: Set up agent with proper standards and context
4. **Execution**: Run Agent-OS commands through Claude Code or direct prompts
5. **Iteration**: Use Agent Builder to refine and improve agents
6. **Integration**: Ensure agents work with AI Lab Framework systems

### Agent Development Best Practices

When creating or modifying Agent-OS agents:

1. **Use Agent Builder**: Leverage the meta-agent for agent creation
2. **Follow Framework Patterns**: Maintain Agent-OS structure and conventions
3. **Test Thoroughly**: Validate agents in isolated environments
4. **Document Clearly**: Provide comprehensive agent documentation
5. **Iterate Based on Feedback**: Continuously improve agent performance
6. **Maintain Standards**: Ensure compliance with AI Lab Framework patterns

### Subtask Management for Agent Development

When developing agents or working on tasks related to agent development, it is crucial to break down complex tasks into smaller, manageable subtasks. These subtasks should then be added to the Gemini CLI's internal todo list. This ensures clear progress tracking, organization of complex queries, and comprehensive task completion.

*   **Break Down Tasks:** Decompose large tasks into distinct, actionable subtasks.
*   **Add to Todo List:** Utilize the `write_todos` tool to add these subtasks to the current session's todo list.
*   **Track Progress:** Mark subtasks as `pending`, `in_progress`, `completed`, or `cancelled` as work progresses.
*   **Iterative Refinement:** The todo list is dynamic; update it as new information emerges or plans evolve.
