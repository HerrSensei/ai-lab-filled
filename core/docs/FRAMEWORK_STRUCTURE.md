# AI Lab Framework Structure

## 🏗️ Single Source of Truth for Framework Architecture

This document provides the authoritative structure of the AI Lab Framework. All components, tools, and documentation should follow this structure exactly.

## 📁 Complete Framework Structure

```
ai-lab/                                    # 🚀 Root Repository
├── README.md                              # Main framework overview
├── GETTING_STARTED.md                     # Single source for setup (NEW)
├── DEVELOPER_GUIDE.md                     # Human developer documentation
├── AI_GUIDE.md                           # AI agent instructions
├── Makefile                              # Build automation
├── pyproject.toml                        # Python dependencies
├── .gitignore                            # Git ignore rules
├── .pre-commit-config.yaml               # Pre-commit hooks
│
├── 🏗️ core/                              # FRAMEWORK CORE (Single Source)
│   ├── docs/                             # Framework documentation
│   │   ├── FRAMEWORK_STRUCTURE.md        # This file (authoritative)
│   │   ├── PROJECT_CONTEXT.md            # AI context summary
│   │   ├── getting-started.md            # Tutorial (references GETTING_STARTED.md)
│   │   ├── analyses/                     # Analysis documents
│   │   └── research/                     # Research findings
│   ├── guidelines/                       # Development standards
│   │   ├── GUIDELINES.md                 # Coding standards
│   │   ├── GUIDELINES_KI_TOOLS.md        # AI tool standards
│   │   ├── DECISIONS.md                  # Architecture decisions
│   │   └── VISION.md                     # Long-term vision
│   ├── templates/                        # Project templates (single source)
│   │   ├── project/                      # Software project templates
│   │   ├── project-management/           # PM templates
│   │   ├── ai_logging/                   # AI logging templates
│   │   └── agentos/                      # AgentOS templates
│   ├── tools/                            # Framework tools
│   │   ├── framework-setup/              # Environment setup
│   │   ├── project-creator/              # Project creation
│   │   └── ai-assistant/                 # AI integration
│   ├── scripts/                          # Utility scripts
│   └── MANUAL.md                         # Framework manual
│
├── 📊 dashboard/                          # Project monitoring
│   ├── DASHBOARD.md                      # Generated dashboard
│   ├── dashboard_generator.py            # Data generator
│   ├── dashboard_data.json               # Raw data
│   └── update_dashboard.sh               # Update script
│
├── 📈 ai-logs/                           # AI session logging
│   ├── change_log/                       # Change history
│   │   └── CHANGELOG.md                  # Main changelog
│   ├── sessions/                         # Session logs
│   └── SYSTEM.md                         # AI logging system docs
│
├── 📋 project-management/                 # Project coordination
│   ├── PROJECT_STATUS.md                 # Overall status
│   └── work-items/                       # Work items and tasks
│
├── 🚀 projects/                          # Active projects
│   └── [project-name]/                   # Individual project directories
│
├── 💾 data/                              # Structured data (JSON-first)
│   ├── ideas/                            # Ideas database
│   ├── work-items/                       # Work items database (JSON)
│   ├── schemas/                          # Data validation schemas
│   └── *.json                            # Data files
│
├── 💡 ideas/                             # Idea development (markdown)
│   ├── backlog/                          # Unprocessed ideas
│   ├── refining/                         # Ideas in development
│   ├── ready/                            # Ready for implementation
│   └── implemented/                      # Completed ideas
│
├── 📚 docs/                              # Public documentation site
│   ├── _site/                            # Generated site
│   ├── assets/                           # Static assets
│   ├── content/                          # Markdown content
│   └── mkdocs.yml                        # Site configuration
│
├── 🔧 tools/                             # Standalone tools
│   └── [tool-name]/                      # Individual tool directories
│
├── 🧪 src/                               # Framework source code
│   └── ai_lab_framework/                # Core framework package
│
├── 🗄️ archive/                           # Archived content
│   ├── reports/                          # Archived reports
│   ├── projects/                         # Archived projects
│   ├── plans/                            # Archived plans
│   └── ARCHIVE_INDEX.md                  # Archive index
│
└── 📜 scripts/                           # Utility scripts
    ├── backup.sh                         # Backup utility
    ├── sync-docs.sh                      # Documentation sync
    └── list_ideas.py                     # Ideas listing
```

