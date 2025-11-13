#!/usr/bin/env python3
"""
AI Lab Framework - Project Repository Manager
Manages creation and synchronization of local projects with GitHub repositories
"""

import os
import json
import time
from typing import Dict, List, Optional, Any
from datetime import datetime
from github import Github, GithubException
from github.Repository import Repository

from infrastructure.db.database import SessionLocal
from infrastructure.db.models.models import Project, WorkItem, Idea


class ProjectRepositoryManager:
    """Manages project-to-repository creation and synchronization"""

    def __init__(self, github_token: str, github_org: Optional[str] = None):
        self.github = Github(github_token)
        self.github_org = github_org  # If None, creates under user account
        self.session = SessionLocal()

    def create_repository_from_project(self, project_id: str) -> Optional[Repository]:
        """Create GitHub repository from local project"""
        try:
            # Get project from database
            project = (
                self.session.query(Project).filter(Project.id == project_id).first()
            )
            if not project:
                print(f"❌ Project {project_id} not found")
                return None

            print(f"🚀 Creating GitHub repository for project: {project.name}")

            # Prepare repository configuration
            repo_config = self._prepare_repository_config(project)

            # Create repository
            if self.github_org:
                repo = self.github.get_organization(self.github_org).create_repo(
                    **repo_config
                )
            else:
                repo = self.github.get_user().create_repo(**repo_config)

            print(f"✅ Repository created: {repo.html_url}")

            # Create project-specific labels
            self._create_repository_labels(repo, project)

            # Update project with repository info
            project.repository_url = repo.html_url
            project.github_repo_id = repo.id  # Add this field to model
            self.session.commit()

            # Initialize repository structure
            self._initialize_repository(repo, project)

            # Sync project work items to repository issues
            self._sync_work_items_to_repository(project, repo)

            print(
                f"🎉 Project {project_id} successfully synchronized to GitHub repository"
            )
            return repo

        except GithubException as e:
            print(f"❌ Failed to create repository for project {project_id}: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error creating repository for {project_id}: {e}")
            return None

    def _prepare_repository_config(self, project: Project) -> Dict[str, Any]:
        """Prepare GitHub repository configuration from project"""
        # Generate repository name from project name
        repo_name = self._generate_repo_name(project.name)

        config = {
            "name": repo_name,
            "description": project.description,
            "private": project.visibility == "private",
            "has_issues": True,
            "has_projects": True,
            "has_wiki": True,
            "auto_init": False,  # We'll initialize manually
            "allow_squash_merge": True,
            "allow_merge_commit": True,
            "allow_rebase_merge": True,
        }

        return config

    def _generate_repo_name(self, project_name: str) -> str:
        """Generate GitHub-compatible repository name"""
        # Convert to lowercase, replace spaces with hyphens, remove special chars
        import re

        repo_name = re.sub(r"[^a-zA-Z0-9\s-]", "", project_name)
        repo_name = re.sub(r"\s+", "-", repo_name.strip().lower())

        # Ensure it's not too long (GitHub max 100 chars)
        return repo_name[:80] if len(repo_name) > 80 else repo_name

    def _get_project_labels(self, project: Project) -> List[Dict[str, str]]:
        """Get project-specific labels for repository"""
        base_labels = [
            {
                "name": "bug",
                "color": "d73a4a",
                "description": "Something isn't working",
            },
            {
                "name": "documentation",
                "color": "0075ca",
                "description": "Improvements or additions to documentation",
            },
            {
                "name": "duplicate",
                "color": "cfd3d7",
                "description": "This issue or pull request already exists",
            },
            {
                "name": "enhancement",
                "color": "a2eeef",
                "description": "New feature or request",
            },
            {
                "name": "good first issue",
                "color": "7057ff",
                "description": "Good for newcomers",
            },
            {
                "name": "help wanted",
                "color": "008672",
                "description": "Extra attention is needed",
            },
            {
                "name": "invalid",
                "color": "e4e669",
                "description": "This doesn't seem right",
            },
            {
                "name": "question",
                "color": "d876e3",
                "description": "Further information is requested",
            },
            {
                "name": "wontfix",
                "color": "ffffff",
                "description": "This will not be worked on",
            },
        ]

        # Add project-specific labels
        project_labels = [
            {
                "name": f"project:{project.id}",
                "color": "0366d6",
                "description": f"Related to {project.name}",
            },
            {
                "name": f"priority:{project.priority}",
                "color": self._get_priority_color(project.priority),
                "description": f"Priority: {project.priority}",
            },
            {
                "name": f"category:{project.category}",
                "color": "f1e05a",
                "description": f"Category: {project.category}",
            },
        ]

        return base_labels + project_labels

    def _create_repository_labels(self, repo: Repository, project: Project):
        """Create project-specific labels in repository"""
        try:
            print("🏷️ Creating repository labels...")

            labels = self._get_project_labels(project)
            existing_labels = {label.name for label in repo.get_labels()}

            for label_data in labels:
                if label_data["name"] not in existing_labels:
                    repo.create_label(**label_data)
                    print(f"  ✅ Created label: {label_data['name']}")

            print("✅ Repository labels created")

        except Exception as e:
            print(f"⚠️  Failed to create repository labels: {e}")

    def _get_priority_color(self, priority: str) -> str:
        """Get color for priority label"""
        colors = {
            "low": "98fb98",
            "medium": "ffa500",
            "high": "d73a4a",
            "critical": "b60205",
        }
        return colors.get(priority, "ffa500")

    def _initialize_repository(self, repo: Repository, project: Project):
        """Initialize repository with project structure"""
        try:
            print("📁 Initializing repository structure...")

            # Create README
            readme_content = self._generate_readme(project)
            repo.create_file(
                "README.md", "Initial README", readme_content, branch="main"
            )

            # Create .gitignore
            gitignore_content = self._generate_gitignore(project)
            repo.create_file(
                ".gitignore", "Initial .gitignore", gitignore_content, branch="main"
            )

            # Create project configuration files
            if project.technologies:
                config_content = self._generate_project_config(project)
                repo.create_file(
                    "project.json",
                    "Project configuration",
                    json.dumps(config_content, indent=2),
                    branch="main",
                )

            # Create initial project structure
            self._create_directory_structure(repo, project)

            print("✅ Repository structure initialized")

        except Exception as e:
            print(f"⚠️  Failed to initialize repository structure: {e}")

    def _generate_readme(self, project: Project) -> str:
        """Generate README content for project"""
        readme = f"""# {project.name}

{project.description}

## 📋 Project Details

- **Status**: {project.status}
- **Priority**: {project.priority}
- **Category**: {project.category}
- **Owner**: {project.owner}
- **Visibility**: {project.visibility}

## 🎯 Objectives

"""

        for i, objective in enumerate(project.objectives or [], 1):
            readme += f"{i}. {objective}\n"

        readme += f"""
## 📦 Deliverables

"""

        for i, deliverable in enumerate(project.deliverables or [], 1):
            readme += f"- [ ] {deliverable}\n"

        readme += f"""
## 🛠️ Technologies

"""

        for tech in project.technologies or []:
            readme += f"- {tech}\n"

        readme += f"""
## 👥 Team

"""

        for member in project.team or []:
            readme += f"- {member}\n"

        readme += f"""
## 📊 Progress

**Progress**: {project.progress_percentage}%
**Health Status**: {project.health_status}

---

*This repository was automatically created from AI Lab Framework local project management.*
*Last updated: {datetime.now().isoformat()}*
"""

        return readme

    def _generate_gitignore(self, project: Project) -> str:
        """Generate .gitignore content based on project technologies"""
        base_gitignore = """# AI Lab Framework
.venv/
venv/
env/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment variables
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
"""

        # Add technology-specific ignores
        tech_ignores = {
            "node": [
                "node_modules/",
                "npm-debug.log*",
                "yarn-debug.log*",
                "yarn-error.log*",
            ],
            "python": ["*.py[cod]", "$py.class/", ".coverage", "htmlcov/"],
            "java": ["*.class", "*.jar", "*.war", "*.ear", "target/"],
            "docker": [".dockerignore"],
        }

        for tech in project.technologies or []:
            tech_lower = tech.lower()
            for key, ignores in tech_ignores.items():
                if key in tech_lower:
                    base_gitignore += "\n# " + tech + "\n"
                    base_gitignore += "\n".join(ignores) + "\n"

        return base_gitignore

    def _generate_project_config(self, project: Project) -> Dict[str, Any]:
        """Generate project configuration JSON"""
        return {
            "project": {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "status": project.status,
                "priority": project.priority,
                "category": project.category,
                "visibility": project.visibility,
                "owner": project.owner,
                "team": project.team,
                "technologies": project.technologies,
                "objectives": project.objectives,
                "deliverables": project.deliverables,
                "acceptance_criteria": project.acceptance_criteria,
                "risks": project.risks,
                "created_date": project.created_date.isoformat()
                if project.created_date
                else None,
                "updated_date": project.updated_date.isoformat()
                if project.updated_date
                else None,
                "start_date": project.start_date.isoformat()
                if project.start_date
                else None,
                "target_date": project.target_date.isoformat()
                if project.target_date
                else None,
            },
            "repository": {
                "created_at": datetime.now().isoformat(),
                "created_by": "AI Lab Framework",
                "auto_sync_enabled": True,
            },
        }

    def _create_directory_structure(self, repo: Repository, project: Project):
        """Create basic directory structure"""
        directories = ["docs", "src", "tests", "scripts", "config"]

        # Add technology-specific directories
        if project.technologies:
            for tech in project.technologies:
                tech_lower = tech.lower()
                if "python" in tech_lower:
                    directories.extend(["src/main", "src/tests", "requirements"])
                elif "node" in tech_lower or "javascript" in tech_lower:
                    directories.extend(["src/components", "src/utils", "public"])
                elif "java" in tech_lower:
                    directories.extend(
                        ["src/main/java", "src/test/java", "src/main/resources"]
                    )
                elif "docker" in tech_lower:
                    directories.append("docker")

        # Create directories with placeholder files
        for directory in directories:
            try:
                repo.create_file(
                    f"{directory}/.gitkeep",
                    f"Create {directory} directory",
                    "",
                    branch="main",
                )
            except:
                pass  # Directory might already exist

    def _sync_work_items_to_repository(self, project: Project, repo: Repository):
        """Sync project work items to repository issues"""
        try:
            print("📋 Syncing work items to repository issues...")

            work_items = (
                self.session.query(WorkItem)
                .filter(WorkItem.project_id == project.id)
                .all()
            )

            for work_item in work_items:
                # Create issue for work item
                issue_title = f"[{work_item.id}] {work_item.title}"
                issue_body = self._generate_work_item_issue_body(work_item)

                labels = [
                    f"project:{project.id}",
                    f"priority:{work_item.priority}",
                    f"type:{work_item.type}",
                    f"status:{work_item.status}",
                ]

                # Add component label if available
                if hasattr(work_item, "component") and work_item.component:
                    labels.append(f"component:{work_item.component}")

                issue = repo.create_issue(
                    title=issue_title, body=issue_body, labels=labels
                )

                # Update work item with GitHub issue info
                work_item.github_issue_id = issue.number
                work_item.github_repo_url = repo.html_url
                work_item.github_synced_at = datetime.now()

                print(f"  ✅ Created issue #{issue.number} for {work_item.id}")
                time.sleep(1)  # Rate limiting

            self.session.commit()
            print(f"✅ Synced {len(work_items)} work items to repository")

        except Exception as e:
            print(f"⚠️  Failed to sync work items: {e}")

    def _generate_work_item_issue_body(self, work_item: WorkItem) -> str:
        """Generate issue body for work item"""
        body = f"""## 📋 Work Item Details

**ID**: {work_item.id}
**Type**: {work_item.type}
**Status**: {work_item.status}
**Priority**: {work_item.priority}
**Assignee**: {work_item.assignee or "Unassigned"}

---

## 📝 Description

{work_item.description}

---

## 📊 Time Tracking

**Estimated Hours**: {work_item.estimated_hours or 0}
**Actual Hours**: {work_item.actual_hours or 0}

---

## ✅ Acceptance Criteria

"""

        for i, criteria in enumerate(work_item.acceptance_criteria or [], 1):
            body += f"{i}. {criteria}\n"

        body += f"""
---

## 🏷️ Labels

"""

        for label in work_item.labels or []:
            body += f"- {label}\n"

        body += f"""
---

## 📝 Notes

{work_item.notes or "No notes"}

---

*This issue was automatically created from AI Lab Framework work item.*
*Last updated: {datetime.now().isoformat()}*
"""

        return body

    def sync_all_projects_to_repositories(self) -> Dict[str, int]:
        """Sync all local projects to GitHub repositories"""
        results = {"created": 0, "updated": 0, "errors": 0}

        projects = self.session.query(Project).all()
        print(f"📦 Found {len(projects)} projects to process")

        for project in projects:
            try:
                if not project.repository_url:
                    # Create new repository
                    repo = self.create_repository_from_project(project.id)
                    if repo:
                        results["created"] += 1
                    else:
                        results["errors"] += 1
                else:
                    # Update existing repository
                    print(
                        f"📝 Project {project.name} already has repository: {project.repository_url}"
                    )
                    results["updated"] += 1

            except Exception as e:
                print(f"❌ Error processing project {project.id}: {e}")
                results["errors"] += 1

        return results

    def get_project_status(self) -> Dict[str, Any]:
        """Get status of all projects and their repository sync"""
        projects = self.session.query(Project).all()

        status = {
            "total_projects": len(projects),
            "with_repositories": 0,
            "without_repositories": 0,
            "projects": [],
        }

        for project in projects:
            project_info = {
                "id": project.id,
                "name": project.name,
                "status": project.status,
                "has_repository": bool(project.repository_url),
                "repository_url": project.repository_url,
                "work_items_count": len(project.work_items)
                if project.work_items
                else 0,
            }

            status["projects"].append(project_info)

            if project.repository_url:
                status["with_repositories"] += 1
            else:
                status["without_repositories"] += 1

        return status


# Global instance
repo_manager = None


def get_repo_manager() -> ProjectRepositoryManager:
    """Get global repository manager instance"""
    global repo_manager

    if not repo_manager:
        github_token = os.getenv("GITHUB_TOKEN")
        github_org = os.getenv("GITHUB_ORG")  # Optional

        if not github_token:
            raise ValueError("GITHUB_TOKEN environment variable required")

        repo_manager = ProjectRepositoryManager(github_token, github_org)

    return repo_manager


def create_repository_from_project(project_id: str) -> bool:
    """Convenience function to create repository from project"""
    manager = get_repo_manager()
    repo = manager.create_repository_from_project(project_id)
    return repo is not None


def sync_all_projects() -> Dict[str, int]:
    """Convenience function to sync all projects"""
    manager = get_repo_manager()
    return manager.sync_all_projects_to_repositories()


def get_project_sync_status() -> Dict[str, Any]:
    """Convenience function to get project sync status"""
    manager = get_repo_manager()
    return manager.get_project_status()
