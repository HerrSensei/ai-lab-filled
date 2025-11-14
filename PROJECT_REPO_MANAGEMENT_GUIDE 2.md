# Project Repository Management - Complete Guide

## Overview

The AI Lab Framework now provides **automatic project-to-repository creation** where your local database serves as the single source of truth. Each project in your local project management system automatically creates a corresponding GitHub repository with proper configuration, labels, and work item synchronization.

## 🎯 Key Features

✅ **Automatic Repository Creation**: Projects create GitHub repositories with proper configuration  
✅ **Intelligent Repository Naming**: Converts project names to GitHub-compatible repository names  
✅ **Custom Label Sets**: Creates project-specific labels for better organization  
✅ **Work Item Synchronization**: Automatically creates GitHub Issues for project work items  
✅ **Repository Initialization**: Sets up README, .gitignore, and directory structure  
✅ **Template-Based Setup**: Creates project structure based on technologies used  
✅ **Bidirectional Sync**: Maintains synchronization between local and GitHub  

## 🏗️ Architecture

```
Local Database (Single Source of Truth)
├── Projects
│   ├── Create Repository
│   ├── Initialize Structure  
│   └── Sync Work Items
├── Work Items
│   └── Create GitHub Issues
└── Ideas
    └── Create GitHub Issues (when converted to projects)

GitHub Repositories (Mirror of Local)
├── Repository per Project
│   ├── Issues (Work Items)
│   ├── Labels (Status, Priority, Type)
│   └── Project Structure
└── Automatic Updates
    ├── Status Changes
    ├── Priority Changes
    └── New Work Items
```

## 🚀 Quick Start

### 1. Environment Setup
```bash
export GITHUB_TOKEN="your_github_token_with_repo_scope"
export GITHUB_ORG="your_github_org"  # Optional - uses user account if not set
```

### 2. Create a Project
```python
from infrastructure.db.database import SessionLocal
from infrastructure.db.models.models import Project
from datetime import datetime

session = SessionLocal()

project = Project(
    id="PROJ-001",
    name="My Awesome Project",
    description="A project that will automatically create a GitHub repository",
    status="active",
    priority="high",
    category="development",
    visibility="private",
    owner="Your Name",
    team=["Developer 1", "Developer 2"],
    technologies=["Python", "React", "Docker"],
    # ... other fields
)

session.add(project)
session.commit()
```

### 3. Create Repository from Project
```python
from infrastructure.db.project_repo_manager import create_repository_from_project

# Create repository for specific project
success = create_repository_from_project("PROJ-001")
```

### 4. Sync All Projects
```python
from infrastructure.db.project_repo_manager import sync_all_projects

results = sync_all_projects()
print(f"Created: {results['created']}, Updated: {results['updated']}")
```

## 🛠️ Command Line Interface

### Project Repository Management CLI

```bash
# Check sync status
python project_repo_cli.py status

# List all projects
python project_repo_cli.py list

# Create repository for specific project
python project_repo_cli.py create PROJ-001

# Sync all projects to repositories
python project_repo_cli.py sync-all
```

### GitHub Sync CLI

```bash
# Sync work item changes
python github_sync_cli.py sync-work-item WORK-001 --status done

# Sync idea changes  
python github_sync_cli.py sync-idea IDEA-001 --priority high

# Full bidirectional sync
python github_sync_cli.py full-sync
```

## 📁 Repository Structure

### Automatic Directory Creation

Based on project technologies, the system creates appropriate directory structures:

#### Python Projects
```
project-repo/
├── src/
│   ├── main/
│   └── tests/
├── requirements/
├── docs/
├── tests/
├── scripts/
├── config/
├── README.md
├── .gitignore
└── project.json
```

#### Node.js/JavaScript Projects
```
project-repo/
├── src/
│   ├── components/
│   └── utils/
├── public/
├── docs/
├── tests/
├── scripts/
├── config/
├── README.md
├── .gitignore
└── project.json
```

#### Java Projects
```
project-repo/
├── src/
│   ├── main/
│   │   └── java/
│   └── test/
│       └── java/
├── src/main/resources/
├── docs/
├── tests/
├── scripts/
├── config/
├── README.md
├── .gitignore
└── project.json
```

## 🏷️ Label System

### Standard Labels
- `bug` - Something isn't working
- `documentation` - Documentation improvements
- `enhancement` - New feature or request
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention needed

### Project-Specific Labels
- `project:{PROJECT_ID}` - Links issue to project
- `priority:{low|medium|high|critical}` - Priority level
- `category:{development|infrastructure|automation|research|optimization}` - Project category
- `type:{feature|bug|task|research|documentation|infrastructure}` - Work item type

### Status Labels
- `status:{todo|in_progress|review|done|blocked}` - Work item status
- `status:{backlog|refining|ready|implemented|archived}` - Idea status

## 📊 Project Configuration

### Repository Configuration
```json
{
  "name": "project-name",
  "description": "Project description",
  "private": true,
  "has_issues": true,
  "has_projects": true,
  "has_wiki": true,
  "allow_squash_merge": true,
  "allow_merge_commit": true,
  "allow_rebase_merge": true
}
```

