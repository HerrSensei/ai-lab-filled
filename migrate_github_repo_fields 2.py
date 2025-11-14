#!/usr/bin/env python3
"""
Database migration script to add GitHub repository fields
"""

from infrastructure.db.database import engine
from sqlalchemy import text


def migrate_github_repo_fields():
    """Add GitHub repository fields to existing tables"""

    migrations = [
        # Add github_repo_id to projects table
        """
        ALTER TABLE projects ADD COLUMN github_repo_id INTEGER;
        """,
        # Add github_repo_url to work_items table
        """
        ALTER TABLE work_items ADD COLUMN github_repo_url TEXT;
        """,
    ]

    with engine.connect() as conn:
        for i, migration in enumerate(migrations, 1):
            try:
                print(f"Running migration {i}: {migration.strip()[:50]}...")
                conn.execute(text(migration))
                conn.commit()
                print(f"✅ Migration {i} completed")
            except Exception as e:
                if "duplicate column name" in str(e).lower():
                    print(f"⏭️  Migration {i} skipped (column already exists)")
                else:
                    print(f"❌ Migration {i} failed: {e}")

    print("🎉 GitHub repository fields migration completed!")


if __name__ == "__main__":
    migrate_github_repo_fields()
