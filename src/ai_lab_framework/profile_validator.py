"""
AI Lab Framework - Profile Validator

Automatische Validierung von KI-Tool-Integrationen gegen Profil-Anforderungen.
"""

import ast
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class ProfileType(Enum):
    EXPERIMENTAL = "experimental"
    STANDARD = "standard"
    PRODUCTION = "production"


@dataclass
class ValidationResult:
    profile: ProfileType
    compliant: bool
    violations: list[str]
    suggestions: list[str]


class ProfileValidator:
    """Validiert KI-Tools gegen Profil-Anforderungen"""

    def __init__(self):
        self.requirements = {
            ProfileType.EXPERIMENTAL: {
                "logging": ["basic", "print"],
                "error_handling": ["try_except", "graceful"],
                "testing": ["manual", "optional"],
                "documentation": ["optional"],
            },
            ProfileType.STANDARD: {
                "logging": ["structured", "logger", "correlation_id"],
                "error_handling": ["comprehensive", "recovery", "circuit_breaker"],
                "testing": ["automated", "pytest", "coverage"],
                "documentation": ["docstring", "readme", "required"],
            },
            ProfileType.PRODUCTION: {
                "logging": ["enterprise", "monitoring", "prometheus"],
                "error_handling": ["circuit_breaker", "fallback", "sla"],
                "testing": ["load_test", "performance", "security"],
                "documentation": ["enterprise", "api_docs", "security"],
                "security": ["zero_trust", "validation", "audit"],
            },
        }

    def validate_file(self, file_path: Path) -> ValidationResult:
        """Validiert eine Python-Datei gegen Profil-Anforderungen"""

        # Profil aus Datei-Inhalt erkennen
        profile = self._detect_profile(file_path)

        # Datei analysieren
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        tree = ast.parse(content)

        violations = []
        suggestions = []

        # Logging-Checks
        logging_violations = self._check_logging(tree, profile)
        violations.extend(logging_violations)

        # Error Handling-Checks
        error_violations = self._check_error_handling(tree, profile)
        violations.extend(error_violations)

        # Documentation-Checks
        doc_violations = self._check_documentation(tree, profile)
        violations.extend(doc_violations)

        # Testing-Checks
        test_violations = self._check_testing(file_path, profile)
        violations.extend(test_violations)

        # Suggestions generieren
        suggestions = self._generate_suggestions(violations, profile)

        compliant = len(violations) == 0

        return ValidationResult(
            profile=profile,
            compliant=compliant,
            violations=violations,
            suggestions=suggestions,
        )

    def _detect_profile(self, file_path: Path) -> ProfileType:
        """Erkennt Profil aus Datei-Inhalt oder Pfad"""

        # Aus Datei-Inhalt lesen
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read().lower()

            if "experimentalprofile" in content or "prototype" in content:
                return ProfileType.EXPERIMENTAL
            elif "productionprofile" in content or "enterprise" in content:
                return ProfileType.PRODUCTION
            else:
                return ProfileType.STANDARD  # Default

        except Exception:
            return ProfileType.STANDARD  # Default bei Fehlern

    def _check_logging(self, tree: ast.AST, profile: ProfileType) -> list[str]:
        """Prüft Logging-Anforderungen"""
        violations = []

        self.requirements[profile]["logging"]

        # Nach Logging-Imports suchen
        has_logging = False
        has_structured_logging = False

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if "logging" in alias.name or "structlog" in alias.name:
                        has_logging = True
                        if "structlog" in alias.name:
                            has_structured_logging = True

            elif isinstance(node, ast.ImportFrom):
                if node.module and (
                    "logging" in node.module or "structlog" in node.module
                ):
                    has_logging = True
                    if "structlog" in node.module:
                        has_structured_logging = True

        # Validierung je nach Profil
        if profile == ProfileType.EXPERIMENTAL:
            # Basic logging ausreichend (print oder basic logging)
            pass  # Keine spezifischen Anforderungen

        elif profile == ProfileType.STANDARD:
            if not has_logging:
                violations.append("Standard-Profile erfordert strukturiertes Logging")
            elif not has_structured_logging:
                violations.append(
                    "Standard-Profile empfiehlt structlog für strukturiertes Logging"
                )

        elif profile == ProfileType.PRODUCTION:
            if not has_structured_logging:
                violations.append(
                    "Production-Profile erfordert enterprise-grade Logging (structlog)"
                )

        return violations

    def _check_error_handling(self, tree: ast.AST, profile: ProfileType) -> list[str]:
        """Prüft Error Handling-Anforderungen"""
        violations = []

        # Nach try/except Blöcken suchen
        try_blocks = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Try):
                try_blocks.append(node)

        if profile in [ProfileType.STANDARD, ProfileType.PRODUCTION]:
            if len(try_blocks) == 0:
                violations.append(
                    f"{profile.value.title()}-Profile erfordert umfassendes Error Handling"
                )

        return violations

    def _check_documentation(self, tree: ast.AST, profile: ProfileType) -> list[str]:
        """Prüft Dokumentations-Anforderungen"""
        violations = []

        # Nach Klassen und Funktionen mit Docstrings suchen
        classes_without_docs = []
        functions_without_docs = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if not ast.get_docstring(node):
                    classes_without_docs.append(node.name)
            elif isinstance(node, ast.FunctionDef):
                if not ast.get_docstring(node):
                    functions_without_docs.append(node.name)

        if profile in [ProfileType.STANDARD, ProfileType.PRODUCTION]:
            if classes_without_docs:
                violations.append(
                    f"Klassen ohne Docstrings: {', '.join(classes_without_docs)}"
                )
            if functions_without_docs:
                violations.append(
                    f"Funktionen ohne Docstrings: {', '.join(functions_without_docs[:3])}..."
                )

        return violations

    def _check_testing(self, file_path: Path, profile: ProfileType) -> list[str]:
        """Prüft Test-Anforderungen"""
        violations = []

        # Nach Test-Dateien suchen
        test_file = file_path.parent / f"test_{file_path.name}"
        if not test_file.exists():
            test_file = file_path.parent / f"{file_path.stem}_test.py"

        if profile in [ProfileType.STANDARD, ProfileType.PRODUCTION]:
            if not test_file.exists():
                violations.append(
                    f"{profile.value.title()}-Profile erfordert automatisierte Tests (fehlend: {test_file.name})"
                )

        return violations

    def _generate_suggestions(
        self, violations: list[str], profile: ProfileType
    ) -> list[str]:
        """Generiert Verbesserungsvorschläge"""
        suggestions = []

        if any("logging" in v.lower() for v in violations):
            suggestions.append(f"Logging für {profile.value} Profile implementieren:")
            if profile == ProfileType.STANDARD:
                suggestions.append("  - import structlog")
                suggestions.append("  - logger = structlog.get_logger()")
            elif profile == ProfileType.PRODUCTION:
                suggestions.append("  - Enterprise Logging mit Monitoring")

        if any("error" in v.lower() for v in violations):
            suggestions.append("Error Handling verbessern:")
            suggestions.append("  - try/except Blöcke hinzufügen")
            suggestions.append("  - Recovery-Mechanismen implementieren")

        if any(
            "docstring" in v.lower() or "documentation" in v.lower() for v in violations
        ):
            suggestions.append("Dokumentation ergänzen:")
            suggestions.append("  - Docstrings für Klassen und Funktionen")
            suggestions.append("  - README.md mit Nutzungshinweisen")

        if any("test" in v.lower() for v in violations):
            suggestions.append("Tests implementieren:")
            suggestions.append("  - pytest Tests erstellen")
            suggestions.append("  - Coverage >80% anstreben")

        return suggestions


def main():
    """CLI-Interface für Profile-Validierung"""
    import sys

    if len(sys.argv) != 2:
        print("Usage: python profile_validator.py <file_path>")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"File not found: {file_path}")
        sys.exit(1)

    validator = ProfileValidator()
    result = validator.validate_file(file_path)

    print(f"\n🔍 Profile Validation: {file_path.name}")
    print(f"📋 Detected Profile: {result.profile.value.title()}")
    print(f"✅ Compliant: {'Yes' if result.compliant else 'No'}")

    if result.violations:
        print(f"\n❌ Violations ({len(result.violations)}):")
        for violation in result.violations:
            print(f"  • {violation}")

    if result.suggestions:
        print("\n💡 Suggestions:")
        for suggestion in result.suggestions:
            print(f"  {suggestion}")

    # Exit-Code für CI/CD
    sys.exit(0 if result.compliant else 1)


if __name__ == "__main__":
    main()
