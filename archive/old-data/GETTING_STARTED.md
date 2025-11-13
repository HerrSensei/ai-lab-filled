# Getting Started Guide - AI Lab Framework

## 🎯 Welcome to the AI Lab Framework

This guide provides everything you need to get started with the AI Lab Framework. Whether you're a human developer or AI agent, this is your single source of truth for initial setup and project creation.

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- **Python 3.11+** - Required for all framework operations
- **Docker & Docker Compose** - For containerized development
- **Git** - Version control
- **Make** - Build automation (included with most dev tools)

### 1. Framework Setup
```bash
# Clone and setup the framework
git clone <repository-url>
cd ai-lab

# Complete environment setup (installs all dependencies)
make setup

# Verify installation
make test
```

### 2. Create Your First Project
```bash
# Interactive project creation (recommended for beginners)
./core/tools/project-creator/bin/project-creator

# Quick project creation
./core/tools/project-creator/bin/project-creator --standard my-project

# AI/ML specific project
./core/tools/project-creator/bin/project-creator --type ai_ml my-ml-project
```

### 3. Start Development
```bash
# Navigate to your project
cd projects/my-project

# Start development environment
make dev

# Generate project diagrams
make diagrams
```

## 🤖 AI Assistant Integration

### Available AI Assistants
- **opencode** - OpenAI-based assistant (recommended)
- **gemini-cli** - Google Gemini assistant

### Using AI Assistists
```bash
# Interactive AI assistant selection
make ai-assistant

# Open project with specific assistant
make open-with-opencode projects/my-project
make open-with-gemini projects/my-project

# Check AI tools installation
make check-ai-tools
```

## 📊 Dashboard & Monitoring

### Project Dashboard
The AI Lab Dashboard provides real-time project monitoring:
```bash
# Update dashboard with latest data
./dashboard/update_dashboard.sh

# View dashboard in browser
open dashboard/DASHBOARD.md
```

### Dashboard Features
- **Project Status Tracking** - Real-time status of all projects
- **Blocker Management** - Identify and resolve obstacles
- **Next-Step Recommendations** - AI-powered suggestions
- **Progress Visualization** - Charts and metrics

## 🛠️ Development Tools

### Code Quality & Testing
```bash
# Code formatting
black .

# Linting and import sorting
ruff check --fix .

# Type checking
mypy .

# Run all tests
make test

# Run tests with coverage
pytest --cov=src
```

### Pre-commit Hooks
```bash
# Install pre-commit hooks
pre-commit install

# Run all hooks manually
pre-commit run --all-files
```

## 📁 Understanding the Structure

### Core Framework Components
```
ai-lab/
├── core/                    # Framework core components
│   ├── docs/               # Framework documentation
│   ├── guidelines/         # Development standards
│   ├── templates/          # Project templates
│   └── tools/              # Framework tools
├── projects/               # Your projects
├── data/                   # Structured data (JSON)
├── dashboard/              # Project monitoring
└── docs/                   # Public documentation site
```

### Project Structure
```
projects/my-project/
├── README.md               # Project overview
├── pyproject.toml          # Dependencies and config
├── Makefile               # Project commands
├── src/                   # Source code
└── tests/                 # Test files
```

## 🎯 Project Types

### Available Project Templates
- **standard** - General Python project
- **ai_ml** - AI/ML project with model support
- **api** - FastAPI web service
- **cli** - Command-line tool
- **library** - Python package

### Template Features
- **Pre-configured tooling** - Black, Ruff, MyPy, Pytest
- **CI/CD ready** - GitHub Actions workflows
- **Documentation** - MkDocs setup
- **Docker support** - Containerization ready

## 🔧 Advanced Configuration

### Custom Project Templates
```bash
# Create project from custom template
./core/tools/project-creator/bin/project-creator \
  --template /path/to/custom-template \
  my-custom-project
```

### Environment Variables
```bash
# AI Lab Framework settings
export AI_LAB_DEV_MODE=true
export AI_LAB_LOG_LEVEL=DEBUG
export AI_LAB_DASHBOARD_AUTO_UPDATE=true
```

### Tool Configuration
- **Editor Integration** - VS Code, PyCharm settings
- **Docker Registry** - Custom registry configuration
- **AI Model Settings** - OpenAI/Gemini API keys

## 📚 Next Steps

### For Human Developers
1. **Read the Developer Guide** - `DEVELOPER_GUIDE.md`
2. **Explore Framework Structure** - `core/docs/FRAMEWORK_STRUCTURE.md`
3. **Review Coding Standards** - `core/guidelines/GUIDELINES.md`
4. **Join the Community** - Check `core/guidelines/VISION.md`

### For AI Agents
1. **Read AI Agent Guide** - `AI_GUIDE.md`
2. **Understand Context** - `core/docs/PROJECT_CONTEXT.md`
3. **Setup AI Logging** - `ai-logs/SYSTEM.md`
4. **Follow Agent Standards** - `core/guidelines/ki-tool-guidelines.md`

## 🆘 Troubleshooting

### Common Issues

**Framework setup fails**
```bash
# Check Python version
python --version  # Should be 3.11+

# Update pip
pip install --upgrade pip

# Clean setup
make clean && make setup
```

**Project creation fails**
```bash
# Check permissions
ls -la core/tools/project-creator/bin/project-creator

# Make executable
chmod +x core/tools/project-creator/bin/project-creator
```

**AI assistant not working**
```bash
# Check installation
make check-ai-tools

# Install missing tools
make install-ai-tools
```

**Dashboard not updating**
```bash
# Check Python dependencies
python -c "import json, pathlib; print('OK')"

# Manual update
python dashboard/dashboard_generator.py
```

### Getting Help
- **Documentation** - Check `docs/` directory
- **Issues** - Create GitHub issue
- **Community** - Check community guidelines in `core/guidelines/`

## 🎉 Success!

You now have:
- ✅ Framework installed and configured
- ✅ First project created
- ✅ Development environment ready
- ✅ AI assistants available
- ✅ Dashboard monitoring active

**Welcome to the AI Lab Framework!** 🚀

---
*This document is the single source of truth for getting started. All other getting started content should reference this file.*
*Last updated: 2025-11-09*
