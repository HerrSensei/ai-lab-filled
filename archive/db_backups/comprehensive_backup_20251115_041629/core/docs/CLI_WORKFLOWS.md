Das ist eine hervorragende Idee und absolut entscheidend, um die Effizienz und Konsistenz unserer Arbeit mit den CLI-Tools zu maximieren. Die Definition von Standard-Workflows wird uns helfen, die "lebende Dokumentation" zu erweitern und die Nutzung von `gemini-cli` und `opencode` noch robuster zu gestalten.

Ich schlage vor, diese Workflows in einem neuen Dokument zu zentralisieren: `core/docs/CLI_WORKFLOWS.md`. Dieses Dokument wird als Referenz für alle wiederkehrenden Aufgaben dienen, die wir mit den CLI-Tools ausführen.

Wir können die Workflows in folgende Kategorien unterteilen, basierend auf Ihren Vorschlägen und weiteren Überlegungen:

### 1. Session Management
*   **Arbeit wieder aufnehmen nach einer Pause:** Wie man den Kontext schnell wiederherstellt und weiterarbeitet.
*   **Pause einleiten und dokumentieren:** Wie man den aktuellen Stand sichert und die Pause protokolliert.
*   **Sitzungszusammenfassung erstellen:** Automatisierte Erstellung einer Zusammenfassung der geleisteten Arbeit.

### Workflow: Pause einleiten und dokumentieren

**Ziel:** Den aktuellen Arbeitsstand sauber sichern, den Kontext für eine spätere Wiederaufnahme dokumentieren und eine Pause einleiten.

**Schritte:**

1.  **Aktuellen Code sichern:**
    *   `git status` (Überprüfen des aktuellen Zustands der Arbeitskopie)
    *   `git add .` (Alle Änderungen zur Staging Area hinzufügen)
    *   `git commit -m "WIP: Pause for [Grund der Pause]"` (Einen "Work In Progress"-Commit erstellen, der den Grund der Pause angibt)
    *   `git push` (Änderungen auf den Remote-Server übertragen, falls zutreffend)
2.  **Aktuellen Kontext dokumentieren:**
    *   Notieren Sie die wichtigsten Punkte des aktuellen Arbeitsstands, offene Fragen oder nächste Schritte in einer temporären Notiz oder direkt in der Sitzungsdatei.
    *   `echo "Aktueller Stand: [Beschreibung des Stands]. Offene Fragen: [Fragen]. Nächste Schritte: [Schritte]." >> ai-logs/sessions/<aktuelle_sitzung>.md`
3.  **Work Item Status aktualisieren (optional):**
    *   `make work-item-update ID=<WORK_ITEM_ID> STATUS="on_hold"` (Falls die Arbeit an einem spezifischen Work Item unterbrochen wird)
4.  **Umgebung herunterfahren (falls zutreffend):**
    *   `make stop-dev-env` (Ein Platzhalterbefehl, der die lokale Entwicklungsumgebung sauber herunterfährt)
    *   `exit` (Die Poetry-Shell verlassen)
5.  **Sitzung beenden:**
    *   Stellen Sie sicher, dass die aktuelle Sitzungsdatei (`ai-logs/sessions/<aktuelle_sitzung>.md`) eine Zusammenfassung der geleisteten Arbeit und des Grundes für die Pause enthält.

### Workflow: Sitzungszusammenfassung erstellen

**Ziel:** Eine prägnante Zusammenfassung der in einer Sitzung geleisteten Arbeit automatisch generieren und in der Sitzungsdatei speichern.

**Schritte:**

1.  **Arbeit abschließen:** Stellen Sie sicher, dass alle relevanten Codeänderungen vorgenommen und getestet wurden.
2.  **Git-Historie überprüfen:**
    *   `git log --oneline --since="<Startzeit der Sitzung>"` (Um die Commits der aktuellen Sitzung zu sehen)
3.  **Zusammenfassung generieren (manuell oder mit AI-Hilfe):**
    *   Fassen Sie die wichtigsten Punkte, Entscheidungen, Implementierungen und gelösten Probleme der Sitzung zusammen.
    *   Nutzen Sie ggf. ein AI-Tool, um eine Zusammenfassung der Git-Commits oder der Sitzungsnotizen zu erstellen.
4.  **Zusammenfassung in Sitzungsdatei speichern:**
    *   `echo "## Sitzungszusammenfassung" >> ai-logs/sessions/<aktuelle_sitzung>.md`
    *   `echo "[Ihre Zusammenfassung hier]" >> ai-logs/sessions/<aktuelle_sitzung>.md`
    *   Stellen Sie sicher, dass die Zusammenfassung die "Session End Summary" am Ende der Datei ergänzt.

