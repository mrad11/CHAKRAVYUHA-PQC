"""
PDF-Level Invisible Forensic Steganography
Dual-Mechanism Digital Watermarking:
1. Micro-typographical Unicode Zero-Width Steganography embedded directly in text stream using
   PDF specification Render Mode 3 (Neither fill nor stroke - completely invisible to human viewers).
2. Structural Catalog Object Stream Steganography stored in the low-level PDF Document Catalog.
"""

import pymupdf
from typing import Optional, Dict
from .token import SessionWatermarkToken


class PDFStego:
    """Embeds and extracts forensic session watermarks at the PDF document level."""

    # Zero-width Unicode mappings
    ZW_START = "\uFEFF"  # Byte Order Mark / Zero Width No-Break Space
    ZW_ZERO = "\u200B"   # Zero Width Space
    ZW_ONE = "\u200C"    # Zero Width Non-Joiner
    ZW_END = "\u200D"    # Zero Width Joiner

    @classmethod
    def _bits_to_zero_width(cls, bitstring: str) -> str:
        """Convert a binary bitstring into invisible zero-width Unicode characters."""
        result = [cls.ZW_START]
        for bit in bitstring:
            if bit == "0":
                result.append(cls.ZW_ZERO)
            elif bit == "1":
                result.append(cls.ZW_ONE)
        result.append(cls.ZW_END)
        return "".join(result)

    @classmethod
    def _zero_width_to_bits(cls, text: str) -> Optional[str]:
        """Scan text for zero-width characters and reconstruct the binary bitstring."""
        start_idx = text.find(cls.ZW_START)
        if start_idx == -1:
            return None
        end_idx = text.find(cls.ZW_END, start_idx)
        if end_idx == -1:
            return None

        segment = text[start_idx + len(cls.ZW_START) : end_idx]
        bits = []
        for ch in segment:
            if ch == cls.ZW_ZERO:
                bits.append("0")
            elif ch == cls.ZW_ONE:
                bits.append("1")

        return "".join(bits)

    @classmethod
    def embed(cls, pdf_bytes: bytes, token: SessionWatermarkToken) -> bytes:
        """
        Embed forensic watermark invisibly into the PDF.
        Returns:
            Watermarked PDF bytes (visually identical, forensically distinct).
        """
        doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")

        # 1. Structural Catalog Injection
        try:
            catalog_xref = doc.pdf_catalog()
            compact_token = token.to_compact_string()
            # Store in low-level PDF catalog
            doc.xref_set_key(catalog_xref, "CryptoSealProvenance", f"({compact_token})")
        except Exception:
            pass

        # 2. Document Metadata Tag
        try:
            meta = doc.metadata or {}
            existing_keywords = meta.get("keywords", "")
            mod_tag = f"CSPROC:{token.token_id}:{token.recipient_id}"
            new_keywords = f"{existing_keywords} {mod_tag}".strip()
            doc.set_metadata({**meta, "keywords": new_keywords})
        except Exception:
            pass

        # 3. Micro-typographical Invisible Text Injection
        bitstring = token.to_bits()
        zw_payload = cls._bits_to_zero_width(bitstring)

        # Inject across pages with Render Mode 3 (Invisible)
        for page_idx in range(len(doc)):
            page = doc[page_idx]
            rect = page.rect
            # Position invisibly near the margin
            point = pymupdf.Point(rect.width / 2, rect.height - 20)
            page.insert_text(
                point,
                f" {zw_payload} ",
                fontsize=0.01,
                render_mode=3,  # Official PDF spec: Invisible text
            )

        output_bytes = doc.tobytes(garbage=3, deflate=True)
        doc.close()
        return output_bytes

    @classmethod
    def extract(cls, pdf_bytes: bytes) -> Optional[Dict[str, str]]:
        """
        Extract forensic watermark from digital PDF bytes.
        Returns:
            Dict containing token_id, recipient_id, document_id, session_short if valid, else None.
        """
        try:
            doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
        except Exception:
            return None

        # Strategy A: Check low-level catalog
        try:
            catalog_xref = doc.pdf_catalog()
            val = doc.xref_get_key(catalog_xref, "CryptoSealProvenance")
            if val and val[0] == "string":
                parsed = SessionWatermarkToken.from_compact_string(val[1])
                if parsed:
                    doc.close()
                    return parsed
        except Exception:
            pass

        # Strategy B: Scan text streams for Unicode Zero-Width payload
        for page_idx in range(len(doc)):
            page = doc[page_idx]
            text = page.get_text()
            bits = cls._zero_width_to_bits(text)
            if bits:
                compact_str = SessionWatermarkToken.bits_to_compact_string(bits)
                if compact_str:
                    parsed = SessionWatermarkToken.from_compact_string(compact_str)
                    if parsed:
                        doc.close()
                        return parsed

        # Strategy C: Check PDF metadata keywords
        try:
            meta = doc.metadata or {}
            keywords = meta.get("keywords", "")
            for word in keywords.split():
                if word.startswith("CSPROC:"):
                    parts = word.split(":")
                    if len(parts) >= 3:
                        doc.close()
                        return {
                            "token_id": parts[1],
                            "recipient_id": parts[2],
                            "document_id": "UNKNOWN",
                            "session_short": "METADATA",
                        }
        except Exception:
            pass

        doc.close()
        return None
