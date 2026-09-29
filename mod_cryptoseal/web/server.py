"""
CryptoSeal PQC Web Server
Air-Gapped Defence Operations & Forensic Attribution Console
Ministry of Defence — Problem Statement 237
"""

import os
import io
import json
import base64
import uuid
from typing import Dict, Any

from bottle import Bottle, request, response, static_file, HTTPResponse
import pymupdf
from PIL import Image

from ..crypto.pki import AirGappedPKI
from ..crypto.pqc import PQCKeyManager, HashUtil
from ..ledger.chain import AirGappedLedger
from ..engine.distributor import DocumentDistributor
from ..engine.decryption_guard import DecryptionGuard
from ..engine.forensics import ForensicInvestigator
from sample_documents.generate_sample_pdf import generate_defence_sample_pdf

app = Bottle()

# Base working directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "web_workspace")
UPLOADS_DIR = os.path.join(DATA_DIR, "artifacts")
os.makedirs(UPLOADS_DIR, exist_ok=True)

# Initialize PKI & Ledger
pki = AirGappedPKI(DATA_DIR)
pki.seed_default_defence_personnel()
ledger = AirGappedLedger(DATA_DIR)

# Ensure sample document exists
sample_pdf_path = os.path.join(DATA_DIR, "DEFENCE_OPERATION_TRIDENT.pdf")
if not os.path.exists(sample_pdf_path):
    generate_defence_sample_pdf(sample_pdf_path)

# In-memory session packages cache
latest_package = None
decrypted_artifacts = {}  # artifact_id -> bytes


def enable_cors():
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Origin, Accept, Content-Type, X-Requested-With"


@app.hook("after_request")
def after_request():
    enable_cors()


@app.route("/api/status", method=["GET", "OPTIONS"])
def get_status():
    if request.method == "OPTIONS":
        return {}
    audit = ledger.verify_chain()
    return {
        "status": "OPERATIONAL",
        "air_gapped": True,
        "organization": "Ministry of Defence",
        "cloud_kms_dependency": False,
        "public_blockchain_dependency": False,
        "pqc_kem": "NIST FIPS 203 (ML-KEM-768)",
        "pqc_dsa": "NIST FIPS 204 (ML-DSA-65)",
        "total_officers": len(pki.officers),
        "total_blocks": len(ledger.chain),
        "total_records": sum(len(b.transactions) for b in ledger.chain),
        "ledger_health": audit["status"],
        "is_chain_valid": audit["is_valid"],
    }


@app.route("/api/officers", method=["GET", "OPTIONS"])
def get_officers():
    if request.method == "OPTIONS":
        return {}
    return {"officers": pki.get_public_directory()}


@app.route("/api/distribute", method=["POST", "OPTIONS"])
def api_distribute():
    global latest_package
    if request.method == "OPTIONS":
        return {}
    data = request.json or {}
    
    recipients = data.get("recipients", ["IND-MOD-001", "IND-MOD-002", "IND-MOD-003"])
    doc_id = data.get("document_id", "MOD-OP-TRIDENT-2026")
    title = data.get("title", "STRATEGIC CONTINGENCY PLAN TRIDENT")
    classification = data.get("classification", "COSMIC TOP SECRET // RESTRICTED")
    sender = data.get("sender_id", "JOINT-CHIEFS-OF-STAFF")

    # Read base document
    with open(sample_pdf_path, "rb") as f:
        doc_bytes = f.read()

    distributor = DocumentDistributor(pki)
    package = distributor.create_package(
        document_bytes=doc_bytes,
        document_id=doc_id,
        document_title=title,
        sender_id=sender,
        recipient_ids=recipients,
        classification_level=classification,
    )
    latest_package = package

    # Save package to disk
    pkg_path = os.path.join(UPLOADS_DIR, f"{package.package_id}.modpkg")
    distributor.save_package_to_file(package, pkg_path)

    return {
        "success": True,
        "package_id": package.package_id,
        "document_id": package.document_id,
        "document_hash_sha3": package.document_hash_sha3,
        "recipients_count": len(package.recipient_blocks),
        "recipient_names": [b.officer_name for b in package.recipient_blocks],
        "timestamp": package.timestamp,
        "classification": package.classification_level,
    }


