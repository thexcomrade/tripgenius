import Link from "next/link";
import Image from "next/image";
import { Sparkles, Compass, Leaf, Shield, Heart } from "lucide-react";

export default function AppFooter() {
  return (
    <footer
      style={{
        marginTop: "100px",
        background: "rgba(2, 6, 23, 0.95)",
        backdropFilter: "blur(24px)",
        WebkitBackdropFilter: "blur(24px)",
        borderTop: "1px solid rgba(255, 255, 255, 0.08)",
        color: "#94A3B8",
      }}
    >
      <div
        style={{
          width: "100%",
          maxWidth: "1680px",
          margin: "0 auto",
          padding: "60px clamp(20px, 4vw, 56px) 30px clamp(20px, 4vw, 56px)",
        }}
      >
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))",
            gap: "clamp(24px, 3vw, 48px)",
            marginBottom: "50px",
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
                alt="TripGenius Logo"
                width={36}
                height={36}
                priority
              />
              <span
                style={{
                  color: "#FFFFFF",
                  fontSize: "1.6rem",
                  fontWeight: 800,
                  letterSpacing: "-0.5px",
                }}
              >
                TripGenius
              </span>
            </div>
            <p
              style={{
                color: "#94A3B8",
                fontSize: "0.92rem",
                lineHeight: 1.7,
                marginBottom: "20px",
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
                fontSize: "1rem",
                fontWeight: 700,
                marginBottom: "18px",
              }}
            >
              Explore & Plan
            </h4>
            <ul
              style={{
                listStyle: "none",
                display: "flex",
                flexDirection: "column",
                gap: "10px",
                padding: 0,
              }}
            >
              <li>
                <Link
                  href="/planner"
                  style={{
                    color: "#CBD5E1",
                    textDecoration: "none",
                    fontSize: "0.92rem",
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
                    fontSize: "0.92rem",
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
                    fontSize: "0.92rem",
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
                    fontSize: "0.92rem",
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
                fontSize: "1rem",
                fontWeight: 700,
                marginBottom: "18px",
              }}
            >
              Personal Hub
            </h4>
            <ul
              style={{
                listStyle: "none",
                display: "flex",
                flexDirection: "column",
                gap: "10px",
                padding: 0,
              }}
            >
              <li>
                <Link
                  href="/trip/history"
                  style={{
                    color: "#CBD5E1",
                    textDecoration: "none",
                    fontSize: "0.92rem",
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
                    fontSize: "0.92rem",
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
                    fontSize: "0.92rem",
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
                    fontSize: "0.92rem",
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
                    fontSize: "0.92rem",
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
                fontSize: "1rem",
                fontWeight: 700,
                marginBottom: "18px",
              }}
            >
              Support & Inquiries
            </h4>
            <p
              style={{
                color: "#CBD5E1",
                fontSize: "0.92rem",
                marginBottom: "8px",
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
                fontSize: "0.92rem",
                marginBottom: "8px",
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
                fontSize: "0.92rem",
                marginBottom: "8px",
              }}
            >
              🌐 Live Service API: Connected
            </p>
            <p
              style={{
                color: "#64748B",
                fontSize: "0.85rem",
                marginTop: "16px",
              }}
            >
              Empowered by Google Gemini, OpenWeather Intelligence & Tourism
              Datasets.
            </p>
          </div>
        </div>

        <div
          style={{
            paddingTop: "24px",
            borderTop: "1px solid rgba(255, 255, 255, 0.08)",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            flexWrap: "wrap",
            gap: "14px",
            fontSize: "0.88rem",
          }}
        >
          <p>© 2026 TripGenius AI Platform. All rights reserved.</p>
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
