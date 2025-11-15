import os
import sys
from sqlalchemy.orm import Session

# Add the project root to the sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from infrastructure.db.database import SessionLocal
from infrastructure.db.models.models import WorkItem

def update_work_item_priority(work_item_id: str, new_priority: str):
    db: Session = SessionLocal()
    try:
        work_item = db.query(WorkItem).filter(WorkItem.id == work_item_id).first()
        if work_item:
            print(f"Found Work Item: {work_item.title} (Current Priority: {work_item.priority})")
            work_item.priority = new_priority
            db.commit()
            db.refresh(work_item)
            print(f"Updated Work Item: {work_item.title} (New Priority: {work_item.priority})")
        else:
            print(f"Work Item with ID {work_item_id} not found.")
    except Exception as e:
        db.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    work_item_id_to_update = "PROJ-674C38A1-WI-002"
    new_priority_value = "low"
    update_work_item_priority(work_item_id_to_update, new_priority_value)
