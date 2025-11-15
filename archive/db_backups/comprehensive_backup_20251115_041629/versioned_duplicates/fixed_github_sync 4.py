#!/usr/bin/env python3
"""
Fixed GitHub sync using our actual SQLite database
"""

import os
import time
from typing import Any

from github import Github
from github.Issue import Issue

from ai_lab_framework.database import AILabDatabase


class FixedGitHubIntegration:
    """Fixed GitHub Issues integration using our SQLite database"""

    def __init__(self, github_token: str, repo_name: str):
        self.github = Github(github_token)
        self.repo = self.github.get_repo(repo_name)
        self.db = AILabDatabase()

        # Configuration
        self.work_item_labels = ["ai-lab", "work-item", "framework"]
        self.idea_labels = ["ai-lab", "idea", "innovation"]

    def sync_to_github(self, item_type: str = "all") -> dict[str, int]:
        """Sync unsynced items to GitHub"""
        results = {"work_items": 0, "ideas": 0, "errors": 0}

        try:
            if item_type in ["all", "work_items"]:
                # Sync work items
                unsynced_work_items = self.db.get_unsynced_items("work_item")
                print(f"Found {len(unsynced_work_items)} unsynced work items")

                for work_item in unsynced_work_items:
                    print(f"Syncing work item: {work_item['id']}")
                    if self.create_issue_from_work_item(work_item):
                        results["work_items"] += 1
                    else:
                        results["errors"] += 1
                    time.sleep(1)  # Rate limiting

            if item_type in ["all", "ideas"]:
                # Sync ideas
                unsynced_ideas = self.db.get_unsynced_items("idea")
                print(f"Found {len(unsynced_ideas)} unsynced ideas")

                for idea in unsynced_ideas:
                    print(f"Syncing idea: {idea['id']}")
                    if self.create_issue_from_idea(idea):
                        results["ideas"] += 1
                    else:
                        results["errors"] += 1
                    time.sleep(1)  # Rate limiting

        except Exception as e:
            print(f"❌ Sync to GitHub failed: {e}")
            results["errors"] += 1

        return results

    def create_issue_from_work_item(self, work_item: dict[str, Any]) -> Issue | None:
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

            # Update database with GitHub issue ID
            self.db.update_github_sync(
                local_id=work_item["id"],
                local_type="work_item",
                github_issue_id=issue.number,
                github_url=issue.html_url,
            )

            print(
                f"✅ Created GitHub Issue #{issue.number} for work item {work_item['id']}"
            )
            return issue

        except Exception as e:
            print(f"❌ Error creating issue for work item {work_item['id']}: {e}")
            return None

    def create_issue_from_idea(self, idea: dict[str, Any]) -> Issue | None:
        """Create GitHub Issue from idea"""
        try:
            title = f"💡 [{idea['id']}] {idea['title']}"

            # Build issue body
            body = self._build_idea_body(idea)

            # Determine labels
            labels = self.idea_labels.copy()
            labels.append(f"priority:{idea.get('priority', 'medium')}")
            labels.append(f"status:{idea.get('status', 'proposed')}")
            labels.append(f"category:{idea.get('category', 'general')}")

            # Create issue
            issue = self.repo.create_issue(title=title, body=body, labels=labels)

            # Update database with GitHub issue ID
            self.db.update_github_sync(
                local_id=idea["id"],
                local_type="idea",
                github_issue_id=issue.number,
                github_url=issue.html_url,
            )

            print(f"✅ Created GitHub Issue #{issue.number} for idea {idea['id']}")
            return issue

        except Exception as e:
            print(f"❌ Error creating issue for idea {idea['id']}: {e}")
            return None

    def _build_work_item_body(self, work_item: dict[str, Any]) -> str:
        """Build GitHub Issue body from work item"""
        body = f"""## 📋 Work Item Details

**ID:** {work_item["id"]}
**Status:** {work_item.get("status", "proposed")}
**Priority:** {work_item.get("priority", "medium")}
**Type:** {work_item.get("type", "task")}
**Component:** {work_item.get("component", "N/A")}

**Estimated Hours:** {work_item.get("estimated_hours", 0)}
**Actual Hours:** {work_item.get("actual_hours", 0)}

## 📝 Description

{work_item.get("description", "No description provided")}

---

*This issue was automatically created from the AI Lab Framework database.*
"""
        return body

    def _build_idea_body(self, idea: dict[str, Any]) -> str:
        """Build GitHub Issue body from idea"""
        body = f"""## 💡 Idea Details

**ID:** {idea["id"]}
**Status:** {idea.get("status", "proposed")}
**Priority:** {idea.get("priority", "medium")}
**Category:** {idea.get("category", "general")}

## 📝 Description

{idea.get("description", "No description provided")}

---

*This issue was automatically created from the AI Lab Framework database.*
"""
        return body


def main():
    """Fixed GitHub sync using our database"""
    token = os.getenv("GITHUB_TOKEN")
    repo_name = os.getenv("GITHUB_REPO")

    if not token or not repo_name:
        print("❌ GITHUB_TOKEN and GITHUB_REPO environment variables required")
        return

    integration = FixedGitHubIntegration(token, repo_name)
    results = integration.sync_to_github()
    print(f"📊 Sync results: {results}")


if __name__ == "__main__":
    main()
