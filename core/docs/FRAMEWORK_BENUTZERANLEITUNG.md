# AI Lab Framework - Komplette Benutzeranleitung

**Ein verständlicher Leitfaden für alle mit Basic IT Wissen**

---

## 🎯 **Was ist das AI Lab Framework?**

Stell dir das AI Lab Framework wie ein **Baukasten-System für KI-Anwendungen** vor. Genau wie LEGO Steine, die du zusammensetzen kannst, um verschiedene Dinge zu bauen, bietet dieses Framework Bausteine für KI-Tools und Automatisierungen.

### 📦 **Die drei Repositorys**

Wir haben drei verschiedene "Kästen" mit Bausteinen:

1. **ai-lab** (Der Hauptkasten)
   - Enthält alles: Framework + Anleitungen + Werkzeuge
   - Für die meisten Anwender die beste Wahl

2. **ai-lab-framework** (Nur die Bausteine)
   - Nur das reine Framework ohne Beispiele
   - Für Entwickler, die nur die Kernfunktionen brauchen

3. **ai-lab-filled** (Baukasten + Anleitungen)
   - Framework + fertige Beispiele + Daten
   - Zum Lernen und Ausprobieren

---

## 🚀 **Schnellstart in 5 Minuten**

### 1️⃣ **Installation**

```bash
# Methode 1: Direkter Download (empfohlen für Anfänger)
git clone https://github.com/HerrSensei/ai-lab.git
cd ai-lab

# Methode 2: Über pip (für Python-Nutzer)
pip install ai-lab-framework
```

### 2️⃣ **Einrichtung**

```bash
# Python-Umgebung einrichten
python3 -m venv ai-lab-env
source ai-lab-env/bin/activate  # Auf Windows: ai-lab-env\Scripts\activate

# Abhängigkeiten installieren
pip install -r requirements.txt
```

### 3️⃣ **Erster Test**

```bash
# Framework testen
python -c "from ai_lab_framework import BaseAITool; print('✅ Framework funktioniert!')"

# Session starten (Logging)
python3 scripts/create_session_log.py --session-type work
```

**🎉 Herzlichen Glückwunsch! Du bist startklar!**

---

## 📁 **Die Ordner-Struktur einfach erklärt**

```
ai-lab/
├── 📂 src/ai_lab_framework/     # 🔧 Das Herzstück - alle KI-Funktionen
├── 📂 core/templates/            # 📋 Vorlagen für deine Projekte
├── 📂 data/schemas/             # 🗂️ Regeln und Formate
├── 📂 scripts/                  # 🛠️ Nützliche Werkzeuge
├── 📂 ai-logs/                  # 📊 Deine Arbeitsprotokolle
├── 📂 projects/                 # 🏗️ Beispielprojekte
└── 📄 README.md                 # 📖 Diese Anleitung
```

### Was ist wo?

| Ordner | Inhalt | Wofür brauchst du das? |
|--------|--------|------------------------|
| `src/ai_lab_framework/` | Die KI-Bausteine | Zum Bauen von KI-Tools |
| `core/templates/` | Projekt-Vorlagen | Zum schnellen Starten |
| `data/schemas/` | Daten-Formate | Zur Strukturierung von Daten |
| `scripts/` | Automatisierungs-Tools | Zur Zeitersparnis |
| `ai-logs/` | Arbeitsprotokolle | Zur Nachverfolgung |

---

## 🛠️ **Die wichtigsten Funktionen**

### 1️⃣ **BaseAITool - Die Grundlage**

Das ist die **Mutter aller KI-Tools** im Framework:

```python
from ai_lab_framework import BaseAITool

class MeinErstesTool(BaseAITool):
    def __init__(self):
        super().__init__()
        self.name = "Mein Tool"
        self.description = "Mein erstes KI-Tool"
    
    def execute(self, input_data):
        # Hier passiert die Magie!
        return f"KI verarbeitet: {input_data}"

# Benutzen:
tool = MeinErstesTool()
result = tool.execute("Hallo Welt")
print(result)  # → "KI verarbeitet: Hallo Welt"
```

### 2️⃣ **ProfileManager - Konfiguration einfach gemacht**

Stell dir Profile wie **Einstellungen für verschiedene Aufgaben** vor:

```python
from ai_lab_framework import ProfileManager

# Profile laden
profiles = ProfileManager()

# Verschiedene Profile für verschiedene Aufgaben
developer_profile = profiles.get_profile("developer")
researcher_profile = profiles.get_profile("researcher")

# Dein eigenes Profil erstellen
profiles.create_profile("my_profile", {
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 1000
})
```

