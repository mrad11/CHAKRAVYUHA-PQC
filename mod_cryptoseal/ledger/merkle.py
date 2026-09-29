"""
Cryptographic Merkle Tree Implementation with Inclusion Proof Verification
Provides mathematical proof that an individual Decryption Provenance Record
was committed to a specific block in the immutable blockchain.
"""

from typing import List, Dict, Optional, Tuple
from ..crypto.pqc import HashUtil


class MerkleProof:
    """Represents an inclusion proof (audit path) for a transaction in a Merkle tree."""

    def __init__(self, leaf_index: int, leaf_hash: str, proof_path: List[Dict[str, str]]):
        self.leaf_index = leaf_index
        self.leaf_hash = leaf_hash
        self.proof_path = proof_path  # List of {"position": "left"|"right", "hash": "..."}

    def to_dict(self) -> Dict:
        return {
            "leaf_index": self.leaf_index,
            "leaf_hash": self.leaf_hash,
            "proof_path": self.proof_path,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "MerkleProof":
        return cls(
            leaf_index=data["leaf_index"],
            leaf_hash=data["leaf_hash"],
            proof_path=data["proof_path"],
        )

    def verify(self, expected_root: str) -> bool:
        """Verify this inclusion proof against an expected Merkle root."""
        current = bytes.fromhex(self.leaf_hash)
        for step in self.proof_path:
            sibling = bytes.fromhex(step["hash"])
            if step["position"] == "left":
                current = HashUtil.sha3_256_bytes(sibling + current)
            else:
                current = HashUtil.sha3_256_bytes(current + sibling)
        return current.hex().lower() == expected_root.lower()


class MerkleTree:
    """Constructs and queries binary SHA3-256 Merkle trees."""

    def __init__(self, leaf_data: List[bytes]):
        self.leaves = [HashUtil.sha3_256_bytes(d) for d in leaf_data]
        self.levels: List[List[bytes]] = []
        if self.leaves:
            self._build_tree()

    def _build_tree(self):
        current_level = self.leaves
        self.levels.append(current_level)
        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                right = current_level[i + 1] if i + 1 < len(current_level) else left
                parent = HashUtil.sha3_256_bytes(left + right)
                next_level.append(parent)
            current_level = next_level
            self.levels.append(current_level)

    @property
    def root(self) -> str:
        """Return the hexadecimal Merkle root."""
        if not self.levels or not self.levels[-1]:
            return HashUtil.sha3_256(b"EMPTY_MERKLE_TREE")
        return self.levels[-1][0].hex()

    def get_proof(self, index: int) -> Optional[MerkleProof]:
        """Generate an audit path inclusion proof for the leaf at index."""
        if index < 0 or index >= len(self.leaves):
            return None

        leaf_hash = self.leaves[index].hex()
        path = []
        current_idx = index

        for level in self.levels[:-1]:
            is_right = (current_idx % 2 == 1)
            sibling_idx = current_idx - 1 if is_right else current_idx + 1
            if sibling_idx >= len(level):
                sibling_idx = current_idx  # Duplicated odd leaf
            sibling_hash = level[sibling_idx].hex()
            position = "left" if is_right else "right"
            path.append({"position": position, "hash": sibling_hash})
            current_idx //= 2

        return MerkleProof(leaf_index=index, leaf_hash=leaf_hash, proof_path=path)
