import Link from "next/link";
import { Compass, Home } from "lucide-react";

export default function NotFound() {
  return (
    <div
      style={{
        minHeight: "80vh",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        textAlign: "center",
        padding: "32px 16px",
      }}
    >
      <div
        style={{
          width: "72px",
          height: "72px",
          borderRadius: "20px",
          background: "rgba(14, 165, 233, 0.1)",
          border: "1px solid rgba(14, 165, 233, 0.25)",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          color: "#38BDF8",
          marginBottom: "24px",
        }}
      >
        <Compass size={36} />
      </div>

      <span
        style={{
          display: "inline-block",
          padding: "4px 12px",
          borderRadius: "999px",
          background: "rgba(255, 255, 255, 0.05)",
          border: "1px solid rgba(255, 255, 255, 0.1)",
          fontSize: "0.78rem",
          fontWeight: 700,
          color: "#94A3B8",
          textTransform: "uppercase",
          letterSpacing: "0.1em",
          marginBottom: "16px",
        }}
      >
        404 — Route Not Found
      </span>

      <h1
        style={{
          fontSize: "2.4rem",
          fontWeight: 900,
          color: "#FFFFFF",
          marginBottom: "12px",
          letterSpacing: "-0.02em",
        }}
      >
        Off the Beaten Path
      </h1>

      <p
        style={{
          fontSize: "1rem",
          color: "#94A3B8",
          maxWidth: "460px",
          lineHeight: 1.6,
          marginBottom: "32px",
        }}
      >
        The destination you are navigating to seems to have vanished from the map
        or is temporarily uncharted.
      </p>

      <Link
        href="/"
        style={{
          display: "inline-flex",
          alignItems: "center",
          gap: "8px",
          padding: "12px 24px",
          borderRadius: "12px",
          background: "linear-gradient(135deg, #0EA5E9, #14B8A6)",
          color: "#FFFFFF",
          fontWeight: 700,
          fontSize: "0.95rem",
          textDecoration: "none",
          boxShadow: "0 8px 24px rgba(14, 165, 233, 0.3)",
        }}
      >
        <Home size={18} /> Return to Home
      </Link>
    </div>
  );
}
