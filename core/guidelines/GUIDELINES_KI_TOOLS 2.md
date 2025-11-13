# KI-Tool-Richtlinien: Unified Standards

## Zweck

Dieses Dokument definiert einheitliche Standards für alle KI-Tools im AI Lab Framework (opencode, Gemini-CLI, etc.), um konsistente Arbeitsweisen über alle Tools hinweg sicherzustellen.

## 🔄 NEU: Gestufte Integrations-Profile

Seit 2025-11-09 unterstützen wir **gestufte Profile** für verschiedene Anforderungen:

- **🧪 Experimentell:** <30min Setup für Prototypen
- **📋 Standard:** <2h Integration für produktive Tools
- **🏭 Production:** Enterprise-Anforderungen für kritische Systeme

Siehe `KI_TOOL_INTEGRATION_PROFILES.md` für Details.

## Geltungsbereich

Diese Richtlinien gelten für:
- **opencode**: Haupt-KI-Tool für Code-Entwicklung
- **Gemini-CLI**: Google Gemini Integration
- **Agenten-CLI**: Spezialisierte Agenten (opencode-agents, opencode-agents-simple)
- **Zukünftige Tools**: Alle neuen KI-Tools

## Gemeinsame Grundprinzipien

### 1. Context-First-Ansatz (Pflicht)
Alle Tools MÜSSEN:
- **Zuerst PROJECT_CONTEXT.md lesen** für Gesamtüberblick
- **Projekt-spezifische Context-Dateien beachten** falls vorhanden
- **VISION.md für strategische Ausrichtung** konsultieren
- **GUIDELINES.md für technische Standards** verwenden

