#!/usr/bin/env python3
"""
Enhanced database models with automatic GitHub sync
"""

import os
from datetime import datetime
from typing import Optional

from infrastructure.db.auto_sync import auto_sync


class SyncableMixin:
    """Mixin class for models that can sync to GitHub"""

    def sync_status_to_github(self):
        """Sync status change to GitHub"""
        if hasattr(self, "github_issue_id") and self.github_issue_id:
            if hasattr(self, "__tablename__"):
                if self.__tablename__ == "work_items":
                    auto_sync.sync_work_item_status(self.id, self.status)
                elif self.__tablename__ == "ideas":
                    auto_sync.sync_idea_status(self.id, self.status)

    def sync_priority_to_github(self):
        """Sync priority change to GitHub"""
        if hasattr(self, "github_issue_id") and self.github_issue_id:
            if hasattr(self, "__tablename__"):
                if self.__tablename__ == "work_items":
                    auto_sync.sync_priority_change("work_item", self.id, self.priority)
                elif self.__tablename__ == "ideas":
                    auto_sync.sync_priority_change("idea", self.id, self.priority)


# Enhanced WorkItem with auto-sync
class SyncableWorkItem:
    """WorkItem with automatic GitHub sync capabilities"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._old_status = None
        self._old_priority = None

    def __setattr__(self, name, value):
        if (
            hasattr(self, "_old_status")
            and name == "status"
            and hasattr(self, "status")
        ):
            self._old_status = self.status
        if (
            hasattr(self, "_old_priority")
            and name == "priority"
            and hasattr(self, "priority")
        ):
            self._old_priority = self.priority
        super().__setattr__(name, value)

    def sync_if_changed(self):
        """Sync to GitHub if status or priority changed"""
        if hasattr(self, "_old_status") and self._old_status != self.status:
            self.sync_status_to_github()
        if hasattr(self, "_old_priority") and self._old_priority != self.priority:
            self.sync_priority_to_github()


# Enhanced Idea with auto-sync
class SyncableIdea:
    """Idea with automatic GitHub sync capabilities"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._old_status = None
        self._old_priority = None

    def __setattr__(self, name, value):
        if (
            hasattr(self, "_old_status")
            and name == "status"
            and hasattr(self, "status")
        ):
            self._old_status = self.status
        if (
            hasattr(self, "_old_priority")
            and name == "priority"
            and hasattr(self, "priority")
        ):
            self._old_priority = self.priority
        super().__setattr__(name, value)

    def sync_if_changed(self):
        """Sync to GitHub if status or priority changed"""
        if hasattr(self, "_old_status") and self._old_status != self.status:
            self.sync_status_to_github()
        if hasattr(self, "_old_priority") and self._old_priority != self.priority:
            self.sync_priority_to_github()


def sync_work_item(
    work_item_id: str,
    new_status: Optional[str] = None,
    new_priority: Optional[str] = None,
):
    """Convenience function to sync work item changes"""
    from infrastructure.db.database import SessionLocal
    from infrastructure.db.models.models import WorkItem

    session = SessionLocal()
    try:
        work_item = session.query(WorkItem).filter(WorkItem.id == work_item_id).first()
        if not work_item:
            return False

        if new_status:
            work_item.status = new_status
        if new_priority:
            work_item.priority = new_priority

        session.commit()

        # Manual sync
        if new_status:
            auto_sync.sync_work_item_status(work_item_id, new_status)
        if new_priority:
            auto_sync.sync_priority_change("work_item", work_item_id, new_priority)

        return True
    except Exception as e:
        print(f"❌ Failed to sync work item {work_item_id}: {e}")
        session.rollback()
        return False
    finally:
        session.close()


def sync_idea(
    idea_id: str, new_status: Optional[str] = None, new_priority: Optional[str] = None
):
    """Convenience function to sync idea changes"""
    from infrastructure.db.database import SessionLocal
    from infrastructure.db.models.models import Idea

    session = SessionLocal()
    try:
        idea = session.query(Idea).filter(Idea.id == idea_id).first()
        if not idea:
            return False

        if new_status:
            idea.status = new_status
        if new_priority:
            idea.priority = new_priority

        session.commit()

        # Manual sync
        if new_status:
            auto_sync.sync_idea_status(idea_id, new_status)
        if new_priority:
            auto_sync.sync_priority_change("idea", idea_id, new_priority)

        return True
    except Exception as e:
        print(f"❌ Failed to sync idea {idea_id}: {e}")
        session.rollback()
        return False
    finally:
        session.close()
