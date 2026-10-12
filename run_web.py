"""
One-Command Launcher for CHAKRAVYUHA PQC Offline Web Dashboard
Deep-Ops Threat Matrix Forensic Attribution Console
Ministry of Defence - Problem Statement 237

Run with:
    python run_web.py
Then open http://127.0.0.1:8080/ in your browser.
"""

import sys
import time
import webbrowser

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from mod_cryptoseal.web.server import start_server

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8080
    cache_bust = int(time.time())
    url = f"http://{host}:{port}/?_v={cache_bust}"
    print("\n" + "=" * 80)
    print("  LAUNCHING CHAKRAVYUHA PQC // DEEP-OPS THREAT MATRIX CONSOLE")
    print(f"  Target URL: {url}")
    print("  Status:     100% Air-Gapped / Offline / Post-Quantum Cryptography Active")
    print("=" * 80 + "\n")
    try:
        webbrowser.open(url)
    except Exception:
        pass
    start_server(host=host, port=port)
