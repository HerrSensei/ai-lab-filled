#!/usr/bin/env python3
"""
Check unsynced items in database
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from ai_lab_framework.database import AILabDatabase


def main():
    db = AILabDatabase()

    print("📋 Unsynced Work Items:")
    work_items = db.get_unsynced_items("work_item")
    if work_items:
        for item in work_items:
            print(f"  - {item['id']}: {item['title']}")
    else:
        print("  ✅ All work items synced")

    print("\n💡 Unsynced Ideas:")
    ideas = db.get_unsynced_items("idea")
    if ideas:
        for item in ideas:
            print(f"  - {item['id']}: {item['title']}")
    else:
        print("  ✅ All ideas synced")


if __name__ == "__main__":
    main()
