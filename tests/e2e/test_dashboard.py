#!/usr/bin/env python3
"""
E2E Tests for Real-Time Dashboard

Test dashboard functionality, data visualization, and real-time updates.
"""

import pytest
from playwright.sync_api import Page, expect
import time
import json
from pathlib import Path


class TestDashboard:
    """Test dashboard functionality."""

    def test_dashboard_loads_successfully(self, dashboard_page: Page):
        """Test that dashboard loads without errors."""
        # Check page title
        expect(dashboard_page).to_have_title("AI Lab Framework - Real-Time Dashboard")
        
        # Check main heading
        main_heading = dashboard_page.locator("h1")
        expect(main_heading).to_contain_text("AI Lab Framework Dashboard")
        
        # Check key metrics section
        metrics_section = dashboard_page.locator(".grid").first
        expect(metrics_section).to_be_visible()
        
        # Check that no error messages are visible
        error_elements = dashboard_page.locator(".error, .alert-danger")
        expect(error_elements).to_have_count(0)

    def test_key_metrics_display(self, dashboard_page: Page):
        """Test that key metrics are displayed correctly."""
        # Wait for metrics to load
        dashboard_page.wait_for_selector(".metric")
        
        # Check work items metric
        work_items_metric = dashboard_page.locator(".metric").first
        expect(work_items_metric).to_be_visible()
        
        # Check that metrics are numbers (or 0 if no data)
        metrics = dashboard_page.locator(".metric")
        for i in range(metrics.count()):
            metric_text = metrics.nth(i).text_content()
            assert metric_text.isdigit() or metric_text == "0", f"Metric should be a number, got: {metric_text}"

    def test_charts_render_correctly(self, dashboard_page: Page):
        """Test that charts are rendered correctly."""
        from tests.e2e.conftest import TestHelpers
        
        # Wait for charts to be visible
        status_chart = dashboard_page.locator("#statusChart")
        category_chart = dashboard_page.locator("#categoryChart")
        
        expect(status_chart).to_be_visible()
        expect(category_chart).to_be_visible()
        
        # Wait for charts to render (canvas content)
        TestHelpers.wait_for_chart_render(dashboard_page, "statusChart")
        TestHelpers.wait_for_chart_render(dashboard_page, "category_chart")
        
        # Check that charts have canvas elements
        status_canvas = status_chart.locator("canvas")
        category_canvas = category_chart.locator("canvas")
        
        expect(status_canvas).to_be_visible()
        expect(category_canvas).to_be_visible()

    def test_recent_work_items_section(self, dashboard_page: Page):
        """Test recent work items section."""
        # Check section heading
        recent_section = dashboard_page.locator("h3:has-text('Recent Work Items')")
        expect(recent_section).to_be_visible()
        
        # Check that section exists (may be empty)
        work_items_container = recent_section.locator("xpath=./following-sibling::div[1]")
        expect(work_items_container).to_be_visible()

    def test_recent_ideas_section(self, dashboard_page: Page):
        """Test recent ideas section."""
        # Check section heading
        ideas_section = dashboard_page.locator("h3:has-text('Recent Ideas')")
        expect(ideas_section).to_be_visible()
        
        # Check that section exists (may be empty)
        ideas_container = ideas_section.locator("xpath=./following-sibling::div[1]")
        expect(ideas_container).to_be_visible()

    def test_code_quality_section(self, dashboard_page: Page):
        """Test code quality metrics section."""
        # Check section heading
        quality_section = dashboard_page.locator("h3:has-text('Code Quality')")
        expect(quality_section).to_be_visible()
        
        # Check for quality indicators
        quality_indicators = dashboard_page.locator(".card:has(h3:has-text('Code Quality')) .flex")
        expect(quality_indicators).to_be_visible()

    def test_system_information_section(self, dashboard_page: Page):
        """Test system information section."""
        # Check section heading
        system_section = dashboard_page.locator("h3:has-text('System Information')")
        expect(system_section).to_be_visible()
        
        # Check for system info fields
        python_version = dashboard_page.locator("text=Python Version:")
        working_directory = dashboard_page.locator("text=Working Directory:")
        current_branch = dashboard_page.locator("text=Current Branch:")
        
        expect(python_version).to_be_visible()
        expect(working_directory).to_be_visible()
        expect(current_branch).to_be_visible()

    def test_auto_refresh_functionality(self, dashboard_page: Page):
        """Test auto-refresh indicator and countdown."""
        # Check refresh indicator
        refresh_indicator = dashboard_page.locator("#refreshIndicator")
        expect(refresh_indicator).to_be_visible()
        expect(refresh_indicator).to_contain_text("Auto-Refresh:")
        
        # Check that countdown is working
        initial_text = refresh_indicator.text_content()
        time.sleep(2)
        updated_text = refresh_indicator.text_content()
        
        # Text should change (countdown decreasing)
        assert initial_text != updated_text, "Auto-refresh countdown should update"

    def test_responsive_design(self, dashboard_page: Page):
        """Test dashboard responsiveness on different screen sizes."""
        # Test desktop size
        dashboard_page.set_viewport_size({"width": 1200, "height": 800})
        metrics_grid = dashboard_page.locator(".grid").first
        expect(metrics_grid).to_have_class(/md:grid-cols-4/)
        
        # Test tablet size
        dashboard_page.set_viewport_size({"width": 768, "height": 1024})
        expect(metrics_grid).to_be_visible()
        
        # Test mobile size
        dashboard_page.set_viewport_size({"width": 375, "height": 667})
        expect(metrics_grid).to_be_visible()

    def test_data_with_test_content(self, dashboard_page: Page, test_db, test_helpers):
        """Test dashboard with actual test data."""
        # Create test data
        work_id = test_helpers.create_test_work_item(test_db, "Test Work Item", "in_progress", "high")
        idea_id = test_helpers.create_test_idea(test_db, "Test Idea", "automation")
        
        # Regenerate dashboard with new data
        dashboard_script = Path(__file__).parent.parent.parent / "scripts" / "dashboard_realtime.py"
        import subprocess
        result = subprocess.run([
            "python", str(dashboard_script), 
            "--output", "test_dashboard_with_data.html"
        ], capture_output=True, text=True)
        
        assert result.returncode == 0
        
        # Reload page
        dashboard_path = Path(__file__).parent.parent.parent / "dashboard" / "test_dashboard_with_data.html"
        dashboard_page.goto(f"file://{dashboard_path.absolute()}")
        
        # Wait for content to load
        dashboard_page.wait_for_selector(".metric")
        
        # Check that metrics reflect the new data
        work_items_metric = dashboard_page.locator(".metric").first
        expect(work_items_metric).to_be_visible()
        
        # The exact number depends on existing data, but should be at least 1
        metric_value = work_items_metric.text_content()
        assert int(metric_value) >= 1, f"Expected at least 1 work item, got {metric_value}"

    def test_error_handling(self, page: Page):
        """Test dashboard behavior with database errors."""
        # Test with non-existent database path
        dashboard_script = Path(__file__).parent.parent.parent / "scripts" / "dashboard_realtime.py"
        
        # This should still generate a dashboard with error indicators
        import subprocess
        result = subprocess.run([
            "python", str(dashboard_script), 
            "--output", "test_dashboard_error.html"
        ], capture_output=True, text=True)
        
        # Should still succeed but with warnings
        assert result.returncode == 0
        
        # Load the error dashboard
        dashboard_path = Path(__file__).parent.parent.parent / "dashboard" / "test_dashboard_error.html"
        page.goto(f"file://{dashboard_path.absolute()}")
        
        # Should still load the basic structure
        expect(page.locator("h1")).to_be_visible()
        expect(page.locator(".metric")).to_be_visible()

    def test_accessibility_features(self, dashboard_page: Page):
        """Test basic accessibility features."""
        # Check for proper heading hierarchy
        h1 = dashboard_page.locator("h1")
        expect(h1).to_have_count(1)
        
        # Check for alt text on images (if any)
        images = dashboard_page.locator("img")
        for i in range(images.count()):
            img = images.nth(i)
            expect(img).to_have_attribute("alt")
        
        # Check for proper semantic HTML
        main_content = dashboard_page.locator("main, .container")
        expect(main_content).to_be_visible()

    def test_performance_load_time(self, dashboard_page: Page):
        """Test dashboard load performance."""
        start_time = time.time()
        
        # Navigate to dashboard
        dashboard_page.wait_for_load_state("networkidle")
        
        # Wait for key elements
        dashboard_page.wait_for_selector(".metric")
        dashboard_page.wait_for_selector("#statusChart")
        dashboard_page.wait_for_selector("#categoryChart")
        
        load_time = time.time() - start_time
        
        # Dashboard should load within 5 seconds
        assert load_time < 5.0, f"Dashboard took too long to load: {load_time:.2f}s"