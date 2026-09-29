"""
Document Distributor (Sender Workflow)
Performs multi-recipient hybrid broadcast encryption using NIST FIPS 203 ML-KEM-768
and authenticated AES-256-GCM.
"""

import os
from typing import List, Optional
from ..crypto.pki import AirGappedPKI
from ..crypto.envelope import BroadcastEnvelope, EncryptedPackage


class DocumentDistributor:
    """Manages the creation and distribution of broadcast-encrypted classified packages."""

    def __init__(self, pki: AirGappedPKI):
        self.pki = pki

    def create_package(
        self,
        document_bytes: bytes,
        document_id: str,
        document_title: str,
        sender_id: str,
        recipient_ids: List[str],
        classification_level: str = "TOP SECRET // NOFORN",
    ) -> EncryptedPackage:
        """
        Encrypts a document once and encapsulates the key for each authorized recipient officer.
        """
        recipients_pki_info = []
        for r_id in recipient_ids:
            officer = self.pki.get_officer(r_id)
            if not officer:
                raise ValueError(f"Officer '{r_id}' not found in Air-Gapped PKI directory")
            recipients_pki_info.append({
                "recipient_id": officer.officer_id,
                "officer_name": officer.name,
                "kem_public_key_pem": officer.kem_public_key_pem,
            })

        package = BroadcastEnvelope.encrypt_for_recipients(
            document_bytes=document_bytes,
            document_id=document_id,
            document_title=document_title,
            sender_id=sender_id,
            classification_level=classification_level,
            recipients_pki_info=recipients_pki_info,
        )

        return package

    def save_package_to_file(self, package: EncryptedPackage, file_path: str):
        """Write the encrypted package (.modpkg) to an offline file."""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(package.to_json())

    @staticmethod
    def load_package_from_file(file_path: str) -> EncryptedPackage:
        """Read an encrypted package (.modpkg) from disk."""
        with open(file_path, "r", encoding="utf-8") as f:
            return EncryptedPackage.from_json(f.read())
