#!/usr/bin/env python3
"""
AI Lab Framework - Deployment Script

Automatisiertes Deployment von Framework-Änderungen zu allen Repositories.
Unterstützt Feature Branches, Releases und Hotfixes.

Usage:
    python scripts/deploy_framework.py --version=v1.2.0
    python scripts/deploy_framework.py --feature=FRM-001-new-tool
    python scripts/deploy_framework.py --hotfix=HOTFIX-001-critical-fix
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class FrameworkDeployer:
    """Handles deployment of framework changes across repositories."""

    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = base_dir or Path.cwd()
        self.repositories = {
            "ai-lab": "origin",
            "ai-lab-framework": "ai-lab-framework",
            "ai-lab-filled": "ai-lab-filled",
        }
        self.session_logger = self._init_session_logger()

    def _init_session_logger(self):
        """Initialize session logging."""
        try:
            sys.path.append(str(self.base_dir / "scripts"))
            from create_session_log import SessionLogger

            return SessionLogger(self.base_dir)
        except ImportError:
            return None

    def deploy_version(self, version: str) -> bool:
        """Deploy a specific version to all repositories."""
        print(f"🚀 Deploying version {version} to all repositories...")

        # Create deployment session
        if self.session_logger:
            self.session_logger.create_session_log("deploy")

        # Validate version format
        if not version.startswith("v"):
            version = f"v{version}"

        success = True

        for repo_name, remote in self.repositories.items():
            print(f"\n📦 Deploying to {repo_name}...")

            if not self._deploy_to_repository(repo_name, remote, version):
                print(f"❌ Failed to deploy to {repo_name}")
                success = False
            else:
                print(f"✅ Successfully deployed to {repo_name}")

        return success

    def deploy_feature(self, feature_branch: str) -> bool:
        """Deploy a feature branch to all repositories."""
        print(f"🌿 Deploying feature {feature_branch} to all repositories...")

        if self.session_logger:
            self.session_logger.create_session_log("feature-deploy")

        success = True

        for repo_name, remote in self.repositories.items():
            print(f"\n📦 Deploying feature to {repo_name}...")

            if not self._deploy_feature_to_repository(
                repo_name, remote, feature_branch
            ):
                print(f"❌ Failed to deploy feature to {repo_name}")
                success = False
            else:
                print(f"✅ Successfully deployed feature to {repo_name}")

        return success

    def deploy_hotfix(self, hotfix_branch: str) -> bool:
        """Deploy a hotfix to all repositories."""
        print(f"🚨 Deploying hotfix {hotfix_branch} to all repositories...")

        if self.session_logger:
            self.session_logger.create_session_log("hotfix-deploy")

        success = True

        for repo_name, remote in self.repositories.items():
            print(f"\n📦 Deploying hotfix to {repo_name}...")

            if not self._deploy_hotfix_to_repository(repo_name, remote, hotfix_branch):
                print(f"❌ Failed to deploy hotfix to {repo_name}")
                success = False
            else:
                print(f"✅ Successfully deployed hotfix to {repo_name}")

        return success

    def sync_framework(self) -> bool:
        """Sync framework changes from ai-lab-framework to other repositories."""
        print("🔄 Syncing framework changes to all repositories...")

        if self.session_logger:
            self.session_logger.create_session_log("framework-sync")

        # Get current framework commit
        framework_commit = self._get_current_commit("ai-lab-framework")
        if not framework_commit:
            print("❌ Could not get framework commit")
            return False

        success = True

        # Deploy to ai-lab (main repository)
        if not self._sync_framework_to_repo("ai-lab", "origin", framework_commit):
            print("❌ Failed to sync framework to ai-lab")
            success = False

        # Deploy to ai-lab-filled
        if not self._sync_framework_to_repo(
            "ai-lab-filled", "ai-lab-filled", framework_commit
        ):
            print("❌ Failed to sync framework to ai-lab-filled")
            success = False

        return success

    def _deploy_to_repository(self, repo_name: str, remote: str, version: str) -> bool:
        """Deploy version to specific repository."""
        try:
            # Checkout main branch
            subprocess.run(["git", "checkout", "main"], check=True, capture_output=True)

            # Pull latest changes
            subprocess.run(
                ["git", "pull", remote, "main"], check=True, capture_output=True
            )

            # Create release branch
            release_branch = f"release/{version}"
            subprocess.run(
                ["git", "checkout", "-b", release_branch],
                check=True,
                capture_output=True,
            )

            # Update version files
            self._update_version_files(version)

            # Commit version update
            subprocess.run(["git", "add", "."], check=True, capture_output=True)
            commit_message = f"""chore: Update version to {version}

