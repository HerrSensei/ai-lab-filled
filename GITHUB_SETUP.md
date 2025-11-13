# GitHub Repository Setup für AI Lab Framework

## 🎯 Vorbereitungsschritte

### 1. GitHub Personal Access Token erstellen

1. Gehe zu GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Klicke auf "Generate new token"
3. Berechtigungen festlegen:
   - **Repo**: Full control of private repositories
   - **Issues**: Read and write
   - **Projects**: Read and write
   - **Labels**: Read and write
4. Token kopieren und sicher aufbewahren

### 2. Environment Variable setzen

```bash
export GITHUB_TOKEN="dein_token_hier"
export GITHUB_REPO="dein_username/ai-lab-framework"
```

### 3. Repository Labels automatisch erstellen

```bash
cd /pfad/zum/ai-lab-framework
source venv/bin/activate
python src/ai_lab_framework/github_integration.py --action setup
```

### 4. GitHub Project Board einrichten

1. Gehe zu deinem Repository
2. Klicke auf "Projects" → "New project"
3. Wähle "Board template"
4. Erstelle folgende Spalten:
   - **Backlog** (proposed)
   - **To Do** (ready to start)
   - **In Progress** (currently working)
   - **Review** (ready for review)
   - **Done** (completed)

### 5. Automatische Synchronisation starten

```bash
# Alle Items zu GitHub synchronisieren
python src/ai_lab_framework/github_integration.py --action sync-to-github

# Bidirektionale Synchronisation
python src/ai_lab_framework/github_integration.py --action sync-all
```

## 🏷️ Label-Struktur

### Status Labels
- `status:proposed` - Noch nicht begonnen
- `status:in_progress` - In Bearbeitung
- `status:done` - Abgeschlossen
- `status:archived` - Archiviert

### Priority Labels
- `priority:high` - Hohe Priorität
- `priority:medium` - Mittlere Priorität
- `priority:low` - Niedrige Priorität

### Component Labels
- `component:framework` - Core Framework
- `component:tools` - Development Tools
- `component:data-management` - Datenmanagement
- `component:documentation` - Dokumentation

### Type Labels
- `ai-lab` - Alle AI Lab Items
- `work-item` - Work Items
- `idea` - Ideen
- `session` - Session Logs

## 🔄 Workflow-Integration

### Work Item Workflow
1. **Erstellung** → SQLite → GitHub Issue (status:proposed)
2. **Zuweisung** → GitHub Labels (priority, component)
3. **Start** → GitHub Issue → SQLite (status:in_progress)
4. **Fertigstellung** → GitHub Issue → SQLite (status:done)

### Idea Workflow
1. **Einreichung** → SQLite → GitHub Issue (idea label)
2. **Bewertung** → GitHub Discussion
3. **Implementierung** → Work Item erstellen
4. **Abschluss** → Status aktualisieren

## 📊 Automatisierung

### GitHub Actions (Optional)
```yaml
# .github/workflows/sync.yml
name: Sync with SQLite
on:
  issues:
    types: [opened, edited, closed, reopened]
  push:
    paths:
      - 'data/ai_lab.db'

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Sync GitHub to SQLite
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          python src/ai_lab_framework/github_integration.py --action sync-from-github
```

## 🎯 Vorteile der Integration

### ✅ Vorteile
- **Zentrale Datenhaltung** in SQLite (Performance, Offline)
- **GitHub Collaboration** (Issues, Projects, Discussions)
- **Bidirektionale Synchronisation**
- **Automatisierte Workflows**
- **Team Collaboration**
- **Mobile Access** über GitHub App

### 🔄 Sync-Strategie
- **SQLite als Single Source of Truth**
- **GitHub als Collaboration Layer**
- **Automatische Konflikterkennung**
- **Timestamp-basierte Auflösung**

## 🚀 Nächste Schritte

1. **Setup durchführen** (oben stehende Schritte)
2. **Erste Synchronisation** testen
3. **Team einweisen** auf neuen Workflow
4. **Automatisierung** einrichten (GitHub Actions)
5. **Monitoring** der Sync-Prozesse

---

*Nach dem Setup kannst du deine Work Items und Ideas sowohl lokal als auch auf GitHub verwalten!*