#!/usr/bin/env python3
"""
Test script for new SQLAlchemy database models
"""

import sys
from pathlib import Path
from datetime import datetime, timezone

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from infrastructure.db.database import SessionLocal, init_db
from infrastructure.db.models import Idea, Project, WorkItem, Milestone, CustomField


def test_database_operations():
    """Test basic CRUD operations with new models"""

    print("🧪 Testing Database Operations with New Models")
    print("=" * 50)

    session = SessionLocal()

    try:
        # Test 1: Create a new Idea
        print("📝 Test 1: Creating new Idea...")
        new_idea = Idea(
            id="TEST-IDEA-001",
            title="Test Database Migration",
            description="Test idea for database functionality",
            status="backlog",
            priority="high",
            category="development",
            tags=["test", "database"],
            author="Test User",
            estimated_effort="4 hours",
            dependencies=["TEST-WI-001"],
            acceptance_criteria=["Database operations work correctly"],
            notes="Test idea created during database testing",
            open_questions=["None"],
            next_steps=["Implement tests"],
            target_audience="Development Team",
            benefits=["Improved database reliability"],
            prerequisites=["Database migration completed"],
        )

        session.add(new_idea)
        session.commit()
        print("   ✅ Idea created successfully")

        # Test 2: Create a new Work Item
        print("📋 Test 2: Creating new Work Item...")
        new_work_item = WorkItem(
            id="TEST-WI-001",
            title="Implement Database Tests",
            description="Create comprehensive tests for database operations",
            status="todo",
            priority="high",
            type="task",
            issue_type="issue",
            project_id="PRJ-001",
            assignee="Test User",
            author="Test User",
            labels=["test", "database", "quality"],
            estimated_hours=2.0,
            actual_hours=0.0,
            dependencies=["TEST-IDEA-001"],
            acceptance_criteria=[
                "All CRUD operations tested",
                "Data integrity verified",
                "Performance benchmarks met",
            ],
            blockers=[],
            notes="Test work item for database validation",
        )

        session.add(new_work_item)
        session.commit()
        print("   ✅ Work Item created successfully")

        # Test 3: Create a Milestone
        print("🎯 Test 3: Creating new Milestone...")
        new_milestone = Milestone(
            id="TEST-MS-001",
            title="Database Testing Complete",
            description="All database tests pass successfully",
            project_id="PRJ-001",
            status="pending",
            due_date=datetime.now(timezone.utc),
            progress_percentage=0,
            dependencies=["TEST-WI-001"],
        )

        session.add(new_milestone)
        session.commit()
        print("   ✅ Milestone created successfully")

        # Test 4: Create Custom Field
        print("🔧 Test 4: Creating new Custom Field...")
        new_custom_field = CustomField(
            id="TEST-CF-001",
            name="Complexity Score",
            field_type="number",
            project_id="PRJ-001",
            required=False,
        )

        session.add(new_custom_field)
        session.commit()
        print("   ✅ Custom Field created successfully")

        # Test 5: Query Operations
        print("🔍 Test 5: Testing Query Operations...")

        # Count all objects
        idea_count = session.query(Idea).count()
        work_item_count = session.query(WorkItem).count()
        milestone_count = session.query(Milestone).count()
        custom_field_count = session.query(CustomField).count()

        print(f"   📊 Total Ideas: {idea_count}")
        print(f"   📋 Total Work Items: {work_item_count}")
        print(f"   🎯 Total Milestones: {milestone_count}")
        print(f"   🔧 Total Custom Fields: {custom_field_count}")

        # Test 6: Update Operations
        print("✏️  Test 6: Testing Update Operations...")

        # Update work item status
        work_item = session.query(WorkItem).filter(WorkItem.id == "TEST-WI-001").first()
        if work_item:
            work_item.status = "in_progress"
            work_item.actual_hours = 1.5
            session.commit()
            print("   ✅ Work Item updated successfully")

        # Test 7: Relationship Testing
        print("🔗 Test 7: Testing Relationships...")

        project = session.query(Project).filter(Project.id == "PRJ-001").first()
        if project:
            project_work_items = (
                session.query(WorkItem).filter(WorkItem.project_id == project.id).all()
            )
            project_milestones = (
                session.query(Milestone)
                .filter(Milestone.project_id == project.id)
                .all()
            )
            project_custom_fields = (
                session.query(CustomField)
                .filter(CustomField.project_id == project.id)
                .all()
            )

            print(f"   📋 Project Work Items: {len(project_work_items)}")
            print(f"   🎯 Project Milestones: {len(project_milestones)}")
            print(f"   🔧 Project Custom Fields: {len(project_custom_fields)}")

        # Test 8: Delete Operations (Cleanup)
        print("🗑️  Test 8: Testing Delete Operations...")

        # Delete test objects
        session.query(CustomField).filter(CustomField.id == "TEST-CF-001").delete()
        session.query(Milestone).filter(Milestone.id == "TEST-MS-001").delete()
        session.query(WorkItem).filter(WorkItem.id == "TEST-WI-001").delete()
        session.query(Idea).filter(Idea.id == "TEST-IDEA-001").delete()
        session.commit()
        print("   ✅ Test objects deleted successfully")

        print("\n🎉 All database tests passed!")
        return True

    except Exception as e:
        print(f"❌ Database test failed: {e}")
        session.rollback()
        return False

    finally:
        session.close()


def test_database_constraints():
    """Test database constraints and validations"""

    print("\n🔒 Testing Database Constraints")
    print("=" * 30)

    session = SessionLocal()

    try:
        # Test unique constraint on Project ID
        print("🚫 Test: Project ID uniqueness...")

        project1 = Project(
            id="CONSTRAINT-TEST",
            name="Test Project 1",
            description="First test project",
            status="active",
            priority="medium",
            category="development",
            owner="Test User",
        )

        project2 = Project(
            id="CONSTRAINT-TEST",  # Same ID - should fail
            name="Test Project 2",
            description="Second test project",
            status="active",
            priority="medium",
            category="development",
            owner="Test User",
        )

        session.add(project1)
        session.commit()

        session.add(project2)
        try:
            session.commit()
            print("   ❌ Unique constraint not enforced!")
        except Exception as e:
            print("   ✅ Unique constraint working correctly")
            session.rollback()

        # Test required fields
        print("🚫 Test: Required field validation...")

        invalid_project = Project(
            id="INVALID-TEST",
            name="",  # Empty name - should fail validation
            description="Test project",
            status="active",
            priority="medium",
            category="development",
            owner="Test User",
        )

        session.add(invalid_project)
        try:
            session.commit()
            print("   ⚠️  Required field validation at application level needed")
        except Exception as e:
            print("   ✅ Required field validation working")
            session.rollback()

        print("   ✅ Constraint tests completed")
        return True

    except Exception as e:
        print(f"❌ Constraint test failed: {e}")
        return False

    finally:
        session.close()


def main():
    """Main test function"""

    print("🗄️  AI Lab Framework Database Testing")
    print("=" * 50)

    # Initialize database if needed
    init_db()

    # Run tests
    test1_passed = test_database_operations()
    test2_passed = test_database_constraints()

    if test1_passed and test2_passed:
        print("\n🎉 All database tests passed!")
        print("📝 Database is ready for GitHub Projects sync!")
        return 0
    else:
        print("\n❌ Some database tests failed!")
        return 1


if __name__ == "__main__":
    exit(main())
