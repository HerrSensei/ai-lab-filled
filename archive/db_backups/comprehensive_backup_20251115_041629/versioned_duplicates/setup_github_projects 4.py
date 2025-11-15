#!/usr/bin/env python3
"""
Set up GitHub Projects for proper project management
"""

import os

from github import Github


def main():
    token = os.getenv("GITHUB_TOKEN")
    repo_name = os.getenv("GITHUB_REPO")

    if not token or not repo_name:
        print("❌ GITHUB_TOKEN and GITHUB_REPO environment variables required")
        return

    github = Github(token)
    repo = github.get_repo(repo_name)

    # Check if Projects v2 is available
    try:
        # Create a new project
        project = repo.create_project(
            name="AI Lab Framework Roadmap",
            body="Central project management for AI Lab Framework work items and ideas",
        )
        print(f"✅ Created project: {project.name}")

        # Get all ai-lab issues
        issues = list(repo.get_issues(labels=["ai-lab"]))
        print(f"Found {len(issues)} issues to organize")

        # Add issues to project
        for issue in issues:
            try:
                project.create_card(content=issue)
                print(f"  ✅ Added issue #{issue.number}: {issue.title[:50]}...")
            except Exception as e:
                print(f"  ❌ Failed to add issue #{issue.number}: {e}")

        print("\n📊 Project setup complete!")
        print(f"🔗 View project at: {project.html_url}")

    except Exception as e:
        print(f"❌ Error setting up project: {e}")
        print("Falling back to manual setup...")

        # Fallback: Show how to organize manually
        print("\n📋 Manual Organization Guide:")
        print("1. Go to GitHub Projects tab")
        print("2. Create new project 'AI Lab Framework Roadmap'")
        print("3. Add columns: Backlog, Todo, In Progress, Done")
        print("4. Add all ai-lab labeled issues to the project")
        print("5. Organize by status:")

        issues = list(repo.get_issues(labels=["ai-lab"]))
        for issue in issues:
            status = "todo"
            for label in issue.labels:
                if label.name.startswith("status:"):
                    status = label.name.split(":", 1)[1]
                    break
            print(f"  - #{issue.number}: {issue.title[:40]:<40} -> {status}")


if __name__ == "__main__":
    main()
