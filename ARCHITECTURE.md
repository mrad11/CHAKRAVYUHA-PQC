# CHAKRAVYUHA PQC: System Architecture Specification

## 1. Overview
CHAKRAVYUHA PQC solves the critical military dilemma of **broadcast-encrypted multi-recipient document distribution** in 100% air-gapped environments. When a classified document is shared with multiple officers and subsequently leaked, traditional systems cannot prove which recipient leaked the copy. CHAKRAVYUHA binds every decryption event to a mathematical, immutable provenance chain.

---

## 2. Architectural Layers

### Layer 1: Mission Command Dashboard (Frontend)
- **Tech Stack**: PyWebView (Native Desktop Window), HTML5, Tailwind CSS, Canvas API.
- **Capabilities**:
  - Encryptor Terminal: Encapsulates `.pdf`, `.docx`, `.png` into multi-recipient `.modpkg` envelopes.
  - Decryption Guard: Authenticates officer credentials, enforces biometric/key clearance, and renders watermarked documents.
  - Forensic Attribution Studio: Extracts hidden steganographic tokens from leaked documents and verifies them against the blockchain.

### Layer 2: Cryptographic Engine (Backend)
- **Tech Stack**: Python 3.11, NIST FIPS 203 (ML-KEM-768), NIST FIPS 204 (ML-DSA-65), AES-256-GCM.
- **Capabilities**:
  - Broadcast Key Encapsulation: Generates single master symmetric key encrypted for N recipients via post-quantum lattices.
  - Atomic Decryption Boundary: Enforces DPR signing before the document plaintext is decrypted in memory.
  - Dual-Layer Steganography:
    - Structural PDF Layer: Render Mode 3 (Neither fill nor stroke) + Unicode zero-width sequences.
    - Spatial Blue-Channel Layer: High-frequency differential modulation with Barker-16 synchronization (`0xFA3A`) for screenshot/camera photo resistance.

### Layer 3: Immutable Distributed Ledger Layer (DLT)
- **Tech Stack**: SHA3-256 Merkle DAG, Proof-of-Authority (PoA) Consortium Blockchain.
- **Capabilities**:
  - Multi-Validator Consensus: 3 military validator nodes (Directorate of Military Operations, Defence Cyber Agency, Integrated Defence Staff).
  - Tamper Detection: Detects any retroactive record deletion or alteration instantly.
  - Merkle Inclusion Proofs: Provides cryptographic verification of individual decryption events.

### Layer 4: User & Operational Layer
- **Tech Stack**: Air-Gapped PKI Keystore, Role-Based Access Control (RBAC), Hardware TPM 2.0 Enclave binding.
- **Capabilities**:
  - 100% offline operability with zero internet or intranet requirements.
  - Section 65B electronic evidence certification under the Indian Evidence Act / Bharatiya Sakshya Adhiniyam, 2023.
