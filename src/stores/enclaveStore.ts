import { create } from "zustand";

export interface EnclaveState {
  // Navigation
  activeViewpoint: string;
  setActiveViewpoint: (vp: string) => void;

  // Time-Travel Scrubber
  timelineSeconds: number;
  isScrubbing: boolean;
  setTimelineSeconds: (sec: number) => void;
  setIsScrubbing: (scrub: boolean) => void;

  // Security & Heartbeat
  blockHeartbeat: number;
  triggerHeartbeat: () => void;
  threatLevel: "nominal" | "elevated" | "critical";
  activeOfficer: string;
  setActiveOfficer: (officer: string) => void;

  // Forensic Lens
  isForensicLensActive: boolean;
  toggleForensicLens: () => void;

  // Live Threat Logs
  threatLogs: Array<{
    id: string;
    timestamp: string;
    type: string;
    details: string;
    status: "blocked" | "verified" | "investigating";
  }>;
  addThreatLog: (log: { id: string; type: string; details: string; status: "blocked" | "verified" | "investigating" }) => void;
}

export const useEnclaveStore = create<EnclaveState>((set) => ({
  activeViewpoint: "dispatch",
  setActiveViewpoint: (vp) => set({ activeViewpoint: vp }),

  timelineSeconds: 0,
  isScrubbing: false,
  setTimelineSeconds: (sec) => set({ timelineSeconds: sec }),
  setIsScrubbing: (scrub) => set({ isScrubbing: scrub }),

  blockHeartbeat: 1,
  triggerHeartbeat: () => set((state) => ({ blockHeartbeat: state.blockHeartbeat + 1 })),
  threatLevel: "nominal",
  activeOfficer: "IND-MOD-003",
  setActiveOfficer: (officer) => set({ activeOfficer: officer }),

  isForensicLensActive: false,
  toggleForensicLens: () => set((state) => ({ isForensicLensActive: !state.isForensicLensActive })),

  threatLogs: [
    {
      id: "LOG-0941",
      timestamp: "17:14:02",
      type: "LATTICE_INTEGRITY",
      details: "ML-KEM-768 ciphertext encapsulation verified by Tri-Service root",
      status: "verified",
    },
    {
      id: "LOG-0942",
      timestamp: "17:15:28",
      type: "OPTICAL_STEGO",
      details: "256-bit Tardos watermark injected with mid-band carrier SNR +28.4 dB",
      status: "verified",
    },
    {
      id: "LOG-0943",
      timestamp: "17:16:11",
      type: "UNAUTHORIZED_LEAK",
      details: "Simulated screenshot extraction matched to IND-MOD-003 (Priya Nair)",
      status: "investigating",
    },
  ],
  addThreatLog: (log) =>
    set((state) => ({
      threatLogs: [
        { ...log, timestamp: new Date().toLocaleTimeString() },
        ...state.threatLogs.slice(0, 19),
      ],
    })),
}));
