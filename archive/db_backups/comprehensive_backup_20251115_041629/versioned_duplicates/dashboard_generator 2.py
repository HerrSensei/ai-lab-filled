#!/usr/bin/env python3
"""
AI Lab Framework - Dashboard Generator

Generates comprehensive dashboard from JSON data sources.
Provides project monitoring, progress visualization, and framework health metrics.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any


class DashboardGenerator:
    """Generates dashboard from framework JSON data sources"""

    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.data_path = self.base_path / "data"
        self.output_path = self.base_path / "dashboard"

    def load_work_items(self) -> List[Dict[str, Any]]:
        """Load all work items from JSON files"""
        work_items = []
        work_items_path = self.data_path / "work-items"

        if work_items_path.exists():
            for file_path in work_items_path.glob("*.json"):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        work_items.append(json.load(f))
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")

        return work_items

    def load_ideas(self) -> List[Dict[str, Any]]:
        """Load all ideas from JSON files"""
        ideas = []
        ideas_path = self.data_path / "ideas"

        if ideas_path.exists():
            for file_path in ideas_path.glob("*.json"):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        ideas.append(json.load(f))
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")

        return ideas

    def calculate_metrics(
        self, work_items: List[Dict], ideas: List[Dict]
    ) -> Dict[str, Any]:
        """Calculate dashboard metrics from data"""
        # Work item metrics
        total_work_items = len(work_items)
        completed_items = len([w for w in work_items if w.get("status") == "done"])
        in_progress_items = len(
            [w for w in work_items if w.get("status") == "in_progress"]
        )

        completion_rate = (
            (completed_items / total_work_items * 100) if total_work_items > 0 else 0
        )

        # Idea metrics
        total_ideas = len(ideas)
        implemented_ideas = len([i for i in ideas if i.get("status") == "implemented"])

        # Priority breakdown
        high_priority = len([w for w in work_items if w.get("priority") == "high"])
        medium_priority = len([w for w in work_items if w.get("priority") == "medium"])
        low_priority = len([w for w in work_items if w.get("priority") == "low"])

        return {
            "work_items": {
                "total": total_work_items,
                "completed": completed_items,
                "in_progress": in_progress_items,
                "completion_rate": round(completion_rate, 1),
            },
            "ideas": {
                "total": total_ideas,
                "implemented": implemented_ideas,
                "implementation_rate": round(
                    (implemented_ideas / total_ideas * 100) if total_ideas > 0 else 0, 1
                ),
            },
            "priorities": {
                "high": high_priority,
                "medium": medium_priority,
                "low": low_priority,
            },
        }

    def generate_dashboard_html(self, metrics: Dict[str, Any]) -> str:
        """Generate HTML dashboard"""
        html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Lab Framework Dashboard</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .dashboard { max-width: 1200px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 30px; }
        .header h1 { color: #333; margin-bottom: 10px; }
        .header p { color: #666; font-size: 18px; }
        .metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .metric-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .metric-card h3 { margin: 0 0 15px 0; color: #333; }
        .metric-value { font-size: 2.5em; font-weight: bold; color: #2563eb; margin-bottom: 10px; }
        .metric-label { color: #666; font-size: 1.1em; }
        .progress-bar { width: 100%; height: 20px; background: #e9ecef; border-radius: 10px; overflow: hidden; margin-top: 15px; }
        .progress-fill { height: 100%; background: linear-gradient(90deg, #28a745, #20c997); transition: width 0.3s ease; }
        .priority-breakdown { display: flex; justify-content: space-between; margin-top: 15px; }
        .priority-item { text-align: center; }
        .priority-count { font-size: 1.5em; font-weight: bold; display: block; }
        .priority-label { color: #666; font-size: 0.9em; }
        .high { color: #dc3545; }
        .medium { color: #ffc107; }
        .low { color: #28a745; }
        .last-updated { text-align: center; color: #666; margin-top: 30px; }
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <h1>🚀 AI Lab Framework Dashboard</h1>
            <p>Real-time project monitoring and metrics</p>
        </div>
        
        <div class="metrics">
            <div class="metric-card">
                <h3>📋 Work Items</h3>
                <div class="metric-value">{work_items_total}</div>
                <div class="metric-label">Total work items</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {work_items_completion_rate}%"></div>
                </div>
                <div class="metric-label">{work_items_completed} of {work_items_total} completed ({work_items_completion_rate}%)</div>
            </div>
            
            <div class="metric-card">
                <h3>💡 Ideas</h3>
                <div class="metric-value">{ideas_total}</div>
                <div class="metric-label">Total ideas</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {ideas_implementation_rate}%"></div>
                </div>
                <div class="metric-label">{ideas_implemented} implemented ({ideas_implementation_rate}%)</div>
            </div>
            
            <div class="metric-card">
                <h3>🎯 Priorities</h3>
                <div class="priority-breakdown">
                    <div class="priority-item">
                        <span class="priority-count high">{high_priority}</span>
                        <span class="priority-label high">High</span>
                    </div>
                    <div class="priority-item">
                        <span class="priority-count medium">{medium_priority}</span>
                        <span class="priority-label medium">Medium</span>
                    </div>
                    <div class="priority-item">
                        <span class="priority-count low">{low_priority}</span>
                        <span class="priority-label low">Low</span>
                    </div>
                </div>
            </div>
            
            <div class="metric-card">
                <h3>📊 Active Work</h3>
                <div class="metric-value">{work_items_in_progress}</div>
                <div class="metric-label">Currently in progress</div>
            </div>
        </div>
        
        <div class="last-updated">
            Last updated: {timestamp}
        </div>
    </div>
</body>
</html>
        """

        # Use f-string formatting to avoid template conflicts
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Lab Framework Dashboard</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .dashboard {{ max-width: 1200px; margin: 0 auto; }}
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
        .last-updated {{ text-align: center; color: #666; margin-top: 30px; }}
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <h1>🚀 AI Lab Framework Dashboard</h1>
            <p>Real-time project monitoring and metrics</p>
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
                        <span class="priority-count high">{metrics["priorities"]["high"]}</span>
                        <span class="priority-label high">High</span>
                    </div>
                    <div class="priority-item">
                        <span class="priority-count medium">{metrics["priorities"]["medium"]}</span>
                        <span class="priority-label medium">Medium</span>
                    </div>
                    <div class="priority-item">
                        <span class="priority-count low">{metrics["priorities"]["low"]}</span>
                        <span class="priority-label low">Low</span>
                    </div>
                </div>
            </div>
            
            <div class="metric-card">
                <h3>📊 Active Work</h3>
                <div class="metric-value">{metrics["work_items"]["in_progress"]}</div>
                <div class="metric-label">Currently in progress</div>
            </div>
        </div>
        
        <div class="last-updated">
            Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        </div>
    </div>
</body>
</html>
        """

    def generate_dashboard_data(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Generate JSON data for dashboard"""
        return {
            "timestamp": datetime.now().isoformat(),
            "metrics": metrics,
            "framework_version": "2.0.0",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

    def generate_dashboard(self) -> None:
        """Generate complete dashboard"""
        print("🚀 Generating AI Lab Framework Dashboard...")

        # Ensure output directory exists
        self.output_path.mkdir(exist_ok=True)

        # Load data
        work_items = self.load_work_items()
        ideas = self.load_ideas()

        # Calculate metrics
        metrics = self.calculate_metrics(work_items, ideas)

        # Generate HTML dashboard
        html_content = self.generate_dashboard_html(metrics)
        with open(self.output_path / "DASHBOARD.md", "w", encoding="utf-8") as f:
            f.write("# AI Lab Framework Dashboard\n\n")
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
                f"- **Priorities:** {metrics['priorities']['high']} high, {metrics['priorities']['medium']} medium, {metrics['priorities']['low']} low\n"
            )

        with open(self.output_path / "dashboard.html", "w", encoding="utf-8") as f:
            f.write(html_content)

        # Generate JSON data
        dashboard_data = self.generate_dashboard_data(metrics)
        with open(self.output_path / "dashboard_data.json", "w", encoding="utf-8") as f:
            json.dump(dashboard_data, f, indent=2, ensure_ascii=False)

        print("✅ Dashboard generated successfully!")
        print(
            f"📊 Work Items: {metrics['work_items']['total']} total ({metrics['work_items']['completion_rate']}% complete)"
        )
        print(
            f"💡 Ideas: {metrics['ideas']['total']} total ({metrics['ideas']['implementation_rate']}% implemented)"
        )
        print(f"📁 Files created: DASHBOARD.md, dashboard.html, dashboard_data.json")


def main():
    """Main dashboard generation function"""
    import sys

    # Get base path from command line argument or use current directory
    base_path = sys.argv[1] if len(sys.argv) > 1 else "."

    generator = DashboardGenerator(base_path)
    generator.generate_dashboard()


if __name__ == "__main__":
    main()
