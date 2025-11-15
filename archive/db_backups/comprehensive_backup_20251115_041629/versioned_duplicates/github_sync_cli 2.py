#!/usr/bin/env python3
"""
AI Lab Framework - GitHub Sync CLI
Simple command-line interface for GitHub synchronization
"""

import argparse
import sys
import os


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="AI Lab Framework GitHub Sync CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s sync-work-item WORK-001 --status done --priority high
  %(prog)s sync-idea IDEA-001 --status refining
  %(prog)s full-sync
  %(prog)s setup
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Work item sync command
    work_item_parser = subparsers.add_parser(
        "sync-work-item", help="Sync work item to GitHub"
    )
    work_item_parser.add_argument("id", help="Work item ID")
    work_item_parser.add_argument("--status", help="New status")
    work_item_parser.add_argument("--priority", help="New priority")

    # Idea sync command
    idea_parser = subparsers.add_parser("sync-idea", help="Sync idea to GitHub")
    idea_parser.add_argument("id", help="Idea ID")
    idea_parser.add_argument("--status", help="New status")
    idea_parser.add_argument("--priority", help="New priority")

    # Full sync command
    subparsers.add_parser("full-sync", help="Run full bidirectional sync")

    # Setup command
    subparsers.add_parser("setup", help="Setup GitHub repository labels")

    args = parser.parse_args()

    # Check environment
    if not os.getenv("GITHUB_TOKEN") or not os.getenv("GITHUB_REPO"):
        print("❌ GitHub credentials not configured")
        print("Set GITHUB_TOKEN and GITHUB_REPO environment variables")
        sys.exit(1)

    # Execute command
    if args.command == "sync-work-item":
        from infrastructure.db.sync_helpers import sync_work_item

        if not args.status and not args.priority:
            print("❌ Must specify --status or --priority")
            sys.exit(1)

        success = sync_work_item(args.id, args.status, args.priority)
        if success:
            print(f"✅ Work item {args.id} synced successfully")
        else:
            print(f"❌ Failed to sync work item {args.id}")
            sys.exit(1)

    elif args.command == "sync-idea":
        from infrastructure.db.sync_helpers import sync_idea

        if not args.status and not args.priority:
            print("❌ Must specify --status or --priority")
            sys.exit(1)

        success = sync_idea(args.id, args.status, args.priority)
        if success:
            print(f"✅ Idea {args.id} synced successfully")
        else:
            print(f"❌ Failed to sync idea {args.id}")
            sys.exit(1)

    elif args.command == "full-sync":
        from ai_lab_framework.github_integration import main as github_main

        # Simulate command line args for github_integration
        sys.argv = ["github_integration.py", "--action", "sync-all"]
        github_main()

    elif args.command == "setup":
        from ai_lab_framework.github_integration import main as github_main

        # Simulate command line args for github_integration
        sys.argv = ["github_integration.py", "--action", "setup"]
        github_main()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
