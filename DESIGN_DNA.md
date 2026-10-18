# DESIGN DNA : CHAKRAVYUHA PQC

```json
{
  "seed": 796,
  "app_name": "CHAKRAVYUHA",
  "picks": {
    "hue_story": { "index": 4, "name": "Ultraviolet Dusk [D]", "formula": "(796 * 3) mod 16 = 4" },
    "material": { "index": 8, "name": "Velvet Matte", "formula": "(796 * 5) mod 12 = 8" },
    "light_model": { "index": 8, "name": "Inner-Lit (Luminescent Core)", "formula": "(796 * 2) mod 9 = 8" },
    "motion": { "index": 4, "name": "Magnetic (Elastic Spring)", "formula": "(796 * 5) mod 8 = 4" },
    "signature_object": { "index": 8, "name": "Vault Mechanism (Concentric Chakravyuha Rings)", "formula": "(796 * 3) mod 14 = 8" },
    "texture": { "index": 8, "name": "Engraved Hatching & Guilloche Security Linework", "formula": "(796 * 3) mod 10 = 8" },
    "shape_language": { "index": 1, "name": "Cut-Corner Chamfers & Hardware Enclave Notches", "formula": "Repaired from 8 for military hardware enclave compliance" },
    "layout_archetype": { "index": 6, "name": "Cinematic Full-Bleed (Floating Tactical HUD)", "formula": "(796 * 2) mod 13 = 6" },
    "type_pairing": { "index": 4, "name": "Fraunces / Figtree / IBM Plex Mono", "formula": "(796 * 4) mod 15 = 4" }
  },
  "tokens": {
    "canvas_base": "oklch(0.160 0.040 298)",
    "canvas_surface": "oklch(0.220 0.060 298)",
    "canvas_sunken": "oklch(0.130 0.030 298)",
    "border_subtle": "oklch(0.280 0.050 298)",
    "border_focus": "oklch(0.750 0.180 170)",
    "accent_seafoam": "oklch(0.780 0.160 170)",
    "accent_seafoam_hover": "oklch(0.840 0.180 170)",
    "highlight_rose": "oklch(0.680 0.240 350)",
    "text_primary": "oklch(0.940 0.020 298)",
    "text_secondary": "oklch(0.750 0.040 298)",
    "text_muted": "oklch(0.550 0.050 298)",
    "status_threat_crimson": "oklch(0.580 0.240 22)",
    "status_verified_jade": "oklch(0.740 0.170 155)"
  },
  "motion": {
    "duration_instant": 90,
    "duration_fast": 140,
    "duration_base": 220,
    "duration_deliberate": 360,
    "duration_ceremony": 900,
    "spring_stiffness": 380,
    "spring_damping": 26,
    "spring_mass": 0.8
  }
}
```

## Fingerprint & Concept
* **Fingerprint Line:** 4 (Ultraviolet Dusk) x 8 (Velvet Matte) x 8 (Inner-Lit) x 4 (Magnetic) x 8 (Vault Mechanism) x 8 (Engraved Hatching) x 1 (Chamfered Hardware) x 6 (Cinematic Full-Bleed) x 4 (Fraunces / Figtree / IBM Plex Mono).
* **Concept & Central Metaphor:** An impenetrable, multi-tiered concentric defense fortress derived from the ancient Vedic labyrinth *Chakravyuha*, resurrected as a post-quantum lattice cryptographic enclave. The core is not a generic dashboard, but an inner-lit kinetic vault whose interlocking rings rotate and align with incoming lattice signatures, projecting quantum states onto a velvet matte tactile HUD.
* **Identity in Words:** Velvet-matte light-absorbing deep amethyst ground illuminated solely by internal seafoam luminescence and rare electric orchid highlights. Chamfered military hardware modules hover weightlessly over an interactive Three.js concentric vault mechanism, patterned with microscopic guilloche security hatching that acts as an optical anti-tamper watermark.
* **Personal Security Glyph:** A generative, 12-segment rotating SVG talisman derived from the officer's TPM 2.0 PCR-7 public key hash, rendering a unique mathematical emblem on every trusted surface.
* **The Wow Detail:** **Interactive 4D Kinetic Chakravyuha Vault Core (Three.js WebGL)** with real-time time-travel scrubbing, where drag-rotating the vault scrub bar rewinds the Merkle lattice timeline and decomposes post-quantum ciphertext envelopes layer by layer.

## Palette Table
| Name | Role | OKLCH | Hex (sRGB) | Contrast vs Base |
|---|---|---|---|---|
| `canvas_base` | App Ground / Void | `oklch(0.160 0.040 298)` | `#10091c` | 1:1 |
| `canvas_surface` | Tactical HUD Panels | `oklch(0.220 0.060 298)` | `#1e1332` | 1.5:1 |
| `canvas_sunken` | Data Matrix Well | `oklch(0.130 0.030 298)` | `#090512` | 1.2:1 |
| `border_subtle` | Enclave Hairlines | `oklch(0.280 0.050 298)` | `#2c233e` | 2.1:1 |
| `border_focus` | Active Tactical Focus | `oklch(0.750 0.180 170)` | `#00d19c` | 8.2:1 (AAA) |
| `accent_seafoam` | Primary Kinetic Action | `oklch(0.780 0.160 170)` | `#00d7a8` | 8.8:1 (AAA) |
| `highlight_rose` | Rare Signature Highlight | `oklch(0.680 0.240 350)` | `#fb40ad` | 5.6:1 (AA) |
| `text_primary` | High-Clearance Typography | `oklch(0.940 0.020 298)` | `#ece9f7` | 14.4:1 (AAA) |
| `text_secondary` | Metadata / Telemetry | `oklch(0.750 0.040 298)` | `#b1a9c5` | 7.6:1 (AAA) |
| `text_muted` | Passive Labels | `oklch(0.550 0.050 298)` | `#756c8b` | 3.8:1 (AA Large) |
| `status_threat_crimson` | Lattice Intrusion Alert | `oklch(0.580 0.240 22)` | `#e60031` | 4.9:1 (AA) |
| `status_verified_jade` | Quantum Seal Valid | `oklch(0.740 0.170 155)` | `#2ec97a` | 7.9:1 (AAA) |

## Anti-Sameness Audit
* **Obvious Look 1 (Navy Blue Crypto Dashboard):** Replaced completely by chromatic Ultraviolet Dusk (`#10091c`) with inner-lit Seafoam (`#00d7a8`).
* **Obvious Look 2 (Neon Cyberpunk Green Terminal):** Replaced with refined Velvet Matte materials and high-contrast Fraunces/Figtree typography.
* **Obvious Look 3 (White Minimal SaaS Card Grid):** Replaced with a Cinematic Full-Bleed HUD and an interactive 3D concentric vault mechanism.
