import React from "react";

export interface BadgeProps {
  children: React.ReactNode;
  variant?: "ai" | "eco" | "amber" | "neutral" | "danger" | "purple";
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
      ? { padding: "3px 8px", fontSize: "0.75rem" }
      : { padding: "5px 12px", fontSize: "0.85rem" };

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
