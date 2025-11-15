# AI Lab Richtlinien & Standards

## 🎯 Einleitung

Dieses Dokument definiert die verbindlichen Richtlinien und Standards für alle Projekte im AI Lab. Diese Standards sorgen für Konsistenz, Qualität und Wartbarkeit über alle Projekte hinweg.

---

## 🐍 Code-Standards

### Python-Version
- **Required**: Python 3.11+
- **Begründung**: Beste Performance und moderne Features

### Code-Formatierung
```bash
# Formatierung
black .
# Import-Sortierung
isort .
# Linting
ruff check .
# Type-Checking
mypy .
```

### Namenskonventionen
```python
# Variablen und Funktionen: snake_case
user_name = "john"
def process_data():
    pass

# Klassen: PascalCase
class DataProcessor:
    pass

# Konstanten: UPPER_CASE
MAX_RETRIES = 3

# Private: _leading_underscore
def _internal_method():
    pass
```

### Framework-Namenskonventionen (verbindlich)
- **Verzeichnisse**: `kebab-case` (z.B. `project-creator`, `framework-setup`, `work-items`)
- **Code-Dateien**: `snake_case` (z.B. `setup_ai_lab.sh`, `create_project.py`)
- **Dokumentations-Dateien**: `kebab-case.md` (z.B. `getting-started.md`, `troubleshooting.md`)
- **Work Items**: `PREFIX-###_beschreibung.md` (z.B. `HS-001_netzwerk-fixen.md`, `HYB-001_hybrid-architektur.md`)
- **Templates**: `[name].[extension].template` (z.B. `README.md.template`, `config.yaml.template`)

### Template-Platzhalter (verbindlich)
- **Format**: `{{ variable_name }}` (immer mit Leerzeichen)
- **Beispiele**: `{{ project_name }}`, `{{ work_item_id }}`, `{{ creation_date }}`
- **Filter**: `{{ variable_name|filter }}` (z.B. `{{ project_name|upper }}`)
- **Verboten**: `$VARIABLE`, `{{{variable}}}`, `{{variable}}` (ohne Leerzeichen)

**Platzhalter-Beispiele:**
✅ `{{ project_name }}` (korrekt)
✅ `{{ work_item_id|upper }}` (mit Filter)
❌ `{{project_name}}` (keine Leerzeichen)
❌ `$PROJECT_NAME` (falsches Format)
❌ `{{{project_name}}}` (dreifache Klammern)

