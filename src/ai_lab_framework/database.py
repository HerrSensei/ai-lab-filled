#!/usr/bin/env python3
"""
AI Lab Framework - SQLite Database Implementation
Lightweight database for work items, ideas, and GitHub integration
"""

import sqlite3
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional


class AILabDatabase:
    """SQLite database for AI Lab Framework data management"""

    def __init__(self, db_path: str = "data/ai_lab.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        self.init_database()

    def init_database(self):
        """Initialize database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript("""
                -- Work Items Table
                CREATE TABLE IF NOT EXISTS work_items (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    status TEXT DEFAULT 'proposed',
                    priority TEXT DEFAULT 'medium',
                    type TEXT DEFAULT 'task',
                    component TEXT,
                    estimated_hours REAL DEFAULT 0,
                    actual_hours REAL DEFAULT 0,
                    assignee TEXT,
                    created_date TEXT,
                    updated_date TEXT,
                    due_date TEXT,
                    tags TEXT,  -- JSON array
                    dependencies TEXT,  -- JSON array
                    data JSON,  -- Full original data
                    github_issue_id INTEGER,
                    github_synced_at TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                -- Ideas Table
                CREATE TABLE IF NOT EXISTS ideas (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    status TEXT DEFAULT 'proposed',
                    priority TEXT DEFAULT 'medium',
                    category TEXT,
                    tags TEXT,  -- JSON array
                    created_date TEXT,
                    updated_date TEXT,
                    data JSON,  -- Full original data
                    github_issue_id INTEGER,
                    github_synced_at TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                -- Sessions Table
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    date TEXT,
                    title TEXT,
                    content TEXT,
                    type TEXT DEFAULT 'development',
                    status TEXT DEFAULT 'completed',
                    data JSON,  -- Full original data
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                -- GitHub Sync Table
                CREATE TABLE IF NOT EXISTS github_sync (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    local_id TEXT,
                    local_type TEXT,  -- 'work_item' or 'idea'
                    github_issue_id INTEGER,
                    github_url TEXT,
                    sync_direction TEXT,  -- 'to_github', 'from_github', 'conflict'
                    sync_status TEXT DEFAULT 'synced',
                    last_sync_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    sync_data JSON,  -- Sync metadata
                    UNIQUE(local_id, local_type)
                );
                
                -- Create indexes for performance
                CREATE INDEX IF NOT EXISTS idx_work_items_status ON work_items(status);
                CREATE INDEX IF NOT EXISTS idx_work_items_priority ON work_items(priority);
                CREATE INDEX IF NOT EXISTS idx_work_items_component ON work_items(component);
                CREATE INDEX IF NOT EXISTS idx_ideas_status ON ideas(status);
                CREATE INDEX IF NOT EXISTS idx_ideas_category ON ideas(category);
                CREATE INDEX IF NOT EXISTS idx_github_sync_local ON github_sync(local_id, local_type);
                CREATE INDEX IF NOT EXISTS idx_github_sync_github ON github_sync(github_issue_id);
            """)

    def insert_work_item(self, work_item: Dict[str, Any]) -> bool:
        """Insert or update a work item"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO work_items (
                        id, title, description, status, priority, type, component,
                        estimated_hours, actual_hours, assignee, created_date, updated_date,
                        due_date, tags, dependencies, data
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        work_item.get("id"),
                        work_item.get("title"),
                        work_item.get("description"),
                        work_item.get("status", "proposed"),
                        work_item.get("priority", "medium"),
                        work_item.get("type", "task"),
                        work_item.get("component"),
                        work_item.get("estimated_hours", 0),
                        work_item.get("actual_hours", 0),
                        work_item.get("assignee"),
                        work_item.get("created_date"),
                        work_item.get("updated_date"),
                        work_item.get("due_date"),
                        json.dumps(work_item.get("tags", [])),
                        json.dumps(work_item.get("dependencies", [])),
                        json.dumps(work_item),
                    ),
                )
            return True
        except Exception as e:
            print(f"Error inserting work item {work_item.get('id')}: {e}")
            return False

    def insert_idea(self, idea: Dict[str, Any]) -> bool:
        """Insert or update an idea"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO ideas (
                        id, title, description, status, priority, category,
                        tags, created_date, updated_date, data
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        idea.get("id"),
                        idea.get("title"),
                        idea.get("description"),
                        idea.get("status", "proposed"),
                        idea.get("priority", "medium"),
                        idea.get("category"),
                        json.dumps(idea.get("tags", [])),
                        idea.get("created_date"),
                        idea.get("updated_date"),
                        json.dumps(idea),
                    ),
                )
            return True
        except Exception as e:
            print(f"Error inserting idea {idea.get('id')}: {e}")
            return False

    def get_work_items(
        self, status: Optional[str] = None, priority: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get work items with optional filtering"""
        query = "SELECT * FROM work_items"
        params = []

        if status or priority:
            conditions = []
            if status:
                conditions.append("status = ?")
                params.append(status)
            if priority:
                conditions.append("priority = ?")
                params.append(priority)
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY created_at DESC"

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def get_ideas(
        self, status: Optional[str] = None, category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get ideas with optional filtering"""
        query = "SELECT * FROM ideas"
        params = []

        if status or category:
            conditions = []
            if status:
                conditions.append("status = ?")
                params.append(status)
            if category:
                conditions.append("category = ?")
                params.append(category)
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY created_at DESC"

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def get_work_item_metrics(self) -> Dict[str, Any]:
        """Get work item metrics for dashboard"""
        with sqlite3.connect(self.db_path) as conn:
            # Total counts
            total = conn.execute("SELECT COUNT(*) FROM work_items").fetchone()[0]
            completed = conn.execute(
                "SELECT COUNT(*) FROM work_items WHERE status = 'done'"
            ).fetchone()[0]
            in_progress = conn.execute(
                "SELECT COUNT(*) FROM work_items WHERE status = 'in_progress'"
            ).fetchone()[0]

            # Priority breakdown
            high = conn.execute(
                "SELECT COUNT(*) FROM work_items WHERE priority = 'high'"
            ).fetchone()[0]
            medium = conn.execute(
                "SELECT COUNT(*) FROM work_items WHERE priority = 'medium'"
            ).fetchone()[0]
            low = conn.execute(
                "SELECT COUNT(*) FROM work_items WHERE priority = 'low'"
            ).fetchone()[0]

            completion_rate = (completed / total * 100) if total > 0 else 0

            return {
                "total": total,
                "completed": completed,
                "in_progress": in_progress,
                "completion_rate": round(completion_rate, 1),
                "priorities": {"high": high, "medium": medium, "low": low},
            }

    def get_idea_metrics(self) -> Dict[str, Any]:
        """Get idea metrics for dashboard"""
        with sqlite3.connect(self.db_path) as conn:
            total = conn.execute("SELECT COUNT(*) FROM ideas").fetchone()[0]
            implemented = conn.execute(
                "SELECT COUNT(*) FROM ideas WHERE status = 'implemented'"
            ).fetchone()[0]

            implementation_rate = (implemented / total * 100) if total > 0 else 0

            return {
                "total": total,
                "implemented": implemented,
                "implementation_rate": round(implementation_rate, 1),
            }

    def update_github_sync(
        self, local_id: str, local_type: str, github_issue_id: int, github_url: str
    ):
        """Update GitHub sync information"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO github_sync 
                (local_id, local_type, github_issue_id, github_url, sync_status, last_sync_at)
                VALUES (?, ?, ?, ?, 'synced', CURRENT_TIMESTAMP)
            """,
                (local_id, local_type, github_issue_id, github_url),
            )

            # Update the main table
            if local_type == "work_item":
                conn.execute(
                    """
                    UPDATE work_items 
                    SET github_issue_id = ?, github_synced_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """,
                    (github_issue_id, local_id),
                )
            elif local_type == "idea":
                conn.execute(
                    """
                    UPDATE ideas 
                    SET github_issue_id = ?, github_synced_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """,
                    (github_issue_id, local_id),
                )

    def get_unsynced_items(self, local_type: str) -> List[Dict[str, Any]]:
        """Get items that haven't been synced to GitHub yet"""
        if local_type == "work_item":
            query = "SELECT * FROM work_items WHERE github_issue_id IS NULL"
        elif local_type == "idea":
            query = "SELECT * FROM ideas WHERE github_issue_id IS NULL"
        else:
            return []

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(query)
            return [dict(row) for row in cursor.fetchall()]

    def backup_database(self, backup_path: str = None) -> str:
        """Create a backup of the database"""
        if not backup_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"backups/ai_lab_backup_{timestamp}.db"

        Path(backup_path).parent.mkdir(exist_ok=True)

        with sqlite3.connect(self.db_path) as source:
            with sqlite3.connect(backup_path) as backup:
                source.backup(backup)

        return backup_path


def main():
    """Test database functionality"""
    db = AILabDatabase()

    # Test metrics
    work_metrics = db.get_work_item_metrics()
    idea_metrics = db.get_idea_metrics()

    print("🗄️  AI Lab Database Test")
    print(
        f"📋 Work Items: {work_metrics['total']} total ({work_metrics['completion_rate']}% complete)"
    )
    print(
        f"💡 Ideas: {idea_metrics['total']} total ({idea_metrics['implementation_rate']}% implemented)"
    )
    print(f"📁 Database: {db.db_path}")
    print("✅ Database initialized successfully!")


if __name__ == "__main__":
    main()
