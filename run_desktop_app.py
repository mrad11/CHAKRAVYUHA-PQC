"""
Native Windows Desktop Application Launcher for CHAKRAVYUHA PQC
Deep-Ops Threat Matrix Forensic Attribution Console
Ministry of Defence - Problem Statement 237

Runs as a standalone desktop window application with zero browser tabs needed.
"""

import os
import sys
import time
import threading
import ctypes
import webview
from mod_cryptoseal.web.server import app

def run_server():
    app.run(host="127.0.0.1", port=8080, quiet=True)

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

    # Start offline backend server in background thread
    t = threading.Thread(target=run_server, daemon=True)
    t.start()
    time.sleep(1.0)

    # Launch native desktop application window with anti-cache InPrivate session
    cache_bust = int(time.time())
    window = webview.create_window(
        title="CHAKRAVYUHA PQC // DEEP-OPS THREAT MATRIX v2.0",
        url=f"http://127.0.0.1:8080/?_v={cache_bust}",
        width=1400,
        height=900,
        resizable=True,
        min_size=(1024, 700),
    )
    # private_mode=True bypasses all local WebView2 cache, icon= sets the window & taskbar icon
    if os.path.exists(icon_path):
        webview.start(private_mode=True, icon=icon_path)
    else:
        webview.start(private_mode=True)

