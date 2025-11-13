import json
from pathlib import Path
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.inspection import inspect # Added import

from .database import SessionLocal
from .models.models import Idea, WorkItem

def filter_data_for_model(data: dict, model_class) -> dict:
    """Filters a dictionary to only include keys that are columns in the given SQLAlchemy model."""
    mapper = inspect(model_class)
    valid_keys = {column.key for column in mapper.columns}
    return {key: value for key, value in data.items() if key in valid_keys}

def migrate_json_to_sqlite():
    """
    Migrates existing JSON data from data/ideas and data/work-items
    into the SQLite database.
    """
    db: Session = SessionLocal()
    try:
        # Migrate Ideas
        ideas_path = Path("data/ideas")
        print(f"Migrating ideas from {ideas_path}...")
        for idea_file in ideas_path.glob("IDEA-*.json"):
            with open(idea_file, "r") as f:
                idea_data = json.load(f)

            # Convert array fields to JSON strings
            for field in ["tags", "dependencies", "acceptance_criteria", "open_questions", "next_steps", "benefits", "prerequisites"]:
                if field in idea_data and isinstance(idea_data[field], list):
                    idea_data[field] = json.dumps(idea_data[field])
                elif field not in idea_data:
                    idea_data[field] = "[]" # Ensure default for missing arrays

            # Handle datetime fields
            for field in ["created_date", "updated_date"]:
                if field in idea_data and isinstance(idea_data[field], str):
                    try:
                        idea_data[field] = datetime.fromisoformat(idea_data[field].replace('Z', '+00:00'))
                    except ValueError:
                        print(f"Warning: Could not parse date for {field} in {idea_file}. Using current time.")
                        idea_data[field] = datetime.utcnow()
                elif field not in idea_data:
                    idea_data[field] = datetime.utcnow()

            # Ensure required fields are present or defaulted
            if 'author' not in idea_data: idea_data['author'] = None
            if 'estimated_effort' not in idea_data: idea_data['estimated_effort'] = None
            if 'notes' not in idea_data: idea_data['notes'] = None
            if 'target_audience' not in idea_data: idea_data['target_audience'] = None

            # Filter out any keys not present in the Idea model
            idea_data = filter_data_for_model(idea_data, Idea)
            idea = Idea(**idea_data)
            db.add(idea)
        db.commit()
        print(f"Migrated {len(list(ideas_path.glob('IDEA-*.json')))} ideas.")

        # Migrate WorkItems
        work_items_path = Path("data/work-items")
        print(f"Migrating work items from {work_items_path}...")
        for work_item_file in work_items_path.glob("*.json"):
            # Skip FRM-003-COMP 2.json as it's a duplicate and causes issues
            if "FRM-003-COMP 2.json" in work_item_file.name:
                print(f"Skipping duplicate work item: {work_item_file.name}")
                continue

            with open(work_item_file, "r") as f:
                work_item_data = json.load(f)

            # Convert array fields to JSON strings
            for field in ["tags", "dependencies", "acceptance_criteria", "blockers"]:
                if field in work_item_data and isinstance(work_item_data[field], list):
                    work_item_data[field] = json.dumps(work_item_data[field])
                elif field not in work_item_data:
                    work_item_data[field] = "[]" # Ensure default for missing arrays

            # Handle datetime fields
            for field in ["created_date", "updated_date", "due_date"]:
                if field in work_item_data and isinstance(work_item_data[field], str):
                    try:
                        work_item_data[field] = datetime.fromisoformat(work_item_data[field].replace('Z', '+00:00'))
                    except ValueError:
                        print(f"Warning: Could not parse date for {field} in {work_item_file}. Using current time.")
                        work_item_data[field] = datetime.utcnow()
                elif field not in work_item_data:
                    work_item_data[field] = None # due_date can be None, others default to utcnow

            # Ensure required fields are present or defaulted
            if 'project' not in work_item_data: work_item_data['project'] = None
            if 'assignee' not in work_item_data: work_item_data['assignee'] = None
            if 'estimated_hours' not in work_item_data: work_item_data['estimated_hours'] = None
            if 'actual_hours' not in work_item_data: work_item_data['actual_hours'] = None
            if 'notes' not in work_item_data: work_item_data['notes'] = None
            if 'file_path' not in work_item_data: work_item_data['file_path'] = None
            # Handle missing or null 'type' field
            if 'type' not in work_item_data or work_item_data['type'] is None:
                work_item_data['type'] = "task" # Default to 'task' if missing or None

            # Filter out any keys not present in the WorkItem model
            work_item_data = filter_data_for_model(work_item_data, WorkItem)

            # Check for existing WorkItem with the same ID
            # This check needs to be done *after* filtering, but before creating the WorkItem instance
            # and before adding to the DB.
            # Also, ensure 'id' is present in work_item_data after filtering.
            if 'id' in work_item_data:
                existing_work_item = db.query(WorkItem).filter_by(id=work_item_data['id']).first()
                if existing_work_item:
                    print(f"Warning: WorkItem with ID '{work_item_data['id']}' already exists. Skipping: {work_item_file.name}")
                    continue

            work_item = WorkItem(**work_item_data)
            db.add(work_item)
        db.commit()
        print(f"Migrated {len(list(work_items_path.glob('*.json')))} work items.")

    except Exception as e:
        db.rollback()
        print(f"An error occurred during migration: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    migrate_json_to_sqlite()