- Update version in configuration files
- Prepare for release {version}
- Automated deployment"""
            subprocess.run(
                ["git", "commit", "-m", commit_message], check=True, capture_output=True
            )

            # Push release branch
            subprocess.run(
                ["git", "push", remote, release_branch], check=True, capture_output=True
            )

            # Create and push tag
            subprocess.run(
                ["git", "tag", "-a", version, "-m", f"Release {version}"],
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "push", remote, version], check=True, capture_output=True
            )

            # Merge to main
            subprocess.run(["git", "checkout", "main"], check=True, capture_output=True)
            subprocess.run(
                ["git", "merge", release_branch], check=True, capture_output=True
            )
            subprocess.run(
                ["git", "push", remote, "main"], check=True, capture_output=True
            )

            # Delete release branch
            subprocess.run(
                ["git", "branch", "-d", release_branch], check=True, capture_output=True
            )

            return True

        except subprocess.CalledProcessError as e:
            print(f"Error deploying to {repo_name}: {e}")
            return False

    def _deploy_feature_to_repository(
        self, repo_name: str, remote: str, feature_branch: str
    ) -> bool:
        """Deploy feature branch to specific repository."""
        try:
            # Checkout feature branch
            subprocess.run(
                ["git", "checkout", feature_branch], check=True, capture_output=True
            )

            # Pull latest changes
            subprocess.run(
                ["git", "pull", remote, feature_branch], check=True, capture_output=True
            )

            # Push to remote
            subprocess.run(
                ["git", "push", remote, feature_branch], check=True, capture_output=True
            )

            return True

        except subprocess.CalledProcessError as e:
            print(f"Error deploying feature to {repo_name}: {e}")
            return False

    def _deploy_hotfix_to_repository(
        self, repo_name: str, remote: str, hotfix_branch: str
    ) -> bool:
        """Deploy hotfix to specific repository."""
        try:
            # Checkout hotfix branch
            subprocess.run(
                ["git", "checkout", hotfix_branch], check=True, capture_output=True
            )

            # Pull latest changes
            subprocess.run(
                ["git", "pull", remote, hotfix_branch], check=True, capture_output=True
            )

            # Merge to main
            subprocess.run(["git", "checkout", "main"], check=True, capture_output=True)
            subprocess.run(
                ["git", "merge", hotfix_branch], check=True, capture_output=True
            )

            # Push to main
            subprocess.run(
                ["git", "push", remote, "main"], check=True, capture_output=True
            )

            # Create hotfix tag
            hotfix_tag = hotfix_branch.replace("hotfix/", "hotfix-")
            subprocess.run(
                ["git", "tag", "-a", hotfix_tag, "-m", f"Hotfix {hotfix_tag}"],
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "push", remote, hotfix_tag], check=True, capture_output=True
            )

            return True

        except subprocess.CalledProcessError as e:
            print(f"Error deploying hotfix to {repo_name}: {e}")
            return False

    def _sync_framework_to_repo(
        self, repo_name: str, remote: str, framework_commit: str
    ) -> bool:
        """Sync framework changes to specific repository."""
        try:
            # Checkout main branch
            subprocess.run(["git", "checkout", "main"], check=True, capture_output=True)

            # Pull latest changes
            subprocess.run(
                ["git", "pull", remote, "main"], check=True, capture_output=True
            )

            # Create sync branch
            sync_branch = f"sync/framework-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            subprocess.run(
                ["git", "checkout", "-b", sync_branch], check=True, capture_output=True
            )

            # Cherry-pick framework commit
            subprocess.run(
                ["git", "cherry-pick", framework_commit],
                check=True,
                capture_output=True,
            )

            # Push sync branch
            subprocess.run(
                ["git", "push", remote, sync_branch], check=True, capture_output=True
            )

            # Create pull request (manual step for now)
            print(f"📋 Pull Request created: {sync_branch} -> main")
            print(f"   Please review and merge the PR for {repo_name}")

            return True

        except subprocess.CalledProcessError as e:
            print(f"Error syncing framework to {repo_name}: {e}")
            return False

    def _get_current_commit(self, repo_name: str) -> Optional[str]:
        """Get current commit hash for repository."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None

    def _update_version_files(self, version: str):
        """Update version in configuration files."""
        # Update pyproject.toml
        pyproject_path = self.base_dir / "pyproject.toml"
        if pyproject_path.exists():
            content = pyproject_path.read_text()
            # Simple version replacement (could be improved with proper TOML parsing)
            content = content.replace(
                'version = "0.1.0"', f'version = "{version.lstrip("v")}"'
            )
            pyproject_path.write_text(content)

        # Update README.md
        readme_path = self.base_dir / "README.md"
        if readme_path.exists():
            content = readme_path.read_text()
            if "## Version" in content:
                content = content.replace(
                    "## Version", f"## Version\n\nCurrent version: {version}"
                )
            readme_path.write_text(content)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Deploy AI Lab Framework")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--version", help="Deploy specific version (e.g., v1.2.0)")
    group.add_argument("--feature", help="Deploy feature branch")
    group.add_argument("--hotfix", help="Deploy hotfix branch")
    group.add_argument(
        "--sync-framework", action="store_true", help="Sync framework changes"
    )

    parser.add_argument(
        "--base-dir", type=Path, help="Base directory (default: current)"
    )

    args = parser.parse_args()

    deployer = FrameworkDeployer(args.base_dir)

    success = False

    if args.version:
        success = deployer.deploy_version(args.version)
    elif args.feature:
        success = deployer.deploy_feature(args.feature)
    elif args.hotfix:
        success = deployer.deploy_hotfix(args.hotfix)
    elif args.sync_framework:
        success = deployer.sync_framework()

    if success:
        print("\n🎉 Deployment completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Deployment failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
