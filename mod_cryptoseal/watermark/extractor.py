"""
Universal Forensic Watermark Extractor
Extracts embedded session watermarks from:
- Leaked PDF documents (via PDF structural and micro-typographical decoding)
- Leaked screenshots / photos / scans (via visual blue-channel differential demodulation)
"""

import io
from typing import Optional, Dict, Union
from PIL import Image
import pymupdf
from .pdf_stego import PDFStego
from .visual_stego import VisualStego


class WatermarkExtractor:
    """Forensic investigation engine for extracting session watermarks from leaked artifacts."""

    @classmethod
    def extract_from_file_or_bytes(
        cls,
        data_or_path: Union[str, bytes],
    ) -> Optional[Dict[str, str]]:
        """
        Extract watermark from either a file path or in-memory byte buffer.
        Automatically detects whether the artifact is a PDF or an image/screenshot.
        """
        raw_bytes: bytes
        if isinstance(data_or_path, str):
            with open(data_or_path, "rb") as f:
                raw_bytes = f.read()
        else:
            raw_bytes = data_or_path

        # 1. Test if artifact is a PDF
        if raw_bytes.startswith(b"%PDF-"):
            # Try digital PDF structural / micro-typographical extraction first
            pdf_result = PDFStego.extract(raw_bytes)
            if pdf_result:
                pdf_result["extraction_layer"] = "PDF_STRUCTURAL_STEGANOGRAPHY"
                return pdf_result

            # If digital steganography was stripped or flattened, render PDF pages and scan visual layer
            try:
                doc = pymupdf.open(stream=raw_bytes, filetype="pdf")
                for page_idx in range(min(3, len(doc))):
                    page = doc[page_idx]
                    pix = page.get_pixmap(dpi=150)
                    pil_img = Image.open(io.BytesIO(pix.tobytes("png")))
                    visual_result = VisualStego.extract_from_image(pil_img)
                    if visual_result:
                        doc.close()
                        visual_result["extraction_layer"] = "PDF_PAGE_RASTER_VISUAL"
                        return visual_result
                doc.close()
            except Exception:
                pass

        # 2. Test if artifact is an image / screenshot
        try:
            pil_img = Image.open(io.BytesIO(raw_bytes))
            visual_result = VisualStego.extract_from_image(pil_img)
            if visual_result:
                visual_result["extraction_layer"] = "IMAGE_SCREENSHOT_VISUAL"
                return visual_result
        except Exception:
            pass

        return None
