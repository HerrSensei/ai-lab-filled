#!/usr/bin/env python3
"""
AI Lab Framework - Project Repository CLI
Command-line interface for managing project repositories
"""

import argparse
import sys
import os
from infrastructure.db.project_repo_manager import (
    get_repo_manager,
    create_repository_from_project,
    sync_all_projects,
    get_project_sync_status,
)


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="AI Lab Framework Project Repository CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s status                          # Show project sync status
  %(prog)s create PROJ-001                 # Create repository for project
  %(prog)s sync-all                        # Sync all projects to repositories
  %(prog)s list                            # List all projects
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Status command
    status_parser = subparsers.add_parser("status", help="Show project sync status")

    # Create command
    create_parser = subparsers.add_parser(
        "create", help="Create repository for project"
    )
    create_parser.add_argument("project_id", help="Project ID")

    # Sync all command
    subparsers.add_parser("sync-all", help="Sync all projects to repositories")

    # List command
    subparsers.add_parser("list", help="List all projects")

    args = parser.parse_args()

    # Check environment
    if not os.getenv("GITHUB_TOKEN"):
        print("❌ GITHUB_TOKEN not configured")
        print("Set GITHUB_TOKEN environment variable")
        sys.exit(1)

    # Execute command
    if args.command == "status":
        print("📊 Project Repository Sync Status")
        print("=" * 40)

        status = get_project_sync_status()

        print(f"Total Projects: {status['total_projects']}")
        print(f"With Repositories: {status['with_repositories']}")
        print(f"Without Repositories: {status['without_repositories']}")

        if status["projects"]:
            print("\n📦 Projects:")
            for project in status["projects"]:
                repo_status = "✅" if project["has_repository"] else "❌"
                repo_info = (
                    f" ({project['repository_url']})"
                    if project["repository_url"]
                    else ""
                )
                print(f"  {repo_status} {project['id']}: {project['name']}{repo_info}")
                print(
                    f"      Status: {project['status']}, Work Items: {project['work_items_count']}"
                )

    elif args.command == "create":
        print(f"🚀 Creating repository for project: {args.project_id}")

        success = create_repository_from_project(args.project_id)
        if success:
            print(f"✅ Repository created successfully for {args.project_id}")
        else:
            print(f"❌ Failed to create repository for {args.project_id}")
            sys.exit(1)

    elif args.command == "sync-all":
        print("🔄 Syncing all projects to repositories...")

        results = sync_all_projects()

        print(f"\n📊 Sync Results:")
        print(f"  Created: {results['created']}")
        print(f"  Updated: {results['updated']}")
        print(f"  Errors: {results['errors']}")

        if results["errors"] > 0:
            sys.exit(1)

    elif args.command == "list":
        print("📦 All Projects")
        print("=" * 30)

        status = get_project_sync_status()

        for project in status["projects"]:
            repo_marker = "🌐" if project["has_repository"] else "📁"
            print(f"{repo_marker} {project['id']}: {project['name']}")
            print(f"    Status: {project['status']}")
            print(f"    Work Items: {project['work_items_count']}")
            if project["repository_url"]:
                print(f"    Repository: {project['repository_url']}")
            print()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
