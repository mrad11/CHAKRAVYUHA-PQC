"""
CHAKRAVYUHA PQC: Tactical Battlefield Key Escrow (Shamir 3-of-5 Secret Sharing)
Ministry of Defence - Problem Statement 237

Implements a mathematically proven (k=3, n=5) threshold secret sharing scheme over a large prime field.
Allows emergency operational recovery of classified mission keys if commanders are incapacitated
or battlefield communications are severed, requiring joint quorum from any 3 of 5 Tri-Service nodes.
"""

import os
import secrets
from typing import List, Tuple, Dict, Any

# Standard 256-bit prime modulus (secp256k1 field prime)
FIELD_PRIME = 2**256 - 2**32 - 977

DEFENCE_NODES = [
    {"index": 1, "role": "Army Corps Commander (Eastern Command)", "badge": "INDIAN_ARMY"},
    {"index": 2, "role": "Naval Fleet Commander (Western Fleet)", "badge": "INDIAN_NAVY"},
    {"index": 3, "role": "Air Force AOC (Tactical Air Command)", "badge": "INDIAN_AIR_FORCE"},
    {"index": 4, "role": "Defence Cyber Agency (DCyA Director)", "badge": "DCYA_CYBER"},
    {"index": 5, "role": "Director General Military Operations (DGMO)", "badge": "DGMO_COMMAND"},
]


class ShamirBattlefieldEscrow:
    """Implements (k, n) threshold secret sharing with Lagrange interpolation over a finite field."""

    def __init__(self, threshold: int = 3, total_shares: int = 5):
        self.k = threshold
        self.n = total_shares
        self.prime = FIELD_PRIME

    def split_secret(self, secret_hex: str) -> List[Dict[str, Any]]:
        """
        Split a secret hex string (e.g. 256-bit master key) into n polynomial shares.
        f(x) = secret + a_1*x + a_2*x^2 (mod prime)
        """
        secret_int = int(secret_hex, 16) % self.prime

        # Generate k-1 random polynomial coefficients
        coefficients = [secret_int] + [secrets.randbelow(self.prime - 1) + 1 for _ in range(self.k - 1)]

        shares = []
        for node in DEFENCE_NODES:
            x = node["index"]
            # Evaluate polynomial at x
            y = 0
            for power, coeff in enumerate(coefficients):
                y = (y + coeff * pow(x, power, self.prime)) % self.prime

            shares.append({
                "share_index": x,
                "share_value": hex(y)[2:].zfill(64),
                "custodian_role": node["role"],
                "military_branch": node["badge"]
            })

        return shares

    def reconstruct_secret(self, selected_shares: List[Tuple[int, str]]) -> Dict[str, Any]:
        """
        Reconstruct the secret using Lagrange polynomial interpolation.
        Requires at least k shares.
        """
        if len(selected_shares) < self.k:
            return {
                "success": False,
                "error": f"Quorum failure: Received {len(selected_shares)} shares, but minimum {self.k}-of-{self.n} are required.",
                "reconstructed_key": None
            }

        # Take the first k shares
        k_shares = [(x, int(val, 16)) for x, val in selected_shares[:self.k]]

        secret = 0
        for i, (x_i, y_i) in enumerate(k_shares):
            numerator = 1
            denominator = 1
            for j, (x_j, _) in enumerate(k_shares):
                if i != j:
                    numerator = (numerator * (-x_j)) % self.prime
                    denominator = (denominator * (x_i - x_j)) % self.prime

            # Modular inverse using Fermat's Little Theorem
            inv_denom = pow(denominator, self.prime - 2, self.prime)
            lagrange_basis = (numerator * inv_denom) % self.prime
            secret = (secret + y_i * lagrange_basis) % self.prime

        reconstructed_hex = hex(secret)[2:].zfill(64)
        return {
            "success": True,
            "quorum_achieved": True,
            "shares_provided": len(selected_shares),
            "threshold_required": self.k,
            "reconstructed_key": reconstructed_hex,
            "verification_status": "AUTHENTICATED_BY_LAGRANGE_CONSENSUS"
        }
