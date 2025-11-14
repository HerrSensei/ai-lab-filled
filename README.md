# AI Lab Framework

Core framework code for building AI-powered development tools and agents.

## Purpose

This repository contains the essential framework components only:

- **Core AI Lab Framework** (`src/ai_lab_framework/`)
- **Project Templates** (`core/templates/`)
- **Development Guidelines** (`core/guidelines/`)
- **Data Schemas** (`data/schemas/`)

## Installation

```bash
# Install dependencies
poetry install

# Or with pip
pip install -e .
```

## Framework Components

### AI Lab Framework (`src/ai_lab_framework/`)
- `base_ai_tool.py` - Base class for AI tools
- `database.py` - Database abstraction layer
- `github_integration.py` - GitHub API integration
- `profiles.py` - AI tool profile management
- `tool_generator.py` - Automated tool generation

### Templates (`core/templates/`)
- **Agent OS** (`agentos/`) - Agent configuration templates
- **Projects** (`project/`) - Project structure templates
- **Examples** (`examples/`) - Usage examples

### Schemas (`data/schemas/`)
- JSON schemas for data validation
- Database schema definitions
- Work item and idea schemas

## Usage

```python
from ai_lab_framework import BaseAITool, ProfileManager

# Create a new AI tool
class MyTool(BaseAITool):
    def execute(self, input_data):
        return self.ai_service.process(input_data)

# Load profiles
profiles = ProfileManager()
profile = profiles.get_profile("my-profile")
```

## Repository Structure

- `ai-lab` - Main repository (coordination)
- `ai-lab-filled` - Framework + data/examples
- `ai-lab-framework` - Framework only (this repo)

## Development

See `AGENTS.md` for development guidelines and build commands.

## License

MIT License - see LICENSE file for details.