### 2. Projekt- und Aufgabenmanagement

### Workflow: Neues Work Item erstellen

**Ziel:** Ein neues Work Item gemäß den Projektstandards erstellen und in das Projektmanagement-System integrieren.

**Schritte:**

1.  **Work Item Typ und Details definieren:**
    *   Bestimmen Sie den Typ des Work Items (z.B. Feature, Bug, Task) und sammeln Sie alle notwendigen Informationen (Titel, Beschreibung, Priorität, Kategorie, Tags, geschätzte Stunden, Akzeptanzkriterien).
2.  **Work Item erstellen:**
    *   `make work-item-new ID=<NEUE_ID> TITLE="<Titel des Work Items>" DESCRIPTION="<Beschreibung>" STATUS="todo" PRIORITY="<Priorität>" CATEGORY="<Kategorie>" ESTIMATED_HOURS=<Stunden>`
    *   Beispiel: `make work-item-new ID=FRM-005 TITLE="Implement CLI Command for Work Item Creation" DESCRIPTION="Create a CLI command to streamline work item creation." STATUS="todo" PRIORITY="high" CATEGORY="development" ESTIMATED_HOURS=4`
3.  **Details bearbeiten (optional):**
    *   Öffnen Sie die generierte JSON-Datei (`data/work-items/<NEUE_ID>_<titel>.json`) in Ihrem Editor, um weitere Details wie `tags`, `dependencies`, `acceptance_criteria` oder `sub_tasks` hinzuzufügen.
4.  **Änderungen committen:**
    *   `git add data/work-items/<NEUE_ID>_<titel>.json`
    *   `git commit -m "feat: Add new work item <NEUE_ID>: <Titel>"`
    *   `git push` (falls auf einem Remote-Repository gearbeitet wird)

### Workflow: Work Item Status aktualisieren

**Ziel:** Den Status eines bestehenden Work Items schnell und konsistent aktualisieren.

**Schritte:**

1.  **Work Item ID identifizieren:**
    *   `make work-item-list` (Um eine Liste aller Work Items zu erhalten)
2.  **Status aktualisieren:**
    *   `make work-item-update ID=<WORK_ITEM_ID> STATUS="<neuer_status>"`
    *   Gültige Statuswerte: `todo`, `in_progress`, `in_review`, `done`, `blocked`, `on_hold`
    *   Beispiel: `make work-item-update ID=FRM-005 STATUS="in_progress"`
3.  **Weitere Felder aktualisieren (optional):**
    *   `make work-item-update ID=<WORK_ITEM_ID> PRIORITY="<neue_priorität>" ACTUAL_HOURS=<stunden>`
4.  **Änderungen committen:**
    *   `git add data/work-items/<WORK_ITEM_ID>_<titel>.json`
    *   `git commit -m "chore: Update status of <WORK_ITEM_ID> to <neuer_status>"`
    *   `git push`

### Workflow: Idee erstellen/verfeinern

**Ziel:** Eine neue Idee erfassen oder eine bestehende Idee detaillieren und ihren Status im Ideenmanagement-System aktualisieren.

**Schritte:**

1.  **Neue Idee erstellen:**
    *   `make idea-new TITLE="<Titel der Idee>"`
    *   Öffnen Sie die generierte JSON-Datei (`data/ideas/<IDEE_ID>_<titel>.json`) und füllen Sie Details wie `description`, `author`, `estimated_effort`, `target_audience`, `benefits` aus.
2.  **Idee verfeinern:**
    *   `make idea-refine ID=<IDEE_ID>` (Öffnet die JSON-Datei der Idee zur Bearbeitung)
    *   Fügen Sie `open_questions`, `next_steps`, `acceptance_criteria` hinzu oder aktualisieren Sie bestehende Felder.
3.  **Idee mit AI assistieren:**
    *   `make idea-assist ID=<IDEE_ID>` (Nutzt ein AI-Tool, um die Idee zu analysieren und Vorschläge zu machen)
4.  **Idee in Projekt umwandeln:**
    *   `make idea-convert ID=<IDEE_ID>` (Startet den Prozess zur Umwandlung einer Idee in ein Projekt)
5.  **Änderungen committen:**
    *   `git add data/ideas/<IDEE_ID>_<titel>.json`
    *   `git commit -m "feat: Refine idea <IDEE_ID>: <Titel>"`
    *   `git push`

