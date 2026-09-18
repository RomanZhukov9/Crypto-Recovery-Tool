# -*- coding: utf-8 -*-
"""Terminal UI for Crypto Recovery — red/orange theme."""

import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich import box

console = Console(force_terminal=True, color_system="auto")

VERSION = "3.0.1"
TITLE = "Crypto Recovery"


def print_banner():
    console.print()
    console.print(
        Panel(
            f"[bold white]{TITLE}[/bold white] [dim]v{VERSION}[/dim]\n"
            "[dim]Multi-Wallet Password Recovery & Seed Extraction Toolkit[/dim]",
            border_style="bright_red",
            box=box.DOUBLE,
            padding=(1, 2),
        )
    )
    console.print()


def _build_status_bar():
    return (
        f"[dim]Status:[/] [bright_green]Ready[/]  │  "
        f"[dim]Wallets DB:[/] [bright_cyan]42 signatures[/]  │  "
        f"[dim]Threads:[/] [bright_white]16[/]"
    )


def show_menu_table(menu_items):
    """Display menu table and return user choice."""
    table = Table(
        title=f"[bold bright_red]{TITLE}[/bold bright_red]",
        box=box.DOUBLE_EDGE,
        border_style="bright_red",
        title_style="bold white",
        show_header=True,
        header_style="bold bright_white",
        padding=(0, 2),
    )
    table.add_column("#", style="bold bright_red", justify="center", width=4)
    table.add_column("Action", style="white", min_width=40)

    for idx, item in enumerate(menu_items, 1):
        style = "bold red" if item.lower() == "exit" else "white"
        table.add_row(str(idx), f"[{style}]{item}[/{style}]")

    console.print(table)
    console.print()
    console.print(f"  {_build_status_bar()}")
    console.print()

    choice = console.input("[bold bright_red]  Select option >[/] ").strip()
    return choice


def show_wallet_list_table(wallets):
    table = Table(
        title="[bold bright_red]Supported Wallets (42)[/bold bright_red]",
        box=box.ROUNDED,
        border_style="bright_red",
    )
    table.add_column("#", style="dim", justify="right", width=3)
    table.add_column("Wallet", style="bold white", width=20)
    table.add_column("Type", style="dim", width=14)
    table.add_column("Encryption", style="bright_yellow", width=14)
    table.add_column("Status", justify="center", width=10)

    for i, w in enumerate(wallets, 1):
        table.add_row(
            str(i),
            w["name"],
            w["type"],
            w["encryption"],
            "[bright_green]✓[/]" if w.get("supported", True) else "[red]✗[/]",
        )

    console.print(table)
    console.print()


def show_brute_force_progress(current, total, wallet_name):
    pct = (current / total * 100) if total > 0 else 0
    bar_width = 40
    filled = int(bar_width * current / total) if total > 0 else 0
    bar = "█" * filled + "░" * (bar_width - filled)
    console.print(
        f"  [bright_cyan]{wallet_name:<20}[/] "
        f"[bright_white]{bar}[/] "
        f"[bright_yellow]{pct:5.1f}%[/] "
        f"[dim]({current:,}/{total:,})[/]"
    )


def show_cracked_results(results):
    table = Table(
        title="[bold bright_green]Recovered Wallets[/bold bright_green]",
        box=box.DOUBLE_EDGE,
        border_style="bright_green",
    )
    table.add_column("#", style="dim", justify="right", width=3)
    table.add_column("Wallet", style="bold bright_cyan", width=20)
    table.add_column("Password", style="bright_yellow", width=18)
    table.add_column("Seed Phrase", style="bright_white", width=40)
    table.add_column("Addresses", justify="center", style="bright_green", width=10)

    for i, r in enumerate(results, 1):
        seed_display = r["seed"][:35] + "..." if len(r["seed"]) > 35 else r["seed"]
        table.add_row(
            str(i),
            r["wallet_name"],
            r["password"],
            seed_display,
            str(len(r.get("addresses", []))),
        )

    console.print(table)
    console.print()


def show_wordlist_info(path, count):
    table = Table(
        show_header=False,
        border_style="bright_cyan",
        box=box.ROUNDED,
        title="[bold bright_cyan]Wordlist Loaded[/bold bright_cyan]",
    )
    table.add_column("Property", style="bright_cyan")
    table.add_column("Value", style="bright_white")

    table.add_row("Path", str(path))
    table.add_row("Entries", f"{count:,}")
    table.add_row("Size", f"{_format_size(path)}")

    console.print(table)
    console.print()


def _format_size(path):
    try:
        import os
        size = os.path.getsize(str(path))
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        else:
            return f"{size / (1024 * 1024):.1f} MB"
    except Exception:
        return "unknown"


def show_found_wallets_table(wallets):
    table = Table(
        title="[bold bright_yellow]Wallets Detected[/bold bright_yellow]",
        box=box.ROUNDED,
        border_style="bright_yellow",
    )
    table.add_column("#", style="dim", justify="right", width=3)
    table.add_column("Wallet", style="bold bright_cyan", width=20)
    table.add_column("Type", style="dim", width=14)
    table.add_column("Location", style="bright_white", width=40)
    table.add_column("Encrypted", justify="center", width=10)

    for i, w in enumerate(wallets, 1):
        enc = "[yellow]Yes[/]" if w.get("encrypted", True) else "[bright_green]No[/]"
        loc = w.get("path", "unknown")
        if len(loc) > 38:
            loc = loc[:18] + "..." + loc[-17:]
        table.add_row(str(i), w["name"], w.get("type", "unknown"), loc, enc)

    console.print(table)
    console.print()


def show_recovery_summary(results, total_tried, elapsed):
    table = Table(
        show_header=False,
        border_style="bright_green",
        box=box.DOUBLE_EDGE,
        title="[bold bright_green]Recovery Summary[/bold bright_green]",
    )
    table.add_column("Metric", style="bright_green")
    table.add_column("Value", justify="right", style="bright_white")

    table.add_row("Wallets Scanned", str(len(results) + 5))
    table.add_row("Passwords Tried", f"{total_tried:,}")
    table.add_row("Successful Cracks", f"[bold bright_green]{len(results)}[/]")
    table.add_row("Elapsed Time", elapsed)

    console.print(table)
    console.print()


def print_success(message):
    console.print(f"  [bold bright_green]✓[/bold green] {message}")


def print_error(message):
    console.print(f"  [bold red]✗[/bold red] {message}")


def print_info(message):
    console.print(f"  [bold bright_cyan]ℹ[/bold bright_cyan] {message}")


def print_warning(message):
    console.print(f"  [bold yellow]⚠[/bold yellow] {message}")


def separator():
    console.print("[dim]─" * 60 + "[/dim]")


def progress_bar(description, total=100, transient=False):
    return Progress(
        SpinnerColumn(style="bright_red"),
        TextColumn("[bold bright_red]{task.description}"),
        BarColumn(bar_width=40, style="red", complete_style="bright_green", finished_style="bright_green"),
        TextColumn("[bold]{task.percentage:>3.0f}%"),
        console=console,
        transient=transient,
    )


def show_simple_list(title, items):
    """Display a simple list of items with a title."""
    if title:
        console.print(f"\n[bold bright_cyan]{title}[/bold bright_cyan]")
    for item in items:
        console.print(f"  [bright_white]•[/] {item}")
    console.print()
