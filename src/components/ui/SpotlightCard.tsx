"use client";

import React, { useRef, useState } from "react";
import { motion } from "framer-motion";
import { motionTokens } from "@/design/motion";

interface SpotlightCardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  className?: string;
  glowColor?: string;
}

export function SpotlightCard({
  children,
  className = "",
  glowColor = "rgba(0, 215, 168, 0.15)",
  ...props
}: SpotlightCardProps) {
  const cardRef = useRef<HTMLDivElement>(null);
  const [mousePos, setMousePos] = useState({ x: -1000, y: -1000 });
  const [isHovered, setIsHovered] = useState(false);

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!cardRef.current) return;
    const rect = cardRef.current.getBoundingClientRect();
    setMousePos({
      x: e.clientX - rect.left,
      y: e.clientY - rect.top,
    });
  };

  return (
    <motion.div
      ref={cardRef}
      onMouseMove={handleMouseMove}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      transition={motionTokens.spring.magnetic}
      className={`relative overflow-hidden velvet-matte-panel ${className}`}
      {...props}
    >
      {/* Dynamic Cursor Spotlight Layer */}
      <div
        className="pointer-events-none absolute -inset-px transition-opacity duration-300"
        style={{
          opacity: isHovered ? 1 : 0,
          background: `radial-gradient(350px circle at ${mousePos.x}px ${mousePos.y}px, ${glowColor}, transparent 75%)`,
        }}
      />
      
      {/* Micro-Hatching Guilloche Texture */}
      <div className="guilloche-watermark pointer-events-none absolute inset-0 opacity-40" />

      {/* Content */}
      <div className="relative z-10">{children}</div>
    </motion.div>
  );
}
