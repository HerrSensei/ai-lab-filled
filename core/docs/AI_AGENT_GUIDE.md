# AI Lab Framework - AI Agent Guide

## 🤖 Purpose

This guide provides specific instructions for AI agents working with the AI Lab Framework. It assumes you are an AI assistant tasked with development, analysis, or modification tasks within this framework.

## 🎯 MANDATORY REQUIREMENTS

### 1. Context Analysis (REQUIRED)
Before ANY action, you MUST read and analyze these files in order:

```python
def mandatory_context_analysis():
    """Required context reading sequence for all AI agents."""
    context_files = [
        "project_management.json",           # SSoT for Framework project management
        "data/projects.json",                # SSoT for all projects database
        "core/docs/PROJECT_CONTEXT.md",      # Overall framework overview
        "core/docs/FRAMEWORK_STRUCTURE.md", # Authoritative structure
        "core/guidelines/VISION.md",         # Strategic alignment
        "core/guidelines/GUIDELINES.md",     # Technical standards
    ]

    for file_path in context_files:
        content = read_file(file_path)
        analyze_framework_context(content)

    return context_understanding
```

### 2. Project Management (REQUIRED)
Project status, milestones, and tasks are managed exclusively in JSON files. Markdown-based project management files (`project-management/PROJECT_STATUS.md`, `project-management/work-items/*.md`) are **DEPRECATED**.

- **`project_management.json`**: Main file for the AI Lab Framework meta-project. Contains high-level tasks, milestones, and risks for the framework itself.
- **`data/projects.json`**: Database of all projects managed within the AI Lab.

You MUST consult these files for any project management related queries.

### 3. AI Logging (REQUIRED)
All AI agents MUST log their activities:

```python
def mandatory_ai_logging():
    """Required logging for all AI agent activities."""

    # Session logging
    session_log = f"ai-logs/sessions/{datetime.now().strftime('%Y-%m-%d')}_session-{session_id}.md"

    # Change logging
    change_log = "ai-logs/change_log/CHANGELOG.md"

    return {
        "session_log": session_log,
        "change_log": change_log
    }
```

## 🔄 MANDATORY WORKFLOW

### Step 1: Context Analysis
```markdown
## Context Analysis Checklist
- [ ] core/docs/PROJECT_CONTEXT.md read and understood
- [ ] core/docs/FRAMEWORK_STRUCTURE.md analyzed
- [ ] core/guidelines/VISION.md reviewed for strategic alignment
- [ ] core/guidelines/GUIDELINES.md checked for technical standards
- [ ] Current task aligned with framework principles
```

### Step 2: Session Logging
```markdown
# Session: {Date} Session-{ID}

## Context Analysis
- PROJECT_CONTEXT.md analyzed: ✅
- FRAMEWORK_STRUCTURE.md reviewed: ✅
- VISION.md consulted: ✅
- GUIDELINES.md sections reviewed: [specific sections]

## Task Understanding
- Primary objective: [task description]
- Framework alignment: [how task aligns with framework]
- Dependencies: [what this task depends on]
- Impact: [what this task will affect]

## Planned Actions
1. [Action 1]
2. [Action 2]
3. [Action 3]
```

### Step 3: Implementation with Change Logging
```markdown
## [Unreleased]

### Added
- [New feature or functionality added]

### Changed
- [Modification to existing functionality]

### Fixed
- [Bug fix or problem resolution]

### Removed
- [Removed functionality or deprecated code]
```

## 📁 Framework Structure Understanding

### Core Principle: Single Source of Truth
```
core/                           # ALL framework-relevant code
├── docs/                       # Documentation (single source)
├── guidelines/                 # Standards and vision (single source)
├── templates/                  # Project templates (single source)
├── tools/                      # Framework tools (single source)
└── scripts/                    # Framework scripts (single source)
```

### Key Rules for AI Agents
1. **NEVER** create framework-relevant code outside `core/`
2. **ALWAYS** use templates from `core/templates/`
3. **NEVER** duplicate framework functionality
4. **ALWAYS** follow naming conventions from guidelines
5. **MUST** log all changes in AI logging system

## 🛠️ Common AI Agent Tasks

### Task 1: Creating New Projects
```python
def create_project_workflow(project_name: str, project_type: str):
    """Standard workflow for project creation."""

    # 1. Context analysis (mandatory)
    context = analyze_framework_context()

    # 2. Use project-creator tool (never manual creation)
    tool_path = "core/tools/project-creator/bin/project-creator"
    command = f"{tool_path} --type {project_type} {project_name}"

    # 3. Log the action
    log_change(f"Created project: {project_name} (type: {project_type})")

    return execute_command(command)
```

