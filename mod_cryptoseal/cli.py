import os
import sys
import argparse
import json

# Ensure Windows terminal compatibility
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from .crypto.pki import AirGappedPKI
from .ledger.chain import AirGappedLedger
from .engine.distributor import DocumentDistributor
from .engine.decryption_guard import DecryptionGuard
from .engine.forensics import ForensicInvestigator


def get_default_data_dir() -> str:
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base, "data_store")
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


def cmd_pki_list(args):
    data_dir = get_default_data_dir()
    pki = AirGappedPKI(data_dir)
    pki.seed_default_defence_personnel()
    officers = pki.get_public_directory()

    print("\n" + "=" * 80)
    print("  MINISTRY OF DEFENCE — AIR-GAPPED POST-QUANTUM PKI DIRECTORY")
    print("  Algorithms: NIST FIPS 203 (ML-KEM-768) | NIST FIPS 204 (ML-DSA-65)")
    print("=" * 80)
    for off in officers:
        print(f"  [+] Officer ID:   {off['recipient_id']}")
        print(f"      Name:         {off['officer_name']} ({off['rank']})")
        print(f"      Division:     {off['division']}")
        print(f"      Clearance:    {off['clearance_level']}")
        print(f"      ML-DSA Fingerprint: {off['dsa_fingerprint']}")
        print("-" * 80)
    print(f"  Total Authorized Personnel: {len(officers)}\n")


def cmd_distribute(args):
    data_dir = get_default_data_dir()
    pki = AirGappedPKI(data_dir)
    pki.seed_default_defence_personnel()

    doc_path = args.document
    if not os.path.exists(doc_path):
        print(f"[!] Error: Document file not found: {doc_path}")
        sys.exit(1)

    with open(doc_path, "rb") as f:
        doc_bytes = f.read()

    recipients = [r.strip() for r in args.recipients.split(",") if r.strip()]
    distributor = DocumentDistributor(pki)

    print("\n" + "=" * 80)
    print("  MINISTRY OF DEFENCE — BROADCAST ENCRYPTION PROTOCOL")
    print("=" * 80)
    print(f"  Document File:        {doc_path} ({len(doc_bytes)} bytes)")
    print(f"  Document Identifier:  {args.id}")
    print(f"  Classification:       {args.classification}")
    print(f"  Issuing Authority:    {args.sender}")
    print(f"  Target Recipients:    {', '.join(recipients)}")
    print("  [+] Generating 256-bit symmetric session key...")
    print("  [+] Encrypting document payload using AES-256-GCM...")
    print("  [+] Encapsulating session key with ML-KEM-768 for each recipient...")

    package = distributor.create_package(
        document_bytes=doc_bytes,
        document_id=args.id,
        document_title=args.title,
        sender_id=args.sender,
        recipient_ids=recipients,
        classification_level=args.classification,
    )

    out_file = args.output or f"{args.id}.modpkg"
    distributor.save_package_to_file(package, out_file)

    print(f"  [✓] Broadcast package successfully sealed and saved to: {out_file}")
    print(f"  [✓] Package ID: {package.package_id}")
    print(f"  [✓] Document SHA3-256 Digest: {package.document_hash_sha3}")
    print("=" * 80 + "\n")


