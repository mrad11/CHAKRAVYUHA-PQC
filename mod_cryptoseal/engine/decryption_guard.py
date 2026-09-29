"""
Decryption Guard (Recipient Security Gateway)
Enforces the mandatory atomic sequence upon decryption:
1. PQC ML-KEM-768 Decapsulation & AES-256-GCM Decryption.
2. Dynamic Session Watermark Token generation.
3. Creation and ML-DSA-65 Digital Signing of Decryption Provenance Record (DPR).
4. Committal to the Air-Gapped Immutable DLT Ledger.
5. Dual-Layer Invisible Forensic Watermarking.
6. Delivery of uniquely fingerprinted, visually identical document to recipient.
"""

import uuid
import base64
import datetime
from typing import Dict, Any, Optional
from ..crypto.pki import AirGappedPKI
from ..crypto.pqc import PQCKeyManager, HashUtil
from ..crypto.envelope import BroadcastEnvelope, EncryptedPackage
from ..watermark.token import SessionWatermarkToken
from ..watermark.engine import WatermarkEngine
from ..ledger.block import DecryptionProvenanceRecord
from ..ledger.chain import AirGappedLedger


class DecryptionGuard:
    """Security boundary enforcing non-bypassable watermarking and DLT provenance."""

    def __init__(self, pki: AirGappedPKI, ledger: AirGappedLedger):
        self.pki = pki
        self.ledger = ledger

    def decrypt_and_bind(
        self,
        package: EncryptedPackage,
        recipient_id: str,
        device_fingerprint: str = "SECURE-TERMINAL-AIRGAP-01",
    ) -> Dict[str, Any]:
        """
        Executes atomic decryption, DPR signing, DLT committal, and forensic watermarking.
        
        Returns:
            Dictionary containing:
            - watermarked_pdf_bytes
            - session_token
            - provenance_record
            - block_index
            - block_hash
        """
        # 1. Fetch recipient officer credentials
        officer = self.pki.get_officer(recipient_id)
        if not officer:
            raise PermissionError(f"Officer '{recipient_id}' not found in local air-gapped PKI keystore")

        # 2. Decrypt master payload using recipient's ML-KEM-768 private key
        decrypted_doc_bytes, doc_hash_sha3 = BroadcastEnvelope.decrypt_for_recipient(
            package=package,
            recipient_id=recipient_id,
            recipient_kem_private_key_pem=officer.kem_private_key_pem,
        )

        # 3. Generate unique session watermark token
        session_token = SessionWatermarkToken.create(
            recipient_id=officer.officer_id,
            document_id=package.document_id,
        )

        # 4. Formulate Decryption Provenance Record (DPR)
        now_str = datetime.datetime.now(datetime.timezone.utc).isoformat()
        watermark_digest = HashUtil.sha256(session_token.to_compact_string().encode("utf-8"))

        dpr = DecryptionProvenanceRecord(
            record_id=str(uuid.uuid4()),
            document_id=package.document_id,
            document_title=package.document_title,
            document_hash_sha3=doc_hash_sha3,
            recipient_id=officer.officer_id,
            officer_name=officer.name,
            division=officer.division,
            clearance_level=officer.clearance_level,
            session_id=session_token.session_id,
            watermark_token_id=session_token.token_id,
            watermark_digest_sha256=watermark_digest,
            timestamp=now_str,
            client_device_fingerprint=device_fingerprint,
            recipient_dsa_public_key_pem=officer.dsa_public_key_pem,
            recipient_signature_b64="",
        )

        # 5. Sign DPR using recipient's private NIST FIPS 204 ML-DSA-65 key
        dsa_priv = PQCKeyManager.deserialize_dsa_private_key(officer.dsa_private_key_pem)
        sig = PQCKeyManager.dsa_sign(dsa_priv, dpr.canonical_bytes())
        dpr.recipient_signature_b64 = base64.b64encode(sig).decode("utf-8")

        # 6. Commit to Air-Gapped DLT Ledger
        # The ledger validates the signature, computes Merkle root, and collects PoA validator signatures
        block = self.ledger.commit_record(dpr)

        # 7. Apply Dual-Layer Invisible Forensic Watermark to document
        watermarked_doc_bytes = WatermarkEngine.apply_watermark(
            decrypted_pdf_bytes=decrypted_doc_bytes,
            token=session_token,
        )

        return {
            "watermarked_pdf_bytes": watermarked_doc_bytes,
            "session_token": session_token,
            "provenance_record": dpr,
            "block_index": block.index,
            "block_hash": block.block_hash,
            "merkle_root": block.merkle_root,
        }