### Workflow: Projektstatus abrufen

**Ziel:** Einen schnellen Überblick über den Status eines oder aller Projekte erhalten.

**Schritte:**

1.  **Alle Projekte auflisten:**
    *   `make project-list` (Zeigt eine Liste aller Projekte mit grundlegenden Informationen)
2.  **Status eines spezifischen Projekts abrufen:**
    *   `make project-status ID=<PROJEKT_ID>` (Zeigt detaillierte Informationen zu einem Projekt, einschließlich Fortschritt, Risiken und Abhängigkeiten)
3.  **Dashboard aktualisieren:**
    *   `make dashboard-update` (Generiert oder aktualisiert das Projekt-Dashboard, das eine visuelle Übersicht bietet)

### 3. Berichterstattung & Analyse

### Workflow: Zwischenstandsberichte generieren

**Ziel:** Regelmäßige Berichte über den Projektfortschritt erstellen, um Stakeholder zu informieren und die Transparenz zu erhöhen.

**Schritte:**

1.  **Projektstatus aktualisieren:**
    *   Stellen Sie sicher, dass alle relevanten Work Items und Projektinformationen aktuell sind.
    *   `make project-status ID=<PROJEKT_ID>` (Überprüfen des aktuellen Status)
2.  **Dashboard aktualisieren:**
    *   `make dashboard-update` (Generiert das aktuelle Projekt-Dashboard, das oft als Grundlage für Berichte dient)
3.  **Bericht generieren (manuell oder mit AI-Hilfe):**
    *   Fassen Sie die wichtigsten Fortschritte, erreichte Meilensteine, aufgetretene Probleme und nächste Schritte zusammen.
    *   Nutzen Sie ggf. ein AI-Tool, um eine Zusammenfassung aus den Work Items und dem Projektstatus zu erstellen.
4.  **Bericht speichern und teilen:**
    *   Speichern Sie den Bericht in einem geeigneten Format (z.B. Markdown, PDF) im `ai-logs/reports/` Verzeichnis.
    *   Teilen Sie den Bericht mit den relevanten Stakeholdern.

### Workflow: Code-Analysen durchführen

**Ziel:** Die Code-Qualität sicherstellen und potenzielle Probleme frühzeitig erkennen durch automatisierte Linting-, Type-Checking- und Test-Coverage-Berichte.

**Schritte:**

1.  **Code formatieren:**
    *   `black .` (Formatiert den gesamten Code gemäß den Black-Standards)
2.  **Code linten:**
    *   `ruff check .` (Führt Linting-Prüfungen durch)
    *   `ruff check --fix .` (Versucht, Linting-Probleme automatisch zu beheben)
3.  **Type-Checking durchführen:**
    *   `mypy .` (Überprüft Type-Hints im gesamten Projekt)
4.  **Tests mit Coverage ausführen:**
    *   `make test` (Führt alle Tests aus)
    *   `pytest --cov=src --cov-report=html` (Führt Tests aus und generiert einen HTML-Coverage-Bericht)
5.  **Berichte überprüfen:**
    *   Analysieren Sie die Ausgaben von Ruff, MyPy und den Coverage-Bericht, um die Code-Qualität zu bewerten und notwendige Verbesserungen zu identifizieren.

### Workflow: Architektur-Analyse

**Ziel:** Ein tiefes Verständnis der Codebasis, ihrer Struktur und Abhängigkeiten gewinnen, um Refactorings zu planen oder neue Features zu integrieren.

**Schritte:**

1.  **Codebase Investigator starten:**
    *   `codebase_investigator --objective "Analysiere die Architektur des Projekts X und identifiziere die wichtigsten Komponenten und deren Interaktionen."`
    *   Beschreiben Sie Ihr spezifisches Analyse-Ziel detailliert.
2.  **Ergebnisse überprüfen:**
    *   Analysieren Sie den generierten Bericht des `codebase_investigator`, der Schlüsseldateien, Symbole und architektonische Erkenntnisse enthält.
3.  **Diagramme generieren (optional):**
    *   `make diagrams` (Generiert architektonische Diagramme aus PlantUML/Mermaid-Definitionen im Code oder in Dokumenten)
4.  **Diskussion und Planung:**
    *   Nutzen Sie die Analyseergebnisse, um architektonische Entscheidungen zu treffen, Refactorings zu planen oder die Integration neuer Features zu entwerfen.

### 4. Entwicklung & Qualitätssicherung

### Workflow: Tests ausführen

