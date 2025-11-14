#!/usr/bin/env python3
"""
AI Lab Framework - Work Items Migration Script

Migrates work items from JSON files to SQLite database to ensure consistency.
This should be run whenever new work items are created as JSON files.
"""

import json
import sys
import sqlite3
from pathlib import Path
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from ai_lab_framework.database import AILabDatabase
except ImportError:
    print("❌ Could not import AILabDatabase")
    print("Using direct SQLite connection...")


class WorkItemsMigrator:
    """Migrates work items from JSON files to database"""

    def __init__(self, base_dir: Path = None):
        self.base_dir = base_dir or Path.cwd()
        self.work_items_dir = self.base_dir / "data" / "work-items"
        self.db_path = self.base_dir / "data" / "ai_lab.db"

        # Try to use framework database class
        try:
            self.db = AILabDatabase(str(self.db_path))
            self.use_framework = True
        except:
            self.db = sqlite3.connect(self.db_path)
            self.use_framework = False
            print("⚠️  Using direct SQLite connection")

    def migrate_all_work_items(self, force_update: bool = False):
        """Migrate all work items from JSON to database"""
        print("🔄 Starting work items migration...")

        json_files = list(self.work_items_dir.glob("*.json"))
        print(f"📁 Found {len(json_files)} JSON work item files")

        # Group files by work item ID to handle duplicates
        work_items_by_id = {}
        for json_file in json_files:
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    work_item = json.load(f)
                    work_id = work_item.get("id")
                    if work_id:
                        if work_id not in work_items_by_id:
                            work_items_by_id[work_id] = []
                        work_items_by_id[work_id].append((json_file, work_item))
            except Exception as e:
                print(f"⚠️  Error reading {json_file.name}: {e}")

        print(f"📋 Found {len(work_items_by_id)} unique work items")

        migrated = 0
        updated = 0
        errors = 0

        for work_id, files_list in work_items_by_id.items():
            try:
                # Choose the latest version (prefer files without version numbers)
                latest_file, latest_work_item = self._choose_latest_version(files_list)

                result = self.migrate_work_item(latest_work_item, force_update)
                if result == "created":
                    migrated += 1
                    print(f"✅ Created {work_id} from {latest_file.name}")
                elif result == "updated":
                    updated += 1
                    print(f"🔄 Updated {work_id} from {latest_file.name}")
                elif result == "exists":
                    print(f"⏭️  Exists {work_id}")

            except Exception as e:
                print(f"❌ Error migrating {work_id}: {e}")
                errors += 1

        print(f"\n📊 Migration Summary:")
        print(f"  ✅ Migrated: {migrated}")
        print(f"  🔄 Updated: {updated}")
        print(f"  ❌ Errors: {errors}")
        print(f"  📋 Unique items: {len(work_items_by_id)}")

        return migrated, updated, errors

    def _choose_latest_version(self, files_list):
        """Choose the latest version from multiple files for the same work item"""
        if len(files_list) == 1:
            return files_list[0]

        # Sort by preference: clean name > higher version number
        def file_key(item):
            json_file, work_item = item
            name = json_file.name

            # Prefer clean names (no version suffix)
            if not any(
                suffix in name
                for suffix in [" 2", " 3", " 4", " 5", " 6", " 7", " 8", " 9"]
            ):
                return (0, name)

            # Extract version number if present
            import re

            version_match = re.search(r" (\d+)(?=\.json$)", name)
            if version_match:
                version = int(version_match.group(1))
                return (1, -version, name)  # Higher version = better

            return (2, name)

        return min(files_list, key=file_key)

    def migrate_work_item(self, work_item: dict, force_update: bool = False) -> str:
        """Migrate a single work item to database"""
        work_id = work_item.get("id")
        if not work_id:
            print("⚠️  Work item missing ID, skipping")
            return "error"

        # Check if already exists
        existing = self.get_work_item(work_id)

        if existing and not force_update:
            return "exists"

        # Prepare database record
        db_record = {
            "id": work_id,
            "title": work_item.get("title", ""),
            "description": work_item.get("description", ""),
            "status": work_item.get("status", "todo"),
            "priority": work_item.get("priority", "medium"),
            "type": work_item.get("type", "task"),
            "issue_type": work_item.get("component", ""),  # Map component to issue_type
            "estimated_hours": work_item.get("estimated_hours", 0),
            "actual_hours": work_item.get("actual_hours", 0),
            "assignee": work_item.get("assignee", ""),
            "created_date": work_item.get("created_at", datetime.now().isoformat()),
            "updated_date": work_item.get("updated_at", datetime.now().isoformat()),
            "due_date": work_item.get("due_date", ""),
            "labels": json.dumps(work_item.get("tags", [])),  # Map tags to labels
            "dependencies": json.dumps(work_item.get("dependencies", [])),
            "notes": json.dumps(work_item),  # Store full original data in notes
        }

        # Insert or update
        if existing:
            try:
                self.update_work_item(db_record)
                return "updated"
            except Exception as e:
                print(f"⚠️  Update failed for {work_id}: {e}, trying insert...")
                # If update fails, try to delete and insert
                self.delete_work_item(work_id)
                self.insert_work_item(db_record)
                return "created"
        else:
            try:
                self.insert_work_item(db_record)
                return "created"
            except Exception as e:
                print(f"⚠️  Insert failed for {work_id}: {e}, trying update...")
                # If insert fails, try to update
                self.update_work_item(db_record)
                return "updated"

    def get_work_item(self, work_id: str) -> dict:
        """Get work item from database"""
        try:
            cursor = (
                self.db.cursor() if not self.use_framework else self.db.conn.cursor()
            )
            cursor.execute("SELECT * FROM work_items WHERE id = ?", (work_id,))
            row = cursor.fetchone()
            cursor.close()
            return dict(row) if row else None
        except:
            return None

    def insert_work_item(self, record: dict):
        """Insert work item into database"""
        if self.use_framework:
            self.db.insert_work_item(record)
        else:
            cursor = self.db.cursor()
            columns = ", ".join(record.keys())
            placeholders = ", ".join(["?" for _ in record])
            cursor.execute(
                f"INSERT INTO work_items ({columns}) VALUES ({placeholders})",
                list(record.values()),
            )
            self.db.commit()
            cursor.close()

    def update_work_item(self, record: dict):
        """Update work item in database"""
        if self.use_framework:
            self.db.update_work_item(record["id"], record)
        else:
            cursor = self.db.cursor()
            set_clause = ", ".join([f"{k} = ?" for k in record.keys() if k != "id"])
            values = [v for k, v in record.items() if k != "id"]
            values.append(record["id"])
            cursor.execute(f"UPDATE work_items SET {set_clause} WHERE id = ?", values)
            self.db.commit()
            cursor.close()

    def delete_work_item(self, work_id: str):
        """Delete work item from database"""
        if self.use_framework:
            # Framework might not have delete method, use direct SQL
            cursor = self.db.conn.cursor()
            cursor.execute("DELETE FROM work_items WHERE id = ?", (work_id,))
            self.db.conn.commit()
            cursor.close()
        else:
            cursor = self.db.cursor()
            cursor.execute("DELETE FROM work_items WHERE id = ?", (work_id,))
            self.db.commit()
            cursor.close()

    def sync_status(self):
        """Show sync status between JSON files and database"""
        print("\n📊 Sync Status Report:")

        # Count JSON files
        json_files = list(self.work_items_dir.glob("*.json"))
        json_count = len(json_files)

        # Count database records
        try:
            cursor = (
                self.db.cursor() if not self.use_framework else self.db.conn.cursor()
            )
            cursor.execute("SELECT COUNT(*) FROM work_items")
            db_count = cursor.fetchone()[0]
            cursor.close()
        except:
            db_count = 0

        # Find missing items
        json_ids = set()
        for json_file in json_files:
            try:
                with open(json_file, "r") as f:
                    work_item = json.load(f)
                    json_ids.add(work_item.get("id"))
            except:
                continue

        try:
            cursor = (
                self.db.cursor() if not self.use_framework else self.db.conn.cursor()
            )
            cursor.execute("SELECT id FROM work_items")
            db_ids = set(row[0] for row in cursor.fetchall())
            cursor.close()
        except:
            db_ids = set()

        missing_in_db = json_ids - db_ids
        missing_in_json = db_ids - json_ids

        print(f"  📁 JSON files: {json_count}")
        print(f"  🗄️  Database records: {db_count}")
        print(f"  ➕ Missing in database: {len(missing_in_db)}")
        print(f"  ➖ Missing in JSON: {len(missing_in_json)}")

        if missing_in_db:
            print(f"\n📋 Items missing from database:")
            for item_id in sorted(missing_in_db):
                print(f"  - {item_id}")

        return {
            "json_count": json_count,
            "db_count": db_count,
            "missing_in_db": missing_in_db,
            "missing_in_json": missing_in_json,
        }


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Migrate work items from JSON to database"
    )
    parser.add_argument(
        "--sync-status", action="store_true", help="Show sync status only"
    )
    parser.add_argument(
        "--force-update", action="store_true", help="Update existing items"
    )
    parser.add_argument("--base-dir", type=Path, help="Base directory")

    args = parser.parse_args()

    migrator = WorkItemsMigrator(args.base_dir)

    if args.sync_status:
        migrator.sync_status()
    else:
        migrator.migrate_all_work_items(args.force_update)
        # Show final status
        migrator.sync_status()


if __name__ == "__main__":
    main()
