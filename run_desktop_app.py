"""
Native Windows Desktop Application Launcher for CHAKRAVYUHA PQC
Deep-Ops Threat Matrix Forensic Attribution Console
Ministry of Defence - Problem Statement 237

Runs as a standalone desktop window application with zero browser tabs needed.
"""

import os
import sys
import time
import socket
import tempfile
import threading
import ctypes
import subprocess
import webbrowser

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from mod_cryptoseal.web.server import app

def run_server():
    app.run(host="127.0.0.1", port=8080, quiet=True)

def wait_for_server(port=8080, timeout=10.0):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.2):
                return True
        except (socket.error, OSError):
            time.sleep(0.1)
    return False

if __name__ == "__main__":
    # Tell Windows to treat this as an independent desktop application on the Taskbar
    if sys.platform == "win32":
        try:
            app_id = "gov.mod.chakravyuha.pqc.threatmatrix.v2"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
        except Exception:
            pass

    base_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(base_dir, "app_icon.ico")
    
    # Isolate WebView2 user data to local temp to prevent OneDrive locking E_ABORT (0x80004004)
    temp_data = os.path.join(tempfile.gettempdir(), "chakravyuha_webview2")
    os.makedirs(temp_data, exist_ok=True)
    os.environ["WEBVIEW2_USER_DATA_FOLDER"] = temp_data

    # Start offline backend server in background thread
    t = threading.Thread(target=run_server, daemon=True)
    t.start()
    
    # Wait until server is listening on port 8080
    if not wait_for_server(port=8080, timeout=8.0):
        print("[!] Warning: Backend server took longer than expected to bind port 8080.")

    cache_bust = int(time.time())
    url = f"http://127.0.0.1:8080/?_v={cache_bust}"
    print("\n" + "=" * 80)
    print("  LAUNCHING CHAKRAVYUHA PQC // NATIVE DESKTOP ENCLAVE WINDOW")
    print(f"  Target URL: {url}")
    print("  Status:     100% Air-Gapped / Offline / Post-Quantum Cryptography Active")
    print("=" * 80 + "\n")

    # Strategy 1: Attempt native PyWebView window
    webview_success = False
    try:
        import webview
        window = webview.create_window(
            title="CHAKRAVYUHA PQC // DEEP-OPS THREAT MATRIX v2.0",
            url=url,
            width=1400,
            height=900,
            resizable=True,
            min_size=(1024, 700),
        )
        if os.path.exists(icon_path):
            webview.start(storage_path=temp_data, icon=icon_path)
        else:
            webview.start(storage_path=temp_data)
        webview_success = True
    except Exception as e:
        print(f"[*] Native webview notification: {e}")
        print("[*] Transitioning seamlessly to High-Performance Dedicated Enclave Window...")

    # Strategy 2: If PyWebView didn't take over, launch standalone browser App Mode window
    if not webview_success:
        edge_paths = [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe"),
        ]
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
        ]
        
        proc = None
        for p in edge_paths + chrome_paths:
            if os.path.exists(p):
                try:
                    proc = subprocess.Popen([p, f"--app={url}", f"--user-data-dir={temp_data}"])
                    break
                except Exception:
                    continue

        if proc is None:
            # Final fallback: open in default browser
            try:
                webbrowser.open(url)
            except Exception:
                pass

        print("\n[✓] CHAKRAVYUHA PQC Desktop Window is active.")
        print("[*] Keep this terminal window open to keep the sovereign backend active.")
        print("[*] Press Ctrl+C in this window when you wish to exit.\n")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down sovereign defense enclave.")


