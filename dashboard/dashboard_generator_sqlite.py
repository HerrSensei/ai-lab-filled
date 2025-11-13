#!/usr/bin/env python3
"""
AI Lab Framework - Updated Dashboard Generator (SQLite Version)
Generates comprehensive dashboard from SQLite database
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from ai_lab_framework.database import AILabDatabase


class SQLiteDashboardGenerator:
    """Generates dashboard from SQLite database"""

    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.output_path = self.base_path / "dashboard"
        self.db = AILabDatabase()

    def calculate_metrics(self) -> Dict[str, Any]:
        """Calculate dashboard metrics from database"""
        # Get work item metrics
        work_metrics = self.db.get_work_item_metrics()

        # Get idea metrics
        idea_metrics = self.db.get_idea_metrics()

        # Get additional statistics
        with self.db.db_path.open() as conn:
            import sqlite3

            connection = sqlite3.connect(str(self.db.db_path))
            cursor = connection.cursor()

            # Component breakdown
            cursor.execute("""
                SELECT component, COUNT(*) as count 
                FROM work_items 
                WHERE component IS NOT NULL AND component != ''
                GROUP BY component
                ORDER BY count DESC
            """)
            components = dict(cursor.fetchall())

            # Status breakdown
            cursor.execute("""
                SELECT status, COUNT(*) as count 
                FROM work_items 
                GROUP BY status
                ORDER BY count DESC
            """)
            status_breakdown = dict(cursor.fetchall())

            # Recent activity (last 7 days)
            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM work_items 
                WHERE updated_date >= date('now', '-7 days')
            """)
            recent_activity = cursor.fetchone()[0]

            connection.close()

        return {
            "work_items": work_metrics,
            "ideas": idea_metrics,
            "components": components,
            "status_breakdown": status_breakdown,
            "recent_activity": recent_activity,
            "database_stats": {
                "total_records": work_metrics["total"] + idea_metrics["total"],
                "work_items": work_metrics["total"],
                "ideas": idea_metrics["total"],
            },
        }

    def generate_dashboard_html(self, metrics: Dict[str, Any]) -> str:
        """Generate HTML dashboard"""
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Lab Framework Dashboard - SQLite Edition</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .dashboard {{ max-width: 1400px; margin: 0 auto; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .header h1 {{ color: #333; margin-bottom: 10px; }}
        .header p {{ color: #666; font-size: 18px; }}
        .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .metric-card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .metric-card h3 {{ margin: 0 0 15px 0; color: #333; }}
        .metric-value {{ font-size: 2.5em; font-weight: bold; color: #2563eb; margin-bottom: 10px; }}
        .metric-label {{ color: #666; font-size: 1.1em; }}
        .progress-bar {{ width: 100%; height: 20px; background: #e9ecef; border-radius: 10px; overflow: hidden; margin-top: 15px; }}
        .progress-fill {{ height: 100%; background: linear-gradient(90deg, #28a745, #20c997); transition: width 0.3s ease; }}
        .priority-breakdown {{ display: flex; justify-content: space-between; margin-top: 15px; }}
        .priority-item {{ text-align: center; }}
        .priority-count {{ font-size: 1.5em; font-weight: bold; display: block; }}
        .priority-label {{ color: #666; font-size: 0.9em; }}
        .high {{ color: #dc3545; }}
        .medium {{ color: #ffc107; }}
        .low {{ color: #28a745; }}
        .component-list {{ margin-top: 15px; }}
        .component-item {{ display: flex; justify-content: space-between; padding: 5px 0; border-bottom: 1px solid #eee; }}
        .status-list {{ margin-top: 15px; }}
        .status-item {{ display: flex; justify-content: space-between; padding: 5px 0; border-bottom: 1px solid #eee; }}
        .last-updated {{ text-align: center; color: #666; margin-top: 30px; }}
        .database-info {{ background: #e3f2fd; padding: 15px; border-radius: 8px; margin-bottom: 20px; }}
        .database-info h4 {{ margin: 0 0 10px 0; color: #1976d2; }}
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <h1>🚀 AI Lab Framework Dashboard</h1>
            <p>SQLite-powered project monitoring and metrics</p>
        </div>
        
        <div class="database-info">
            <h4>🗄️ Database Information</h4>
            <div class="metric-label">
                Total Records: {metrics["database_stats"]["total_records"]} | 
                Work Items: {metrics["database_stats"]["work_items"]} | 
                Ideas: {metrics["database_stats"]["ideas"]} | 
                Recent Activity: {metrics["recent_activity"]} items (7 days)
            </div>
        </div>
        
        <div class="metrics">
            <div class="metric-card">
                <h3>📋 Work Items</h3>
                <div class="metric-value">{metrics["work_items"]["total"]}</div>
                <div class="metric-label">Total work items</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {metrics["work_items"]["completion_rate"]}%"></div>
                </div>
                <div class="metric-label">{metrics["work_items"]["completed"]} of {metrics["work_items"]["total"]} completed ({metrics["work_items"]["completion_rate"]}%)</div>
            </div>
            
            <div class="metric-card">
                <h3>💡 Ideas</h3>
                <div class="metric-value">{metrics["ideas"]["total"]}</div>
                <div class="metric-label">Total ideas</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {metrics["ideas"]["implementation_rate"]}%"></div>
                </div>
                <div class="metric-label">{metrics["ideas"]["implemented"]} implemented ({metrics["ideas"]["implementation_rate"]}%)</div>
            </div>
            
            <div class="metric-card">
                <h3>🎯 Priorities</h3>
                <div class="priority-breakdown">
                    <div class="priority-item">
                        <span class="priority-count high">{metrics["work_items"]["priorities"]["high"]}</span>
                        <span class="priority-label high">High</span>
                    </div>
                    <div class="priority-item">
                        <span class="priority-count medium">{metrics["work_items"]["priorities"]["medium"]}</span>
                        <span class="priority-label medium">Medium</span>
                    </div>
                    <div class="priority-item">
                        <span class="priority-count low">{metrics["work_items"]["priorities"]["low"]}</span>
                        <span class="priority-label low">Low</span>
                    </div>
                </div>
            </div>
            
            <div class="metric-card">
                <h3>📊 Active Work</h3>
                <div class="metric-value">{metrics["work_items"]["in_progress"]}</div>
                <div class="metric-label">Currently in progress</div>
            </div>
            
            <div class="metric-card">
                <h3>🏗️ Components</h3>
                <div class="component-list">
                    {self._format_component_list(metrics["components"])}
                </div>
            </div>
            
            <div class="metric-card">
                <h3>📈 Status Breakdown</h3>
                <div class="status-list">
                    {self._format_status_list(metrics["status_breakdown"])}
                </div>
            </div>
        </div>
        
        <div class="last-updated">
            Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | Powered by SQLite
        </div>
    </div>
</body>
</html>
        """

    def _format_component_list(self, components: Dict[str, int]) -> str:
        """Format component list for HTML"""
        if not components:
            return '<div class="metric-label">No components found</div>'

        items = []
        for component, count in list(components.items())[:5]:  # Top 5
            items.append(f"""
                <div class="component-item">
                    <span>{component}</span>
                    <span><strong>{count}</strong></span>
                </div>
            """)
        return "".join(items)

    def _format_status_list(self, status_breakdown: Dict[str, int]) -> str:
        """Format status list for HTML"""
        if not status_breakdown:
            return '<div class="metric-label">No status data found</div>'

        items = []
        for status, count in status_breakdown.items():
            items.append(f"""
                <div class="status-item">
                    <span>{status}</span>
                    <span><strong>{count}</strong></span>
                </div>
            """)
        return "".join(items)

    def generate_dashboard_data(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Generate JSON data for dashboard"""
        return {
            "timestamp": datetime.now().isoformat(),
            "metrics": metrics,
            "framework_version": "2.0.0",
            "database_version": "SQLite",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

    def generate_dashboard(self) -> None:
        """Generate complete dashboard"""
        print("🚀 Generating AI Lab Framework Dashboard (SQLite Edition)...")

        # Ensure output directory exists
        self.output_path.mkdir(exist_ok=True)

        # Calculate metrics from database
        metrics = self.calculate_metrics()

        # Generate HTML dashboard
        html_content = self.generate_dashboard_html(metrics)

        # Write markdown dashboard
        with open(self.output_path / "DASHBOARD.md", "w", encoding="utf-8") as f:
            f.write("# AI Lab Framework Dashboard (SQLite Edition)\n\n")
            f.write(
                f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            )
            f.write("## 📊 Framework Metrics\n\n")
            f.write(
                f"- **Work Items:** {metrics['work_items']['total']} total, {metrics['work_items']['completed']} completed ({metrics['work_items']['completion_rate']}%)\n"
            )
            f.write(
                f"- **Ideas:** {metrics['ideas']['total']} total, {metrics['ideas']['implemented']} implemented ({metrics['ideas']['implementation_rate']}%)\n"
            )
            f.write(
                f"- **In Progress:** {metrics['work_items']['in_progress']} work items\n"
            )
            f.write(
                f"- **Priorities:** {metrics['work_items']['priorities']['high']} high, {metrics['work_items']['priorities']['medium']} medium, {metrics['work_items']['priorities']['low']} low\n"
            )
            f.write(
                f"- **Database Records:** {metrics['database_stats']['total_records']} total\n"
            )
            f.write(
                f"- **Recent Activity:** {metrics['recent_activity']} items updated in last 7 days\n"
            )

            if metrics["components"]:
                f.write("\n## 🏗️ Component Breakdown\n\n")
                for component, count in list(metrics["components"].items())[:10]:
                    f.write(f"- **{component}:** {count} items\n")

            if metrics["status_breakdown"]:
                f.write("\n## 📈 Status Breakdown\n\n")
                for status, count in metrics["status_breakdown"].items():
                    f.write(f"- **{status}:** {count} items\n")

        # Write HTML dashboard
        with open(self.output_path / "dashboard.html", "w", encoding="utf-8") as f:
            f.write(html_content)

        # Generate JSON data
        dashboard_data = self.generate_dashboard_data(metrics)
        with open(self.output_path / "dashboard_data.json", "w", encoding="utf-8") as f:
            json.dump(dashboard_data, f, indent=2, ensure_ascii=False)

        print("✅ SQLite Dashboard generated successfully!")
        print(
            f"📊 Work Items: {metrics['work_items']['total']} total ({metrics['work_items']['completion_rate']}% complete)"
        )
        print(
            f"💡 Ideas: {metrics['ideas']['total']} total ({metrics['ideas']['implementation_rate']}% implemented)"
        )
        print(f"🗄️ Database Records: {metrics['database_stats']['total_records']} total")
        print(f"📁 Files created: DASHBOARD.md, dashboard.html, dashboard_data.json")


def main():
    """Main dashboard generation function"""
    import argparse

    parser = argparse.ArgumentParser(description="Generate SQLite-powered dashboard")
    parser.add_argument("--base-path", default=".", help="Base path of the project")

    args = parser.parse_args()

    generator = SQLiteDashboardGenerator(args.base_path)
    generator.generate_dashboard()


if __name__ == "__main__":
    main()