### Task 2: Modifying Framework Structure
```python
def modify_framework_workflow(change_description: str):
    """Standard workflow for framework modifications."""

    # 1. Context analysis (mandatory)
    context = analyze_framework_context()

    # 2. Impact analysis
    impact = analyze_change_impact(change_description)

    # 3. Check framework principles
    if violates_single_source_of_truth(change_description):
        raise Exception("Change violates Single Source of Truth principle")

    # 4. Implement change
    result = implement_framework_change(change_description)

    # 5. Update documentation
    update_framework_documentation(change_description, result)

    # 6. Log changes
    log_framework_change(change_description, result)

    return result
```

### Task 3: Template Management
```python
def template_management_workflow():
    """Rules for template management."""

    # Templates ONLY exist in core/templates/
    template_source = "core/templates/"

    # NEVER create templates elsewhere
    # ALWAYS use existing templates as base
    # MAINTAIN template naming conventions

    return template_source
```

## 📋 Naming Conventions (AI Agent Compliance)

### Directory Names
```python
# ✅ Correct
directory_names = [
    "project-creator",
    "framework-setup",
    "work-items",
    "ai-logging"
]

# ❌ Wrong (violates kebab-case)
wrong_names = [
    "projectCreator",
    "frameworkSetup",
    "work_items",
    "aiLogging"
]
```

### File Names
```python
# ✅ Correct formats
file_formats = {
    "scripts": "setup_ai_lab.sh",
    "documentation": "getting-started.md",
    "work_items": "HS-001_netzwerk-fixen.md",
    "templates": "README.md.template"
}

# ❌ Wrong formats
wrong_formats = {
    "scripts": "setupAiLab.sh",
    "documentation": "gettingStarted.md",
    "work_items": "netzwerkfixen.md",
    "templates": "README.template"
}
```

## 🔍 Decision Making Framework

### Before Any Action, Ask:
1. **Context**: Have I read all required context files?
2. **Alignment**: Does this action align with VISION.md?
3. **Standards**: Does this follow GUIDELINES.md?
4. **Structure**: Does this respect FRAMEWORK_STRUCTURE.md?
5. **Logging**: Have I set up proper AI logging?
6. **Impact**: What will this change affect?

### Decision Tree
```python
def ai_agent_decision_tree(action: str):
    """Decision framework for AI agents."""

    if not context_analyzed():
        return "ANALYZE_CONTEXT_FIRST"

    if not aligns_with_vision(action):
        return "CONSULT_VISION_MD"

    if not follows_guidelines(action):
        return "CHECK_GUIDELINES_MD"

    if violates_structure(action):
        return "REVIEW_FRAMEWORK_STRUCTURE_MD"

    if not logging_setup():
        return "SETUP_AI_LOGGING"

    return "PROCEED_WITH_IMPLEMENTATION"
```

## 🤖 AI Assistant Integration

### Framework AI Assistant Tools
The AI Lab Framework provides specialized integration with AI coding assistants:

#### Available AI Assistants
1. **opencode** - OpenAI GPT-based assistant
2. **gemini-cli** - Google Gemini-based assistant

#### AI Assistant Workflow
```bash
# For AI agents working on projects
make check-ai-tools                    # Verify tools available
make ai-assistant                       # Interactive mode
make open-with-opencode projects/target  # Open specific project
make open-with-gemini projects/target    # Alternative assistant
```

#### AI Context Integration
When using AI assistant integration, the framework automatically:
- Creates context files with project information
- Provides AI Lab Framework guidelines
- Includes current project status
- Sets up development instructions

#### AI Agent Best Practices
```python
def ai_assistant_integration_workflow():
    """Best practices for AI agents using framework integration."""

    # 1. Always use framework integration
    use_make_targets = [
        "make check-ai-tools",
        "make open-with-opencode project_path",
        "make open-with-gemini project_path"
    ]

    # 2. Leverage auto-generated context
    context_files = [
        ".opencode-context.md",  # Auto-generated for opencode
        ".gemini-context.md"     # Auto-generated for gemini
    ]

    # 3. Follow framework guidelines in AI interactions
    ai_interaction_rules = {
        "respect_structure": "Follow FRAMEWORK_STRUCTURE.md",
        "maintain_consistency": "Apply GUIDELINES.md standards",
        "update_documentation": "Keep PROJECT_OVERVIEW.md current",
        "log_changes": "Use ai-logs/ for change tracking"
    }

    return framework_compliant_ai_work
```

#### AI Assistant Context Template
The framework generates context files with this structure:
```markdown
# AI Lab Project Context

## Project Information
- **Project Name**: [project_name]
- **Framework**: AI Lab Framework
- **Directory**: [project_path]

## Project Structure
This is an AI Lab Framework project with:
- work_items/: Project management and tasks
- src/: Source code
- docs/: Documentation
- tests/: Test files
- PROJECT_OVERVIEW.md: Project overview and status

## AI Assistant Guidelines
1. Follow the AI Lab Framework guidelines
2. Use the existing project structure
3. Update PROJECT_OVERVIEW.md when making significant changes
4. Create work items for new features or tasks
5. Follow the coding standards defined in the framework
```

