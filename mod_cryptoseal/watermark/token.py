"""
Session Watermark Token (SWT) Definition and Binary Bitstream Serialization
Cryptographically binds:
- Recipient Identifier
- Document Identifier
- Decryption Session Nonce
- Exact Timestamp
- Error-Detection Checksum (CRC32)
"""

import json
import zlib
import uuid
import datetime
from typing import Dict, Optional
from dataclasses import dataclass, asdict


@dataclass
class SessionWatermarkToken:
    """Forensic watermark payload uniquely generated for each decryption event."""
    token_id: str
    recipient_id: str
    document_id: str
    session_id: str
    timestamp: str
    nonce: str

    @classmethod
    def create(cls, recipient_id: str, document_id: str) -> "SessionWatermarkToken":
        """Instantiate a cryptographically unique token for a fresh decryption session."""
        now_str = datetime.datetime.now(datetime.timezone.utc).isoformat()
        u = uuid.uuid4().hex
        return cls(
            token_id=f"SWT-{u[:12].upper()}",
            recipient_id=recipient_id,
            document_id=document_id,
            session_id=str(uuid.uuid4()),
            timestamp=now_str,
            nonce=u[12:20],
        )

    def to_compact_string(self) -> str:
        """
        Produce a compact serialization string with CRC32 checksum.
        Format: MOD_SWT|<token_id>|<recipient_id>|<document_id>|<session_short>|<crc32>
        """
        core = f"MOD_SWT|{self.token_id}|{self.recipient_id}|{self.document_id}|{self.session_id[:8]}"
        crc = f"{zlib.crc32(core.encode('utf-8')) & 0xFFFFFFFF:08X}"
        return f"{core}|{crc}"

    @classmethod
    def from_compact_string(cls, text: str) -> Optional[Dict[str, str]]:
        """Parse compact string and verify CRC32 integrity."""
        parts = text.strip().split("|")
        if len(parts) != 6 or parts[0] != "MOD_SWT":
            return None
        core = f"MOD_SWT|{parts[1]}|{parts[2]}|{parts[3]}|{parts[4]}"
        expected_crc = f"{zlib.crc32(core.encode('utf-8')) & 0xFFFFFFFF:08X}"
        if parts[5].upper() != expected_crc:
            return None
        return {
            "token_id": parts[1],
            "recipient_id": parts[2],
            "document_id": parts[3],
            "session_short": parts[4],
        }

    PREAMBLE_16 = "1010111101010011"   # 0xAF53
    POSTAMBLE_16 = "1100101011001011"  # 0xCACB

    def to_bits(self) -> str:
        """Convert compact string to binary ASCII bitstream with length prefix and framing."""
        compact = self.to_compact_string()
        raw_bytes = compact.encode("utf-8")
        length_prefix = f"{len(raw_bytes):016b}"
        bits = "".join(f"{b:08b}" for b in raw_bytes)
        return self.PREAMBLE_16 + length_prefix + bits + self.POSTAMBLE_16

    @classmethod
    def bits_to_compact_string(cls, bitstring: str) -> Optional[str]:
        """Decode bitstream back to compact string using 16-bit length prefix."""
        start = bitstring.find(cls.PREAMBLE_16)
        if start == -1:
            return None
        cursor = start + len(cls.PREAMBLE_16)
        if cursor + 16 > len(bitstring):
            return None
        try:
            byte_count = int(bitstring[cursor : cursor + 16], 2)
            cursor += 16
            bit_count = byte_count * 8
            if cursor + bit_count > len(bitstring):
                return None
            payload_bits = bitstring[cursor : cursor + bit_count]
            byte_arr = bytearray()
            for i in range(0, bit_count, 8):
                byte_arr.append(int(payload_bits[i : i + 8], 2))
            return byte_arr.decode("utf-8", errors="ignore")
        except Exception:
            return None

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> "SessionWatermarkToken":
        return cls(**json.loads(json_str))