@app.route("/api/decrypt", method=["POST", "OPTIONS"])
def api_decrypt():
    global latest_package, decrypted_artifacts
    if request.method == "OPTIONS":
        return {}
    data = request.json or {}
    recipient_id = data.get("recipient_id")

    if not latest_package:
        # Create a default package if none generated yet
        distributor = DocumentDistributor(pki)
        with open(sample_pdf_path, "rb") as f:
            doc_bytes = f.read()
        latest_package = distributor.create_package(
            document_bytes=doc_bytes,
            document_id="MOD-OP-TRIDENT-2026",
            document_title="STRATEGIC CONTINGENCY PLAN TRIDENT",
            sender_id="JOINT-CHIEFS-OF-STAFF",
            recipient_ids=["IND-MOD-001", "IND-MOD-002", "IND-MOD-003"],
            classification_level="COSMIC TOP SECRET",
        )

    guard = DecryptionGuard(pki, ledger)
    try:
        res = guard.decrypt_and_bind(
            package=latest_package,
            recipient_id=recipient_id,
            device_fingerprint=f"SECURE-TERMINAL-{recipient_id[-3:]}",
        )
    except Exception as e:
        response.status = 400
        return {"success": False, "error": str(e)}

    # Store watermarked document artifact
    art_id = str(uuid.uuid4())
    pdf_bytes = res["watermarked_pdf_bytes"]
    decrypted_artifacts[art_id] = {
        "pdf_bytes": pdf_bytes,
        "recipient_id": recipient_id,
        "token_id": res["session_token"].token_id,
    }

    # Render screenshot of page 1 for simulation
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    pix = doc[0].get_pixmap(dpi=150)
    png_bytes = pix.tobytes("png")
    doc.close()
    decrypted_artifacts[f"{art_id}_screenshot"] = {
        "img_bytes": png_bytes,
        "recipient_id": recipient_id,
        "token_id": res["session_token"].token_id,
    }

    # Save to disk
    pdf_out = os.path.join(UPLOADS_DIR, f"decrypted_{recipient_id}.pdf")
    with open(pdf_out, "wb") as f:
        f.write(pdf_bytes)

    png_out = os.path.join(UPLOADS_DIR, f"screenshot_{recipient_id}.png")
    with open(png_out, "wb") as f:
        f.write(png_bytes)

    dpr = res["provenance_record"]
    return {
        "success": True,
        "artifact_id": art_id,
        "recipient_id": recipient_id,
        "officer_name": dpr.officer_name,
        "division": dpr.division,
        "watermark_token_id": dpr.watermark_token_id,
        "block_index": res["block_index"],
        "block_hash": res["block_hash"],
        "merkle_root": res["merkle_root"],
        "timestamp": dpr.timestamp,
        "pdf_download_url": f"/download/artifact/{art_id}.pdf",
        "screenshot_url": f"/download/screenshot/{art_id}.png",
    }


@app.route("/api/investigate", method=["POST", "OPTIONS"])
def api_investigate():
    if request.method == "OPTIONS":
        return {}
    
    investigator = ForensicInvestigator(ledger)

    # Check if a file was uploaded or artifact_id specified
    upload = request.files.get("file")
    artifact_id = request.forms.get("artifact_id")

    if upload:
        raw_bytes = upload.file.read()
    elif artifact_id and artifact_id in decrypted_artifacts:
        art = decrypted_artifacts[artifact_id]
        raw_bytes = art.get("pdf_bytes") or art.get("img_bytes")
    elif artifact_id and f"{artifact_id}_screenshot" in decrypted_artifacts:
        art = decrypted_artifacts[f"{artifact_id}_screenshot"]
        raw_bytes = art["img_bytes"]
    else:
        # Fallback to scanning the most recently generated decrypted PDF or screenshot in uploads
        files = [os.path.join(UPLOADS_DIR, f) for f in os.listdir(UPLOADS_DIR) if f.startswith("decrypted_") or f.startswith("screenshot_")]
        if files:
            latest_f = max(files, key=os.path.getmtime)
            with open(latest_f, "rb") as f:
                raw_bytes = f.read()
        else:
            response.status = 400
            return {"success": False, "error": "No file or artifact provided for investigation"}

    cert = investigator.investigate_leak(raw_bytes)
    return {
        "success": True,
        "certificate": cert.to_dict(),
    }


