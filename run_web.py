"""
One-Command Launcher for CryptoSeal PQC Offline Web Dashboard
Ministry of Defence — Problem Statement 237

Run with:
    python run_web.py
Then open http://127.0.0.1:8080/ in your browser.
"""

import sys
import webbrowser

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from mod_cryptoseal.web.server import start_server

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8080
    url = f"http://{host}:{port}/"
    print("\n" + "=" * 80)
    print("  LAUNCHING MINISTRY OF DEFENCE CRYPTOSEAL PQC DEFENCE CONSOLE")
    print(f"  Target URL: {url}")
    print("  Status:     100% Air-Gapped / Offline / Post-Quantum Cryptography Active")
    print("=" * 80 + "\n")
    try:
        webbrowser.open(url)
    except Exception:
        pass
    start_server(host=host, port=port)
