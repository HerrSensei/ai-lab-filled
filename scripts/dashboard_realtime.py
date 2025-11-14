#!/usr/bin/env python3
"""
AI Lab Framework - Real-Time Dashboard Generator

Erstellt ein interaktives Dashboard mit Echtzeit-Datenbankanbindung,
automatischen Updates und umfassenden Visualisierungen.

Usage:
    python scripts/dashboard_realtime.py --port=8080
    python scripts/dashboard_realtime.py --output=dashboard.html
    python scripts/dashboard_realtime.py --auto-refresh=30
"""

import argparse
import json
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import subprocess


class RealTimeDashboard:
    """Real-time dashboard with database integration."""

    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = base_dir or Path.cwd()
        self.db_path = self.base_dir / "data" / "ai_lab.db"
        self.output_dir = self.base_dir / "dashboard"
        self.output_dir.mkdir(exist_ok=True)

    def generate_dashboard(
        self,
        output_file: Optional[str] = None,
        port: Optional[int] = None,
        auto_refresh: int = 60,
    ) -> str:
        """Generate real-time dashboard."""
        print("🚀 Generating real-time dashboard...")

        # Collect data
        dashboard_data = self._collect_dashboard_data()

        # Generate HTML
        html_content = self._generate_html(dashboard_data, auto_refresh)

        # Save or serve
        if output_file:
            output_path = Path(output_file)
            output_path.write_text(html_content, encoding="utf-8")
            print(f"✅ Dashboard saved to: {output_path}")
            return str(output_path)
        elif port:
            return self._serve_dashboard(html_content, port)
        else:
            # Default output
            output_path = self.output_dir / "dashboard_realtime.html"
            output_path.write_text(html_content, encoding="utf-8")
            print(f"✅ Dashboard saved to: {output_path}")
            return str(output_path)

    def _collect_dashboard_data(self) -> Dict[str, Any]:
        """Collect all dashboard data from database and files."""
        data = {
            "timestamp": datetime.now().isoformat(),
            "work_items": self._get_work_items_data(),
            "ideas": self._get_ideas_data(),
            "projects": self._get_projects_data(),
            "github": self._get_github_data(),
            "system": self._get_system_data(),
            "sessions": self._get_sessions_data(),
            "quality": self._get_quality_data(),
        }
        return data

    def _get_work_items_data(self) -> Dict[str, Any]:
        """Get work items statistics and data."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Overall statistics
            cursor.execute("SELECT COUNT(*) FROM work_items")
            total_items = cursor.fetchone()[0]

            cursor.execute("SELECT status, COUNT(*) FROM work_items GROUP BY status")
            status_counts = dict(cursor.fetchall())

            cursor.execute(
                "SELECT priority, COUNT(*) FROM work_items GROUP BY priority"
            )
            priority_counts = dict(cursor.fetchall())

            # Recent items
            cursor.execute("""
                SELECT id, title, status, priority, created_date, updated_date 
                FROM work_items 
                ORDER BY created_date DESC 
                LIMIT 10
            """)
            recent_items = [
                {
                    "id": row[0],
                    "title": row[1],
                    "status": row[2],
                    "priority": row[3],
                    "created_at": row[4],
                    "updated_at": row[5],
                }
                for row in cursor.fetchall()
            ]

            # Completion trends (last 30 days)
            thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat()
            cursor.execute(
                """
                SELECT DATE(updated_date) as date, COUNT(*) as count
                FROM work_items 
                WHERE status = 'done' AND updated_date > ?
                GROUP BY DATE(updated_date)
                ORDER BY date
            """,
                (thirty_days_ago,),
            )
            completion_trends = dict(cursor.fetchall())

            conn.close()

            return {
                "total": total_items,
                "by_status": status_counts,
                "by_priority": priority_counts,
                "recent": recent_items,
                "completion_trends": completion_trends,
                "completion_rate": self._calculate_completion_rate(),
            }

        except Exception as e:
            print(f"⚠️  Error getting work items data: {e}")
            return {"error": str(e)}

    def _get_ideas_data(self) -> Dict[str, Any]:
        """Get ideas statistics and data."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM ideas")
            total_ideas = cursor.fetchone()[0]

            cursor.execute("SELECT category, COUNT(*) FROM ideas GROUP BY category")
            category_counts = dict(cursor.fetchall())

            cursor.execute("SELECT status, COUNT(*) FROM ideas GROUP BY status")
            status_counts = dict(cursor.fetchall())

            # Recent ideas
            cursor.execute("""
                SELECT id, title, category, status, created_date 
                FROM ideas 
                ORDER BY created_date DESC 
                LIMIT 10
            """)
            recent_ideas = [
                {
                    "id": row[0],
                    "title": row[1],
                    "category": row[2],
                    "status": row[3],
                    "created_at": row[4],
                }
                for row in cursor.fetchall()
            ]

            conn.close()

            return {
                "total": total_ideas,
                "by_category": category_counts,
                "by_status": status_counts,
                "recent": recent_ideas,
            }

        except Exception as e:
            print(f"⚠️  Error getting ideas data: {e}")
            return {"error": str(e)}

    def _get_projects_data(self) -> Dict[str, Any]:
        """Get projects data."""
        projects_dir = self.base_dir / "projects"
        if not projects_dir.exists():
            return {"total": 0, "projects": []}

        projects = []
        for project_dir in projects_dir.iterdir():
            if project_dir.is_dir():
                # Get project info
                readme_path = project_dir / "README.md"
                readme_content = readme_path.read_text() if readme_path.exists() else ""

                # Count files
                python_files = len(list(project_dir.rglob("*.py")))
                yaml_files = len(list(project_dir.rglob("*.yaml"))) + len(
                    list(project_dir.rglob("*.yml"))
                )

                projects.append(
                    {
                        "name": project_dir.name,
                        "readme": readme_content[:200] + "..."
                        if len(readme_content) > 200
                        else readme_content,
                        "python_files": python_files,
                        "yaml_files": yaml_files,
                        "last_modified": datetime.fromtimestamp(
                            project_dir.stat().st_mtime
                        ).isoformat(),
                    }
                )

        return {"total": len(projects), "projects": projects}

    def _get_github_data(self) -> Dict[str, Any]:
        """Get GitHub integration data."""
        try:
            # Get git stats
            result = subprocess.run(
                ["git", "log", "--oneline", "--since='30 days ago'"],
                capture_output=True,
                text=True,
                check=True,
            )
            recent_commits = (
                len(result.stdout.strip().split("\n")) if result.stdout.strip() else 0
            )

            # Get current branch and commit
            branch_result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True,
                text=True,
                check=True,
            )
            current_branch = branch_result.stdout.strip()

            commit_result = subprocess.run(
                ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True
            )
            current_commit = commit_result.stdout.strip()[:8]

            return {
                "recent_commits": recent_commits,
                "current_branch": current_branch,
                "current_commit": current_commit,
                "last_sync": datetime.now().isoformat(),
            }

        except Exception as e:
            return {"error": str(e)}

    def _get_system_data(self) -> Dict[str, Any]:
        """Get system information."""
        return {
            "python_version": sys.version,
            "working_directory": str(self.base_dir),
            "dashboard_version": "2.0.0",
            "last_update": datetime.now().isoformat(),
            "uptime": "N/A",  # Could be implemented
        }

    def _get_sessions_data(self) -> Dict[str, Any]:
        """Get recent session data."""
        sessions_dir = self.base_dir / "ai-logs" / "logs" / "sessions"
        if not sessions_dir.exists():
            return {"recent": [], "total": 0}

        sessions = []
        for json_file in sorted(sessions_dir.glob("*.json"), reverse=True)[:10]:
            try:
                with open(json_file) as f:
                    session_data = json.load(f)
                    sessions.append(
                        {
                            "session_id": session_data.get("session_id"),
                            "timestamp": session_data.get("timestamp"),
                            "session_type": session_data.get("session_type"),
                            "git_branch": session_data.get("git_branch"),
                            "git_commit": session_data.get("git_commit"),
                        }
                    )
            except (json.JSONDecodeError, FileNotFoundError):
                continue

        return {"recent": sessions, "total": len(list(sessions_dir.glob("*.json")))}

    def _get_quality_data(self) -> Dict[str, Any]:
        """Get quality metrics."""
        try:
            # Run quality checks
            quality_data = {}

            # Black check
            try:
                result = subprocess.run(
                    ["black", "--check", "--diff", "--quiet", "."],
                    capture_output=True,
                    text=True,
                )
                quality_data["black_status"] = (
                    "passed" if result.returncode == 0 else "failed"
                )
            except FileNotFoundError:
                quality_data["black_status"] = "not_installed"

            # Ruff check
            try:
                result = subprocess.run(
                    ["ruff", "check", "."], capture_output=True, text=True
                )
                quality_data["ruff_issues"] = (
                    len(result.stdout.strip().split("\n"))
                    if result.stdout.strip()
                    else 0
                )
                quality_data["ruff_status"] = (
                    "passed" if result.returncode == 0 else "failed"
                )
            except FileNotFoundError:
                quality_data["ruff_status"] = "not_installed"
                quality_data["ruff_issues"] = 0

            # MyPy check
            try:
                result = subprocess.run(
                    ["mypy", "src/"], capture_output=True, text=True
                )
                quality_data["mypy_status"] = (
                    "passed" if result.returncode == 0 else "failed"
                )
            except FileNotFoundError:
                quality_data["mypy_status"] = "not_installed"

            return quality_data

        except Exception as e:
            return {"error": str(e)}

    def _calculate_completion_rate(self) -> float:
        """Calculate work item completion rate."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM work_items")
            total = cursor.fetchone()[0]

            if total == 0:
                return 0.0

            cursor.execute("SELECT COUNT(*) FROM work_items WHERE status = 'done'")
            completed = cursor.fetchone()[0]

            conn.close()
            return round((completed / total) * 100, 2)

        except Exception:
            return 0.0

    def _generate_html(self, data: Dict[str, Any], auto_refresh: int) -> str:
        """Generate HTML dashboard."""
        html_template = f"""
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Lab Framework - Real-Time Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .card {{ @apply bg-white rounded-lg shadow-md p-6 mb-6; }}
        .metric {{ @apply text-3xl font-bold text-blue-600; }}
        .status-completed {{ @apply bg-green-100 text-green-800; }}
        .status-in-progress {{ @apply bg-yellow-100 text-yellow-800; }}
        .status-todo {{ @apply bg-gray-100 text-gray-800; }}
        .priority-high {{ @apply bg-red-100 text-red-800; }}
        .priority-medium {{ @apply bg-orange-100 text-orange-800; }}
        .priority-low {{ @apply bg-blue-100 text-blue-800; }}
        .refresh-indicator {{ 
            position: fixed; 
            top: 20px; 
            right: 20px; 
            background: #10b981; 
            color: white; 
            padding: 8px 16px; 
            border-radius: 20px; 
            font-size: 12px;
            z-index: 1000;
        }}
    </style>
