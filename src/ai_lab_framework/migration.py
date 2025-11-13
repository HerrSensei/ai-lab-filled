#!/usr/bin/env python3
"""
AI Lab Framework - JSON to SQLite Migration
Migrates existing JSON work items and ideas to SQLite database
"""

import json
import glob
import sqlite3
from pathlib import Path
from typing import List, Dict, Any
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from ai_lab_framework.database import AILabDatabase


class JSONToSQLiteMigrator:
    """Migrates JSON files to SQLite database"""

    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.db = AILabDatabase()
        self.data_path = self.base_path / "data"

    def load_json_files(self, pattern: str) -> List[Dict[str, Any]]:
        """Load all JSON files matching pattern"""
        files = []
        for file_path in glob.glob(str(self.data_path / pattern)):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        files.extend(data)
                    else:
                        files.append(data)
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
        return files

    def migrate_work_items(self) -> int:
        """Migrate work items from JSON to SQLite"""
        print("🔄 Migrating work items...")

        # Load work items from individual JSON files
        work_items = []
        work_items_path = self.data_path / "work-items"

        if work_items_path.exists():
            for file_path in work_items_path.glob("*.json"):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        work_item = json.load(f)
                        work_items.append(work_item)
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")

        # Insert work items into database
        migrated_count = 0
        for work_item in work_items:
            if self.db.insert_work_item(work_item):
                migrated_count += 1
                print(f"✅ Migrated work item: {work_item.get('id', 'Unknown')}")
            else:
                print(
                    f"❌ Failed to migrate work item: {work_item.get('id', 'Unknown')}"
                )

        print(f"📋 Work items migration completed: {migrated_count}/{len(work_items)}")
        return migrated_count

    def migrate_ideas(self) -> int:
        """Migrate ideas from JSON to SQLite"""
        print("🔄 Migrating ideas...")

        # Load ideas from individual JSON files
        ideas = []
        ideas_path = self.data_path / "ideas"

        if ideas_path.exists():
            for file_path in ideas_path.glob("*.json"):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        idea = json.load(f)
                        ideas.append(idea)
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")

        # Insert ideas into database
        migrated_count = 0
        for idea in ideas:
            if self.db.insert_idea(idea):
                migrated_count += 1
                print(f"✅ Migrated idea: {idea.get('id', 'Unknown')}")
            else:
                print(f"❌ Failed to migrate idea: {idea.get('id', 'Unknown')}")

        print(f"💡 Ideas migration completed: {migrated_count}/{len(ideas)}")
        return migrated_count

    def migrate_sessions(self) -> int:
        """Migrate session logs to SQLite"""
        print("🔄 Migrating sessions...")

        sessions = []
        ai_logs_path = self.base_path / "ai-logs" / "sessions"

        if ai_logs_path.exists():
            for file_path in ai_logs_path.glob("*.md"):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    # Extract session metadata from filename
                    filename = file_path.stem
                    parts = filename.split("_")
                    date = parts[0] if len(parts) > 0 else ""
                    session_id = parts[1] if len(parts) > 1 else ""

                    # Extract title from content
                    title = (
                        content.split("\n")[0].replace("# ", "")
                        if content
                        else filename
                    )

                    session = {
                        "id": filename,
                        "date": date,
                        "title": title,
                        "content": content,
                        "type": "development",
                        "status": "completed",
                    }
                    sessions.append(session)

                except Exception as e:
                    print(f"Error loading session {file_path}: {e}")

        # Insert sessions into database
        migrated_count = 0
        for session in sessions:
            try:
                with sqlite3.connect(self.db.db_path) as conn:
                    conn.execute(
                        """
                        INSERT OR REPLACE INTO sessions (id, date, title, content, type, status)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """,
                        (
                            session.get("id"),
                            session.get("date"),
                            session.get("title"),
                            session.get("content"),
                            session.get("type"),
                            session.get("status"),
                        ),
                    )
                migrated_count += 1
                print(f"✅ Migrated session: {session.get('id')}")
            except Exception as e:
                print(f"❌ Failed to migrate session {session.get('id')}: {e}")

        print(f"📝 Sessions migration completed: {migrated_count}/{len(sessions)}")
        return migrated_count

    def verify_migration(self) -> bool:
        """Verify migration results"""
        print("\n🔍 Verifying migration...")

        work_metrics = self.db.get_work_item_metrics()
        idea_metrics = self.db.get_idea_metrics()

        print(f"📋 Work Items in DB: {work_metrics['total']}")
        print(f"💡 Ideas in DB: {idea_metrics['total']}")

        # Check if data looks reasonable
        if work_metrics["total"] > 0 and idea_metrics["total"] > 0:
            print("✅ Migration verification passed!")
            return True
        else:
            print("❌ Migration verification failed - no data found!")
            return False

    def run_full_migration(self) -> bool:
        """Run complete migration process"""
        print("🚀 Starting JSON to SQLite migration...")

        try:
            # Migrate all data types
            work_items_count = self.migrate_work_items()
            ideas_count = self.migrate_ideas()
            sessions_count = self.migrate_sessions()

            # Verify results
            success = self.verify_migration()

            print(f"\n📊 Migration Summary:")
            print(f"   Work Items: {work_items_count}")
            print(f"   Ideas: {ideas_count}")
            print(f"   Sessions: {sessions_count}")
            print(f"   Database: {self.db.db_path}")

            if success:
                print("🎉 Migration completed successfully!")
                return True
            else:
                print("❌ Migration completed with errors!")
                return False

        except Exception as e:
            print(f"❌ Migration failed with error: {e}")
            return False

    def create_backup(self) -> str:
        """Create backup of original JSON files"""
        print("💾 Creating backup of original JSON files...")

        backup_path = self.db.backup_database()
        print(f"✅ Database backup created: {backup_path}")
        return backup_path


def main():
    """Main migration function"""
    import argparse

    parser = argparse.ArgumentParser(description="Migrate JSON data to SQLite database")
    parser.add_argument("--base-path", default=".", help="Base path of the project")
    parser.add_argument(
        "--verify-only", action="store_true", help="Only verify existing migration"
    )

    args = parser.parse_args()

    migrator = JSONToSQLiteMigrator(args.base_path)

    if args.verify_only:
        migrator.verify_migration()
    else:
        # Create backup first
        migrator.create_backup()

        # Run migration
        success = migrator.run_full_migration()

        if success:
            print("\n🎯 Next steps:")
            print("1. Update dashboard generator to use SQLite")
            print("2. Update list_ideas.py to use SQLite")
            print("3. Test all functionality")
            print("4. Archive original JSON files")
        else:
            print("\n❌ Please check the errors above and retry migration")


if __name__ == "__main__":
    main()