#### AI Agent Integration Commands
```bash
# For AI agents to open projects with proper context
./core/tools/ai-assistant/scripts/ai_assistant.sh --opencode projects/target
./core/tools/ai-assistant/scripts/ai_assistant.sh --gemini projects/target

# Interactive mode for AI agents
./core/tools/ai-assistant/scripts/ai_assistant.sh --interactive
```
```

## 🚨 Forbidden Actions

### NEVER Do These:
1. **Create framework code outside `core/`**
2. **Duplicate existing functionality**
3. **Ignore naming conventions**
4. **Skip context analysis**
5. **Forget AI logging**
6. **Modify templates directly in projects**
7. **Create conflicting documentation**

### ALWAYS Do These:
1. **Read context files first**
2. **Use existing tools and templates**
3. **Follow naming conventions**
4. **Log all activities**
5. **Update relevant documentation**
6. **Test changes before completion**
7. **Align with framework principles**

## 📞 Emergency Procedures

### If You Encounter Conflicts:
```python
def handle_conflicts(conflict_type: str):
    """Procedures for handling common conflicts."""

    if conflict_type == "documentation_conflict":
        # Check FRAMEWORK_STRUCTURE.md as source of truth
        return resolve_with_structure_doc()

    if conflict_type == "naming_convention_conflict":
        # Check GUIDELINES.md for naming rules
        return resolve_with_guidelines()

    if conflict_type == "template_conflict":
        # Use only core/templates/ as source
        return resolve_with_core_templates()

    if conflict_type == "structural_conflict":
        # Consult PROJECT_CONTEXT.md for principles
        return resolve_with_project_context()
```

## 🛠️ Framework Tools for AI Agents

### AI Assistant Integration Tool
Location: `core/tools/ai-assistant/`

#### Purpose
Provides seamless integration between AI Lab projects and AI coding assistants.

#### Key Features for AI Agents
- **Context Generation**: Automatically creates project-specific context
- **Framework Integration**: Provides AI Lab guidelines and structure
- **Multi-Assistant Support**: Works with opencode and gemini-cli
- **Project Validation**: Ensures valid AI Lab project structure

#### AI Agent Usage
```bash
# Check available AI tools
make check-ai-tools

# Open project with AI assistant (recommended for AI agents)
make ai-assistant

# Direct project opening
make open-with-opencode projects/target-project
make open-with-gemini projects/target-project
```

#### Benefits for AI Agents
1. **Rich Context**: Automatic project context generation
2. **Framework Compliance**: Built-in AI Lab guidelines
3. **Structure Awareness**: Understands project layout
4. **Logging Integration**: Tracks AI-assisted changes

### Project Creator Tool
Location: `core/tools/project-creator/`

#### Purpose
Creates new AI Lab compliant projects with full structure.

### Framework Setup Tool
Location: `core/tools/framework-setup/`

#### Purpose
Sets up the entire AI Lab Framework environment.

## 🔄 Continuous Improvement

### Learning Loop
```python
def ai_agent_learning_loop():
    """Continuous improvement for AI agents."""

    # 1. Analyze previous actions
    previous_actions = review_session_logs()

    # 2. Identify patterns
    patterns = identify_success_patterns(previous_actions)

    # 3. Update decision framework
    update_decision_framework(patterns)

    # 4. Share learnings
    document_ai_learnings(patterns)

    return improved_capabilities
```

## 📚 Quick Reference

### Essential Commands
```bash
# Project creation
./core/tools/project-creator/bin/project-creator

# Framework setup
cd core/tools/framework-setup && make setup

# Testing
make test

# Documentation updates
# Always update core/docs/ first
```

### Critical File Paths
```
core/docs/FRAMEWORK_STRUCTURE.md    # Structure authority
core/docs/PROJECT_CONTEXT.md        # Context authority
core/guidelines/GUIDELINES.md        # Standards authority
core/guidelines/VISION.md            # Strategy authority
core/templates/                      # Template source
ai-logs/change_log/CHANGELOG.md     # Change logging
```

---

**REMEMBER**: You are an AI agent working within a structured framework. Your effectiveness depends on following these guidelines precisely. Always prioritize context analysis, proper logging, and framework alignment.

For human-oriented documentation, see [DEVELOPER_GUIDE.md](./DEVELOPER_GUIDE.md).
For the authoritative framework structure, see [core/docs/FRAMEWORK_STRUCTURE.md](./core/docs/FRAMEWORK_STRUCTURE.md).
