# Contributing to CHAKRAVYUHA PQC

We welcome defense researchers, cryptographic engineers, and military IT specialists to contribute to **CHAKRAVYUHA PQC**.

## Development Workflow
1. Fork the repository and create a feature branch (`git checkout -b feature/defense-enclave-enhancement`).
2. Ensure all 11 automated test suites pass with 100% compliance (`pytest tests/`).
3. Adhere to strict air-gapped constraints:
   - **Zero External Sockets**: No external network listeners or phone-home telemetry.
   - **Deterministic Lattice Math**: Strict adherence to NIST FIPS 203 & FIPS 204.
   - **Memory Purging**: All decrypted buffers must be zeroized upon session completion.
4. Commit your changes with clear, semantic commit messages.
5. Submit a Pull Request for review by the security oversight committee.
