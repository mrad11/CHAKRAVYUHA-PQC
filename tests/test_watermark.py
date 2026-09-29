"""
Unit Tests for Dual-Layer Forensic Watermarking (PDF & Visual)
"""

import unittest
from PIL import Image
import pymupdf
from mod_cryptoseal.watermark.token import SessionWatermarkToken
from mod_cryptoseal.watermark.pdf_stego import PDFStego
from mod_cryptoseal.watermark.visual_stego import VisualStego
from mod_cryptoseal.watermark.engine import WatermarkEngine
from mod_cryptoseal.watermark.extractor import WatermarkExtractor


class TestWatermarking(unittest.TestCase):

    def setUp(self):
        self.token = SessionWatermarkToken.create("IND-MOD-002", "DOC-SECRET-01")

        # Create dummy PDF
        doc = pymupdf.open()
        p = doc.new_page()
        p.insert_text(pymupdf.Point(50, 50), "Classified Operational Directives", fontsize=12)
        self.sample_pdf_bytes = doc.tobytes()
        doc.close()

    def test_token_bitstream_serialization(self):
        compact = self.token.to_compact_string()
        self.assertIn("MOD_SWT|", compact)
        
        # Verify parse and CRC32
        parsed = SessionWatermarkToken.from_compact_string(compact)
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed["token_id"], self.token.token_id)
        self.assertEqual(parsed["recipient_id"], self.token.recipient_id)

        # Bitstream encode/decode
        bits = self.token.to_bits()
        decoded_compact = SessionWatermarkToken.bits_to_compact_string(bits)
        self.assertEqual(compact, decoded_compact)

    def test_pdf_stego_roundtrip(self):
        wm_pdf = PDFStego.embed(self.sample_pdf_bytes, self.token)
        self.assertGreater(len(wm_pdf), 0)

        extracted = PDFStego.extract(wm_pdf)
        self.assertIsNotNone(extracted)
        self.assertEqual(extracted["token_id"], self.token.token_id)
        self.assertEqual(extracted["recipient_id"], self.token.recipient_id)

    def test_visual_stego_roundtrip(self):
        img = Image.new("RGB", (600, 800), color=(255, 255, 255))
        stego_img = VisualStego.embed_on_image(img, self.token)
        
        extracted = VisualStego.extract_from_image(stego_img)
        self.assertIsNotNone(extracted)
        self.assertEqual(extracted["token_id"], self.token.token_id)
        self.assertEqual(extracted["recipient_id"], self.token.recipient_id)

    def test_universal_extractor(self):
        # 1. Test full PDF
        wm_pdf = WatermarkEngine.apply_watermark(self.sample_pdf_bytes, self.token)
        res_pdf = WatermarkExtractor.extract_from_file_or_bytes(wm_pdf)
        self.assertIsNotNone(res_pdf)
        self.assertEqual(res_pdf["token_id"], self.token.token_id)

        # 2. Test rendered raster screenshot
        doc = pymupdf.open(stream=wm_pdf, filetype="pdf")
        pix = doc[0].get_pixmap(dpi=150)
        img_bytes = pix.tobytes("png")
        doc.close()

        res_img = WatermarkExtractor.extract_from_file_or_bytes(img_bytes)
        self.assertIsNotNone(res_img)
        self.assertEqual(res_img["token_id"], self.token.token_id)


if __name__ == "__main__":
    unittest.main()
