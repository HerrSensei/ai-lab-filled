#!/usr/bin/env python3
"""
E2E Tests Configuration

Shared configuration and fixtures for Playwright E2E tests.
"""

import pytest
from playwright.sync_api import Page, expect
from pathlib import Path
import tempfile
import shutil
import sqlite3
import json


@pytest.fixture(scope="session")
def test_db():
    """Create temporary test database."""
    temp_dir = tempfile.mkdtemp()
    db_path = Path(temp_dir) / "test_ai_lab.db"

    # Copy schema from main database
    main_db = Path(__file__).parent.parent.parent / "data" / "ai_lab.db"
    if main_db.exists():
        shutil.copy2(main_db, db_path)
    else:
        # Create empty database with schema
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Create work_items table
        cursor.execute("""
            CREATE TABLE work_items (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'todo',
                priority TEXT DEFAULT 'medium',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create ideas table
        cursor.execute("""
            CREATE TABLE ideas (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                category TEXT,
                status TEXT DEFAULT 'draft',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()

    yield db_path

    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def page(page: Page):
    """Configure page with default settings."""
    # Set default timeout
    page.set_default_timeout(10000)

    # Handle console errors
    def handle_console_error(msg):
        if msg.type == "error":
            pytest.fail(f"Console error: {msg.text}")

    page.on("console", handle_console_error)

    yield page


@pytest.fixture
def dashboard_page(page: Page, test_db):
    """Navigate to dashboard page."""
    # Generate dashboard with test database
    dashboard_script = (
        Path(__file__).parent.parent.parent / "scripts" / "dashboard_realtime.py"
    )

    # Update script to use test database
    import subprocess

    result = subprocess.run(
        ["python", str(dashboard_script), "--output", "test_dashboard.html"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, f"Dashboard generation failed: {result.stderr}"

    # Navigate to test dashboard
    dashboard_path = (
        Path(__file__).parent.parent.parent / "dashboard" / "test_dashboard.html"
    )
    page.goto(f"file://{dashboard_path.absolute()}")

    return page


class TestHelpers:
    """Helper methods for E2E tests."""

    @staticmethod
    def create_test_work_item(
        db_path: Path, title: str, status: str = "todo", priority: str = "medium"
    ):
        """Create a test work item in database."""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        import uuid

        work_id = str(uuid.uuid4())

        cursor.execute(
            """
            INSERT INTO work_items (id, title, description, status, priority)
            VALUES (?, ?, ?, ?, ?)
        """,
            (work_id, title, f"Test description for {title}", status, priority),
        )

        conn.commit()
        conn.close()

        return work_id

    @staticmethod
    def create_test_idea(db_path: Path, title: str, category: str = "general"):
        """Create a test idea in database."""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        import uuid

        idea_id = str(uuid.uuid4())

        cursor.execute(
            """
            INSERT INTO ideas (id, title, description, category, status)
            VALUES (?, ?, ?, ?, ?)
        """,
            (idea_id, title, f"Test idea description for {title}", category, "draft"),
        )

        conn.commit()
        conn.close()

        return idea_id

    @staticmethod
    def wait_for_chart_render(page: Page, chart_id: str):
        """Wait for chart to be rendered."""
        chart_element = page.locator(f"#{chart_id}")
        expect(chart_element).to_be_visible()

        # Wait for canvas to have content
        page.wait_for_function(f"""
            () => {{
                const canvas = document.getElementById('{chart_id}');
                return canvas && canvas.getContext('2d') && 
                       canvas.width > 0 && canvas.height > 0;
            }}
        """)


@pytest.fixture
def test_helpers():
    """Provide test helper methods."""
    return TestHelpers()
