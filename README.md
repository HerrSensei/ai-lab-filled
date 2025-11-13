# 🧠 AI Lab Framework

<div align="center">

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Status](https://img.shields.io/badge/status-✅%20Ready%20for%20Development-green.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

*A clean, organized framework for building AI-powered development environments*

[Quick Start](#-quick-start) • [Status Overview](#-status-overview) • [Documentation](#-documentation) • [Changelog](#-changelog)

</div>

---

## 🚀 Quick Start

```bash
# Install dependencies
poetry install

# Set up development environment
cp .env.template .env
# Edit .env with your configuration

# Run the framework
python -m ai_lab_framework
```

---

## 📊 Status Overview

### 🎯 Work Items (49 total)

| Status | Count | Progress |
|--------|-------|----------|
| ✅ Done | 20 | 40.8% |
| 🔄 In Progress | 6 | 12.2% |
| 📋 To Do | 12 | 24.5% |
| 🔓 Open | 7 | 14.3% |
| 📦 Backlog | 1 | 2.0% |
| ✅ Completed | 2 | 4.1% |
| ❌ Cancelled | 1 | 2.0% |

**By Priority:**
- 🔴 Critical: 1
- 🔴 High: 36
- 🟡 Medium: 12

**By Type:**
- 🛠️ FRM (Framework): 35
- 🔧 HS (Hotfix): 9
- 🏗️ INF (Infrastructure): 3
- 🔄 HYB (Hybrid): 1
- 💡 IDEA: 1

### 💡 Ideas (11 total)

| Status | Count | Progress |
|--------|-------|----------|
| 🔄 Converted | 5 | 45.5% |
| ✅ Implemented | 2 | 18.2% |
| 📦 Backlog | 4 | 36.4% |

**By Priority:**
- 🔴 High: 6
- 🟡 Medium: 5

### 🏗️ Projects (1 total)

| Project | Status | Description |
|---------|--------|-------------|
| 🏠 homelab-agent-os | ✅ Complete | Home infrastructure automation with agent OS |

---

## 📁 Framework Structure

```
├── 📂 src/                    # Core framework code
│   ├── 🤖 ai_lab_framework/   # Main framework modules
│   ├── 🔌 core/               # Core interfaces and ports
│   └── 🏗️ infrastructure/     # Database and AI services
├── 📂 core/                   # Templates and documentation
│   ├── 📚 docs/               # Framework documentation
│   ├── 📋 guidelines/         # Development guidelines
│   └── 📄 templates/          # Project templates
├── 📂 tools/                  # Tool implementations
│   └── 🌐 fritzbox/           # Network automation tools
├── 📂 data/                   # Data management
│   ├── 💡 ideas/              # Innovation ideas (11)
│   ├── 📋 work-items/         # Task management (49)
│   └── 🗂️ schemas/            # JSON schemas
├── 📂 scripts/                # Utility scripts
├── 📂 projects/               # Generated projects
└── 📂 tests/                  # Test suite
```

---

## 🎯 Key Features

### ✅ **Core Framework**
- **Multi-AI Service Support**: OpenAI, Gemini, and extensible AI providers
- **Profile System**: Three-tier configuration for different deployment scenarios
- **Database Integration**: SQLite with SQLAlchemy ORM and migrations
- **Tool Generation**: Dynamic tool creation and management system
- **GitHub Integration**: Repository management and automation

### ✅ **Data Management**
- **JSON-based Work Items**: 49 structured tasks with schema validation
- **Ideas System**: 11 innovation concepts with status tracking
- **Schema Validation**: Comprehensive JSON schemas for data integrity
- **Migration Tools**: Automated data migration and backup systems

### ✅ **Development Tools**
- **Project Templates**: Complete scaffolding for different project types
- **CLI Workflows**: 20+ documented command-line procedures
- **Code Quality**: Black, Ruff, MyPy integration with pre-commit hooks
- **Testing**: Pytest with coverage and comprehensive test suite

### ✅ **Documentation**
- **Comprehensive Guides**: Vision, guidelines, and best practices
- **API Documentation**: Complete reference documentation
- **Tutorials**: Step-by-step implementation guides
- **Changelog**: Detailed version history and change tracking

---

## 🛠️ Development

### Code Quality Tools
```bash
# Code formatting
black .                       # Format code
ruff check --fix .            # Lint and auto-fix
mypy .                        # Type checking

# Testing
pytest                        # Run all tests
pytest --cov=src              # With coverage
pytest -x                     # Stop on first failure
```

### Project Management
```bash
# List work items
python scripts/list_work_items.py

# List ideas
python scripts/list_ideas.py

# Generate project
python -m ai_lab.tools.project_generator
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [📖 Framework Structure](core/docs/FRAMEWORK_STRUCTURE.md) | Complete architecture overview |
| [🔧 CLI Workflows](core/docs/CLI_WORKFLOWS.md) | 20+ command-line procedures |
| [📋 Guidelines](core/guidelines/GUIDELINES.md) | Development standards and practices |
| [🎯 Vision](core/guidelines/VISION.md) | Project vision and roadmap |
| [🤖 Agent Guidelines](AGENTS.md) | AI agent development guidelines |

---

## 📈 Changelog

### 🆕 [Version 2.0.0] - 2025-11-13

#### ✨ Added
- Clean framework rebuild from messy backup
- JSON-based ideas management system (11 ideas)
- Complete project scaffolding templates
- Three-tier AI tool profile system
- Comprehensive documentation and workflows
- FritzBox MCP server integration
- Schema validation for all data structures

#### 🔄 Changed
- Migrated from markdown-based to JSON-based data management
- Improved framework architecture with clean separation of concerns
- Enhanced project templates with modern best practices
- Updated naming conventions for consistency

#### 🐛 Fixed
- Eliminated organizational complexity from original framework
- Resolved duplicate documentation issues
- Fixed broken component references
- Cleaned cache and artifact accumulation

#### 🔒 Security
- Improved API key management guidelines
- Enhanced input validation with Pydantic
- Added security best practices to templates

**[📋 View Full Changelog →](ai-logs/change_log/CHANGELOG.md)**

---

## 🏗️ Architecture

### 🎯 Three-Tier Profile System

1. **🔧 Development Profile**
   - Local AI services
   - Development databases
   - Debug logging enabled

2. **🚀 Staging Profile**
   - Cloud AI services
   - Staging databases
   - Performance monitoring

3. **🌐 Production Profile**
   - Production AI services
   - Production databases
   - Security-hardened configuration

### 🔄 Data Flow

```
📝 Input → 🔍 Validation → 🤖 AI Processing → 💾 Storage → 📊 Output
    ↓           ↓              ↓              ↓         ↓
📋 Schemas   ✅ Checks     🧠 LLMs     🗄️ Database  📈 Reports
```

---

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Requirements
- Python 3.11+
- Poetry for dependency management
- Follow [AGENTS.md](AGENTS.md) guidelines
- Ensure all tests pass
- Update documentation as needed

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **AI Agents** for framework development and maintenance
- **Open Source Community** for the amazing tools and libraries
- **Contributors** who help improve this framework

---

<div align="center">

**🌟 Star this repository if it helps you!**

Made with ❤️ by the AI Lab Team

</div>