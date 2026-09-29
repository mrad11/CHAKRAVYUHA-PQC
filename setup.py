from setuptools import setup, find_packages

setup(
    name="chakravyuha-pqc",
    version="1.0.0",
    description="Sovereign Post-Quantum Cryptographic Attribution and Immutable Decryption Provenance Enclave",
    author="CHAKRAVYUHA Defense Team",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "cryptography>=41.0.0",
        "pycryptodome>=3.19.0",
        "numpy>=1.24.0",
        "Pillow>=10.0.0",
        "pymupdf>=1.23.0",
        "pywebview>=4.4.1",
        "bottle>=0.12.25",
    ],
    entry_points={
        "console_scripts": [
            "chakravyuha=mod_cryptoseal.cli:main",
        ],
    },
)
