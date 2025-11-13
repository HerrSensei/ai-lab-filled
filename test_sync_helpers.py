#!/usr/bin/env python3
"""
Test automatic GitHub sync using helper functions
"""

import os
import time
from infrastructure.db.database import SessionLocal
from infrastructure.db.models.models import WorkItem, Idea
from infrastructure.db.sync_helpers import sync_work_item, sync_idea


def test_sync_helpers():
    """Test sync helper functions"""

    # Check environment
    if not os.getenv("GITHUB_TOKEN") or not os.getenv("GITHUB_REPO"):
        print("❌ GitHub credentials not configured")
        return

    session = SessionLocal()

    try:
        print("🧪 Testing GitHub Sync Helper Functions")
        print("=" * 50)

        # Test work item sync
        work_item = (
            session.query(WorkItem).filter(WorkItem.github_issue_id.isnot(None)).first()
        )
        if work_item:
            print(f"\n📋 Testing Work Item Sync: {work_item.id}")
            print(f"Current Status: {work_item.status}")
            print(f"Current Priority: {work_item.priority}")
            print(f"GitHub Issue: #{work_item.github_issue_id}")

            # Test status change
            new_status = "in_progress" if work_item.status != "in_progress" else "done"
            print(f"\n🔄 Syncing status change to: {new_status}")

            if sync_work_item(work_item.id, new_status=new_status):
                print("✅ Status sync successful")
                time.sleep(2)
            else:
                print("❌ Status sync failed")

            # Test priority change
            new_priority = "high" if work_item.priority != "high" else "medium"
            print(f"\n🎯 Syncing priority change to: {new_priority}")

            if sync_work_item(work_item.id, new_priority=new_priority):
                print("✅ Priority sync successful")
                time.sleep(2)
            else:
                print("❌ Priority sync failed")

            # Reset
            sync_work_item(
                work_item.id,
                new_status=work_item.status,
                new_priority=work_item.priority,
            )
            print("🔄 Reset to original values")

        # Test idea sync
        idea = session.query(Idea).filter(Idea.github_issue_id.isnot(None)).first()
        if idea:
            print(f"\n💡 Testing Idea Sync: {idea.id}")
            print(f"Current Status: {idea.status}")
            print(f"Current Priority: {idea.priority}")
            print(f"GitHub Issue: #{idea.github_issue_id}")

            # Test status change
            new_status = "refining" if idea.status != "refining" else "ready"
            print(f"\n🔄 Syncing status change to: {new_status}")

            if sync_idea(idea.id, new_status=new_status):
                print("✅ Status sync successful")
                time.sleep(2)
            else:
                print("❌ Status sync failed")

            # Test priority change
            new_priority = "critical" if idea.priority != "critical" else "low"
            print(f"\n🎯 Syncing priority change to: {new_priority}")

            if sync_idea(idea.id, new_priority=new_priority):
                print("✅ Priority sync successful")
                time.sleep(2)
            else:
                print("❌ Priority sync failed")

            # Reset
            sync_idea(idea.id, new_status=idea.status, new_priority=idea.priority)
            print("🔄 Reset to original values")

        print("\n🎉 Sync helper test completed!")
        print("Check your GitHub repository to see synchronized changes")

    except Exception as e:
        print(f"❌ Test failed: {e}")

    finally:
        session.close()


if __name__ == "__main__":
    test_sync_helpers()
