#!/usr/bin/env python3
"""
Check what's actually on GitHub vs database
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

    # Get all issues with ai-lab label
    issues = list(repo.get_issues(labels=["ai-lab"]))

    print(f"Found {len(issues)} issues with 'ai-lab' label:")
    for issue in issues:
        labels = [label.name for label in issue.labels]
        print(f"  #{issue.number}: {issue.title}")
        print(f"    Labels: {', '.join(labels)}")
        print(f"    State: {issue.state}")
        print()


if __name__ == "__main__":
    main()
