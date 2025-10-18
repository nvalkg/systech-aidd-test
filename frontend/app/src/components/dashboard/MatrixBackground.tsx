"use client";

import { useEffect, useRef } from "react";

export function MatrixBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // Set canvas size
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    // Matrix characters
    const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()";
    const fontSize = 14;
    const columns = canvas.width / fontSize;

    // Array to store y-position of each column
    const drops: number[] = [];
    for (let i = 0; i < columns; i++) {
      drops[i] = Math.random() * -100;
    }

    function draw() {
      if (!ctx || !canvas) return;

      // Black background with transparency for trail effect
      ctx.fillStyle = "rgba(0, 0, 0, 0.05)";
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Green text
      ctx.fillStyle = "#0F0";
      ctx.font = `${fontSize}px monospace`;

      for (let i = 0; i < drops.length; i++) {
        // Random character
        const text = chars[Math.floor(Math.random() * chars.length)] || "0";
        const dropY = drops[i] ?? 0;

        // Draw character
        ctx.fillStyle = "#0F0";
        ctx.fillText(text, i * fontSize, dropY * fontSize);

        // Reset drop to top randomly after it crosses screen
        if (dropY * fontSize > canvas.height && Math.random() > 0.975) {
          drops[i] = 0;
        } else {
          drops[i] = dropY + 1;
        }
      }
    }

    const interval = setInterval(draw, 35);

    // Handle window resize
    const handleResize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    window.addEventListener("resize", handleResize);

    return () => {
      clearInterval(interval);
      window.removeEventListener("resize", handleResize);
    };
  }, []);

  return (
    <>
      {/* Matrix green gradient background */}
      <div
        className="fixed inset-0 z-0"
        style={{
          background: 'linear-gradient(to bottom, #0d0208 0%, #001a00 50%, #000000 100%)',
        }}
      />

      {/* Animated matrix rain */}
      <canvas
        ref={canvasRef}
        className="fixed inset-0 z-0"
        style={{ opacity: 0.8 }}
      />

      {/* Dark overlay for better readability */}
      <div className="fixed inset-0 z-0 bg-black/40" />
    </>
  );
}