## 🎯 Component Responsibilities

### Core Framework (`core/`)
**Purpose**: Single source of truth for all framework components
- **Templates**: Authoritative project templates
- **Guidelines**: Binding development standards
- **Tools**: Framework-specific utilities
- **Documentation**: Internal framework docs

### Data Management (`data/`, `ideas/`)
**Purpose**: Structured information management
- **JSON-first**: All structured data in JSON format
- **Schemas**: Validation schemas for data integrity
- **Markdown**: Idea development and documentation

### Projects (`projects/`)
**Purpose**: Active development work
- **Self-contained**: Each project is independent
- **Template-based**: Created from core templates
- **Standardized**: Consistent structure across projects

### Documentation (`docs/`)
**Purpose**: Public-facing documentation
- **MkDocs-based**: Static site generator
- **Content-focused**: Markdown content in `content/`
- **Generated**: Site built from markdown sources

### Tools (`tools/`)
**Purpose**: Standalone utility tools
- **Independent**: Separate from framework core
- **Specialized**: Each tool has specific purpose
- **Optional**: Not required for framework operation

## 🔄 Data Flow Principles

### 1. Single Source of Truth
- **Templates**: Only in `core/templates/`
- **Guidelines**: Only in `core/guidelines/`
- **Schemas**: Only in `data/schemas/`
- **Structure**: This document is authoritative

### 2. JSON-First Data Management
- **Structured data**: Always JSON format
- **Validation**: Using schemas in `data/schemas/`
- **Markdown**: For documentation and idea development only

### 3. Clear Separation of Concerns
- **Framework core**: `core/` (framework development)
- **Projects**: `projects/` (application development)
- **Data**: `data/` (structured information)
- **Documentation**: `docs/` (public docs)

## 📋 Naming Conventions

### Directories
- **kebab-case**: All directories use kebab-case
- **Descriptive**: Names clearly indicate purpose
- **Consistent**: Same pattern throughout framework

### Files
- **snake_case**: Python files and scripts
- **kebab-case**: Documentation and configuration
- **PascalCase**: Classes and components (where applicable)

### Projects
- **Format**: `project-name` (kebab-case)
- **Templates**: Created from `core/templates/`
- **Independent**: Self-contained structure

## 🚀 Extension Points

### Adding New Tools
1. Create directory in `tools/[tool-name]/`
2. Follow framework naming conventions
3. Include README.md with setup instructions
4. Use framework coding standards

### Adding New Templates
1. Create in `core/templates/[category]/`
2. Follow template structure guidelines
3. Include template documentation
4. Test with project-creator tool

### Adding New Project Types
1. Create template in `core/templates/project/`
2. Update project-creator configuration
3. Document in framework docs
4. Test complete workflow

## 🔍 Maintenance Guidelines

### Regular Tasks
- **Archive completed projects**: Move to `archive/projects/`
- **Update schemas**: Keep `data/schemas/` current
- **Clean cache**: Remove temporary files and caches
- **Update documentation**: Keep docs in sync with changes

### Structural Changes
1. **Update this document first** (FRAMEWORK_STRUCTURE.md)
2. **Update affected components**
3. **Test all workflows**
4. **Update cross-references**

### Quality Assurance
- **Validate JSON**: Use schemas in `data/schemas/`
- **Test templates**: Verify project creation
- **Check links**: Ensure documentation links work
- **Run tests**: Execute framework test suite

## 🎯 Success Metrics

### Structure Health
- **No duplicate directories**: Clear separation of concerns
- **Consistent naming**: All directories follow conventions
- **Working links**: All cross-references functional
- **Up-to-date docs**: Documentation matches structure

### Workflow Efficiency
- **Project creation**: Works from templates
- **Data management**: JSON schemas validate correctly
- **Documentation**: Generates without errors
- **Tools**: Function independently

---
**This document is the single source of truth for AI Lab Framework structure.**
**All structural changes must be reflected here first.**

*Last updated: 2025-11-09*
*Version: 1.0.0*
