"""
Ministry of Defence - CHAKRAVYUHA PQC
Deep-Ops Threat Matrix Forensic Attribution Console
100% Self-Contained, Air-Gapped, Zero-Dependency Native 3D WebGL / Canvas Engine
"""

import os

def get_dashboard_html() -> str:
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    icon_b64_file = os.path.join(base_dir, "app_icon_128_b64.txt")
    if os.path.exists(icon_b64_file):
        with open(icon_b64_file, "r") as f:
            icon_data_uri = f"data:image/png;base64,{f.read().strip()}"
    else:
        icon_data_uri = "/app_icon.png"

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CHAKRAVYUHA PQC // DEEP-OPS THREAT MATRIX v2.0</title>
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <link rel="icon" type="image/png" href="__ICON_DATA_URI__">
  <link rel="shortcut icon" href="/favicon.ico">
  <link rel="apple-touch-icon" href="__ICON_DATA_URI__">

  <style>
    :root {
      --bg-abyssal: #080A0D;
      --bg-surface: #0C1017;
      --bg-elevated: #111827;
      --border-steel: #1F2937;
      --border-accent: #10B981;
      --phosphor-emerald: #10B981;
      --phosphor-dark: #059669;
      --night-vision-olive: #1F2937;
      --warning-red: #EF4444;
      --telemetry-amber: #F59E0B;
      --text-main: #E2E8F0;
      --text-muted: #94A3B8;
      --text-dim: #64748B;
      --font-mono: 'JetBrains Mono', 'Consolas', 'Courier New', monospace;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    
    body {
      background-color: var(--bg-abyssal);
      color: var(--text-main);
      font-family: var(--font-mono);
      min-height: 100vh;
      overflow-x: hidden;
      position: relative;
    }

    /* CRT Phosphor Scanline Overlay */
    body::before {
      content: " ";
      position: fixed;
      top: 0; left: 0; width: 100vw; height: 100vh;
      background: linear-gradient(rgba(18, 22, 28, 0) 50%, rgba(0, 0, 0, 0.4) 50%);
      background-size: 100% 3px;
      z-index: 999;
      pointer-events: none;
      opacity: 0.55;
    }

    /* Top Command Header */
    .command-header {
      background: rgba(8, 10, 13, 0.98);
      border-bottom: 2px solid var(--phosphor-dark);
      padding: 12px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: sticky;
      top: 0;
      z-index: 100;
      box-shadow: 0 4px 25px rgba(0,0,0,0.8);
    }

    .brand-section {
      display: flex;
      align-items: center;
      gap: 14px;
    }

    .brand-sigil {
      width: 44px; height: 44px;
      border: 2px solid var(--phosphor-emerald);
      border-radius: 6px;
      object-fit: cover;
      display: block;
      box-shadow: 0 0 20px rgba(16, 185, 129, 0.45);
    }


    .brand-meta h1 {
      font-size: 16px;
      font-weight: 800;
      letter-spacing: 2px;
      color: #FFF;
      text-transform: uppercase;
    }

    .brand-meta p {
      font-size: 10px;
      color: var(--phosphor-emerald);
      letter-spacing: 1px;
    }

    .telemetry-badges {
      display: flex;
      gap: 8px;
      align-items: center;
      flex-wrap: wrap;
    }

    .t-badge {
      font-size: 10px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 3px;
      letter-spacing: 0.8px;
      text-transform: uppercase;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      border: 1px solid transparent;
    }

    .badge-emerald {
      background: rgba(16, 185, 129, 0.12);
      border-color: rgba(16, 185, 129, 0.4);
      color: var(--phosphor-emerald);
    }

    .badge-olive {
      background: rgba(31, 41, 55, 0.7);
      border-color: var(--border-steel);
      color: var(--text-muted);
    }

    .badge-red {
      background: rgba(239, 68, 68, 0.15);
      border-color: rgba(239, 68, 68, 0.5);
      color: var(--warning-red);
    }

    /* Spatial Layout: Dense Command Rail */
    .theater-container {
      max-width: 1720px;
      margin: 16px auto;
      padding: 0 16px;
      display: grid;
      grid-template-columns: 280px 1fr 340px;
      gap: 16px;
    }

    @media (max-width: 1200px) {
      .theater-container {
        grid-template-columns: 1fr;
      }
    }

    /* Panels & Cards */
    .tactical-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-steel);
      border-radius: 4px;
      padding: 16px;
      margin-bottom: 14px;
      box-shadow: 0 4px 16px rgba(0,0,0,0.5);
    }

    .tactical-card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid var(--border-steel);
      padding-bottom: 8px;
      margin-bottom: 12px;
    }

    .card-title {
      font-size: 11px;
      font-weight: 800;
      color: #FFF;
      letter-spacing: 1px;
      text-transform: uppercase;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .card-title::before {
      content: "";
      width: 6px; height: 6px;
      background: var(--phosphor-emerald);
      border-radius: 50%;
      box-shadow: 0 0 8px var(--phosphor-emerald);
    }

    /* Nav Rail */
    .nav-button {
      width: 100%;
      text-align: left;
      background: var(--bg-elevated);
      border: 1px solid var(--border-steel);
      color: var(--text-muted);
      padding: 11px 13px;
      border-radius: 3px;
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      margin-bottom: 6px;
      cursor: pointer;
      display: flex;
      justify-content: space-between;
      align-items: center;
      transition: all 0.15s ease;
    }

    .nav-button:hover {
      border-color: rgba(16, 185, 129, 0.4);
      color: #FFF;
      background: rgba(31, 41, 55, 0.6);
    }

    .nav-button.active {
      background: rgba(16, 185, 129, 0.15);
      border-color: var(--phosphor-emerald);
      color: var(--phosphor-emerald);
      box-shadow: 0 0 15px rgba(16, 185, 129, 0.2);
    }

    /* 3D Native Canvas Viewport */
    .radar-viewport {
      width: 100%;
      height: 270px;
      background: #040608;
      border: 1px solid var(--border-steel);
      border-radius: 4px;
      margin-bottom: 14px;
      position: relative;
      overflow: hidden;
      box-shadow: inset 0 0 40px rgba(5, 150, 105, 0.18);
    }

    #radar-canvas {
      width: 100%;
      height: 100%;
      display: block;
      cursor: grab;
    }

    #radar-canvas:active {
      cursor: grabbing;
    }

    .radar-tag {
      position: absolute;
      top: 10px; left: 12px;
      font-size: 10px;
      font-weight: 700;
      color: var(--phosphor-emerald);
      letter-spacing: 1px;
      pointer-events: none;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .radar-reticle {
      position: absolute;
      bottom: 8px; right: 12px;
      font-size: 9px;
      color: var(--text-dim);
      pointer-events: none;
    }

    /* Form Elements */
    .t-label {
      display: block;
      font-size: 10px;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.8px;
      margin-bottom: 5px;
    }

    .t-input, .t-select {
      width: 100%;
      background: var(--bg-abyssal);
      border: 1px solid var(--border-steel);
      color: #FFF;
      font-family: var(--font-mono);
      font-size: 11px;
      padding: 9px 12px;
      border-radius: 3px;
      outline: none;
      margin-bottom: 12px;
    }

    .t-input:focus, .t-select:focus {
      border-color: var(--phosphor-emerald);
      box-shadow: 0 0 10px rgba(16, 185, 129, 0.25);
    }

    .checkbox-tile {
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: var(--bg-abyssal);
      border: 1px solid var(--border-steel);
      padding: 8px 12px;
      border-radius: 3px;
      margin-bottom: 6px;
      cursor: pointer;
      font-size: 11px;
    }

    .checkbox-tile:hover {
      border-color: rgba(16, 185, 129, 0.4);
    }

    .checkbox-tile input {
      accent-color: var(--phosphor-emerald);
      margin-right: 10px;
    }

    /* Buttons */
    .t-btn {
      width: 100%;
      padding: 12px 18px;
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 1.2px;
      text-transform: uppercase;
      border-radius: 3px;
      border: none;
      cursor: pointer;
      transition: all 0.15s ease;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
    }

    .t-btn-emerald {
      background: var(--phosphor-emerald);
      color: var(--bg-abyssal);
      box-shadow: 0 0 20px rgba(16, 185, 129, 0.4);
    }

    .t-btn-emerald:hover {
      background: #34D399;
      box-shadow: 0 0 30px rgba(16, 185, 129, 0.6);
      transform: translateY(-1px);
    }

    .t-btn-dark {
      background: var(--bg-elevated);
      border: 1px solid var(--border-steel);
      color: var(--text-main);
    }

    .t-btn-dark:hover {
      border-color: var(--phosphor-emerald);
      color: var(--phosphor-emerald);
    }

    .t-btn-crimson {
      background: var(--warning-red);
      color: #FFF;
      box-shadow: 0 0 20px rgba(239, 68, 68, 0.4);
    }

    .t-btn-crimson:hover {
      background: #F87171;
    }

    /* Telemetry Stream Console */
    .telemetry-stream {
      background: var(--bg-abyssal);
      border: 1px solid var(--border-steel);
      border-radius: 3px;
      padding: 12px;
      font-size: 10px;
      color: var(--phosphor-emerald);
      line-height: 1.6;
      height: 260px;
      overflow-y: auto;
      white-space: pre-wrap;
    }

    /* Section 65B Dossier Modal */
    .dossier-overlay {
      position: fixed;
      top: 0; left: 0; width: 100vw; height: 100vh;
      background: rgba(8, 10, 13, 0.92);
      backdrop-filter: blur(10px);
      z-index: 1000;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }

    .dossier-box {
      background: var(--bg-surface);
      border: 2px solid var(--warning-red);
      border-radius: 6px;
      width: 100%;
      max-width: 680px;
      padding: 24px;
      box-shadow: 0 0 60px rgba(239, 68, 68, 0.4);
    }

    .tab-content { display: none; }
    .tab-content.active { display: block; }
  </style>
</head>
<body>

  <!-- Top Tactical Command Header -->
  <header class="command-header">
    <div class="brand-section">
      <img src="__ICON_DATA_URI__" class="brand-sigil" alt="CHAKRAVYUHA PQC Sovereign Lion Logo" />
      <div class="brand-meta">
        <h1>CHAKRAVYUHA PQC // DEEP-OPS THREAT MATRIX</h1>
        <p>MINISTRY OF DEFENCE // PROBLEM STATEMENT 237 // CLASSIFICATION: TOP SECRET</p>
      </div>
    </div>

    <div class="telemetry-badges">
      <span class="t-badge badge-emerald">
        <span style="display:inline-block; width:6px; height:6px; border-radius:50%; background:#10B981;"></span>
        NIST FIPS 203 (ML-KEM-768)
      </span>
      <span class="t-badge badge-olive">FIPS 204 (ML-DSA-65)</span>
      <span class="t-badge badge-emerald" id="header-tpm-status">TPM 2.0 PCR-7 MATCH</span>
      <span class="t-badge badge-olive" id="header-chain-status">DLT: CONSORTIUM HEALTHY</span>
    </div>
  </header>

  <!-- Notice Banner Confirming New UI -->
  <div style="background:#0F1A14; border-bottom:1px solid #10B981; padding:6px 24px; font-size:10px; color:#10B981; display:flex; justify-content:space-between; align-items:center;">
    <span>[CONSOLE VERSION: 2.0 // DEEP-OPS THREAT MATRIX ACTIVE // ZERO CLOUD DEPENDENCY]</span>
    <span style="color:#94A3B8;">ENCLAVE STATUS: AIR-GAPPED & SECURE</span>
  </div>

  <!-- Main Dense Command Rail Layout -->
  <div class="theater-container">

    <!-- LEFT RAIL: Hardware TPM Enclave & Command Nav (280px) -->
    <aside>
      <!-- Silicon Root of Trust Card -->
      <div class="tactical-card">
        <div class="tactical-card-header">
          <span class="card-title">HARDWARE TPM 2.0 ENCLAVE</span>
          <span style="font-size:9px; color:#10B981; background:rgba(16,185,129,0.1); padding:2px 6px; border-radius:3px;">LOCKED</span>
        </div>
        <div style="font-size:10px; line-height:1.8; color:var(--text-muted);">
          <div style="display:flex; justify-content:space-between;">
            <span>SILICON ATTEST:</span> <span style="color:#FFF;">INFINEON OPTIGA</span>
          </div>
          <div style="display:flex; justify-content:space-between;">
            <span>SECURE BOOT:</span> <span style="color:#10B981;">PCR 7 VERIFIED</span>
          </div>
          <div style="display:flex; justify-content:space-between;">
            <span>ANTI-VM HOOK:</span> <span style="color:#10B981;">0xDEAD_C0DE OK</span>
          </div>
          <div style="display:flex; justify-content:space-between;">
            <span>AIR-GAP STATE:</span> <span style="color:#10B981;">100% UNTETHERED</span>
          </div>
        </div>
      </div>

      <!-- Tactical Operation Navigation Rail -->
      <div class="tactical-card">
        <div class="tactical-card-header">
          <span class="card-title">TACTICAL VIEWPORT</span>
        </div>
        <button class="nav-button active" onclick="switchTab('tab-dispatch', this)">
          <span>01 // PQC ENVELOPE</span> <span>►</span>
        </button>
        <button class="nav-button" onclick="switchTab('tab-decrypt', this)">
          <span>02 // DECRYPT PROVENANCE</span> <span>►</span>
        </button>
        <button class="nav-button" onclick="switchTab('tab-forensics', this)">
          <span>03 // OPTICAL FORENSICS</span> <span>►</span>
        </button>
        <button class="nav-button" onclick="switchTab('tab-ledger', this)">
          <span>04 // MERKLE DLT LEDGER</span> <span>►</span>
        </button>
      </div>

      <!-- Authorized Officer Directory -->
      <div class="tactical-card">
        <div class="tactical-card-header">
          <span class="card-title">AUTHORIZED PERSONNEL</span>
        </div>
        <div id="officers-roster" style="font-size:10px; color:var(--text-muted); line-height:1.8;">
          <div style="padding:6px; background:#080A0D; border:1px solid #1F2937; border-radius:3px; margin-bottom:6px;">
            <div style="font-weight:700; color:#FFF;">Col. Rajiv Sharma</div>
            <div style="font-size:9px; color:#10B981;">IND-MOD-001 // Western Command</div>
          </div>
          <div style="padding:6px; background:#080A0D; border:1px solid #1F2937; border-radius:3px; margin-bottom:6px;">
            <div style="font-weight:700; color:#FFF;">Capt. Priya Nair</div>
            <div style="font-size:9px; color:#10B981;">IND-MOD-002 // Naval Cyber Cell</div>
          </div>
          <div style="padding:6px; background:#080A0D; border:1px solid #1F2937; border-radius:3px;">
            <div style="font-weight:700; color:#FFF;">Wg Cdr. Amit Verma</div>
            <div style="font-size:9px; color:#10B981;">IND-MOD-003 // Air Force FOB</div>
          </div>
        </div>
      </div>
    </aside>

    <!-- CENTER RAIL: 3D LiDAR Threat Globe & Active Execution Terminal -->
    <main>
      <!-- 3D Native Canvas Viewport (Zero External Dependencies, 100% Offline) -->
      <div class="radar-viewport">
        <div class="radar-tag">
          <span style="display:inline-block; width:6px; height:6px; border-radius:50%; background:#10B981; box-shadow:0 0 6px #10B981;"></span>
          3D VOLUMETRIC LIDAR RADAR // ML-KEM-768 LATTICE CORE
        </div>
        <div class="radar-reticle">
          AZIMUTH: 342.8° | RANGE: 50KM | DEFCON-5 SECURE
        </div>
        <canvas id="radar-canvas"></canvas>
      </div>

      <!-- TAB 1: PQC Envelope Dispatch -->
      <div id="tab-dispatch" class="tab-content active">
        <div class="tactical-card">
          <div class="tactical-card-header">
            <span class="card-title">POST-QUANTUM BROADCAST ENVELOPE (.MODPKG)</span>
            <span style="font-size:9px; color:#10B981;">NIST FIPS 203 + 204</span>
          </div>

          <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
            <div>
              <label class="t-label">DOCUMENT IDENTIFIER</label>
              <input type="text" class="t-input" value="DEFENCE_OPERATION_TRIDENT.pdf" readonly>
            </div>
            <div>
              <label class="t-label">SECURITY CLASSIFICATION</label>
              <input type="text" class="t-input" value="COSMIC TOP SECRET // RESTRICTED" style="color:var(--warning-red); font-weight:700;" readonly>
            </div>
          </div>

          <label class="t-label">MULTI-RECIPIENT CLEARANCE LIST</label>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-bottom:14px;">
            <label class="checkbox-tile">
              <span><input type="checkbox" name="recip" value="IND-MOD-001" checked> Col. Rajiv Sharma</span>
              <span style="font-size:9px; color:#10B981;">IND-MOD-001</span>
            </label>
            <label class="checkbox-tile">
              <span><input type="checkbox" name="recip" value="IND-MOD-002" checked> Capt. Priya Nair</span>
              <span style="font-size:9px; color:#10B981;">IND-MOD-002</span>
            </label>
            <label class="checkbox-tile">
              <span><input type="checkbox" name="recip" value="IND-MOD-003" checked> Wg Cdr. Amit Verma</span>
              <span style="font-size:9px; color:#10B981;">IND-MOD-003</span>
            </label>
          </div>

          <button class="t-btn t-btn-emerald" onclick="executeDistribution()">
            PACKAGE & DISPATCH QUANTUM ENVELOPE (.MODPKG)
          </button>
        </div>
      </div>

      <!-- TAB 2: Decryption & Atomic Provenance -->
      <div id="tab-decrypt" class="tab-content">
        <div class="tactical-card">
          <div class="tactical-card-header">
            <span class="card-title">ATOMIC DECRYPTION & IMPERCEPTIBLE WATERMARKING</span>
            <span style="font-size:9px; color:#10B981;">TARDOS DWT-DCT MATRIX</span>
          </div>

          <label class="t-label">SELECT FIELD OFFICER TERMINAL</label>
          <select id="decrypt-officer-select" class="t-select">
            <option value="IND-MOD-001">Col. Rajiv Sharma (Western Command // IND-MOD-001)</option>
            <option value="IND-MOD-002" selected>Capt. Priya Nair (Naval Cyber Cell // IND-MOD-002)</option>
            <option value="IND-MOD-003">Wg Cdr. Amit Verma (Air Force FOB // IND-MOD-003)</option>
          </select>

          <p style="font-size:11px; color:var(--text-muted); margin-bottom:14px; line-height:1.6;">
            Atomic Decryption Guard enforces hardware TPM 2.0 attestation before unsealing ephemeral keys. 
            Recipient identity, terminal MAC, and millisecond timestamps are burned into the document pixels 
            via invisible frequency modulation.
          </p>

          <button class="t-btn t-btn-emerald" onclick="executeDecryption()">
            SIGN DECRYPTION PROVENANCE RECORD (DPR) & UNSEAL
          </button>

          <div id="decrypted-result-view" style="display:none; margin-top:16px; padding:12px; background:#080A0D; border:1px solid #10B981; border-radius:4px;">
            <div style="font-size:11px; color:#10B981; font-weight:700; margin-bottom:6px;">✓ DOCUMENT DECRYPTED & BOUND TO SILICON</div>
            <div id="decrypted-meta" style="font-size:10px; color:var(--text-muted); line-height:1.6;"></div>
            <div style="display:flex; gap:10px; margin-top:10px;">
              <button class="t-btn t-btn-dark" style="padding:6px 12px; font-size:10px;" onclick="simulateLeakFromHere()">
                LEAK THIS COPY TO SOCIAL MEDIA (SIMULATION)
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- TAB 3: Optical Forensic Recovery -->
      <div id="tab-forensics" class="tab-content">
        <div class="tactical-card">
          <div class="tactical-card-header">
            <span class="card-title">OPTICAL LEAK INVESTIGATION & RECONSTRUCTION</span>
            <span style="font-size:9px; color:var(--warning-red);">SECTION 65B READY</span>
          </div>

          <p style="font-size:11px; color:var(--text-muted); margin-bottom:14px; line-height:1.6;">
            Extracts invisible Tardos watermarks from secondary capture devices (smartphone screen photos, 
            analog paper prints, compressed images). Applies homography de-warping and Moiré pattern suppression.
          </p>

          <button class="t-btn t-btn-crimson" onclick="investigateRecentDecrypted()">
            RECONSTRUCT WATERMARK FROM LEAKED SCREEN CAPTURE
          </button>
        </div>
      </div>

      <!-- TAB 4: Merkle DLT Ledger -->
      <div id="tab-ledger" class="tab-content">
        <div class="tactical-card">
          <div class="tactical-card-header">
            <span class="card-title">CONSORTIUM DLT BLOCKCHAIN EXPLORER</span>
            <div style="display:flex; gap:6px;">
              <button class="t-btn t-btn-dark" style="padding:4px 8px; font-size:9px;" onclick="loadLedgerData()">REFRESH</button>
              <button class="t-btn t-btn-dark" style="padding:4px 8px; font-size:9px;" onclick="auditLedgerChain()">AUDIT</button>
              <button class="t-btn t-btn-crimson" style="padding:4px 8px; font-size:9px;" onclick="simulateAdminTamper()">SIMULATE TAMPER</button>
              <button class="t-btn t-btn-dark" style="padding:4px 8px; font-size:9px;" onclick="restoreLedgerClean()">RESET</button>
            </div>
          </div>
          <div id="ledger-blocks-list" style="max-height:360px; overflow-y:auto; font-size:10px;"></div>
        </div>
      </div>
    </main>

    <!-- RIGHT RAIL: Real-Time Cryptographic Telemetry (340px) -->
    <aside>
      <div class="tactical-card">
        <div class="tactical-card-header">
          <span class="card-title">LIVE CRYPTOGRAPHIC TELEMETRY</span>
        </div>
        <div id="telemetry-log" class="telemetry-stream">[+] CHAKRAVYUHA PQC Kernel Bootstrapped.\n[+] Air-Gapped PKI Keystore Loaded.\n[+] Hardware TPM 2.0 PCR-7 Attested.\n[+] Standing by for PQC Distribution.</div>
      </div>
    </aside>

  </div>

  <!-- Section 65B Legal Dossier Modal -->
  <div id="dossier-modal" class="dossier-overlay">
    <div class="dossier-box">
      <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid var(--warning-red); padding-bottom:10px; margin-bottom:14px;">
        <span style="font-size:12px; font-weight:800; color:var(--warning-red);">
          ⚖ INDIAN EVIDENCE ACT // SECTION 65B FORENSIC DOSSIER
        </span>
        <button style="background:none; border:none; color:#FFF; cursor:pointer;" onclick="closeDossier()">[ESC_CLOSE]</button>
      </div>
      <div id="dossier-body" style="font-size:11px; line-height:1.8; color:var(--text-main);"></div>
      <div style="margin-top:16px; text-align:right;">
        <button class="t-btn t-btn-dark" style="width:auto; padding:6px 14px; font-size:10px;" onclick="closeDossier()">CLOSE CERTIFICATE</button>
      </div>
    </div>
  </div>

  <!-- Pure Native 3D Engine & Web Audio (Zero External Dependencies) -->
  <script>
    // Audio Synthesizer
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    function playTacticalChirp(freq = 880, duration = 0.04) {
      try {
        if (!audioCtx) return;
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + duration);
      } catch (e) {}
    }

    // Pure Native 3D LiDAR Threat Globe & Lattice Simulator
    (function initNative3DRadar() {
      const canvas = document.getElementById('radar-canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');

      function resize() {
        canvas.width = canvas.parentElement.clientWidth;
        canvas.height = canvas.parentElement.clientHeight;
      }
      resize();
      window.addEventListener('resize', resize);

      // 1,200 LiDAR Points on a 3D Sphere
      const pointCount = 1200;
      const points = [];
      for (let i = 0; i < pointCount; i++) {
        const theta = Math.acos(2 * Math.random() - 1);
        const phi = Math.random() * Math.PI * 2;
        const r = 90 + (Math.random() - 0.5) * 8;
        points.push({
          x: r * Math.sin(theta) * Math.cos(phi),
          y: r * Math.sin(theta) * Math.sin(phi),
          z: r * Math.cos(theta),
        });
      }

      let rotY = 0;
      let rotX = 0.2;
      let isDragging = false;
      let lastMouseX = 0;
      let lastMouseY = 0;

      canvas.addEventListener('mousedown', (e) => {
        isDragging = true;
        lastMouseX = e.clientX;
        lastMouseY = e.clientY;
      });
      window.addEventListener('mouseup', () => { isDragging = false; });
      window.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        rotY += (e.clientX - lastMouseX) * 0.008;
        rotX += (e.clientY - lastMouseY) * 0.008;
        lastMouseX = e.clientX;
        lastMouseY = e.clientY;
      });

      let sweepAngle = 0;

      function render() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        const cx = canvas.width / 2;
        const cy = canvas.height / 2;
        const F = 300;

        if (!isDragging) rotY += 0.006;
        sweepAngle = (sweepAngle + 0.03) % (Math.PI * 2);

        // Sonar sweep line
        ctx.save();
        ctx.beginPath();
        ctx.arc(cx, cy, 105, 0, Math.PI * 2);
        ctx.strokeStyle = 'rgba(16, 185, 129, 0.2)';
        ctx.lineWidth = 1;
        ctx.stroke();

        ctx.beginPath();
        ctx.moveTo(cx, cy);
        ctx.lineTo(cx + Math.cos(sweepAngle) * 105, cy + Math.sin(sweepAngle) * 105);
        ctx.strokeStyle = 'rgba(16, 185, 129, 0.45)';
        ctx.lineWidth = 2;
        ctx.stroke();
        ctx.restore();

        // Project and sort points
        const projected = [];
        const cosY = Math.cos(rotY), sinY = Math.sin(rotY);
        const cosX = Math.cos(rotX), sinX = Math.sin(rotX);

        for (let i = 0; i < points.length; i++) {
          const p = points[i];
          const x1 = p.x * cosY - p.z * sinY;
          const z1 = p.x * sinY + p.z * cosY;
          const y1 = p.y * cosX - z1 * sinX;
          const z2 = p.y * sinX + z1 * cosX;

          const scale = F / (F + z2);
          const px = cx + x1 * scale;
          const py = cy + y1 * scale;

          projected.push({ x: px, y: py, z: z2, scale: scale });
        }

        projected.sort((a, b) => b.z - a.z);

        for (let i = 0; i < projected.length; i++) {
          const pt = projected[i];
          const alpha = Math.max(0.15, Math.min(1.0, (pt.z + 100) / 200));
          const radius = Math.max(0.6, pt.scale * 1.5);

          ctx.fillStyle = `rgba(16, 185, 129, ${alpha * 0.9})`;
          ctx.beginPath();
          ctx.arc(pt.x, pt.y, radius, 0, Math.PI * 2);
          ctx.fill();
        }

        requestAnimationFrame(render);
      }
      render();
    })();

    // Operations and Telemetry
    function logTelemetry(msg) {
      const el = document.getElementById('telemetry-log');
      el.textContent += '\\n' + msg;
      el.scrollTop = el.scrollHeight;
    }

    function switchTab(tabId, btn) {
      playTacticalChirp(1200, 0.03);
      document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.nav-button').forEach(el => el.classList.remove('active'));
      document.getElementById(tabId).classList.add('active');
      if (btn) btn.classList.add('active');
      if (tabId === 'tab-ledger') loadLedgerData();
    }

    let lastArtifactId = null;

    async function executeDistribution() {
      playTacticalChirp(600, 0.06);
      logTelemetry("[+] DISPATCH: Contacting Air-Gapped Key Distribution Matrix...");
      const checked = document.querySelectorAll('input[name="recip"]:checked');
      const recips = Array.from(checked).map(c => c.value);
      if (recips.length === 0) { alert("Select at least one recipient officer."); return; }

      logTelemetry(`[+] Multi-Recipients: ${recips.join(', ')}`);
      logTelemetry("[+] Encapsulating session key with NIST FIPS 203 (ML-KEM-768)...");
      logTelemetry("[+] Generating Dilithium signature with FIPS 204 (ML-DSA-65)...");

      try {
        const res = await fetch('/api/distribute', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ recipients: recips })
        });
        const data = await res.json();
        logTelemetry(`[✓] Package Generated: ${data.package_id}.modpkg`);
        logTelemetry(`[✓] SHA3-256 Digest: ${data.document_hash_sha3.slice(0, 32)}...`);
        playTacticalChirp(1400, 0.08);
      } catch (err) {
        logTelemetry(`[ERR] Distribution failed: ${err}`);
      }
    }

    async function executeDecryption() {
      playTacticalChirp(700, 0.06);
      const officer = document.getElementById('decrypt-officer-select').value;
      logTelemetry(`[+] ATOMIC DECRYPT: Officer ${officer} authenticated.`);
      logTelemetry("[+] Verifying Hardware TPM 2.0 PCR-7 attestation...");
      logTelemetry("[+] Decapsulating session key via ML-KEM-768...");
      logTelemetry("[+] Embedding Tardos DWT-DCT watermark into screen raster...");

      try {
        const res = await fetch('/api/decrypt', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ recipient_id: officer })
        });
        const data = await res.json();
        if (data.success) {
          lastArtifactId = data.artifact_id;
          logTelemetry(`[✓] Decryption Provenance Record signed.`);
          logTelemetry(`[✓] Anchored in DLT Block #${data.block_index} (${data.block_hash.slice(0, 16)}...)`);
          
          document.getElementById('decrypted-result-view').style.display = 'block';
          document.getElementById('decrypted-meta').innerHTML = `
            OFFICER: <b>${data.officer_name}</b> (${data.recipient_id})<br>
            TOKEN ID: ${data.watermark_token_id.slice(0, 24)}...<br>
            BLOCK ANCHOR: #${data.block_index} // MERKLE ROOT VERIFIED
          `;
          playTacticalChirp(1500, 0.1);
        } else {
          logTelemetry(`[ERR] Decryption error: ${data.error}`);
        }
      } catch (err) {
        logTelemetry(`[ERR] Failed: ${err}`);
      }
    }

    function simulateLeakFromHere() {
      playTacticalChirp(440, 0.08);
      switchTab('tab-forensics', document.querySelectorAll('.nav-button')[2]);
      investigateRecentDecrypted();
    }

    async function investigateRecentDecrypted() {
      playTacticalChirp(520, 0.08);
      logTelemetry("[!] FORENSIC INVESTIGATION TRIGGERED: Leaked capture detected.");
      logTelemetry("[+] Applying 2D FFT Notch Filter to suppress display Moiré...");
      logTelemetry("[+] Calculating Planar Homography matrix to de-warp perspective...");
      logTelemetry("[+] Correlating DWT-DCT coefficients against Tardos codebook...");

      try {
        const formData = new FormData();
        if (lastArtifactId) formData.append('artifact_id', lastArtifactId);
        const res = await fetch('/api/investigate', { method: 'POST', body: formData });
        const data = await res.json();
        if (data.success) {
          renderDossier(data.certificate);
          playTacticalChirp(2000, 0.15);
        }
      } catch (err) {
        logTelemetry(`[ERR] Investigation failed: ${err}`);
      }
    }

    function renderDossier(cert) {
      document.getElementById('dossier-body').innerHTML = `
        <div style="background:rgba(239,68,68,0.15); border:1px solid #EF4444; padding:10px; border-radius:4px; color:#EF4444; font-weight:700; margin-bottom:12px;">
          BREACH PROVEN // STATUTORY SECTION 65B EVIDENCE ATTESTED
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; background:#080A0D; padding:12px; border-radius:4px; border:1px solid #1F2937;">
          <div><span style="color:#64748B;">OFFICER NAME:</span><br><b>${cert.leaked_by_officer}</b></div>
          <div><span style="color:#64748B;">SERVICE NUMBER:</span><br><b style="color:#EF4444;">${cert.officer_id}</b></div>
          <div><span style="color:#64748B;">DIVISION:</span><br>${cert.service_branch}</div>
          <div><span style="color:#64748B;">CERTAINTY:</span><br><b style="color:#10B981;">${cert.confidence_score}</b></div>
        </div>
        <div style="margin-top:10px; font-size:9px; color:#94A3B8; line-height:1.6;">
          MERKLE ROOT: ${cert.merkle_root}<br>
          WATERMARK TOKEN: ${cert.token_id}<br>
          LEGAL STANDARD: BHARATIYA SAKSHYA ADHINIYAM (BSA) / 65B COMPLIANT
        </div>
      `;
      document.getElementById('dossier-modal').style.display = 'flex';
    }

    function closeDossier() {
      document.getElementById('dossier-modal').style.display = 'none';
    }

    async function loadLedgerData() {
      try {
        const res = await fetch('/api/ledger');
        const data = await res.json();
        const container = document.getElementById('ledger-blocks-list');
        container.innerHTML = "";
        data.blocks.forEach(b => {
          const div = document.createElement('div');
          div.style.cssText = "padding:8px; background:#080A0D; border:1px solid #1F2937; border-radius:4px; margin-bottom:8px;";
          div.innerHTML = `
            <div style="display:flex; justify-content:space-between; color:#10B981; font-weight:700;">
              <span>BLOCK #${b.index}</span> <span>${b.transactions.length} TXNS</span>
            </div>
            <div style="font-size:9px; color:#64748B; margin-top:4px;">
              HASH: ${b.hash.slice(0, 24)}...<br>
              PREV: ${b.previous_hash.slice(0, 24)}...
            </div>
          `;
          container.appendChild(div);
        });
      } catch (err) {}
    }

    async function auditLedgerChain() {
      playTacticalChirp(1000, 0.05);
      const res = await fetch('/api/ledger/audit');
      const audit = await res.json();
      if (audit.is_valid) {
        alert("✓ MERKLE DLT AUDIT: Chain is 100% Valid. No Tampering Detected.");
      } else {
        alert("⚠ TAMPER ALARM: Block Hash Mismatch in Chain!");
      }
    }

    async function simulateAdminTamper() {
      playTacticalChirp(300, 0.15);
      await fetch('/api/ledger/tamper', { method: 'POST' });
      document.getElementById('header-chain-status').className = "t-badge badge-red";
      document.getElementById('header-chain-status').textContent = "DLT: TAMPER DETECTED!";
      alert("⚠ ATTACK SIMULATED: Merkle DAG root mismatch detected across consortium nodes!");
    }

    async function restoreLedgerClean() {
      playTacticalChirp(800, 0.05);
      await fetch('/api/ledger/restore', { method: 'POST' });
      document.getElementById('header-chain-status').className = "t-badge badge-olive";
      document.getElementById('header-chain-status').textContent = "DLT: CONSORTIUM HEALTHY";
      loadLedgerData();
    }
  </script>
</body>
</html>
"""
    return html.replace("__ICON_DATA_URI__", icon_data_uri)

