#!/usr/bin/env python3
"""
AI Lab Framework - Release Automation Script

Automatisiert die Erstellung von Releases mit Versionierung, Tagging und Deployment.

Usage:
    python scripts/create_release.py --version=v1.2.0
    python scripts/create_release.py --version=v1.2.0 --auto-deploy
    python scripts/create_release.py --version=v1.2.0 --release-candidate
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class ReleaseManager:
    """Manages the release process for AI Lab Framework."""
    
    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = base_dir or Path.cwd()
        self.changelog_path = self.base_dir / 'ai-logs' / 'changelogs' / 'CHANGELOG.md'
        self.version_pattern = r'^v?\d+\.\d+\.\d+(-rc\d+)?$'
    
    def create_release(self, version: str, auto_deploy: bool = False, release_candidate: bool = False) -> bool:
        """Create a new release."""
        print(f"🚀 Creating release {version}...")
        
        # Validate version format
        if not self._validate_version(version):
            print(f"❌ Invalid version format: {version}")
            return False
        
        # Ensure version starts with 'v'
        if not version.startswith('v'):
            version = f'v{version}'
        
        # Create release session log
        self._create_release_session(version)
        
        try:
            # 1. Update version files
            print("📝 Updating version files...")
            self._update_version_files(version)
            
            # 2. Generate changelog
            print("📋 Generating changelog...")
            self._generate_changelog(version)
            
            # 3. Create release branch
            print("🌿 Creating release branch...")
            release_branch = f'release/{version}'
            subprocess.run(['git', 'checkout', '-b', release_branch], check=True, capture_output=True)
            
            # 4. Commit changes
            print("💾 Committing release changes...")
            self._commit_release_changes(version)
            
            # 5. Create and push tag
            print("🏷️  Creating and pushing tag...")
            self._create_and_push_tag(version)
            
            # 6. Push release branch
            print("📤 Pushing release branch...")
            subprocess.run(['git', 'push', 'origin', release_branch], check=True, capture_output=True)
            
            # 7. Create GitHub Release
            print("🌐 Creating GitHub release...")
            self._create_github_release(version)
            
            # 8. Auto-deploy if requested
            if auto_deploy:
                print("🚀 Auto-deploying release...")
                self._auto_deploy(version)
            
            print(f"✅ Release {version} created successfully!")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error creating release: {e}")
            return False
    
    def _validate_version(self, version: str) -> bool:
        """Validate version format."""
        import re
        version = version.lstrip('v')
        return bool(re.match(r'^\d+\.\d+\.\d+(-rc\d+)?$', version))
    
    def _create_release_session(self, version: str):
        """Create release session log."""
        try:
            sys.path.append(str(self.base_dir / 'scripts'))
            from create_session_log import SessionLogger
            
            logger = SessionLogger(self.base_dir)
            session_data = logger.create_session_log("release")
            
            # Add release-specific data
            session_data['release_version'] = version
            session_data['release_type'] = 'release'
            
            # Update session files with release info
            timestamp = datetime.now().strftime('%Y-%m-%d')
            session_id = session_data['session_id'][-6:]
            
            log_file = logger.sessions_dir / f"{timestamp}_session-{session_id}.log"
            json_file = logger.sessions_dir / f"{timestamp}_session-{session_id}.json"
            
            # Append release info to log file
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"\n\nRelease Information:\n")
                f.write(f"- Version: {version}\n")
                f.write(f"- Type: Production Release\n")
                f.write(f"- Timestamp: {datetime.now().isoformat()}\n")
            
            # Update JSON file
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)
                
        except ImportError:
            print("⚠️  Could not create release session log")
    
    def _update_version_files(self, version: str):
        """Update version in configuration files."""
        version_clean = version.lstrip('v')
        
        # Update pyproject.toml
        pyproject_path = self.base_dir / 'pyproject.toml'
        if pyproject_path.exists():
            content = pyproject_path.read_text()
            # Simple version replacement
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('version = '):
                    lines[i] = f'version = "{version_clean}"'
                    break
            pyproject_path.write_text('\n'.join(lines))
        
        # Update README.md
        readme_path = self.base_dir / 'README.md'
        if readme_path.exists():
            content = readme_path.read_text()
            # Update version mentions
            content = content.replace(
                '## Version',
                f'## Version\n\nCurrent version: {version}'
            )
            readme_path.write_text(content)
        
        # Update __init__.py files
        for init_file in self.base_dir.rglob('__init__.py'):
            content = init_file.read_text()
            if '__version__' in content:
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if line.strip().startswith('__version__'):
                        lines[i] = f'__version__ = "{version_clean}"'
                        break
                init_file.write_text('\n'.join(lines))
    
    def _generate_changelog(self, version: str):
        """Generate changelog for the release."""
        # Get commits since last release
        try:
            # Get last release tag
            result = subprocess.run(
                ['git', 'describe', '--tags', '--abbrev=0'],
                capture_output=True, text=True, check=True
            )
            last_tag = result.stdout.strip()
        except subprocess.CalledProcessError:
            last_tag = None
        
        # Get commits
        if last_tag:
            result = subprocess.run(
                ['git', 'log', f'{last_tag}..HEAD', '--oneline', '--grep=feat:', '--grep=fix:', '--grep=chore:'],
                capture_output=True, text=True, check=True
            )
        else:
            result = subprocess.run(
                ['git', 'log', 'HEAD', '--oneline', '--grep=feat:', '--grep=fix:', '--grep=chore:'],
                capture_output=True, text=True, check=True
            )
        
        commits = result.stdout.strip().split('\n')
        
        # Categorize commits
        features = []
        fixes = []
        chores = []
        
        for commit in commits:
            if not commit.strip():
                continue
            if 'feat:' in commit:
                features.append(commit)
            elif 'fix:' in commit:
                fixes.append(commit)
            elif 'chore:' in commit:
                chores.append(commit)
        
        # Generate changelog entry
        changelog_entry = f"""
