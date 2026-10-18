/**
 * CHAKRAVYUHA PQC - IDENTITY & TALISMAN GENERATOR
 */

export const IDENTITY = {
  appName: "CHAKRAVYUHA",
  appSubtitle: "Post-Quantum Cryptographic Defense Enclave",
  problemStatement: "MoD SIH PS 237",
  seed: 796,
  signatureObject: "Vault Mechanism (Concentric Chakravyuha Rings)",
  themeName: "Ultraviolet Dusk [D]",
  palette: {
    canvasBase: "#10091c",
    canvasSurface: "#1e1332",
    canvasSunken: "#090512",
    borderSubtle: "#2c233e",
    borderFocus: "#00d19c",
    accentSeafoam: "#00d7a8",
    highlightRose: "#fb40ad",
    textPrimary: "#ece9f7",
    textSecondary: "#b1a9c5",
    textMuted: "#756c8b",
    statusCrimson: "#e60031",
    statusJade: "#2ec97a",
  }
} as const;

/**
 * Generate SVG paths for the unique Personal Security Glyph
 * derived mathematically from the officer's enclave public key
 */
export function generatePersonalGlyph(enclaveSeed: string = "IND-MOD-003"): string {
  let hash = 0;
  for (let i = 0; i < enclaveSeed.length; i++) {
    hash = (hash << 5) - hash + enclaveSeed.charCodeAt(i);
    hash |= 0;
  }
  const radius = 18;
  const segments = 12;
  const points: [number, number][] = [];
  
  for (let i = 0; i < segments; i++) {
    const angle = (i * 2 * Math.PI) / segments;
    const r = radius * (0.75 + 0.25 * Math.sin(hash + i * 1.5));
    points.push([
      Math.round(24 + r * Math.cos(angle)),
      Math.round(24 + r * Math.sin(angle))
    ]);
  }
  
  return points.reduce((acc, [x, y], idx) => 
    idx === 0 ? `M ${x} ${y}` : `${acc} L ${x} ${y}`, "") + " Z";
}
