"""
Generates a realistic Ministry of Defence Top Secret Operational Briefing PDF.
"""

import os
import pymupdf


def generate_defence_sample_pdf(output_path: str):
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    doc = pymupdf.open()
    page = doc.new_page(width=595, height=842)  # Standard A4

    # Top Classification Banner
    page.draw_rect(pymupdf.Rect(0, 0, 595, 30), color=(0.7, 0.1, 0.1), fill=(0.7, 0.1, 0.1))
    page.insert_text(
        pymupdf.Point(140, 20),
        "TOP SECRET // RESTRICTED ACCESS // EYES ONLY",
        fontsize=11,
        color=(1, 1, 1),
    )

    # Header
    page.insert_text(
        pymupdf.Point(50, 60),
        "MINISTRY OF DEFENCE — GOVERNMENT OF INDIA",
        fontsize=14,
        color=(0.1, 0.1, 0.2),
    )
    page.insert_text(
        pymupdf.Point(50, 78),
        "HEADQUARTERS INTEGRATED DEFENCE STAFF | NEW DELHI",
        fontsize=9,
        color=(0.4, 0.4, 0.4),
    )
    page.draw_line(pymupdf.Point(50, 88), pymupdf.Point(545, 88), color=(0.2, 0.2, 0.3), width=1.5)

    # Document Metadata Box
    page.draw_rect(pymupdf.Rect(50, 98, 545, 168), color=(0.8, 0.8, 0.8), fill=(0.96, 0.96, 0.98))
    page.insert_text(pymupdf.Point(60, 115), "DOCUMENT IDENTIFIER: MOD-DOC-2026-OP-TRIDENT", fontsize=9, color=(0.1, 0.1, 0.1))
    page.insert_text(pymupdf.Point(60, 130), "CLASSIFICATION: COSMIC TOP SECRET // AIR-GAPPED DISTRIBUTION ONLY", fontsize=9, color=(0.7, 0.1, 0.1))
    page.insert_text(pymupdf.Point(60, 145), "ISSUING COMMAND: Joint Directorate of Strategic Cyber & Cryptographic Operations", fontsize=9, color=(0.2, 0.2, 0.2))
    page.insert_text(pymupdf.Point(60, 160), "EFFECTIVE DATE: 25 SEPTEMBER 2026 | CRYPTOGRAPHIC VALIDITY: 365 DAYS", fontsize=9, color=(0.2, 0.2, 0.2))

    # Subject & Directives
    page.insert_text(
        pymupdf.Point(50, 195),
        "SUBJECT: STRATEGIC CONTINGENCY PLAN 'TRIDENT SHIELD' (PHASE IV)",
        fontsize=12,
        color=(0.05, 0.1, 0.3),
    )

    content_lines = [
        "1. OPERATIONAL SITUATION & CONTEXT:",
        "   Hostile automated cyber reconnaissance and quantum-assisted algorithmic attacks against regional",
        "   critical defense infrastructure mandate immediate deployment of post-quantum resilient broadcast",
        "   encryption frameworks across all Joint Military Operations Command Centers.",
        "",
        "2. CRYPTOGRAPHIC GOVERNANCE DIRECTIVE:",
        "   All operational orders and tactical plans shall henceforth be distributed under NIST FIPS 203",
        "   (ML-KEM-768) key encapsulation and audited via NIST FIPS 204 (ML-DSA-65) post-quantum digital",
        "   signatures committed to an air-gapped, multi-validator Distributed Ledger Technology (DLT) network.",
        "",
        "3. ATTRIBUTION AND NON-REPUDIATION PROTOCOL:",
        "   Every individual officer decryption is bound to a forensic, session-unique invisible watermark.",
        "   In the event of an unauthorized document extraction, screenshot, or digital breach, forensic extraction",
        "   engines will match the physical and structural artifacts to the officer's non-repudiable signature.",
        "",
        "4. DESIGNATED STRATEGIC TARGET NODES:",
        "   - Sector Alpha (Naval EW Radar Array): Operational status 100% encrypted.",
        "   - Sector Bravo (Air Defence Early Warning Grid): Post-quantum key rollover active.",
        "   - Sector Charlie (Strategic Command Fiber Link): Tamper-evident optical telemetry engaged.",
        "",
        "5. ENFORCEMENT & COMPLIANCE:",
        "   Any leak shall result in immediate cryptographic attribution, court-martial proceedings, and",
        "   permanent revocation of national security clearances under the Official Secrets Act.",
    ]

    y_pos = 220
    for line in content_lines:
        if line.startswith("1.") or line.startswith("2.") or line.startswith("3.") or line.startswith("4.") or line.startswith("5."):
            page.insert_text(pymupdf.Point(50, y_pos), line, fontsize=10, color=(0.1, 0.1, 0.2))
            y_pos += 16
        else:
            page.insert_text(pymupdf.Point(50, y_pos), line, fontsize=9, color=(0.25, 0.25, 0.25))
            y_pos += 14

    # Signoff Block
    page.draw_rect(pymupdf.Rect(50, 710, 545, 770), color=(0.85, 0.85, 0.85), fill=(0.98, 0.98, 0.98))
    page.insert_text(pymupdf.Point(60, 730), "AUTHORIZING SIGNATORY:", fontsize=9, color=(0.2, 0.2, 0.2))
    page.insert_text(pymupdf.Point(60, 745), "Vice Admiral S. K. Mehta, PVSM, AVSM", fontsize=10, color=(0.1, 0.1, 0.2))
    page.insert_text(pymupdf.Point(60, 760), "Deputy Chief of Integrated Defence Staff (Policy, Planning & Force Development)", fontsize=8, color=(0.4, 0.4, 0.4))

    # Bottom Banner
    page.draw_rect(pymupdf.Rect(0, 812, 595, 842), color=(0.7, 0.1, 0.1), fill=(0.7, 0.1, 0.1))
    page.insert_text(
        pymupdf.Point(140, 830),
        "TOP SECRET // RESTRICTED ACCESS // EYES ONLY",
        fontsize=11,
        color=(1, 1, 1),
    )

    doc.save(output_path, garbage=3, deflate=True)
    doc.close()
    print(f"Sample Defence PDF successfully created at: {output_path}")


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "DEFENCE_OPERATION_TRIDENT.pdf")
    generate_defence_sample_pdf(out)
