"use client";

import { usePathname } from "next/navigation";
import Link from "next/link";
import Image from "next/image";
import { Leaf, Shield } from "lucide-react";

/** Pages where the footer should be hidden (e.g. full-height chat UI). */
const FOOTER_HIDDEN_PATHS = ["/ai-chat"];

export default function AppFooter() {
  const pathname = usePathname();
  if (FOOTER_HIDDEN_PATHS.includes(pathname)) return null;
  return (
    <footer
      style={{
        marginTop: "48px",
        background: "rgba(2, 6, 23, 0.95)",
        backdropFilter: "blur(24px)",
        WebkitBackdropFilter: "blur(24px)",
        borderTop: "1px solid rgba(255, 255, 255, 0.08)",
        color: "#94A3B8",
      }}
    >
      <div
        className="footer-content-container"
        style={{
          width: "80%",
          maxWidth: "1240px",
          margin: "0 auto",
          padding: "36px clamp(16px, 2.5vw, 32px) 18px clamp(16px, 2.5vw, 32px)",
        }}
      >
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
            gap: "clamp(20px, 2.5vw, 36px)",
            marginBottom: "28px",
          }}
        >
          {/* BRAND COL */}
          <div>
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "12px",
                marginBottom: "16px",
              }}
            >
              <Image
                src="/logo/logo.svg"
                alt="Trip Geni Logo"
                width={30}
                height={30}
                priority
              />
              <span
                style={{
                  color: "#FFFFFF",
                  fontSize: "1.35rem",
                  fontWeight: 800,
                  letterSpacing: "-0.5px",
                }}
              >
                Trip Geni
              </span>
            </div>
            <p
              style={{
                color: "#94A3B8",
                fontSize: "0.85rem",
                lineHeight: 1.55,
                marginBottom: "14px",
              }}
            >
              Next-generation AI travel companion designed for personalized,
              sustainable, and intelligent itineraries around the globe.
            </p>
            <div style={{ display: "flex", gap: "12px", alignItems: "center" }}>
              <span
                style={{
                  display: "inline-flex",
                  alignItems: "center",
                  gap: "6px",
                  fontSize: "0.8rem",
                  color: "#34D399",
                  background: "rgba(16, 185, 129, 0.12)",
                  padding: "4px 10px",
                  borderRadius: "999px",
                  border: "1px solid rgba(16, 185, 129, 0.25)",
                }}
              >
                <Leaf size={12} /> Carbon Conscious
              </span>
              <span
                style={{
                  display: "inline-flex",
                  alignItems: "center",
                  gap: "6px",
                  fontSize: "0.8rem",
                  color: "#38BDF8",
                  background: "rgba(14, 165, 233, 0.12)",
                  padding: "4px 10px",
                  borderRadius: "999px",
                  border: "1px solid rgba(14, 165, 233, 0.25)",
                }}
              >
                <Shield size={12} /> Realtime AI
              </span>
            </div>
          </div>

          {/* EXPLORE LINKS */}
          <div>
            <h4
              style={{
                color: "#FFFFFF",
                fontSize: "0.88rem",
                fontWeight: 700,
                marginBottom: "12px",
                letterSpacing: "0.3px",
              }}
            >
              Explore & Plan
            </h4>
            <ul
              style={{
                listStyle: "none",
                display: "flex",
                flexDirection: "column",
                gap: "7px",
                padding: 0,
              }}
            >
              <li>
                <Link
                  href="/planner"
                  style={{
                    color: "#CBD5E1",
                    textDecoration: "none",
                    fontSize: "0.84rem",
                    transition: "color 0.2s",
                  }}
                >
                  AI Itinerary Studio
                </Link>
              </li>
              <li>
                <Link
                  href="/explore"
                  style={{
                    color: "#CBD5E1",
                    textDecoration: "none",
                    fontSize: "0.84rem",
                    transition: "color 0.2s",
                  }}
                >
                  Curated Destinations
                </Link>
              </li>
              <li>
                <Link
                  href="/ai-chat"
                  style={{
                    color: "#CBD5E1",
                    textDecoration: "none",
                    fontSize: "0.84rem",
                    transition: "color 0.2s",
                  }}
                >
                  Conversational Assistant
                </Link>
              </li>
              <li>
                <Link
                  href="/dashboard"
                  style={{
                    color: "#CBD5E1",
                    textDecoration: "none",
                    fontSize: "0.84rem",
                    transition: "color 0.2s",
                  }}
                >
                  Travel Command Center
                </Link>
              </li>
            </ul>
          </div>

          {/* ACCOUNT & STATS */}
          <div>
            <h4
              style={{
                color: "#FFFFFF",
                fontSize: "0.88rem",
                fontWeight: 700,
                marginBottom: "12px",
                letterSpacing: "0.3px",
              }}
            >
              Personal Hub
            </h4>
            <ul
              style={{
                listStyle: "none",
                display: "flex",
                flexDirection: "column",
                gap: "7px",
                padding: 0,
              }}
            >
              <li>
                <Link
                  href="/trip/history"
                  style={{
                    color: "#CBD5E1",
                    textDecoration: "none",
                    fontSize: "0.84rem",
                  }}
                >
                  Trip History & Archive
                </Link>
              </li>
              <li>
                <Link
                  href="/favorites"
                  style={{
                    color: "#CBD5E1",
                    textDecoration: "none",
                    fontSize: "0.84rem",
                  }}
                >
                  Saved Bucket List
                </Link>
              </li>
              <li>
                <Link
                  href="/analytics"
                  style={{
                    color: "#CBD5E1",
                    textDecoration: "none",
                    fontSize: "0.84rem",
                  }}
                >
                  Travel Analytics
                </Link>
              </li>
              <li>
                <Link
                  href="/achievements"
                  style={{
                    color: "#CBD5E1",
                    textDecoration: "none",
                    fontSize: "0.84rem",
                  }}
                >
                  Explorer Achievements
                </Link>
              </li>
              <li>
                <Link
                  href="/settings"
                  style={{
                    color: "#CBD5E1",
                    textDecoration: "none",
                    fontSize: "0.84rem",
                  }}
                >
                  Account Settings
                </Link>
              </li>
            </ul>
          </div>

          {/* CONTACT */}
          <div>
            <h4
              style={{
                color: "#FFFFFF",
                fontSize: "0.88rem",
                fontWeight: 700,
                marginBottom: "12px",
                letterSpacing: "0.3px",
              }}
            >
              Support & Inquiries
            </h4>
            <p
              style={{
                color: "#CBD5E1",
                fontSize: "0.84rem",
                marginBottom: "6px",
              }}
            >
              📧{" "}
              <a
                href="mailto:devanarayananstackuplearning@gmail.com"
                style={{ color: "#38BDF8", textDecoration: "none" }}
              >
                devanarayananstackuplearning@gmail.com
              </a>
            </p>
            <p
              style={{
                color: "#CBD5E1",
                fontSize: "0.84rem",
                marginBottom: "6px",
              }}
            >
              📞{" "}
              <a
                href="tel:+918078421005"
                style={{ color: "#CBD5E1", textDecoration: "none" }}
              >
                +91 8078421005
              </a>
            </p>
            <p
              style={{
                color: "#CBD5E1",
                fontSize: "0.84rem",
                marginBottom: "6px",
              }}
            >
              🌐 Live Service API: Connected
            </p>
            <p
              style={{
                color: "#64748B",
                fontSize: "0.78rem",
                marginTop: "10px",
              }}
            >
              Empowered by Google Gemini, OpenWeather Intelligence & Tourism
              Datasets.
            </p>
          </div>
        </div>

        <div
          style={{
            paddingTop: "16px",
            borderTop: "1px solid rgba(255, 255, 255, 0.08)",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            flexWrap: "wrap",
            gap: "12px",
            fontSize: "0.82rem",
          }}
        >
          <p>© 2026 Trip Geni AI Platform. All rights reserved.</p>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "8px",
              flexWrap: "wrap",
            }}
          >
            <span style={{ color: "#94A3B8" }}>
              developed by{" "}
              <span
                style={{
                  color: "#F8FAFC",
                  fontWeight: 600,
                  letterSpacing: "0.2px",
                }}
              >
                thexcomrade
              </span>
            </span>
            <span style={{ color: "rgba(255, 255, 255, 0.25)" }}>•</span>
            <span
              style={{
                color: "#FF7700",
                fontWeight: 700,
                letterSpacing: "0.5px",
                background: "rgba(255, 119, 0, 0.12)",
                padding: "2px 8px",
                borderRadius: "6px",
                border: "1px solid rgba(255, 119, 0, 0.3)",
              }}
            >
              stackup
            </span>
          </div>
        </div>
      </div>
    </footer>
  );
}
