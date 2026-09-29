"""
Full End-to-End System Integration Test
Simulates the entire multi-recipient broadcast encryption, individual decryption,
mandatory watermarking, DLT committal, leak simulation, and forensic attribution workflow.
"""

import unittest
import os
import pymupdf
from mod_cryptoseal.crypto.pki import AirGappedPKI
from mod_cryptoseal.ledger.chain import AirGappedLedger
from mod_cryptoseal.engine.distributor import DocumentDistributor
from mod_cryptoseal.engine.decryption_guard import DecryptionGuard
from mod_cryptoseal.engine.forensics import ForensicInvestigator


class TestEndToEnd(unittest.TestCase):

    def setUp(self):
        # 1. Initialize PKI with cleared Ministry of Defence officers
        self.pki = AirGappedPKI()
        self.pki.seed_default_defence_personnel()

        # 2. Initialize Air-Gapped DLT Ledger
        self.ledger = AirGappedLedger()

        # 3. Create Sample Top-Secret PDF
        doc = pymupdf.open()
        p = doc.new_page()
        p.insert_text(pymupdf.Point(72, 72), "MINISTRY OF DEFENCE — WARFARE PLAN DELTA", fontsize=16)
        p.insert_text(pymupdf.Point(72, 120), "Restricted multi-recipient operational intelligence.", fontsize=11)
        self.doc_bytes = doc.tobytes()
        doc.close()

    def test_full_mission_lifecycle(self):
        # Phase 1: Sender Broadcast Encryption
        distributor = DocumentDistributor(self.pki)
        recipients = ["IND-MOD-001", "IND-MOD-002", "IND-MOD-003"]

        package = distributor.create_package(
            document_bytes=self.doc_bytes,
            document_id="MOD-PLAN-DELTA-2026",
            document_title="OPERATION PLAN DELTA",
            sender_id="AUTH-CHIEF-OF-DEFENCE-STAFF",
            recipient_ids=recipients,
            classification_level="COSMIC TOP SECRET",
        )
        self.assertEqual(len(package.recipient_blocks), 3)

        # Phase 2: Unauthorized Recipient Attempt (Access Control)
        guard = DecryptionGuard(self.pki, self.ledger)
        with self.assertRaises(PermissionError):
            guard.decrypt_and_bind(package, "IND-MOD-004")  # Officer 4 was not included!

        # Phase 3: Authorized Decryption by Officer 3 (Maj. Priya Nair)
        # Enforces atomic decryption, DPR signing, DLT commit, and dual-layer watermark
        decryption_result = guard.decrypt_and_bind(package, "IND-MOD-003")
        watermarked_doc = decryption_result["watermarked_pdf_bytes"]
        token = decryption_result["session_token"]
        block_idx = decryption_result["block_index"]

        self.assertIsNotNone(watermarked_doc)
        self.assertEqual(token.recipient_id, "IND-MOD-003")
        self.assertGreater(block_idx, 0)

        # Phase 4: Verify DLT Ledger State
        ledger_audit = self.ledger.verify_chain()
        self.assertTrue(ledger_audit["is_valid"])
        self.assertEqual(ledger_audit["total_records"], 1)

        # Phase 5: Leak Simulation (Officer 3 leaks document)
        # Scenario A: Digital PDF Leak
        investigator = ForensicInvestigator(self.ledger)
        cert_pdf = investigator.investigate_leak(watermarked_doc)

        self.assertEqual(cert_pdf.status, "CONFIRMED_LEAK_ATTRIBUTED")
        self.assertEqual(cert_pdf.culprit_officer_id, "IND-MOD-003")
        self.assertEqual(cert_pdf.culprit_name, "Maj. Priya Nair")
        self.assertTrue(cert_pdf.pqc_signature_valid)
        self.assertTrue(cert_pdf.merkle_inclusion_valid)
        self.assertTrue(cert_pdf.validator_consensus_valid)
        print("\n[E2E] PDF Leak Forensic Attribution: SUCCESS!")
        print(f"      Attributed to: {cert_pdf.culprit_name} ({cert_pdf.culprit_officer_id})")
        print(f"      PQC ML-DSA-65 Signature Verified: {cert_pdf.pqc_signature_valid}")
        print(f"      Merkle Inclusion Proof Verified: {cert_pdf.merkle_inclusion_valid}")

        # Scenario B: Screenshot Leak (Officer 3 took screenshot of page 1)
        leak_doc = pymupdf.open(stream=watermarked_doc, filetype="pdf")
        pix = leak_doc[0].get_pixmap(dpi=150)
        screenshot_png = pix.tobytes("png")
        leak_doc.close()

        cert_screenshot = investigator.investigate_leak(screenshot_png)
        self.assertEqual(cert_screenshot.status, "CONFIRMED_LEAK_ATTRIBUTED")
        self.assertEqual(cert_screenshot.culprit_officer_id, "IND-MOD-003")
        self.assertEqual(cert_screenshot.culprit_name, "Maj. Priya Nair")
        print("\n[E2E] Screenshot Leak Forensic Attribution: SUCCESS!")
        print(f"      Attributed to: {cert_screenshot.culprit_name} ({cert_screenshot.culprit_officer_id})")

        # Exoneration Check: Verify that Officer 1 (Col. Arvind Sharma) is NOT blamed
        self.assertNotEqual(cert_pdf.culprit_officer_id, "IND-MOD-001")


if __name__ == "__main__":
    unittest.main()
