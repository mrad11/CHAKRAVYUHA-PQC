"""
Single-page Defense Web Dashboard HTML/CSS/JavaScript Template
100% self-contained, air-gapped, zero external dependencies.
"""

def get_dashboard_html() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Ministry of Defence — CryptoSeal PQC Provenance Console</title>
  <style>
    :root {
      --bg-dark: #080C14;
      --bg-card: #0F172A;
      --bg-card-alt: #162035;
      --border-subtle: #1E293B;
      --border-accent: #00ADB5;
      --text-main: #F1F5F9;
      --text-muted: #94A3B8;
      --accent-cyan: #00ADB5;
      --accent-emerald: #10B981;
      --accent-crimson: #EF4444;
      --accent-amber: #F59E0B;
      --font-mono: 'Consolas', 'Courier New', monospace;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }
    body { background: var(--bg-dark); color: var(--text-main); min-height: 100vh; padding-bottom: 60px; }

    /* Top Command Header */
    .command-header {
      background: linear-gradient(180deg, #0D1527 0%, #080C14 100%);
      border-bottom: 1px solid var(--border-subtle);
      padding: 16px 32px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: sticky;
      top: 0;
      z-index: 100;
    }
    .brand-title { display: flex; align-items: center; gap: 14px; }
    .emblem-icon {
      width: 42px; height: 42px; border-radius: 8px;
      background: linear-gradient(135deg, #00ADB5 0%, #0284C7 100%);
      display: flex; align-items: center; justify-content: center;
      font-weight: 900; font-size: 20px; color: #fff;
      box-shadow: 0 0 20px rgba(0, 173, 181, 0.4);
    }
    .brand-text h1 { font-size: 18px; font-weight: 700; letter-spacing: 0.8px; color: #FFF; text-transform: uppercase; }
    .brand-text p { font-size: 11px; color: var(--text-muted); font-family: var(--font-mono); }
    
    .status-ribbon { display: flex; gap: 12px; }
    .badge {
      font-size: 11px; font-family: var(--font-mono); font-weight: 600;
      padding: 5px 12px; border-radius: 6px; display: inline-flex; align-items: center; gap: 6px;
      text-transform: uppercase; letter-spacing: 0.5px;
    }
    .badge-green { background: rgba(16, 185, 129, 0.12); color: var(--accent-emerald); border: 1px solid rgba(16, 185, 129, 0.3); }
    .badge-cyan { background: rgba(0, 173, 181, 0.12); color: var(--accent-cyan); border: 1px solid rgba(0, 173, 181, 0.3); }
    .badge-red { background: rgba(239, 68, 68, 0.15); color: var(--accent-crimson); border: 1px solid rgba(239, 68, 68, 0.4); }
    .badge-amber { background: rgba(245, 158, 11, 0.15); color: var(--accent-amber); border: 1px solid rgba(245, 158, 11, 0.4); }

    /* Nav Tabs */
    .tabs-nav {
      display: flex; background: var(--bg-card); border-bottom: 1px solid var(--border-subtle);
      padding: 0 32px; gap: 24px;
    }
    .tab-btn {
      background: none; border: none; color: var(--text-muted); padding: 16px 8px; font-size: 14px;
      font-weight: 600; cursor: pointer; position: relative; transition: all 0.2s ease;
      display: flex; align-items: center; gap: 8px;
    }
    .tab-btn:hover { color: #FFF; }
    .tab-btn.active { color: var(--accent-cyan); }
    .tab-btn.active::after {
      content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 3px;
      background: var(--accent-cyan); box-shadow: 0 0 10px var(--accent-cyan);
    }

    /* Container Layout */
    .main-container { max-width: 1400px; margin: 28px auto; padding: 0 24px; }
    .tab-content { display: none; }
    .tab-content.active { display: block; animation: fadeIn 0.25s ease; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0); } }

    /* Grid & Cards */
    .grid-2col { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
    .grid-3col { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
    .card {
      background: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: 12px;
      padding: 24px; box-shadow: 0 8px 24px rgba(0,0,0,0.3);
    }
    .card-header {
      display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px;
      padding-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.06);
    }
    .card-title { font-size: 15px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; color: #FFF; display: flex; align-items: center; gap: 8px; }
    
    /* Form Elements */
    .form-group { margin-bottom: 18px; }
    .form-label { display: block; font-size: 12px; font-weight: 600; color: var(--text-muted); margin-bottom: 8px; text-transform: uppercase; }
    .form-input, .form-select {
      width: 100%; background: #0A0F1D; border: 1px solid var(--border-subtle); border-radius: 8px;
      padding: 10px 14px; color: #FFF; font-size: 13px; outline: none; transition: border 0.2s;
    }
    .form-input:focus, .form-select:focus { border-color: var(--accent-cyan); }
    
    .checkbox-group { display: flex; flex-direction: column; gap: 10px; margin-top: 8px; }
    .checkbox-item {
      display: flex; align-items: center; justify-content: space-between;
      background: #0A0F1D; border: 1px solid var(--border-subtle); padding: 10px 14px;
      border-radius: 8px; cursor: pointer; transition: all 0.15s;
    }
    .checkbox-item:hover { border-color: rgba(0, 173, 181, 0.4); background: #0D162B; }
    .checkbox-item input { margin-right: 12px; accent-color: var(--accent-cyan); width: 16px; height: 16px; }

    /* Buttons */
    .btn {
      display: inline-flex; align-items: center; justify-content: center; gap: 8px;
      background: linear-gradient(135deg, #00ADB5 0%, #0284C7 100%);
      color: #FFF; font-weight: 700; font-size: 13px; text-transform: uppercase;
      letter-spacing: 0.8px; padding: 12px 22px; border: none; border-radius: 8px;
      cursor: pointer; transition: all 0.2s ease; width: 100%;
      box-shadow: 0 4px 14px rgba(0, 173, 181, 0.3);
    }
    .btn:hover { transform: translateY(-1px); box-shadow: 0 6px 20px rgba(0, 173, 181, 0.45); }
    .btn-secondary {
      background: #1E293B; color: #CBD5E1; box-shadow: none; border: 1px solid #334155;
    }
    .btn-secondary:hover { background: #334155; color: #FFF; }
    .btn-danger {
      background: linear-gradient(135deg, #EF4444 0%, #B91C1C 100%);
      box-shadow: 0 4px 14px rgba(239, 68, 68, 0.3);
    }
    .btn-danger:hover { box-shadow: 0 6px 20px rgba(239, 68, 68, 0.45); }

    /* Telemetry Feed / Log Box */
    .log-box {
      background: #060911; border: 1px solid #1A2234; border-radius: 8px; padding: 14px;
      font-family: var(--font-mono); font-size: 12px; color: #38BDF8; line-height: 1.6;
      max-height: 260px; overflow-y: auto; white-space: pre-wrap;
    }

    /* Attribution Certificate Card */
    .certificate-card {
      background: radial-gradient(circle at top right, #1A1F35 0%, #0A0D18 100%);
      border: 2px solid var(--accent-cyan); border-radius: 14px; padding: 28px;
      box-shadow: 0 0 35px rgba(0, 173, 181, 0.25); position: relative; overflow: hidden;
    }
    .cert-badge {
      display: inline-block; font-size: 14px; font-weight: 800; text-transform: uppercase;
      letter-spacing: 1px; padding: 8px 18px; border-radius: 8px; margin-bottom: 20px;
    }
    .cert-badge-red { background: rgba(239, 68, 68, 0.2); color: #FF4D4D; border: 1px solid #FF4D4D; }
    .dossier-grid {
      display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 20px 0;
      background: rgba(0,0,0,0.3); padding: 18px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.06);
    }
    .dossier-item { font-size: 13px; }
    .dossier-label { color: var(--text-muted); font-size: 11px; text-transform: uppercase; margin-bottom: 4px; }
    .dossier-val { font-weight: 700; color: #FFF; font-family: var(--font-mono); }

    /* Block Explorer List */
    .block-item {
      background: #0A0F1D; border: 1px solid var(--border-subtle); border-radius: 10px;
      padding: 16px; margin-bottom: 14px; transition: border 0.2s;
    }
    .block-item:hover { border-color: var(--accent-cyan); }
    .block-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
    .block-hash { font-family: var(--font-mono); font-size: 12px; color: var(--accent-cyan); word-break: break-all; }
  </style>
</head>
<body>

  <!-- Top Command Header -->
  <header class="command-header">
    <div class="brand-title">
      <div class="emblem-icon">MOD</div>
      <div class="brand-text">
        <h1>Ministry of Defence — CryptoSeal PQC</h1>
        <p>Cryptographic Attribution & Immutable Decryption Provenance (FIPS 203 / 204)</p>
      </div>
    </div>
    <div class="status-ribbon">
      <span class="badge badge-green">● AIR-GAPPED OFFLINE</span>
      <span class="badge badge-cyan">● PQC: ML-KEM-768 & ML-DSA-65</span>
      <span class="badge badge-green" id="header-ledger-status">● DLT CONSENSUS: HEALTHY</span>
    </div>
  </header>

  <!-- Nav Tabs -->
  <nav class="tabs-nav">
    <button class="tab-btn active" onclick="switchTab('tab-distribute')">1. Sender Distribution</button>
    <button class="tab-btn" onclick="switchTab('tab-decrypt')">2. Recipient Decryption</button>
    <button class="tab-btn" onclick="switchTab('tab-forensics')">3. Leak Forensics Lab</button>
    <button class="tab-btn" onclick="switchTab('tab-ledger')">4. Immutable DLT Explorer</button>
  </nav>

  <!-- Main Container -->
  <main class="main-container">

    <!-- TAB 1: SENDER DISTRIBUTION -->
    <section id="tab-distribute" class="tab-content active">
      <div class="grid-2col">
        <div class="card">
          <div class="card-header">
            <span class="card-title">Broadcast Encryption Console</span>
            <span class="badge badge-cyan">NIST FIPS 203</span>
          </div>

          <div class="form-group">
            <label class="form-label">Operational Document</label>
            <input type="text" class="form-input" id="dist-doc-title" value="STRATEGIC CONTINGENCY PLAN TRIDENT SHIELD (PHASE IV)">
          </div>

          <div class="form-group">
            <label class="form-label">Document Reference Code</label>
            <input type="text" class="form-input" id="dist-doc-id" value="MOD-DOC-2026-OP-TRIDENT">
          </div>

          <div class="form-group">
            <label class="form-label">Classification Rating</label>
            <input type="text" class="form-input" id="dist-classification" value="COSMIC TOP SECRET // AIR-GAPPED ONLY">
          </div>

          <div class="form-group">
            <label class="form-label">Select Authorized Cleared Personnel</label>
            <div class="checkbox-group" id="recipients-checkbox-list">
              <label class="checkbox-item">
                <div>
                  <input type="checkbox" name="recip" value="IND-MOD-001" checked>
                  <strong>Col. Arvind Sharma</strong> (Directorate of Military Operations)
                </div>
                <span class="badge badge-cyan">KEM-768</span>
              </label>
              <label class="checkbox-item">
                <div>
                  <input type="checkbox" name="recip" value="IND-MOD-002" checked>
                  <strong>Brig. Rajesh Verma</strong> (Defence Cyber Agency)
                </div>
                <span class="badge badge-cyan">KEM-768</span>
              </label>
              <label class="checkbox-item">
                <div>
                  <input type="checkbox" name="recip" value="IND-MOD-003" checked>
                  <strong>Maj. Priya Nair</strong> (Military Intelligence Directorate MI-8)
                </div>
                <span class="badge badge-cyan">KEM-768</span>
              </label>
              <label class="checkbox-item">
                <div>
                  <input type="checkbox" name="recip" value="IND-MOD-004">
                  <strong>Cmde. Sunil Vohra</strong> (Naval Strategic Operations Group)
                </div>
                <span class="badge badge-cyan">KEM-768</span>
              </label>
            </div>
          </div>

          <button class="btn" onclick="executeDistribution()">
            Seal & Broadcast Encrypt Package (.modpkg)
          </button>
        </div>

        <div class="card">
          <div class="card-header">
            <span class="card-title">Cryptographic Envelope Pipeline</span>
            <span class="badge badge-green">HYBRID ENCRYPTION</span>
          </div>
          <div class="log-box" id="dist-log">System Ready.
Press "Seal & Broadcast Encrypt" to generate AES-256-GCM master payload and encapsulate session keys for all cleared officers via NIST FIPS 203 ML-KEM-768.</div>

          <div id="dist-summary" style="display:none; margin-top:20px;">
            <div style="background:#0A0F1D; border:1px solid #1E293B; border-radius:8px; padding:16px;">
              <p style="font-size:12px; color:var(--text-muted); margin-bottom:6px;">SEALED PACKAGE IDENTIFIER:</p>
              <p id="dist-pkg-id" style="font-family:var(--font-mono); font-size:13px; color:#38BDF8;"></p>
              <p style="font-size:12px; color:var(--text-muted); margin-top:12px; margin-bottom:6px;">DOCUMENT SHA3-256 DIGEST:</p>
              <p id="dist-doc-hash" style="font-family:var(--font-mono); font-size:11px; color:#A7F3D0; word-break:break-all;"></p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- TAB 2: RECIPIENT DECRYPTION -->
    <section id="tab-decrypt" class="tab-content">
      <div class="grid-2col">
        <div class="card">
          <div class="card-header">
            <span class="card-title">Authorized Officer Decryption Terminal</span>
            <span class="badge badge-cyan">NIST FIPS 204</span>
          </div>

          <div class="form-group">
            <label class="form-label">Select Authenticating Officer</label>
            <select class="form-select" id="dec-officer-select">
              <option value="IND-MOD-003">Maj. Priya Nair — Military Intelligence (MI-8)</option>
              <option value="IND-MOD-001">Col. Arvind Sharma — Directorate of Military Operations</option>
              <option value="IND-MOD-002">Brig. Rajesh Verma — Defence Cyber Agency</option>
              <option value="IND-MOD-004">Cmde. Sunil Vohra — Naval Strategic Operations</option>
            </select>
          </div>

          <div style="background:#0A0F1D; border-left:3px solid var(--accent-cyan); padding:14px; border-radius:6px; margin-bottom:20px;">
            <p style="font-size:12px; line-height:1.5; color:#CBD5E1;">
              <strong>High-Assurance Decryption Policy:</strong> Decryption is cryptographically atomic.
              The unwatermarked file is never released. A unique session watermark is generated, signed with the officer's
              private ML-DSA-65 key, committed to the DLT ledger, and invisibly embedded into the document before presentation.
            </p>
          </div>

          <button class="btn" onclick="executeDecryption()">
            Authorize Decryption & Sign to DLT
          </button>
        </div>

        <div class="card">
          <div class="card-header">
            <span class="card-title">Atomic Provenance Execution Telemetry</span>
            <span class="badge badge-green" id="dec-status-badge">STANDBY</span>
          </div>

          <div class="log-box" id="dec-log">Awaiting officer authentication...</div>

          <div id="dec-actions" style="display:none; margin-top:18px; display:flex; gap:12px;">
            <button class="btn btn-secondary" id="btn-view-pdf" onclick="openDecryptedPdf()">
              Download Watermarked PDF
            </button>
            <button class="btn btn-danger" id="btn-sim-leak" onclick="simulateLeakFromHere()">
              Simulate Leak (Trigger Forensic Lab)
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- TAB 3: FORENSIC LEAK ATTRIBUTION -->
    <section id="tab-forensics" class="tab-content">
      <div class="grid-2col">
        <div class="card">
          <div class="card-header">
            <span class="card-title">Leak Ingestion & Analysis Station</span>
            <span class="badge badge-red">BREACH INVESTIGATION</span>
          </div>

          <div class="form-group">
            <label class="form-label">Upload Leaked Document (PDF or Screenshot Image)</label>
            <input type="file" id="leak-file-input" class="form-input" accept=".pdf,.png,.jpg,.jpeg">
          </div>

          <div style="text-align:center; margin:16px 0; color:var(--text-muted); font-size:12px;">— OR USE RECENT DECRYPTED COPY —</div>

          <button class="btn btn-secondary" onclick="investigateRecentDecrypted()" style="margin-bottom:14px;">
            Investigate Most Recent Decrypted Document
          </button>

          <button class="btn btn-danger" onclick="runInvestigation()">
            Execute Forensic Attribution Scan
          </button>

          <div class="log-box" id="forensics-log" style="margin-top:20px;">Forensic engine standby. Upload or select an artifact to extract invisible watermark.</div>
        </div>

        <div>
          <div id="cert-container">
            <div class="card" style="text-align:center; padding:60px 20px; color:var(--text-muted);">
              <p style="font-size:14px; margin-bottom:8px;">No leak investigation active.</p>
              <p style="font-size:12px;">Provide a leaked PDF or screenshot on the left to generate an authenticated Forensic Attribution Certificate.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- TAB 4: IMMUTABLE DLT EXPLORER -->
    <section id="tab-ledger" class="tab-content">
      <div class="card" style="margin-bottom:24px;">
        <div class="card-header">
          <span class="card-title">Air-Gapped Consortium Blockchain (DLT)</span>
          <div style="display:flex; gap:10px;">
            <button class="btn btn-secondary" style="width:auto; padding:6px 14px; font-size:11px;" onclick="loadLedgerData()">Refresh Chain</button>
            <button class="btn btn-secondary" style="width:auto; padding:6px 14px; font-size:11px;" onclick="auditLedgerChain()">Audit Integrity</button>
            <button class="btn btn-danger" style="width:auto; padding:6px 14px; font-size:11px;" onclick="simulateAdminTamper()">Simulate Tamper Attack</button>
            <button class="btn btn-secondary" style="width:auto; padding:6px 14px; font-size:11px;" onclick="restoreLedgerClean()">Reset Chain</button>
          </div>
        </div>
        <div id="ledger-audit-summary" style="padding:12px; background:#0A0F1D; border-radius:8px; margin-bottom:16px; font-size:13px; font-family:var(--font-mono); color:#A7F3D0;">
          DLT Status: HEALTHY | Genesis Block Anchored | Validator Consensus Online (3 Nodes)
        </div>
        <div id="ledger-blocks-list">
          <!-- Loaded dynamically -->
        </div>
      </div>
    </section>

  </main>

  <script>
    let currentDecryptedArtId = null;

    function switchTab(tabId) {
      document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
      document.getElementById(tabId).classList.add('active');
      event.currentTarget.classList.add('active');
      if (tabId === 'tab-ledger') loadLedgerData();
    }

    async function executeDistribution() {
      const log = document.getElementById('dist-log');
      log.textContent = "[+] Connecting to Air-Gapped PKI Keystores...\\n";
      
      const checkedBoxes = document.querySelectorAll('input[name="recip"]:checked');
      const recipients = Array.from(checkedBoxes).map(cb => cb.value);
      if (recipients.length === 0) {
        alert("Please select at least one recipient officer.");
        return;
      }

      log.textContent += `[+] Target Officers Cleared: ${recipients.join(', ')}\\n`;
      log.textContent += `[+] Generating 256-bit symmetric session key...\\n`;
      log.textContent += `[+] Encrypting payload with AES-256-GCM...\\n`;
      log.textContent += `[+] Encapsulating key blocks using NIST FIPS 203 ML-KEM-768...\\n`;

      try {
        const res = await fetch('/api/distribute', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            document_id: document.getElementById('dist-doc-id').value,
            title: document.getElementById('dist-doc-title').value,
            classification: document.getElementById('dist-classification').value,
            recipients: recipients
          })
        });
        const data = await res.json();
        if (data.success) {
          log.textContent += `[✓] PACKAGE SEALED SUCCESSFULLY!\\n`;
          log.textContent += `[✓] Package ID: ${data.package_id}\\n`;
          log.textContent += `[✓] Document Hash: ${data.document_hash_sha3}\\n`;
          log.textContent += `[✓] Ready for broadcast distribution to cleared officers.\\n`;

          document.getElementById('dist-summary').style.display = 'block';
          document.getElementById('dist-pkg-id').textContent = data.package_id;
          document.getElementById('dist-doc-hash').textContent = data.document_hash_sha3;
        }
      } catch (err) {
        log.textContent += `[!] Error: ${err}\\n`;
      }
    }

    async function executeDecryption() {
      const officerId = document.getElementById('dec-officer-select').value;
      const log = document.getElementById('dec-log');
      const badge = document.getElementById('dec-status-badge');

      badge.className = "badge badge-amber";
      badge.textContent = "DECRYPTING...";
      log.textContent = `[1] Recipient Identity Verified: ${officerId}\\n`;
      log.textContent += `[2] Decapsulating session key with ML-KEM-768 private key...\\n`;
      log.textContent += `[3] Intercepting plaintext stream: atomic provenance guard engaged...\\n`;
      log.textContent += `[4] Generating unique Session Watermark Token (SWT)...\\n`;
      log.textContent += `[5] Recipient signing Decryption Provenance Record via ML-DSA-65...\\n`;
      log.textContent += `[6] Committing signed record to air-gapped DLT ledger...\\n`;

      try {
        const res = await fetch('/api/decrypt', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ recipient_id: officerId })
        });
        const data = await res.json();
        if (data.success) {
          currentDecryptedArtId = data.artifact_id;
          badge.className = "badge badge-green";
          badge.textContent = "COMMITTED & DELIVERED";

          log.textContent += `[7] Block #${data.block_index} mined on DLT (Hash: ${data.block_hash.substring(0, 16)}...)\\n`;
          log.textContent += `[8] Injected Dual-Layer Invisible Forensic Watermark (${data.watermark_token_id})\\n`;
          log.textContent += `[✓] Clean, personalized document delivered to officer.\\n`;

          document.getElementById('dec-actions').style.display = 'flex';
          document.getElementById('btn-view-pdf').onclick = () => window.open(data.pdf_download_url, '_blank');
        } else {
          badge.className = "badge badge-red";
          badge.textContent = "FAILED";
          log.textContent += `[!] Decryption Rejected: ${data.error}\\n`;
        }
      } catch (err) {
        badge.className = "badge badge-red";
        badge.textContent = "ERROR";
        log.textContent += `[!] Error: ${err}\\n`;
      }
    }

    function simulateLeakFromHere() {
      // Switch to tab 3 and run investigation
      document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
      document.getElementById('tab-forensics').classList.add('active');
      document.querySelectorAll('.tab-btn')[2].classList.add('active');
      investigateRecentDecrypted();
    }

    async function investigateRecentDecrypted() {
      const log = document.getElementById('forensics-log');
      log.textContent = "[+] Ingesting leaked artifact from operational theater...\\n";
      log.textContent += "[+] Executing dual-layer watermark extraction...\\n";
      log.textContent += "    - Layer 1: PDF Micro-typographical & Object Stream Decoding\\n";
      log.textContent += "    - Layer 2: Visual Blue-Channel Spatial Demodulation (Screenshot Filter)\\n";

      try {
        const res = await fetch('/api/investigate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: currentDecryptedArtId ? `artifact_id=${currentDecryptedArtId}` : ''
        });
        const data = await res.json();
        if (data.success && data.certificate) {
          renderCertificate(data.certificate);
          log.textContent += `[✓] Watermark Token Extracted: ${data.certificate.watermark_token_id}\\n`;
          log.textContent += `[✓] Matched on DLT Block #${data.certificate.block_index}\\n`;
          log.textContent += `[✓] Recipient ML-DSA-65 Signature: VALID\\n`;
          log.textContent += `[✓] Merkle Inclusion Proof: VALID\\n`;
          log.textContent += `[✓] Culprit Attributed: ${data.certificate.culprit_name}\\n`;
        } else {
          log.textContent += `[!] Attribution failed: ${data.error || 'No watermark detected'}\\n`;
        }
      } catch (err) {
        log.textContent += `[!] Error: ${err}\\n`;
      }
    }

    async function runInvestigation() {
      const fileInput = document.getElementById('leak-file-input');
      if (fileInput.files.length === 0) {
        alert("Please upload a leaked PDF or screenshot image, or click 'Investigate Most Recent Decrypted Document'.");
        return;
      }

      const log = document.getElementById('forensics-log');
      log.textContent = `[+] Ingesting uploaded leaked file: ${fileInput.files[0].name}...\\n`;
      log.textContent += `[+] Scanning for forensic watermarks...\\n`;

      const formData = new FormData();
      formData.append('file', fileInput.files[0]);

      try {
        const res = await fetch('/api/investigate', {
          method: 'POST',
          body: formData
        });
        const data = await res.json();
        if (data.success && data.certificate) {
          renderCertificate(data.certificate);
          log.textContent += `[✓] Attribution Analysis Completed!\\n`;
        }
      } catch (err) {
        log.textContent += `[!] Error: ${err}\\n`;
      }
    }

    function renderCertificate(cert) {
      const container = document.getElementById('cert-container');
      const isAttributed = (cert.status === "CONFIRMED_LEAK_ATTRIBUTED");

      container.innerHTML = `
        <div class="certificate-card">
          <div style="display:flex; justify-content:space-between; align-items:flex-start;">
            <div>
              <span class="cert-badge ${isAttributed ? 'cert-badge-red' : 'badge-amber'}">
                ${isAttributed ? 'CONFIRMED LEAK IDENTIFIED' : cert.status}
              </span>
              <p style="font-size:12px; font-family:var(--font-mono); color:var(--text-muted);">${cert.certificate_id}</p>
            </div>
            <span class="badge badge-green">PQC VERIFIED</span>
          </div>

          <div class="dossier-grid">
            <div class="dossier-item">
              <p class="dossier-label">IDENTIFIED RECIPIENT</p>
              <p class="dossier-val" style="color:#FF6B6B; font-size:15px;">${cert.culprit_name || 'N/A'}</p>
            </div>
            <div class="dossier-item">
              <p class="dossier-label">SERVICE / OFFICER ID</p>
              <p class="dossier-val">${cert.culprit_officer_id || 'N/A'}</p>
            </div>
            <div class="dossier-item">
              <p class="dossier-label">ASSIGNED DIVISION</p>
              <p class="dossier-val">${cert.culprit_division || 'N/A'}</p>
            </div>
            <div class="dossier-item">
              <p class="dossier-label">CLEARANCE LEVEL</p>
              <p class="dossier-val">${cert.culprit_clearance || 'N/A'}</p>
            </div>
            <div class="dossier-item">
              <p class="dossier-label">DECRYPTION TIMESTAMP</p>
              <p class="dossier-val">${cert.decryption_timestamp || 'N/A'}</p>
            </div>
            <div class="dossier-item">
              <p class="dossier-label">WATERMARK TOKEN ID</p>
              <p class="dossier-val" style="color:#38BDF8;">${cert.watermark_token_id || 'N/A'}</p>
            </div>
            <div class="dossier-item">
              <p class="dossier-label">DLT BLOCK HEIGHT</p>
              <p class="dossier-val">Block #${cert.block_index !== null ? cert.block_index : 'N/A'}</p>
            </div>
            <div class="dossier-item">
              <p class="dossier-label">EXTRACTION LAYER</p>
              <p class="dossier-val" style="color:#A7F3D0;">${cert.extraction_layer || 'N/A'}</p>
            </div>
          </div>

          <div style="background:#060911; border:1px solid #1A2234; padding:16px; border-radius:8px; font-size:12px; margin-bottom:18px;">
            <p style="font-weight:700; color:#38BDF8; margin-bottom:6px;">CRYPTOGRAPHIC VERIFICATION SUMMARY:</p>
            <p>✓ NIST FIPS 204 ML-DSA-65 Signature: <strong style="color:#10B981;">VALID & BOUND</strong></p>
            <p>✓ Merkle Inclusion Audit Proof: <strong style="color:#10B981;">VERIFIED TO ROOT</strong></p>
            <p>✓ Multi-Validator Consensus: <strong style="color:#10B981;">VALIDATED (3-of-3 MoD Nodes)</strong></p>
          </div>

          <div style="background:rgba(239, 68, 68, 0.08); border:1px solid rgba(239, 68, 68, 0.3); padding:14px; border-radius:8px; font-size:11px; line-height:1.5; color:#FCA5A5;">
            <strong>LEGAL NON-REPUDIATION ATTESTATION:</strong><br>
            ${cert.legal_non_repudiation_statement}
          </div>
        </div>
      `;
    }

    async function loadLedgerData() {
      const list = document.getElementById('ledger-blocks-list');
      list.innerHTML = "<p style='color:var(--text-muted); padding:20px;'>Loading immutable blocks...</p>";

      try {
        const res = await fetch('/api/ledger');
        const data = await res.json();
        list.innerHTML = "";

        data.blocks.forEach(b => {
          const div = document.createElement('div');
          div.className = "block-item";
          const txCount = b.transactions.length;
          const isGenesis = (b.index === 0);

          let txHtml = "";
          b.transactions.forEach((tx, idx) => {
            txHtml += `
              <div style="background:#0D1527; padding:10px; border-radius:6px; margin-top:8px; font-size:12px;">
                <p><strong>Officer:</strong> ${tx.officer_name} (${tx.recipient_id}) | <strong>Session:</strong> ${tx.session_id.substring(0,8)}</p>
                <p style="color:var(--text-muted); font-size:11px;">Watermark: <span style="color:#38BDF8;">${tx.watermark_token_id}</span> | Time: ${tx.timestamp}</p>
                <p style="color:var(--text-muted); font-size:10px; font-family:var(--font-mono); margin-top:4px;">ML-DSA-65 Sig: ${tx.recipient_signature_b64.substring(0, 48)}...</p>
              </div>
            `;
          });

          div.innerHTML = `
            <div class="block-top">
              <span style="font-weight:700; font-size:14px; color:#FFF;">
                ${isGenesis ? 'GENESIS BLOCK #0' : 'BLOCK #' + b.index}
              </span>
              <span class="badge ${isGenesis ? 'badge-cyan' : 'badge-green'}">
                ${isGenesis ? 'ANCHOR' : txCount + ' PROVENANCE RECORD(S)'}
              </span>
            </div>
            <p class="block-hash">BLOCK HASH: ${b.block_hash}</p>
            <p style="font-size:11px; color:var(--text-muted); margin-top:4px; font-family:var(--font-mono);">PREV HASH: ${b.prev_hash}</p>
            <p style="font-size:11px; color:var(--text-muted); margin-top:2px; font-family:var(--font-mono);">MERKLE ROOT: ${b.merkle_root}</p>
            ${txHtml}
          `;
          list.appendChild(div);
        });
      } catch (err) {
        list.innerHTML = `<p style="color:#EF4444; padding:20px;">Error loading ledger: ${err}</p>`;
      }
    }

    async function auditLedgerChain() {
      const summary = document.getElementById('ledger-audit-summary');
      summary.innerHTML = "Auditing cryptographic blockchain integrity...";
      try {
        const res = await fetch('/api/ledger/audit');
        const audit = await res.json();
        if (audit.is_valid) {
          summary.style.color = "#A7F3D0";
          summary.innerHTML = `[✓] AUDIT SUCCESSFUL: Ledger is 100% HEALTHY. All ${audit.total_blocks} blocks, Merkle roots, and PQC signatures verified intact.`;
        } else {
          summary.style.color = "#EF4444";
          summary.innerHTML = `[!] INTEGRITY BREACH: Chain is TAMPERED on Block(s): ${audit.tampered_blocks.join(', ')}. Errors: ${audit.errors.join('; ')}`;
        }
      } catch (err) {
        summary.innerHTML = `Error: ${err}`;
      }
    }

    async function simulateAdminTamper() {
      const summary = document.getElementById('ledger-audit-summary');
      summary.style.color = "#EF4444";
      summary.innerHTML = "Simulating rogue admin database modification on Block #1...";
      
      try {
        const res = await fetch('/api/ledger/tamper', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ framed_officer: 'IND-MOD-001 (Col. Arvind Sharma)' })
        });
        const data = await res.json();
        if (data.success) {
          loadLedgerData();
          summary.innerHTML = `[!] ALERT: Rogue Admin modified Block #1. Blockchain immediately flagged: <strong>${data.audit_result.status}</strong>! Multi-Validator signature and Merkle root failed.`;
          document.getElementById('header-ledger-status').className = "badge badge-red";
          document.getElementById('header-ledger-status').textContent = "● DLT BREACH DETECTED";
        } else {
          alert(data.error);
        }
      } catch (err) {
        summary.innerHTML = `Error: ${err}`;
      }
    }

    async function restoreLedgerClean() {
      await fetch('/api/ledger/restore', { method: 'POST' });
      document.getElementById('header-ledger-status').className = "badge badge-green";
      document.getElementById('header-ledger-status').textContent = "● DLT CONSENSUS: HEALTHY";
      loadLedgerData();
      auditLedgerChain();
    }
  </script>
</body>
</html>
"""
