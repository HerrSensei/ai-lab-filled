# AI Lab Framework - Project Overview for Gemini

This document provides a comprehensive overview of the AI Lab Framework, designed to serve as instructional context for future interactions with the Gemini CLI.

## Project Overview

The AI Lab Framework is a Python-based project focused on building and managing AI tools. It emphasizes structured development, robust context management, and comprehensive quality assurance. The framework aims to provide a clean, organized, and maintainable structure for developing various AI-related functionalities.

**Key Features:**
*   **Profile System:** A three-tier system (`Experimental`, `Standard`, `Production`) that defines requirements for logging, context management, error handling, testing, documentation, and validation, adapting to different development stages and criticality levels.
*   **Base AI Tool Abstraction:** A `BaseAITool` abstract class that provides a standardized interface for AI tools, integrating profile-specific context management, structured logging, and error recovery mechanisms.
*   **Work Management:** Utilizes JSON-based schemas for managing ideas, work items, and projects, facilitating organized development and tracking.
*   **CLI Workflows:** Detailed command-line interface workflows for various tasks, including session management, project/task management, reporting, analysis, development, quality assurance, and deployment.
*   **Agent-OS Framework Workflows:** Specialized agent workflows built on the agent-os framework for automated task execution. These workflows are currently under development and require review and fixes to reach full functionality.

**Main Technologies:**
*   **Language:** Python (>=3.11)
*   **Dependency Management:** Poetry
*   **CLI Development:** `click`, `rich` (for rich terminal output)
*   **Logging:** `structlog` (for structured logging)
*   **Data Validation:** `pydantic`
*   **Testing:** `pytest`
*   **Code Quality:** `black` (formatter), `ruff` (linter), `mypy` (type checker)
*   **Templating:** `jinja2`

## Building and Running

The project uses Poetry for dependency management. While some `make` commands are referenced in documentation, a root `Makefile` is not present, suggesting these commands might be placeholders, generated, or located in specific subdirectories.

### Setup and Installation

1.  **Install Dependencies:**
    ```bash
    poetry install
    ```

### Core Commands

*   **Main CLI Entry Point:**
    ```bash
    ai-lab
    ```
    (Defined in `pyproject.toml` as `ai_lab.cli:main`)

*   **Project Creator CLI:**
    ```bash
    project-creator
    ```
    (Defined in `pyproject.toml` as `ai_lab.tools.project_creator:main`)

*   **Interactive CLI:**
    ```bash
    interactive-cli
    ```
    (Defined in `pyproject.toml` as `run:main`. This script (`run.py`) is designed to execute `make` targets found in a `makefiles` directory, which is currently not present. Its full functionality depends on the creation and population of this directory.)

### Placeholder/Intended Commands (from `README.md` and `CLI_WORKFLOWS.md`)

The following commands are mentioned in the project's documentation but may require a `Makefile` or further setup to function:

*   `make setup`: Intended for development environment setup.
*   `make test`: Intended for running project tests.
*   `make work-item-new`, `make work-item-update`, `make work-item-list`: For managing work items.
*   `make idea-new`, `make idea-refine`, `make idea-assist`, `make idea-convert`: For managing ideas.
*   `make project-list`, `make project-status`: For managing projects.
*   `make dashboard-update`: For updating project dashboards.
*   `make deploy <ENVIRONMENT>`: For deployment.
*   `make start-dev-env`, `make stop-dev-env`: For managing development environments.

## Development Conventions

The project adheres to high standards of code quality and structured development:

*   **Code Formatting:** Enforced with `black`.
*   **Linting:** Performed with `ruff`.
*   **Type Checking:** Utilizes `mypy` for static type analysis.
*   **Testing:** Comprehensive testing with `pytest`, including code coverage analysis.
*   **Structured Logging:** Implemented using `structlog` for better observability and analysis.
*   **CLI Workflows:** A detailed set of documented CLI workflows (`core/docs/CLI_WORKFLOWS.md`) guides developers through common tasks, ensuring consistency and efficiency.

### Agent-OS Framework Integration