def cmd_decrypt(args):
    data_dir = get_default_data_dir()
    pki = AirGappedPKI(data_dir)
    pki.seed_default_defence_personnel()
    ledger = AirGappedLedger(data_dir)

    pkg_path = args.package
    if not os.path.exists(pkg_path):
        print(f"[!] Error: Package file not found: {pkg_path}")
        sys.exit(1)

    package = DocumentDistributor.load_package_from_file(pkg_path)
    guard = DecryptionGuard(pki, ledger)

    print("\n" + "=" * 80)
    print("  MINISTRY OF DEFENCE — HIGH-ASSURANCE DECRYPTION GATEWAY")
    print("=" * 80)
    print(f"  Package:              {pkg_path}")
    print(f"  Document Title:       {package.document_title} ({package.classification_level})")
    print(f"  Recipient ID:         {args.recipient}")
    print("  [1] Decapsulating session key via recipient NIST FIPS 203 ML-KEM-768 private key...")
    print("  [2] Intercepting plaintext: atomic provenance guard engaged...")
    print("  [3] Generating unique session watermark token...")
    print("  [4] Formulating Decryption Provenance Record (DPR)...")
    print("  [5] Signing DPR with recipient NIST FIPS 204 ML-DSA-65 private key...")
    print("  [6] Committing signed record to air-gapped multi-validator DLT ledger...")

    try:
        res = guard.decrypt_and_bind(
            package=package,
            recipient_id=args.recipient,
            device_fingerprint=args.device or "AIRGAP-SECURE-TERMINAL-01",
        )
    except Exception as e:
        print(f"\n[!] DECRYPTION ABORTED: {e}\n")
        sys.exit(1)

    out_pdf = args.output or f"DECRYPTED_{args.recipient}_{package.document_id}.pdf"
    with open(out_pdf, "wb") as f:
        f.write(res["watermarked_pdf_bytes"])

    token = res["session_token"]
    print(f"  [7] Injected dual-layer invisible watermark (Token: {token.token_id})")
    print(f"  [✓] Block #{res['block_index']} mined on DLT ledger (Hash: {res['block_hash'][:16]}...)")
    print(f"  [✓] Output document written to: {out_pdf}")
    print(f"  [!] Note: Decrypted copy is visually clean but uniquely, forensically fingerprinted.")
    print("=" * 80 + "\n")


def cmd_investigate(args):
    data_dir = get_default_data_dir()
    ledger = AirGappedLedger(data_dir)
    investigator = ForensicInvestigator(ledger)

    artifact_path = args.artifact
    if not os.path.exists(artifact_path):
        print(f"[!] Error: Leaked artifact file not found: {artifact_path}")
        sys.exit(1)

    print("\n" + "=" * 80)
    print("  MINISTRY OF DEFENCE — FORENSIC LEAK ATTRIBUTION LABORATORY")
    print("=" * 80)
    print(f"  Target Leaked Artifact: {artifact_path}")
    print("  [+] Executing dual-layer watermark extraction (PDF stego & visual demodulation)...")

    cert = investigator.investigate_leak(artifact_path)

    print("\n" + "#" * 80)
    print(f"  FORENSIC ATTRIBUTION CERTIFICATE: {cert.certificate_id}")
    print(f"  STATUS: {cert.status}")
    print("#" * 80)
    if cert.status == "CONFIRMED_LEAK_ATTRIBUTED":
        print(f"  CULPRIT IDENTIFIED:     {cert.culprit_name} ({cert.culprit_officer_id})")
        print(f"  DIVISION:               {cert.culprit_division}")
        print(f"  CLEARANCE:              {cert.culprit_clearance}")
        print(f"  DOCUMENT:               {cert.document_title} ({cert.document_id})")
        print(f"  DECRYPTION TIMESTAMP:   {cert.decryption_timestamp}")
        print(f"  SESSION IDENTIFIER:     {cert.decryption_session_id}")
        print(f"  DEVICE FINGERPRINT:     {cert.device_fingerprint}")
        print(f"  WATERMARK TOKEN ID:     {cert.watermark_token_id}")
        print(f"  EXTRACTION MECHANISM:   {cert.extraction_layer}")
        print("-" * 80)
        print("  CRYPTOGRAPHIC VERIFICATION:")
        print(f"  [✓] Recipient ML-DSA-65 Digital Signature: VALID (NIST FIPS 204)")
        print(f"  [✓] Merkle Inclusion Proof:               VALID (Block #{cert.block_index})")
        print(f"  [✓] Multi-Validator Consensus:            VALID (Consortium PoA)")
        print("-" * 80)
        print(f"  LEGAL EVIDENCE STATEMENT:")
        print(f"  {cert.legal_non_repudiation_statement}")
    else:
        print(f"  Outcome: {cert.legal_non_repudiation_statement}")
    print("#" * 80 + "\n")


