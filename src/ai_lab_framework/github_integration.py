#!/usr/bin/env python3
"""
AI Lab Framework - GitHub Integration
Bidirectional synchronization between SQLite database and GitHub Issues
"""

import os
import json
import sqlite3
import time
from datetime import datetime
from typing import List, Dict, Any, Optional
from github import Github, GithubException
from github.Issue import Issue
from github.Repository import Repository

from .database import AILabDatabase


class GitHubIntegration:
    """GitHub Issues integration for AI Lab Framework"""

    def __init__(
        self, github_token: str, repo_name: str, db: Optional[AILabDatabase] = None
    ):
        self.github = Github(github_token)
        self.repo = self.github.get_repo(repo_name)
        self.db = db or AILabDatabase()

        # Configuration
        self.work_item_labels = ["ai-lab", "work-item", "framework"]
        self.idea_labels = ["ai-lab", "idea", "innovation"]
        self.session_labels = ["ai-lab", "session", "log"]

    def create_issue_from_work_item(self, work_item: Dict[str, Any]) -> Optional[Issue]:
        """Create GitHub Issue from work item"""
        try:
            title = f"[{work_item['id']}] {work_item['title']}"

            # Build issue body
            body = self._build_work_item_body(work_item)

            # Determine labels
            labels = self.work_item_labels.copy()
            labels.append(f"priority:{work_item.get('priority', 'medium')}")
            labels.append(f"status:{work_item.get('status', 'proposed')}")

            if work_item.get("component"):
                labels.append(f"component:{work_item['component']}")

            # Create issue
            issue = self.repo.create_issue(title=title, body=body, labels=labels)

            # Update database with GitHub info
            self.db.update_github_sync(
                work_item["id"], "work_item", issue.number, issue.html_url
            )

            print(
                f"✅ Created GitHub Issue #{issue.number} for work item {work_item['id']}"
            )
            return issue

        except GithubException as e:
            print(f"❌ Error creating GitHub Issue for {work_item['id']}: {e}")
            return None

    def create_issue_from_idea(self, idea: Dict[str, Any]) -> Optional[Issue]:
        """Create GitHub Issue from idea"""
        try:
            title = f"[{idea['id']}] 💡 {idea['title']}"

            # Build issue body
            body = self._build_idea_body(idea)

            # Determine labels
            labels = self.idea_labels.copy()
            labels.append(f"priority:{idea.get('priority', 'medium')}")
            labels.append(f"status:{idea.get('status', 'proposed')}")

            if idea.get("category"):
                labels.append(f"category:{idea['category']}")

            # Create issue
            issue = self.repo.create_issue(title=title, body=body, labels=labels)

            # Update database with GitHub info
            self.db.update_github_sync(idea["id"], "idea", issue.number, issue.html_url)

            print(f"✅ Created GitHub Issue #{issue.number} for idea {idea['id']}")
            return issue

        except GithubException as e:
            print(f"❌ Error creating GitHub Issue for {idea['id']}: {e}")
            return None

    def sync_to_github(self, item_type: str = "all") -> Dict[str, int]:
        """Sync unsynced items to GitHub"""
        results = {"work_items": 0, "ideas": 0, "errors": 0}

        try:
            if item_type in ["all", "work_items"]:
                # Sync work items
                unsynced_work_items = self.db.get_unsynced_items("work_item")
                for work_item in unsynced_work_items:
                    if self.create_issue_from_work_item(work_item):
                        results["work_items"] += 1
                    else:
                        results["errors"] += 1
                    time.sleep(1)  # Rate limiting

            if item_type in ["all", "ideas"]:
                # Sync ideas
                unsynced_ideas = self.db.get_unsynced_items("idea")
                for idea in unsynced_ideas:
                    if self.create_issue_from_idea(idea):
                        results["ideas"] += 1
                    else:
                        results["errors"] += 1
                    time.sleep(1)  # Rate limiting

        except Exception as e:
            print(f"❌ Sync to GitHub failed: {e}")
            results["errors"] += 1

        return results

    def sync_from_github(self) -> Dict[str, int]:
        """Sync changes from GitHub back to local database"""
        results = {"updated": 0, "errors": 0}

        try:
            # Get all AI Lab issues
            issues = self.repo.get_issues(labels="ai-lab", state="all")

            for issue in issues:
                try:
                    # Extract item ID from title
                    item_id = self._extract_item_id(issue.title)
                    if not item_id:
                        continue

                    # Determine item type from labels
                    item_type = self._determine_item_type(issue.labels)
                    if not item_type:
                        continue

                    # Update local database
                    if self._update_local_from_github(issue, item_id, item_type):
                        results["updated"] += 1

                    time.sleep(0.5)  # Rate limiting

                except Exception as e:
                    print(f"❌ Error processing issue #{issue.number}: {e}")
                    results["errors"] += 1

        except Exception as e:
            print(f"❌ Sync from GitHub failed: {e}")
            results["errors"] += 1

        return results

    def _build_work_item_body(self, work_item: Dict[str, Any]) -> str:
        """Build GitHub Issue body from work item"""
        body = f"""## 📋 Work Item Details

**ID:** {work_item["id"]}
**Status:** {work_item.get("status", "proposed")}
**Priority:** {work_item.get("priority", "medium")}
**Type:** {work_item.get("type", "task")}
**Component:** {work_item.get("component", "N/A")}

**Estimated Hours:** {work_item.get("estimated_hours", 0)}
**Actual Hours:** {work_item.get("actual_hours", 0)}
**Assignee:** {work_item.get("assignee", "Unassigned")}

**Created:** {work_item.get("created_date", "N/A")}
**Updated:** {work_item.get("updated_date", "N/A")}
**Due Date:** {work_item.get("due_date", "N/A")}

---

## 📝 Description

{work_item.get("description", "No description provided")}

---

## 🏷️ Tags

{", ".join(work_item.get("tags", [])) if work_item.get("tags") else "No tags"}

---

## 🔗 Dependencies

{", ".join(work_item.get("dependencies", [])) if work_item.get("dependencies") else "No dependencies"}

---

*This issue is automatically synchronized from the AI Lab Framework SQLite database.*
"""
        return body

    def _build_idea_body(self, idea: Dict[str, Any]) -> str:
        """Build GitHub Issue body from idea"""
        body = f"""## 💡 Idea Details

**ID:** {idea["id"]}
**Status:** {idea.get("status", "proposed")}
**Priority:** {idea.get("priority", "medium")}
**Category:** {idea.get("category", "N/A")}

**Created:** {idea.get("created_date", "N/A")}
**Updated:** {idea.get("updated_date", "N/A")}

---

## 📝 Description

{idea.get("description", "No description provided")}

---

## 🏷️ Tags

{", ".join(idea.get("tags", [])) if idea.get("tags") else "No tags"}

---

## 💬 Implementation Notes

*This idea is automatically synchronized from the AI Lab Framework SQLite database.*

---

## 🎯 Next Steps

- [ ] Evaluate feasibility
- [ ] Define requirements
- [ ] Plan implementation
- [ ] Assign to work item
"""
        return body

    def _extract_item_id(self, title: str) -> Optional[str]:
        """Extract item ID from GitHub Issue title"""
        import re

        match = re.match(r"\[([A-Z0-9-]+)\]", title)
        return match.group(1) if match else None

    def _determine_item_type(self, labels) -> Optional[str]:
        """Determine item type from GitHub labels"""
        label_names = [label.name for label in labels]

        if "work-item" in label_names:
            return "work_item"
        elif "idea" in label_names:
            return "idea"
        elif "session" in label_names:
            return "session"

        return None

    def _update_local_from_github(
        self, issue: Issue, item_id: str, item_type: str
    ) -> bool:
        """Update local database from GitHub Issue"""
        try:
            # Extract status from labels
            status = "proposed"
            for label in issue.labels:
                if label.name.startswith("status:"):
                    status = label.name.replace("status:", "")
                    break

            # Update database
            with sqlite3.connect(self.db.db_path) as conn:
                if item_type == "work_item":
                    conn.execute(
                        """
                        UPDATE work_items 
                        SET status = ?, updated_date = ?
                        WHERE id = ?
                    """,
                        (status, issue.updated_at.isoformat(), item_id),
                    )
                elif item_type == "idea":
                    conn.execute(
                        """
                        UPDATE ideas 
                        SET status = ?, updated_date = ?
                        WHERE id = ?
                    """,
                        (status, issue.updated_at.isoformat(), item_id),
                    )

            return True

        except Exception as e:
            print(f"❌ Error updating local database for {item_id}: {e}")
            return False

    def setup_repository_labels(self) -> bool:
        """Create required labels in GitHub repository"""
        try:
            required_labels = [
                # AI Lab labels
                {
                    "name": "ai-lab",
                    "color": "0366d6",
                    "description": "AI Lab Framework item",
                },
                {
                    "name": "work-item",
                    "color": "7057ff",
                    "description": "Framework work item",
                },
                {"name": "idea", "color": "a2eeef", "description": "Innovation idea"},
                {"name": "session", "color": "0075ca", "description": "AI session log"},
                # Status labels
                {
                    "name": "status:proposed",
                    "color": "f1e05a",
                    "description": "Proposed but not started",
                },
                {
                    "name": "status:in_progress",
                    "color": "fbca04",
                    "description": "Currently being worked on",
                },
                {"name": "status:done", "color": "28a745", "description": "Completed"},
                {
                    "name": "status:archived",
                    "color": "6f42c1",
                    "description": "Archived",
                },
                # Priority labels
                {
                    "name": "priority:high",
                    "color": "d73a4a",
                    "description": "High priority",
                },
                {
                    "name": "priority:medium",
                    "color": "ffa500",
                    "description": "Medium priority",
                },
                {
                    "name": "priority:low",
                    "color": "98fb98",
                    "description": "Low priority",
                },
                # Component labels
                {
                    "name": "component:framework",
                    "color": "bfdadc",
                    "description": "Core framework",
                },
                {
                    "name": "component:tools",
                    "color": "c5def5",
                    "description": "Development tools",
                },
                {
                    "name": "component:data-management",
                    "color": "bfd4f2",
                    "description": "Data management",
                },
                {
                    "name": "component:documentation",
                    "color": "d4c5f9",
                    "description": "Documentation",
                },
            ]

            existing_labels = {label.name for label in self.repo.get_labels()}

            for label_data in required_labels:
                if label_data["name"] not in existing_labels:
                    self.repo.create_label(**label_data)
                    print(f"✅ Created label: {label_data['name']}")

            print("🏷️ Repository labels setup completed!")
            return True

        except GithubException as e:
            print(f"❌ Error setting up repository labels: {e}")
            return False


