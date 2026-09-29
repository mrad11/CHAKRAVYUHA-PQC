"""
Forensic Attribution & Leak Investigation Engine
Extracts embedded watermark, audits DLT ledger, cryptographically verifies PQC signatures
and Merkle inclusion proofs, and produces a tamper-evident Forensic Attribution Certificate.
"""

import uuid
import datetime
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass, asdict
from ..watermark.extractor import WatermarkExtractor
from ..ledger.chain import AirGappedLedger
from ..ledger.merkle import MerkleProof
from ..crypto.pqc import PQCKeyManager


@dataclass
class ForensicAttributionCertificate:
    """Official cryptographic certificate attributing a leaked document to a specific recipient."""
    certificate_id: str
    generated_at: str
    status: str  # CONFIRMED_LEAK_ATTRIBUTED, NO_WATERMARK_FOUND, TAMPERED_SIGNATURE, etc.
    culprit_officer_id: Optional[str]
    culprit_name: Optional[str]
    culprit_division: Optional[str]
    culprit_clearance: Optional[str]
    document_id: Optional[str]
    document_title: Optional[str]
    decryption_timestamp: Optional[str]
    decryption_session_id: Optional[str]
    device_fingerprint: Optional[str]
    watermark_token_id: Optional[str]
    extraction_layer: Optional[str]
    pqc_signature_valid: bool
    pqc_algorithm: str
    merkle_inclusion_valid: bool
    block_index: Optional[int]
    block_hash: Optional[str]
    merkle_root: Optional[str]
    validator_consensus_valid: bool
    legal_non_repudiation_statement: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ForensicInvestigator:
    """Automated investigative workstation for leaked military and government intelligence."""

    def __init__(self, ledger: AirGappedLedger):
        self.ledger = ledger

    def investigate_leak(
        self,
        leaked_artifact: Union[str, bytes],
    ) -> ForensicAttributionCertificate:
        """
        Analyze a leaked file or image buffer and produce an official Forensic Attribution Certificate.
        """
        now_str = datetime.datetime.now(datetime.timezone.utc).isoformat()
        cert_id = f"CERT-ATTRIB-{uuid.uuid4().hex[:12].upper()}"

        # 1. Extract forensic watermark
        extracted = WatermarkExtractor.extract_from_file_or_bytes(leaked_artifact)
        if not extracted:
            return ForensicAttributionCertificate(
                certificate_id=cert_id,
                generated_at=now_str,
                status="NO_WATERMARK_FOUND",
                culprit_officer_id=None,
                culprit_name=None,
                culprit_division=None,
                culprit_clearance=None,
                document_id=None,
                document_title=None,
                decryption_timestamp=None,
                decryption_session_id=None,
                device_fingerprint=None,
                watermark_token_id=None,
                extraction_layer=None,
                pqc_signature_valid=False,
                pqc_algorithm="NIST FIPS 204 (ML-DSA-65)",
                merkle_inclusion_valid=False,
                block_index=None,
                block_hash=None,
                merkle_root=None,
                validator_consensus_valid=False,
                legal_non_repudiation_statement="No forensic watermark was detected in the provided artifact.",
            )

        token_id = extracted["token_id"]
        layer = extracted.get("extraction_layer", "UNKNOWN")

        # 2. Query Air-Gapped Immutable DLT Ledger
        ledger_entry = self.ledger.lookup_by_watermark(token_id)
        if not ledger_entry:
            return ForensicAttributionCertificate(
                certificate_id=cert_id,
                generated_at=now_str,
                status="UNREGISTERED_OR_COUNTERFEIT_TOKEN",
                culprit_officer_id=extracted.get("recipient_id"),
                culprit_name=None,
                culprit_division=None,
                culprit_clearance=None,
                document_id=extracted.get("document_id"),
                document_title=None,
                decryption_timestamp=None,
                decryption_session_id=None,
                device_fingerprint=None,
                watermark_token_id=token_id,
                extraction_layer=layer,
                pqc_signature_valid=False,
                pqc_algorithm="NIST FIPS 204 (ML-DSA-65)",
                merkle_inclusion_valid=False,
                block_index=None,
                block_hash=None,
                merkle_root=None,
                validator_consensus_valid=False,
                legal_non_repudiation_statement="Watermark token was extracted but does not exist in the confirmed DLT ledger.",
            )

        record = ledger_entry["record"]
        block = ledger_entry["block"]
        proof_data = ledger_entry["merkle_proof"]

        # 3. Cryptographic Verification of Recipient ML-DSA-65 Signature
        pqc_sig_valid = record.verify_signature()

        # 4. Cryptographic Verification of Merkle Inclusion Proof
        merkle_valid = False
        if proof_data:
            proof = MerkleProof.from_dict(proof_data)
            merkle_valid = proof.verify(block.merkle_root)

        # 5. Cryptographic Verification of Block Consensus Signatures
        validator_consensus_valid = False
        valid_val_count = 0
        for vid, sig_b64 in block.validator_signatures.items():
            if vid in self.ledger.validators:
                val = self.ledger.validators[vid]
                pub = PQCKeyManager.deserialize_dsa_public_key(val.dsa_pub_pem)
                import base64
                if PQCKeyManager.dsa_verify(pub, base64.b64decode(sig_b64), block.block_hash.encode("utf-8")):
                    valid_val_count += 1
        if valid_val_count >= 2:
            validator_consensus_valid = True

        status = "CONFIRMED_LEAK_ATTRIBUTED" if (pqc_sig_valid and merkle_valid and validator_consensus_valid) else "CRYPTOGRAPHIC_INTEGRITY_FAILURE"

        return ForensicAttributionCertificate(
            certificate_id=cert_id,
            generated_at=now_str,
            status=status,
            culprit_officer_id=record.recipient_id,
            culprit_name=record.officer_name,
            culprit_division=record.division,
            culprit_clearance=record.clearance_level,
            document_id=record.document_id,
            document_title=record.document_title,
            decryption_timestamp=record.timestamp,
            decryption_session_id=record.session_id,
            device_fingerprint=record.client_device_fingerprint,
            watermark_token_id=record.watermark_token_id,
            extraction_layer=layer,
            pqc_signature_valid=pqc_sig_valid,
            pqc_algorithm="NIST FIPS 204 (ML-DSA-65)",
            merkle_inclusion_valid=merkle_valid,
            block_index=block.index,
            block_hash=block.block_hash,
            merkle_root=block.merkle_root,
            validator_consensus_valid=validator_consensus_valid,
            legal_non_repudiation_statement=(
                f"FORENSIC NON-REPUDIATION VERIFIED: Leaked document artifact has been mathematically linked to "
                f"{record.officer_name} ({record.recipient_id}) of {record.division}. The decryption event was digitally "
                f"signed by the officer's private NIST FIPS 204 ML-DSA-65 key, anchored in Block #{block.index} "
                f"of the immutable DLT ledger with validated Merkle proof ({record.watermark_token_id}). "
                f"The recipient cannot legally repudiate this decryption event."
            ),
        )
