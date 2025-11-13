# FRM-002-2: Analyse überflüssiger Strukturen - Analyseergebnisse

## 1. Leere Verzeichnisse

Die folgenden Verzeichnisse sind leer und können potenziell entfernt werden, sofern sie nicht als Platzhalter für zukünftige Inhalte dienen oder von Tools automatisch erstellt werden:

*   `./tools/hisense-tv`
*   `./archive/legacy`
*   `./projects/homeserver-vision-documentation/models/checkpoints`
*   `./projects/homeserver-vision-documentation/models/fine-tuned`
*   `./projects/homeserver-vision-documentation/docs/architecture`
*   `./projects/homeserver-vision-documentation/docs/api`
*   `./projects/homeserver-vision-documentation/logs`
*   `./projects/homeserver-vision-documentation/scripts/setup`
*   `./projects/homeserver-vision-documentation/scripts/deployment`
*   `./projects/homeserver-vision-documentation/prompts`
*   `./projects/homeserver-vision-documentation/fixtures`
*   `./projects/homeserver-vision-documentation/.git/objects/pack`
*   `./projects/homeserver-vision-documentation/.git/objects/info`
*   `./projects/homeserver-vision-documentation/.git/refs/tags`
*   `./projects/homeserver-vision-documentation/monitoring/metrics`
*   `./projects/homeserver-vision-documentation/monitoring/logs`
*   `./projects/homeserver-vision-documentation/data/processed`
*   `./projects/homeserver-vision-documentation/data/raw`
*   `./projects/agent-control-plane/poc`
*   `./projects/agent-control-plane/config`
*   `./projects/agent-control-plane/tests`
*   `./projects/agent-control-plane/models/checkpoints`
*   `./projects/agent-control-plane/models/fine-tuned`
*   `./projects/agent-control-plane/docs/architecture`
*   `./projects/agent-control-plane/docs/api`
*   `./projects/agent-control-plane/scripts/setup`
*   `./projects/agent-control-plane/scripts/deployment`
*   `./projects/agent-control-plane/prompts`
*   `./projects/agent-control-plane/monitoring/metrics`
*   `./projects/agent-control-plane/monitoring/logs`
*   `./projects/agent-control-plane/data/processed`
*   `./projects/agent-control-plane/data/raw`
*   `./projects/agent-control-plane/src/models`
*   `./projects/homeserver-vision-infrastructure/models/checkpoints`
*   `./projects/homeserver-vision-infrastructure/models/fine-tuned`
*   `./projects/homeserver-vision-infrastructure/docs/architecture`
*   `./projects/homeserver-vision-infrastructure/docs/api`
*   `./projects/homeserver-vision-infrastructure/logs`
*   `./projects/homeserver-vision-infrastructure/scripts/setup`
*   `./projects/homeserver-vision-infrastructure/scripts/deployment`
*   `./projects/homeserver-vision-infrastructure/fixtures`
*   `./projects/homeserver-vision-infrastructure/.git/objects/info`
*   `./projects/homeserver-vision-infrastructure/.git/refs/tags`
*   `./projects/homeserver-vision-infrastructure/monitoring/metrics`
*   `./projects/homeserver-vision-infrastructure/monitoring/logs`
*   `./projects/homeserver-vision-infrastructure/data/processed`
*   `./projects/homeserver-vision-infrastructure/data/raw`
*   `./projects/archived`
*   `./docs/content/ai-guide/agentos-standards`
*   `./docs/assets/css`
*   `./docs/assets/images`
*   `./docs/assets/js`
*   `./functional-mcp-server/.git/objects/pack`
*   `./functional-mcp-server/.git/objects/info`
*   `./functional-mcp-server/.git/refs/tags`
*   `./venv/include`
*   `./ideas/ready`
*   `./ideas/refining`
*   `./.git/objects/pack`
*   `./.git/objects/info`
*   `./.git/refs/tags`

## 2. Redundante, veraltete oder zu konsolidierende Dateien

Basierend auf den Analysen aus `FRM-002-1.1` bis `FRM-002-1.4` wurden folgende Dateien als redundant, veraltet oder für eine Konsolidierung/Refaktorierung identifiziert:

### 2.1. Root-Level Dateien (zu löschen/konsolidieren)
*   `AGENTS.md` (Inhalt nach `AI_GUIDE.md` oder `core/guidelines/GUIDELINES_KI_TOOLS.md` verschieben)
*   `GEMINI.md` (Inhalt nach `AI_GUIDE.md` oder `core/guidelines/GUIDELINES_KI_TOOLS.md` verschieben)
*   `SCRIPT_ORGANIZATION.md` (Inhalt nach `DEVELOPER_GUIDE.md` verschieben)
*   `BACKUP_README.md` (Inhalt nach `core/docs/OPERATIONS.md` verschieben und archivieren)

### 2.2. `core/` Dateien (zu refaktorieren)
*   `core/MANUAL.md` (Strukturinformationen nach `core/docs/FRAMEWORK_STRUCTURE.md` verschieben, dann als High-Level-Handbuch refaktorieren)

### 2.3. `docs/content/` Dateien (Duplikate von SSoT-Dokumenten, zu löschen/synchronisieren)
*   `docs/content/getting-started/index.md` (Duplikat von `GETTING_STARTED.md`)
*   `docs/content/developer-guide/index.md` (Duplikat von `DEVELOPER_GUIDE.md`)
*   `docs/content/ai-guide/index.md` (Duplikat von `AI_GUIDE.md`)
*   `docs/content/core-docs/FRAMEWORK_STRUCTURE.md` (Duplikat von `core/docs/FRAMEWORK_STRUCTURE.md`)
*   `docs/content/core-docs/PROJECT_CONTEXT.md` (Duplikat von `core/docs/PROJECT_CONTEXT.md`)
*   `docs/content/developer-guide/documentation-matrix.md` (Duplikat von `core/docs/DOCUMENTATION_MATRIX.md`)
*   `docs/content/project-management/project-status.md` (Veraltet, da Projektstatus jetzt JSON-basiert ist)
*   `docs/content/project-management/work-items/*.md` (Alle Dateien in diesem Verzeichnis sind veraltete Markdown-Arbeitspakete)

### 2.4. Projekt-Level Dateien (zu konsolidieren/löschen)
*   `projects/*/PROJECT_OVERVIEW.md` (Alle Dateien, die diesem Muster entsprechen, sind redundant und sollten in die jeweilige `README.md` konsolidiert werden)

## Zusammenfassung

Die Analyse hat eine beträchtliche Anzahl leerer Verzeichnisse und redundanter/veralteter Dokumentationsdateien identifiziert. Die Konsolidierungsstrategie aus `FRM-002-1.5` wird diese Probleme im nächsten Schritt angehen.