### 3️⃣ **Database Integration - Daten speichern**

```python
from ai_lab_framework import AILabDatabase

# Datenbank verbinden
db = AILabDatabase("meine_daten.db")

# Arbeitsspeicher (Work Items) erstellen
db.create_work_item({
    "title": "Meine erste Aufgabe",
    "description": "Lerne das AI Lab Framework",
    "status": "in_progress",
    "priority": "high"
})

# Ideen speichern
db.create_idea({
    "title": "KI für Gartenarbeit",
    "description": "Ein Tool, das beim Gärtnern hilft",
    "category": "home_automation"
})
```

---

## 📋 **Templates - Deine Projekt-Vorlagen**

Templates sind wie **Kuchenrezepte** - du musst nicht jedes Mal von vorne anfangen!

### 🏗️ **Projekt-Templates**

#### 1️⃣ **AI/ML Projekt**
```bash
# Neues KI-Projekt erstellen
python -m ai_lab_framework create-project --template=ai_ml --name=mein_ki_projekt
```

**Was du bekommst:**
- Fertige Ordner-Struktur
- Beispiel-Code für Modelle
- Konfigurationsdateien
- Test-Dateien

#### 2️⃣ **Infrastructure Projekt**
```bash
# Infrastructure-Projekt
python -m ai_lab_framework create-project --template=infrastructure --name=meine_infra
```

**Was du bekommst:**
- Terraform-Vorlagen
- Docker-Konfigurationen
- Kubernetes-Dateien
- Monitoring-Setup

#### 3️⃣ **Hybrid Architecture**
```bash
# Hybrid-Projekt (KI + Infrastructure)
python -m ai_lab_framework create-project --template=hybrid_arch --name=mein_hybrid
```

### 🤖 **Agent OS Templates**

Für intelligente Agenten:

```yaml
# agent.yaml - Konfiguration für einen Agenten
name: "Mein Assistant"
type: "development_agent"
capabilities:
  - "code_generation"
  - "debugging"
  - "documentation"
tools:
  - "git_integration"
  - "file_operations"
  - "ai_chat"
```

---

## 🛠️ **Die wichtigsten Werkzeuge (Scripts)**

### 📊 **Session Logging**

**Was es tut:** Protokolliert deine Arbeit automatisch

```bash
# Neue Session starten
python3 scripts/create_session_log.py --session-type work

# Letzte Sessions ansehen
python3 scripts/create_session_log.py --list
```

**Warum nützlich:**
- Du siehst, was du wann gemacht hast
- Perfekt für die Teamarbeit
- Hilft bei der Fehlersuche

### 🚀 **Multi-Repository Management**

**Was es tut:** Synchronisiert Änderungen zwischen allen Repositorys

```bash
# Änderungen zu allen Repositorys pushen
python3 scripts/push_to_all_repos.py --message="Update documentation"

# Nur zu bestimmten Repositorys
python3 scripts/push_to_all_repos.py --repos="ai-lab,ai-lab-framework" --message="Fix bug"

# Status prüfen
python3 scripts/push_to_all_repos.py --status
```

### 🏷️ **Release Management**

**Was es tut:** Erstellt neue Versionen automatisch

```bash
# Neue Version erstellen
python3 scripts/create_release.py --version=v1.2.0

# Mit automatischem Deployment
python3 scripts/create_release.py --version=v1.2.0 --auto-deploy
```

---

## 🎯 **Praktische Beispiele**

### Beispiel 1️⃣: Einfacher Text-Analyzer

```python
from ai_lab_framework import BaseAITool
import re

class TextAnalyzer(BaseAITool):
    def __init__(self):
        super().__init__()
        self.name = "Text Analyzer"
        self.description = "Analysiert Texte und gibt Statistiken"
    
    def execute(self, text):
        # Wörter zählen
        words = len(text.split())
        
        # Sätze zählen
        sentences = len(re.split(r'[.!?]+', text))
        
        # Zeichen zählen
        chars = len(text)
        
        return {
            "words": words,
            "sentences": sentences,
            "characters": chars,
            "avg_words_per_sentence": words / max(sentences, 1)
        }

# Benutzen
analyzer = TextAnalyzer()
result = analyzer.execute("Hallo Welt! Wie geht es dir? Mir geht's gut.")
print(result)
# → {'words': 9, 'sentences': 3, 'characters': 47, 'avg_words_per_sentence': 3.0}
```