def main():
    """Test GitHub integration"""
    import argparse

    parser = argparse.ArgumentParser(
        description="GitHub Integration for AI Lab Framework"
    )
    parser.add_argument("--token", help="GitHub personal access token")
    parser.add_argument("--repo", help="GitHub repository (owner/repo)")
    parser.add_argument(
        "--action",
        choices=["setup", "sync-to-github", "sync-from-github", "sync-all"],
        default="sync-all",
        help="Action to perform",
    )

    args = parser.parse_args()

    # Get token from environment or argument
    token = args.token or os.getenv("GITHUB_TOKEN")
    if not token:
        print(
            "❌ GitHub token required. Set GITHUB_TOKEN environment variable or use --token"
        )
        return

    # Get repository name
    repo_name = args.repo or os.getenv(
        "GITHUB_REPO", "ai-lab-framework/ai-lab-framework"
    )

    # Initialize integration
    integration = GitHubIntegration(token, repo_name)

    # Perform action
    if args.action == "setup":
        integration.setup_repository_labels()
    elif args.action == "sync-to-github":
        results = integration.sync_to_github()
        print(f"📊 Sync to GitHub results: {results}")
    elif args.action == "sync-from-github":
        results = integration.sync_from_github()
        print(f"📊 Sync from GitHub results: {results}")
    elif args.action == "sync-all":
        integration.setup_repository_labels()
        results_to = integration.sync_to_github()
        results_from = integration.sync_from_github()
        print(f"📊 Sync results - To GitHub: {results_to}, From GitHub: {results_from}")


if __name__ == "__main__":
    main()
