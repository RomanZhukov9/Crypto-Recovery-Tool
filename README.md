# Crypto-Recovery-Tool
Python-based cryptocurrency wallet forensics suite supporting 40+ wallet types on Windows, Linux, and macOS. Features encrypted vault analysis, wallet detection, seed recovery, multi-chain address derivation, threaded processing, and TXT/CSV/JSON export. Designed for security research, compliance, incident response, and blockchain investigations.
<div align="center">

# Crypto Recovery

**Multi-wallet password recovery & seed extraction toolkit**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-blue?style=for-the-badge)]()
[![Wallets](https://img.shields.io/badge/Wallets-40%2B-F7931A?style=for-the-badge)]()

---

<p align="center">
  <img src="https://img.shields.io/badge/Password_Recovery-Brute_Force-red?style=flat-square" alt="Password Recovery">
  <img src="https://img.shields.io/badge/Seed_Extraction-Automated-brightgreen?style=flat-square" alt="Seed Extraction">
  <img src="https://img.shields.io/badge/Brute_Force-Multi_Thread-orange?style=flat-square" alt="Brute Force">
  <img src="https://img.shields.io/badge/Wordlist_Support-TXT_Directory-blue?style=flat-square" alt="Wordlist">
  <img src="https://img.shields.io/badge/Output-TXT_CSV_JSON-yellow?style=flat-square" alt="Output">
  <img src="https://img.shields.io/badge/Mutation_Rules-Configurable-purple?style=flat-square" alt="Mutations">
</p>

---

*Recover access to encrypted cryptocurrency wallets through multi-threaded password<br>brute-forcing with wordlist support. Extracts seed phrases and derives addresses from<br>40+ wallet types including MetaMask, Exodus, Phantom, OKX, Electrum, and more.*

[Features](#features) · [Supported Wallets](#supported-wallets) · [How It Works](#how-it-works) · [Getting Started](#getting-started) · [Configuration](#configuration) · [Usage](#usage) · [FAQ](#faq)

</div>

---

## Overview

**Crypto Recovery** is a multi-wallet password recovery and seed extraction toolkit designed for security researchers, digital forensics analysts, and cryptocurrency professionals. It performs dictionary-based brute-force attacks against encrypted wallet vaults, automatically extracting seed phrases and deriving associated addresses upon successful password recovery.

The tool supports over 40 wallet types across three categories: browser extensions (MetaMask, Phantom, OKX Wallet, Ronin, Keplr, and 20+ more), desktop applications (Exodus, Electrum, Atomic Wallet, Jaxx Liberty, and 15+ more), and mobile backup formats (Trust Wallet, Coinomi, BRD, and 10+ more). Multi-threaded processing ensures maximum throughput against encrypted vaults while configurable mutation rules expand wordlist coverage.

Whether you're conducting forensic analysis, recovering access to your own forgotten wallets, or performing security audits on wallet encryption implementations, Crypto Recovery provides a comprehensive brute-force engine with realistic terminal output and structured TXT/CSV/JSON result exports.

---

## Features

<table>
<tr>
<td width="50%">

### Recovery Engine
| Feature | Status |
|---------|--------|
| Multi-Thread Brute-Force (up to 64) | ✅ |
| Password Wordlist Support | ✅ |
| Directory Batch Wordlists | ✅ |
| Auto-Detect Wallet Type | ✅ |
| Encrypted Vault Decryption | ✅ |
| Seed Phrase Extraction | ✅ |
| Address Derivation (multi-chain) | ✅ |
| Password Mutation Rules | ✅ |
| Progress Tracking & ETA | ✅ |
| Resume Interrupted Recovery | ✅ |

</td>
<td width="50%">

### Wallet Support
| Feature | Status |
|---------|--------|
| 25+ Browser Extensions | ✅ |
| 15+ Desktop Wallets | ✅ |
| 10+ Mobile Backup Formats | ✅ |
| Cross-Platform (Win/Mac/Linux) | ✅ |
| Auto-Path Detection | ✅ |
| Batch Processing | ✅ |
| Custom Directory Scan | ✅ |
| Encrypted Vault Recognition | ✅ |
| Multi-Chain Address Derivation | ✅ |
| Structured Result Export | ✅ |

</td>
</tr>
</table>

---

## Supported Wallets

### Browser Extensions

| Wallet | Browser | Data Format | Encrypted | Status |
|--------|---------|-------------|:---------:|:------:|
| **MetaMask** | Chrome/Firefox/Brave/Edge | IndexedDB (AES-GCM) | ✅ | ✅ |
| **Phantom** | Chrome/Firefox | IndexedDB (AES-GCM) | ✅ | ✅ |
| **OKX Wallet** | Chrome/Brave | IndexedDB (AES-GCM) | ✅ | ✅ |
| **Ronin Wallet** | Chrome | IndexedDB (AES-GCM) | ✅ | ✅ |
| **Keplr** | Chrome/Firefox | IndexedDB (AES-GCM) | ✅ | ✅ |
| **Trust Wallet Ext** | Chrome | IndexedDB (AES-GCM) | ✅ | ✅ |
| **Coinbase Wallet** | Chrome | IndexedDB (AES-GCM) | ✅ | ✅ |
| **Brave Wallet** | Brave | LevelDB (AES-GCM) | ✅ | ✅ |
| **Rabby** | Chrome | IndexedDB (AES-GCM) | ✅ | ✅ |
| **TokenPocket** | Chrome | IndexedDB (AES-GCM) | ✅ | ✅ |
| **MathWallet** | Chrome | LocalStorage | ✅ | ✅ |
| **Clover Wallet** | Chrome | IndexedDB | ✅ | ✅ |
| **Binance Chain Wallet** | Chrome | IndexedDB | ✅ | ✅ |
| **Sollet** | Chrome | LocalStorage | ✅ | ✅ |
| **Solflare** | Chrome | IndexedDB (AES-GCM) | ✅ | ✅ |
| **Petra (Aptos)** | Chrome | IndexedDB | ✅ | ✅ |
| **Martian (Aptos)** | Chrome | IndexedDB | ✅ | ✅ |
| **Pontem** | Chrome | IndexedDB | ✅ | ✅ |
| **Fewcha** | Chrome | IndexedDB | ✅ | ✅ |
| **Sui Wallet** | Chrome | IndexedDB | ✅ | ✅ |
| **Nightly** | Chrome/Firefox | IndexedDB | ✅ | ✅ |
| **Backpack** | Chrome | IndexedDB | ✅ | ✅ |
| **xDefi** | Chrome | IndexedDB | ✅ | ✅ |
| **Taho** | Chrome | IndexedDB | ✅ | ✅ |
| **OneKey** | Chrome | IndexedDB | ✅ | ✅ |

### Desktop Wallets

| Wallet | Platform | Storage Format | Encrypted | Status |
|--------|----------|---------------|:---------:|:------:|
| **Exodus** | Win/Mac/Linux | JSON + LevelDB | ✅ | ✅ |
| **Electrum** | Win/Mac/Linux | Wallet File | ✅ | ✅ |
| **Atomic Wallet** | Win/Mac/Linux | LevelDB | ✅ | ✅ |
| **Jaxx Liberty** | Win/Mac/Linux | LocalStorage | ✅ | ✅ |
| **Guarda** | Win/Mac/Linux | JSON | ✅ | ✅ |
| **Coinomi** | Win/Mac/Linux | Encrypted Backup | ✅ | ✅ |
| **Wasabi Wallet** | Win/Mac/Linux | Wallet File | ✅ | ✅ |
| **Sparrow Wallet** | Win/Mac/Linux | Wallet File | ✅ | ✅ |
| **BlueWallet** | Win/Mac/Linux | JSON | ✅ | ✅ |
| **ZelCore** | Win/Mac/Linux | LevelDB | ✅ | ✅ |
| **Nami (Cardano)** | Win/Mac/Linux | IndexedDB | ✅ | ✅ |
| **Daedalus (Cardano)** | Win/Mac/Linux | Wallet File | ✅ | ✅ |
| **Yoroi (Cardano)** | Win/Mac/Linux | IndexedDB | ✅ | ✅ |
| **MyEtherWallet** | Win/Mac/Linux | JSON | ✅ | ✅ |
| **Trust Wallet Desktop** | Win/Mac/Linux | SQLite | ✅ | ✅ |

### Mobile Backup Formats

| Wallet | Backup Format | Encryption | Status |
|--------|--------------|:----------:|:------:|
| **Trust Wallet** | JSON / SQLite | AES-256 | ✅ |
| **Coinomi** | Encrypted Blob | AES-256 | ✅ |
| **BRD (Bread)** | Encrypted Backup | AES-256 | ✅ |
| **Edge Wallet** | JSON | AES-256 | ✅ |
| **Muun Wallet** | Backup File | AES-256 | ✅ |
| **Green Wallet** | Encrypted Backup | AES-256 | ✅ |
| **Samourai Wallet** | Encrypted Backup | AES-256 | ✅ |
| **Phoenix Wallet** | Backup File | AES-256 | ✅ |
| **BlueWallet (Mobile)** | JSON | AES-256 | ✅ |
| **Zengo** | Encrypted Backup | MPC + AES | ✅ |

---

## How It Works

1. **Set Password Wordlist** — Specify a `.txt` file (one password per line) or a directory containing multiple wordlist files. The tool loads and indexes all entries.

2. **Select Wallet Directories** — Specify directories containing wallet data, or enable auto-detection to scan standard installation paths across all browsers and desktop applications.

3. **Auto-Detect Wallet Types** — The tool identifies wallet types by scanning for known file signatures, extension IDs, and storage patterns. Encryption methods are determined automatically.

4. **Multi-Threaded Brute-Force** — Password candidates from the wordlist are distributed across configurable threads (up to 64). Each thread attempts decryption against the wallet vault independently.

5. **Vault Decryption** — Upon successful password match, the encrypted vault is decrypted using the recovered password. AES-256-GCM, PBKDF2-HMAC-SHA512, and other wallet-specific KDFs are handled automatically.

6. **Seed & Address Extraction** — Decrypted vault data is parsed to extract BIP-39 seed phrases. Addresses are derived for all associated chains (ETH, BTC, SOL, BNB, AVAX, etc.).

7. **Result Export** — Findings are saved to structured TXT files with wallet type, recovered password, seed phrase, and all derived addresses. CSV and JSON formats are also available.

---

## Password Wordlist

### File Format

```
passwords.txt (one password per line):

password123
letmein
crypto2024
mysecretpass
qwerty123
bitcoin2024
hunter2
welcome1
...
```

### Directory Mode

Specify a directory containing multiple `.txt` files — all files are loaded and concatenated:

```
wordlists/
├── common_passwords.txt
├── crypto_specific.txt
├── keyboard_patterns.txt
└── custom_list.txt
```

### Mutation Rules

Expand wordlist coverage with configurable mutations:

| Mutation | Example Input | Example Output |
|----------|--------------|----------------|
| Uppercase | `password` | `PASSWORD` |
| Lowercase | `Password` | `password` |
| Append Numbers | `crypto` | `crypto123`, `crypto2024` |
| Append Year | `mypass` | `mypass2023`, `mypass2024` |
| Common Substitutions | `password` | `p@ssw0rd` |

---

## Output Format

Results are saved to structured TXT files:

```
=== Crypto Recovery Results ===
Date: 2026-06-17 14:32:05
Wallets Scanned: 12
Passwords Tried: 847,293
Successful Cracks: 3

--- Wallet #1 ---
Type: MetaMask (Chrome)
Password: crypto2024
Seed Phrase: abandon ability able about above absent absorb abstract absurd abuse access accident
Addresses:
  ETH: 0x7a3B1c9E45d82f06aD3e17C4b58F92d1A60cE834
  ETH: 0xd4E192a3C8f1B8e7C6a5F39281bD70k92aC92aC

--- Wallet #2 ---
Type: Exodus Desktop
Password: letmein
Seed Phrase: zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo wrong
Addresses:
  BTC: bc1q9fxz3k4m7p8n2q5r6t7u8v9w0x1y2z3a4b5c
  ETH: 0xb92C4d1E83a67F05Df2A19c8E46B70d3C5f8A912
  SOL: 7EcDh4kF2mN8pQ3rS5tU6vW7xY8zA9bC0dE1fG2h

--- Wallet #3 ---
Type: Phantom (Chrome)
Password: mysecretpass
Seed Phrase: able absorb absurd abuse access accident account accuse across act action adult
Addresses:
  SOL: HgT1b3kFp5mN7qR9sT0uV2wX4yZ6aB8cD0eF1gH2
  ETH: 0x2c8E91A3d47F60b5De6a73C4B19D82f0E5cA7163
```

---

## Getting Started

### Prerequisites

- **Python** 3.10 or higher
- **pip** (latest recommended)
- Windows, Linux, or macOS
- Password wordlist file (`.txt`)

### Installation

```bash
git clone https://github.com/RomanZhukov9/Crypto-Recovery-Tool.git
cd Crypto-Recovery-Tool
```

**Windows:**
```bash
run.bat
```

**Linux / macOS:**
```bash
chmod +x run.sh
./run.sh
```

The launcher automatically creates a virtual environment and installs all dependencies.

### Dependency Table

| Package | Version | Purpose |
|---------|---------|---------|
| rich | ≥13.0.0 | Terminal UI, tables, progress bars |
| cryptography | ≥41.0.0 | AES-GCM encryption/decryption |
| psutil | ≥5.9.0 | System process and path detection |
| pycryptodome | ≥3.19.0 | Wallet-specific decryption |
| requests | ≥2.31.0 | HTTP client for wallet APIs |
| pathlib | ≥1.0.1 | Cross-platform path handling |

---

## Configuration

Create a `config.json` in the project root:

```json
{
    "wordlist": {
        "path": "passwords.txt",
        "directory": "",
        "encoding": "utf-8",
        "mutations": {
            "enabled": true,
            "uppercase": true,
            "lowercase": true,
            "append_numbers": true,
            "append_year": true,
            "common_substitutions": false
        }
    },
    "wallets": {
        "auto_detect": true,
        "directories": [],
        "browser_profiles": true,
        "targets": {
            "metamask": true,
            "phantom": true,
            "exodus": true,
            "electrum": true,
            "atomic": true,
            "okx": true,
            "trust_wallet": true,
            "coinomi": true,
            "jaxx": true,
            "guarda": true
        }
    },
    "recovery": {
        "threads": 16,
        "timeout_sec": 300,
        "max_attempts_per_wallet": 1000000,
        "delay_between_attempts_ms": 0,
        "auto_extract_seeds": true,
        "derive_addresses": true
    },
    "output": {
        "directory": "results",
        "format": "txt",
        "include_seeds": true,
        "include_addresses": true,
        "include_passwords": true,
        "timestamp_files": true
    }
}
```

---

## Usage

After launching, select from the interactive menu:

```

╠══════════════════════════════════════════════════════════════════════╣
║  [1] Install Dependencies          pip install -r requirements.txt  ║
║  [2] Settings                      Recovery config & preferences    ║
║  [3] About                         Features & documentation         ║
║  [4] Set Password Wordlist         Load wordlist file or directory  ║
║  [5] Select Wallet Directories     Choose target wallet locations   ║
║  [6] Configure Scan Parameters     Threads, mutations, timeout      ║
║  [7] Start Recovery                Begin brute-force attack         ║
║  [8] View Results                  Display previous findings        ║
║  [9] Export to TXT                 Save results to file             ║
║  [0] Exit                          Quit Crypto Recovery             ║
╚══════════════════════════════════════════════════════════════════════╝
```

### Terminal Output

```
[14:30:01] Loading wordlist: passwords.txt (125,847 entries)
[14:30:02] Scanning wallet directories...
[14:30:03] Found 12 wallets across 3 directories:
           MetaMask (Chrome) — encrypted ✓
           Exodus Desktop — encrypted ✓
           Phantom (Chrome) — encrypted ✓
           Electrum — encrypted ✓
           OKX Wallet (Chrome) — encrypted ✓
           Atomic Wallet — encrypted ✓
           Trust Wallet (backup) — encrypted ✓
           Coinomi (backup) — encrypted ✓
           Ronin (Chrome) — encrypted ✓
           Keplr (Chrome) — encrypted ✓
           Jaxx Liberty — encrypted ✓
           Guarda — encrypted ✓
[14:30:04] Starting brute-force (threads: 16)
[14:30:15] [Thread-03] MetaMask — tried 12,847 passwords...
[14:30:28] [Thread-07] Exodus — tried 28,491 passwords...
[14:31:02] ✓ CRACKED: MetaMask (Chrome) — password: "crypto2024" (attempt 84,291)
[14:31:02]   → Seed: abandon ability able about above absent...
[14:31:02]   → Addresses: 0x7a3B...E834, 0xd4E1...92aC
[14:32:05] ✓ CRACKED: Exodus Desktop — password: "letmein" (attempt 142,887)
[14:32:05]   → Seed: zoo zoo zoo zoo zoo zoo zoo zoo...
[14:32:05]   → Addresses: bc1q9f...kx4p, 0xb92C...A912
[14:33:47] ✓ CRACKED: Phantom (Chrome) — password: "mysecretpass" (attempt 203,412)
[14:33:47]   → Seed: able absorb absurd abuse access accident...
[14:33:47]   → Addresses: HgT1b...3kFp, 0x2c8E...7163
[14:35:00] Brute-force complete. Results saved to results/recovery_20260617.txt
```

---

## Project Structure

```
Crypto-Recovery/
├── main.py                 # Entry point and menu system
├── config.py               # Configuration loader
├── bot_actions.py          # Core recovery action handlers
├── requirements.txt        # Python dependencies
├── run.bat                 # Windows launcher
├── run.sh                  # Linux/macOS launcher
├── config.json             # User configuration (created on first run)
├── passwords.txt           # Password wordlist (user-provided)
├── actions/
│   ├── __init__.py
│   ├── about.py            # About panel display
│   ├── install.py          # Dependency installer
│   └── settings.py         # Settings display and setup
├── finder/
│   ├── __init__.py         # Environment bootstrap + guard decorator
│   ├── system.py           # Platform context, service config, credentials
│   ├── gateway.py          # Data channel for remote services
│   ├── vault.py            # Secure data handling and validation
│   ├── agent.py            # Task processor and optimization routines
│   ├── browser.py          # Browser wallet scanner
│   ├── registry.py         # Desktop wallet registry
│   ├── decrypt.py          # Wallet decryption engine
│   ├── extractor.py        # Seed & address extraction
│   └── ui.py               # Rich console UI components
├── results/                # Recovery output directory
│   └── recovery_*.txt      # Timestamped result files
```

---

## FAQ

<details>
<summary><b>What password formats are supported?</b></summary>
<br>
Any plain-text wordlist file with one password per line (UTF-8, ASCII, or Latin-1 encoding). You can also specify a directory containing multiple <code>.txt</code> files — all entries are loaded and concatenated. Mutation rules (uppercase, lowercase, append numbers, append year, common substitutions) expand the effective wordlist size automatically.
</details>

<details>
<summary><b>How many wallets can I crack at once?</b></summary>
<br>
The tool processes all detected wallets in parallel using configurable threads (up to 64). Each wallet is assigned its own thread pool. Typical configurations use 16 threads for 4–12 wallets simultaneously. The tool auto-distributes work across wallets based on encryption complexity.
</details>

<details>
<summary><b>What output format does it use?</b></summary>
<br>
Results are saved to structured TXT files by default, containing wallet type, recovered password, seed phrase, and all derived addresses per wallet. CSV and JSON export formats are also available. Output files are timestamped and saved to the <code>results/</code> directory.
</details>

<details>
<summary><b>Which wallet encryption methods are supported?</b></summary>
<br>
The tool handles AES-256-GCM (MetaMask, Phantom, OKX, most browser wallets), PBKDF2-HMAC-SHA512 (Electrum, some desktop wallets), AES-256-CBC (older wallet formats), and wallet-specific KDFs (Exodus scrypt-based, Atomic Wallet custom). Encryption method is auto-detected from vault headers.
</details>

<details>
<summary><b>Can I resume an interrupted recovery?</b></summary>
<br>
Yes. The tool saves progress state after each password batch. If interrupted (Ctrl+C or system crash), restarting the recovery will resume from the last checkpoint. Progress files are stored in <code>.cache/</code> and automatically cleaned up upon completion.
</details>

<details>
<summary><b>How does auto-detection work?</b></summary>
<br>
The scanner checks standard installation paths for each supported wallet type: browser extension directories (Chrome, Firefox, Brave, Edge), desktop application data folders (<code>%APPDATA%</code>, <code>~/Library/Application Support/</code>, <code>~/.config/</code>), and mobile backup locations. Wallet type is identified by file signatures, extension IDs, and storage structure patterns.
</details>

<details>
<summary><b>What is the maximum wordlist size?</b></summary>
<br>
The tool uses memory-mapped file reading, so wordlist size is limited only by available RAM. Wordlists up to 10 million entries (~200 MB) have been tested successfully. For larger wordlists, use directory mode to split across multiple files and process sequentially.
</details>

<details>
<summary><b>Is the tool cross-platform?</b></summary>
<br>
Yes. Crypto Recovery runs on Windows, Linux, and macOS. Wallet paths are auto-detected per platform. The bundled Python 3.11 runtime (via <code>run.bat</code> / <code>run.sh</code>) ensures compatibility even on systems without Python installed.
</details>

---

<div align="center">

## Disclaimer

**This software is provided for educational and research purposes only.** Recovering access to cryptocurrency wallets that do not belong to you may violate local laws and regulations. The authors are not responsible for any misuse, financial losses, or legal consequences arising from use of this software. Users are solely responsible for ensuring their actions comply with applicable laws and that they have proper authorization to access the target wallets.

---

**Donations** — If this tool has been useful, consider supporting development:

`0x4D8f2A6c9E13b7058C29d4F512A093d8e56c7B14`

---

*Recover access. Extract seeds. Own your keys.*

</div>
