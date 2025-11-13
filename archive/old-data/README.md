# AI Lab Framework

## 🎯 Zweck & Vision

Dieses AI Lab Framework dient als zentrale Struktur für die Entwicklung von KI-Projekten. Es standardisiert Best Practices, beschleunigt die Entwicklung und stellt sicher, dass alle Projekte konsistente Qualitätsstandards einhalten.

## 🚀 Schnellstart

**📖 Complete Getting Started Guide**: [GETTING_STARTED.md](./GETTING_STARTED.md)

### Quick Overview
```bash
# 1. Framework setup
make setup

# 2. Create project
./core/tools/project-creator/bin/project-creator

# 3. Start development
cd projects/your-project && make dev

# 4. AI assistant support
make ai-assistant
```

## 📊 Dashboard & Monitoring

### Aktuelles Projekt-Status
Das **[AI Lab Dashboard](./dashboard/DASHBOARD.md)** bietet einen schnellen Überblick über alle Projekte:

- 📈 **Gesamt-Statistiken** - Fortschritt, Blocker, Prioritäten
- 🎯 **Projekt-Details** - Status, nächste Schritte, Empfehlungen
- 🚨 **Gesamt-Empfehlungen** - Ressourcen-Fokus, kritische Issues

### Dashboard aktualisieren
```bash
# Dashboard neu generieren
./dashboard/update_dashboard.sh

# Oder direkt mit Python
python dashboard/dashboard_generator.py
```



## 📋 Documentation

### Getting Started
- **[GETTING_STARTED.md](./GETTING_STARTED.md)** - 🚖 Complete setup and project creation guide
- **[DEVELOPER_GUIDE.md](./DEVELOPER_GUIDE.md)** - 📖 In-depth developer documentation
- **[AI_GUIDE.md](./AI_GUIDE.md)** - 🤖 Specific instructions for AI agents
- **[core/docs/FRAMEWORK_STRUCTURE.md](./core/docs/FRAMEWORK_STRUCTURE.md)** - 🏗️ Authoritative framework structure

### Framework Core
- **[core/guidelines/DECISIONS.md](./core/guidelines/DECISIONS.md)** - Detaillierte Begründung aller Architektur-Entscheidungen
- **[core/guidelines/GUIDELINES.md](./core/guidelines/GUIDELINES.md)** - Allgemeine Richtlinien und Standards
- **[core/guidelines/VISION.md](./core/guidelines/VISION.md)** - Vision und langfristige Ziele
- **[core/docs/](./core/docs/)** - Ausführliche Dokumentation und Tutorials

### Tools
- **[core/tools/project-creator/](./core/tools/project-creator/)** - Project Creator Tool
- **[core/tools/framework-setup/](./core/tools/framework-setup/)** - Framework Setup Tool
- **[core/tools/ai-assistant/](./core/tools/ai-assistant/)** - AI Assistant Integration

## 🎯 Design-Prinzipien

### 1. **Einfachheit vor Komplexität**
- Jede Komponente sollte einen klaren Zweck haben
- Vermeidung von übermäßiger Abstraktion
- Fokus auf Developer Experience

### 2. **Konsistenz**
- Einheitliche Code-Standards über alle Projekte
- Standardisierte Projektstrukturen
- Gemeinsame Tooling und Prozesse

### 3. **Skalierbarkeit**
- Modularer Aufbau für einfache Erweiterung
- Trennung von Concerns
- Wiederverwendbarkeit von Komponenten

### 4. **Sicherheit**
- Security by Design
- Standardisierte Sicherheitspraktiken
- Automatisierte Security-Checks

## 🛠️ Technologie-Stack

### Core-Technologien
- **Python 3.11+**: Hauptprogrammiersprache
- **Poetry**: Dependency Management
- **Docker**: Containerisierung
- **FastAPI**: API-Framework

### AI/ML Frameworks
- **LangChain**: LLM-Orchestrierung
- **LlamaIndex**: RAG-Framework
- **Transformers**: Hugging Face Modelle
- **OpenAI SDK**: OpenAI Integration

### Development Tools
- **Black**: Code-Formatierung
- **Ruff**: Linting und Formatting
- **MyPy**: Type Checking
- **Pytest**: Testing Framework

### AI Assistant Tools
- **opencode**: OpenAI-basierter KI-Assistent
- **gemini-cli**: Google Gemini KI-Assistent

## 🔄 Workflow

### 1. **Projekt-Initialisierung**
```bash
# Framework Setup (einmalig)
make setup

# Geführte Projekterstellung
./core/tools/project-creator/bin/project-creator

# Oder mit spezifischem Typ
./core/tools/project-creator/bin/project-creator --type ai_ml mein-ml-projekt
```

### 2. **Entwicklung**
```bash
# Zum Projekt wechseln
cd projects/projekt-name

# Entwicklungsumgebung starten
make dev

# Diagramme aktualisieren
make diagrams
```

### 3. **KI-Unterstützte Entwicklung**
```bash
# Projekt mit KI-Assistent öffnen
make ai-assistant

# Spezifischen Assistenten verwenden
make open-with-opencode projects/projekt-name
make open-with-gemini projects/projekt-name

# KI-Tools prüfen
make check-ai-tools
```

### 4. **Testing**
```bash
make test      # Führt alle Tests durch
make lint      # Code-Qualität Checks
make diagrams-test  # Teste Diagramm-Tools
```

## 📚 Nächste Schritte

### Für Entwickler
1. **[GETTING_STARTED.md](./GETTING_STARTED.md) durchführen** - Vollständiges Setup
2. **[DEVELOPER_GUIDE.md](./DEVELOPER_GUIDE.md) lesen** - Tiefgehende Dokumentation
3. **[core/guidelines/DECISIONS.md](./core/guidelines/DECISIONS.md) lesen** - Architektur-Entscheidungen
4. **Framework-Struktur verstehen** in [core/docs/FRAMEWORK_STRUCTURE.md](./core/docs/FRAMEWORK_STRUCTURE.md)

### Für KI-Agenten
1. **[AI_GUIDE.md](./AI_GUIDE.md) lesen** - Pflichtanweisungen
2. **[GETTING_STARTED.md](./GETTING_STARTED.md) für Kontext** - Framework-Verständnis
3. **[core/docs/FRAMEWORK_STRUCTURE.md](./core/docs/FRAMEWORK_STRUCTURE.md) respektieren** - Single Source of Truth

### Wichtige Referenzen
- **🏗️ Struktur**: [core/docs/FRAMEWORK_STRUCTURE.md](./core/docs/FRAMEWORK_STRUCTURE.md) (Autoritative Quelle)
- **📖 Entwickler**: [DEVELOPER_GUIDE.md](./DEVELOPER_GUIDE.md) (Vollständige Anleitung)
- **🤖 KI-Agenten**: [AI_GUIDE.md](./AI_GUIDE.md) (Pflichtanweisungen)

## 🤝 Beitrag

Dieses Framework ist lebendig und wird kontinuierlich verbessert. Beiträge sind willkommen!

### Verbesserungsvorschläge
- Erstelle ein Issue für neue Features
- Reiche Pull Requests für Verbesserungen ein
- Teile Best Practices aus deinen Projekten
