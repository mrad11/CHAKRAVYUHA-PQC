"""
Air-Gapped Public Key Infrastructure (PKI) and Secure Keystore Manager
Designed for strictly offline Ministry of Defence environments.
Zero dependency on external cloud KMS services or internet PKI roots.
"""

import os
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from .pqc import PQCKeyManager, HashUtil


@dataclass
class OfficerIdentity:
    """Identity record containing PQC public and private keypairs for an authorized officer."""
    officer_id: str
    name: str
    rank: str
    division: str
    clearance_level: str
    kem_public_key_pem: str
    kem_private_key_pem: str
    dsa_public_key_pem: str
    dsa_private_key_pem: str
    created_at: str

    def to_public_dict(self) -> Dict[str, str]:
        """Return public information suitable for the broadcast directory."""
        return {
            "recipient_id": self.officer_id,
            "officer_name": self.name,
            "rank": self.rank,
            "division": self.division,
            "clearance_level": self.clearance_level,
            "kem_public_key_pem": self.kem_public_key_pem,
            "dsa_public_key_pem": self.dsa_public_key_pem,
            "dsa_fingerprint": HashUtil.sha256(self.dsa_public_key_pem.encode("utf-8"))[:16],
        }

    def to_dict(self) -> Dict[str, str]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "OfficerIdentity":
        return cls(**data)


class AirGappedPKI:
    """
    Offline Identity and Keystore Authority.
    Manages generation, storage, and retrieval of Post-Quantum keys for cleared personnel.
    """

    def __init__(self, storage_dir: Optional[str] = None):
        self.storage_dir = storage_dir
        self.officers: Dict[str, OfficerIdentity] = {}
        if storage_dir and os.path.exists(storage_dir):
            self.load()

    def register_officer(
        self,
        officer_id: str,
        name: str,
        rank: str,
        division: str,
        clearance_level: str = "TOP SECRET // NOFORN",
    ) -> OfficerIdentity:
        """Generate Post-Quantum (ML-KEM-768 + ML-DSA-65) credentials for a new officer."""
        import datetime

        # 1. Generate NIST FIPS 203 ML-KEM-768 keypair
        kem_priv, kem_pub = PQCKeyManager.generate_kem_keypair()
        kem_priv_pem = PQCKeyManager.serialize_kem_private_key(kem_priv)
        kem_pub_pem = PQCKeyManager.serialize_kem_public_key(kem_pub)

        # 2. Generate NIST FIPS 204 ML-DSA-65 keypair
        dsa_priv, dsa_pub = PQCKeyManager.generate_dsa_keypair()
        dsa_priv_pem = PQCKeyManager.serialize_dsa_private_key(dsa_priv)
        dsa_pub_pem = PQCKeyManager.serialize_dsa_public_key(dsa_pub)

        identity = OfficerIdentity(
            officer_id=officer_id,
            name=name,
            rank=rank,
            division=division,
            clearance_level=clearance_level,
            kem_public_key_pem=kem_pub_pem,
            kem_private_key_pem=kem_priv_pem,
            dsa_public_key_pem=dsa_pub_pem,
            dsa_private_key_pem=dsa_priv_pem,
            created_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        )

        self.officers[officer_id] = identity
        if self.storage_dir:
            self.save()
        return identity

    def get_officer(self, officer_id: str) -> Optional[OfficerIdentity]:
        """Retrieve full officer record including private keys from secure keystore."""
        return self.officers.get(officer_id)

    def get_public_directory(self) -> List[Dict[str, str]]:
        """Return public directory of all authorized officers for broadcast distribution."""
        return [officer.to_public_dict() for officer in self.officers.values()]

    def save(self):
        """Persist offline PKI keystores to disk."""
        if not self.storage_dir:
            return
        os.makedirs(self.storage_dir, exist_ok=True)
        path = os.path.join(self.storage_dir, "pki_store.json")
        data = {oid: off.to_dict() for oid, off in self.officers.items()}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load(self):
        """Load offline PKI keystores from disk."""
        if not self.storage_dir:
            return
        path = os.path.join(self.storage_dir, "pki_store.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.officers = {oid: OfficerIdentity.from_dict(d) for oid, d in data.items()}

    def seed_default_defence_personnel(self):
        """Initialize standard high-ranking Ministry of Defence officers for simulation."""
        if not self.officers:
            self.register_officer(
                officer_id="IND-MOD-001",
                name="Col. Arvind Sharma",
                rank="Colonel",
                division="Directorate of Military Operations (DMO)",
                clearance_level="COSMIC TOP SECRET",
            )
            self.register_officer(
                officer_id="IND-MOD-002",
                name="Brig. Rajesh Verma",
                rank="Brigadier",
                division="Defence Cyber Agency (DCA)",
                clearance_level="TOP SECRET // EYES ONLY",
            )
            self.register_officer(
                officer_id="IND-MOD-003",
                name="Maj. Priya Nair",
                rank="Major",
                division="Military Intelligence Directorate (MI-8)",
                clearance_level="TOP SECRET // STRATCOM",
            )
            self.register_officer(
                officer_id="IND-MOD-004",
                name="Cmde. Sunil Vohra",
                rank="Commodore",
                division="Naval Strategic Operations Group",
                clearance_level="COSMIC TOP SECRET",
            )
            if self.storage_dir:
                self.save()
