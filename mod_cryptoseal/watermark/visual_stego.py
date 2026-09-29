"""
Visual / Raster Invisible Forensic Watermarking
Designed for screenshots, photographed printouts, and rasterized leaked pages.
Uses imperceptible high-frequency differential modulation in the Blue channel
(leveraging the human eye's minimal sensitivity to high-frequency blue channel variations).
Features multi-quadrant redundancy and Barker-sequence synchronization for robust recovery.
"""

import io
from typing import Optional, Dict, Tuple, List
import numpy as np
from PIL import Image
from .token import SessionWatermarkToken


class VisualStego:
    """
    Embeds and extracts forensic session watermarks at the pixel / image level.
    Resistant to screenshotting, PNG/JPEG export, and document viewer clipping.
    """

    # 16-bit Barker synchronization sequence (0xFA3A)
    BARKER_SYNC = "1111101000111010"
    STEP_Y = 3
    STEP_X = 1
    DELTA = 2  # Imperceptible 2-level difference out of 255

    @classmethod
    def _encode_payload(cls, token: SessionWatermarkToken) -> str:
        """Construct full bitstream: Sync Barker code + compact token bitstream + Postamble."""
        compact = token.to_compact_string()
        raw_bytes = compact.encode("utf-8")
        token_bits = "".join(f"{b:08b}" for b in raw_bytes)
        # Total bits = len(SYNC) + 16-bit length prefix + token_bits
        length_prefix = f"{len(token_bits):016b}"
        return cls.BARKER_SYNC + length_prefix + token_bits

    @classmethod
    def embed_on_image(cls, image: Image.Image, token: SessionWatermarkToken) -> Image.Image:
        """
        Embed forensic watermark into an image invisibly.
        Returns a new PIL Image with forensic watermarks replicated across quadrants.
        """
        img_arr = np.array(image.convert("RGB"), dtype=np.uint8)
        h, w, _ = img_arr.shape

        bitstream = cls._encode_payload(token)
        total_bits = len(bitstream)

        # We embed the redundant stream in 4 quadrant anchor points
        anchors = [
            (20, 20),                     # Top-left margin
            (20, max(20, w - 80)),        # Top-right margin
            (max(20, h - 300), 20),       # Bottom-left margin
            (max(20, h - 300), max(20, w - 80)), # Bottom-right margin
        ]

        for start_y, start_x in anchors:
            avail_h = max(20, h - start_y - 10)
            avail_w = max(10, w - start_x - 10)
            for i, bit in enumerate(bitstream):
                y = start_y + (i * cls.STEP_Y) % avail_h
                x_offset = ((i * cls.STEP_Y) // avail_h) * 4
                x = min(w - 2, start_x + (x_offset % avail_w))

                curr_val = int(img_arr[y, x, 2])
                # If pixel is near pure white (> 250), modulate downwards
                # If pixel is dark (< 10), modulate upwards
                if curr_val > 128:
                    if bit == "1":
                        img_arr[y, x, 2] = max(0, curr_val - cls.DELTA)
                        img_arr[y, x + 1, 2] = curr_val
                    else:
                        img_arr[y, x, 2] = curr_val
                        img_arr[y, x + 1, 2] = max(0, curr_val - cls.DELTA)
                else:
                    if bit == "1":
                        img_arr[y, x, 2] = min(255, curr_val + cls.DELTA)
                        img_arr[y, x + 1, 2] = curr_val
                    else:
                        img_arr[y, x, 2] = curr_val
                        img_arr[y, x + 1, 2] = min(255, curr_val + cls.DELTA)

        return Image.fromarray(img_arr)

    @classmethod
    def extract_from_image(cls, image: Image.Image) -> Optional[Dict[str, str]]:
        """
        Extract forensic watermark from an image or screenshot.
        Scans anchors and demodulates the Blue-channel differential signal.
        """
        img_arr = np.array(image.convert("RGB"), dtype=np.uint8)
        h, w, _ = img_arr.shape

        anchors = [
            (20, 20),
            (20, max(20, w - 80)),
            (max(20, h - 300), 20),
            (max(20, h - 300), max(20, w - 80)),
        ]

        # Scan each anchor
        for start_y, start_x in anchors:
            avail_h = max(20, h - start_y - 10)
            avail_w = max(10, w - start_x - 10)
            extracted_bits = []
            max_scan = min(1500, (avail_h // cls.STEP_Y) * (avail_w // 4) * 2)
            if max_scan < 50:
                max_scan = 500

            for i in range(max_scan):
                y = start_y + (i * cls.STEP_Y) % avail_h
                x_offset = ((i * cls.STEP_Y) // avail_h) * 4
                x = min(w - 2, start_x + (x_offset % avail_w))

                pA = int(img_arr[y, x, 2])
                pB = int(img_arr[y, x + 1, 2])

                if pA > 128 or pB > 128:
                    bit = "1" if pA < pB else "0"
                else:
                    bit = "1" if pA > pB else "0"
                extracted_bits.append(bit)

            bitstring = "".join(extracted_bits)
            sync_pos = bitstring.find(cls.BARKER_SYNC)
            if sync_pos != -1:
                cursor = sync_pos + len(cls.BARKER_SYNC)
                if cursor + 16 <= len(bitstring):
                    try:
                        length_bits = bitstring[cursor : cursor + 16]
                        payload_length = int(length_bits, 2)
                        cursor += 16
                        if cursor + payload_length <= len(bitstring) and payload_length > 0:
                            payload_bits = bitstring[cursor : cursor + payload_length]
                            # Convert bits to bytes
                            byte_arr = bytearray()
                            for b_idx in range(0, len(payload_bits), 8):
                                chunk = payload_bits[b_idx : b_idx + 8]
                                if len(chunk) == 8:
                                    byte_arr.append(int(chunk, 2))
                            compact_str = byte_arr.decode("utf-8", errors="ignore")
                            parsed = SessionWatermarkToken.from_compact_string(compact_str)
                            if parsed:
                                return parsed
                    except Exception:
                        continue

        return None
