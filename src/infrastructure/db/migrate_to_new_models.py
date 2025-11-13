#!/usr/bin/env python3
"""
Migration script to transfer data from old SQLite schema to new SQLAlchemy models
"""

import sqlite3
import json
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from infrastructure.db.database import engine, Base, SessionLocal
from infrastructure.db.models import (
    Idea,
    Project,
    WorkItem,
    Milestone,
    CustomField,
    ProjectView,
)


def migrate_from_old_database(old_db_path: str = "data/ai_lab.db"):
    """Migrate data from old SQLite database to new SQLAlchemy models"""

    print("🔄 Starting migration from old database...")

    # Connect to old database
    old_conn = sqlite3.connect(old_db_path)
    old_conn.row_factory = sqlite3.Row

    # Create new session
    new_session = SessionLocal()

    try:
        # Drop existing tables to start fresh
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

        # Migrate Ideas
        print("📝 Migrating Ideas...")
        migrate_ideas(old_conn, new_session)

        # Migrate Work Items
        print("📋 Migrating Work Items...")
        migrate_work_items(old_conn, new_session)

        # Create default project for existing work items
        print("🏗️  Creating default project...")
        create_default_project(new_session)

        # Commit all changes
        new_session.commit()
        print("✅ Migration completed successfully!")

        # Print summary
        print_migration_summary(new_session)

    except Exception as e:
        print(f"❌ Migration failed: {e}")
        new_session.rollback()
        raise
    finally:
        old_conn.close()
        new_session.close()


def migrate_ideas(old_conn: sqlite3.Connection, new_session):
    """Migrate ideas from old to new schema"""

    old_ideas = old_conn.execute("SELECT * FROM ideas").fetchall()

    for idea_row in old_ideas:
        # Parse old data
        data = json.loads(idea_row["data"]) if idea_row["data"] else {}

        # Create new Idea object
        new_idea = Idea(
            id=idea_row["id"],
            title=idea_row["title"],
            description=idea_row["description"],
            status=idea_row.get("status", "backlog"),
            priority=idea_row.get("priority", "medium"),
            category=data.get("category", "development"),
            tags=data.get("tags", []),
            created_date=idea_row.get("created_date"),
            updated_date=idea_row.get("updated_date"),
            estimated_effort=data.get("estimated_effort"),
            dependencies=data.get("dependencies", []),
            acceptance_criteria=data.get("acceptance_criteria", []),
            notes=data.get("notes"),
            author=data.get("author"),
            open_questions=data.get("open_questions", []),
            next_steps=data.get("next_steps", []),
            target_audience=data.get("target_audience"),
            benefits=data.get("benefits", []),
            prerequisites=data.get("prerequisites", []),
        )

        new_session.add(new_idea)

    print(f"   ✓ Migrated {len(old_ideas)} ideas")


def migrate_work_items(old_conn: sqlite3.Connection, new_session):
    """Migrate work items from old to new schema"""

    old_work_items = old_conn.execute("SELECT * FROM work_items").fetchall()

    for work_item_row in old_work_items:
        # Parse old data
        data = json.loads(work_item_row["data"]) if work_item_row["data"] else {}

        # Create new WorkItem object
        new_work_item = WorkItem(
            id=work_item_row["id"],
            title=work_item_row["title"],
            description=work_item_row["description"],
            status=work_item_row.get("status", "todo"),
            priority=work_item_row.get("priority", "medium"),
            type=work_item_row.get("type", "task"),
            issue_type="issue",  # Default to issue type
            assignee=work_item_row.get("assignee"),
            author=data.get("author", work_item_row.get("assignee")),
            labels=data.get("labels", work_item_row.get("tags", [])),
            created_date=work_item_row.get("created_date"),
            updated_date=work_item_row.get("updated_date"),
            due_date=work_item_row.get("due_date"),
            estimated_hours=work_item_row.get("estimated_hours"),
            actual_hours=work_item_row.get("actual_hours"),
            dependencies=data.get("dependencies", []),
            acceptance_criteria=data.get("acceptance_criteria", []),
            blockers=data.get("blockers", []),
            notes=data.get("notes"),
            file_path=data.get("file_path"),
            repository_url=data.get("repository_url"),
            is_draft=False,
            archived=False,
        )

        new_session.add(new_work_item)

    print(f"   ✓ Migrated {len(old_work_items)} work items")


