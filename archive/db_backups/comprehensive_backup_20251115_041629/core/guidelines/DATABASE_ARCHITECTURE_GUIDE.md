# Database Architecture Guide

## Overview

The AI Lab Framework uses a **SQLAlchemy ORM with SQLite backend** for data persistence. This guide clarifies the architecture and prevents confusion between different database implementations.

## 🏗️ Architecture

### Current Implementation (ACTIVE)
```
SQLAlchemy ORM → SQLite Database
     ↓
data/ai_lab.db
```

- **ORM**: SQLAlchemy with full model definitions
- **Database**: SQLite file at `data/ai_lab.db`
- **Models**: `src/infrastructure/db/models/models.py`
- **Configuration**: `src/infrastructure/db/database.py`

### Legacy Implementation (DEPRECATED)
```
Direct SQLite → Simple Wrapper
     ↓
data/ai_lab.db
```

- **Location**: `src/ai_lab_framework/database.py`
- **Status**: DEPRECATED - DO NOT USE
- **Reason**: Replaced by full SQLAlchemy implementation

## 📁 File Structure

```
src/
├── infrastructure/db/
│   ├── database.py          # ✅ SQLAlchemy configuration
│   └── models/
│       └── models.py        # ✅ SQLAlchemy models
└── ai_lab_framework/
    └── database.py          # ❌ DEPRECATED - Do not use
```

## 🔧 Correct Usage

### Database Operations
```python
# ✅ CORRECT - Use SQLAlchemy
from src.infrastructure.db.database import SessionLocal, get_db
from src.infrastructure.db.models.models import WorkItem, Project

# Get database session
db = next(get_db())
try:
    # Query with SQLAlchemy ORM
    work_items = db.query(WorkItem).all()
    projects = db.query(Project).filter(Project.status == 'active').all()
finally:
    db.close()
```

### Model Definitions
```python
# ✅ CORRECT - Use SQLAlchemy models
from src.infrastructure.db.models.models import WorkItem

# Create new work item
work_item = WorkItem(
    id="FRM-001",
    title="Framework Task",
    description="Task description",
    status="todo"
)
db.add(work_item)
db.commit()
```

## ❌ Incorrect Usage

### NEVER Use This Pattern
```python
# ❌ WRONG - Deprecated module
from src.ai_lab_framework.database import AILabDatabase  # DEPRECATED!

# This should NOT be used anymore
db = AILabDatabase()  # WRONG!
```

## 🔄 Migration Scripts

When creating migration scripts:

```python
# ✅ CORRECT - Use SQLAlchemy
from src.infrastructure.db.database import SessionLocal
from src.infrastructure.db.models.models import WorkItem

def migrate_work_items():
    db = SessionLocal()
    try:
        # Use SQLAlchemy ORM
        work_items = db.query(WorkItem).all()
        # Process items...
    finally:
        db.close()
```

## 🎯 Quick Reference

| Task | Correct Approach | Wrong Approach |
|------|------------------|----------------|
| Database Session | `SessionLocal()` or `get_db()` | `AILabDatabase()` |
| Model Import | `from infrastructure.db.models` | `from ai_lab_framework.database` |
| Queries | SQLAlchemy ORM | Raw SQL with deprecated wrapper |
| Schema Changes | Update SQLAlchemy models | Modify deprecated module |

## 🚨 Emergency Checklist

Before committing any database-related code:

1. [ ] Import from `infrastructure.db.models`?
2. [ ] Using SQLAlchemy sessions?
3. [ ] No imports from `ai_lab_framework.database`?
4. [ ] Using ORM queries, not raw SQL?

## 📋 Database Schema

Current tables (SQLAlchemy):
- `work_items` - Tasks and issues
- `projects` - Project management
- `ideas` - Innovation tracking
- `milestones` - Project milestones
- `custom_fields` - Flexible field definitions
- `custom_field_values` - Field values
- `project_views` - View configurations
- `automation_rules` - Automation logic

## 🔍 Verification

To verify you're using the correct implementation:

```bash
# Check database schema (should show SQLAlchemy tables)
sqlite3 data/ai_lab.db ".schema"

# Should show foreign key constraints and proper column types
# NOT the simple schema from deprecated module
```

---

**Rule of Thumb**: If you're importing from `ai_lab_framework.database`, you're using the wrong implementation!