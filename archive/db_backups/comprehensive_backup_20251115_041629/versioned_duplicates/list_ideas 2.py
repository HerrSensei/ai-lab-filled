#!/usr/bin/env python3
"""
AI Lab Framework - List Ideas Utility
Lists and filters ideas from the JSON ideas database
"""

import json
import argparse
from pathlib import Path
from typing import List, Dict, Any


def load_ideas(ideas_path: Path) -> List[Dict[str, Any]]:
    """Load all ideas from JSON files"""
    ideas = []

    if ideas_path.exists():
        for file_path in ideas_path.glob("*.json"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    ideas.append(json.load(f))
            except Exception as e:
                print(f"Error loading {file_path}: {e}")

    return ideas


def filter_ideas(
    ideas: List[Dict],
    status: str = None,
    priority: str = None,
    category: str = None,
    tag: str = None,
) -> List[Dict]:
    """Filter ideas based on criteria"""
    filtered = ideas

    if status:
        filtered = [i for i in filtered if i.get("status") == status]

    if priority:
        filtered = [i for i in filtered if i.get("priority") == priority]

    if category:
        filtered = [i for i in filtered if i.get("category") == category]

    if tag:
        filtered = [i for i in filtered if tag in i.get("tags", [])]

    return filtered


def display_ideas(ideas: List[Dict], format_type: str = "table") -> None:
    """Display ideas in specified format"""
    if not ideas:
        print("No ideas found.")
        return

    if format_type == "table":
        print(
            f"{'ID':<6} {'Title':<30} {'Status':<12} {'Priority':<9} {'Category':<15}"
        )
        print("-" * 75)

        for idea in ideas:
            idea_id = idea.get("id", "N/A")[:6]
            title = idea.get("title", "N/A")[:28]
            status = idea.get("status", "N/A")[:10]
            priority = idea.get("priority", "N/A")[:7]
            category = idea.get("category", "N/A")[:13]

            print(f"{idea_id:<6} {title:<30} {status:<12} {priority:<9} {category:<15}")

    elif format_type == "detailed":
        for idea in ideas:
            print(f"\n📋 {idea.get('title', 'N/A')}")
            print(f"   ID: {idea.get('id', 'N/A')}")
            print(f"   Status: {idea.get('status', 'N/A')}")
            print(f"   Priority: {idea.get('priority', 'N/A')}")
            print(f"   Category: {idea.get('category', 'N/A')}")
            print(f"   Tags: {', '.join(idea.get('tags', []))}")
            print(f"   Created: {idea.get('created_date', 'N/A')}")
            if idea.get("description"):
                print(f"   Description: {idea['description'][:100]}...")

    elif format_type == "json":
        print(json.dumps(ideas, indent=2, ensure_ascii=False))


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="List and filter AI Lab Framework ideas"
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

    args = parser.parse_args()

    # Load ideas
    base_path = Path(".")
    ideas_path = base_path / "data" / "ideas"
    ideas = load_ideas(ideas_path)

    # Filter ideas
    filtered_ideas = filter_ideas(
        ideas,
        status=args.status,
        priority=args.priority,
        category=args.category,
        tag=args.tag,
    )

    # Show count if requested
    if args.count:
        print(f"Total ideas: {len(filtered_ideas)}")
        return

    # Display ideas
    display_ideas(filtered_ideas, args.format)


if __name__ == "__main__":
    main()
