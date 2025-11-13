#!/usr/bin/env python3
"""
Test GitHub Projects sync functionality with new database models
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timezone

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from infrastructure.db.database import SessionLocal, init_db
from infrastructure.db.models import Project, WorkItem, Idea


def create_test_data():
    """Create test data for GitHub sync testing"""

    print("📝 Creating test data for GitHub sync...")

    session = SessionLocal()

    try:
        # Create test work item
        test_work_item = WorkItem(
            id="SYNC-TEST-001",
            title="Test GitHub Projects Sync",
            description="Test work item to verify GitHub Projects synchronization functionality",
            status="todo",
            priority="high",
            type="task",
            issue_type="issue",
            project_id="PRJ-001",
            assignee="AI Lab Framework Team",
            author="AI Lab Framework Team",
            labels=["test", "github", "sync"],
            created_date=datetime.now(timezone.utc),
            updated_date=datetime.now(timezone.utc),
            estimated_hours=2.0,
            actual_hours=0.0,
            dependencies=[],
            acceptance_criteria=[
                "GitHub issue created successfully",
                "Sync status updated in database",
                "Bidirectional sync working",
            ],
            blockers=[],
            notes="Test work item created to verify GitHub Projects sync functionality",
        )

        session.add(test_work_item)

        # Create test idea
        test_idea = Idea(
            id="SYNC-IDEA-001",
            title="Implement GitHub Projects Integration",
            description="Enhance GitHub sync to work with new Projects API and features",
            status="backlog",
            priority="high",
            category="development",
            tags=["github", "projects", "integration", "sync"],
            author="AI Lab Framework Team",
            estimated_effort="8 hours",
            dependencies=[],
            acceptance_criteria=[
                "GitHub Projects API integration",
                "Custom fields support",
                "Views and layouts support",
                "Automation rules support",
            ],
            notes="Test idea for GitHub Projects integration",
            open_questions=[
                "How to handle custom fields mapping?",
                "Best approach for views synchronization?",
            ],
            next_steps=[
                "Research GitHub Projects API",
                "Design data mapping strategy",
                "Implement sync functionality",
            ],
            target_audience="Development Team",
            benefits=[
                "Better project management",
                "Enhanced collaboration",
                "Improved workflow automation",
            ],
            prerequisites=["GitHub token configured", "New database models deployed"],
        )

        session.add(test_idea)
        session.commit()

        print("   ✅ Test work item created: SYNC-TEST-001")
        print("   ✅ Test idea created: SYNC-IDEA-001")

        return True

    except Exception as e:
        print(f"❌ Failed to create test data: {e}")
        session.rollback()
        return False

    finally:
        session.close()


def test_github_sync():
    """Test GitHub sync functionality"""

    print("\n🔄 Testing GitHub Sync Functionality")
    print("=" * 40)

    # Check if GitHub token is available
    github_token = os.getenv("GITHUB_TOKEN")
    github_repo = os.getenv("GITHUB_REPO", "HerrSensei/ai-lab")

    if not github_token:
        print("⚠️  GITHUB_TOKEN not found in environment")
        print("   To test GitHub sync:")
        print("   1. Create a GitHub Personal Access Token")
        print("   2. Set environment variable: export GITHUB_TOKEN=your_token")
        print("   3. Run this test again")
        return False

    print(f"🔑 GitHub Token: {'✅ Available' if github_token else '❌ Missing'}")
    print(f"📁 GitHub Repository: {github_repo}")

    try:
        # Import GitHub integration
        from ai_lab_framework.github_integration import GitHubIntegration

        # Initialize integration
        integration = GitHubIntegration(github_token, github_repo)

        # Setup repository labels
        print("\n🏷️  Setting up repository labels...")
        if integration.setup_repository_labels():
            print("   ✅ Repository labels setup completed")
        else:
            print("   ❌ Repository labels setup failed")
            return False

        # Test sync to GitHub
        print("\n⬆️  Testing sync to GitHub...")
        sync_results = integration.sync_to_github("all")

        print(f"   📊 Sync Results: {sync_results}")

        if sync_results["errors"] == 0:
            print("   ✅ Sync to GitHub completed successfully")
        else:
            print(f"   ❌ Sync to GitHub had {sync_results['errors']} errors")
            return False

        # Test sync from GitHub
        print("\n⬇️  Testing sync from GitHub...")
        reverse_sync_results = integration.sync_from_github()

        print(f"   📊 Reverse Sync Results: {reverse_sync_results}")

        if reverse_sync_results["errors"] == 0:
            print("   ✅ Sync from GitHub completed successfully")
        else:
            print(f"   ❌ Sync from GitHub had {reverse_sync_results['errors']} errors")
            return False

        print("\n🎉 GitHub sync functionality working!")
        return True

    except ImportError as e:
        print(f"❌ GitHub integration module not found: {e}")
        print("   This is expected if PyGithub is not installed")
        print("   Install with: poetry add PyGithub")
        return False

    except Exception as e:
        print(f"❌ GitHub sync test failed: {e}")
        return False


def test_database_sync_status():
    """Test database sync status tracking"""

    print("\n📊 Testing Database Sync Status")
    print("=" * 35)

    session = SessionLocal()

    try:
        # Check for unsynced work items
        unsynced_work_items = (
            session.query(WorkItem)
            .filter(
                (WorkItem.github_issue_id.is_(None)) | (WorkItem.github_issue_id == 0)
            )
            .all()
        )

        # Check for unsynced ideas
        unsynced_ideas = (
            session.query(Idea)
            .filter((Idea.github_issue_id.is_(None)) | (Idea.github_issue_id == 0))
            .all()
        )

        print(f"📋 Unsynced Work Items: {len(unsynced_work_items)}")
        for wi in unsynced_work_items:
            print(f"   - {wi.id}: {wi.title}")

        print(f"💡 Unsynced Ideas: {len(unsynced_ideas)}")
        for idea in unsynced_ideas:
            print(f"   - {idea.id}: {idea.title}")

        # Check total counts
        total_work_items = session.query(WorkItem).count()
        total_ideas = session.query(Idea).count()

        print(f"\n📈 Total Work Items: {total_work_items}")
        print(f"📈 Total Ideas: {total_ideas}")

        if len(unsynced_work_items) > 0 or len(unsynced_ideas) > 0:
            print("   ✅ Items ready for GitHub sync")
        else:
            print("   ℹ️  All items are synced")

        return True

    except Exception as e:
        print(f"❌ Database sync status test failed: {e}")
        return False

    finally:
        session.close()


def main():
    """Main test function"""

    print("🗄️  AI Lab Framework GitHub Sync Testing")
    print("=" * 50)

    # Initialize database
    init_db()

    # Create test data
    if not create_test_data():
        print("❌ Failed to create test data")
        return 1

    # Test database sync status
    if not test_database_sync_status():
        print("❌ Database sync status test failed")
        return 1

    # Test GitHub sync
    if not test_github_sync():
        print("❌ GitHub sync test failed")
        return 1

    print("\n🎉 All GitHub sync tests completed!")
    print("📝 Next steps:")
    print("   1. Verify GitHub issues were created")
    print("   2. Test bidirectional sync")
    print("   3. Test with custom fields and views")
    print("   4. Create work item for any fixes needed")

    return 0


if __name__ == "__main__":
    exit(main())
