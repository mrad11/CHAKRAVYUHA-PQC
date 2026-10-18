"use client";

import React, { useRef, useState } from "react";
import { motion } from "framer-motion";
import { motionTokens } from "@/design/motion";

interface MagneticButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  variant?: "primary" | "secondary" | "danger" | "ghost";
  className?: string;
}

export function MagneticButton({
  children,
  variant = "primary",
  className = "",
  onClick,
  ...props
}: MagneticButtonProps) {
  const btnRef = useRef<HTMLButtonElement>(null);
  const [position, setPosition] = useState({ x: 0, y: 0 });

  const handleMouseMove = (e: React.MouseEvent<HTMLButtonElement>) => {
    if (!btnRef.current) return;
    const { clientX, clientY } = e;
    const { left, top, width, height } = btnRef.current.getBoundingClientRect();
    const x = (clientX - (left + width / 2)) * 0.28;
    const y = (clientY - (top + height / 2)) * 0.28;
    setPosition({ x, y });
  };

  const handleMouseLeave = () => {
    setPosition({ x: 0, y: 0 });
  };

  const variantStyles = {
    primary: "bg-[oklch(0.780_0.160_170)] text-[oklch(0.160_0.040_298)] font-bold shadow-[0_0_20px_rgba(0,215,168,0.35)] hover:bg-[oklch(0.840_0.180_170)]",
    secondary: "bg-[oklch(0.220_0.060_298)] text-[oklch(0.940_0.020_298)] border border-[oklch(0.280_0.050_298)] hover:border-[oklch(0.750_0.180_170)]",
    danger: "bg-[oklch(0.580_0.240_22)] text-white shadow-[0_0_20px_rgba(230,0,49,0.35)]",
    ghost: "bg-transparent text-[oklch(0.750_0.040_298)] hover:text-[oklch(0.940_0.020_298)]",
  };

  return (
    <motion.button
      ref={btnRef}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      animate={{ x: position.x, y: position.y }}
      transition={motionTokens.spring.magnetic}
      whileTap={{ scale: 0.96 }}
      onClick={onClick}
      className={`relative inline-flex items-center justify-center gap-2 px-5 py-2.5 text-xs tracking-wider uppercase font-mono transition-colors rounded-[var(--r-md)] ${variantStyles[variant]} ${className}`}
      {...props}
    >
      {children}
    </motion.button>
  );
}