</head>
<body class="bg-gray-50">
    <div class="refresh-indicator" id="refreshIndicator">
        🔄 Auto-Refresh: {auto_refresh}s
    </div>
    
    <div class="container mx-auto px-4 py-8">
        <header class="mb-8">
            <h1 class="text-4xl font-bold text-gray-800 mb-2">AI Lab Framework Dashboard</h1>
            <p class="text-gray-600">Real-time project overview and metrics</p>
            <p class="text-sm text-gray-500">Last updated: {data["timestamp"]}</p>
        </header>

        <!-- Key Metrics -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div class="card">
                <h3 class="text-lg font-semibold mb-2">Work Items</h3>
                <div class="metric">{data.get("work_items", {}).get("total", 0)}</div>
                <p class="text-sm text-gray-600">Completion Rate: {data.get("work_items", {}).get("completion_rate", 0)}%</p>
            </div>
            <div class="card">
                <h3 class="text-lg font-semibold mb-2">Ideas</h3>
                <div class="metric">{data.get("ideas", {}).get("total", 0)}</div>
                <p class="text-sm text-gray-600">Active ideas</p>
            </div>
            <div class="card">
                <h3 class="text-lg font-semibold mb-2">Projects</h3>
                <div class="metric">{data.get("projects", {}).get("total", 0)}</div>
                <p class="text-sm text-gray-600">Active projects</p>
            </div>
            <div class="card">
                <h3 class="text-lg font-semibold mb-2">Sessions</h3>
                <div class="metric">{data.get("sessions", {}).get("total", 0)}</div>
                <p class="text-sm text-gray-600">Total sessions</p>
            </div>
        </div>

        <!-- Charts Row -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div class="card">
                <h3 class="text-lg font-semibold mb-4">Work Items by Status</h3>
                <canvas id="statusChart" width="400" height="200"></canvas>
            </div>
            <div class="card">
                <h3 class="text-lg font-semibold mb-4">Ideas by Category</h3>
                <canvas id="categoryChart" width="400" height="200"></canvas>
            </div>
        </div>

        <!-- Recent Activity -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div class="card">
                <h3 class="text-lg font-semibold mb-4">Recent Work Items</h3>
                <div class="space-y-2">
                    {self._generate_recent_work_items_html(data.get("work_items", {}).get("recent", []))}
                </div>
            </div>
            <div class="card">
                <h3 class="text-lg font-semibold mb-4">Recent Ideas</h3>
                <div class="space-y-2">
                    {self._generate_recent_ideas_html(data.get("ideas", {}).get("recent", []))}
                </div>
            </div>
        </div>

        <!-- Quality Metrics -->
        <div class="card mb-8">
            <h3 class="text-lg font-semibold mb-4">Code Quality</h3>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                {self._generate_quality_html(data.get("quality", {}))}
            </div>
        </div>

        <!-- System Info -->
        <div class="card">
            <h3 class="text-lg font-semibold mb-4">System Information</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div>
                    <strong>Python Version:</strong> {data.get("system", {}).get("python_version", "N/A")[:50]}...
                </div>
                <div>
                    <strong>Working Directory:</strong> {data.get("system", {}).get("working_directory", "N/A")}
                </div>
                <div>
                    <strong>Current Branch:</strong> {data.get("github", {}).get("current_branch", "N/A")}
                </div>
                <div>
                    <strong>Current Commit:</strong> {data.get("github", {}).get("current_commit", "N/A")}
                </div>
            </div>
        </div>
    </div>

    <script>
        // Auto-refresh
        setInterval(() => {{
            location.reload();
        }}, {auto_refresh * 1000});

        // Update refresh indicator
        let refreshTime = {auto_refresh};
        setInterval(() => {{
            refreshTime--;
            document.getElementById('refreshIndicator').textContent = `🔄 Auto-Refresh: ${{refreshTime}}s`;
            if (refreshTime <= 0) refreshTime = {auto_refresh};
        }}, 1000);

        // Charts
        const statusData = {json.dumps(data.get("work_items", {}).get("by_status", {}))};
        const categoryData = {json.dumps(data.get("ideas", {}).get("by_category", {}))};

        // Status Chart
        new Chart(document.getElementById('statusChart'), {{
            type: 'doughnut',
            data: {{
                labels: Object.keys(statusData),
                datasets: [{{
                    data: Object.values(statusData),
                    backgroundColor: ['#10b981', '#f59e0b', '#6b7280', '#ef4444']
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false
            }}
        }});

        // Category Chart
        new Chart(document.getElementById('categoryChart'), {{
            type: 'bar',
            data: {{
                labels: Object.keys(categoryData),
                datasets: [{{
                    label: 'Ideas by Category',
                    data: Object.values(categoryData),
                    backgroundColor: '#3b82f6'
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    y: {{
                        beginAtZero: true
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
        """
        return html_template

    def _generate_recent_work_items_html(self, items: List[Dict]) -> str:
        """Generate HTML for recent work items."""
        if not items:
            return "<p class='text-gray-500'>No recent work items</p>"

        html = ""
        for item in items[:5]:
            status_class = f"status-{item.get('status', 'todo').replace('_', '-')}"
            priority_class = f"priority-{item.get('priority', 'medium')}"

            html += f"""
            <div class="flex justify-between items-center p-2 border rounded">
                <div class="flex-1">
                    <div class="font-medium">{item.get("title", "N/A")}</div>
                    <div class="text-xs text-gray-500">{item.get("updated_at", "N/A")[:10]}</div>
                </div>
                <div class="flex gap-2">
                    <span class="px-2 py-1 text-xs rounded {status_class}">{item.get("status", "N/A")}</span>
                    <span class="px-2 py-1 text-xs rounded {priority_class}">{item.get("priority", "N/A")}</span>
                </div>
            </div>
            """
        return html

    def _generate_recent_ideas_html(self, ideas: List[Dict]) -> str:
        """Generate HTML for recent ideas."""
        if not ideas:
            return "<p class='text-gray-500'>No recent ideas</p>"

        html = ""
        for idea in ideas[:5]:
            html += f"""
            <div class="flex justify-between items-center p-2 border rounded">
                <div class="flex-1">
                    <div class="font-medium">{idea.get("title", "N/A")}</div>
                    <div class="text-xs text-gray-500">{idea.get("category", "N/A")} • {idea.get("created_at", "N/A")[:10]}</div>
                </div>
                <div class="px-2 py-1 text-xs rounded bg-purple-100 text-purple-800">
                    {idea.get("status", "N/A")}
                </div>
            </div>
            """
        return html

    def _generate_quality_html(self, quality_data: Dict) -> str:
        """Generate HTML for quality metrics."""
        html = ""

        quality_items = [
            ("Black", quality_data.get("black_status", "unknown"), "#000000"),
            ("Ruff", quality_data.get("ruff_status", "unknown"), "#f59e0b"),
            ("MyPy", quality_data.get("mypy_status", "unknown"), "#3b82f6"),
        ]

        for tool, status, color in quality_items:
            status_icon = (
                "✅" if status == "passed" else "❌" if status == "failed" else "⚠️"
            )
            html += f"""
            <div class="flex items-center justify-between p-3 border rounded">
                <div class="flex items-center gap-2">
                    <span style="color: {color}">■</span>
                    <span class="font-medium">{tool}</span>
                </div>
                <div class="flex items-center gap-2">
                    <span>{status_icon}</span>
                    <span class="text-sm">{status}</span>
                </div>
            </div>
            """

        return html

    def _serve_dashboard(self, html_content: str, port: int) -> str:
        """Serve dashboard on local server."""
        try:
            import http.server
            import socketserver
            import threading
            import webbrowser

            # Write to temporary file
            temp_file = self.output_dir / "temp_dashboard.html"
            temp_file.write_text(html_content, encoding="utf-8")

            # Start server
            os.chdir(self.output_dir)

            class DashboardHandler(http.server.SimpleHTTPRequestHandler):
                def do_GET(self):
                    if self.path == "/":
                        self.path = "/temp_dashboard.html"
                    return super().do_GET()

            with socketserver.TCPServer(("", port), DashboardHandler) as httpd:
                print(f"🚀 Dashboard serving at: http://localhost:{port}")

                # Open browser
                def open_browser():
                    import time

                    time.sleep(1)
                    webbrowser.open(f"http://localhost:{port}")

                threading.Thread(target=open_browser, daemon=True).start()

                # Serve until interrupted
                try:
                    httpd.serve_forever()
                except KeyboardInterrupt:
                    print("\n🛑 Dashboard server stopped")

            return f"http://localhost:{port}"

        except ImportError:
            print("❌ http.server not available, saving to file instead")
            return self.generate_dashboard()

    def export_data(self, format: str = "json") -> str:
        """Export dashboard data."""
        data = self._collect_dashboard_data()

        if format.lower() == "json":
            output_file = self.output_dir / "dashboard_data.json"
            output_file.write_text(json.dumps(data, indent=2, ensure_ascii=False))
            print(f"✅ Data exported to: {output_file}")
            return str(output_file)

        elif format.lower() == "csv":
            import csv

            # Export work items
            work_items = data.get("work_items", {}).get("recent", [])
            if work_items:
                output_file = self.output_dir / "work_items.csv"
                with open(output_file, "w", newline="", encoding="utf-8") as f:
                    if work_items:
                        writer = csv.DictWriter(f, fieldnames=work_items[0].keys())
                        writer.writeheader()
                        writer.writerows(work_items)
                print(f"✅ Work items exported to: {output_file}")
                return str(output_file)

        else:
            print(f"❌ Unsupported format: {format}")
            return ""


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Generate real-time dashboard")

    parser.add_argument("--port", type=int, help="Serve dashboard on port (e.g., 8080)")
    parser.add_argument("--output", help="Output HTML file path")
    parser.add_argument(
        "--auto-refresh", type=int, default=60, help="Auto-refresh interval in seconds"
    )
    parser.add_argument("--export", choices=["json", "csv"], help="Export data format")
    parser.add_argument(
        "--base-dir", type=Path, help="Base directory (default: current)"
    )

    args = parser.parse_args()

    dashboard = RealTimeDashboard(args.base_dir)

    if args.export:
        dashboard.export_data(args.export)
    else:
        dashboard.generate_dashboard(args.output, args.port, args.auto_refresh)


if __name__ == "__main__":
    main()
