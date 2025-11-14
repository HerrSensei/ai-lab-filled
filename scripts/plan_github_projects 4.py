#!/usr/bin/env python3
"""
Generate GitHub Projects organization plan
"""

import os
from collections import defaultdict

from github import Github


def main():
    token = os.getenv("GITHUB_TOKEN")
    repo_name = os.getenv("GITHUB_REPO")

    if not token or not repo_name:
        print("❌ GITHUB_TOKEN and GITHUB_REPO environment variables required")
        return

    github = Github(token)
    repo = github.get_repo(repo_name)

    # Get all ai-lab issues
    issues = list(repo.get_issues(labels=["ai-lab"]))

    # Organize by status and type
    by_status = defaultdict(list)
    by_type = defaultdict(list)
    by_project = defaultdict(list)

    for issue in issues:
        # Get status from labels
        status = "todo"
        issue_type = "unknown"

        for label in issue.labels:
            label_name = label.name
            if label_name.startswith("status:"):
                status = label_name.split(":", 1)[1]
            elif label_name in ["work-item", "idea"]:
                issue_type = label_name

        # Get project from issue ID
        issue_id = None
        if "[" in issue.title and "]" in issue.title:
            issue_id = issue.title.split("[")[1].split("]")[0]

        by_status[status].append(issue)
        by_type[issue_type].append(issue)

        if issue_id:
            project_id = issue_id.split("-")[0] if "-" in issue_id else "unknown"
            by_project[project_id].append(issue)

    print("🎯 GitHub Projects Organization Plan")
    print("=" * 50)

    print("\n📋 By Status (Columns):")
    for status, items in by_status.items():
        print(f"\n{status.title()} ({len(items)} items):")
        for issue in items:
            print(f"  - #{issue.number}: {issue.title[:50]}...")

    print("\n🏷️ By Type:")
    for issue_type, items in by_type.items():
        print(f"\n{issue_type.title()} ({len(items)} items):")
        for issue in items:
            print(f"  - #{issue.number}: {issue.title[:50]}...")

    print("\n📁 By Project:")
    for project_id, items in by_project.items():
        print(f"\n{project_id.upper()} ({len(items)} items):")
        for issue in items:
            status = "todo"
            for label in issue.labels:
                if label.name.startswith("status:"):
                    status = label.name.split(":", 1)[1]
                    break
            print(f"  - #{issue.number}: {issue.title[:45]:<45} [{status}]")

    print("\n🚀 Recommended Project Structure:")
    print("\n1. Main Board: AI Lab Framework Roadmap")
    print("   Columns: Backlog, Todo, In Progress, Done")

    print("\n2. Suggested Milestones:")
    for project_id, items in by_project.items():
        if project_id not in ["unknown", "SYNC", "PROJ"]:
            print(f"   - {project_id.upper()} Project ({len(items)} items)")

    print("\n3. Quick Actions:")
    print("   - Move 'done' items to Done column")
    print("   - Move 'in_progress' items to In Progress column")
    print("   - Move 'backlog' items to Backlog column")
    print("   - Keep 'todo' items in Todo column")

    print(f"\n📊 Summary: {len(issues)} total issues ready for project management!")


if __name__ == "__main__":
    main()
