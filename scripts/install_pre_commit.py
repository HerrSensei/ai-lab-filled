#!/usr/bin/env python3
"""
AI Lab Framework - Pre-Commit Hook Installer

Installiert und konfiguriert Pre-Commit Hooks für automatische Tests.

Usage:
    python scripts/install_pre_commit.py
    python scripts/install_pre_commit.py --force
"""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Dict, List


class PreCommitInstaller:
    """Installs and configures pre-commit hooks."""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.pre_commit_config = base_dir / ".pre-commit-config.yaml"

    def install(self, force: bool = False) -> bool:
        """Install pre-commit hooks."""
        print("🔧 Installing pre-commit hooks...")

        # Create pre-commit config
        if not self._create_pre_commit_config(force):
            return False

        # Install pre-commit package
        if not self._install_pre_commit_package():
            return False

        # Install hooks
        if not self._install_hooks():
            return False

        print("✅ Pre-commit hooks installed successfully!")
        print("\n📋 Installed hooks:")
        print("  • Black - Code formatting")
        print("  • Ruff - Linting and import sorting")
        print("  • MyPy - Type checking")
        print("  • pytest - Unit tests")
        print("  • Bandit - Security scanning")
        print("  • Safety - Dependency vulnerability check")

        print("\n🚀 Hooks will run automatically before each commit!")
        return True

    def _create_pre_commit_config(self, force: bool) -> bool:
        """Create pre-commit configuration file."""
        config_content = """repos:
  # Black - Code formatting
  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black
        language_version: python3.11
        args: [--line-length=88]

  # Ruff - Linting and import sorting
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  # MyPy - Type checking
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
        args: [--ignore-missing-imports, src/]

  # pytest - Unit tests
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: python -m pytest tests/unit/ -v --tb=short
        language: system
        pass_filenames: false
        always_run: true

  # Bandit - Security scanning
  - repo: https://github.com/pycqa/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: [-r, src/, -f, json, -o, bandit-report.json]
        pass_filenames: false

  # Safety - Dependency vulnerability check
  - repo: https://github.com/pyupio/safety
    rev: 2.3.5
    hooks:
      - id: safety
        args: [--json, --output, safety-report.json]

  # General hooks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-added-large-files
        args: [--maxkb=1000]
      - id: check-merge-conflict
      - id: debug-statements

  # Custom hooks for AI Lab Framework
  - repo: local
    hooks:
      - id: ai-lab-session-check
        name: AI Lab Session Check
        entry: python scripts/create_session_log.py --list
        language: system
        pass_filenames: false
        always_run: false
        stages: [commit]

  - repo: local
    hooks:
      - id: ai-lab-dashboard-update
        name: AI Lab Dashboard Update
        entry: python scripts/dashboard_realtime.py --output=dashboard/pre-commit.html
        language: system
        pass_filenames: false
        always_run: false
        stages: [push]
"""

        if self.pre_commit_config.exists() and not force:
            print(f"⚠️  Pre-commit config already exists: {self.pre_commit_config}")
            response = input("Overwrite? (y/N): ")
            if response.lower() != "y":
                return False

        try:
            self.pre_commit_config.write_text(config_content)
            print(f"✅ Pre-commit config created: {self.pre_commit_config}")
            return True
        except Exception as e:
            print(f"❌ Failed to create pre-commit config: {e}")
            return False

    def _install_pre_commit_package(self) -> bool:
        """Install pre-commit package."""
        print("📦 Installing pre-commit package...")

        try:
            # Check if pre-commit is already installed
            result = subprocess.run(
                ["pre-commit", "--version"], capture_output=True, text=True, check=True
            )
            print(f"✅ Pre-commit already installed: {result.stdout.strip()}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Install pre-commit
            try:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "pre-commit"],
                    check=True,
                    capture_output=True,
                )
                print("✅ Pre-commit package installed")
                return True
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install pre-commit: {e}")
                return False

    def _install_hooks(self) -> bool:
        """Install pre-commit hooks."""
        print("🪝 Installing pre-commit hooks...")

        try:
            result = subprocess.run(
                ["pre-commit", "install"], capture_output=True, text=True, check=True
            )
            print("✅ Pre-commit hooks installed")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install hooks: {e}")
            print(f"Output: {e.output}")
            return False

    def uninstall(self) -> bool:
        """Uninstall pre-commit hooks."""
        print("🗑️  Uninstalling pre-commit hooks...")

        try:
            subprocess.run(
                ["pre-commit", "uninstall"], capture_output=True, text=True, check=True
            )
            print("✅ Pre-commit hooks uninstalled")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to uninstall hooks: {e}")
            return False

    def run_all_files(self) -> bool:
        """Run pre-commit on all files."""
        print("🔍 Running pre-commit on all files...")

        try:
            result = subprocess.run(
                ["pre-commit", "run", "--all-files"], capture_output=True, text=True
            )

            if result.returncode == 0:
                print("✅ All pre-commit checks passed")
                return True
            else:
                print("❌ Some pre-commit checks failed")
                print(result.stdout)
                if result.stderr:
                    print(result.stderr)
                return False
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to run pre-commit: {e}")
            return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Install pre-commit hooks")

    parser.add_argument(
        "--install", action="store_true", help="Install pre-commit hooks"
    )
    parser.add_argument(
        "--uninstall", action="store_true", help="Uninstall pre-commit hooks"
    )
    parser.add_argument(
        "--run-all", action="store_true", help="Run pre-commit on all files"
    )
    parser.add_argument(
        "--force", action="store_true", help="Force overwrite existing config"
    )
    parser.add_argument(
        "--base-dir", type=Path, default=Path.cwd(), help="Base directory"
    )

    args = parser.parse_args()

    installer = PreCommitInstaller(args.base_dir)

    if args.uninstall:
        success = installer.uninstall()
    elif args.run_all:
        success = installer.run_all_files()
    else:
        # Default action: install
        success = installer.install(args.force)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