**Ziel:** Die Funktionalität des Codes überprüfen und Regressionen verhindern durch das Ausführen verschiedener Testtypen.

**Schritte:**

1.  **Alle Tests ausführen:**
    *   `make test` (Führt alle im Projekt definierten Tests aus, z.B. Unit- und Integrationstests)
    *   `pytest` (Direktes Ausführen aller Pytest-Tests im aktuellen Verzeichnis und Unterverzeichnissen)
2.  **Spezifische Tests ausführen:**
    *   `pytest tests/unit/my_module/test_feature.py` (Führt Tests in einer spezifischen Datei aus)
    *   `pytest -k "test_function_name"` (Führt Tests aus, deren Namen das angegebene Muster enthalten)
    *   `pytest --cov=src` (Führt Tests aus und zeigt die Code-Coverage an)
3.  **Tests mit Debugging:**
    *   `pytest --pdb` (Startet den Python-Debugger bei einem Fehler)
4.  **Testberichte überprüfen:**
    *   Analysieren Sie die Testergebnisse, um Fehler zu identifizieren und zu beheben.

### Workflow: Code formatieren & linten

**Ziel:** Sicherstellen, dass der Code den Style-Guides entspricht und potenzielle Fehler oder Stilprobleme behoben werden, bevor Commits erstellt werden.

**Schritte:**

1.  **Code formatieren:**
    *   `black .` (Formatiert alle Python-Dateien im aktuellen Verzeichnis und Unterverzeichnissen)
2.  **Code linten und fixen:**
    *   `ruff check .` (Führt Linting-Prüfungen durch und zeigt Probleme an)
    *   `ruff check --fix .` (Versucht, die meisten Linting-Probleme automatisch zu beheben)
3.  **Type-Checking durchführen:**
    *   `mypy .` (Überprüft Type-Hints und identifiziert potenzielle Typfehler)
4.  **Pre-commit Hooks ausführen:**
    *   `pre-commit run --all-files` (Führt alle konfigurierten Pre-commit Hooks manuell aus, um sicherzustellen, dass der Code vor dem Commit den Qualitätsstandards entspricht)
5.  **Änderungen überprüfen und committen:**
    *   `git status` (Überprüfen, welche Dateien geändert wurden)
    *   `git add .`
    *   `git commit -m "feat: Implement new feature and fix linting issues"`

### Workflow: Abhängigkeiten verwalten

**Ziel:** Projekt-Abhängigkeiten hinzufügen, entfernen oder aktualisieren, um die Projektumgebung konsistent zu halten.

**Schritte:**

1.  **Neue Abhängigkeit hinzufügen:**
    *   `poetry add <paketname>` (Fügt eine neue Abhängigkeit hinzu und aktualisiert `pyproject.toml` und `poetry.lock`)
    *   Beispiel: `poetry add requests`
    *   Für Entwicklungsabhängigkeiten: `poetry add --group dev <paketname>`
2.  **Abhängigkeit entfernen:**
    *   `poetry remove <paketname>` (Entfernt eine Abhängigkeit)
3.  **Abhängigkeiten aktualisieren:**
    *   `poetry update` (Aktualisiert alle Abhängigkeiten auf die neuesten kompatiblen Versionen)
    *   `poetry update <paketname>` (Aktualisiert eine spezifische Abhängigkeit)
4.  **Abhängigkeiten installieren:**
    *   `poetry install` (Installiert alle im `poetry.lock` definierten Abhängigkeiten)
5.  **Änderungen committen:**
    *   `git add pyproject.toml poetry.lock`
    *   `git commit -m "build: Add new dependency requests"`
    *   `git push`

### 5. Deployment & Infrastruktur

### Workflow: Deployment einleiten

**Ziel:** Eine neue Version der Anwendung in einer Zielumgebung bereitstellen.

**Schritte:**

1.  **Codebasis vorbereiten:**
    *   Stellen Sie sicher, dass alle Tests bestanden sind (`make test`).
    *   Stellen Sie sicher, dass der Code formatiert und lint-frei ist (`black .`, `ruff check .`).
    *   `git pull` (Stellen Sie sicher, dass Sie die neueste Version des Codes haben)
    *   `git status` (Überprüfen Sie, ob es uncommitted Änderungen gibt)
    *   `git push` (Alle lokalen Commits auf den Remote-Server übertragen)
