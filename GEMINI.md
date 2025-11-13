# AI Lab Framework - Project Overview for Gemini

This document provides a comprehensive overview of the AI Lab Framework, designed to serve as instructional context for future interactions with the Gemini CLI.

## Project Overview

The AI Lab Framework is a Python-based project focused on building and managing AI tools. It emphasizes structured development, robust context management, and comprehensive quality assurance. The framework aims to provide a clean, organized, and maintainable structure for developing various AI-related functionalities.

**Key Features:**
*   **Profile System:** A three-tier system (`Experimental`, `Standard`, `Production`) that defines requirements for logging, context management, error handling, testing, documentation, and validation, adapting to different development stages and criticality levels.
*   **Base AI Tool Abstraction:** A `BaseAITool` abstract class that provides a standardized interface for AI tools, integrating profile-specific context management, structured logging, and error recovery mechanisms.
*   **Work Management:** Utilizes JSON-based schemas for managing ideas, work items, and projects, facilitating organized development and tracking.
*   **CLI Workflows:** Detailed command-line interface workflows for various tasks, including session management, project/task management, reporting, analysis, development, quality assurance, and deployment.

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

## Project Structure

*   **`src/`**: Contains the core framework code, including AI tool abstractions, profile definitions, and infrastructure services.
*   **`data/`**: Stores JSON-based work management artifacts such as schemas for ideas, work items, and projects, along with actual work item and idea data.
*   **`core/`**: Houses templates, extensive documentation (including CLI workflows and architectural guidelines), and audit reports.
*   **`tools/`**: Contains specific tool implementations, such as the `fritzbox` integration.
*   **`projects/`**: An empty directory intended for generated projects, serving as a placeholder for new project scaffolding.
*   **`pyproject.toml`**: Project configuration, dependencies, and script definitions.
*   **`run.py`**: An interactive CLI script designed to execute `make` targets, acting as a central operational interface.
