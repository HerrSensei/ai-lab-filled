#!/usr/bin/env python3
"""
Recreate work items on GitHub with better error handling
"""

import os
import time

from github import Github

from ai_lab_framework.database import AILabDatabase


def main():
    token = os.getenv("GITHUB_TOKEN")
    repo_name = os.getenv("GITHUB_REPO")

    if not token or not repo_name:
        print("❌ GITHUB_TOKEN and GITHUB_REPO environment variables required")
        return

    github = Github(token)
    repo = github.get_repo(repo_name)
    db = AILabDatabase()

    # Get unsynced work items
    work_items = db.get_unsynced_items("work_item")
    print(f"Recreating {len(work_items)} work items on GitHub...")

    success_count = 0
    error_count = 0

    for work_item in work_items:
        try:
            print(f"Creating: {work_item['id']}")

            # Create title
            title = f"[{work_item['id']}] {work_item['title']}"

            # Create body
            body = f"""## 📋 Work Item Details

**ID:** {work_item["id"]}
**Status:** {work_item.get("status", "proposed")}
**Priority:** {work_item.get("priority", "medium")}
**Type:** {work_item.get("type", "task")}

## 📝 Description

{work_item.get("description", "No description provided")}

---

*This issue was automatically created from the AI Lab Framework database.*
"""

            # Create labels
            labels = ["ai-lab", "work-item", "framework"]
            labels.append(f"priority:{work_item.get('priority', 'medium')}")
            labels.append(f"status:{work_item.get('status', 'proposed')}")

            if work_item.get("component"):
                labels.append(f"component:{work_item['component']}")

            # Create issue
            issue = repo.create_issue(title=title, body=body, labels=labels)

            # Update database
            db.update_github_sync(
                local_id=work_item["id"],
                local_type="work_item",
                github_issue_id=issue.number,
                github_url=issue.html_url,
            )

            print(f"  ✅ Created #{issue.number}: {issue.title[:50]}...")
            success_count += 1

            # Rate limiting
            time.sleep(2)

        except Exception as e:
            print(f"  ❌ Failed to create {work_item['id']}: {e}")
            error_count += 1

    print(f"\n📊 Results: {success_count} created, {error_count} errors")

    # Verify
    print("\n🔍 Verification:")
    all_issues = list(repo.get_issues(labels=["ai-lab"]))
    work_item_issues = [
        i for i in all_issues if "work-item" in [l.name for l in i.labels]
    ]
    print(f"Total work item issues on GitHub: {len(work_item_issues)}")


if __name__ == "__main__":
    main()
