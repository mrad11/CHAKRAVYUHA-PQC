"""
One-Command Launcher for CHAKRAVYUHA PQC Offline Web Dashboard
Deep-Ops Threat Matrix Forensic Attribution Console
Ministry of Defence - Problem Statement 237

Run with:
    python run_web.py
Then open http://127.0.0.1:8080/ in your browser.
"""

import os
import sys
import time
import socket
import threading
import webbrowser

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from mod_cryptoseal.web.server import app

def wait_and_open_browser(url, port):
    """Poll socket until server is accepting requests, then open browser."""
    start = time.time()
    while time.time() - start < 10.0:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.2):
                break
        except (socket.error, OSError):
            time.sleep(0.1)
    time.sleep(0.3)
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"Browser launch notification: {e}")

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8080
    cache_bust = int(time.time())
    url = f"http://{host}:{port}/?_v={cache_bust}"
    print("\n" + "=" * 80)
    print("  LAUNCHING CHAKRAVYUHA PQC // DEEP-OPS THREAT MATRIX WEB DASHBOARD")
    print(f"  Target URL: {url}")
    print("  Status:     100% Air-Gapped / Offline / Post-Quantum Cryptography Active")
    print("=" * 80 + "\n")

    # Start browser opener in background thread that waits for the server to be ready
    t = threading.Thread(target=wait_and_open_browser, args=(url, port), daemon=True)
    t.start()

    print(f"[*] Sovereign Defence Console starting on http://{host}:{port}/ ...")
    print("[*] Press Ctrl+C in this console to terminate the server.\n")

    try:
        app.run(host=host, port=port, debug=False, quiet=True)
    except KeyboardInterrupt:
        print("\nServer terminated by operator.")

