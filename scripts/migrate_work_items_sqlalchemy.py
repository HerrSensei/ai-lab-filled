#!/usr/bin/env python3
"""
AI Lab Framework - Work Items Migration Script (SQLAlchemy Version)

Migrates work items from JSON files to SQLAlchemy database to ensure consistency.
This should be run whenever new work items are created as JSON files.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sqlalchemy.orm import sessionmaker
from infrastructure.db.database import engine, Base, init_db, SessionLocal
from infrastructure.db.models.models import WorkItem


class WorkItemsMigrator:
    """Migrates work items from JSON files to SQLAlchemy database"""

    def __init__(self, base_dir: Path = None):
        self.base_dir = base_dir or Path.cwd()
        self.work_items_dir = self.base_dir / "data" / "work-items"

        # Initialize database
        init_db()

        # Use SessionLocal from database module
        self.SessionLocal = SessionLocal

    def migrate_all_work_items(self, force_update: bool = False):
        """Migrate all work items from JSON to database"""
        print("🔄 Starting work items migration...")

        json_files = list(self.work_items_dir.glob("*.json"))
        print(f"📁 Found {len(json_files)} JSON work item files")

        migrated = 0
        updated = 0
        errors = 0

        with self.SessionLocal() as db:
            for json_file in json_files:
                try:
                    with open(json_file, "r", encoding="utf-8") as f:
                        work_item = json.load(f)

                    result = self.migrate_work_item(work_item, db, force_update)
                    if result == "created":
                        migrated += 1
                        print(f"✅ Created: {work_item.get('id')}")
                    elif result == "updated":
                        updated += 1
                        print(f"🔄 Updated: {work_item.get('id')}")
                    elif result == "exists":
                        print(f"⏭️  Exists: {work_item.get('id')}")

                except Exception as e:
                    print(f"❌ Error migrating {json_file.name}: {e}")
                    errors += 1

            db.commit()

        print(f"\n📊 Migration Summary:")
        print(f"  ✅ Migrated: {migrated}")
        print(f"  🔄 Updated: {updated}")
        print(f"  ❌ Errors: {errors}")
        print(f"  📁 Total files: {len(json_files)}")

        return migrated, updated, errors

    def migrate_work_item(
        self, work_item: dict, db: Session, force_update: bool = False
    ) -> str:
        """Migrate a single work item to database"""
        work_id = work_item.get("id")
        if not work_id:
            print("⚠️  Work item missing ID, skipping")
            return "error"

        # Check if already exists
        existing = db.query(WorkItem).filter(WorkItem.id == work_id).first()

        if existing and not force_update:
            return "exists"

        # Parse dates
        created_date = self.parse_date(work_item.get("created_at"))
        updated_date = self.parse_date(work_item.get("updated_at"))
        due_date = self.parse_date(work_item.get("due_date"))

        # Prepare database record
        if existing:
            # Update existing record
            existing.title = work_item.get("title", "")
            existing.description = work_item.get("description", "")
            existing.status = work_item.get("status", "todo")
            existing.priority = work_item.get("priority", "medium")
            existing.type = work_item.get("type", "task")
            existing.estimated_hours = work_item.get("estimated_hours", 0)
            existing.actual_hours = work_item.get("actual_hours", 0)
            existing.assignee = work_item.get("assignee", "")
            existing.created_date = created_date or datetime.utcnow()
            existing.updated_date = updated_date or datetime.utcnow()
            existing.due_date = due_date
            existing.labels = work_item.get("labels", [])
            existing.dependencies = work_item.get("dependencies", [])
            existing.acceptance_criteria = work_item.get("acceptance_criteria", [])
            existing.notes = work_item.get("notes", "")
            existing.github_issue_id = work_item.get("github_issue_id")
            existing.github_synced_at = self.parse_date(
                work_item.get("github_synced_at")
            )

            return "updated"
        else:
            # Create new record
            db_work_item = WorkItem(
                id=work_id,
                title=work_item.get("title", ""),
                description=work_item.get("description", ""),
                status=work_item.get("status", "todo"),
                priority=work_item.get("priority", "medium"),
                type=work_item.get("type", "task"),
                estimated_hours=work_item.get("estimated_hours", 0),
                actual_hours=work_item.get("actual_hours", 0),
                assignee=work_item.get("assignee", ""),
                created_date=created_date or datetime.utcnow(),
                updated_date=updated_date or datetime.utcnow(),
                due_date=due_date,
                labels=work_item.get("labels", []),
                dependencies=work_item.get("dependencies", []),
                acceptance_criteria=work_item.get("acceptance_criteria", []),
                notes=work_item.get("notes", ""),
                github_issue_id=work_item.get("github_issue_id"),
                github_synced_at=self.parse_date(work_item.get("github_synced_at")),
            )

            db.add(db_work_item)
            return "created"

    def parse_date(self, date_str: str) -> datetime:
        """Parse date string to datetime object"""
        if not date_str:
            return None

        try:
            # Handle ISO format with Z
            if date_str.endswith("Z"):
                date_str = date_str.replace("Z", "+00:00")
            return datetime.fromisoformat(date_str)
        except:
            try:
                # Try other common formats
                return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            except:
                return None

    def sync_status(self):
        """Show sync status between JSON files and database"""
        print("\n📊 Sync Status Report:")

        # Count JSON files
        json_files = list(self.work_items_dir.glob("*.json"))
        json_count = len(json_files)

        # Count database records
        with self.SessionLocal() as db:
            db_count = db.query(WorkItem).count()

        # Find missing items
        json_ids = set()
        for json_file in json_files:
            try:
                with open(json_file, "r") as f:
                    work_item = json.load(f)
                    json_ids.add(work_item.get("id"))
            except:
                continue

        with self.SessionLocal() as db:
            db_items = db.query(WorkItem.id).all()
            db_ids = set(item[0] for item in db_items)

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

    def list_work_items(
        self, status: str = None, priority: str = None, limit: int = None
    ):
        """List work items from database with optional filtering"""
        with self.SessionLocal() as db:
            query = db.query(WorkItem)

            if status:
                query = query.filter(WorkItem.status == status)

            if priority:
                query = query.filter(WorkItem.priority == priority)

            if limit:
                query = query.limit(limit)

            work_items = query.all()

            print(f"\n📋 Found {len(work_items)} work items:")
            for item in work_items:
                status_emoji = {
                    "todo": "📋",
                    "in_progress": "🔄",
                    "done": "✅",
                    "review": "🔴",
                    "blocked": "🚫",
                }.get(item.status, "❓")

                priority_emoji = {
                    "low": "🟢",
                    "medium": "🟡",
                    "high": "🔴",
                    "critical": "🚨",
                }.get(item.priority, "⚪")

                print(f"  {status_emoji} {priority_emoji} {item.id}: {item.title}")
                print(f"     Status: {item.status} | Priority: {item.priority}")
                if item.assignee:
                    print(f"     Assignee: {item.assignee}")
                print()


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Migrate work items from JSON to SQLAlchemy database"
    )
    parser.add_argument(
        "--sync-status", action="store_true", help="Show sync status only"
    )
    parser.add_argument(
        "--force-update", action="store_true", help="Update existing items"
    )
    parser.add_argument(
        "--list", action="store_true", help="List work items from database"
    )
    parser.add_argument("--status", help="Filter by status")
    parser.add_argument("--priority", help="Filter by priority")
    parser.add_argument("--limit", type=int, help="Limit number of results")
    parser.add_argument("--base-dir", type=Path, help="Base directory")

    args = parser.parse_args()

    migrator = WorkItemsMigrator(args.base_dir)

    if args.sync_status:
        migrator.sync_status()
    elif args.list:
        migrator.list_work_items(args.status, args.priority, args.limit)
    else:
        migrator.migrate_all_work_items(args.force_update)
        # Show final status
        migrator.sync_status()


if __name__ == "__main__":
    main()
