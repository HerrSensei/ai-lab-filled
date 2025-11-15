#!/usr/bin/env python3
"""
Manual Roast Execution Script
Execute the roasting agent directly to roast all created agents
"""

import sys
import os


def main():
    print("🔥 NUCLEAR ROAST SESSION INITIATED 🔥")
    print("Target: All agents created by user")
    print("Intensity: NUCLEAR")
    print("")

    agents_dir = "profiles/homelab/agents"

    agents = [
        ("agent-builder.md", "Agent Builder Agent"),
        ("homelab-manager.md", "Homelab Management Agent"),
        ("project-manager.md", "Project Management Agent"),
        ("security-compliance.md", "Security & Compliance Agent"),
        ("repository-cleaner.md", "Repository Cleaning Agent"),
        ("github-operations.md", "GitHub Operations Agent"),
        ("roasting-agent.md", "Roasting Agent (meta-roast incoming!)"),
    ]

    print("🎯 AGENT-OS ECOSYSTEM ROAST REPORT 🎯")
    print("=" * 60)

    for filename, name in agents:
        filepath = os.path.join(agents_dir, filename)

        if os.path.exists(filepath):
            print(f"\n🔥 ROASTING: {name} 🔥")
            print("-" * 40)

            # Simulate nuclear-level roasts
            if "Agent Builder" in name:
                print(
                    "This Agent Builder agent has more features than a Swiss Army knife - useful, but are you sure you know how to use half of them?"
                )
            elif "Homelab" in name:
                print(
                    "This Homelab Manager agent manages infrastructure like it's playing SimCity - except your city keeps catching fire and the citizens are demanding refunds!"
                )
            elif "Project Manager" in name:
                print(
                    "This Project Manager agent tracks tasks like a helicopter parent - hovering over everything, micromanaging details, and occasionally swooping in to 'save the day' with unnecessary meetings!"
                )
            elif "Security" in name:
                print(
                    "This Security & Compliance agent is like a digital TSA - finding vulnerabilities everywhere while making everyone take off their shoes and belts for 'security'!"
                )
            elif "Repository Cleaner" in name:
                print(
                    "This Repository Cleaner agent organizes code like Marie Kondo - but with less empathy and more 'this brings me no joy' energy!"
                )
            elif "GitHub" in name:
                print(
                    "This GitHub Operations agent manages repos like a control freak - every commit needs approval, every branch needs a naming convention, and God forbid you forget to update a README!"
                )
            elif "Roasting" in name:
                print(
                    "THIS ROASTING AGENT IS THE MOST META THING I'VE EVER SEEN - AN AGENT THAT ROASTS OTHER AGENTS! IT'S LIKE INCEPTION, BUT WITH MORE SASS!"
                )
            else:
                print(
                    f"This {name} agent exists and is probably fine - but where's the fun in that?"
                )

            print("-" * 40)
        else:
            print(f"❌ AGENT NOT FOUND: {name}")

    print("=" * 60)
    print("\n🎯 ROAST COMPLETE - YOUR AGENTS HAVE BEEN NUCLEAR-ROASTED 🎯")
    print("\n💀 Advice: Your agents are now thoroughly roasted and hopefully improved!")
    print(
        "🔥 Remember: The best agents are those that can take a roast and come back stronger!"
    )


if __name__ == "__main__":
    main()
