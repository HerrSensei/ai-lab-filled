#!/usr/bin/env python3
"""
Create proper session log with structured format
"""

import os
import json
from datetime import datetime
from pathlib import Path


def create_session_log(session_data):
    """Create structured session log"""

    # Create logs directory if not exists
    logs_dir = Path("ai-logs/logs")
    logs_dir.mkdir(exist_ok=True)

    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"session_{timestamp}.log"
    filepath = logs_dir / filename

    # Create log content
    log_content = f"""AI Lab Framework Session Log
=====================================
Session ID: {session_data.get("session_id", timestamp)}
Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Type: {session_data.get("type", "Development")}
Status: {session_data.get("status", "COMPLETED")}
Duration: {session_data.get("duration", "Unknown")}

SESSION OBJECTIVES
==================
{chr(10).join(f"{i + 1}. {'✅' if obj.get('completed') else '⏳'} {obj.get('description', 'N/A')}" for i, obj in enumerate(session_data.get("objectives", [])))}

TECHNICAL WORK PERFORMED
=========================
{session_data.get("technical_work", "No technical work recorded")}

RESULTS ACHIEVED
================
{chr(10).join(f"- {result}" for result in session_data.get("results", []))}

FILES CREATED/MODIFIED
======================
{chr(10).join(f"- {file}" for file in session_data.get("files", []))}

DATABASE CHANGES
================
Work Items: {session_data.get("db_changes", {}).get("work_items", "N/A")}
Ideas: {session_data.get("db_changes", {}).get("ideas", "N/A")}
Sync Status: {session_data.get("db_changes", {}).get("sync_status", "N/A")}

NEXT STEPS
===========
{chr(10).join(f"1. {step}" for step in session_data.get("next_steps", []))}

BLOCKERS & ISSUES
=================
{chr(10).join(f"- {issue}" for issue in session_data.get("blockers", []))}

METRICS
========
Total Tasks: {session_data.get("metrics", {}).get("total_tasks", 0)}
Completed: {session_data.get("metrics", {}).get("completed", 0)}
Success Rate: {session_data.get("metrics", {}).get("success_rate", 0)}%

SESSION END
===========
End Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Next Session: {session_data.get("next_session", "TBD")}

=====================================
Log Format: AI Lab Framework v1.0
=====================================
"""

    # Write log file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(log_content)

    # Also create JSON for machine reading
    json_data = {
        "session_id": session_data.get("session_id", timestamp),
        "timestamp": datetime.now().isoformat(),
        "type": session_data.get("type", "Development"),
        "status": session_data.get("status", "COMPLETED"),
        "duration": session_data.get("duration", "Unknown"),
        "objectives": session_data.get("objectives", []),
        "results": session_data.get("results", []),
        "files": session_data.get("files", []),
        "db_changes": session_data.get("db_changes", {}),
        "next_steps": session_data.get("next_steps", []),
        "blockers": session_data.get("blockers", []),
        "metrics": session_data.get("metrics", {}),
        "next_session": session_data.get("next_session", "TBD"),
    }

    json_filepath = logs_dir / f"session_{timestamp}.json"
    with open(json_filepath, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)

    return filepath, json_filepath


if __name__ == "__main__":
    # Example usage for today's session
    session_data = {
        "session_id": "2025-11-14_001",
        "type": "GitHub Sync & Project Management",
        "status": "COMPLETED",
        "duration": "~2 hours",
        "objectives": [
            {"description": "Fix GitHub sync issues", "completed": True},
            {"description": "Restore work items to GitHub", "completed": True},
            {"description": "Set up project management foundation", "completed": True},
            {"description": "Document all changes", "completed": True},
        ],
        "technical_work": """1. Database Schema Repair
   - Added missing columns: component, created_at, updated_at
   - Fixed SQLite constraints

2. GitHub Integration Fix
   - Updated src/ai_lab_framework/github_integration.py
   - Switched from SQLAlchemy to SQLite database class
   - Fixed sync methods

3. Work Items Recreation
   - Cleared incorrect GitHub issue IDs
   - Recreated 13 work items as GitHub Issues #21-33
   - Verified all 19 items (13 work + 6 ideas) are synced""",
        "results": [
            "GitHub sync 100% operational (19/19 items)",
            "Database schema stable and consistent",
            "All work items properly organized on GitHub",
            "Complete documentation created",
            "Project management foundation established",
        ],
        "files": [
            "scripts/check_sync_status.py",
            "scripts/check_github_issues.py",
            "scripts/fixed_github_sync.py",
            "scripts/recreate_work_items.py",
            "scripts/plan_github_projects.py",
            "GITHUB_PROJECTS_COMPLETE.md",
            "FRAMEWORK_ITEMS_PRIORITY.md",
            "src/ai_lab_framework/github_integration.py (modified)",
            "data/ai_lab.db (schema updated)",
        ],
        "db_changes": {
            "work_items": "14 total (13 synced + 1 test)",
            "ideas": "6 total (all synced)",
            "sync_status": "100% complete",
        },
        "next_steps": [
            "Create GitHub Projects board at https://github.com/HerrSensei/ai-lab/projects",
            "Add all 19 issues to project board",
            "Organize by status (Done/In Progress/Todo/Backlog)",
            "Start working on high-priority framework items (FRM-007, FRM-010, FRM-011)",
        ],
        "blockers": [
            "GitHub Projects API not fully supported via PyGithub",
            "Manual setup required for project board creation",
        ],
        "metrics": {"total_tasks": 4, "completed": 4, "success_rate": 100},
        "next_session": "GitHub Projects board setup and Dashboard project completion",
    }

    log_file, json_file = create_session_log(session_data)
    print(f"✅ Session log created:")
    print(f"   📄 Text: {log_file}")
    print(f"   📊 JSON: {json_file}")