## [{datetime.now().strftime('%Y-%m-%d')}] - {version}

### Added
{chr(10).join(f"- {feat}" for feat in features) if features else "- No new features"}

### Fixed
{chr(10).join(f"- {fix}" for fix in fixes) if fixes else "- No bug fixes"}

### Changed
{chr(10).join(f"- {chore}" for chore in chores) if chores else "- No changes"}

"""
        
        # Update changelog file
        if self.changelog_path.exists():
            content = self.changelog_path.read_text()
            # Insert after the first header
            lines = content.split('\n')
            insert_index = 0
            for i, line in enumerate(lines):
                if line.startswith('## [Unreleased]'):
                    insert_index = i + 2
                    break
            
            lines.insert(insert_index, changelog_entry)
            self.changelog_path.write_text('\n'.join(lines))
        else:
            # Create new changelog
            changelog_content = f"""# AI Lab Framework Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

{changelog_entry}
"""
            self.changelog_path.parent.mkdir(parents=True, exist_ok=True)
            self.changelog_path.write_text(changelog_content)
    
    def _commit_release_changes(self, version: str):
        """Commit release changes."""
        subprocess.run(['git', 'add', '.'], check=True, capture_output=True)
        subprocess.run([
            'git', 'commit', '-m', f'chore: Prepare release {version}

- Update version to {version}
- Generate changelog
- Update documentation

Release: {version}'
        ], check=True, capture_output=True)
    
    def _create_and_push_tag(self, version: str):
        """Create and push git tag."""
        tag_message = f"Release {version}\n\nAutomated release creation.\nTimestamp: {datetime.now().isoformat()}"
        subprocess.run(['git', 'tag', '-a', version, '-m', tag_message], check=True, capture_output=True)
        subprocess.run(['git', 'push', 'origin', version], check=True, capture_output=True)
    
    def _create_github_release(self, version: str):
        """Create GitHub release using gh CLI."""
        try:
            # Get changelog for this release
            changelog_content = self._get_release_changelog(version)
            
            # Create GitHub release
            cmd = [
                'gh', 'release', 'create', version,
                '--title', f'Release {version}',
                '--notes', changelog_content
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️  Could not create GitHub release (gh CLI not available)")
    
    def _get_release_changelog(self, version: str) -> str:
        """Get changelog content for the release."""
        if self.changelog_path.exists():
            content = self.changelog_path.read_text()
            lines = content.split('\n')
            
            # Find the changelog entry for this version
            start_index = None
            end_index = None
            
            for i, line in enumerate(lines):
                if version in line and line.startswith('## ['):
                    start_index = i
                elif start_index is not None and line.startswith('## [') and version not in line:
                    end_index = i
                    break
            
            if start_index is not None:
                if end_index is None:
                    end_index = len(lines)
                
                return '\n'.join(lines[start_index:end_index])
        
        return f"Release {version}\n\nAutomated release creation."
    
    def _auto_deploy(self, version: str):
        """Auto-deploy release to all repositories."""
        try:
            # Import and use deploy_framework
            sys.path.append(str(self.base_dir / 'scripts'))
            from deploy_framework import FrameworkDeployer
            
            deployer = FrameworkDeployer(self.base_dir)
            success = deployer.deploy_version(version)
            
            if success:
                print(f"✅ Auto-deploy of {version} completed")
            else:
                print(f"⚠️  Auto-deploy of {version} failed")
                
        except ImportError:
            print("⚠️  Could not auto-deploy (deploy_framework.py not available)")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Create AI Lab Framework release")
    
    parser.add_argument('--version', required=True, help='Release version (e.g., v1.2.0)')
    parser.add_argument('--auto-deploy', action='store_true', help='Auto-deploy after release')
    parser.add_argument('--release-candidate', action='store_true', help='Create release candidate')
    parser.add_argument('--base-dir', type=Path, help='Base directory (default: current)')
    
    args = parser.parse_args()
    
    manager = ReleaseManager(args.base_dir)
    
    success = manager.create_release(
        args.version,
        args.auto_deploy,
        args.release_candidate
    )
    
    if success:
        print(f"\n🎉 Release {args.version} completed successfully!")
        sys.exit(0)
    else:
        print(f"\n❌ Release {args.version} failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()