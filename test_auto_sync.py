#!/usr/bin/env python3
"""
Test script for automatic GitHub sync functionality
"""

import os
import time
from infrastructure.db.database import SessionLocal
from infrastructure.db.models.models import WorkItem, Idea
from infrastructure.db.auto_sync import (
    manual_sync_work_item_status,
    manual_sync_idea_status,
    manual_sync_priority,
)


def test_auto_sync():
    """Test automatic GitHub sync functionality"""

    # Check environment
    if not os.getenv("GITHUB_TOKEN") or not os.getenv("GITHUB_REPO"):
        print("❌ GitHub credentials not configured")
        print("Set GITHUB_TOKEN and GITHUB_REPO environment variables")
        return

    session = SessionLocal()

    try:
        print("🧪 Testing Auto GitHub Sync")
        print("=" * 50)

        # Test work item status change
        work_item = (
            session.query(WorkItem).filter(WorkItem.github_issue_id.isnot(None)).first()
        )
        if work_item:
            print(f"\n📋 Testing Work Item Status Sync")
            print(f"Item: {work_item.id}")
            print(f"Current Status: {work_item.status}")
            print(f"GitHub Issue: #{work_item.github_issue_id}")

            # Change status
            old_status = work_item.status
            new_status = "in_progress" if old_status != "in_progress" else "done"

            print(f"Changing status to: {new_status}")
            work_item.status = new_status
            session.commit()

            print("✅ Status changed in database")
            print("⏳ Waiting for auto-sync...")
            time.sleep(2)

            # Test manual sync as well
            print("🔄 Testing manual sync...")
            manual_sync_work_item_status(work_item.id, "todo")
            time.sleep(2)

            # Reset to original
            work_item.status = old_status
            session.commit()

        else:
            print("⚠️  No work items with GitHub sync found")

        # Test idea status change
        idea = session.query(Idea).filter(Idea.github_issue_id.isnot(None)).first()
        if idea:
            print(f"\n💡 Testing Idea Status Sync")
            print(f"Idea: {idea.id}")
            print(f"Current Status: {idea.status}")
            print(f"GitHub Issue: #{idea.github_issue_id}")

            # Change status
            old_status = idea.status
            new_status = "refining" if old_status != "refining" else "ready"

            print(f"Changing status to: {new_status}")
            idea.status = new_status
            session.commit()

            print("✅ Status changed in database")
            print("⏳ Waiting for auto-sync...")
            time.sleep(2)

            # Test manual sync as well
            print("🔄 Testing manual sync...")
            manual_sync_idea_status(idea.id, "backlog")
            time.sleep(2)

            # Reset to original
            idea.status = old_status
            session.commit()

        else:
            print("⚠️  No ideas with GitHub sync found")

        # Test priority change
        if work_item:
            print(f"\n🎯 Testing Priority Sync")
            print(f"Item: {work_item.id}")
            print(f"Current Priority: {work_item.priority}")

            # Change priority
            old_priority = work_item.priority
            new_priority = "high" if old_priority != "high" else "medium"

            print(f"Changing priority to: {new_priority}")
            work_item.priority = new_priority
            session.commit()

            print("✅ Priority changed in database")
            print("⏳ Waiting for auto-sync...")
            time.sleep(2)

            # Test manual sync
            print("🔄 Testing manual priority sync...")
            manual_sync_priority("work_item", work_item.id, "low")
            time.sleep(2)

            # Reset to original
            work_item.priority = old_priority
            session.commit()

        print("\n🎉 Auto-sync test completed!")
        print("Check your GitHub repository to see the synchronized changes")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        session.rollback()

    finally:
        session.close()


if __name__ == "__main__":
    test_auto_sync()
