"""
Native Windows Desktop Application Launcher for CryptoSeal PQC
Ministry of Defence — Problem Statement 237

Runs as a standalone desktop window application with zero browser tabs needed.
"""

import sys
import time
import threading
import webview
from mod_cryptoseal.web.server import app

def run_server():
    app.run(host="127.0.0.1", port=8080, quiet=True)

if __name__ == "__main__":
    # Start offline backend server in background thread
    t = threading.Thread(target=run_server, daemon=True)
    t.start()
    time.sleep(1.0)

    # Launch native desktop application window
    window = webview.create_window(
        title="Ministry of Defence — CryptoSeal PQC Console",
        url="http://127.0.0.1:8080/",
        width=1320,
        height=880,
        resizable=True,
        min_size=(1024, 700),
    )
    webview.start()
