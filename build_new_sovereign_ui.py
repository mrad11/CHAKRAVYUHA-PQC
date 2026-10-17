"""
Builder script to generate the new Sovereign Basalt & Cinnabar-Celadon UI for CHAKRAVYUHA PQC.
Generates:
1. mod_cryptoseal/web/index_html.py
2. LAUNCH_PORTAL.html
3. index.html
"""

import os
import sys

def build():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    icon_b64_file = os.path.join(base_dir, "app_icon_128_b64.txt")
    
    if os.path.exists(icon_b64_file):
        with open(icon_b64_file, "r") as f:
            icon_data_uri = f"data:image/png;base64,{f.read().strip()}"
    else:
        icon_data_uri = "app_icon.png"

    # Read the master HTML template
    template_path = os.path.join(base_dir, "sovereign_ui_template.html")
    with open(template_path, "r", encoding="utf-8") as f:
        html_template = f.read()

    rendered_html = html_template.replace("__ICON_DATA_URI__", icon_data_uri)

    # 1. Update index_html.py
    index_py_path = os.path.join(base_dir, "mod_cryptoseal", "web", "index_html.py")
    py_code = f'''"""
Chakravyuha PQC - Sovereign Defense Cryptographic Enclave UI
Auto-generated from sovereign_ui_template.html
"""
import os

HTML_CONTENT = {repr(rendered_html)}

def get_dashboard_html():
    return HTML_CONTENT
'''
    with open(index_py_path, "w", encoding="utf-8") as f:
        f.write(py_code)
    print("[+] Successfully generated: mod_cryptoseal/web/index_html.py")

    # 2. Update LAUNCH_PORTAL.html
    portal_path = os.path.join(base_dir, "LAUNCH_PORTAL.html")
    with open(portal_path, "w", encoding="utf-8") as f:
        f.write(rendered_html)
    print("[+] Successfully generated: LAUNCH_PORTAL.html")

    # 3. Update index.html
    root_index_path = os.path.join(base_dir, "index.html")
    with open(root_index_path, "w", encoding="utf-8") as f:
        f.write(rendered_html)
    print("[+] Successfully generated: index.html")

if __name__ == "__main__":
    build()
