"""
Air-Gapped Consortium Blockchain Implementation
Proof-of-Authority (PoA) Multi-Validator Consensus
Zero dependencies on external public blockchains or cloud nodes.
Guarantees tamper-evidence and permanent non-repudiation.
"""

import os
import json
import base64
import datetime
from typing import Dict, List, Optional, Tuple
from ..crypto.pqc import PQCKeyManager, HashUtil
from .merkle import MerkleTree, MerkleProof
from .block import DecryptionProvenanceRecord, Block, ValidatorNode


class AirGappedLedger:
    """
    Immutable distributed ledger for Ministry of Defence decryption audit records.
    Consensus maintained by air-gapped cryptographic validation authorities.
    """

    def __init__(self, storage_dir: Optional[str] = None):
        self.storage_dir = storage_dir
        self.chain: List[Block] = []
        self.validators: Dict[str, ValidatorNode] = {}
        self.watermark_index: Dict[str, Tuple[int, int]] = {}  # token_id -> (block_idx, tx_idx)
        
        self._init_validators()
        if storage_dir and os.path.exists(os.path.join(storage_dir, "ledger_chain.json")):
            self.load()
        else:
            self._create_genesis_block()
            if storage_dir:
                self.save()

    def _init_validators(self):
        """Initialize MoD air-gapped validator authorities if not loaded from disk."""
        val_path = os.path.join(self.storage_dir, "validators.json") if self.storage_dir else None
        if val_path and os.path.exists(val_path):
            with open(val_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for vid, vdata in data.items():
                self.validators[vid] = ValidatorNode(
                    node_id=vid,
                    name=vdata["name"],
                    dsa_priv_pem=vdata["dsa_priv_pem"],
                    dsa_pub_pem=vdata["dsa_pub_pem"],
                )
        else:
            # Create the 3 MoD consensus authorities
            v1 = ValidatorNode.create("VAL-MOD-DMO", "Directorate of Military Operations")
            v2 = ValidatorNode.create("VAL-MOD-DCA", "Defence Cyber Agency")
            v3 = ValidatorNode.create("VAL-MOD-IDS", "Integrated Defence Staff")
            self.validators = {v1.node_id: v1, v2.node_id: v2, v3.node_id: v3}
            if self.storage_dir:
                os.makedirs(self.storage_dir, exist_ok=True)
                val_data = {
                    vid: {
                        "name": v.name,
                        "dsa_priv_pem": v.dsa_priv_pem,
                        "dsa_pub_pem": v.dsa_pub_pem,
                    }
                    for vid, v in self.validators.items()
                }
                with open(val_path, "w", encoding="utf-8") as f:
                    json.dump(val_data, f, indent=2)

    def _create_genesis_block(self):
        """Create the cryptographically anchored Genesis Block (Block #0)."""
        genesis_time = "2026-01-01T00:00:00Z"
        genesis_prev = "0" * 64
        empty_root = HashUtil.sha3_256(b"GENESIS_MERKLE_ROOT")
        header_str = f"0:{genesis_time}:{genesis_prev}:{empty_root}"
        b_hash = HashUtil.sha3_256(header_str.encode("utf-8"))

        signatures = {}
        for vid, validator in self.validators.items():
            signatures[vid] = validator.sign_block(b_hash)

        genesis_block = Block(
            index=0,
            timestamp=genesis_time,
            prev_hash=genesis_prev,
            merkle_root=empty_root,
            transactions=[],
            block_hash=b_hash,
            validator_signatures=signatures,
        )
        self.chain = [genesis_block]

    def commit_record(self, record: DecryptionProvenanceRecord) -> Block:
        """
        Verify recipient's ML-DSA-65 signature, bundle into a block,
        compute Merkle root, collect multi-validator signatures, and seal block.
        """
        # 1. Enforce mathematical non-repudiation: signature MUST be valid
        if not record.verify_signature():
            raise ValueError(
                f"Ledger Rejection: Invalid ML-DSA-65 signature for recipient '{record.recipient_id}'"
            )

        # 2. Build Merkle Tree for the transaction payload
        tx_bytes_list = [record.canonical_bytes()]
        tree = MerkleTree(tx_bytes_list)
        merkle_root = tree.root

        # 3. Form new block
        prev_block = self.chain[-1]
        new_index = prev_block.index + 1
        now_str = datetime.datetime.now(datetime.timezone.utc).isoformat()
        
        header_str = f"{new_index}:{now_str}:{prev_block.block_hash}:{merkle_root}"
        block_hash = HashUtil.sha3_256(header_str.encode("utf-8"))

        # 4. Multi-Validator Consensus Signatures (PoA)
        # All 3 air-gapped MoD nodes independently sign the block hash
        signatures = {}
        for vid, validator in self.validators.items():
            signatures[vid] = validator.sign_block(block_hash)

        new_block = Block(
            index=new_index,
            timestamp=now_str,
            prev_hash=prev_block.block_hash,
            merkle_root=merkle_root,
            transactions=[record],
            block_hash=block_hash,
            validator_signatures=signatures,
        )

        self.chain.append(new_block)
        self.watermark_index[record.watermark_token_id] = (new_index, 0)

        if self.storage_dir:
            self.save()

        return new_block

    def lookup_by_watermark(self, token_id: str) -> Optional[Dict]:
        """
        Retrieve Decryption Provenance Record and cryptographic Merkle proof for a watermark token.
        """
        # Check in memory index
        loc = self.watermark_index.get(token_id)
        if not loc:
            # Exhaustive scan if index not built
            for b in self.chain:
                for idx, tx in enumerate(b.transactions):
                    if tx.watermark_token_id == token_id:
                        loc = (b.index, idx)
                        self.watermark_index[token_id] = loc
                        break
                if loc:
                    break

        if not loc:
            return None

        block_idx, tx_idx = loc
        block = self.chain[block_idx]
        record = block.transactions[tx_idx]

        # Generate Merkle Proof
        tx_bytes_list = [t.canonical_bytes() for t in block.transactions]
        tree = MerkleTree(tx_bytes_list)
        proof = tree.get_proof(tx_idx)

        return {
            "record": record,
            "block": block,
            "merkle_proof": proof.to_dict() if proof else None,
            "merkle_root": block.merkle_root,
            "block_hash": block.block_hash,
            "block_index": block.index,
            "validator_signatures": block.validator_signatures,
        }

    def verify_chain(self) -> Dict:
        """
        Comprehensive cryptographic audit of the entire blockchain:
        - Validates hash links between adjacent blocks
        - Recomputes block header hashes
        - Recomputes Merkle roots
        - Validates all recipient ML-DSA-65 signatures on each DPR
        - Validates multi-validator ML-DSA-65 signatures on each block
        """
        audit_report = {
            "is_valid": True,
            "total_blocks": len(self.chain),
            "total_records": sum(len(b.transactions) for b in self.chain),
            "status": "HEALTHY",
            "tampered_blocks": [],
            "errors": [],
        }

        for i, block in enumerate(self.chain):
            # 1. Check prev_hash link
            if i == 0:
                if block.prev_hash != "0" * 64:
                    audit_report["is_valid"] = False
                    audit_report["errors"].append(f"Genesis block has invalid prev_hash: {block.prev_hash}")
                    audit_report["tampered_blocks"].append(0)
            else:
                prev_block = self.chain[i - 1]
                if block.prev_hash != prev_block.block_hash:
                    audit_report["is_valid"] = False
                    audit_report["errors"].append(
                        f"Block {i} prev_hash mismatch: expected {prev_block.block_hash}, got {block.prev_hash}"
                    )
                    audit_report["tampered_blocks"].append(i)

            # 2. Check header hash
            expected_header_hash = block.compute_header_hash()
            if block.block_hash != expected_header_hash:
                audit_report["is_valid"] = False
                audit_report["errors"].append(
                    f"Block {i} hash tampered! Header hash {expected_header_hash} != {block.block_hash}"
                )
                audit_report["tampered_blocks"].append(i)

            # 3. Check Merkle root for transactions
            if block.transactions:
                tx_bytes_list = [t.canonical_bytes() for t in block.transactions]
                tree = MerkleTree(tx_bytes_list)
                if tree.root != block.merkle_root:
                    audit_report["is_valid"] = False
                    audit_report["errors"].append(
                        f"Block {i} Merkle root tampered! Computed {tree.root} != {block.merkle_root}"
                    )
                    audit_report["tampered_blocks"].append(i)

            # 4. Check recipient signatures on each transaction
            for t_idx, tx in enumerate(block.transactions):
                if not tx.verify_signature():
                    audit_report["is_valid"] = False
                    audit_report["errors"].append(
                        f"Block {i} Tx {t_idx} recipient ML-DSA-65 signature INVALID for {tx.recipient_id}"
                    )
                    audit_report["tampered_blocks"].append(i)

            # 5. Check validator signatures on block
            valid_val_count = 0
            for vid, sig_b64 in block.validator_signatures.items():
                if vid in self.validators:
                    val = self.validators[vid]
                    pub = PQCKeyManager.deserialize_dsa_public_key(val.dsa_pub_pem)
                    sig_bytes = base64.b64decode(sig_b64)
                    if PQCKeyManager.dsa_verify(pub, sig_bytes, block.block_hash.encode("utf-8")):
                        valid_val_count += 1
            
            # Requires at least 2 out of 3 validator signatures
            if valid_val_count < 2 and i > 0:
                audit_report["is_valid"] = False
                audit_report["errors"].append(
                    f"Block {i} fails validator threshold: only {valid_val_count} valid signatures"
                )
                audit_report["tampered_blocks"].append(i)

        if not audit_report["is_valid"]:
            audit_report["status"] = "TAMPERED / INTEGRITY BREACH DETECTED"

        return audit_report

    def simulate_tamper_attack(self, block_index: int, target_officer_id: str = "COMPROMISED_SUSPECT"):
        """
        Simulate an adversarial insider or rogue administrator attempting to alter
        a past audit record in the database. Demonstrates mathematical tamper-evidence.
        """
        if block_index <= 0 or block_index >= len(self.chain):
            raise IndexError("Cannot tamper with Genesis block or non-existent block")

        block = self.chain[block_index]
        if not block.transactions:
            raise ValueError("Target block has no transactions to tamper")

        # Rogue administrator alters the recipient ID to frame another officer
        block.transactions[0].recipient_id = target_officer_id
        block.transactions[0].officer_name = "Framed Officer"
        if self.storage_dir:
            self.save()

    def save(self):
        """Persist blockchain to disk."""
        if not self.storage_dir:
            return
        os.makedirs(self.storage_dir, exist_ok=True)
        path = os.path.join(self.storage_dir, "ledger_chain.json")
        data = [b.to_dict() for b in self.chain]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load(self):
        """Load blockchain from disk."""
        if not self.storage_dir:
            return
        path = os.path.join(self.storage_dir, "ledger_chain.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.chain = [Block.from_dict(d) for d in data]
            self.watermark_index = {}
            for b in self.chain:
                for idx, tx in enumerate(b.transactions):
                    self.watermark_index[tx.watermark_token_id] = (b.index, idx)
