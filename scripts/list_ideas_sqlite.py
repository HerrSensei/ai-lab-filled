#!/usr/bin/env python3
"""
AI Lab Framework - Updated List Ideas Utility (SQLite Version)
Lists and filters ideas from the SQLite database
"""

import argparse
import sys
import os
from typing import List, Dict, Any

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from ai_lab_framework.database import AILabDatabase


class SQLiteIdeasLister:
    """Lists and filters ideas from SQLite database"""

    def __init__(self):
        self.db = AILabDatabase()

    def filter_ideas(
        self,
        status: str = None,
        priority: str = None,
        category: str = None,
        tag: str = None,
    ) -> List[Dict[str, Any]]:
        """Filter ideas based on criteria"""
        ideas = self.db.get_ideas()

        if status:
            ideas = [i for i in ideas if i.get("status") == status]

        if priority:
            ideas = [i for i in ideas if i.get("priority") == priority]

        if category:
            ideas = [i for i in ideas if i.get("category") == category]

        if tag:
            ideas = [i for i in ideas if tag in i.get("tags", [])]

        return ideas

    def display_ideas(self, ideas: List[Dict], format_type: str = "table") -> None:
        """Display ideas in specified format"""
        if not ideas:
            print("No ideas found.")
            return

        if format_type == "table":
            print(
                f"{'ID':<8} {'Title':<30} {'Status':<12} {'Priority':<9} {'Category':<15}"
            )
            print("-" * 80)

            for idea in ideas:
                idea_id = idea.get("id", "N/A")[:8]
                title = idea.get("title", "N/A")[:28]
                status = idea.get("status", "N/A")[:10]
                priority = idea.get("priority", "N/A")[:7]
                category = idea.get("category", "N/A")[:13]

                print(
                    f"{idea_id:<8} {title:<30} {status:<12} {priority:<9} {category:<15}"
                )

        elif format_type == "detailed":
            for idea in ideas:
                print(f"\n💡 {idea.get('title', 'N/A')}")
                print(f"   ID: {idea.get('id', 'N/A')}")
                print(f"   Status: {idea.get('status', 'N/A')}")
                print(f"   Priority: {idea.get('priority', 'N/A')}")
                print(f"   Category: {idea.get('category', 'N/A')}")
                print(f"   Tags: {', '.join(idea.get('tags', []))}")
                print(f"   Created: {idea.get('created_date', 'N/A')}")
                if idea.get("description"):
                    print(f"   Description: {idea['description'][:100]}...")

        elif format_type == "json":
            import json

            print(json.dumps(ideas, indent=2, ensure_ascii=False))

    def get_statistics(self) -> Dict[str, Any]:
        """Get ideas statistics"""
        all_ideas = self.db.get_ideas()

        stats = {
            "total": len(all_ideas),
            "by_status": {},
            "by_priority": {},
            "by_category": {},
            "implemented": 0,
        }

        for idea in all_ideas:
            # Status breakdown
            status = idea.get("status", "unknown")
            stats["by_status"][status] = stats["by_status"].get(status, 0) + 1

            # Priority breakdown
            priority = idea.get("priority", "unknown")
            stats["by_priority"][priority] = stats["by_priority"].get(priority, 0) + 1

            # Category breakdown
            category = idea.get("category", "unknown")
            stats["by_category"][category] = stats["by_category"].get(category, 0) + 1

            # Count implemented
            if idea.get("status") == "implemented":
                stats["implemented"] += 1

        return stats


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="List and filter AI Lab Framework ideas (SQLite Edition)"
    )
    parser.add_argument(
        "--status",
        help="Filter by status (proposed, in_progress, implemented, archived)",
    )
    parser.add_argument("--priority", help="Filter by priority (high, medium, low)")
    parser.add_argument("--category", help="Filter by category")
    parser.add_argument("--tag", help="Filter by tag")
    parser.add_argument(
        "--format",
        choices=["table", "detailed", "json"],
        default="table",
        help="Output format (default: table)",
    )
    parser.add_argument("--count", action="store_true", help="Show only count")
    parser.add_argument("--stats", action="store_true", help="Show statistics")

    args = parser.parse_args()

    # Initialize lister
    lister = SQLiteIdeasLister()

    # Show statistics if requested
    if args.stats:
        stats = lister.get_statistics()
        print("📊 Ideas Statistics")
        print(f"Total ideas: {stats['total']}")
        print(f"Implemented: {stats['implemented']}")

        print("\nBy Status:")
        for status, count in stats["by_status"].items():
            print(f"  {status}: {count}")

        print("\nBy Priority:")
        for priority, count in stats["by_priority"].items():
            print(f"  {priority}: {count}")

        print("\nBy Category:")
        for category, count in stats["by_category"].items():
            print(f"  {category}: {count}")
        return

    # Filter ideas
    filtered_ideas = lister.filter_ideas(
        status=args.status, priority=args.priority, category=args.category, tag=args.tag
    )

    # Show count if requested
    if args.count:
        print(f"Total ideas: {len(filtered_ideas)}")
        return

    # Display ideas
    lister.display_ideas(filtered_ideas, args.format)


if __name__ == "__main__":
    main()
