import React from "react";

export interface GlassCardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  interactive?: boolean;
  style?: React.CSSProperties;
  className?: string;
}

export function GlassCard({
  children,
  interactive = false,
  style,
  className = "",
  ...props
}: GlassCardProps) {
  return (
    <div
      style={{
        background: "rgba(15, 23, 42, 0.65)",
        backdropFilter: "blur(20px)",
        WebkitBackdropFilter: "blur(20px)",
        border: "1px solid rgba(255, 255, 255, 0.08)",
        borderRadius: "20px",
        padding: "24px",
        boxShadow: "0 8px 32px rgba(0, 0, 0, 0.35)",
        transition: interactive
          ? "all 0.25s cubic-bezier(0.16, 1, 0.3, 1)"
          : undefined,
        ...style,
      }}
      className={`${interactive ? "glass-card-interactive" : ""} ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}

export interface MetricCardProps {
  title: string;
  value: string | number;
  icon: React.ReactNode;
  change?: string;
  changeType?: "positive" | "negative" | "neutral";
  subtitle?: string;
  style?: React.CSSProperties;
  onClick?: () => void;
}

export function MetricCard({
  title,
  value,
  icon,
  change,
  changeType = "neutral",
  subtitle,
  style,
  onClick,
}: MetricCardProps) {
  const changeColor = {
    positive: "#34D399",
    negative: "#F87171",
    neutral: "#94A3B8",
  }[changeType];

  return (
    <GlassCard
      interactive={!!onClick}
      onClick={onClick}
      style={{
        padding: "22px",
        display: "flex",
        flexDirection: "column",
        gap: "12px",
        ...style,
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
        }}
      >
        <span
          style={{
            fontSize: "0.85rem",
            fontWeight: 600,
            color: "#94A3B8",
            textTransform: "uppercase",
            letterSpacing: "0.5px",
          }}
        >
          {title}
        </span>
        <div
          style={{
            width: "36px",
            height: "36px",
            borderRadius: "10px",
            background: "rgba(255, 255, 255, 0.05)",
            border: "1px solid rgba(255, 255, 255, 0.10)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: "#38BDF8",
          }}
        >
          {icon}
        </div>
      </div>

      <div style={{ display: "flex", alignItems: "baseline", gap: "10px" }}>
        <span
          style={{
            fontSize: "2.1rem",
            fontWeight: 800,
            color: "#FFFFFF",
            letterSpacing: "-0.5px",
          }}
        >
          {value}
        </span>
        {change && (
          <span
            style={{ fontSize: "0.82rem", fontWeight: 700, color: changeColor }}
          >
            {change}
          </span>
        )}
      </div>

      {subtitle && (
        <p style={{ fontSize: "0.82rem", color: "#64748B", marginTop: "-4px" }}>
          {subtitle}
        </p>
      )}
    </GlassCard>
  );
}

export function SectionHeader({
  title,
  subtitle,
  badge,
  action,
}: {
  title: string;
  subtitle?: string;
  badge?: string;
  action?: React.ReactNode;
}) {
  return (
    <div
      style={{
        display: "flex",
        alignItems: "flex-end",
        justifyContent: "space-between",
        flexWrap: "wrap",
        gap: "16px",
        marginBottom: "24px",
      }}
    >
      <div>
        {badge && (
          <span
            style={{
              display: "inline-block",
              fontSize: "0.75rem",
              fontWeight: 700,
              textTransform: "uppercase",
              letterSpacing: "1px",
              color: "#38BDF8",
              marginBottom: "6px",
            }}
          >
            {badge}
          </span>
        )}
        <h2
          style={{
            fontSize: "1.8rem",
            fontWeight: 800,
            color: "#FFFFFF",
            letterSpacing: "-0.5px",
          }}
        >
          {title}
        </h2>
        {subtitle && (
          <p
            style={{ color: "#94A3B8", fontSize: "0.95rem", marginTop: "4px" }}
          >
            {subtitle}
          </p>
        )}
      </div>
      {action && <div>{action}</div>}
    </div>
  );
}
