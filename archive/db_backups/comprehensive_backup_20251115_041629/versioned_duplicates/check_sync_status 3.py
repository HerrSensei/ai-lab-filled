#!/usr/bin/env python3
"""
Check all items in database and their sync status
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from ai_lab_framework.database import AILabDatabase


def main():
    db = AILabDatabase()

    print("📋 All Work Items in Database:")
    work_items = db.get_work_items()
    for item in work_items:
        github_id = item.get("github_issue_id")
        sync_status = "✅ Synced" if github_id else "❌ Not Synced"
        print(f"  {item['id']}: {item['title'][:40]:<40} [{sync_status}]")

    print("\n💡 All Ideas in Database:")
    ideas = db.get_ideas()
    for item in ideas:
        github_id = item.get("github_issue_id")
        sync_status = "✅ Synced" if github_id else "❌ Not Synced"
        print(f"  {item['id']}: {item['title'][:40]:<40} [{sync_status}]")

    print("\n📊 Summary:")
    print(f"  Work Items: {len(work_items)} total")
    unsynced_work = [w for w in work_items if not w.get("github_issue_id")]
    print(f"  Work Items Not Synced: {len(unsynced_work)}")

    print(f"  Ideas: {len(ideas)} total")
    unsynced_ideas = [i for i in ideas if not i.get("github_issue_id")]
    print(f"  Ideas Not Synced: {len(unsynced_ideas)}")


if __name__ == "__main__":
    main()
