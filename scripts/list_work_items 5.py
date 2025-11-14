#!/usr/bin/env python3
"""
Quick script to list work items from database
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from ai_lab_framework.database import AILabDatabase


def main():
    db = AILabDatabase()
    work_items = db.get_work_items()

    print(f"{'ID':<10} {'Title':<30} {'Status':<12} {'Priority':<10}")
    print("-" * 70)

    for item in work_items:
        print(
            f"{item['id']:<10} {item['title'][:28]:<30} {item['status']:<12} {item['priority']:<10}"
        )


if __name__ == "__main__":
    main()
