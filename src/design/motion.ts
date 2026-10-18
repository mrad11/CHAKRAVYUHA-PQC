/**
 * CHAKRAVYUHA PQC - MOTION ENGINE
 * Personality: Magnetic (Elastic, Springy, Decisive)
 */

export const motionTokens = {
  duration: {
    instant: 0.09,
    fast: 0.14,
    base: 0.22,
    deliberate: 0.36,
    ceremony: 0.90,
  },
  spring: {
    snappy: { type: "spring", stiffness: 420, damping: 28, mass: 0.7 },
    magnetic: { type: "spring", stiffness: 340, damping: 24, mass: 0.85 },
    glide: { type: "spring", stiffness: 220, damping: 30, mass: 1.0 },
    vaultLock: { type: "spring", stiffness: 480, damping: 32, mass: 1.2 },
  },
  easing: {
    magnetic: [0.16, 1.0, 0.30, 1.0],
    anticipate: [0.36, 0, 0.66, -0.56],
    smooth: [0.25, 0.1, 0.25, 1.0],
  },
  stagger: {
    tacticalPills: 0.04,
    matrixBits: 0.005,
    threatAlerts: 0.06,
  }
} as const;

export const fadeInVariants = {
  initial: { opacity: 0, y: 12, scale: 0.98 },
  animate: { opacity: 1, y: 0, scale: 1, transition: motionTokens.spring.magnetic },
  exit: { opacity: 0, y: -8, scale: 0.98, transition: { duration: motionTokens.duration.fast } }
};

export const vaultRotationVariants = {
  locked: { rotate: 0, scale: 1 },
  scanning: { rotate: [0, 90, 180, 270, 360], transition: { duration: 4, repeat: Infinity, ease: "linear" } },
  verified: { rotate: 0, scale: 1.04, transition: motionTokens.spring.vaultLock },
  alarm: { rotate: [-4, 4, -4, 4, 0], transition: { duration: 0.3 } }
};
