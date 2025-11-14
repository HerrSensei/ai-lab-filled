#!/usr/bin/env python3
"""
Multi-repository push script for AI Lab Framework
Pushes changes to all three repositories: ai-lab, ai-lab-filled, ai-lab-framework
"""

import subprocess
import sys
from datetime import datetime


def run_command(cmd, description):
    """Run command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed")
            return True
        else:
            print(f"❌ {description} failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ {description} failed: {e}")
        return False


def main():
    """Push to all repositories"""

    # Check if we have changes to commit
    result = subprocess.run(
        "git status --porcelain", shell=True, capture_output=True, text=True
    )
    if not result.stdout.strip():
        print("ℹ️  No changes to commit")
        return

    print("🚀 AI Lab Framework - Multi-Repository Push")
    print("=" * 50)

    # Add all changes
    if not run_command("git add .", "Staging changes"):
        return

    # Get commit message or use default
    try:
        commit_msg = (
            sys.argv[1]
            if len(sys.argv) > 1
            else f"Update {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )
    except:
        commit_msg = f"Update {datetime.now().strftime('%Y-%m-%d %H:%M')}"

    # Commit changes
    if not run_command(f'git commit -m "{commit_msg}"', "Committing changes"):
        return

    # Define repositories
    repos = [
        ("origin", "ai-lab (main)"),
        ("ai-lab-filled", "ai-lab-filled"),
        ("ai-lab-framework", "ai-lab-framework"),
    ]

    success_count = 0

    # Push to each repository
    for remote, description in repos:
        if run_command(f"git push {remote} main --force", f"Pushing to {description}"):
            success_count += 1
        print()

    # Summary
    print("=" * 50)
    print(f"📊 Push Summary: {success_count}/{len(repos)} repositories updated")

    if success_count == len(repos):
        print("🎉 All repositories updated successfully!")
    else:
        print("⚠️  Some repositories failed to update")

    # Show remotes for reference
    print("\n📡 Configured Remotes:")
    result = subprocess.run("git remote -v", shell=True, capture_output=True, text=True)
    print(result.stdout)


if __name__ == "__main__":
    main()
