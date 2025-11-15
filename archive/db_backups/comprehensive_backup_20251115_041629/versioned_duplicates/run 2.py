import os
import subprocess

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt


def get_make_targets(makefile_path):
    """Parses a makefile to extract targets and their descriptions."""
    targets = {}
    with open(makefile_path) as f:
        for line in f:
            if line.startswith(".PHONY:"):
                targets.update(
                    {
                        target.strip(): ""
                        for target in line.split(":")[1].strip().split()
                    }
                )
    return targets


def main():
    """Main function to run the interactive CLI."""
    console = Console()
    console.print(
        Panel.fit("[bold cyan]AI Lab Framework - Interactive CLI[/bold cyan]")
    )

    makefiles_dir = "makefiles"
    all_targets = {}
    if os.path.exists(makefiles_dir):
        for filename in os.listdir(makefiles_dir):
            if filename.endswith(".mk"):
                category = filename.replace(".mk", "")
                targets = get_make_targets(os.path.join(makefiles_dir, filename))
                if targets:
                    all_targets[category] = list(targets.keys())

    if not all_targets:
        console.print("[bold red]No makefile targets found.[/bold red]")
        return

    while True:
        console.print("\n[bold green]Select a category:[/bold green]")
        categories = list(all_targets.keys())
        for i, category in enumerate(categories, 1):
            console.print(f"{i}. {category.capitalize()}")
        console.print(f"{len(categories) + 1}. Exit")

        try:
            category_choice = Prompt.ask(
                "\nEnter category number",
                choices=[str(i) for i in range(1, len(categories) + 2)],
                default=str(len(categories) + 1),
            )
            category_choice = int(category_choice)

            if category_choice == len(categories) + 1:
                break

            selected_category = categories[category_choice - 1]
            targets_in_category = all_targets[selected_category]

            console.print(
                f"\n[bold green]Select a target from '{selected_category.capitalize()}':[/bold green]"
            )
            for i, target in enumerate(targets_in_category, 1):
                console.print(f"{i}. {target}")
            console.print(f"{len(targets_in_category) + 1}. Back")

            target_choice = Prompt.ask(
                "\nEnter target number",
                choices=[str(i) for i in range(1, len(targets_in_category) + 2)],
                default=str(len(targets_in_category) + 1),
            )
            target_choice = int(target_choice)

            if target_choice == len(targets_in_category) + 1:
                continue

            selected_target = targets_in_category[target_choice - 1]

            console.print(
                f"\n[bold yellow]Executing 'make {selected_target}'...[/bold yellow]\n"
            )
            try:
                process = subprocess.run(
                    ["make", selected_target],
                    check=True,
                    text=True,
                    capture_output=True,
                )
                if process.stdout:
                    console.print(f"[bold green]Output:[/bold green]\n{process.stdout}")
                if process.stderr:
                    console.print(f"[bold red]Errors:[/bold red]\n{process.stderr}")
            except subprocess.CalledProcessError as e:
                console.print(
                    f"[bold red]Error executing 'make {selected_target}':[/bold red]"
                )
                if e.stdout:
                    console.print(f"[bold green]Output:[/bold green]\n{e.stdout}")
                if e.stderr:
                    console.print(f"[bold red]Errors:[/bold red]\n{e.stderr}")
            except FileNotFoundError:
                console.print(
                    "[bold red]'make' command not found. Is it installed and in your PATH?[/bold red]"
                )

        except (ValueError, IndexError):
            console.print("[bold red]Invalid choice. Please try again.[/bold red]")
        except KeyboardInterrupt:
            console.print("\n[bold yellow]Exiting.[/bold yellow]")
            break


if __name__ == "__main__":
    main()
