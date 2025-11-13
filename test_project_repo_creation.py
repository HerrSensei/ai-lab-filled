#!/usr/bin/env python3
"""
Test script for project repository creation
"""

import os
from infrastructure.db.project_repo_manager import (
    get_repo_manager,
    get_project_sync_status,
)


def test_project_repo_creation():
    """Test project repository creation functionality"""

    # Check environment
    if not os.getenv("GITHUB_TOKEN"):
        print("❌ GITHUB_TOKEN not configured")
        return

    print("🧪 Testing Project Repository Creation")
    print("=" * 50)

    # Get project sync status
    print("📊 Getting project sync status...")
    status = get_project_sync_status()

    print(f"Total Projects: {status['total_projects']}")
    print(f"With Repositories: {status['with_repositories']}")
    print(f"Without Repositories: {status['without_repositories']}")

    print("\n📦 Projects:")
    for project in status["projects"]:
        repo_status = "✅" if project["has_repository"] else "❌"
        print(
            f"  {repo_status} {project['id']}: {project['name']} ({project['work_items_count']} work items)"
        )

    # Test creating repository for a project without one
    projects_without_repo = [p for p in status["projects"] if not p["has_repository"]]

    if projects_without_repo:
        project = projects_without_repo[0]
        print(f"\n🚀 Creating repository for project: {project['id']}")

        manager = get_repo_manager()
        repo = manager.create_repository_from_project(project["id"])

        if repo:
            print(f"✅ Repository created: {repo.html_url}")
            print(f"📝 Repository name: {repo.name}")
            print(f"🔒 Private: {repo.private}")
            print(f"📋 Issues enabled: {repo.has_issues}")
        else:
            print("❌ Failed to create repository")
    else:
        print("\n✅ All projects already have repositories!")

    print("\n🎉 Test completed!")


if __name__ == "__main__":
    test_project_repo_creation()
