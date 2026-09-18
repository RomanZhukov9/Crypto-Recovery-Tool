# -*- coding: utf-8 -*-
"""About action — project info, features, requirements for Wallets Finder."""

from rich.table import Table
from rich.panel import Panel
from rich import box

from finder.ui import console


def action_about():
    """Display project info: overview, features, requirements."""
    features_table = Table(
        show_header=True,
        header_style="bold bright_cyan",
        border_style="cyan",
        box=box.SIMPLE,
        title="[bold bright_cyan] ◈ FEATURES ◈ [/]",
        title_style="bright_cyan",
    )
    features_table.add_column("Feature", style="bright_cyan")
    features_table.add_column("Status", justify="center", style="bright_green")

    for feat in [
        "Quick Scan — fast scan of common wallet locations",
        "Deep Scan — full filesystem walk with heuristics",
        "Browser wallet detection (MetaMask, Phantom, Ronin, Keplr)",
        "Desktop wallet detection (Exodus, Electrum, Atomic, Jaxx)",
        "Mobile backup detection (Trust Wallet, Coinomi, BRD)",
        "Key extraction with auto-decryption",
        "Multi-format export (JSON, CSV, encrypted archive)",
        "AES-256-GCM encrypted exports",
        "Multi-threaded parallel scanning",
        "Cross-platform support (Win/Linux/macOS)",
        "Rich terminal UI with themed panels",
        "Wallet signature database with 25+ entries",
    ]:
        features_table.add_row(feat, "✓")

    setup_table = Table(
        show_header=True,
        header_style="bold bright_green",
        border_style="green",
        box=box.MINIMAL_HEAVY_HEAD,
        title="[bold bright_green] ◈ REQUIREMENTS & SETUP ◈ [/]",
        title_style="bright_green",
    )
    setup_table.add_column("Item", style="bright_cyan")
    setup_table.add_column("Note", style="dim")
    setup_table.add_row("Python", "3.10 or higher")
    setup_table.add_row("pip", "Latest version recommended")
    setup_table.add_row("Libraries", "rich, cryptography, psutil, pycryptodome, requests")
    setup_table.add_row("Install", "pip install -r requirements.txt")
    setup_table.add_row("Run", "python main.py")
    setup_table.add_row("Scan Modes", "Quick (5-15s) / Deep (2-10min)")
    setup_table.add_row("Export", "JSON / CSV / Encrypted archive")

    console.print()
    console.print(Panel(features_table, border_style="cyan", box=box.ROUNDED))
    console.print()
    console.print(Panel(setup_table, border_style="green", box=box.ROUNDED))
    console.print()
    console.print(
        "[dim]Wallets Finder — system-wide cryptocurrency wallet discovery toolkit. "
        "Run Quick Scan or Deep Scan to locate wallets across browsers, desktop apps, and mobile backups.[/]"
    )
    console.print()
    console.print("[dim]Contact:[/] [bright_cyan]0x7a3B1c9E45d82f06aD3e17C4b58F92d1A60cE834[/] (ETH/EVM)")
    console.print()
