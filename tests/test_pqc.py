"""
Unit Tests for NIST Post-Quantum Cryptography (FIPS 203 & FIPS 204)
"""

import unittest
from mod_cryptoseal.crypto.pqc import PQCKeyManager, HashUtil


class TestPQC(unittest.TestCase):

    def test_mlkem768_key_exchange(self):
        # 1. Keypair generation
        priv, pub = PQCKeyManager.generate_kem_keypair()
        self.assertIsNotNone(priv)
        self.assertIsNotNone(pub)

        # 2. Encapsulation
        shared_secret_sender, ciphertext = PQCKeyManager.kem_encapsulate(pub)
        self.assertEqual(len(shared_secret_sender), 32)
        self.assertEqual(len(ciphertext), 1088)

        # 3. Decapsulation
        shared_secret_recipient = PQCKeyManager.kem_decapsulate(priv, ciphertext)
        self.assertEqual(shared_secret_sender, shared_secret_recipient)

    def test_mlkem768_serialization(self):
        priv, pub = PQCKeyManager.generate_kem_keypair()
        
        # Serialize to PEM
        pub_pem = PQCKeyManager.serialize_kem_public_key(pub)
        priv_pem = PQCKeyManager.serialize_kem_private_key(priv)
        self.assertTrue(pub_pem.startswith("-----BEGIN PUBLIC KEY-----"))
        self.assertTrue(priv_pem.startswith("-----BEGIN PRIVATE KEY-----"))

        # Deserialize from PEM
        re_pub = PQCKeyManager.deserialize_kem_public_key(pub_pem)
        re_priv = PQCKeyManager.deserialize_kem_private_key(priv_pem)

        # Verify functionality of reloaded keys
        ss_sender, ct = PQCKeyManager.kem_encapsulate(re_pub)
        ss_recip = PQCKeyManager.kem_decapsulate(re_priv, ct)
        self.assertEqual(ss_sender, ss_recip)

    def test_mldsa65_digital_signatures(self):
        priv, pub = PQCKeyManager.generate_dsa_keypair()
        message = b"MILITARY_DECRYPTION_AUDIT_RECORD_CANONICAL_PAYLOAD"

        # Sign
        sig = PQCKeyManager.dsa_sign(priv, message)
        self.assertIsInstance(sig, bytes)
        self.assertGreater(len(sig), 1000)

        # Verify
        is_valid = PQCKeyManager.dsa_verify(pub, sig, message)
        self.assertTrue(is_valid)

        # Tampered message must fail
        tampered_msg = b"MILITARY_DECRYPTION_AUDIT_RECORD_CANONICAL_PAYLOAD_TAMPERED"
        is_tampered_valid = PQCKeyManager.dsa_verify(pub, sig, tampered_msg)
        self.assertFalse(is_tampered_valid)

    def test_mldsa65_serialization(self):
        priv, pub = PQCKeyManager.generate_dsa_keypair()
        pub_pem = PQCKeyManager.serialize_dsa_public_key(pub)
        priv_pem = PQCKeyManager.serialize_dsa_private_key(priv)

        re_pub = PQCKeyManager.deserialize_dsa_public_key(pub_pem)
        re_priv = PQCKeyManager.deserialize_dsa_private_key(priv_pem)

        msg = b"TEST_RELOADED_SIGNATURE"
        sig = PQCKeyManager.dsa_sign(re_priv, msg)
        self.assertTrue(PQCKeyManager.dsa_verify(re_pub, sig, msg))


if __name__ == "__main__":
    unittest.main()
