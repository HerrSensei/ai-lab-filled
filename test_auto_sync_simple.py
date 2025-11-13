#!/usr/bin/env python3
"""
Simple test for automatic GitHub sync using database events
"""

import os
import time
from infrastructure.db.database import SessionLocal, init_db
from infrastructure.db.models.models import WorkItem, Idea


def test_automatic_sync():
    """Test automatic GitHub sync through database events"""

    # Check environment
    if not os.getenv("GITHUB_TOKEN") or not os.getenv("GITHUB_REPO"):
        print("❌ GitHub credentials not configured")
        return

    # Initialize database with auto-sync
    print("🔧 Initializing database with auto-sync...")
    init_db()

    session = SessionLocal()

    try:
        print("🧪 Testing Automatic GitHub Sync via Database Events")
        print("=" * 60)

        # Get a work item to test with
        work_item = (
            session.query(WorkItem).filter(WorkItem.github_issue_id.isnot(None)).first()
        )
        if not work_item:
            print("❌ No work items with GitHub sync found")
            return

        print(f"\n📋 Testing Work Item: {work_item.id}")
        print(f"Current Status: {work_item.status}")
        print(f"GitHub Issue: #{work_item.github_issue_id}")

        # Change status - this should trigger auto-sync
        old_status = work_item.status
        new_status = "in_progress" if old_status != "in_progress" else "done"

        print(f"\n🔄 Changing status from '{old_status}' to '{new_status}'...")
        work_item.status = new_status

        # Commit to trigger events
        session.commit()
        print("✅ Database committed - auto-sync should trigger now")

        # Wait for sync
        print("⏳ Waiting 3 seconds for GitHub sync...")
        time.sleep(3)

        # Change priority
        print(f"\n🎯 Testing priority change...")
        old_priority = work_item.priority
        new_priority = "high" if old_priority != "high" else "medium"

        print(f"Changing priority from '{old_priority}' to '{new_priority}'...")
        work_item.priority = new_priority
        session.commit()
        print("✅ Database committed - priority auto-sync should trigger")

        print("⏳ Waiting 3 seconds for GitHub sync...")
        time.sleep(3)

        # Test with idea
        idea = session.query(Idea).filter(Idea.github_issue_id.isnot(None)).first()
        if idea:
            print(f"\n💡 Testing Idea: {idea.id}")
            print(f"Current Status: {idea.status}")
            print(f"GitHub Issue: #{idea.github_issue_id}")

            old_status = idea.status
            new_status = "refining" if old_status != "refining" else "ready"

            print(f"Changing status from '{old_status}' to '{new_status}'...")
            idea.status = new_status
            session.commit()
            print("✅ Database committed - idea auto-sync should trigger")

            print("⏳ Waiting 3 seconds for GitHub sync...")
            time.sleep(3)

        print("\n🎉 Automatic sync test completed!")
        print("Check your GitHub repository to see the synchronized changes")

        # Reset changes
        print("\n🔄 Resetting test changes...")
        work_item.status = old_status
        work_item.priority = old_priority
        if idea:
            idea.status = old_status
        session.commit()
        print("✅ Test changes reset")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        session.rollback()

    finally:
        session.close()


if __name__ == "__main__":
    test_automatic_sync()