### Beispiel 2️⃣: GitHub Issue Manager

```python
from ai_lab_framework import BaseAITool, GitHubIntegration

class IssueManager(BaseAITool):
    def __init__(self, github_token):
        super().__init__()
        self.github = GitHubIntegration(github_token)
        self.name = "Issue Manager"
    
    def execute(self, repo_name, issue_data):
        # Issue erstellen
        issue = self.github.create_issue(repo_name, issue_data)
        
        # In lokaler Datenbank speichern
        db = AILabDatabase()
        db.create_work_item({
            "title": issue_data["title"],
            "description": issue_data["body"],
            "github_issue_id": issue["id"],
            "status": "open"
        })
        
        return issue

# Benutzen
manager = IssueManager("dein_github_token")
issue = manager.execute("HerrSensei/ai-lab", {
    "title": "Neues Feature vorschlagen",
    "body": "Ich hätte gerne ein Feature für...",
    "labels": ["enhancement"]
})
```

### Beispiel 3️⃣: Automatischer Dokumentations-Generator

```python
from ai_lab_framework import BaseAITool
import os
from pathlib import Path

class DocGenerator(BaseAITool):
    def __init__(self):
        super().__init__()
        self.name = "Documentation Generator"
    
    def execute(self, project_path):
        docs = {}
        
        # Python-Dateien analysieren
        for py_file in Path(project_path).rglob("*.py"):
            with open(py_file) as f:
                content = f.read()
                
            # Klassen und Funktionen finden
            classes = re.findall(r'class (\w+)', content)
            functions = re.findall(r'def (\w+)', content)
            
            docs[str(py_file)] = {
                "classes": classes,
                "functions": functions,
                "lines": len(content.split('\n'))
            }
        
        # README.md erstellen
        readme_content = f"# Projekt-Dokumentation\n\n"
        readme_content += f"## Übersicht\n\n"
        readme_content += f"- Python-Dateien: {len(docs)}\n"
        readme_content += f"- Gesamtzeilen: {sum(d['lines'] for d in docs.values())}\n\n"
        
        for file_path, info in docs.items():
            readme_content += f"## {file_path}\n\n"
            readme_content += f"- Klassen: {', '.join(info['classes'])}\n"
            readme_content += f"- Funktionen: {', '.join(info['functions'])}\n\n"
        
        # Speichern
        with open(os.path.join(project_path, "AUTO_README.md"), "w") as f:
            f.write(readme_content)
        
        return {"generated_file": "AUTO_README.md", "analyzed_files": len(docs)}

# Benutzen
generator = DocGenerator()
result = generator.execute("/pfad/zum/projekt")
print(result)
```

---

## 🔧 **Troubleshooting - Häufige Probleme**

### ❌ **Problem: "ImportError: No module named 'ai_lab_framework'"**

**Lösung:**
```bash
# 1. Im richtigen Ordner?
pwd  # Sollte im ai-lab Ordner sein

# 2. Python-Pfad setzen
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# 3. Neu installieren
pip install -e .
```

### ❌ **Problem: "Permission denied" bei Scripts**

**Lösung:**
```bash
# Scripts ausführbar machen
chmod +x scripts/*.py

# Oder mit python3 ausführen
python3 scripts/create_session_log.py
```

### ❌ **Problem: Git funktioniert nicht**

**Lösung:**
```bash
# Git konfigurieren
git config --global user.name "Dein Name"
git config --global user.email "deine.email@example.com"

# SSH-Key einrichten (oder HTTPS verwenden)
ssh-keygen -t ed25519 -C "deine.email@example.com"
```

### ❌ **Problem: Datenbank-Fehler**

**Lösung:**
```bash
# Datenbank neu erstellen
rm -f data/*.db
python -c "from ai_lab_framework import AILabDatabase; AILabDatabase().init_db()"
```

---

## 📚 **Best Practices - So arbeitest du effizient**

### 🎯 **1. Sessions immer starten**

```bash
# Jede Arbeitssession beginnen mit:
python3 scripts/create_session_log.py --session-type work
```

**Warum?** Du hast später eine perfekte Übersicht, was du wann gemacht hast.

### 🔄 **2. Regelmäßig speichern**

```bash
# Nach wichtigen Änderungen:
python3 scripts/push_to_all_repos.py --message="Wichtiger Meilenstein erreicht"
```

### 📋 **3. Work Items nutzen**

