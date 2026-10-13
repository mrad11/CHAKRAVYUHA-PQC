"""
Unit Tests for CHAKRAVYUHA PQC Elite Defence Capabilities (MoD PS 237)
Tests:
- Hardware TPM 2.0 Silicon Attestation & PCR Sealing
- Shamir 3-of-5 Battlefield Key Escrow
- Zero-Knowledge Attribution Proofs (zk-SNARKs)
- Mathematical Tardos Anti-Collusion Fingerprinting
- Semantic Honeytoken Context-Bait Scanner
- Quantum vs Classical Performance Benchmarking
- Computer Vision 2D FFT Moiré Suppression & Dewarping
"""

import unittest
import os
import numpy as np
from PIL import Image

from mod_cryptoseal.crypto.tpm_enclave import HardwareTPMEnclave
from mod_cryptoseal.crypto.shamir_escrow import ShamirBattlefieldEscrow
from mod_cryptoseal.crypto.zk_proof import ZeroKnowledgeAttributionEngine
from mod_cryptoseal.crypto.benchmark import QuantumPerformanceBenchmark
from mod_cryptoseal.watermark.tardos import TardosAntiCollusionEngine
from mod_cryptoseal.engine.cv_dewarp import ComputerVisionDeWarper
from mod_cryptoseal.engine.honeytoken import SemanticHoneytokenEngine


class TestEliteFeatures(unittest.TestCase):

    def test_01_tpm_hardware_enclave(self):
        tpm = HardwareTPMEnclave()
        telemetry = tpm.get_hardware_telemetry()
        self.assertTrue(telemetry["tpm_ready"])
        self.assertIn("PCR_7_SECURE_BOOT", telemetry["pcrs"])
        self.assertIn("composite_pcr_digest", telemetry)

        # Test key sealing to PCR 7
        key = os.urandom(32)
        pcr7 = telemetry["pcrs"]["PCR_7_SECURE_BOOT"]
        ticket = tpm.seal_key_to_tpm(key, pcr7)
        self.assertEqual(ticket["status"], "SEALED_IN_SILICON")
        self.assertTrue(tpm.unseal_key(ticket, pcr7))
        self.assertFalse(tpm.unseal_key(ticket, "TAMPERED_PCR_VALUE"))

    def test_02_shamir_3_of_5_escrow(self):
        escrow = ShamirBattlefieldEscrow(threshold=3, total_shares=5)
        secret = os.urandom(32).hex()
        shares = escrow.split_secret(secret)
        self.assertEqual(len(shares), 5)

        # 3 shares must succeed
        subset_3 = [(s["share_index"], s["share_value"]) for s in shares[:3]]
        rec_3 = escrow.reconstruct_secret(subset_3)
        self.assertTrue(rec_3["success"])
        self.assertEqual(int(rec_3["reconstructed_key"], 16), int(secret, 16))

        # 2 shares must fail (quorum violation)
        subset_2 = [(s["share_index"], s["share_value"]) for s in shares[:2]]
        rec_2 = escrow.reconstruct_secret(subset_2)
        self.assertFalse(rec_2["success"])

    def test_03_zero_knowledge_proof(self):
        doc_hash = "abc123def456"
        proof = ZeroKnowledgeAttributionEngine.generate_zk_proof(
            officer_name="Col. Rajesh Sharma",
            service_id="IND-ARMY-001",
            command_unit="WESTERN_COMMAND",
            clearance_grade="TOP_SECRET",
            target_document_hash=doc_hash
        )
        self.assertEqual(proof["status"], "VALID_VERIFIED")
        self.assertTrue(ZeroKnowledgeAttributionEngine.verify_zk_proof(proof, doc_hash))
        self.assertFalse(ZeroKnowledgeAttributionEngine.verify_zk_proof(proof, "WRONG_DOC_HASH"))

    def test_04_tardos_anti_collusion(self):
        engine = TardosAntiCollusionEngine(code_length=128, max_colluders=3)
        bias = engine.generate_bias_vector("TEST_SALT")
        cw1 = engine.generate_officer_codeword("Officer_A", bias)
        cw2 = engine.generate_officer_codeword("Officer_B", bias)
        cw3 = engine.generate_officer_codeword("Officer_C_Innocent", bias)

        # Collusion between A and B
        forged = engine.simulate_collusion_attack([cw1, cw2], strategy="majority")
        candidates = {"Officer_A": cw1, "Officer_B": cw2, "Officer_C_Innocent": cw3}
        result = engine.calculate_suspicion_scores(forged, bias, candidates, threshold=8.0)

        # Both A and B should have positive scores, C should be lower
        self.assertGreater(result["all_scores"]["Officer_A"], result["all_scores"]["Officer_C_Innocent"])
        self.assertGreater(result["all_scores"]["Officer_B"], result["all_scores"]["Officer_C_Innocent"])

    def test_05_semantic_honeytoken_scanner(self):
        leaked_call = "Source mentions 50 main battle tanks on 142.80 MHz tactical band."
        scan = SemanticHoneytokenEngine.scan_leaked_plaintext(leaked_call)
        self.assertTrue(scan["attribution_found"])
        self.assertEqual(scan["identified_culprit"], "Maj. Priya Nair")

    def test_06_quantum_micro_benchmark(self):
        bench = QuantumPerformanceBenchmark.run_benchmark_suite()
        self.assertIn("ml_kem_768", bench)
        self.assertIn("ml_dsa_65", bench)
        self.assertIn("rsa_4096", bench)
        self.assertGreater(bench["ml_kem_768"]["keygen_ms"], 0)

    def test_07_cv_dewarp_and_fft_filter(self):
        # Create synthetic test image
        img = Image.new("RGB", (200, 200), color="white")
        filtered, stats = ComputerVisionDeWarper.suppress_moire_fft_2d(img)
        self.assertEqual(stats["frequency_filter_type"], "2D_SPECTRAL_NOTCH")
        dewarped, gstats = ComputerVisionDeWarper.rectify_perspective_homography(img)
        self.assertEqual(gstats["homography_matrix"], "3x3_PLANAR_PERSPECTIVE")


if __name__ == "__main__":
    unittest.main()
