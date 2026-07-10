# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

"""
RedditReal Bot License Key Generator
================================
This script generates a valid license key for the RedditReal Bot_V5 project.
Run this script to get your machine's HWID and generate a working license.
"""

import hashlib
import platform
import socket
import os
from datetime import datetime, timedelta


# ─────────────────────────────────────────────
# Must match the secret key in decoded_source.py
# ─────────────────────────────────────────────
SECRET_KEY = "mhvt81anyuazoq7m2yznn5nrpb3r25glbz9trsq7lur4g5omobmup3ucsgec4fqz"


def generate_hardware_id():
    """
    Generates the Hardware ID exactly as decoded_source.py does.
    Based on: CPU model, hostname, OS name, machine architecture.
    """
    try:
        cpu_model = platform.processor() or "unknown"
        hostname  = socket.gethostname()
        system    = platform.system()
        machine   = platform.machine()
        hardware_string = f"{cpu_model}|{hostname}|{system}|{machine}"
        hash_obj  = hashlib.sha256(hardware_string.encode())
        return hash_obj.hexdigest()[:32].upper()
    except Exception:
        import time
        return "UNKNOWN-" + hashlib.md5(str(time.time()).encode()).hexdigest()[:20].upper()


def generate_license(hardware_id: str, expiry_date: datetime) -> str:
    """
    Generates a K02-format license key for the given HWID and expiry date.
    Format: K02-{hwid[:8]}-{hex(YYYYMMDD)}-{sha256_sig[:16]}
    """
    expiry_str    = expiry_date.strftime("%Y%m%d")
    hex_expiry    = expiry_str.encode().hex().upper()
    hwid_prefix   = hardware_id[:8]
    data_to_sign  = f"{hardware_id}|{hex_expiry}|{SECRET_KEY}"
    signature     = hashlib.sha256(data_to_sign.encode()).hexdigest()[:16].upper()
    license_key   = f"K02-{hwid_prefix}-{hex_expiry}-{signature}"
    return license_key


def verify_license(license_key: str, hardware_id: str):
    """
    Verifies the license key using the same logic as decoded_source.py.
    """
    parts = license_key.strip().split('-')
    if len(parts) != 4 or parts[0] != 'K02':
        return False, "Invalid format (must start with K02)"

    hwid_prefix   = parts[1]
    hex_expiry    = parts[2]
    provided_sig  = parts[3]

    if hwid_prefix != hardware_id[:8]:
        return False, f"HWID mismatch (key is for: {hwid_prefix}, this machine: {hardware_id[:8]})"

    try:
        expiry_str = bytes.fromhex(hex_expiry).decode()
        expiry_date = datetime(int(expiry_str[:4]), int(expiry_str[4:6]), int(expiry_str[6:8]))
    except Exception:
        return False, "Invalid expiry date format in key"

    if expiry_date < datetime.now():
        return False, f"License expired on {expiry_date.strftime('%Y-%m-%d')}"

    data_to_sign   = f"{hardware_id}|{hex_expiry}|{SECRET_KEY}"
    computed_sig   = hashlib.sha256(data_to_sign.encode()).hexdigest()[:16].upper()

    if computed_sig != provided_sig:
        return False, "Invalid signature"

    days_left = (expiry_date - datetime.now()).days
    return True, f"Valid until {expiry_date.strftime('%Y-%m-%d')} ({days_left} days remaining)"


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("   RedditReal -- License Key Generator")
    print("=" * 60)

    local_hwid = generate_hardware_id()
    hwid_input = input(f"\nEnter Hardware ID (leave blank to use local HWID: {local_hwid}): ").strip()
    hwid = hwid_input if hwid_input else local_hwid

    print(f"\n[HWID]  Using Hardware ID:\n        {hwid}")
    print(f"        Prefix (first 8 chars): {hwid[:8]}")

    # ── Choose your expiry date here ──────────────────────────────
    # Option 1: Fixed expiry date (edit as needed)
    # expiry = datetime(2027, 12, 31)

    # Option 2: N days from today
    try:
        user_input = input("\nEnter number of days for license validity (default 30): ").strip()
        days_valid = int(user_input) if user_input else 30
    except ValueError:
        print("Invalid input, using default 30 days.")
        days_valid = 30
        
    expiry = datetime.now() + timedelta(days=days_valid)
    # ──────────────────────────────────────────────────────────────

    license_key = generate_license(hwid, expiry)

    print(f"\n[DATE]  Expiry Date  : {expiry.strftime('%Y-%m-%d')} ({days_valid} days from today)")
    print(f"\n[KEY]   License Key  :\n\n        {license_key}\n")

    # Verify the generated key immediately
    ok, msg = verify_license(license_key, hwid)
    if ok:
        print(f"[OK]    Verification : {msg}")
    else:
        print(f"[FAIL]  Verification Failed: {msg}")

    # Save to license.key in the same directory as the script
    bot_dir      = os.path.dirname(os.path.abspath(__file__))
    license_path = os.path.join(bot_dir, "license.key")
    try:
        with open(license_path, "w") as f:
            f.write(license_key)
        print(f"\n[SAVED] License saved to:\n        {license_path}")
    except Exception as e:
        print(f"\n[WARN]  Could not auto-save: {e}")
        print(f"        Please manually save the key to: {license_path}")

    print("\n" + "=" * 60)
    input("\nPress Enter to exit...")