def cmd_ledger_audit(args):
    data_dir = get_default_data_dir()
    ledger = AirGappedLedger(data_dir)
    print("\n" + "=" * 80)
    print("  MINISTRY OF DEFENCE — IMMUTABLE DLT LEDGER INTEGRITY AUDIT")
    print("=" * 80)
    audit = ledger.verify_chain()
    print(f"  Ledger Status:         {audit['status']}")
    print(f"  Is Chain Valid:        {audit['is_valid']}")
    print(f"  Total Blocks:          {audit['total_blocks']}")
    print(f"  Total Provenance Logs: {audit['total_records']}")
    if not audit["is_valid"]:
        print(f"  [!] TAMPER DETECTED ON BLOCKS: {audit['tampered_blocks']}")
        for err in audit["errors"]:
            print(f"      - {err}")
    else:
        print("  [✓] All block headers, Merkle roots, PQC signatures, and multi-validator PoA keys intact.")
    print("=" * 80 + "\n")


def cmd_tamper_demo(args):
    data_dir = get_default_data_dir()
    ledger = AirGappedLedger(data_dir)
    if len(ledger.chain) <= 1:
        print("[!] No transaction blocks present to tamper. Please decrypt a document first!")
        return

    print("\n" + "=" * 80)
    print("  SIMULATING ROGUE ADMINISTRATOR / INSIDER THREAT ATTACK")
    print("=" * 80)
    print("  [Scenario]: A database administrator with root access directly edits Block #1")
    print("              to alter the recipient ID and frame an innocent officer...")
    ledger.simulate_tamper_attack(1, "IND-MOD-FRAMED-COLONEL")
    print("  [+] Block #1 payload has been illicitly modified in offline database.")
    print("  [+] Executing immediate cryptographic audit...")
    audit = ledger.verify_chain()
    print(f"\n  AUDIT RESULT: {audit['status']}")
    for err in audit["errors"]:
        print(f"  [ALERT] {err}")
    print("=" * 80 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="CryptoSeal PQC: Cryptographic Attribution & Immutable Decryption Provenance (MoD)"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # pki list
    p_pki = subparsers.add_parser("pki-list", help="List cleared personnel in air-gapped PKI directory")
    p_pki.set_defaults(func=cmd_pki_list)

    # distribute
    p_dist = subparsers.add_parser("distribute", help="Broadcast-encrypt classified document for recipients")
    p_dist.add_argument("--document", required=True, help="Path to input PDF document")
    p_dist.add_argument("--id", required=True, help="Document ID (e.g. MOD-OP-TRIDENT)")
    p_dist.add_argument("--title", required=True, help="Document title")
    p_dist.add_argument("--sender", default="MOD-JOINT-OPERATIONS-COMMAND", help="Issuing command/officer")
    p_dist.add_argument("--recipients", required=True, help="Comma-separated recipient IDs (e.g. IND-MOD-001,IND-MOD-003)")
    p_dist.add_argument("--classification", default="COSMIC TOP SECRET", help="Classification level")
    p_dist.add_argument("--output", help="Output package path (.modpkg)")
    p_dist.set_defaults(func=cmd_distribute)

    # decrypt
    p_dec = subparsers.add_parser("decrypt", help="Recipient decrypts document (forces watermarking & DLT commit)")
    p_dec.add_argument("--package", required=True, help="Path to encrypted .modpkg file")
    p_dec.add_argument("--recipient", required=True, help="Recipient Officer ID (e.g. IND-MOD-003)")
    p_dec.add_argument("--device", default="AIRGAP-TERMINAL-01", help="Device terminal fingerprint")
    p_dec.add_argument("--output", help="Output decrypted watermarked PDF path")
    p_dec.set_defaults(func=cmd_decrypt)

    # investigate
    p_inv = subparsers.add_parser("investigate", help="Investigate a leaked document/screenshot and attribute suspect")
    p_inv.add_argument("--artifact", required=True, help="Path to leaked PDF or image screenshot")
    p_inv.set_defaults(func=cmd_investigate)

    # ledger-audit
    p_aud = subparsers.add_parser("ledger-audit", help="Audit the immutable DLT blockchain integrity")
    p_aud.set_defaults(func=cmd_ledger_audit)

    # tamper-demo
    p_tamp = subparsers.add_parser("tamper-demo", help="Simulate a rogue administrator tamper attack")
    p_tamp.set_defaults(func=cmd_tamper_demo)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)

    args.func(args)


if __name__ == "__main__":
    main()
