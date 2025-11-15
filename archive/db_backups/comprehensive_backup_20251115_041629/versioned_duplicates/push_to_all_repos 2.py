#!/usr/bin/env python3
"""
AI Lab Framework - Multi-Repository Push Script

Automatisiertes Pushen von Änderungen zu allen Repositories.
Unterstützt selektive Pushes und Synchronisation.

Usage:
    python scripts/push_to_all_repos.py --message="Update documentation"
    python scripts/push_to_all_repos.py --repos="ai-lab,ai-lab-framework" --message="Fix bug"
    python scripts/push_to_all_repos.py --feature-branch --message="Feature update"
"""

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional


class MultiRepoPusher:
    """Handles pushing changes to multiple repositories."""

    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = base_dir or Path.cwd()
        self.repositories = {
            "ai-lab": "origin",
            "ai-lab-framework": "ai-lab-framework",
            "ai-lab-filled": "ai-lab-filled",
        }

    def push_to_all(self, message: str, feature_branch: bool = False) -> bool:
        """Push changes to all repositories."""
        print(f"🚀 Pushing changes to all repositories...")
        print(f"📝 Message: {message}")

        if feature_branch:
            current_branch = self._get_current_branch()
            print(f"🌿 Feature branch: {current_branch}")

        success = True

        for repo_name, remote in self.repositories.items():
            print(f"\n📦 Pushing to {repo_name}...")

            if not self._push_to_repository(repo_name, remote, message, feature_branch):
                print(f"❌ Failed to push to {repo_name}")
                success = False
            else:
                print(f"✅ Successfully pushed to {repo_name}")

        return success

    def push_to_selected(
        self, repos: List[str], message: str, feature_branch: bool = False
    ) -> bool:
        """Push changes to selected repositories."""
        print(f"🚀 Pushing changes to selected repositories...")
        print(f"📝 Message: {message}")
        print(f"📦 Repositories: {', '.join(repos)}")

        if feature_branch:
            current_branch = self._get_current_branch()
            print(f"🌿 Feature branch: {current_branch}")

        success = True

        for repo_name in repos:
            if repo_name not in self.repositories:
                print(f"⚠️  Unknown repository: {repo_name}")
                continue

            remote = self.repositories[repo_name]
            print(f"\n📦 Pushing to {repo_name}...")

            if not self._push_to_repository(repo_name, remote, message, feature_branch):
                print(f"❌ Failed to push to {repo_name}")
                success = False
            else:
                print(f"✅ Successfully pushed to {repo_name}")

        return success

    def sync_repositories(self) -> bool:
        """Synchronize all repositories with their remotes."""
        print("🔄 Synchronizing all repositories...")

        success = True

        for repo_name, remote in self.repositories.items():
            print(f"\n📦 Syncing {repo_name}...")

            if not self._sync_repository(repo_name, remote):
                print(f"❌ Failed to sync {repo_name}")
                success = False
            else:
                print(f"✅ Successfully synced {repo_name}")

        return success

    def _push_to_repository(
        self, repo_name: str, remote: str, message: str, feature_branch: bool
    ) -> bool:
        """Push changes to specific repository."""
        try:
            # Stage all changes
            subprocess.run(["git", "add", "."], check=True, capture_output=True)

            # Commit changes
            commit_message = f"{message}\n\nAutomated push to {repo_name}\nTimestamp: {datetime.now().isoformat()}"
            subprocess.run(
                ["git", "commit", "-m", commit_message], check=True, capture_output=True
            )

            # Push to remote
            if feature_branch:
                current_branch = self._get_current_branch()
                subprocess.run(
                    ["git", "push", remote, current_branch],
                    check=True,
                    capture_output=True,
                )
            else:
                subprocess.run(
                    ["git", "push", remote, "main"], check=True, capture_output=True
                )

            return True

        except subprocess.CalledProcessError as e:
            print(f"Error pushing to {repo_name}: {e}")
            return False

    def _sync_repository(self, repo_name: str, remote: str) -> bool:
        """Synchronize specific repository with remote."""
        try:
            # Fetch latest changes
            subprocess.run(["git", "fetch", remote], check=True, capture_output=True)

            # Get current branch
            current_branch = self._get_current_branch()

            # Pull latest changes
            subprocess.run(
                ["git", "pull", remote, current_branch], check=True, capture_output=True
            )

            return True

        except subprocess.CalledProcessError as e:
            print(f"Error syncing {repo_name}: {e}")
            return False

    def _get_current_branch(self) -> str:
        """Get current git branch."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return "main"

    def list_repositories(self):
        """List all available repositories."""
        print("📦 Available repositories:")
        for repo_name in self.repositories.keys():
            print(f"  - {repo_name}")

    def get_status(self) -> bool:
        """Get status of all repositories."""
        print("📊 Repository Status:")

        success = True

        for repo_name, remote in self.repositories.items():
            print(f"\n📦 {repo_name}:")

            try:
                # Check if remote is accessible
                result = subprocess.run(
                    ["git", "ls-remote", remote, "HEAD"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                print(f"  ✅ Remote accessible")

                # Check if local is ahead/behind
                current_branch = self._get_current_branch()
                result = subprocess.run(
                    [
                        "git",
                        "rev-list",
                        "--count",
                        "--left-right",
                        f"{remote}/{current_branch}...HEAD",
                    ],
                    capture_output=True,
                    text=True,
                    check=True,
                )

                behind, ahead = result.stdout.strip().split("\t")
                if ahead == "0" and behind == "0":
                    print(f"  ✅ Up to date")
                elif ahead != "0":
                    print(f"  ⬆️  Ahead by {ahead} commits")
                elif behind != "0":
                    print(f"  ⬇️  Behind by {behind} commits")

            except subprocess.CalledProcessError as e:
                print(f"  ❌ Error checking status: {e}")
                success = False

        return success


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Push to multiple repositories")

    parser.add_argument("--message", "-m", required=True, help="Commit message")
    parser.add_argument("--repos", help="Comma-separated list of repositories")
    parser.add_argument(
        "--feature-branch", action="store_true", help="Push current feature branch"
    )
    parser.add_argument(
        "--sync", action="store_true", help="Sync repositories instead of pushing"
    )
    parser.add_argument("--status", action="store_true", help="Show repository status")
    parser.add_argument(
        "--list", action="store_true", help="List available repositories"
    )
    parser.add_argument(
        "--base-dir", type=Path, help="Base directory (default: current)"
    )

    args = parser.parse_args()

    pusher = MultiRepoPusher(args.base_dir)

    if args.list:
        pusher.list_repositories()
        return

    if args.status:
        pusher.get_status()
        return

    if args.sync:
        success = pusher.sync_repositories()
    elif args.repos:
        repos = [repo.strip() for repo in args.repos.split(",")]
        success = pusher.push_to_selected(repos, args.message, args.feature_branch)
    else:
        success = pusher.push_to_all(args.message, args.feature_branch)

    if success:
        print("\n🎉 Operation completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Operation failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
