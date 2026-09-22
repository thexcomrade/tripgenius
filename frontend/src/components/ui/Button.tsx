import React from "react";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "accent" | "ghost" | "danger" | "outline";
  size?: "sm" | "md" | "lg";
  isLoading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

export default function Button({
  children,
  variant = "primary",
  size = "md",
  isLoading = false,
  leftIcon,
  rightIcon,
  disabled,
  style,
  className = "",
  ...props
}: ButtonProps) {
  const sizeStyles = {
    sm: { padding: "6px 14px", fontSize: "0.82rem", borderRadius: "8px" },
    md: { padding: "10px 20px", fontSize: "0.92rem", borderRadius: "12px" },
    lg: { padding: "14px 28px", fontSize: "1.05rem", borderRadius: "14px" },
  }[size];

  const variantStyles: Record<string, React.CSSProperties> = {
    primary: {
      background: "linear-gradient(135deg, #0EA5E9 0%, #14B8A6 100%)",
      color: "#FFFFFF",
      border: "none",
      boxShadow: "0 4px 14px rgba(14, 165, 233, 0.35)",
      fontWeight: 600,
    },
    secondary: {
      background: "rgba(255, 255, 255, 0.06)",
      color: "#F8FAFC",
      border: "1px solid rgba(255, 255, 255, 0.14)",
      fontWeight: 500,
    },
    accent: {
      background: "linear-gradient(135deg, #F59E0B 0%, #F97316 100%)",
      color: "#FFFFFF",
      border: "none",
      boxShadow: "0 4px 14px rgba(245, 158, 11, 0.35)",
      fontWeight: 600,
    },
    ghost: {
      background: "transparent",
      color: "#CBD5E1",
      border: "none",
      fontWeight: 500,
    },
    outline: {
      background: "transparent",
      color: "#38BDF8",
      border: "1px solid rgba(56, 189, 248, 0.40)",
      fontWeight: 500,
    },
    danger: {
      background: "rgba(239, 68, 68, 0.15)",
      color: "#FCA5A5",
      border: "1px solid rgba(239, 68, 68, 0.35)",
      fontWeight: 600,
    },
  };

  return (
    <button
      disabled={disabled || isLoading}
      style={{
        display: "inline-flex",
        alignItems: "center",
        justifyContent: "center",
        gap: "8px",
        cursor: disabled || isLoading ? "not-allowed" : "pointer",
        opacity: disabled || isLoading ? 0.65 : 1,
        transition: "all 0.2s cubic-bezier(0.16, 1, 0.3, 1)",
        ...sizeStyles,
        ...variantStyles[variant],
        ...style,
      }}
      className={`btn-base ${className}`}
      {...props}
    >
      {isLoading && (
        <span
          style={{
            width: "14px",
            height: "14px",
            borderRadius: "50%",
            border: "2px solid rgba(255, 255, 255, 0.3)",
            borderTopColor: "#FFFFFF",
            animation: "spin 0.8s linear infinite",
            display: "inline-block",
          }}
        />
      )}
      {!isLoading && leftIcon}
      <span>{children}</span>
      {!isLoading && rightIcon}
      <style jsx>{`
        @keyframes spin {
          to {
            transform: rotate(360deg);
          }
        }
      `}</style>
    </button>
  );
}