**Beispiele:**
✅ `project-creator/` (Verzeichnis: kebab-case)
✅ `setup_ai_lab.sh` (Skript: snake_case)
✅ `getting-started.md` (Dokumentation: kebab-case)
✅ `HS-001_netzwerk-fixen.md` (Work Item: PREFIX-###_beschreibung)
✅ `README.md.template` (Template: name.extension.template)

❌ `projectCreator/` (falsches Verzeichnis-Format)
❌ `setupAiLab.sh` (falsches Skript-Format)
❌ `gettingStarted.md` (falsches Dokumentations-Format)
❌ `netzwerkfixen.md` (Work Item ohne Prefix/Nummer)

### Type Hints (Pflicht)
```python
from typing import List, Dict, Optional
from pydantic import BaseModel

def process_users(users: List[Dict[str, str]]) -> Optional[str]:
    """Process a list of users."""
    return users[0].get("name") if users else None

class UserResponse(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
```

### Docstring-Format (Google Style)
```python
def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate similarity between two texts.

    Args:
        text1: First text for comparison.
        text2: Second text for comparison.

    Returns:
        Similarity score between 0.0 and 1.0.

    Raises:
        ValueError: If either text is empty.
    """
    if not text1 or not text2:
        raise ValueError("Texts cannot be empty")
    return 0.5
```

---

## 📁 Projektstruktur-Standards

### Pflicht-Ordner in jedem Projekt
```
project-name/
├── src/                    # Source Code (Pflicht)
├── tests/                   # Tests (Pflicht)
├── docs/                    # Projekt-Dokumentation (Pflicht)
├── prompts/                 # Prompt-Templates (Pflicht bei AI-Projekten)
├── data/                    # Daten (Optional)
├── notebooks/               # Experimente (Optional)
├── config/                  # Konfigurationen (Optional)
└── deployment/              # Deployment-Konfig (Optional)
```

### Datei-Namenskonventionen
- **Verzeichnisse**: `kebab-case` (z.B. `project-creator`, `framework-setup`)
- **Python-Module**: `snake_case.py`
- **Konfigurationen**: `kebab-case.yaml` oder `kebab-case.json`
- **Dokumentation**: `kebab-case.md`
- **Notebooks**: `Descriptive_Case.ipynb`
- **Work Items**: `PREFIX-###_beschreibung.md` Format (z.B. `HS-001_netzwerk-fixen.md`)
- **Templates**: `[name].[extension].template` (z.B. `README.md.template`, `main.py.template`)

---

## 🧪 Testing-Standards

### Test-Struktur
```
tests/
├── unit/                   # Unit Tests (Pflicht)
├── integration/            # Integration Tests (Pflicht)
├── e2e/                   # End-to-End Tests (Optional)
├── fixtures/              # Test-Daten (Pflicht)
└── conftest.py           # pytest Konfiguration (Pflicht)
```

### Test-Coverage
- **Minimum**: 80% Code-Coverage
- **Ziel**: 90% für kritische Komponenten
- **Ausnahme**: Experimenteller Code: 60%

### Test-Namenskonventionen
```python
class TestUserService:
    def test_create_user_success(self):
        """Test successful user creation."""
        pass

    def test_create_user_duplicate_email_raises_error(self):
        """Test that duplicate email raises appropriate error."""
        pass

    def test_create_user_with_invalid_data(self):
        """Test user creation with various invalid inputs."""
        pass
```

### AI-spezifische Tests
```python
def test_prompt_consistency():
    """Test that prompt produces consistent results."""
    pass

def test_model_output_format():
    """Test that model output matches expected schema."""
    pass

def test_cost_limits():
    """Test that API calls stay within cost limits."""
    pass
```

---

## 🔐 Security-Standards

### API Key Management
- **NIEMALS** Keys im Code speichern
- **IMMER** Environment-Variablen verwenden
- **PFLICHT**: `.env.example` mit allen benötigten Variablen

```python
# ❌ FALSCH
api_key = "sk-1234567890"

# ✅ RICHTIG
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is required")
```

### Input Validation
```python
from pydantic import BaseModel, validator
import re

class PromptRequest(BaseModel):
    text: str
    max_tokens: int = 100

    @validator('text')
    def validate_text(cls, v):
        if len(v) > 10000:
            raise ValueError("Text too long")
        # Basic injection prevention
        if any(pattern in v.lower() for pattern in ['system:', 'admin:', 'debug']):
            raise ValueError("Invalid characters in prompt")
        return v

    @validator('max_tokens')
    def validate_max_tokens(cls, v):
        if v < 1 or v > 4000:
            raise ValueError("Max tokens must be between 1 and 4000")
        return v
```

### Output Filtering
```python
def filter_pii(text: str) -> str:
    """Filter personally identifiable information."""
    # Email filtering
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
    # Phone filtering
    text = re.sub(r'\b\d{3}-\d{3}-\d{4}\b', '[PHONE]', text)
    # SSN filtering
    text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN]', text)
    return text
```

---

## 📊 Monitoring & Logging-Standards

### Logging-Level
```python
import logging

# DEBUG: Detaillierte Informationen für Debugging
logger.debug("Processing prompt: %s", prompt[:50])

# INFO: Allgemeine Informationen
logger.info("User %s created new chat session", user_id)

# WARNING: Unerwartete Situationen
logger.warning("Rate limit approaching for user %s", user_id)

# ERROR: Fehler, die nicht fatal sind
logger.error("API call failed: %s", str(e))

# CRITICAL: Fatale Fehler
logger.critical("Database connection lost")
```

### Strukturiertes Logging
```python
import structlog

logger = structlog.get_logger()

logger.info(
    "api_call_completed",
    user_id=user_id,
    model="gpt-4",
    tokens_used=tokens,
    cost=cost,
    duration_ms=duration
)
```

### Metriken (Pflicht)
Jede API muss folgende Metriken tracken:
- **Request Count**: Gesamtzahl der Anfragen
- **Response Time**: Durchschnittliche Antwortzeit
- **Error Rate**: Fehlerrate
- **Cost Tracking**: API-Kosten
- **Token Usage**: Verbrauchte Tokens

---

## 🚀 Deployment-Standards

### Environment-Variablen (Pflicht)
```bash
# .env.example (Pflicht in jedem Projekt)
OPENAI_API_KEY=your_openai_key_here
DATABASE_URL=postgresql://user:pass@localhost/db
REDIS_URL=redis://localhost:6379
LOG_LEVEL=INFO
ENVIRONMENT=development
MAX_TOKENS_PER_REQUEST=1000
COST_BUDGET_PER_DAY=100
```

### Docker-Standards
```dockerfile
# Multi-stage build (Pflicht)
FROM python:3.11-slim as builder
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry config virtualenvs.create false
RUN poetry install --only=main

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY src/ ./src/
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Health Checks (Pflicht)
```python
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Check database
        db_status = await check_database()
        # Check external APIs
        api_status = await check_external_apis()

        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "checks": {
                "database": db_status,
                "external_apis": api_status
            }
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
```

---

## 📝 Dokumentations-Standards

### README.md (Pflicht)
Jedes Projekt muss eine README.md mit folgenden Sektionen haben:
```markdown
# Project Name

## Description
Kurze Beschreibung (2-3 Sätze)

## Quick Start
Installation und erster Start

## Usage
Haupt-Use Cases mit Code-Beispielen

## API Documentation
Link zur API-Dokumentation

## Development
Setup für Entwickler

## Testing
Wie Tests ausgeführt werden

## Deployment
Deployment-Anleitung

## Contributing
Wie man beitragen kann

## License
Lizenz-Informationen
```

### API-Dokumentation (Pflicht)
- Automatisch generiert mit FastAPI/OpenAPI
- Manuelle Ergänzungen für komplexe Endpunkte
- Beispiele für jeden Endpunkt

### Changelog (Pflicht)
```markdown
# Changelog

## [1.2.0] - 2024-01-15
### Added
- New feature X
- Support for model Y

### Changed
- Improved performance of Z

### Fixed
- Bug in authentication

### Deprecated
- Old endpoint will be removed in v2.0
```

---

## 🤖 AI-spezifische Standards

### Prompt-Management
```python
# prompts/system_prompts.yaml
chatbot:
  version: "1.0"
  template: |
    You are a helpful assistant named {name}.
    Your goal is to {goal}.

    Guidelines:
    - Be concise and helpful
    - Ask clarifying questions if needed
    - Never share sensitive information

  variables:
    - name: str
    - goal: str

  constraints:
    max_length: 1000
    forbidden_topics: ["politics", "religion"]
```

### Model-Konfiguration
```python
# config/models.yaml
openai:
  gpt-4:
    max_tokens: 4000
    temperature: 0.7
    top_p: 0.9
    frequency_penalty: 0.0
    presence_penalty: 0.0

  gpt-3.5-turbo:
    max_tokens: 3000
    temperature: 0.5
    cost_per_token: 0.000002
```

### Cost-Management
```python
class CostTracker:
    def __init__(self, daily_budget: float):
        self.daily_budget = daily_budget
        self.daily_spend = 0.0

    def can_make_request(self, estimated_tokens: int) -> bool:
        estimated_cost = self.estimate_cost(estimated_tokens)
        return (self.daily_spend + estimated_cost) <= self.daily_budget

    def track_usage(self, tokens: int, model: str):
        cost = self.calculate_cost(tokens, model)
        self.daily_spend += cost

        if self.daily_spend > self.daily_budget * 0.8:
            logger.warning("Approaching daily budget limit: %.2f/%.2f",
                         self.daily_spend, self.daily_budget)
```

---

## 🔄 Git-Standards

### Commit-Nachrichten (Conventional Commits)
```
feat: add user authentication
fix: resolve memory leak in data processing
docs: update API documentation
style: format code with black
refactor: simplify prompt validation logic
test: add integration tests for chat endpoint
chore: update dependencies
```

### Branch-Strategie
```
main                    # Production-ready code
develop                 # Integration branch
feature/user-auth       # Feature branches
hotfix/critical-bug     # Hotfixes
release/v1.2.0         # Release preparation
```

### Pull Request-Standards
- **Title**: Conventional Commit Format
- **Description**: Was wurde geändert und warum
- **Tests**: Alle Tests müssen grün sein
- **Review**: Mindestens ein Review erforderlich
- **Documentation**: Docs müssen aktualisiert sein

---

## 📋 Quality Gates

### Pre-commit Hooks (Pflicht)
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black

  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.0.261
    hooks:
      - id: ruff

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.0.1
    hooks:
      - id: mypy
```

### CI/CD Pipeline (Pflicht)
1. **Linting**: Code-Qualität Checks
2. **Testing**: Alle Tests durchführen
3. **Security**: Security-Scans
4. **Build**: Docker Image bauen
5. **Deploy**: Zu Staging deployen

### Release-Prozess
1. **Version bump**: SemVer Version erhöhen
2. **Changelog**: Änderungen dokumentieren
3. **Tag**: Git Tag erstellen
4. **Build**: Release-Artefakte bauen
5. **Deploy**: Zu Production deployen

---

## ⚡ Performance-Standards

### Response Time
- **API Endpoints**: < 500ms (95th percentile)
- **LLM Calls**: < 30s (mit Timeout)
- **Database Queries**: < 100ms

### Memory Usage
- **Max Memory**: 512MB für einfache APIs
- **Memory Leaks**: Keine Memory Leaks erlaubt
- **Monitoring**: Memory-Nutzung tracken

### Caching
```python
from functools import lru_cache
import redis

# In-memory cache für häufige Anfragen
@lru_cache(maxsize=1000)
def get_prompt_template(template_name: str):
    return load_template(template_name)

# Redis cache für API-Antworten
def cache_api_response(key: str, data: dict, ttl: int = 300):
    redis_client.setex(key, ttl, json.dumps(data))
```

---

## 🚨 Compliance & Rechtliches

### Data Privacy
- **PII Protection**: Automatische PII-Erkennung und -Filterung
- **Data Retention**: Keine längere Speicherung als nötig
- **GDPR**: DSGVO-Konformität für EU-Daten

### Model Usage
- **Terms of Service**: Einhaltung der LLM-Provider ToS
- **Attribution**: Korrekte Attribution bei generierten Inhalten
- **Copyright**: Keine Copyright-Verletzungen

### Audit Trail
```python
def log_ai_interaction(user_id: str, prompt: str, response: str, model: str):
    """Log all AI interactions for audit purposes."""
    audit_log = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": user_id,
        "prompt_hash": hashlib.sha256(prompt.encode()).hexdigest(),
        "response_hash": hashlib.sha256(response.encode()).hexdigest(),
        "model": model,
        "tokens_used": count_tokens(prompt + response)
    }
    # Store in secure, immutable storage
    audit_db.store(audit_log)
```

---

## 📦 Dependency Management (KISS-Prinzip)

### Golden Rule: Minimal Dependencies
**Installiere NUR was du wirklich verwendest - nicht was du "vielleicht" brauchst!**

### Richtlinien für Dependencies

#### 1. Starte immer minimal
```toml
# Anfang - NUR das was du sicher brauchst
[tool.poetry.dependencies]
python = "^3.11"

# Füge NUR hinzu was du tatsächlich im Code importierst
```

#### 2. Common Anti-Patterns (VERBOTEN)
❌ **"Just in Case" Dependencies**
```toml
# FALSCH: Database "vielleicht" später gebraucht
sqlalchemy = "^2.0.0"  # Wird nirgends importiert!

# FALSCH: Alle AI Libraries "für completeness"
openai = "^1.3.0"      # Wird nicht verwendet
anthropic = "^0.7.0"    # Wird nicht verwendet
langchain = "^0.0.350"  # Wird nicht verwendet
```

❌ **"Standard Setup" Kopieren**
```toml
# FALSCH: Kopiere nicht einfach von anderen Projekten
# Jedes Projekt ist anders!
```

#### 3. Correct Approach (ERLAUBT)
✅ **Need-Based Installation**
```toml
# RICHTIG: Nur was im Code tatsächlich verwendet wird
[tool.poetry.dependencies]
python = "^3.11"

# Web-API? → FastAPI
fastapi = "^0.104.1"
uvicorn = {extras = ["standard"], version = "^0.24.0"}

# AI-Integration? → OpenAI (nur wenn verwendet!)
openai = "^1.3.0"  # Nur wenn `import openai` im Code steht
```

#### 4. Dependency Check Process
Bevor du eine Dependency hinzufügst:

1. **Code Check:** Wird diese Library tatsächlich importiert?
2. **Single Purpose:** Kann ich das ohne diese Library lösen?
3. **Alternative:** Gibt es eine leichtere Alternative?
4. **Future Proof:** Brauche ich das wirklich oder nur "vielleicht"?

#### 5. Beispiele für minimale Setups

**CLI Tool:**
```toml
[tool.poetry.dependencies]
python = "^3.11"
click = "^8.1.0"  # CLI Framework
```

**Simple Web API:**
```toml
[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.104.1"
uvicorn = {extras = ["standard"], version = "^0.24.0"}
```

**AI Service:**
```toml
[tool.poetry.dependencies]
python = "^3.11"
openai = "^1.3.0"  # Nur wenn OpenAI verwendet wird
```

**Data Processing:**
```toml
[tool.poetry.dependencies]
python = "^3.11"
pandas = "^2.1.0"  # Nur wenn Daten verarbeitet werden
```

#### 6. Template Usage
Im Framework-Template sind ALLE Dependencies standardmäßig auskommentiert. Entwickler MÜSSEN bewusst entscheiden, was sie benötigen.

---

## 🏗️ Framework-Struktur-Standards

### Golden Rule: Single Source of Truth
**Alles Framework-relevante gehört in `core/`** - dies stellt Konsistenz, Wartbarkeit und Klarheit sicher.

### Framework-Verzeichnisstruktur
```
ai-lab/
├── core/                           # 🏗️ FRAMEWORK CORE (Alles Framework-relevante)
│   ├── docs/                       # 📚 Framework-Dokumentation
│   │   ├── analyses/               # Analysen & Forschungsergebnisse
│   │   ├── research/               # Research-Ergebnisse
│   │   ├── FRAMEWORK_STRUCTURE.md  # Struktur-Dokumentation
│   │   ├── PROJECT_CONTEXT.md      # Framework-Kontext für KI-Tools
│   │   └── README.md               # Framework-Doku-Übersicht
│   ├── guidelines/                 # 📋 Richtlinien & Vision
│   │   ├── GUIDELINES.md           # Allgemeine Richtlinien (diese Datei)
│   │   ├── DECISIONS.md            # Architektur-Entscheidungen
│   │   ├── VISION.md               # Vision & Ziele
│   │   └── GUIDELINES_KI_TOOLS.md  # KI-Tool-spezifische Standards
│   ├── templates/                  # 📝 Projekt-Templates (Single Source!)
│   │   ├── project/                # Software-Projekt Templates
│   │   ├── project_management/     # PM Templates
│   │   ├── ai_logging/             # AI-Logging Templates
│   │   └── agentos/                # AgentOS Templates
│   ├── scripts/                    # ⚙️ Framework-Skripte
│   │   ├── setup_ai_lab.sh         # Framework-Setup
│   │   └── setup_diagram_tools.sh  # Diagramm-Tools Setup
│   ├── tools/                      # 🔧 Spezialisierte Tools
│   │   └── project-creator/        # Projekterstellung Tool
│   └── MANUAL.md                   # Framework-Handbuch
├── ai_logs/                       # 📊 AI-Logging (vereinfacht)
│   ├── change_log/                 # Change Log (GitHub-style)
│   └── sessions/                  # Session-Protokolle
├── project_management/             # 📋 Projektverwaltung
│   └── work_items/                 # Arbeitspakete
└── projects/                      # 🚀 Aktuelle Projekte
    └── [projekt-name]/             # Konkrete Implementierungen
```

### Regeln für Framework-Erweiterungen

#### Neue Templates?
→ Gehören nach `core/templates/`

#### Neue Framework-Dokumentation?
→ Gehört nach `core/docs/`

#### Neue Richtlinien?
→ Gehören nach `core/guidelines/`

#### Neue Tools?
→ Gehören nach `core/tools/`

#### Neue Skripte?
→ Gehören nach `core/scripts/`

#### Neue Projekte?
→ Gehören nach `projects/`

### Konsistenz-Regeln

#### 1. Keine Duplikate
- Templates existieren nur in `core/templates/`
- Dokumentation existiert nur in `core/docs/`
- Tools existieren nur in `core/tools/`

#### 2. Single Source of Truth
- Jede Information hat genau einen Ort
- Verlinkungen statt Kopien
- Zentrale Verwaltung in `core/`

#### 3. Klarheit vor Komplexität
- Jeder Ordner hat einen klaren Zweck
- Vermeidung von übermäßiger Abstraktion
- Fokus auf Developer Experience

---

## 🤖 Anweisungen für KI-Agenten

### WICHTIG: Pflichtanforderungen für alle Agenten

Alle KI-Agenten MÜSSEN beides verwenden:

#### 1. KI-Logging nutzen (Pflicht)
```python
# Sessions dokumentieren
session_log = f"ai_logs/sessions/{datetime.now().strftime('%Y-%m-%d')}_session-{session_id}.md"

# Change Log für Änderungen nutzen
change_log = "ai_logs/change_log/CHANGELOG.md"
```

#### 2. Context-Dateien verarbeiten (Pflicht)
- **Zuerst lesen:** `core/docs/PROJECT_CONTEXT.md` für Gesamtüberblick
- **Strategisch:** `core/guidelines/VISION.md` und `core/guidelines/GUIDELINES.md` für Entscheidungen
- **Strukturell:** `core/docs/FRAMEWORK_STRUCTURE.md` für Framework-Verständnis

#### 3. Workflow (Pflicht)
```
Context → Planung → Logging → Implementierung → Dokumentation
```

**Keine Änderungen ohne vorherige Context-Analyse!**
**Alle Schritte im AI-Logging dokumentieren!**

### Framework-spezifische Agenten-Regeln

#### 1. Framework-Struktur respektieren
- Framework-relevantes immer in `core/` platzieren
- Single Source of Principle beachten
- Keine Duplikate erstellen

#### 2. Change Log statt komplexe Ordner
- Änderungen in `ai_logs/change_log/CHANGELOG.md` dokumentieren
- GitHub-style Format verwenden (Added/Changed/Removed/Fixed)
- Alte AI-Logging Struktur nicht mehr verwenden

#### 3. Templates korrekt verwenden
- Templates nur aus `core/templates/` verwenden
- Keine manuellen Kopien erstellen
- Platzhalter korrekt ersetzen

### Logging-Vorlagen für Agenten

#### Session-Log Struktur
```markdown
# Session: {Datum} Session-{ID}

## Kontext-Analyse
- core/docs/PROJECT_CONTEXT.md gelesen: ✅
- core/guidelines/VISION.md konsultiert: ✅
- core/guidelines/GUIDELINES.md Abschnitte: [Abschnitte]
- core/docs/FRAMEWORK_STRUCTURE.md geprüft: ✅

## Aufgaben
- [ ] Aufgabe 1
- [ ] Aufgabe 2

## Entscheidungen
- Entscheidung 1: Begründung
- Entscheidung 2: Begründung

## Ergebnisse
- Ergebnis 1
- Ergebnis 2
```

#### Change Log Eintrag (statt Implementation-Log)
```markdown
## [Unreleased]

### Added
- Neue Funktion/Funktionität

### Changed
- Änderung an bestehender Funktionalität

### Fixed
- Bugfix oder Problembehebung

### Removed
- Entfernte Funktionalität
```

### Context-Verarbeitungs-Regeln

1. **Immer zuerst core/docs/PROJECT_CONTEXT.md lesen** - gibt Überblick über Framework-Struktur
2. **core/docs/FRAMEWORK_STRUCTURE.md prüfen** - für Framework-Verständnis und Platzierung
3. **core/guidelines/VISION.md für strategische Entscheidungen** - ensures alignment with overall goals
4. **core/guidelines/GUIDELINES.md für technische Standards** - ensures code quality and consistency

### Beispiel-Workflow für Agenten
```python
def agent_workflow(task_description: str):
    # 1. Context lesen (neue Reihenfolge)
    context = read_core_project_context()
    structure = read_framework_structure()
    vision = read_vision()
    guidelines = read_guidelines()

    # 2. Session starten
    session_id = start_session_log(task_description, context)

    # 3. Planung basierend auf Context und Framework-Struktur
    plan = create_plan(task_description, context, structure, vision, guidelines)

    # 4. Implementierung mit Change Log
    for step in plan.steps:
        result = execute_step(step)
        update_change_log(step, result)  # Statt implementation log

    # 5. Session abschließen
    complete_session_log(session_id, plan.results)
```

---

## 🔄 Wartung & Updates

### Dependency Updates
- **Weekly**: Automatische Updates für Patch-Versionen
- **Monthly**: Review und Update von Minor-Versionen
- **Quarterly**: Major Version Updates mit Testing

### Security Updates
- **Immediate**: Kritische Security Patches
- **Weekly**: Security Scan Ergebnisse reviewen
- **Monthly**: Dependency Security Audit

### Documentation Updates
- **Per Release**: Changelog und Release Notes
- **Quarterly**: Architektur-Dokumentation reviewen
- **Annually**: Complete Framework Review

---

*Diese Richtlinien sind lebendig und werden kontinuierlich verbessert. Bei Fragen oder Vorschlägen bitte ein Issue erstellen.*
