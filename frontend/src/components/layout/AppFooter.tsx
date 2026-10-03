"use client";

import { useState } from "react";
import { usePathname } from "next/navigation";
import Link from "next/link";
import Image from "next/image";
import { Mail, Phone, Check, Copy, Leaf, Sparkles, Activity } from "lucide-react";

/** Pages where the footer should be hidden (e.g. full-height chat UI). */
const FOOTER_HIDDEN_PATHS = ["/ai-chat"];

export default function AppFooter() {
  const pathname = usePathname();
  const [copiedEmail, setCopiedEmail] = useState(false);

  if (FOOTER_HIDDEN_PATHS.includes(pathname)) return null;

  const copyEmail = (e: React.MouseEvent) => {
    e.preventDefault();
    const email = "devanarayananstackuplearning@gmail.com";
    if (typeof navigator !== "undefined" && navigator.clipboard?.writeText) {
      navigator.clipboard
        .writeText(email)
        .then(() => {
          setCopiedEmail(true);
          setTimeout(() => setCopiedEmail(false), 2000);
        })
        .catch(() => fallbackCopy(email));
    } else {
      fallbackCopy(email);
    }
  };

  const fallbackCopy = (text: string) => {
    try {
      const textArea = document.createElement("textarea");
      textArea.value = text;
      textArea.style.position = "fixed";
      textArea.style.left = "-999999px";
      textArea.style.top = "-999999px";
      document.body.appendChild(textArea);
      textArea.focus();
      textArea.select();
      document.execCommand("copy");
      document.body.removeChild(textArea);
      setCopiedEmail(true);
      setTimeout(() => setCopiedEmail(false), 2000);
    } catch {
      // fallback silent
    }
  };

  return (
    <footer
      style={{
        position: "relative",
        marginTop: "48px",
        background: "linear-gradient(180deg, rgba(3, 7, 18, 0.90) 0%, rgba(2, 6, 23, 0.98) 100%)",
        backdropFilter: "blur(24px)",
        WebkitBackdropFilter: "blur(24px)",
        borderTop: "1px solid rgba(255, 255, 255, 0.08)",
        color: "#94A3B8",
        padding: "36px 0 24px",
        fontSize: "0.85rem",
      }}
    >
      {/* Top subtle ambient glow line */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: "15%",
          right: "15%",
          height: "1px",
          background:
            "linear-gradient(90deg, transparent, rgba(56, 189, 248, 0.45), rgba(16, 185, 129, 0.35), transparent)",
        }}
      />

      <div
        className="footer-content-container"
        style={{
          width: "100%",
          maxWidth: "1680px",
          margin: "0 auto",
          padding: "36px clamp(16px, 3.5vw, 44px) 18px clamp(16px, 3.5vw, 44px)",
        }}
      >
        {/* ==================================================== */}
        {/* ROW 1: BRAND HEADER & NAVIGATION LINKS               */}
        {/* ==================================================== */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            flexWrap: "wrap",
            gap: "18px 32px",
          }}
        >
          {/* BRAND */}
          <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
            <Link
              href="/"
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: "10px",
                textDecoration: "none",
              }}
            >
              <Image
                src="/logo/logo.svg"
                alt="Trip Geni Logo"
                width={28}
                height={28}
              />
              <span
                style={{
                  color: "#FFFFFF",
                  fontSize: "1.25rem",
                  fontWeight: 800,
                  letterSpacing: "-0.4px",
                }}
              >
                Trip Geni
              </span>
            </Link>
            <span
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: "5px",
                fontSize: "0.74rem",
                fontWeight: 600,
                color: "#38BDF8",
                background: "rgba(14, 165, 233, 0.12)",
                border: "1px solid rgba(56, 189, 248, 0.25)",
                padding: "3px 10px",
                borderRadius: "999px",
              }}
            >
              <Sparkles size={11} color="#38BDF8" /> AI Travel Platform
            </span>
          </div>

          {/* QUICK NAVIGATION */}
          <nav
            style={{
              display: "flex",
              alignItems: "center",
              gap: "20px",
              flexWrap: "wrap",
            }}
          >
            {[
              { label: "Home", href: "/" },
              { label: "Planner", href: "/planner" },
              { label: "Explore", href: "/explore" },
              { label: "Dashboard", href: "/dashboard" },
              { label: "History", href: "/trip/history" },
              { label: "Favorites", href: "/favorites" },
              { label: "Analytics", href: "/analytics" },
              { label: "AI ChatBot", href: "/ai-chat", highlight: true },
            ].map((item) => (
              <Link
                key={item.label}
                href={item.href}
                style={{
                  color: item.highlight ? "#38BDF8" : "#CBD5E1",
                  fontWeight: item.highlight ? 700 : 500,
                  textDecoration: "none",
                  fontSize: "0.85rem",
                  transition: "all 0.2s ease",
                  display: "inline-flex",
                  alignItems: "center",
                  gap: "4px",
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.color = "#38BDF8";
                  e.currentTarget.style.transform = "translateY(-1px)";
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.color = item.highlight ? "#38BDF8" : "#CBD5E1";
                  e.currentTarget.style.transform = "translateY(0)";
                }}
              >
                {item.label}
              </Link>
            ))}
          </nav>
        </div>

        {/* ==================================================== */}
        {/* ROW 2: CONTACT, HELPLINE & REAL-TIME SYSTEM STATUS    */}
        {/* ==================================================== */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            flexWrap: "wrap",
            gap: "14px 20px",
            padding: "14px 20px",
            background: "rgba(255, 255, 255, 0.02)",
            border: "1px solid rgba(255, 255, 255, 0.06)",
            borderRadius: "16px",
          }}
        >
          {/* STATUS PILLS (LEFT) */}
          <div style={{ display: "flex", alignItems: "center", gap: "12px", flexWrap: "wrap" }}>
            {/* LIVE API STATUS */}
            <div
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: "7px",
                fontSize: "0.78rem",
                color: "#A7F3D0",
                background: "rgba(16, 185, 129, 0.08)",
                border: "1px solid rgba(16, 185, 129, 0.22)",
                padding: "5px 12px",
                borderRadius: "999px",
              }}
            >
              <span
                style={{
                  width: "7px",
                  height: "7px",
                  borderRadius: "50%",
                  background: "#10B981",
                  boxShadow: "0 0 8px #10B981",
                }}
              />
              <span>Live Services: Connected &amp; Operational</span>
            </div>

            {/* ECO RATING PILL */}
            <div
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: "6px",
                fontSize: "0.78rem",
                color: "#BAE6FD",
                background: "rgba(14, 165, 233, 0.08)",
                border: "1px solid rgba(56, 189, 248, 0.22)",
                padding: "5px 12px",
                borderRadius: "999px",
              }}
            >
              <Leaf size={12} color="#38BDF8" />
              <span>Carbon-Calibrated Planning</span>
            </div>
          </div>

          {/* CONTACT BADGES (RIGHT) */}
          <div style={{ display: "flex", alignItems: "center", gap: "12px", flexWrap: "wrap" }}>
            {/* EMAIL COPY CHIP */}
            <button
              type="button"
              onClick={copyEmail}
              title="Click to copy official email"
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: "8px",
                background: "rgba(14, 165, 233, 0.08)",
                border: "1px solid rgba(56, 189, 248, 0.20)",
                borderRadius: "10px",
                padding: "6px 14px",
                color: copiedEmail ? "#34D399" : "#E2E8F0",
                fontSize: "0.80rem",
                fontWeight: 500,
                cursor: "pointer",
                transition: "all 0.2s ease",
              }}
            >
              <Mail size={14} color={copiedEmail ? "#34D399" : "#38BDF8"} />
              <span>devanarayananstackuplearning@gmail.com</span>
              {copiedEmail ? (
                <Check size={13} color="#34D399" />
              ) : (
                <Copy size={13} color="#94A3B8" />
              )}
            </button>

            {/* DIRECT HELPLINE */}
            <a
              href="tel:+918078421005"
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: "8px",
                background: "rgba(16, 185, 129, 0.08)",
                border: "1px solid rgba(16, 185, 129, 0.20)",
                borderRadius: "10px",
                padding: "6px 14px",
                color: "#E2E8F0",
                fontSize: "0.80rem",
                fontWeight: 600,
                textDecoration: "none",
                transition: "all 0.2s ease",
              }}
            >
              <Phone size={14} color="#34D399" />
              <span>+91 8078421005</span>
            </a>
          </div>
        </div>

        {/* ==================================================== */}
        {/* ROW 3: COPYRIGHT, PLATFORM TAGLINE & DEV CREDITS     */}
        {/* ==================================================== */}
        <div
          style={{
            borderTop: "1px solid rgba(255, 255, 255, 0.07)",
            paddingTop: "18px",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            flexWrap: "wrap",
            gap: "12px 20px",
            fontSize: "0.80rem",
            color: "#64748B",
          }}
        >
          {/* COPYRIGHT */}
          <div>
            © {new Date().getFullYear()} <strong>Trip Geni</strong> AI Platform. Synthesizing data-calibrated travel experiences worldwide.
          </div>

          {/* DEVELOPER CREDITS */}
          <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
            <span>developed by</span>
            <strong style={{ color: "#fbbf24" }}>thexcomrade</strong>
            <span
              style={{
                fontSize: "0.70rem",
                padding: "2px 8px",
                borderRadius: "5px",
                background: "#f2631a",
                color: "#f8f7f3",
                fontWeight: 700,
                letterSpacing: "0.4px",
              }}
            >
              STACKUP
            </span>
          </div>
        </div>
      </div>
    </footer>
  );
}
