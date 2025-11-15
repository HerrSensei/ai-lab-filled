#!/usr/bin/env python3
"""
GitHub PAT Security Checker - Fixed Version
Fixed repository validation logic
"""

import os
import sys
import requests
import subprocess
import json
from pathlib import Path


class GitHubPATSecurityChecker:
    """Validates GitHub PAT security setup"""

    def __init__(self):
        self.github_api_url = "https://api.github.com"

    def check_token_from_env(self) -> bool:
        """Check if token is properly set in environment"""
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            print("❌ GITHUB_TOKEN nicht in Environment gefunden")
            return False

        if len(token) < 20:
            print("❌ Token scheint zu kurz zu sein")
            return False

        print(f"✅ Token in Environment gefunden (Länge: {len(token)})")
        return True

    def check_repo_from_env(self) -> bool:
        """Check if repository is properly set in environment"""
        repo = os.getenv("GITHUB_REPO")
        if not repo:
            print("❌ GITHUB_REPO nicht in Environment gefunden")
            return False

        if "/" not in repo:
            print("❌ Repository Format sollte 'owner/repo' sein")
            return False

        print(f"✅ Repository in Environment gefunden: {repo}")
        return True

    def test_token_permissions(self) -> bool:
        """Test token permissions against GitHub API"""
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            return False

        try:
            headers = {"Authorization": f"token {token}"}

            # Test basic authentication
            response = requests.get(f"{self.github_api_url}/user", headers=headers)
            if response.status_code != 200:
                print(
                    f"❌ Token Authentifizierung fehlgeschlagen: {response.status_code}"
                )
                return False

            user_data = response.json()
            print(f"✅ Token authentifiziert als: {user_data.get('login')}")

            # Test repository access
            repo = os.getenv("GITHUB_REPO")
            if repo:
                response = requests.get(
                    f"{self.github_api_url}/repos/{repo}", headers=headers
                )

                # Check if response is successful
                if response.status_code == 200:
                    repo_data = response.json()
                    print(f"✅ Repository-Zugriff bestätigt: {repo}")

                    # Check if repository has issues enabled
                    if not repo_data.get("has_issues", False):
                        print("⚠️  Repository hat Issues deaktiviert")
                        return False

                    # Check if repository is accessible
                    if repo_data.get("private", False) and repo_data.get(
                        "permissions", {}
                    ).get("admin", False):
                        print("✅ Private Repository mit Admin-Rechten")
                    elif not repo_data.get("private", False):
                        print("✅ Public Repository")
                    else:
                        print("❌ Unzureichende Berechtigungen für privates Repository")
                        return False

                    print(f"   Repository Größe: {repo_data.get('size', 0)} KB")
                    print(f"   Issues aktiviert: {repo_data.get('has_issues', False)}")
                    print(
                        f"   Projects aktiviert: {repo_data.get('has_projects', False)}"
                    )

                elif response.status_code == 404:
                    print(f"❌ Repository nicht gefunden: {repo}")
                    print("   Mögliche Ursachen:")
                    print("   - Repository existiert nicht")
                    print("   - Falscher Repository-Name")
                    print("   - Keine Berechtigung für privates Repository")
                    return False
                else:
                    print(
                        f"❌ Repository-Zugriff fehlgeschlagen: {response.status_code}"
                    )
                    return False

            # Test permissions scope
            response = requests.get(f"{self.github_api_url}/user", headers=headers)
            auth_header = response.headers.get("X-OAuth-Scopes", "")
            scopes = auth_header.split(", ") if auth_header else []

            required_scopes = ["repo", "issues", "projects"]
            missing_scopes = [scope for scope in required_scopes if scope not in scopes]

            if missing_scopes:
                print(f"❌ Fehlende Scopes: {missing_scopes}")
                print(f"   Aktuelle Scopes: {scopes}")
                return False

            print(f"✅ Alle erforderlichen Scopes vorhanden: {scopes}")
            return True

        except requests.exceptions.RequestException as e:
            print(f"❌ Netzwerkfehler bei Token-Test: {e}")
            return False

    def check_gitignore_security(self) -> bool:
        """Check if .gitignore properly excludes sensitive files"""
        project_root = Path.cwd()
        gitignore_path = project_root / ".gitignore"

        if not gitignore_path.exists():
            print("❌ .gitignore nicht gefunden")
            return False

        with open(gitignore_path, "r") as f:
            gitignore_content = f.read()

        required_entries = [".env", "*.token", "GITHUB_TOKEN"]
        missing_entries = []

        for entry in required_entries:
            if entry not in gitignore_content:
                missing_entries.append(entry)

        if missing_entries:
            print(f"❌ Fehlende .gitignore Einträge: {missing_entries}")
            return False

        print("✅ .gitignore enthält alle erforderlichen Sicherheitseinträge")
        return True

    def check_env_file_security(self) -> bool:
        """Check if .env file exists and is properly secured"""
        project_root = Path.cwd()
        env_path = project_root / ".env"

        if not env_path.exists():
            print("⚠️  .env Datei nicht gefunden (verwende Environment Variablen)")
            return True

        # Check file permissions
        stat_info = env_path.stat()
        mode = oct(stat_info.st_mode)[-3:]

        if mode != "600":
            print(f"⚠️  .env Datei hat unsichere Berechtigungen: {mode}")
            print("   Empfohlen: chmod 600 .env")
            return False

        print("✅ .env Datei hat sichere Berechtigungen")
        return True

    def check_for_hardcoded_tokens(self) -> bool:
        """Check for hardcoded tokens in project files"""
        project_root = Path.cwd()
        suspicious_patterns = ["ghp_", "github_pat_", "GITHUB_TOKEN="]

        # Files to check
        files_to_check = []
        for pattern in ["*.py", "*.sh", "*.md", "*.json", "*.yaml", "*.yml"]:
            files_to_check.extend(project_root.rglob(pattern))

        found_issues = []

        for file_path in files_to_check:
            if ".git" in str(file_path) or "venv" in str(file_path):
                continue

            # Skip our own security files
            if file_path.name in ["github_pat_security.py", "setup_github_pat.sh"]:
                continue

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                for pattern in suspicious_patterns:
                    if pattern in content:
                        found_issues.append(f"{file_path}: enthält '{pattern}'")

            except Exception:
                continue

        if found_issues:
            print("❌ Potenziell hardcodierte Tokens gefunden:")
            for issue in found_issues:
                print(f"   {issue}")
            return False

        print("✅ Keine hardcodierten Tokens gefunden")
        return True

    def run_security_check(self) -> bool:
        """Run complete security check"""
        print("🔐 GitHub PAT Security Check")
        print("=" * 40)

        checks = [
            ("Environment Token", self.check_token_from_env),
            ("Environment Repository", self.check_repo_from_env),
            ("Token Permissions", self.test_token_permissions),
            ("Gitignore Security", self.check_gitignore_security),
            ("Env File Security", self.check_env_file_security),
            ("Hardcoded Tokens", self.check_for_hardcoded_tokens),
        ]

        results = []
        for check_name, check_func in checks:
            print(f"\n🔍 Prüfe: {check_name}")
            try:
                result = check_func()
                results.append(result)
            except Exception as e:
                print(f"❌ Fehler bei {check_name}: {e}")
                results.append(False)

        print(f"\n📊 Security Check Ergebnis:")
        passed = sum(results)
        total = len(results)
        print(f"   Bestanden: {passed}/{total}")

        if passed == total:
            print("🎉 Alle Sicherheitstests bestanden!")
            return True
        else:
            print("⚠️  Einige Sicherheitstests fehlgeschlagen")
            return False

    def generate_secure_config(self) -> str:
        """Generate secure configuration template"""
        return f"""
# GitHub PAT Configuration Template
# Kopiere diese Datei als .env und fülle die Werte ein

# GitHub Personal Access Token
GITHUB_TOKEN=dein_token_hier

# GitHub Repository (owner/repo)
GITHUB_REPO=dein_username/dein_repo

# Optional: GitHub API URL (nur für Enterprise)
# GITHUB_API_URL=https://api.github.com

# Optional: Sync Intervall in Minuten
# SYNC_INTERVAL=30

# Optional: Rate Limiting
# GITHUB_RATE_LIMIT=5000

# Sicherheitshinweise:
# 1. Teile diese Datei mit niemandem
# 2. Füge .env zu .gitignore hinzu
# 3. Rotiere den Token regelmäßig
# 4. Verwende minimale Berechtigungen
"""


def main():
    """Main security checker function"""
    import argparse

    parser = argparse.ArgumentParser(description="GitHub PAT Security Checker")
    parser.add_argument(
        "--generate-config", action="store_true", help="Generate secure .env template"
    )
    parser.add_argument(
        "--check", action="store_true", default=True, help="Run security check"
    )

    args = parser.parse_args()

    checker = GitHubPATSecurityChecker()

    if args.generate_config:
        config = checker.generate_secure_config()
        print(config)

        # Save to .env.template
        with open(".env.template", "w") as f:
            f.write(config)
        print("✅ .env.template erstellt")

    if args.check:
        success = checker.run_security_check()
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
