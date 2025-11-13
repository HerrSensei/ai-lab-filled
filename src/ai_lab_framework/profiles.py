"""
AI Lab Framework - Profile Definitions

Definiert die verschiedenen Integrations-Profile für KI-Tools.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any


class ProfileType(Enum):
    EXPERIMENTAL = "experimental"
    STANDARD = "standard"
    PRODUCTION = "production"


@dataclass
class ProfileRequirements:
    """Anforderungen für ein spezifisches Profil"""

    logging: str
    context_management: str
    error_handling: str
    testing: str
    documentation: str
    validation: str = "runtime_only"


class ExperimentalProfile:
    """Experimentelles Profil für schnelle Prototypen"""

    requirements = ProfileRequirements(
        logging="basic",
        context_management="minimal",
        error_handling="graceful_degradation",
        testing="manual_only",
        documentation="optional",
        validation="runtime_only",
    )

    def setup(self):
        """Minimal setup - keine komplexen Abhängigkeiten"""
        return {"type": "basic_logger"}


class StandardProfile:
    """Standard-Profil für produktive Tools"""

    requirements = ProfileRequirements(
        logging="structured_with_correlation_ids",
        context_management="full_with_persistence",
        error_handling="comprehensive_with_recovery",
        testing="automated_with_coverage",
        documentation="required",
        validation="automated_compliance",
    )

    def setup(self):
        """Standard setup mit voller Funktionalität"""
        return {
            "type": "structured_logger",
            "correlation_ids": True,
            "persistence": True,
            "recovery": True,
        }


class ProductionProfile:
    """Produktions-Profil für kritische Systeme"""

    requirements = ProfileRequirements(
        logging="enterprise_grade_with_monitoring",
        context_management="distributed_with_caching",
        error_handling="circuit_breaker_with_fallbacks",
        testing="comprehensive_with_load_testing",
        documentation="enterprise_standard",
        validation="multi_layer_security",
    )

    def setup(self):
        """Enterprise setup mit allen Features"""
        return {
            "type": "enterprise_logger",
            "monitoring": True,
            "caching": True,
            "circuit_breaker": True,
            "security": "zero_trust",
        }


def get_profile(profile_type: ProfileType):
    """Factory-Funktion für Profile"""
    if profile_type == ProfileType.EXPERIMENTAL:
        return ExperimentalProfile()
    elif profile_type == ProfileType.STANDARD:
        return StandardProfile()
    elif profile_type == ProfileType.PRODUCTION:
        return ProductionProfile()
    else:
        raise ValueError(f"Unknown profile type: {profile_type}")


def detect_profile(context: dict[str, Any]) -> ProfileType:
    """
    Automatische Profil-Erkennung basierend auf Kontext
    """
    if context.get("prototype", False) or context.get("experimental", False):
        return ProfileType.EXPERIMENTAL

    if (
        context.get("critical", False)
        or context.get("external_users", False)
        or context.get("enterprise", False)
    ):
        return ProfileType.PRODUCTION

    return ProfileType.STANDARD  # Default