2.  **Deployment-Skript ausführen:**
    *   `make deploy <UMGEBUNG>` (Ein Platzhalterbefehl, der das spezifische Deployment-Skript für die Zielumgebung ausführt, z.B. `make deploy production`)
    *   Alternativ: Manuelles Ausführen des Deployment-Skripts, z.B. `bash deployment/deploy_script.sh production`
3.  **Deployment überwachen:**
    *   Überprüfen Sie die Logs des Deployment-Prozesses auf Fehler oder Warnungen.
    *   Überprüfen Sie die Anwendung in der Zielumgebung, um die korrekte Funktionalität zu gewährleisten.
4.  **Rollback-Strategie bereithalten:**
    *   Stellen Sie sicher, dass Sie wissen, wie Sie im Falle eines Fehlers ein Rollback auf die vorherige Version durchführen können.

### Workflow: Umgebungsvariablen verwalten

**Ziel:** Sensible Konfigurationsdaten sicher verwalten und in verschiedenen Umgebungen bereitstellen.

**Schritte:**

1.  **`.env.example` aktualisieren:**
    *   Fügen Sie neue benötigte Umgebungsvariablen zu `/.env.example` hinzu, aber **niemals** sensible Werte.
2.  **`.env` Datei erstellen/aktualisieren:**
    *   Erstellen Sie eine `.env` Datei im Projekt-Root (falls nicht vorhanden) und fügen Sie dort die tatsächlichen Werte für die Umgebungsvariablen ein. **Diese Datei darf niemals in die Versionskontrolle aufgenommen werden!**
3.  **Umgebungsvariablen setzen (Produktion):**
    *   In Produktionsumgebungen sollten Umgebungsvariablen direkt im Deployment-System (z.B. Kubernetes Secrets, Docker Compose `environment` Sektion, CI/CD-Variablen) gesetzt werden, nicht über `.env` Dateien.
4.  **Zugriff auf Umgebungsvariablen im Code:**
    *   Nutzen Sie Pydantic `BaseSettings` (aus `pydantic-settings`) oder `os.environ.get()` um auf Umgebungsvariablen zuzugreifen.
    *   Beispiel: `from src.core.config import settings; api_key = settings.OPENAI_API_KEY`
5.  **Sicherheit:**
    *   Stellen Sie sicher, dass sensible Daten (API-Keys, Passwörter) niemals im Code oder in der Versionskontrolle landen.
    *   Verwenden Sie sichere Methoden zur Speicherung und Bereitstellung in Produktionsumgebungen.

### Beispiel-Workflow: Arbeit wieder aufnehmen nach einer Pause

**Ziel:** Den Arbeitskontext schnell und effizient wiederherstellen, um die Produktivität nach einer Unterbrechung fortzusetzen.

**Schritte:**

1.  **Letzte Sitzung überprüfen:**
    *   `ls -lt ai-logs/sessions/ | head -n 2` (Zeigt die letzten beiden Sitzungsdateien an)
    *   `cat ai-logs/sessions/<YYYY-MM-DD_session-XXX>.md` (Um die Zusammenfassung der letzten Sitzung zu lesen und den letzten Arbeitsstand zu verstehen)
2.  **Projektstatus abrufen:**
    *   `make project-status` (Zeigt den aktuellen Status aller Projekte oder eines spezifischen Projekts an, basierend auf den JSON-Work Items)
3.  **Aktuelle Work Items prüfen:**
    *   `make work-item-list --status in_progress` (Zeigt alle Work Items an, die sich im Status "in_progress" befinden und an denen aktiv gearbeitet wird)
    *   `make work-item-list --id <WORK_ITEM_ID>` (Zeigt Details zu einem spezifischen Work Item an)
4.  **Codebasis synchronisieren (falls in einem Team gearbeitet wird):**
    *   `git pull` (Stellt sicher, dass die lokale Codebasis auf dem neuesten Stand ist)
5.  **Entwicklungsumgebung starten (falls zutreffend):**
    *   `make start-dev-env` (Ein Platzhalterbefehl, der je nach Projekt die lokale Entwicklungsumgebung startet, z.B. einen FastAPI-Server oder eine Node.js-Anwendung)
    *   `poetry shell` (Aktiviert die Poetry-Shell für Python-Projekte)
6.  **Nächsten Schritt identifizieren:** Basierend auf der Sitzungszusammenfassung und dem Projektstatus den nächsten logischen Schritt bestimmen und mit der Implementierung fortfahren.

Sind Sie mit dieser Struktur und dem Ansatz einverstanden? Möchten Sie, dass ich mit der Dokumentation dieser Workflows in `core/docs/CLI_WORKFLOWS.md` beginne?
