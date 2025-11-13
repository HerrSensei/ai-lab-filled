#!/usr/bin/env python3
"""
AI Lab Framework - Tool Generator CLI

Assistent für schnelle Erstellung von KI-Tools mit verschiedenen Profilen.
"""

import argparse
import sys
from pathlib import Path


class ToolGenerator:
    """Generator für KI-Tool Templates"""

    def __init__(self):
        self.templates = {
            "experimental": self._get_experimental_template(),
            "standard": self._get_standard_template(),
            "production": self._get_production_template(),
        }

    def generate_tool(self, name: str, profile: str, output_dir: Path = None):
        """Generiert ein neues KI-Tool"""

        if profile not in self.templates:
            raise ValueError(
                f"Unknown profile: {profile}. Available: {list(self.templates.keys())}"
            )

        if output_dir is None:
            output_dir = Path.cwd()

        # Dateinamen generieren
        tool_file = output_dir / f"{name.lower().replace('-', '_')}_tool.py"
        test_file = output_dir / f"test_{name.lower().replace('-', '_')}_tool.py"
        readme_file = output_dir / f"{name.lower().replace('-', '_')}_README.md"

        # Tool-Datei erstellen
        template = self.templates[profile]
        class_name = name.title().replace("-", "").replace("_", "")
        tool_content = template.format(
            name=name,
            class_name=f"{class_name}Tool",
            description=f"Generated {profile} AI tool: {name}",
        )

        with open(tool_file, "w") as f:
            f.write(tool_content)

        # Test-Datei erstellen (für Standard/Production)
        if profile in ["standard", "production"]:
            test_content = self._get_test_template().format(
                name=name,
                class_name=f"{name.title()}Tool",
                import_path=f"{name.lower()}_tool",
            )

            with open(test_file, "w") as f:
                f.write(test_content)

        # README erstellen
        readme_content = self._get_readme_template().format(
            name=name,
            class_name=f"{name.title()}Tool",
            profile=profile,
            description=f"Generated {profile} AI tool: {name}",
        )

        with open(readme_file, "w") as f:
            f.write(readme_content)

        print(f"✅ Generated {profile.title()} AI Tool: {name}")
        print("📁 Files created:")
        print(f"   • {tool_file}")
        if profile in ["standard", "production"]:
            print(f"   • {test_file}")
        print(f"   • {readme_file}")

        # Nächste Schritte
        print("\n🚀 Next steps:")
        print(f"   1. Edit {tool_file} and implement the process() method")
        if profile in ["standard", "production"]:
            print(f"   2. Run tests: python -m pytest {test_file}")
        print(f"   3. Test your tool: python {tool_file}")

    def _get_experimental_template(self) -> str:
        """Template für experimentelle Tools"""
        return '''"""
{description}

Experimentelles KI-Tool mit minimalem Setup.
"""

import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from ai_lab_framework.base_ai_tool import ExperimentalAITool, ToolContext


class {class_name}(ExperimentalAITool):
    """
    Experimentelles KI-Tool für schnelle Prototypen.
    """

    def __init__(self, config=None):
        super().__init__(config)
        self.name = "{name}"

    async def process(self, input_data, context: ToolContext):
        """
        Tool-spezifische Verarbeitungslogik.

        Args:
            input_data: Die zu verarbeitenden Daten
            context: Der Ausführungskontext

        Returns:
            Verarbeitete Daten
        """
        # TODO: Implementiere deine Logik hier
        print(f"Processing: {{input_data}}")

        # Beispiel-Implementierung
        if isinstance(input_data, str):
            result = f"Processed: {{input_data.upper()}}"
        else:
            result = f"Processed: {{str(input_data)}}"

        return result


async def main():
    """Beispiel-Nutzung des Tools"""
    tool = {class_name}()

    # Führe Tool aus
    result = await tool.execute("test input")

    print(f"Success: {{result.success}}")
    print(f"Data: {{result.data}}")
    print(f"Execution Time: {{result.execution_time}}s")


if __name__ == "__main__":
    asyncio.run(main())
'''

    def _get_standard_template(self) -> str:
        """Template für Standard-Tools"""
        return '''"""
{description}

Standard KI-Tool mit vollem Framework-Support.
"""

import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from ai_lab_framework.base_ai_tool import StandardAITool, ToolContext


class {class_name}(StandardAITool):
    """
    Standard KI-Tool mit umfassendem Logging und Error Handling.
    """

    def __init__(self, config=None):
        super().__init__(config)
        self.name = "{name}"

    async def process(self, input_data, context: ToolContext):
        """
        Tool-spezifische Verarbeitungslogik.

        Args:
            input_data: Die zu verarbeitenden Daten
            context: Der Ausführungskontext

        Returns:
            Verarbeitete Daten

        Raises:
            ValueError: Bei ungültigen Eingabedaten
            ProcessingError: Bei Verarbeitungsfehlern
        """
        # Input-Validierung
        if not input_data:
            raise ValueError("Input data cannot be empty")

        # TODO: Implementiere deine Logik hier
        try:
            # Beispiel-Implementierung
            if isinstance(input_data, str):
                result = {{
                    "original": input_data,
                    "processed": input_data.upper(),
                    "length": len(input_data),
                    "context_id": context.correlation_id
                }}
            elif isinstance(input_data, dict):
                result = {{k.upper(): v for k, v in input_data.items()}}
            else:
                result = {{"processed": str(input_data)}}

            # Simuliere Verarbeitung
            await asyncio.sleep(0.1)

            return result

        except Exception as e:
            # Fehler werden vom Framework automatisch geloggt
            raise


async def main():
    """Beispiel-Nutzung des Tools"""
    tool = {class_name}()

    # Führe Tool aus
    result = await tool.execute("hello world")

    print(f"Success: {{result.success}}")
    print(f"Data: {{result.data}}")
    print(f"Execution Time: {{result.execution_time}}s")
    print(f"Session ID: {{result.context.session_id}}")


if __name__ == "__main__":
    asyncio.run(main())
'''

    def _get_production_template(self) -> str:
        """Template für Production-Tools"""
        return '''"""
{description}

Production KI-Tool mit Enterprise-Anforderungen.
"""

import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from ai_lab_framework.base_ai_tool import ProductionAITool, ToolContext


class {class_name}(ProductionAITool):
    """
    Production KI-Tool mit Enterprise-Security und Monitoring.
    """

    def __init__(self, config=None):
        super().__init__(config)
        self.name = "{name}"

        # Production-spezifische Initialisierung
        self._validate_config()
        self._setup_monitoring()

    def _validate_config(self):
        """Validiert Production-Konfiguration"""
        required_keys = ["api_key", "endpoint", "timeout"]
        for key in required_keys:
            if key not in self.config:
                raise ValueError(f"Missing required config key: {{key}}")

    def _setup_monitoring(self):
        """Richtet Monitoring ein"""
        # TODO: Implementiere Prometheus-Metrics
        pass

    async def process(self, input_data, context: ToolContext):
        """
        Tool-spezifische Verarbeitungslogik mit Enterprise-Security.

        Args:
            input_data: Die zu verarbeitenden Daten
            context: Der Ausführungskontext

        Returns:
            Verarbeitete Daten

        Raises:
            SecurityError: Bei Sicherheitsverletzungen
            ValidationError: Bei Validierungsfehlern
            ProcessingError: Bei Verarbeitungsfehlern
        """
        # Security-Checks
        await self._security_check(input_data, context)

        # Input-Validierung
        validated_data = await self._validate_input(input_data)

        # Processing mit Monitoring
        with self._monitoring_context():
            result = await self._process_with_circuit_breaker(validated_data, context)

        # Output-Sanitization
        return await self._sanitize_output(result)

    async def _security_check(self, input_data, context: ToolContext):
        """Security-Validierung"""
        # TODO: Implementiere Security-Checks
        if not context.user_id:
            raise SecurityError("User authentication required")

    async def _validate_input(self, input_data):
        """Input-Validierung"""
        if not input_data:
            raise ValidationError("Input data cannot be empty")
        return input_data

    def _monitoring_context(self):
        """Monitoring-Context Manager"""
        # TODO: Implementiere Monitoring-Context
        return self

    async def _process_with_circuit_breaker(self, validated_data, context: ToolContext):
        """Verarbeitung mit Circuit Breaker"""
        # TODO: Implementiere Circuit Breaker Logik

        # Beispiel-Implementierung
        if isinstance(validated_data, str):
            result = {{
                "original": validated_data,
                "processed": validated_data.upper(),
                "timestamp": context.start_time.isoformat(),
                "user_id": context.user_id,
                "security_level": "enterprise"
            }}
        else:
            result = {{"processed": str(validated_data)}}

        await asyncio.sleep(0.1)
        return result

    async def _sanitize_output(self, result):
        """Output-Sanitization"""
        # TODO: Implementiere Output-Sanitization
        return result


class SecurityError(Exception):
    """Security-related errors"""
    pass


class ValidationError(Exception):
    """Validation-related errors"""
    pass


async def main():
    """Beispiel-Nutzung des Tools"""
    config = {{
        "api_key": "your-api-key",
        "endpoint": "https://api.example.com",
        "timeout": 30
    }}

    tool = {class_name}(config)

    # Führe Tool aus
    result = await tool.execute("test input", user_id="test-user")

    print(f"Success: {{result.success}}")
    print(f"Data: {{result.data}}")
    print(f"Execution Time: {{result.execution_time}}s")


if __name__ == "__main__":
    asyncio.run(main())
'''

    def _get_test_template(self) -> str:
        """Template für Test-Dateien"""
        return '''"""
Tests für {class_name}
"""

import pytest
import asyncio
import sys
import os
sys.path.append(os.path.dirname(__file__))

from {import_path} import {class_name}


class Test{class_name}:
    """Test-Suite für {class_name}"""

    @pytest.fixture
    def tool(self):
        """Fixture für Tool-Instanz"""
        return {class_name}()

    @pytest.mark.asyncio
    async def test_successful_execution(self, tool):
        """Test für erfolgreiche Ausführung"""
        result = await tool.execute("test input")

        assert result.success is True
        assert result.data is not None
        assert result.execution_time > 0
        assert result.context is not None

    @pytest.mark.asyncio
    async def test_empty_input(self, tool):
        """Test für leere Eingabe"""
        result = await tool.execute("")

        # Sollte fehlschlagen bei leerer Eingabe
        assert result.success is False
        assert "empty" in result.error.lower()

    @pytest.mark.asyncio
    async def test_string_processing(self, tool):
        """Test für String-Verarbeitung"""
        test_input = "hello world"
        result = await tool.execute(test_input)

        assert result.success is True
        assert "processed" in str(result.data).lower()

    @pytest.mark.asyncio
    async def test_dict_processing(self, tool):
        """Test für Dict-Verarbeitung"""
        test_input = {{"key": "value"}}
        result = await tool.execute(test_input)

        assert result.success is True
        assert isinstance(result.data, dict)

    @pytest.mark.asyncio
    async def test_context_generation(self, tool):
        """Test für Kontext-Generierung"""
        result = await tool.execute("test")

        assert result.context.session_id is not None
        assert result.context.correlation_id is not None
        assert result.context.start_time is not None


if __name__ == "__main__":
    pytest.main([__file__])
'''

    def _get_readme_template(self) -> str:
        """Template für README-Dateien"""
        return """# {name} AI Tool

{description}

## Profil

**Profil:** {profile}

## Setup

```bash
# Abhängigkeiten installieren
pip install -r requirements.txt

# Tool testen
python {name}_tool.py
```

## Nutzung

```python
from {name}_tool import {class_name}

# Tool initialisieren
tool = {class_name}()

# Ausführen
result = await tool.execute("input data")
```

## Features

- Automatisches Logging
- Context Management
- Error Handling
- {profile} Profile Compliance

## Entwicklung

```bash
# Tests ausführen (Standard/Production)
python -m pytest test_{name}_tool.py

# Profile-Validierung
python src/ai_lab_framework/profile_validator.py {name}_tool.py
```

## Anforderungen

- Python 3.11+
- AI Lab Framework

---

*Generated with AI Lab Framework Tool Generator*
"""


def main():
    """CLI-Interface"""
    parser = argparse.ArgumentParser(description="AI Lab Framework Tool Generator")
    parser.add_argument("name", help="Name of the AI tool")
    parser.add_argument(
        "profile",
        choices=["experimental", "standard", "production"],
        help="Profile for the AI tool",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help="Output directory (default: current directory)",
    )

    args = parser.parse_args()

    generator = ToolGenerator()

    try:
        generator.generate_tool(args.name, args.profile, args.output)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
