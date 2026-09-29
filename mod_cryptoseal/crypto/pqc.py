"""
NIST Post-Quantum Cryptography Core Implementation
Compliant with:
- NIST FIPS 203 (ML-KEM-768): Module-Lattice-Based Key-Encapsulation Mechanism
- NIST FIPS 204 (ML-DSA-65): Module-Lattice-Based Digital Signature Standard
All operations run offline and air-gapped using hardware-grade Rust-backed primitives.
"""

import os
import hashlib
import hmac
from typing import Tuple, Optional
from cryptography.hazmat.primitives.asymmetric import mlkem, mldsa
from cryptography.hazmat.primitives import serialization


class HashUtil:
    """Standardized cryptographic hashing utility for air-gapped defense workflows."""

    @staticmethod
    def sha3_256(data: bytes) -> str:
        """Compute SHA3-256 hexadecimal digest."""
        h = hashlib.sha3_256()
        h.update(data)
        return h.hexdigest()

    @staticmethod
    def sha3_256_bytes(data: bytes) -> bytes:
        """Compute SHA3-256 raw bytes."""
        h = hashlib.sha3_256()
        h.update(data)
        return h.digest()

    @staticmethod
    def sha256(data: bytes) -> str:
        """Compute SHA-256 hexadecimal digest."""
        h = hashlib.sha256()
        h.update(data)
        return h.hexdigest()

    @staticmethod
    def sha256_bytes(data: bytes) -> bytes:
        """Compute SHA-256 raw bytes."""
        h = hashlib.sha256()
        h.update(data)
        return h.digest()

    @staticmethod
    def hmac_sha256(key: bytes, message: bytes) -> bytes:
        """Compute HMAC-SHA256 for message integrity."""
        return hmac.new(key, message, hashlib.sha256).digest()

    @staticmethod
    def constant_time_compare(val1: bytes, val2: bytes) -> bool:
        """Perform constant-time comparison to prevent timing attacks."""
        return hmac.compare_digest(val1, val2)


class PQCKeyManager:
    """Manages NIST Post-Quantum Key Encapsulation (ML-KEM-768) and Digital Signatures (ML-DSA-65)."""

    # -------------------------------------------------------------
    # NIST FIPS 203: ML-KEM-768 (Key Encapsulation Mechanism)
    # -------------------------------------------------------------

    @staticmethod
    def generate_kem_keypair() -> Tuple[mlkem.MLKEM768PrivateKey, mlkem.MLKEM768PublicKey]:
        """Generate a new NIST FIPS 203 ML-KEM-768 keypair."""
        private_key = mlkem.MLKEM768PrivateKey.generate()
        public_key = private_key.public_key()
        return private_key, public_key

    @staticmethod
    def kem_encapsulate(public_key: mlkem.MLKEM768PublicKey) -> Tuple[bytes, bytes]:
        """
        Encapsulate a symmetric key against an ML-KEM-768 public key.
        Returns:
            (shared_secret: 32 bytes, ciphertext: 1088 bytes)
        """
        shared_secret, ciphertext = public_key.encapsulate()
        return shared_secret, ciphertext

    @staticmethod
    def kem_decapsulate(private_key: mlkem.MLKEM768PrivateKey, ciphertext: bytes) -> bytes:
        """
        Decapsulate the shared symmetric key using the recipient's ML-KEM-768 private key.
        Returns:
            shared_secret: 32 bytes
        """
        return private_key.decapsulate(ciphertext)

    @staticmethod
    def serialize_kem_public_key(public_key: mlkem.MLKEM768PublicKey) -> str:
        """Serialize ML-KEM public key to PEM string."""
        pem_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        return pem_bytes.decode("utf-8")

    @staticmethod
    def deserialize_kem_public_key(pem_str: str) -> mlkem.MLKEM768PublicKey:
        """Deserialize ML-KEM public key from PEM string."""
        key = serialization.load_pem_public_key(pem_str.encode("utf-8"))
        if not isinstance(key, mlkem.MLKEM768PublicKey):
            raise TypeError(f"Expected MLKEM768PublicKey, got {type(key)}")
        return key

    @staticmethod
    def serialize_kem_private_key(private_key: mlkem.MLKEM768PrivateKey) -> str:
        """Serialize ML-KEM private key to PKCS#8 PEM string."""
        pem_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        return pem_bytes.decode("utf-8")

    @staticmethod
    def deserialize_kem_private_key(pem_str: str) -> mlkem.MLKEM768PrivateKey:
        """Deserialize ML-KEM private key from PKCS#8 PEM string."""
        key = serialization.load_pem_private_key(pem_str.encode("utf-8"), password=None)
        if not isinstance(key, mlkem.MLKEM768PrivateKey):
            raise TypeError(f"Expected MLKEM768PrivateKey, got {type(key)}")
        return key

    # -------------------------------------------------------------
    # NIST FIPS 204: ML-DSA-65 (Digital Signature Standard)
    # -------------------------------------------------------------

    @staticmethod
    def generate_dsa_keypair() -> Tuple[mldsa.MLDSA65PrivateKey, mldsa.MLDSA65PublicKey]:
        """Generate a new NIST FIPS 204 ML-DSA-65 keypair."""
        private_key = mldsa.MLDSA65PrivateKey.generate()
        public_key = private_key.public_key()
        return private_key, public_key

    @staticmethod
    def dsa_sign(private_key: mldsa.MLDSA65PrivateKey, data: bytes) -> bytes:
        """Sign arbitrary data using recipient's ML-DSA-65 private key."""
        return private_key.sign(data)

    @staticmethod
    def dsa_verify(public_key: mldsa.MLDSA65PublicKey, signature: bytes, data: bytes) -> bool:
        """
        Verify an ML-DSA-65 digital signature.
        Returns True if valid, False if invalid.
        """
        try:
            public_key.verify(signature, data)
            return True
        except Exception:
            return False

    @staticmethod
    def serialize_dsa_public_key(public_key: mldsa.MLDSA65PublicKey) -> str:
        """Serialize ML-DSA public key to PEM string."""
        pem_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        return pem_bytes.decode("utf-8")

    @staticmethod
    def deserialize_dsa_public_key(pem_str: str) -> mldsa.MLDSA65PublicKey:
        """Deserialize ML-DSA public key from PEM string."""
        key = serialization.load_pem_public_key(pem_str.encode("utf-8"))
        if not isinstance(key, mldsa.MLDSA65PublicKey):
            raise TypeError(f"Expected MLDSA65PublicKey, got {type(key)}")
        return key

    @staticmethod
    def serialize_dsa_private_key(private_key: mldsa.MLDSA65PrivateKey) -> str:
        """Serialize ML-DSA private key to PKCS#8 PEM string."""
        pem_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        return pem_bytes.decode("utf-8")

    @staticmethod
    def deserialize_dsa_private_key(pem_str: str) -> mldsa.MLDSA65PrivateKey:
        """Deserialize ML-DSA private key from PKCS#8 PEM string."""
        key = serialization.load_pem_private_key(pem_str.encode("utf-8"), password=None)
        if not isinstance(key, mldsa.MLDSA65PrivateKey):
            raise TypeError(f"Expected MLDSA65PrivateKey, got {type(key)}")
        return key
