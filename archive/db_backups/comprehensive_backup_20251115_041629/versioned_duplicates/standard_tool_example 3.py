"""
Beispiel-Tool mit Standard-Profil

Demonstriert die Verwendung des AI Lab Framework SDK.
"""

import asyncio

from ai_lab_framework.base_ai_tool import StandardAITool, ToolContext


class MyStandardTool(StandardAITool):
    """
    Beispiel für ein Standard-KI-Tool mit vollem Framework-Support.
    """

    def __init__(self, config=None):
        super().__init__(config)
        self.name = "MyStandardTool"

    async def process(self, input_data, context: ToolContext):
        """
        Tool-spezifische Verarbeitungslogik.

        Args:
            input_data: Die zu verarbeitenden Daten
            context: Der Ausführungskontext

        Returns:
            Verarbeitete Daten
        """
        # Beispiel-Verarbeitung
        if isinstance(input_data, str):
            result = input_data.upper()
        elif isinstance(input_data, dict):
            result = {k.upper(): v for k, v in input_data.items()}
        else:
            result = str(input_data)

        # Simuliere etwas Arbeit
        await asyncio.sleep(0.1)

        return result


async def main():
    """Beispiel-Nutzung des Tools"""
    tool = MyStandardTool()

    # Führe Tool aus
    result = await tool.execute("hello world")

    print(f"Success: {result.success}")
    print(f"Data: {result.data}")
    print(f"Execution Time: {result.execution_time}s")
    print(f"Session ID: {result.context.session_id}")


if __name__ == "__main__":
    asyncio.run(main())
