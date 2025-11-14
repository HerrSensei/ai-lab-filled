# 🏗️ Framework/Instanz-Trennung - Detaillierte Planung

## 📋 Executive Summary

Das AI Lab Framework wird als **immutable Bibliothek** von der **ai-lab Instanz** getrennt. Das Framework ist eigenständiges GitHub-Repo, während `ai-lab` die Produktivinstanz mit Projekten wie `homeserver-agent` ist.

## 🎯 Zielsetzung

### Framework (`ai-lab-framework`)
- **Eigenständiges Repository** unter `ai-lab/ai-lab-framework`
- **Immutable Bibliothek** - keine Modifikation in Instanz möglich
- **Versioniertes Deployment** über PyPI/GitHub Releases
- **Eigene Datenbank** für Tool-Execution, Logging, Konfiguration
- **CLI-Tool Fokus** - Integration mit opencode, gemini-cli

### Instanz (`ai-lab`)
- **Produktivumgebung** für konkrete Projekte
- **Projekte wie `homeserver-agent`** als Framework-Nutzer
- **Eigene Datenbank** für Projekte, Ideen, Work Items
- **Keine Framework-Modifikationen** möglich
- **Framework als Dependency** über pip/GitHub

## 🏗️ Architektur-Modell

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Organization                     │
├─────────────────────────────────────────────────────────────┤
│  ai-lab-framework (Repository)                           │
│  ├── Framework Core                                      │
│  ├── Database Models (Framework-spezifisch)              │
│  ├── CLI Integration                                     │
│  └── Releases → PyPI                                   │
├─────────────────────────────────────────────────────────────┤
│  ai-lab (Repository)                                     │
│  ├── projects/                                           │
│  │   ├── homeserver-agent/ (Projekt)                     │
│  │   ├── other-project/ (Projekt)                        │
│  │   └── ...                                            │
│  ├── data/ (Instanz-DB)                                 │
│  ├── tools/ (Instanz-spezifische Tools)                  │
│  └── Depends on: ai-lab-framework (PyPI)                │
└─────────────────────────────────────────────────────────────┘
```

## 📦 Datenbank-Trennung

### Framework-Datenbank (`~/.ai-lab/framework.db`)
```sql
-- Framework-spezifische Tabellen
tool_executions     -- Tool-Ausführungs-Logs
tool_sessions       -- Kontext-Persistenz
tool_configurations -- Tool-Konfigurationen
tool_metrics        -- Performance-Metriken
framework_logs      -- Framework-Logging
```

### Instanz-Datenbank (`data/ai_lab.db`)
```sql
-- Instanz-spezifische Tabellen
projects           -- Projekte (homeserver-agent, etc.)
ideas              -- Ideen
work_items         -- Work Items
milestones         -- Meilensteine
github_repos       -- GitHub-Integration
```

## 🚀 Deployment-Prozess

### Framework Release-Prozess
1. **Entwicklung** in `ai-lab-framework` Repo
2. **Tests** mit `pytest` und CI/CD
3. **Versionierung** mit Semantic Versioning
4. **Release** auf GitHub mit Changelog
5. **Publish** auf PyPI als `ai-lab-framework`
6. **Installation** in Instanz mit `pip install ai-lab-framework`

### Instanz Update-Prozess
1. **Framework Update**: `pip install --upgrade ai-lab-framework`
2. **Datenbank-Migration**: `ai-lab-framework migrate-db`
3. **Kompatibilitäts-Check**: `ai-lab-framework check-compatibility`
4. **Neustart** der Instanz-Dienste

## 🔒 Immutable Framework Garantie

### Technische Maßnahmen
1. **Read-Only Installation** - Framework als pip-Package
2. **Keine Source-Modifikation** - Framework-Code nicht im Instanz-Repo
3. **Version-Pinning** - Explizite Version in `requirements.txt`
4. **Interface-Contracts** - Stabile APIs über Major-Versionen

### Organisatorische Maßnahmen
1. **Getrennte Repositories** - Kein Cross-Repo-Code
2. **Release-Management** - Formeller Release-Prozess
3. **Backward-Compatibility** - API-Stabilität garantieren
4. **Documentation** - Klare Interface-Dokumentation

## 📁 Verzeichnisstruktur

### Framework Repository (`ai-lab/ai-lab-framework`)
```
ai-lab-framework/
├── src/ai_lab_framework/
│   ├── __init__.py
│   ├── base_ai_tool.py
│   ├── profiles.py
│   ├── profile_validator.py
│   ├── tool_generator.py
│   └── db/
│       ├── __init__.py
│       ├── database.py
│       └── models.py
├── tests/
├── docs/
│   ├── FRAMEWORK_INSTANCE_SEPARATION.md
│   ├── DEPLOYMENT_GUIDE.md
│   └── API_REFERENCE.md
├── AGENTS.md
├── GEMINI.md
├── pyproject.toml
└── README.md
```

### Instanz Repository (`ai-lab/ai-lab`)
```
ai-lab/
├── projects/
│   ├── homeserver-agent/
│   │   ├── src/
│   │   │   └── integrations/
│   │   │       ├── github_integration.py
│   │   │       └── database_integration.py
│   │   ├── tools/
│   │   │   ├── fritzbox/
│   │   │   └── monitoring/
│   │   ├── data/
│   │   │   └── work-items/
│   │   └── pyproject.toml
│   └── other-project/
├── data/
│   ├── ai_lab.db
│   ├── schemas/
│   └── backups/
├── tools/
│   └── global-tools/
├── scripts/
│   ├── deploy.sh
│   └── backup.sh
├── config/
├── requirements.txt  # ai-lab-framework==1.0.0
└── README.md
```

## 🔄 Migrationsstrategie

### Phase 1: Vorbereitung
- [ ] Framework-Core extrahieren und bereinigen
- [ ] Framework-Datenbank-Modelle erstellen
- [ ] Instanz-spezifischen Code identifizieren
- [ ] GitHub-Repositories vorbereiten

### Phase 2: Trennung
- [ ] `ai-lab-framework` Repository erstellen
- [ ] Framework-Code verschieben und bereinigen
- [ ] Instanz-Code umorganisieren
- [ ] Abhängigkeiten anpassen

### Phase 3: Integration
- [ ] Framework als PyPI-Package veröffentlichen
- [ ] Instanz-Dependencies aktualisieren
- [ ] Deployment-Prozesse implementieren
- [ ] Dokumentation vervollständigen

### Phase 4: Validierung
- [ ] End-to-End-Tests durchführen
- [ ] Immutable-Framework überprüfen
- [ ] Performance-Tests durchführen
- [ ] Sicherheits-Review durchführen

## 📊 Projektmanagement-Einträge

### Work Items für Framework-Trennung

#### FRM-020: Framework Core Extraktion
- **Typ**: Framework
- **Priorität**: Critical
- **Status**: In Progress
- **Beschreibung**: Extrahiere Framework-Core aus ai-lab-clean in eigenes Repository
- **Akzeptanzkriterien**:
  - [ ] Framework-Code in `ai-lab-framework` Repo
  - [ ] Framework-Datenbank-Modelle implementiert
  - [ ] CI/CD für Framework eingerichtet
  - [ ] PyPI-Publishing konfiguriert

#### FRM-021: Instanz Datenbank-Trennung
- **Typ**: Framework  
- **Priorität**: High
- **Status**: To Do
- **Beschreibung**: Trenne Instanz-spezifische Daten von Framework-Daten
- **Akzeptanzkriterien**:
  - [ ] Instanz-DB enthält nur Projekte/Ideen/Work Items
  - [ ] Framework-DB enthält nur Tool-Execution/Logging
  - [ ] Migrations-Skripte für beide DBs
  - [ ] Backup/Restore-Prozesse

#### FRM-022: Immutable Framework Deployment
- **Typ**: Framework
- **Priorität**: High
- **Status**: To Do
- **Beschreibung**: Implementiere immutable Framework Deployment-Prozess
- **Akzeptanzkriterien**:
  - [ ] Framework als PyPI-Package installierbar
  - [ ] Version-Pinning in Instanz möglich
  - [ ] Automatische Updates mit Kompatibilitäts-Check
  - [ ] Rollback-Möglichkeit

#### FRM-023: Homeserver-Agent Projekt-Setup
- **Typ**: Framework
- **Priorität**: Medium
- **Status**: To Do
- **Beschreibung**: Organisiere homeserver-agent als Projekt innerhalb ai-lab Instanz
- **Akzeptanzkriterien**:
  - [ ] Projekt-Struktur unter `projects/homeserver-agent/`
  - [ ] Eigene `pyproject.toml` mit Framework-Dependency
  - [ ] Tools und Integrationen organisiert
  - [ ] Eigene Tests und Dokumentation

#### FRM-024: Dokumentation und Training
- **Typ**: Framework
- **Priorität**: Medium
- **Status**: To Do
- **Beschreibung**: Erstelle umfassende Dokumentation für Framework/Instanz-Trennung
- **Akzeptanzkriterien**:
  - [ ] Deployment-Guide erstellt
  - [ ] API-Referenz vervollständigt
  - [ ] Developer-Training-Material
  - [ ] Troubleshooting-Guide

## 🎯 Success-Kriterien

### Technische Ziele
- [ ] Framework ist eigenständiges PyPI-Package
- [ ] Instanz kann Framework nicht modifizieren
- [ ] Beide Datenbanken sind funktionsfähig
- [ ] Deployment-Prozess ist automatisiert
- [ ] Backward-Compatibility ist gewährleistet

### Organisatorische Ziele
- [ ] Klare Verantwortlichkeiten definiert
- [ ] Entwickler-Prozesse etabliert
- [ ] Dokumentation ist vollständig
- [ ] Team ist geschult

### Qualitätsziele
- [ ] Test-Coverage > 90%
- [ ] Performance-Regression < 5%
- [ ] Sicherheits-Review bestanden
- [ ] User-Feedback positiv

---

*Diese Planung ist die Grundlage für die erfolgreiche Trennung von Framework und Instanz.*