@app.route("/api/ledger", method=["GET", "OPTIONS"])
def api_ledger():
    if request.method == "OPTIONS":
        return {}
    blocks = [b.to_dict() for b in ledger.chain]
    return {"blocks": blocks}


@app.route("/api/ledger/audit", method=["GET", "OPTIONS"])
def api_ledger_audit():
    if request.method == "OPTIONS":
        return {}
    return ledger.verify_chain()


@app.route("/api/ledger/tamper", method=["POST", "OPTIONS"])
def api_ledger_tamper():
    if request.method == "OPTIONS":
        return {}
    if len(ledger.chain) <= 1:
        response.status = 400
        return {"success": False, "error": "Cannot tamper: ledger has only genesis block. Decrypt a document first!"}
    
    target_officer = request.json.get("framed_officer", "IND-MOD-001 (Col. Arvind Sharma)") if request.json else "IND-MOD-001 (Col. Arvind Sharma)"
    ledger.simulate_tamper_attack(1, target_officer)
    audit = ledger.verify_chain()
    return {
        "success": True,
        "tampered_block": 1,
        "framed_officer": target_officer,
        "audit_result": audit,
    }


@app.route("/api/ledger/restore", method=["POST", "OPTIONS"])
def api_ledger_restore():
    global ledger
    if request.method == "OPTIONS":
        return {}
    # Reinitialize clean ledger
    ledger_path = os.path.join(DATA_DIR, "ledger_chain.json")
    if os.path.exists(ledger_path):
        os.remove(ledger_path)
    ledger = AirGappedLedger(DATA_DIR)
    return {"success": True, "message": "Ledger state cleanly re-initialized to Genesis."}


@app.route("/download/artifact/<art_id>.pdf")
def download_pdf(art_id):
    if art_id in decrypted_artifacts:
        raw_bytes = decrypted_artifacts[art_id]["pdf_bytes"]
        res = HTTPResponse(body=raw_bytes, status=200)
        res.set_header("Content-Type", "application/pdf")
        res.set_header("Content-Disposition", f"attachment; filename=decrypted_classified_{art_id[:8]}.pdf")
        return res
    return HTTPResponse(body="Not found", status=404)


@app.route("/download/screenshot/<art_id>.png")
def download_screenshot(art_id):
    key = f"{art_id}_screenshot"
    if key in decrypted_artifacts:
        raw_bytes = decrypted_artifacts[key]["img_bytes"]
        res = HTTPResponse(body=raw_bytes, status=200)
        res.set_header("Content-Type", "image/png")
        return res
    return HTTPResponse(body="Not found", status=404)


# Web UI Dashboard Route
from .index_html import get_dashboard_html

@app.route("/")
def index():
    return get_dashboard_html()


def start_server(host="127.0.0.1", port=8080):
    print("\n" + "=" * 80)
    print("  MINISTRY OF DEFENCE — CRYPTOSEAL PQC DEFENCE DASHBOARD")
    print(f"  Server online at: http://{host}:{port}/")
    print("  Mode: 100% Offline / Air-Gapped / Post-Quantum Cryptography Active")
    print("=" * 80 + "\n")
    app.run(host=host, port=port, debug=False, quiet=True)


if __name__ == "__main__":
    start_server()
