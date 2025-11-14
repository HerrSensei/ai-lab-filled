#!/usr/bin/env python3
"""
AI Lab Framework - Ideas Migration Script (SQLAlchemy Version)

Migrates ideas from JSON files to SQLite database using SQLAlchemy ORM.
This replaces the deprecated direct SQLite approach.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# ✅ CORRECT - Use SQLAlchemy ORM
from infrastructure.db.database import SessionLocal
from infrastructure.db.models.models import Idea


class IdeasMigrator:
    """Migrates ideas from JSON files to database using SQLAlchemy"""

    def __init__(self, base_dir: Path = None):
        self.base_dir = base_dir or Path.cwd()
        self.ideas_dir = self.base_dir / "data" / "ideas"

        # ✅ CORRECT - Use SQLAlchemy session
        self.db = SessionLocal()

    def migrate_all_ideas(self, force_update: bool = False):
        """Migrate all ideas from JSON to database"""
        print("🔄 Starting ideas migration (SQLAlchemy ORM)...")

        json_files = list(self.ideas_dir.glob("*.json"))
        print(f"📁 Found {len(json_files)} JSON idea files")

        # Group by ID to handle duplicates
        ideas_by_id = {}
        for json_file in json_files:
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    idea = json.load(f)
                    idea_id = idea.get("id")
                    if idea_id:
                        if idea_id not in ideas_by_id:
                            ideas_by_id[idea_id] = []
                        ideas_by_id[idea_id].append((json_file, idea))
            except Exception as e:
                print(f"⚠️  Error reading {json_file.name}: {e}")

        print(f"💡 Found {len(ideas_by_id)} unique ideas")

        migrated = 0
        updated = 0
        errors = 0

        for idea_id, files_list in ideas_by_id.items():
            try:
                # Choose the latest version
                latest_file, latest_idea = self._choose_latest_version(files_list)

                result = self.migrate_idea(latest_idea, force_update)
                if result == "created":
                    migrated += 1
                    print(f"✅ Created {idea_id} from {latest_file.name}")
                elif result == "updated":
                    updated += 1
                    print(f"🔄 Updated {idea_id} from {latest_file.name}")
                elif result == "exists":
                    print(f"⏭️  Exists {idea_id}")

            except Exception as e:
                print(f"❌ Error migrating {idea_id}: {e}")
                errors += 1

        print(f"\n📊 Migration Summary:")
        print(f"  ✅ Migrated: {migrated}")
        print(f"  🔄 Updated: {updated}")
        print(f"  ❌ Errors: {errors}")
        print(f"  💡 Unique ideas: {len(ideas_by_id)}")

        return migrated, updated, errors

    def _choose_latest_version(self, files_list):
        """Choose the latest version from multiple files"""
        if len(files_list) == 1:
            return files_list[0]

        # Prefer clean names (no version suffix)
        def file_key(item):
            json_file, idea = item
            name = json_file.name

            if not any(
                suffix in name
                for suffix in [" 2", " 3", " 4", " 5", " 6", " 7", " 8", " 9"]
            ):
                return (0, name)

            import re

            version_match = re.search(r" (\d+)(?=\.json$)", name)
            if version_match:
                version = int(version_match.group(1))
                return (1, -version, name)

            return (2, name)

        return min(files_list, key=file_key)

    def migrate_idea(self, idea_data: dict, force_update: bool = False) -> str:
        """Migrate a single idea to database using SQLAlchemy"""
        idea_id = idea_data.get("id")
        if not idea_id:
            print("⚠️  Idea missing ID, skipping")
            return "error"

        # Check if already exists
        existing = self.db.query(Idea).filter(Idea.id == idea_id).first()

        if existing and not force_update:
            return "exists"

        # Parse dates
        created_date = self._parse_date(idea_data.get("created_date"))
        updated_date = self._parse_date(idea_data.get("updated_date"))

        # Create or update SQLAlchemy model
        if existing:
            # Update existing
            existing.title = idea_data.get("title", existing.title)
            existing.description = idea_data.get("description", existing.description)
            existing.status = idea_data.get("status", existing.status)
            existing.priority = idea_data.get("priority", existing.priority)
            existing.category = idea_data.get("category", existing.category)
            existing.tags = idea_data.get("tags", existing.tags)
            existing.created_date = created_date or existing.created_date
            existing.updated_date = updated_date or datetime.utcnow()
            existing.dependencies = idea_data.get("dependencies", existing.dependencies)
            existing.acceptance_criteria = idea_data.get(
                "acceptance_criteria", existing.acceptance_criteria
            )
            existing.notes = idea_data.get("notes", existing.notes)
            existing.author = idea_data.get("author", existing.author)
            existing.open_questions = idea_data.get(
                "open_questions", existing.open_questions
            )
            existing.next_steps = idea_data.get("next_steps", existing.next_steps)
            existing.target_audience = idea_data.get(
                "target_audience", existing.target_audience
            )
            existing.benefits = idea_data.get("benefits", existing.benefits)
            existing.prerequisites = idea_data.get(
                "prerequisites", existing.prerequisites
            )

            self.db.commit()
            return "updated"
        else:
            # Create new
            new_idea = Idea(
                id=idea_id,
                title=idea_data.get("title", ""),
                description=idea_data.get("description", ""),
                status=idea_data.get("status", "proposed"),
                priority=idea_data.get("priority", "medium"),
                category=idea_data.get("category", "development"),
                tags=idea_data.get("tags", []),
                created_date=created_date or datetime.utcnow(),
                updated_date=updated_date or datetime.utcnow(),
                dependencies=idea_data.get("dependencies", []),
                acceptance_criteria=idea_data.get("acceptance_criteria", []),
                notes=idea_data.get("notes", ""),
                author=idea_data.get("author", ""),
                open_questions=idea_data.get("open_questions", []),
                next_steps=idea_data.get("next_steps", []),
                target_audience=idea_data.get("target_audience", ""),
                benefits=idea_data.get("benefits", []),
                prerequisites=idea_data.get("prerequisites", []),
            )

            self.db.add(new_idea)
            self.db.commit()
            return "created"

    def _parse_date(self, date_str: str):
        """Parse date string to datetime"""
        if not date_str:
            return None
        try:
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except:
            return None

    def sync_status(self):
        """Show sync status between JSON files and database"""
        print("\n📊 Ideas Sync Status Report:")

        # Count JSON files
        json_files = list(self.ideas_dir.glob("*.json"))
        json_count = len(json_files)

        # Count database records
        db_count = self.db.query(Idea).count()

        # Find unique IDs
        json_ids = set()
        for json_file in json_files:
            try:
                with open(json_file, "r") as f:
                    idea = json.load(f)
                    json_ids.add(idea.get("id"))
            except:
                continue

        db_ids = set(idea.id for idea in self.db.query(Idea.id).all())

        missing_in_db = json_ids - db_ids
        missing_in_json = db_ids - json_ids

        print(f"  📁 JSON files: {json_count}")
        print(f"  🗄️  Database records: {db_count}")
        print(f"  ➕ Missing in database: {len(missing_in_db)}")
        print(f"  ➖ Missing in JSON: {len(missing_in_json)}")

        if missing_in_db:
            print(f"\n💡 Ideas missing from database:")
            for idea_id in sorted(missing_in_db):
                print(f"  - {idea_id}")

        return {
            "json_count": json_count,
            "db_count": db_count,
            "missing_in_db": missing_in_db,
            "missing_in_json": missing_in_json,
        }

    def __del__(self):
        """Cleanup database session"""
        if hasattr(self, "db"):
            self.db.close()


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Migrate ideas from JSON to database (SQLAlchemy)"
    )
    parser.add_argument(
        "--sync-status", action="store_true", help="Show sync status only"
    )
    parser.add_argument(
        "--force-update", action="store_true", help="Update existing items"
    )
    parser.add_argument("--base-dir", type=Path, help="Base directory")

    args = parser.parse_args()

    migrator = IdeasMigrator(args.base_dir)

    if args.sync_status:
        migrator.sync_status()
    else:
        migrator.migrate_all_ideas(args.force_update)
        # Show final status
        migrator.sync_status()


if __name__ == "__main__":
    main()
