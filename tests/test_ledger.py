"""
Unit Tests for Air-Gapped Immutable DLT Ledger, Merkle Proofs & Tamper Evidence
"""

import unittest
import uuid
import base64
from mod_cryptoseal.crypto.pqc import PQCKeyManager, HashUtil
from mod_cryptoseal.ledger.merkle import MerkleTree, MerkleProof
from mod_cryptoseal.ledger.block import DecryptionProvenanceRecord
from mod_cryptoseal.ledger.chain import AirGappedLedger


class TestLedger(unittest.TestCase):

    def test_merkle_tree_and_proofs(self):
        tx1 = b"TRANSACTION_ONE"
        tx2 = b"TRANSACTION_TWO"
        tx3 = b"TRANSACTION_THREE"
        tx4 = b"TRANSACTION_FOUR"

        tree = MerkleTree([tx1, tx2, tx3, tx4])
        self.assertEqual(len(tree.root), 64)

        # Generate and verify proof for each leaf
        for idx in range(4):
            proof = tree.get_proof(idx)
            self.assertIsNotNone(proof)
            self.assertTrue(proof.verify(tree.root))

        # Tampered leaf hash must fail verification
        bad_proof = MerkleProof(0, "0" * 64, proof.proof_path)
        self.assertFalse(bad_proof.verify(tree.root))

    def test_blockchain_immutability_and_consensus(self):
        ledger = AirGappedLedger()
        
        # Initial chain has genesis block
        self.assertEqual(len(ledger.chain), 1)
        audit_initial = ledger.verify_chain()
        self.assertTrue(audit_initial["is_valid"])

        # Create recipient PQC keys
        priv, pub = PQCKeyManager.generate_dsa_keypair()
        pub_pem = PQCKeyManager.serialize_dsa_public_key(pub)

        # Create DPR
        dpr = DecryptionProvenanceRecord(
            record_id=str(uuid.uuid4()),
            document_id="DOC-TEST-LEDGER",
            document_title="TEST CLASSIFIED TITLE",
            document_hash_sha3=HashUtil.sha3_256(b"DOC_RAW_BYTES"),
            recipient_id="IND-MOD-001",
            officer_name="Col. Sharma",
            division="DMO",
            clearance_level="TOP SECRET",
            session_id=str(uuid.uuid4()),
            watermark_token_id="SWT-LEDGER-001",
            watermark_digest_sha256=HashUtil.sha256(b"TOKEN_DIGEST"),
            timestamp="2026-09-25T14:30:00Z",
            client_device_fingerprint="TERMINAL-01",
            recipient_dsa_public_key_pem=pub_pem,
            recipient_signature_b64="",
        )

        # Sign DPR
        sig = PQCKeyManager.dsa_sign(priv, dpr.canonical_bytes())
        dpr.recipient_signature_b64 = base64.b64encode(sig).decode("utf-8")

        # Commit to ledger
        new_block = ledger.commit_record(dpr)
        self.assertEqual(new_block.index, 1)

        # Verify chain validity
        audit_post = ledger.verify_chain()
        self.assertTrue(audit_post["is_valid"])

        # Lookup by watermark
        res = ledger.lookup_by_watermark("SWT-LEDGER-001")
        self.assertIsNotNone(res)
        self.assertEqual(res["record"].recipient_id, "IND-MOD-001")

        # Simulate Tamper Attack by Rogue Administrator
        ledger.simulate_tamper_attack(1, "IND-MOD-FRAMED-OFFICER")
        audit_tampered = ledger.verify_chain()
        self.assertFalse(audit_tampered["is_valid"])
        self.assertIn("TAMPERED", audit_tampered["status"])


if __name__ == "__main__":
    unittest.main()
