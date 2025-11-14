#!/usr/bin/env python3
"""
Migration script to transfer project data from JSON to SQLite database.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sqlalchemy.orm import Session

from infrastructure.db.database import Base, engine
from infrastructure.db.models.models import Project


def load_projects_from_json(json_file: str) -> dict:
    """Load projects from JSON file."""
    with open(json_file, encoding="utf-8") as f:
        return json.load(f)


def migrate_project_to_db(project_data: dict, db: Session) -> Project:
    """Convert JSON project data to database model."""

    # Parse dates
    created_date = datetime.fromisoformat(
        project_data["created_date"].replace("Z", "+00:00")
    )
    updated_date = datetime.fromisoformat(
        project_data["updated_date"].replace("Z", "+00:00")
    )

    # Parse timeline dates if available
    start_date = None
    target_date = None
    if "timeline" in project_data:
        timeline = project_data["timeline"]
        if timeline.get("start_date"):
            start_date = datetime.strptime(timeline["start_date"], "%Y-%m-%d")
        if timeline.get("end_date"):
            target_date = datetime.strptime(timeline["end_date"], "%Y-%m-%d")

    # Extract progress
    progress_percentage = 0
    if "progress" in project_data:
        progress_percentage = project_data["progress"].get("percentage", 0)

    # Create project instance
    project = Project(
        id=project_data["id"],
        name=project_data["name"],
        description=project_data["description"],
        status=project_data["status"],
        priority=project_data["priority"],
        category=project_data["category"],
        owner=project_data["author"],
        team=project_data.get("team", []),
        tags=project_data.get("tags", []),
        created_date=created_date,
        updated_date=updated_date,
        start_date=start_date,
        target_date=target_date,
        source_idea=project_data.get("source_idea"),
        vision=project_data.get("vision"),
        objectives=project_data.get("objectives", []),
        deliverables=project_data.get("deliverables", []),
        technologies=project_data.get("technologies", []),
        acceptance_criteria=project_data.get("acceptance_criteria", []),
        risks=project_data.get("risks", []),
        progress_percentage=progress_percentage,
        notes=project_data.get("notes"),
    )

    return project


def main():
    """Main migration function."""
    print("🔄 Starting project migration to database...")

    # Create tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created/verified")

    # Load projects from JSON
    json_file = Path(__file__).parent.parent / "data" / "projects.json"
    if not json_file.exists():
        print(f"❌ Projects JSON file not found: {json_file}")
        return

    projects_data = load_projects_from_json(str(json_file))
    print(f"📋 Loaded {len(projects_data['projects'])} projects from JSON")

    # Migrate to database
    with Session(engine) as db:
        # Check existing projects
        existing_ids = {p.id for p in db.query(Project.id).all()}
        print(f"📊 Found {len(existing_ids)} existing projects in database")

        migrated_count = 0
        updated_count = 0

        for project_data in projects_data["projects"]:
            if project_data["id"] in existing_ids:
                # Update existing project
                existing = (
                    db.query(Project).filter(Project.id == project_data["id"]).first()
                )
                if existing:
                    # Update fields
                    existing.name = project_data["name"]
                    existing.description = project_data["description"]
                    existing.status = project_data["status"]
                    existing.priority = project_data["priority"]
                    existing.category = project_data["category"]
                    existing.team = project_data.get("team", [])
                    existing.tags = project_data.get("tags", [])
                    existing.updated_date = datetime.fromisoformat(
                        project_data["updated_date"].replace("Z", "+00:00")
                    )
                    existing.vision = project_data.get("vision")
                    existing.objectives = project_data.get("objectives", [])
                    existing.deliverables = project_data.get("deliverables", [])
                    existing.technologies = project_data.get("technologies", [])
                    existing.acceptance_criteria = project_data.get(
                        "acceptance_criteria", []
                    )
                    existing.risks = project_data.get("risks", [])
                    existing.progress_percentage = project_data.get("progress", {}).get(
                        "percentage", 0
                    )
                    existing.notes = project_data.get("notes")
                    updated_count += 1
            else:
                # Create new project
                project = migrate_project_to_db(project_data, db)
                db.add(project)
                migrated_count += 1

        # Commit changes
        db.commit()
        print(f"✅ Migration complete: {migrated_count} new, {updated_count} updated")

        # Verify migration
        total_projects = db.query(Project).count()
        print(f"📈 Total projects in database: {total_projects}")


if __name__ == "__main__":
    main()
