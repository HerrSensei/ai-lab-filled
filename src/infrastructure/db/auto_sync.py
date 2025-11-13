#!/usr/bin/env python3
"""
AI Lab Framework - Automatic GitHub Sync
Automatically syncs status changes to GitHub Issues
"""

import os
import time
from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event
from sqlalchemy.engine import Engine

from .database import SessionLocal, engine
from .models.models import WorkItem, Idea, Project
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from ai_lab_framework.github_integration import GitHubIntegration


class AutoGitHubSync:
    """Automatic GitHub synchronization for status changes"""

    def __init__(self):
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.github_repo = os.getenv("GITHUB_REPO")
        self._integration = None
        self._enabled = True

    @property
    def integration(self) -> Optional[GitHubIntegration]:
        """Lazy-load GitHub integration"""
        if not self._enabled:
            return None

        if not self.github_token or not self.github_repo:
            print("⚠️  GitHub credentials not configured, skipping auto-sync")
            self._enabled = False
            return None

        if not self._integration:
            try:
                self._integration = GitHubIntegration(
                    self.github_token, self.github_repo
                )
                print("✅ GitHub integration initialized for auto-sync")
            except Exception as e:
                print(f"❌ Failed to initialize GitHub integration: {e}")
                self._enabled = False
                return None

        return self._integration

    def sync_work_item_status(self, work_item_id: str, new_status: str) -> bool:
        """Sync work item status change to GitHub"""
        if not self.integration:
            return False

        try:
            session = SessionLocal()
            work_item = (
                session.query(WorkItem).filter(WorkItem.id == work_item_id).first()
            )

            if not work_item or not work_item.github_issue_id:
                session.close()
                return False

            # Get the GitHub issue
            issue = self.integration.repo.get_issue(work_item.github_issue_id)

            # Update status labels
            current_labels = [label.name for label in issue.labels]
            new_labels = []

            # Remove old status labels
            for label in current_labels:
                if not label.startswith("status:"):
                    new_labels.append(label)

            # Add new status label
            new_labels.append(f"status:{new_status}")

            # Update issue labels
            issue.edit(labels=new_labels)

            # Update sync timestamp
            work_item.github_synced_at = datetime.now()
            session.commit()

            print(
                f"🔄 Auto-synced {work_item_id} status to '{new_status}' in GitHub issue #{work_item.github_issue_id}"
            )
            session.close()
            return True

        except Exception as e:
            print(f"❌ Failed to auto-sync work item {work_item_id}: {e}")
            if "session" in locals():
                session.close()
            return False

    def sync_idea_status(self, idea_id: str, new_status: str) -> bool:
        """Sync idea status change to GitHub"""
        if not self.integration:
            return False

        try:
            session = SessionLocal()
            idea = session.query(Idea).filter(Idea.id == idea_id).first()

            if not idea or not idea.github_issue_id:
                session.close()
                return False

            # Get the GitHub issue
            issue = self.integration.repo.get_issue(idea.github_issue_id)

            # Update status labels
            current_labels = [label.name for label in issue.labels]
            new_labels = []

            # Remove old status labels
            for label in current_labels:
                if not label.startswith("status:"):
                    new_labels.append(label)

            # Add new status label
            new_labels.append(f"status:{new_status}")

            # Update issue labels
            issue.edit(labels=new_labels)

            # Update sync timestamp
            idea.github_synced_at = datetime.now()
            session.commit()

            print(
                f"🔄 Auto-synced {idea_id} status to '{new_status}' in GitHub issue #{idea.github_issue_id}"
            )
            session.close()
            return True

        except Exception as e:
            print(f"❌ Failed to auto-sync idea {idea_id}: {e}")
            if "session" in locals():
                session.close()
            return False

    def sync_priority_change(
        self, item_type: str, item_id: str, new_priority: str
    ) -> bool:
        """Sync priority change to GitHub"""
        if not self.integration:
            return False

        try:
            session = SessionLocal()

            if item_type == "work_item":
                item = session.query(WorkItem).filter(WorkItem.id == item_id).first()
            elif item_type == "idea":
                item = session.query(Idea).filter(Idea.id == item_id).first()
            else:
                session.close()
                return False

            if not item or not item.github_issue_id:
                session.close()
                return False

            # Get the GitHub issue
            issue = self.integration.repo.get_issue(item.github_issue_id)

            # Update priority labels
            current_labels = [label.name for label in issue.labels]
            new_labels = []

            # Remove old priority labels
            for label in current_labels:
                if not label.startswith("priority:"):
                    new_labels.append(label)

            # Add new priority label
            new_labels.append(f"priority:{new_priority}")

            # Update issue labels
            issue.edit(labels=new_labels)

            # Update sync timestamp
            item.github_synced_at = datetime.now()
            session.commit()

            print(
                f"🔄 Auto-synced {item_id} priority to '{new_priority}' in GitHub issue #{item.github_issue_id}"
            )
            session.close()
            return True

        except Exception as e:
            print(f"❌ Failed to auto-sync {item_type} {item_id} priority: {e}")
            if "session" in locals():
                session.close()
            return False


# Global auto-sync instance
auto_sync = AutoGitHubSync()


def setup_auto_sync():
    """Setup SQLAlchemy event listeners for automatic sync"""

    @event.listens_for(SessionLocal, "after_commit")
    def after_commit(session):
        """Handle sync after successful commit"""
        # Get all dirty instances from the just-completed session
        for instance in session.dirty:
            if hasattr(instance, "_sa_instance_state"):
                state = instance._sa_instance_state
                for attr in state.attrs:
                    if attr.history.has_changes():
                        old_value = (
                            attr.history.deleted[0] if attr.history.deleted else None
                        )
                        new_value = (
                            attr.history.added[0] if attr.history.added else None
                        )

                        if old_value != new_value:
                            # Handle WorkItem changes
                            if isinstance(instance, WorkItem):
                                if attr.key == "status" and instance.github_issue_id:
                                    auto_sync.sync_work_item_status(
                                        instance.id, new_value
                                    )
                                elif (
                                    attr.key == "priority" and instance.github_issue_id
                                ):
                                    auto_sync.sync_priority_change(
                                        "work_item", instance.id, new_value
                                    )

                            # Handle Idea changes
                            elif isinstance(instance, Idea):
                                if attr.key == "status" and instance.github_issue_id:
                                    auto_sync.sync_idea_status(instance.id, new_value)
                                elif (
                                    attr.key == "priority" and instance.github_issue_id
                                ):
                                    auto_sync.sync_priority_change(
                                        "idea", instance.id, new_value
                                    )

    print("✅ Auto-sync event listeners registered")


# Manual sync functions for testing
def manual_sync_work_item_status(work_item_id: str, new_status: str):
    """Manually trigger work item status sync"""
    return auto_sync.sync_work_item_status(work_item_id, new_status)


def manual_sync_idea_status(idea_id: str, new_status: str):
    """Manually trigger idea status sync"""
    return auto_sync.sync_idea_status(idea_id, new_status)


def manual_sync_priority(item_type: str, item_id: str, new_priority: str):
    """Manually trigger priority sync"""
    return auto_sync.sync_priority_change(item_type, item_id, new_priority)
