"""
Multi-Recipient Hybrid Broadcast Encryption Envelope
Broadcast-Encrypt, Individually-Decrypt Model:
- Sender encrypts document once with AES-256-GCM.
- Symmetric session key is wrapped for each recipient using NIST FIPS 203 ML-KEM-768.
- Recipient header contains individualized post-quantum encapsulated key blocks.
"""

import os
import json
import base64
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from .pqc import PQCKeyManager, HashUtil


@dataclass
class RecipientKeyBlock:
    """Header entry containing PQC encapsulated key for a single recipient."""
    recipient_id: str
    officer_name: str
    kem_ciphertext_b64: str
    wrapped_doc_key_b64: str
    wrap_nonce_b64: str


@dataclass
class EncryptedPackage:
    """Complete broadcast-encrypted distribution container."""
    package_id: str
    document_id: str
    document_title: str
    document_hash_sha3: str
    sender_id: str
    timestamp: str
    classification_level: str
    encrypted_payload_b64: str
    payload_nonce_b64: str
    payload_auth_tag_b64: str
    recipient_blocks: List[RecipientKeyBlock]

    def to_json(self) -> str:
        data = asdict(self)
        return json.dumps(data, indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> "EncryptedPackage":
        data = json.loads(json_str)
        recipient_blocks = [
            RecipientKeyBlock(**rb) for rb in data.pop("recipient_blocks")
        ]
        return cls(recipient_blocks=recipient_blocks, **data)


class BroadcastEnvelope:
    """Handles hybrid broadcast encryption and individualized recipient decapsulation."""

    @staticmethod
    def _derive_wrapping_key(shared_secret: bytes, recipient_id: str) -> bytes:
        """Derive an AES-256 key from ML-KEM shared secret using HKDF-SHA256."""
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b"MOD-CRYPTOSEAL-PQC-KDF-SALT-v1",
            info=f"recipient:{recipient_id}".encode("utf-8"),
        )
        return hkdf.derive(shared_secret)

    @classmethod
    def encrypt_for_recipients(
        cls,
        document_bytes: bytes,
        document_id: str,
        document_title: str,
        sender_id: str,
        classification_level: str,
        recipients_pki_info: List[Dict[str, str]],
    ) -> EncryptedPackage:
        """
        Broadcast-encrypts a document once and encapsulates the key for each authorized recipient.
        
        Args:
            document_bytes: Raw plaintext document bytes (e.g. PDF).
            document_id: Unique document reference code.
            document_title: Subject / Title of classified document.
            sender_id: Identity of issuing authority.
            classification_level: Security classification (e.g. TOP SECRET // NOFORN).
            recipients_pki_info: List of dicts with keys:
                - 'recipient_id'
                - 'officer_name'
                - 'kem_public_key_pem'
        """
        import datetime
        import uuid

        # 1. Compute unencrypted document hash for cryptographic provenance
        doc_hash_sha3 = HashUtil.sha3_256(document_bytes)

        # 2. Generate random 256-bit symmetric document master key
        master_doc_key = AESGCM.generate_key(bit_length=256)
        aesgcm = AESGCM(master_doc_key)
        payload_nonce = os.urandom(12)

        # 3. Encrypt document bytes once using AES-256-GCM
        # Additional authenticated data includes document_id and classification
        aad = f"{document_id}:{classification_level}:{sender_id}".encode("utf-8")
        ciphertext_with_tag = aesgcm.encrypt(payload_nonce, document_bytes, aad)

        # In cryptography AESGCM, the last 16 bytes are the auth tag
        ciphertext_body = ciphertext_with_tag[:-16]
        payload_auth_tag = ciphertext_with_tag[-16:]

        # 4. For each recipient, encapsulate key using their PQC ML-KEM-768 public key
        recipient_blocks: List[RecipientKeyBlock] = []
        for rec in recipients_pki_info:
            r_id = rec["recipient_id"]
            r_name = rec["officer_name"]
            kem_pub_pem = rec["kem_public_key_pem"]

            kem_pub = PQCKeyManager.deserialize_kem_public_key(kem_pub_pem)
            kem_shared_secret, kem_ciphertext = PQCKeyManager.kem_encapsulate(kem_pub)

            # Derive key-wrapping key from post-quantum shared secret
            wrapping_key = cls._derive_wrapping_key(kem_shared_secret, r_id)
            wrap_aesgcm = AESGCM(wrapping_key)
            wrap_nonce = os.urandom(12)
            wrap_aad = f"wrap:{document_id}:{r_id}".encode("utf-8")

            # Encrypt master_doc_key with wrapping key
            wrapped_doc_key = wrap_aesgcm.encrypt(wrap_nonce, master_doc_key, wrap_aad)

            recipient_blocks.append(
                RecipientKeyBlock(
                    recipient_id=r_id,
                    officer_name=r_name,
                    kem_ciphertext_b64=base64.b64encode(kem_ciphertext).decode("utf-8"),
                    wrapped_doc_key_b64=base64.b64encode(wrapped_doc_key).decode("utf-8"),
                    wrap_nonce_b64=base64.b64encode(wrap_nonce).decode("utf-8"),
                )
            )

        package = EncryptedPackage(
            package_id=str(uuid.uuid4()),
            document_id=document_id,
            document_title=document_title,
            document_hash_sha3=doc_hash_sha3,
            sender_id=sender_id,
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            classification_level=classification_level,
            encrypted_payload_b64=base64.b64encode(ciphertext_body).decode("utf-8"),
            payload_nonce_b64=base64.b64encode(payload_nonce).decode("utf-8"),
            payload_auth_tag_b64=base64.b64encode(payload_auth_tag).decode("utf-8"),
            recipient_blocks=recipient_blocks,
        )

        return package

    @classmethod
    def decrypt_for_recipient(
        cls,
        package: EncryptedPackage,
        recipient_id: str,
        recipient_kem_private_key_pem: str,
    ) -> Tuple[bytes, str]:
        """
        Decapsulates the document master key and decrypts the document payload.
        
        Returns:
            (decrypted_document_bytes, document_hash_sha3)
        Raises:
            PermissionError: If recipient is not authorized in this package.
            ValueError: If ciphertext or key unwrapping fails.
        """
        # Find recipient block
        target_block: Optional[RecipientKeyBlock] = None
        for block in package.recipient_blocks:
            if block.recipient_id == recipient_id:
                target_block = block
                break

        if not target_block:
            raise PermissionError(
                f"Access Denied: Recipient '{recipient_id}' is not an authorized recipient of package {package.package_id}"
            )

        # 1. Decapsulate post-quantum shared secret using recipient's ML-KEM-768 private key
        kem_priv = PQCKeyManager.deserialize_kem_private_key(recipient_kem_private_key_pem)
        kem_ciphertext = base64.b64decode(target_block.kem_ciphertext_b64)
        shared_secret = PQCKeyManager.kem_decapsulate(kem_priv, kem_ciphertext)

        # 2. Derive wrapping key
        wrapping_key = cls._derive_wrapping_key(shared_secret, recipient_id)
        wrap_aesgcm = AESGCM(wrapping_key)
        wrap_nonce = base64.b64decode(target_block.wrap_nonce_b64)
        wrapped_doc_key = base64.b64decode(target_block.wrapped_doc_key_b64)
        wrap_aad = f"wrap:{package.document_id}:{recipient_id}".encode("utf-8")

        # 3. Unwrap master_doc_key
        try:
            master_doc_key = wrap_aesgcm.decrypt(wrap_nonce, wrapped_doc_key, wrap_aad)
        except Exception as e:
            raise ValueError(f"Cryptographic key unwrap failed: {e}")

        # 4. Decrypt master document payload
        payload_aesgcm = AESGCM(master_doc_key)
        payload_nonce = base64.b64decode(package.payload_nonce_b64)
        ciphertext_body = base64.b64decode(package.encrypted_payload_b64)
        auth_tag = base64.b64decode(package.payload_auth_tag_b64)
        full_ciphertext = ciphertext_body + auth_tag
        payload_aad = f"{package.document_id}:{package.classification_level}:{package.sender_id}".encode("utf-8")

        try:
            decrypted_bytes = payload_aesgcm.decrypt(payload_nonce, full_ciphertext, payload_aad)
        except Exception as e:
            raise ValueError(f"Document payload decryption failed: {e}")

        # 5. Verify unencrypted document hash against package header
        computed_hash = HashUtil.sha3_256(decrypted_bytes)
        if computed_hash != package.document_hash_sha3:
            raise ValueError(
                f"Document integrity mismatch! Expected {package.document_hash_sha3}, got {computed_hash}"
            )

        return decrypted_bytes, computed_hash
