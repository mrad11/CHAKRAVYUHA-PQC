"""
Block Structure, Decryption Provenance Records (DPR), and Multi-Validator Consensus
Implements Post-Quantum non-repudiable recipient signatures and consortium PoA block validation.
"""

import json
import base64
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from ..crypto.pqc import PQCKeyManager, HashUtil


@dataclass
class DecryptionProvenanceRecord:
    """
    Legally binding, non-repudiable record of a document decryption event.
    Signed by the recipient using their NIST FIPS 204 ML-DSA-65 private key.
    """
    record_id: str
    document_id: str
    document_title: str
    document_hash_sha3: str
    recipient_id: str
    officer_name: str
    division: str
    clearance_level: str
    session_id: str
    watermark_token_id: str
    watermark_digest_sha256: str
    timestamp: str
    client_device_fingerprint: str
    recipient_dsa_public_key_pem: str
    recipient_signature_b64: str

    def canonical_bytes(self) -> bytes:
        """Produce deterministic canonical byte string of the record fields for signing/verifying."""
        data = {
            "record_id": self.record_id,
            "document_id": self.document_id,
            "document_title": self.document_title,
            "document_hash_sha3": self.document_hash_sha3,
            "recipient_id": self.recipient_id,
            "officer_name": self.officer_name,
            "division": self.division,
            "clearance_level": self.clearance_level,
            "session_id": self.session_id,
            "watermark_token_id": self.watermark_token_id,
            "watermark_digest_sha256": self.watermark_digest_sha256,
            "timestamp": self.timestamp,
            "client_device_fingerprint": self.client_device_fingerprint,
        }
        canonical_json = json.dumps(data, sort_keys=True, separators=(",", ":"))
        return canonical_json.encode("utf-8")

    def verify_signature(self) -> bool:
        """Verify that the recipient's ML-DSA-65 signature covers the canonical record bytes."""
        try:
            pub_key = PQCKeyManager.deserialize_dsa_public_key(self.recipient_dsa_public_key_pem)
            sig_bytes = base64.b64decode(self.recipient_signature_b64)
            msg_bytes = self.canonical_bytes()
            return PQCKeyManager.dsa_verify(pub_key, sig_bytes, msg_bytes)
        except Exception:
            return False

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> "DecryptionProvenanceRecord":
        return cls(**data)


class ValidatorNode:
    """Consortium validation authority (e.g. Army HQ, Naval Cyber, Joint Ops Command)."""

    def __init__(self, node_id: str, name: str, dsa_priv_pem: str, dsa_pub_pem: str):
        self.node_id = node_id
        self.name = name
        self.dsa_priv_pem = dsa_priv_pem
        self.dsa_pub_pem = dsa_pub_pem

    @classmethod
    def create(cls, node_id: str, name: str) -> "ValidatorNode":
        priv, pub = PQCKeyManager.generate_dsa_keypair()
        priv_pem = PQCKeyManager.serialize_dsa_private_key(priv)
        pub_pem = PQCKeyManager.serialize_dsa_public_key(pub)
        return cls(node_id, name, priv_pem, pub_pem)

    def sign_block(self, block_hash: str) -> str:
        """Sign a block header hash using this validator's ML-DSA-65 private key."""
        priv = PQCKeyManager.deserialize_dsa_private_key(self.dsa_priv_pem)
        sig = PQCKeyManager.dsa_sign(priv, block_hash.encode("utf-8"))
        return base64.b64encode(sig).decode("utf-8")


@dataclass
class Block:
    """An immutable block containing a Merkle tree of Decryption Provenance Records."""
    index: int
    timestamp: str
    prev_hash: str
    merkle_root: str
    transactions: List[DecryptionProvenanceRecord]
    block_hash: str
    validator_signatures: Dict[str, str]  # node_id -> b64 signature

    def compute_header_hash(self) -> str:
        """Compute SHA3-256 hash of block header."""
        header_str = f"{self.index}:{self.timestamp}:{self.prev_hash}:{self.merkle_root}"
        return HashUtil.sha3_256(header_str.encode("utf-8"))

    def to_dict(self) -> Dict:
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "prev_hash": self.prev_hash,
            "merkle_root": self.merkle_root,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "block_hash": self.block_hash,
            "validator_signatures": self.validator_signatures,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Block":
        txs = [DecryptionProvenanceRecord.from_dict(t) for t in data["transactions"]]
        return cls(
            index=data["index"],
            timestamp=data["timestamp"],
            prev_hash=data["prev_hash"],
            merkle_root=data["merkle_root"],
            transactions=txs,
            block_hash=data["block_hash"],
            validator_signatures=data.get("validator_signatures", {}),
        )
