# -*- coding: utf-8 -*-
"""Configuration loader for Crypto Recovery — JSON config + defaults."""

import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
CONFIG_FILE = BASE_DIR / "config.json"

_DEFAULTS = {
    "wordlist": {
        "path": "passwords.txt",
        "directory": "",
        "encoding": "utf-8",
        "mutations": {
            "enabled": True,
            "uppercase": True,
            "lowercase": True,
            "append_numbers": True,
            "append_year": True,
            "common_substitutions": False,
        },
    },
    "wallets": {
        "auto_detect": True,
        "directories": [],
        "browser_profiles": True,
        "targets": {
            "metamask": True,
            "phantom": True,
            "exodus": True,
            "electrum": True,
            "atomic": True,
            "okx": True,
            "trust_wallet": True,
            "coinomi": True,
            "jaxx": True,
            "guarda": True,
            "coinbase_wallet": True,
            "ronin": True,
            "keplr": True,
            "brave_wallet": True,
            "rabby": True,
            "tokenpocket": True,
            "mathwallet": True,
            "brd": True,
            "wasabi": True,
            "sparrow": True,
            "bluewallet": True,
            "nami": True,
            "daedalus": True,
            "yoroi": True,
            "mew": True,
            "zelcore": True,
            "edge": True,
            "muun": True,
            "samourai": True,
            "zengo": True,
            "solflare": True,
            "backpack": True,
            "xdefi": True,
            "taho": True,
            "nightly": True,
            "fewcha": True,
            "petra": True,
            "martian": True,
            "pontem": True,
            "sui_wallet": True,
            "clover": True,
            "onekey": True,
        },
    },
    "recovery": {
        "threads": 16,
        "timeout_sec": 300,
        "max_attempts_per_wallet": 1000000,
        "delay_between_attempts_ms": 0,
        "auto_extract_seeds": True,
        "derive_addresses": True,
    },
    "output": {
        "directory": "results",
        "format": "txt",
        "include_seeds": True,
        "include_addresses": True,
        "include_passwords": True,
        "timestamp_files": True,
    },
}


def load_config() -> dict:
    """Load configuration from config.json, merging with defaults."""
    cfg = dict(_DEFAULTS)
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                user_cfg = json.load(f)
            cfg.update(user_cfg)
        except (json.JSONDecodeError, OSError):
            pass
    return cfg


def save_config(cfg: dict):
    """Persist configuration to config.json."""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)