### Project Metadata
```json
{
  "project": {
    "id": "PROJ-001",
    "name": "Project Name",
    "status": "active",
    "priority": "high",
    "category": "development",
    "visibility": "private",
    "owner": "Owner Name",
    "team": ["Team Member 1", "Team Member 2"],
    "technologies": ["Python", "React", "Docker"],
    "objectives": ["Objective 1", "Objective 2"],
    "deliverables": ["Deliverable 1", "Deliverable 2"],
    "acceptance_criteria": ["Criteria 1", "Criteria 2"],
    "risks": ["Risk 1", "Risk 2"],
    "progress_percentage": 25,
    "health_status": "healthy"
  },
  "repository": {
    "created_at": "2025-11-13T23:00:00",
    "created_by": "AI Lab Framework",
    "auto_sync_enabled": true
  }
}
```

## 🔄 Synchronization Workflow

### 1. Project Creation
1. Create project in local database
2. Run `project_repo_cli.py create PROJECT_ID`
3. System creates GitHub repository
4. Repository is initialized with structure
5. Work items are synced as GitHub Issues

### 2. Work Item Updates
1. Update work item in local database
2. System automatically syncs to GitHub Issue
3. Status and priority labels are updated
4. Sync timestamp is recorded

### 3. Bidirectional Sync
1. Changes in GitHub sync back to local database
2. Status label changes update local status
3. New issues can be created in GitHub
4. Manual sync brings changes to local database

## 🎯 Best Practices

### Project Management
1. **Single Source of Truth**: Always make changes in local database first
2. **Consistent Naming**: Use clear, descriptive project names
3. **Technology Tags**: Accurately list technologies for proper structure
4. **Team Management**: Keep team information up to date
5. **Progress Tracking**: Regularly update progress percentages

### Repository Management
1. **Private by Default**: Use private repositories for sensitive projects
2. **Descriptive Names**: Repository names should reflect project purpose
3. **Label Consistency**: Use standard label naming conventions
4. **Issue Templates**: Use consistent issue formats
5. **Documentation**: Keep README files current

### Synchronization
1. **Regular Syncs**: Run sync operations regularly
2. **Error Monitoring**: Watch for sync failures
3. **Rate Limiting**: Be aware of GitHub API limits
4. **Conflict Resolution**: Handle sync conflicts gracefully
5. **Backup Strategy**: Maintain local database backups

## 🔧 Advanced Configuration

### Custom Repository Templates
Create custom repository templates by modifying the `_initialize_repository` method:

```python
def _initialize_repository(self, repo: Repository, project: Project):
    # Custom initialization logic
    if "custom-template" in project.tags:
        # Create custom structure
        pass
```

### Custom Label Sets
Define project-specific label sets:

```python
def _get_project_labels(self, project: Project):
    if "security" in project.tags:
        return security_labels
    elif "ml" in project.tags:
        return ml_labels
    else:
        return standard_labels
```

### Integration with CI/CD
Add CI/CD pipeline files based on technologies:

```python
def _create_ci_cd_files(self, repo: Repository, project: Project):
    if "GitHub Actions" in project.tags:
        # Create .github/workflows/
        pass
    elif "GitLab CI" in project.tags:
        # Create .gitlab-ci.yml
        pass
```

## 🚨 Troubleshooting

### Common Issues

#### Repository Creation Fails
- **Check Token Permissions**: Ensure token has `repo` scope
- **Check Organization Access**: Verify org membership if using GITHUB_ORG
- **Check Rate Limits**: GitHub has API rate limits
- **Check Repository Limits**: Verify account hasn't reached repository limit

#### Work Item Sync Fails
- **Check GitHub Issue ID**: Ensure work items have github_issue_id set
- **Check Repository URL**: Verify github_repo_url is correct
- **Check Network**: Ensure internet connectivity
- **Check Permissions**: Verify write access to repository

#### Label Creation Fails
- **Check Label Limits**: GitHub has label count limits
- **Check Label Names**: Ensure valid label format
- **Check Color Codes**: Use valid hex color codes

### Debug Mode
Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Manual Recovery
If automatic sync fails, use manual commands:

```bash
# Manual repository creation
python project_repo_cli.py create PROJ-001

# Manual work item sync
python github_sync_cli.py sync-work-item WORK-001 --status done

# Full manual sync
python github_sync_cli.py full-sync
```

## 📈 Monitoring and Analytics

### Sync Status Dashboard
```python
from infrastructure.db.project_repo_manager import get_project_sync_status

status = get_project_sync_status()
print(f"Projects with repos: {status['with_repositories']}")
print(f"Projects needing repos: {status['without_repositories']}")
```

### Repository Statistics
```python
# Get repository statistics
repo = manager.github.get_repo("repository-name")
print(f"Issues: {repo.open_issues_count}")
print(f"Stars: {repo.stargazers_count}")
print(f"Forks: {repo.forks_count}")
```

## 🎉 Success Stories

### Example Use Cases

1. **Development Team**: Manages 15 projects with automatic repository creation
2. **Research Organization**: Tracks 50+ research projects with GitHub integration
3. **Startup**: Uses system for rapid project prototyping and deployment
4. **Open Source**: Manages community projects with contributor synchronization
5. **Enterprise**: Integrates with existing project management tools

---

## 📚 Additional Resources

- [GitHub API Documentation](https://docs.github.com/en/rest)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [AI Lab Framework Documentation](README.md)
- [GitHub Auto-Sync Guide](GITHUB_AUTO_SYNC_GUIDE.md)

---

*This system establishes your local database as the single source of truth while maintaining perfect synchronization with GitHub repositories.*