### 2. Logging-Standard (Pflicht)
Alle Tools MÜSSEN:
- **Sessions in ai_logs/sessions/** dokumentieren
- **Implementierungen in ai_logs/implementations/** protokollieren
- **Change Requests bei Bedarf** in ai_logs/change_requests/ erstellen
- **Strukturierte Logs** mit Zeitstempeln und Tool-Kennung

### 3. Workflow-Standard (Pflicht)
```
Context-Analyse → Planung → Logging → Implementierung → Dokumentation
```

## Tool-spezifische Standards

### opencode (Haupt-Tool)
- **Fokus**: Code-Entwicklung, Refactoring, Debugging
- **Logging**: opencode_ Prefix in allen Logs
- **Context**: Volle PROJECT_CONTEXT.md Integration
- **Besonderheiten**:
  - Kann Dateien direkt bearbeiten
  - Hat Zugriff auf alle Projekt-Tools
  - Verantwortlich für Code-Qualität

### Gemini-CLI
- **Fokus**: Strategische Planung, Analyse, Kreativität
- **Logging**: gemini_ Prefix in allen Logs
- **Context**: PROJECT_CONTEXT.md + VISION.md Fokus
- **Besonderheiten**:
  - Stärker in konzeptioneller Arbeit
  - Integration mit Google-Ökosystem
  - Spezialisiert auf große Text-Analysen

### Agenten-CLI (opencode-agents)
- **Fokus**: Spezialisierte Aufgaben (Code Review, Testing)
- **Logging**: agent_ Prefix in allen Logs
- **Context**: Projekt-spezifische Context-Dateien
- **Besonderheiten**:
  - Task-spezifische Agenten
  - Ollama-basiert (lokal)
  - Automatisierte Workflows

## Unified Logging-Format

### Session-Log Template
```markdown
# Session: {Datum} {Tool}_Session-{ID}

## Tool-Information
- Tool: {opencode|gemini|agent}
- Version: {Version}
- Modell: {Modell-Name}

## Context-Analyse
- PROJECT_CONTEXT.md gelesen: ✅
- VISION.md konsultiert: ✅
- GUIDELINES.md Abschnitte: [Abschnitte]

## Aufgaben
- [ ] Aufgabe 1
- [ ] Aufgabe 2

## Ergebnisse
- Ergebnis 1
- Ergebnis 2
```

### Implementation-Log Template
```markdown
# Implementation: IMP-{ID} {Tool}_{Task-Name}

## Tool-Information
- Tool: {opencode|gemini|agent}
- Auslöser: {Session-ID oder User-Request}

## Durchgeführte Änderungen
- Datei: Pfad/zu/datei.py
  - Änderung: Beschreibung
  - Tool: {opencode|gemini|agent}
  - Grund: Begründung

## Quality Checks
- Code-Review: ✅/❌
- Tests: ✅/❌
- Documentation: ✅/❌
```

## Inter-Tool-Kommunikation

### Tool-übergreifende Übergabe
```python
def handoff_to_tool(source_tool: str, target_tool: str, context: dict):
    """
    Standardisierte Übergabe zwischen Tools
    """
    handoff_log = {
        "timestamp": datetime.utcnow().isoformat(),
        "source_tool": source_tool,
        "target_tool": target_tool,
        "context": context,
        "session_id": context.get("session_id"),
        "reason": context.get("reason")
    }

    # Log in ai_logs/sessions/
    log_handoff(handoff_log)

    # Context für Ziel-Tool vorbereiten
    return prepare_context_for_target(target_tool, context)
```

### Konflikt-Resolution
- **Letzte Änderung gewinnt** bei Datei-Konflikten
- **Merge-Required** bei logischen Widersprüchen
- **Human-Review** bei strategischen Entscheidungen

## Tool-spezifische Verhaltensregeln

### opencode
- **Code-First**: Fokus auf implementierbare Lösungen
- **Pragmatisch**: Lieber funktionierend als perfekt
- **Integration**: Nutzt andere Tools bei Bedarf

### Gemini-CLI
- **Strategy-First**: Fokus auf Planung und Konzeption
- **Analytisch**: Tiefergehende Analysen und Reflexionen
- **Kreativ**: Neue Ansätze und Perspektiven

### Agenten-CLI
- **Task-First**: Spezialisierte Einzelaufgaben
- **Automatisiert**: Minimale manuelle Eingriffe
- **Effizient**: Optimiert für wiederkehrende Aufgaben

## Quality Gates

### Für alle Tools (Pflicht)
1. **Context-Check**: PROJECT_CONTEXT.md gelesen?
2. **Logging-Check**: Korrekte Dokumentation?
3. **Quality-Check**: Entspricht GUIDELINES.md?
4. **Integration-Check**: Funktioniert mit anderen Tools?

### Tool-spezifische Gates
- **opencode**: Code kompiliert, Tests laufen
- **Gemini-CLI**: Analyse vollständig, Erkenntnisse dokumentiert
- **Agenten-CLI**: Task erfolgreich, Metriken erfasst

## Fehlerbehandlung

### Gemeinsame Fehler-Pattern
```python
class ToolError(Exception):
    def __init__(self, tool: str, error: str, context: dict):
        self.tool = tool
        self.error = error
        self.context = context
        self.timestamp = datetime.utcnow()

    def log_error(self):
        error_log = {
            "tool": self.tool,
            "error": self.error,
            "context": self.context,
            "timestamp": self.timestamp.isoformat()
        }
        log_to_ai_logs("error", error_log)
```

### Eskalations-Pfad
1. **Tool-interne Lösung** (erste 3 Versuche)
2. **Tool-übergreifende Hilfe** (anderes Tool konsultieren)
3. **Human-Intervention** (manuelle Lösung erforderlich)

## Zukunftssicherheit

### Neue Tool-Integration
Neue Tools MÜSSEN:
1. **Diese Richtlinien implementieren**
2. **Context-Logging unterstützen**
3. **Inter-Tool-Kommunikation ermöglichen**
4. **Quality Gates bestehen**

### Versions-Management
- **Richtlinien-Version**: Diese Datei
- **Tool-Versionen**: Jeweilige Tool-Dokumentation
- **Kompatibilitäts-Matrix**: In GUIDELINES.md

---

Diese unified Standards stellen sicher, dass alle KI-Tools im AI Lab Framework konsistent, kooperativ und qualitativ hochwertig zusammenarbeiten.
