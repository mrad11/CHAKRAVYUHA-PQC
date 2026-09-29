# Security Policy: CHAKRAVYUHA PQC

## 1. Cryptographic Boundary & Threat Model
CHAKRAVYUHA PQC is engineered for mission-critical military operations in **100% air-gapped, zero-trust environments**.
The system is hardened against:
- **Quantum Cryptanalytic Attacks**: Implements NIST FIPS 203 (ML-KEM-768) and FIPS 204 (ML-DSA-65) to protect against *Harvest Now, Decrypt Later* (HNDL) attacks.
- **Rogue Insider Collusion**: Employs session-unique steganography and consortium PoA blockchain anchoring.
- **Tampering & Repudiation**: Mandatory digital signatures on Decryption Provenance Records (DPR) before payload rendering.
- **Memory Scrubbing**: Immediate in-memory wiping of decrypted plaintext buffers upon session termination.

## 2. Supported Versions
| Version | Supported | Cryptographic Standard |
| :--- | :--- | :--- |
| 1.0.x | Yes | NIST FIPS 203 (ML-KEM) & FIPS 204 (ML-DSA) |

## 3. Reporting a Vulnerability
To report a security vulnerability or cryptographic anomaly, submit an issue to the project repository or coordinate via the designated Ministry of Defence defense innovation portal.
