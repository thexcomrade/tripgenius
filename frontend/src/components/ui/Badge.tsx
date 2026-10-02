import React from "react";

export interface BadgeProps {
  children: React.ReactNode;
  variant?: "ai" | "eco" | "amber" | "neutral" | "danger" | "purple" | "overlay" | "glass";
  size?: "sm" | "md";
  icon?: React.ReactNode;
  style?: React.CSSProperties;
  className?: string;
}

export default function Badge({
  children,
  variant = "ai",
  size = "sm",
  icon,
  style,
  className = "",
}: BadgeProps) {
  const sizeStyle =
    size === "sm"
      ? { padding: "4px 10px", fontSize: "0.78rem" }
      : { padding: "6px 14px", fontSize: "0.85rem" };

  const variantStyles: Record<string, React.CSSProperties> = {
    ai: {
      background: "rgba(14, 165, 233, 0.15)",
      color: "#38BDF8",
      border: "1px solid rgba(14, 165, 233, 0.30)",
    },
    eco: {
      background: "rgba(16, 185, 129, 0.15)",
      color: "#34D399",
      border: "1px solid rgba(16, 185, 129, 0.30)",
    },
    amber: {
      background: "rgba(245, 158, 11, 0.15)",
      color: "#FBBF24",
      border: "1px solid rgba(245, 158, 11, 0.30)",
    },
    neutral: {
      background: "rgba(255, 255, 255, 0.08)",
      color: "#CBD5E1",
      border: "1px solid rgba(255, 255, 255, 0.12)",
    },
    danger: {
      background: "rgba(239, 68, 68, 0.15)",
      color: "#FCA5A5",
      border: "1px solid rgba(239, 68, 68, 0.30)",
    },
    purple: {
      background: "rgba(168, 85, 247, 0.15)",
      color: "#C084FC",
      border: "1px solid rgba(168, 85, 247, 0.30)",
    },
    overlay: {
      background: "rgba(3, 7, 18, 0.85)",
      backdropFilter: "blur(12px)",
      WebkitBackdropFilter: "blur(12px)",
      color: "#FFFFFF",
      border: "1px solid rgba(255, 255, 255, 0.22)",
      boxShadow: "0 2px 10px rgba(0, 0, 0, 0.55)",
      fontWeight: 700,
      letterSpacing: "0.03em",
    },
    glass: {
      background: "rgba(15, 23, 42, 0.82)",
      backdropFilter: "blur(12px)",
      WebkitBackdropFilter: "blur(12px)",
      color: "#38BDF8",
      border: "1px solid rgba(56, 189, 248, 0.40)",
      boxShadow: "0 2px 10px rgba(0, 0, 0, 0.45)",
      fontWeight: 700,
      letterSpacing: "0.03em",
    },
  };

  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: "5px",
        borderRadius: "999px",
        fontWeight: 600,
        letterSpacing: "0.2px",
        ...sizeStyle,
        ...variantStyles[variant],
        ...style,
      }}
      className={`badge-component ${className}`}
    >
      {icon}
      <span>{children}</span>
    </span>
  );
}
