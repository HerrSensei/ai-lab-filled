# AI-LAB Guidelines Integration

This directory contains AI-LAB guidelines and rules that are automatically integrated into generated projects.

## Structure

```
guidelines/
├── core/                   # Core AI-LAB guidelines
│   ├── coding-standards.md
│   ├── project-structure.md
│   ├── documentation.md
│   └── security.md
├── templates/              # Template-specific guidelines
│   ├── web-app.md
│   ├── api-service.md
│   ├── agent-skill.md
│   ├── data-pipeline.md
│   └── microservice.md
├── checklists/             # Development checklists
│   ├── pre-commit.md
│   ├── pre-release.md
│   └── security-review.md
└── automation/             # Automated enforcement
    ├── pre-commit-hooks.sh
    ├── github-actions.yml
    └── validation-scripts.py
```

## Integration Points

### 1. Project Generation
- Guidelines are automatically included in generated projects
- Template-specific rules are applied based on project type
- AI-LAB standards are enforced by default

### 2. Development Workflow
- Pre-commit hooks ensure compliance
- Automated checks in CI/CD pipeline
- Documentation templates for consistency

### 3. Quality Assurance
- Automated code quality checks
- Security scanning integration
- Performance monitoring setup

## Usage

Guidelines are automatically integrated when using the project generator. For existing projects, run:

```bash
# Apply AI-LAB guidelines to existing project
./apply-guidelines.sh [project-path]
```

## Customization

Guidelines can be customized per project while maintaining AI-LAB core standards:

```yaml
# .ai-lab/guidelines-config.yml
guidelines:
  core_version: "1.0"
  custom_rules:
    - "team-specific-rule-1"
    - "project-specific-rule-2"
  overrides:
    max_line_length: 100  # Override default 88
```