def create_default_project(new_session):
    """Create a default project for existing work items"""

    # Check if project already exists
    existing_project = (
        new_session.query(Project).filter(Project.id == "PRJ-001").first()
    )
    if existing_project:
        print("   ✓ Default project already exists")
        return

    # Create default project
    default_project = Project(
        id="PRJ-001",
        name="AI Lab Framework Migration",
        description="Default project created during database migration",
        status="active",
        priority="high",
        category="development",
        visibility="private",
        owner="AI Lab Framework Team",
        team=["AI Lab Framework Team"],
        tags=["migration", "framework"],
        created_date=datetime.now(timezone.utc),
        updated_date=datetime.now(timezone.utc),
        vision="Migrate existing work items to new GitHub Projects compatible structure",
        objectives=[
            "Successfully migrate all existing data",
            "Maintain data consistency",
            "Enable GitHub Projects synchronization",
        ],
        deliverables=[
            "Complete database migration",
            "Functional GitHub Projects sync",
            "Updated documentation",
        ],
        technologies=["Python", "SQLAlchemy", "SQLite", "GitHub API"],
        acceptance_criteria=[
            "All work items migrated successfully",
            "Data integrity verified",
            "GitHub sync functional",
        ],
        progress_percentage=75,  # Migration is mostly done
        health_status="healthy",
    )

    new_session.add(default_project)

    # Assign all work items to this project
    work_items = new_session.query(WorkItem).all()
    for work_item in work_items:
        work_item.project_id = "PRJ-001"

    print("   ✓ Created default project and assigned work items")


def print_migration_summary(new_session):
    """Print summary of migrated data"""

    ideas_count = new_session.query(Idea).count()
    work_items_count = new_session.query(WorkItem).count()
    projects_count = new_session.query(Project).count()

    print("\n📊 Migration Summary:")
    print(f"   Ideas: {ideas_count}")
    print(f"   Work Items: {work_items_count}")
    print(f"   Projects: {projects_count}")
    print(f"   Database: data/ai_lab.db (new SQLAlchemy models)")


def verify_migration():
    """Verify data consistency after migration"""

    print("\n🔍 Verifying migration consistency...")

    new_session = SessionLocal()

    try:
        # Check for duplicate IDs
        idea_ids = [idea.id for idea in new_session.query(Idea).all()]
        work_item_ids = [wi.id for wi in new_session.query(WorkItem).all()]

        if len(idea_ids) != len(set(idea_ids)):
            print("   ❌ Duplicate Idea IDs found!")
            return False

        if len(work_item_ids) != len(set(work_item_ids)):
            print("   ❌ Duplicate Work Item IDs found!")
            return False

        # Check required fields
        ideas_without_title = (
            new_session.query(Idea).filter(Idea.title.is_(None)).count()
        )
        work_items_without_title = (
            new_session.query(WorkItem).filter(WorkItem.title.is_(None)).count()
        )

        if ideas_without_title > 0:
            print(f"   ❌ {ideas_without_title} Ideas without title!")
            return False

        if work_items_without_title > 0:
            print(f"   ❌ {work_items_without_title} Work Items without title!")
            return False

        print("   ✅ Data consistency verified!")
        return True

    finally:
        new_session.close()


def main():
    """Main migration function"""

    print("🗄️  AI Lab Framework Database Migration")
    print("=" * 50)

    # Backup current database
    backup_path = f"data/ai_lab_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    if Path("data/ai_lab.db").exists():
        import shutil

        shutil.copy2("data/ai_lab.db", backup_path)
        print(f"💾 Backup created: {backup_path}")

    # Run migration
    try:
        migrate_from_old_database()

        # Verify migration
        if verify_migration():
            print("\n🎉 Migration completed successfully!")
            print("📝 Next steps:")
            print("   1. Test database functionality")
            print("   2. Test GitHub Projects sync")
            print("   3. Update documentation")
        else:
            print("\n❌ Migration verification failed!")
            return 1

    except Exception as e:
        print(f"\n💥 Migration failed: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
