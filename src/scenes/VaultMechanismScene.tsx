"use client";

import React, { useRef, useMemo } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import * as THREE from "three";

/**
 * Concentric Chakravyuha Rings Component
 */
function ConcentricVaultRings({ riskLevel = 0.12 }: { riskLevel?: number }) {
  const ring1Ref = useRef<THREE.Group>(null);
  const ring2Ref = useRef<THREE.Group>(null);
  const ring3Ref = useRef<THREE.Group>(null);
  const coreRef = useRef<THREE.Mesh>(null);

  // Seafoam & Orchid Materials
  const materials = useMemo(() => {
    return {
      seafoam: new THREE.MeshStandardMaterial({
        color: new THREE.Color("#00d7a8"),
        emissive: new THREE.Color("#00d7a8"),
        emissiveIntensity: 0.45,
        roughness: 0.2,
        metalness: 0.8,
        wireframe: true,
      }),
      orchid: new THREE.MeshStandardMaterial({
        color: new THREE.Color("#fb40ad"),
        emissive: new THREE.Color("#fb40ad"),
        emissiveIntensity: 0.5,
        roughness: 0.3,
        metalness: 0.7,
        wireframe: true,
      }),
      amethyst: new THREE.MeshStandardMaterial({
        color: new THREE.Color("#2c233e"),
        roughness: 0.5,
        metalness: 0.9,
      }),
    };
  }, []);

  useFrame((_, delta) => {
    if (ring1Ref.current) ring1Ref.current.rotation.z += delta * 0.25;
    if (ring2Ref.current) ring2Ref.current.rotation.z -= delta * 0.40;
    if (ring3Ref.current) ring3Ref.current.rotation.z += delta * 0.15;
    if (coreRef.current) {
      coreRef.current.rotation.x += delta * 0.5;
      coreRef.current.rotation.y += delta * 0.6;
    }
  });

  return (
    <group rotation={[Math.PI * 0.22, 0, 0]}>
      {/* Central Inner-Lit Octahedral Enclave Core */}
      <mesh ref={coreRef}>
        <octahedronGeometry args={[0.9, 0]} />
        <primitive object={materials.orchid} />
      </mesh>

      {/* Ring 1: Outer Bastion (36-segment Torus) */}
      <group ref={ring1Ref}>
        <mesh>
          <torusGeometry args={[2.5, 0.05, 16, 64]} />
          <primitive object={materials.seafoam} />
        </mesh>
      </group>

      {/* Ring 2: Intermediate Cryptographic Rotor (Lattice Gates) */}
      <group ref={ring2Ref}>
        <mesh>
          <torusGeometry args={[1.9, 0.04, 16, 48]} />
          <primitive object={materials.amethyst} />
        </mesh>
      </group>

      {/* Ring 3: Inner Vault Seal (Quantum Quorum Lock) */}
      <group ref={ring3Ref}>
        <mesh>
          <torusGeometry args={[1.35, 0.06, 16, 32]} />
          <primitive object={materials.seafoam} />
        </mesh>
      </group>
    </group>
  );
}

export default function VaultMechanismScene({ riskLevel = 0.05 }: { riskLevel?: number }) {
  return (
    <div className="w-full h-full min-h-[320px] relative pointer-events-none">
      <Canvas
        camera={{ position: [0, 0, 6], fov: 45 }}
        gl={{ antialias: true, alpha: true }}
        dpr={[1, 1.5]}
      >
        <ambientLight intensity={0.4} color="#10091c" />
        <pointLight position={[4, 5, 4]} intensity={1.5} color="#00d7a8" />
        <pointLight position={[-4, -3, -2]} intensity={1.2} color="#fb40ad" />
        <ConcentricVaultRings riskLevel={riskLevel} />
      </Canvas>
    </div>
  );
}