The AI Lab Framework integrates with **Agent-OS** (https://github.com/buildermethods/agent-os) - a spec-driven development system that transforms AI coding from guesswork into structured, reliable workflows.

## Agent-OS Framework Overview

Agent-OS provides a **3-layer context system**:
1. **Standards** - How you build (coding standards, patterns, best practices)
2. **Product** - What you're building and why (vision, roadmap, use cases)  
3. **Specs** - What you're building next (specific features with implementation details)

## Available Agents

The framework includes specialized Agent-OS agents for different domains:

### 🤖 Agent Builder Agent (`agent-builder.md`)
**Purpose**: Meta-agent for creating, editing, and improving Agent-OS agents
**Capabilities**:
- Agent creation with proper YAML frontmatter and metadata
- Workflow design following Agent-OS patterns
- Standards development and integration
- Template generation for common agent types
- Profile management and configuration

### 🏠 Homelab Management Agent (`homelab-manager.md`)
**Purpose**: Manage homelab infrastructure via SSH and CLI tools
**Capabilities**:
- System monitoring (CPU, memory, disk, network usage)
- Service management (Docker containers, systemd services)
- Backup automation with configurable schedules and retention
- Update management for systems and containers
- Health checks and alerting
- Security considerations and access control

### 📊 Project Management Agent (`project-manager.md`)
**Purpose**: Manage projects, tasks, work items, and team coordination
**Capabilities**:
- Project planning with scope, objectives, and deliverables
- Task management with dependencies and prioritization
- Progress tracking and milestone management
- Resource coordination and team assignment
- Agile methodology support (Scrum, Kanban, hybrid)
- Risk management and mitigation strategies

### 🔒 Security & Compliance Agent (`security-compliance.md`)
**Purpose**: Security scanning, compliance checking, access control, and incident response
**Capabilities**:
- Vulnerability scanning and security assessments
- Compliance monitoring (GDPR, SOC2, ISO27001, HIPAA, PCI DSS)
- Access control with identity and permission management
- Incident response with classification and handling
- Risk assessment and mitigation
- Security auditing and policy management

## Using Agent-OS Agents

### Configuration
The framework uses `projects/Homelab-Orchestrator/agent-os/config.yml`:
```yaml
version: 2.1.1
base_install: true
claude_code_commands: true
agent_os_commands: true
use_claude_code_subagents: true
standards_as_claude_code_skills: false
profile: homelab
```

### Profile Structure
```
projects/Homelab-Orchestrator/agent-os/profiles/homelab/
├── agents/          # Agent definitions (.md files)
├── standards/        # Coding standards and best practices
└── commands/         # Command templates
```

### Agent Usage
Each agent follows Agent-OS patterns:
- **YAML Frontmatter**: Metadata with name, description, tools, color, model
- **Workflow References**: `{{workflows/*}}` syntax for workflow integration
- **Standards Integration**: `{{standards/*}}` syntax for standards compliance
- **Context Awareness**: Specific to AI Lab Framework tech stack and patterns

## Implementation Status

**✅ Completed:**
- Agent Builder Agent for creating and improving agents
- Homelab Management Agent for infrastructure management
- Project Management Agent for task and project coordination
- Security & Compliance Agent for security and compliance
- Proper Agent-OS profile structure and configuration
- Integration with AI Lab Framework standards

**📋 Planned Work Items:**
- Development Workflow Agent (PROJ-336F4EE3-WI-A1478773)
- Data & Analytics Agent (PROJ-336F4EE3-WI-7E62E290)

## Getting Started

1. **Install Agent-OS**: Follow setup from https://buildermethods.com/agent-os
2. **Configure Profile**: Use the homelab profile in `projects/Homelab-Orchestrator/agent-os/`
3. **Select Agent**: Choose appropriate agent for your task
4. **Execute Commands**: Use Agent-OS commands or Claude Code integration
5. **Follow Standards**: Agents automatically apply AI Lab Framework standards

### Agent-OS Integration with Gemini CLI

When working with Agent-OS agents, use the following approach:

1. **Select Appropriate Agent**: Choose agent based on task domain (homelab, project management, security, etc.)
2. **Use Agent Commands**: Execute Agent-OS commands through Claude Code or direct prompts
3. **Follow Agent Guidance**: Agents provide structured workflows and domain-specific expertise
4. **Leverage Standards**: Agents automatically apply AI Lab Framework standards
5. **Iterate with Agent Builder**: Use agent-builder.md to create or improve agents as needed

### Subtask Management for Gemini CLI

When working on a work item or a task from a project, it is crucial to break down complex tasks into smaller, manageable subtasks. These subtasks should then be added to the Gemini CLI's internal todo list. This ensures clear progress tracking, organization of complex queries, and comprehensive task completion.

*   **Break Down Tasks:** Decompose large tasks into distinct, actionable subtasks.
*   **Add to Todo List:** Utilize the `write_todos` tool to add these subtasks to the current session's todo list.
*   **Track Progress:** Mark subtasks as `pending`, `in_progress`, `completed`, or `cancelled` as work progresses.
*   **Iterative Refinement:** The todo list is dynamic; update it as new information emerges or plans evolve.

## Project Structure

*   **`src/`**: Contains the core framework code, including AI tool abstractions, profile definitions, and infrastructure services.
*   **`data/`**: Stores JSON-based work management artifacts such as schemas for ideas, work items, and projects, along with actual work item and idea data.
*   **`core/`**: Houses templates, extensive documentation (including CLI workflows and architectural guidelines), and audit reports.
*   **`tools/`**: Contains specific tool implementations, such as the `fritzbox` integration.
*   **`projects/`**: An empty directory intended for generated projects, serving as a placeholder for new project scaffolding.
*   **`pyproject.toml`**: Project configuration, dependencies, and script definitions.
*   **`run.py`**: An interactive CLI script designed to execute `make` targets, acting as a central operational interface.

## 🚨 Database Interaction (ALWAYS VERIFY)
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