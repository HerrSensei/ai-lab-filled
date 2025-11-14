# 🚨 DATABASE ARCHITECTURE REMINDER

## BEFORE ANY DATABASE OPERATION - CHECKLIST

### ✅ CORRECT (SQLAlchemy ORM)
- **Location**: `src/infrastructure/db/models/models.py`
- **Import**: `from src.infrastructure.db.models.models import WorkItem`
- **Session**: `SessionLocal()` or `get_db()`
- **Database**: `data/ai_lab.db` (SQLite with SQLAlchemy)

### ❌ WRONG (Deprecated)
- **Location**: `src/ai_lab_framework/database.py`
- **Import**: `from src.ai_lab_framework.database import AILabDatabase`
- **Status**: DEPRECATED - DO NOT USE

### QUICK TEST
```python
# ✅ This is correct
from src.infrastructure.db.database import SessionLocal
from src.infrastructure.db.models.models import WorkItem

# ❌ This is wrong
from src.ai_lab_framework.database import AILabDatabase  # DEPRECATED
```

## REMEMBER: SQLAlchemy ORM ONLY!