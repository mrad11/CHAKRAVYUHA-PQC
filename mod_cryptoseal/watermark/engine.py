"""
Forensic Watermark Embedding Engine
Orchestrates dual-layer invisible watermark embedding at the exact moment of decryption.
Guarantees that raw, unwatermarked document bytes are never released to the recipient client.
"""

import io
from typing import Tuple
from PIL import Image
import pymupdf
from .token import SessionWatermarkToken
from .pdf_stego import PDFStego
from .visual_stego import VisualStego


class WatermarkEngine:
    """Orchestrates forensic watermark embedding into documents upon decryption."""

    @classmethod
    def apply_watermark(
        cls,
        decrypted_pdf_bytes: bytes,
        token: SessionWatermarkToken,
    ) -> bytes:
        """
        Embeds dual-layer invisible forensic watermark into the PDF document:
        Layer 1: Structural catalog and zero-width text steganography.
        Layer 2: Visual blue-channel high-frequency modulation.
        
        Returns:
            Watermarked PDF bytes ready for recipient presentation.
        """
        # 1. Apply PDF structural and micro-typographical steganography
        watermarked_pdf = PDFStego.embed(decrypted_pdf_bytes, token)

        # 2. To ensure visual robustness against screenshotting,
        # open the document and apply the visual modulation pattern as an invisible layer
        doc = pymupdf.open(stream=watermarked_pdf, filetype="pdf")
        for page_idx in range(len(doc)):
            page = doc[page_idx]
            # Render page to pixmap to apply visual modulation
            pix = page.get_pixmap(dpi=150)
            pil_img = Image.open(io.BytesIO(pix.tobytes("png")))
            
            # Embed visual stego on page image
            stego_img = VisualStego.embed_on_image(pil_img, token)
            
            # Save watermarked image to bytes
            img_byte_arr = io.BytesIO()
            stego_img.save(img_byte_arr, format="PNG")
            
            # Overlay an imperceptible subtle visual background anchor on the page
            # Or insert the stego image as a background replacement
            rect = page.rect
            page.clean_contents()
            page.insert_image(rect, stream=img_byte_arr.getvalue())

        output_bytes = doc.tobytes(garbage=3, deflate=True)
        doc.close()
        return output_bytes
