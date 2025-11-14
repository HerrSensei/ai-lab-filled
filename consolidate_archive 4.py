#!/usr/bin/env python3
"""
Consolidate all work-items and ideas from archive into database
"""

import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path


def create_database_schema():
    """Create database schema if not exists"""
    conn = sqlite3.connect("ai_lab.db")
    cursor = conn.cursor()

    # Create work_items table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS work_items (
            id VARCHAR PRIMARY KEY,
            title VARCHAR NOT NULL,
            description TEXT NOT NULL,
            status VARCHAR NOT NULL,
            priority VARCHAR NOT NULL,
            type VARCHAR NOT NULL,
            project VARCHAR,
            assignee VARCHAR,
            tags TEXT,
            created_date DATETIME NOT NULL,
            updated_date DATETIME NOT NULL,
            due_date DATETIME,
            estimated_hours FLOAT,
            actual_hours FLOAT,
            dependencies TEXT,
            acceptance_criteria TEXT,
            blockers TEXT,
            notes TEXT,
            file_path VARCHAR
        )
    """
    )

    # Create ideas table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS ideas (
            id VARCHAR PRIMARY KEY,
            title VARCHAR NOT NULL,
            description TEXT NOT NULL,
            status VARCHAR NOT NULL,
            priority VARCHAR NOT NULL,
            category VARCHAR NOT NULL,
            tags TEXT,
            created_date DATETIME NOT NULL,
            updated_date DATETIME NOT NULL,
            estimated_effort VARCHAR,
            dependencies TEXT,
            acceptance_criteria TEXT,
            notes TEXT,
            author VARCHAR,
            open_questions TEXT,
            next_steps TEXT,
            target_audience VARCHAR,
            benefits TEXT,
            prerequisites TEXT
        )
    """
    )

    conn.commit()
    conn.close()


def parse_work_item(file_path):
    """Parse a work item JSON file"""
    try:
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)

        # Convert lists to JSON strings for storage
        for field in ["tags", "dependencies", "acceptance_criteria", "blockers"]:
            if field in data and isinstance(data[field], list):
                data[field] = json.dumps(data[field])

        # Handle sub_tasks separately (not storing in main table)
        if "sub_tasks" in data:
            del data["sub_tasks"]

        return data
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return None


def parse_idea_from_markdown(file_path):
    """Parse ideas from markdown files"""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        # This is a simplified parser - in real implementation you'd want more sophisticated parsing
        # For now, we'll create a basic idea entry

        title = os.path.basename(file_path).replace(".md", "").replace("_", " ").title()

        return {
            "id": f"IDEA-{hash(title) % 10000:04d}",
            "title": title,
            "description": content[:500] + "..." if len(content) > 500 else content,
            "status": "backlog",
            "priority": "medium",
            "category": "general",
            "tags": json.dumps(["archive"]),
            "created_date": datetime.now().isoformat(),
            "updated_date": datetime.now().isoformat(),
            "estimated_effort": None,
            "dependencies": None,
            "acceptance_criteria": None,
            "notes": f"Imported from archive file: {file_path}",
            "author": "archive",
            "open_questions": None,
            "next_steps": None,
            "target_audience": None,
            "benefits": None,
            "prerequisites": None,
        }
    except Exception as e:
        print(f"Error parsing idea from {file_path}: {e}")
        return None


def insert_work_item(conn, work_item):
    """Insert a work item into the database"""
    cursor = conn.cursor()

    # Prepare values with proper defaults
    values = (
        work_item.get("id"),
        work_item.get("title"),
        work_item.get("description"),
        work_item.get("status"),
        work_item.get("priority"),
        work_item.get("type") or "task",  # Default to 'task' if missing
        work_item.get("project"),
        work_item.get("assignee"),
        work_item.get("tags"),
        work_item.get("created_date"),
        work_item.get("updated_date"),
        work_item.get("due_date"),
        work_item.get("estimated_hours"),
        work_item.get("actual_hours"),
        work_item.get("dependencies"),
        work_item.get("acceptance_criteria"),
        work_item.get("blockers"),
        work_item.get("notes"),
        work_item.get("file_path"),
    )

    cursor.execute(
        """
        INSERT OR REPLACE INTO work_items (
            id, title, description, status, priority, type, project, assignee,
            tags, created_date, updated_date, due_date, estimated_hours,
            actual_hours, dependencies, acceptance_criteria, blockers, notes, file_path
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        values,
    )

    conn.commit()


def insert_idea(conn, idea):
    """Insert an idea into the database"""
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO ideas (
            id, title, description, status, priority, category, tags,
            created_date, updated_date, estimated_effort, dependencies,
            acceptance_criteria, notes, author, open_questions, next_steps,
            target_audience, benefits, prerequisites
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            idea.get("id"),
            idea.get("title"),
            idea.get("description"),
            idea.get("status"),
            idea.get("priority"),
            idea.get("category"),
            idea.get("tags"),
            idea.get("created_date"),
            idea.get("updated_date"),
            idea.get("estimated_effort"),
            idea.get("dependencies"),
            idea.get("acceptance_criteria"),
            idea.get("notes"),
            idea.get("author"),
            idea.get("open_questions"),
            idea.get("next_steps"),
            idea.get("target_audience"),
            idea.get("benefits"),
            idea.get("prerequisites"),
        ),
    )

    conn.commit()


def main():
    """Main consolidation function"""
    print("🔄 Starting archive consolidation...")

    # Create database schema
    create_database_schema()

    # Connect to database
    conn = sqlite3.connect("ai_lab.db")

    archive_path = Path("archive/old-data")

    # Process work items
    print("\n📋 Processing work items...")
    work_item_files = (
        list(archive_path.glob("FRM-*.json"))
        + list(archive_path.glob("HS-*.json"))
        + list(archive_path.glob("INF-*.json"))
        + list(archive_path.glob("HYB-*.json"))
    )

    work_items_processed = 0
    for file_path in work_item_files:
        work_item = parse_work_item(file_path)
        if work_item:
            insert_work_item(conn, work_item)
            work_items_processed += 1
            print(f"  ✅ Processed: {work_item['id']} - {work_item['title']}")

    # Process ideas from markdown files
    print("\n💡 Processing ideas...")
    idea_files = list(archive_path.glob("*IDEAS*.md")) + list(
        archive_path.glob("ideas_*.md")
    )

    ideas_processed = 0
    for file_path in idea_files:
        idea = parse_idea_from_markdown(file_path)
        if idea:
            insert_idea(conn, idea)
            ideas_processed += 1
            print(f"  ✅ Processed: {idea['id']} - {idea['title']}")

    # Close connection
    conn.close()

    # Print summary
    print("\n📊 Consolidation Summary:")
    print(f"  Work items processed: {work_items_processed}")
    print(f"  Ideas processed: {ideas_processed}")
    print(f"  Total items: {work_items_processed + ideas_processed}")

    # Verify data
    print("\n🔍 Verifying data...")
    conn = sqlite3.connect("ai_lab.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM work_items")
    work_items_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM ideas")
    ideas_count = cursor.fetchone()[0]

    cursor.execute("SELECT DISTINCT status FROM work_items")
    work_statuses = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT status FROM ideas")
    idea_statuses = [row[0] for row in cursor.fetchall()]

    conn.close()

    print(f"  Database work items: {work_items_count}")
    print(f"  Database ideas: {ideas_count}")
    print(f"  Work item statuses: {', '.join(work_statuses)}")
    print(f"  Idea statuses: {', '.join(idea_statuses)}")

    print("\n✅ Archive consolidation completed successfully!")


if __name__ == "__main__":
    main()