```python
# Aufgaben im System verfolgen
db = AILabDatabase()
db.create_work_item({
    "title": "Dokumentation schreiben",
    "status": "todo",
    "priority": "medium"
})
```

### 🏗️ **4. Templates verwenden**

```bash
# Nicht das Rad neu erfinden!
python -m ai_lab_framework list-templates
python -m ai_lab_framework create-project --template=passende_vorlage
```

### 🧪 **5. Tests schreiben**

```python
# Einfache Tests für deine Tools
def test_mein_tool():
    tool = MeinErstesTool()
    result = tool.execute("Test")
    assert "Test" in result
```

---

## 🚀 **Nächste Schritte**

### 🎓 **Lernpfad für Anfänger**

1. **Woche 1:** Grundlagen verstehen
   - [ ] Installation durchführen
   - [ ] Ordner-Struktur erkunden
   - [ ] Erstes einfaches Tool bauen

2. **Woche 2:** Templates nutzen
   - [ ] Projekt mit Template erstellen
   - [ ] Vorlagen anpassen
   - [ ] Eigene Vorlage bauen

3. **Woche 3:** Automatisierung
   - [ ] Session Logging nutzen
   - [ ] Multi-Repo Management verstehen
   - [ ] Eigene Scripts schreiben

4. **Woche 4:** Fortgeschrittene Features
   - [ ] GitHub Integration nutzen
   - [ ] Datenbank anpassen
   - [ ] CI/CD verstehen

### 🎯 **Projekt-Ideen zum Üben**

1. **📝 Notizen-Manager**
   - Speichert Notizen in Datenbank
   - Kategorisiert automatisch
   - Exportiert als Markdown

2. **📊 Projekt-Tracker**
   - Verfolgt Projekt-Fortschritt
   - Erzeugt Berichte
   - Sendet Erinnerungen

3. **🤖 Chat-Bot**
   - Beantwortet Fragen zum Framework
   - Lernt aus Gesprächen
   - Integriert mit Dokumentation

4. **🔧 Code-Refactorer**
   - Analysiert Python-Code
   - Schlägt Verbesserungen vor
   - Automatisiert Refactoring

---

## 🆘 **Hilfe und Community**

### 📖 **Dokumentation**

- **Online:** https://github.com/HerrSensei/ai-lab
- **Lokal:** `docs/` Ordner im Projekt
- **API-Referenz:** `docs/api/`

### 💬 **Community**

- **Issues:** https://github.com/HerrSensei/ai-lab/issues
- **Discussions:** https://github.com/HerrSensei/ai-lab/discussions
- **Wiki:** https://github.com/HerrSensei/ai-lab/wiki

### 🐛 **Fehler melden**

```bash
# Fehler-Report erstellen
python3 scripts/create_session_log.py --session-type debug
# Issue auf GitHub mit Log-Datei erstellen
```

### 🎓 **Tutorials**

- **Video-Tutorials:** YouTube Channel
- **Written Guides:** Blog Posts
- **Examples:** `examples/` Ordner

---

## 🎉 **Zusammenfassung**

Das AI Lab Framework ist dein **persönlicher Baukasten für KI-Anwendungen**. Mit den richtigen Vorlagen und Werkzeugen kannst du schnell und einfach professionelle KI-Tools bauen, ohne alles von Grund auf neu entwickeln zu müssen.

### 🎯 **Die wichtigsten Punkte**

1. **🏗️ Struktur:** Drei Repositorys für verschiedene Bedürfnisse
2. **🛠️ Werkzeuge:** Fertige Scripts für Automatisierung
3. **📋 Templates:** Projekt-Vorlagen für schnellen Start
4. **📊 Logging:** Automatische Protokollierung deiner Arbeit
5. **🔄 Integration:** GitHub, Datenbanken und mehr

### 🚀 **Dein nächster Schritt**

```bash
# 1. Repository klonen
git clone https://github.com/HerrSensei/ai-lab.git
cd ai-lab

# 2. Session starten
python3 scripts/create_session_log.py --session-type learning

# 3. Erstes Projekt erstellen
python -m ai_lab_framework create-project --template=ai_ml --name=mein_erstes_ki_projekt

# 4. Loslegen!
cd mein_erstes_ki_projekt
```

**Viel Erfolg beim Bauen deiner KI-Anwendungen! 🎉**

---

*Diese Anleitung wird kontinuierlich aktualisiert. Schau regelmäßig nach neuen Versionen!*

**Letzte Aktualisierung:** November 2025  
**Version:** 1.0  
**Autor:** AI Lab Framework Team