"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  ShieldCheck,
  Settings,
  Edit3,
  Sparkles,
  MapPin,
  Compass,
  Bookmark,
  Leaf,
  Globe2,
  Copy,
  Check,
} from "lucide-react";

interface UserProfile {
  uid: string;
  tripgenius_id: string;
  full_name: string;
  username: string;
  email: string;
  bio: string;
  country: string;
  profile_image: string;
  total_trips: number;
  saved_trips: number;
  eco_score: number;
  countries_visited: number;
  is_verified: boolean;
  created_at: string;
  travel_preferences: string[];
}

interface ProfileHeaderProps {
  user: UserProfile;
  onSettingsClick: () => void;
  onEditProfileClick: () => void;
  onPhotoClick?: () => void;
}

export default function ProfileHeader({
  user,
  onSettingsClick,
  onEditProfileClick,
}: ProfileHeaderProps) {
  const [copied, setCopied] = useState(false);

  const handleCopyId = () => {
    if (user.tripgenius_id) {
      navigator.clipboard.writeText(user.tripgenius_id);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const getEcoRank = (score: number) => {
    if (score >= 80) return { label: "Eco Sentinel", color: "#10B981" };
    if (score >= 60) return { label: "Green Traveler", color: "#14B8A6" };
    return { label: "Conscious Explorer", color: "#38BDF8" };
  };

  const ecoRank = getEcoRank(user.eco_score || 92);

  // Compute clean initials e.g. "SB" for Sivya Babu
  const getInitials = (name: string) => {
    const parts = name.trim().split(" ");
    if (parts.length >= 2) {
      return (parts[0][0] + parts[1][0]).toUpperCase();
    }
    return name.slice(0, 2).toUpperCase() || "SB";
  };

  return (
    <section style={{ width: "100%", maxWidth: "1200px", margin: "0 auto 36px" }}>
      {/* Background Banner with Ambient Glow */}
      <div
        style={{
          position: "relative",
          overflow: "hidden",
          borderRadius: "28px",
          border: "1px solid rgba(255, 255, 255, 0.12)",
          padding: "36px",
          background:
            "linear-gradient(135deg, rgba(15, 23, 42, 0.92) 0%, rgba(11, 17, 32, 0.96) 100%)",
          backdropFilter: "blur(24px)",
          WebkitBackdropFilter: "blur(24px)",
          boxShadow: "0 20px 50px rgba(0, 0, 0, 0.45)",
        }}
      >
        {/* Subtle Ambient Radial Accents */}
        <div
          style={{
            position: "absolute",
            top: "-100px",
            right: "-100px",
            width: "320px",
            height: "320px",
            borderRadius: "50%",
            pointerEvents: "none",
            opacity: 0.25,
            background: "radial-gradient(circle, #0EA5E9 0%, transparent 70%)",
            filter: "blur(50px)",
          }}
        />
        <div
          style={{
            position: "absolute",
            bottom: "-100px",
            left: "-100px",
            width: "320px",
            height: "320px",
            borderRadius: "50%",
            pointerEvents: "none",
            opacity: 0.20,
            background: "radial-gradient(circle, #10B981 0%, transparent 70%)",
            filter: "blur(50px)",
          }}
        />

        <div
          style={{
            position: "relative",
            zIndex: 10,
            display: "flex",
            flexDirection: "row",
            alignItems: "flex-start",
            gap: "32px",
            flexWrap: "wrap",
          }}
        >
          {/* AVATAR WITH PHOTO UPLOAD */}
          <div style={{ position: "relative", flexShrink: 0 }}>
            <div
              style={{
                width: "130px",
                height: "130px",
                borderRadius: "50%",
                padding: "3px",
                background:
                  "linear-gradient(135deg, #0EA5E9 0%, #14B8A6 50%, #10B981 100%)",
                boxShadow: "0 0 30px rgba(14, 165, 233, 0.40)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
              }}
            >
              <div
                style={{
                  width: "100%",
                  height: "100%",
                  borderRadius: "50%",
                  overflow: "hidden",
                  background: "#0F172A",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                {user.profile_image ? (
                  <img
                    src={user.profile_image}
                    alt={user.full_name}
                    style={{ width: "100%", height: "100%", objectFit: "cover" }}
                  />
                ) : (
                  <span
                    style={{
                      fontSize: "2.4rem",
                      fontWeight: 900,
                      background: "linear-gradient(135deg, #38BDF8 0%, #34D399 100%)",
                      WebkitBackgroundClip: "text",
                      WebkitTextFillColor: "transparent",
                      letterSpacing: "1px",
                    }}
                  >
                    {getInitials(user.full_name || "Sivya Babu")}
                  </span>
                )}
              </div>
            </div>
          </div>

          {/* USER INFO & METRICS */}
          <div style={{ flex: 1, minWidth: "280px" }}>
            {/* TOP ROW: Name + Verified + Action Buttons */}
            <div
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                gap: "16px",
                flexWrap: "wrap",
                marginBottom: "12px",
              }}
            >
              <div>
                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "12px",
                    flexWrap: "wrap",
                  }}
                >
                  <h1
                    style={{
                      fontSize: "clamp(1.6rem, 2.5vw, 2.1rem)",
                      fontWeight: 800,
                      color: "#FFFFFF",
                      margin: 0,
                      letterSpacing: "-0.5px",
                    }}
                  >
                    {user.full_name || "Sivya Babu"}
                  </h1>

                  <span
                    style={{
                      display: "inline-flex",
                      alignItems: "center",
                      gap: "6px",
                      padding: "4px 10px",
                      borderRadius: "999px",
                      fontSize: "0.75rem",
                      fontWeight: 700,
                      background: "rgba(14, 165, 233, 0.15)",
                      color: "#38BDF8",
                      border: "1px solid rgba(14, 165, 233, 0.35)",
                    }}
                  >
                    <ShieldCheck size={14} color="#38BDF8" />
                    Verified Traveler
                  </span>
                </div>

                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "10px",
                    marginTop: "6px",
                    fontSize: "0.88rem",
                    color: "#94A3B8",
                  }}
                >
                  <span>@{user.username || "sivyababu"}</span>
                  <span style={{ color: "#475569" }}>•</span>
                  <button
                    type="button"
                    onClick={handleCopyId}
                    style={{
                      display: "inline-flex",
                      alignItems: "center",
                      gap: "6px",
                      fontSize: "0.78rem",
                      fontFamily: "monospace",
                      padding: "3px 8px",
                      borderRadius: "6px",
                      background: "rgba(30, 41, 59, 0.8)",
                      color: "#38BDF8",
                      border: "1px solid rgba(255, 255, 255, 0.08)",
                      cursor: "pointer",
                    }}
                    title="Click to copy Passport ID"
                  >
                    <span>{user.tripgenius_id || "TG-SB8842"}</span>
                    {copied ? (
                      <Check size={12} color="#34D399" />
                    ) : (
                      <Copy size={12} color="#94A3B8" />
                    )}
                  </button>
                </div>
              </div>

              {/* Action Buttons */}
              <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                <button
                  type="button"
                  onClick={onEditProfileClick}
                  style={{
                    display: "inline-flex",
                    alignItems: "center",
                    gap: "6px",
                    padding: "8px 14px",
                    borderRadius: "12px",
                    fontSize: "0.85rem",
                    fontWeight: 600,
                    background: "rgba(255, 255, 255, 0.08)",
                    border: "1px solid rgba(255, 255, 255, 0.12)",
                    color: "#FFFFFF",
                    cursor: "pointer",
                    transition: "all 0.2s ease",
                  }}
                >
                  <Edit3 size={15} color="#38BDF8" />
                  <span>Edit Profile</span>
                </button>

                <button
                  type="button"
                  onClick={onSettingsClick}
                  style={{
                    padding: "8px 10px",
                    borderRadius: "12px",
                    background: "rgba(255, 255, 255, 0.08)",
                    border: "1px solid rgba(255, 255, 255, 0.12)",
                    color: "#CBD5E1",
                    cursor: "pointer",
                  }}
                  title="Account Settings"
                >
                  <Settings size={16} />
                </button>

                <Link href="/planner" style={{ textDecoration: "none" }}>
                  <button
                    type="button"
                    style={{
                      display: "inline-flex",
                      alignItems: "center",
                      gap: "6px",
                      padding: "8px 16px",
                      borderRadius: "12px",
                      fontSize: "0.85rem",
                      fontWeight: 700,
                      background:
                        "linear-gradient(135deg, #0EA5E9 0%, #14B8A6 100%)",
                      border: "none",
                      color: "#FFFFFF",
                      cursor: "pointer",
                      boxShadow: "0 4px 14px rgba(14, 165, 233, 0.35)",
                    }}
                  >
                    <Sparkles size={15} color="#FDE047" />
                    <span>Plan Trip</span>
                  </button>
                </Link>
              </div>
            </div>

            {/* BIO */}
            <p
              style={{
                color: "#CBD5E1",
                fontSize: "0.92rem",
                lineHeight: 1.6,
                margin: "10px 0 14px",
                maxWidth: "750px",
              }}
            >
              {user.bio &&
              !user.bio.includes("Healthcare Professional") &&
              !user.bio.includes("Dr. Sivya Menon")
                ? user.bio
                : "Passionate traveler based in Trivandrum / Kochi. Loves mindful journeys, peaceful coastal getaways, and exploring authentic cultural sanctuaries."}
            </p>

            {/* TAGS & LOCATION */}
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "8px",
                flexWrap: "wrap",
                marginBottom: "22px",
              }}
            >
              <span
                style={{
                  display: "inline-flex",
                  alignItems: "center",
                  gap: "6px",
                  padding: "4px 10px",
                  borderRadius: "999px",
                  fontSize: "0.78rem",
                  fontWeight: 600,
                  background: "rgba(30, 41, 59, 0.75)",
                  color: "#E2E8F0",
                  border: "1px solid rgba(255, 255, 255, 0.08)",
                }}
              >
                <MapPin size={13} color="#FB7185" />
                {user.country || "Trivandrum, Kerala, India"}
              </span>

              <span
                style={{
                  display: "inline-flex",
                  alignItems: "center",
                  gap: "6px",
                  padding: "4px 10px",
                  borderRadius: "999px",
                  fontSize: "0.78rem",
                  fontWeight: 700,
                  background: "rgba(16, 185, 129, 0.15)",
                  color: "#34D399",
                  border: "1px solid rgba(16, 185, 129, 0.35)",
                }}
              >
                <Leaf size={13} color="#34D399" />
                {ecoRank.label}
              </span>

              {user.travel_preferences &&
                user.travel_preferences.slice(0, 3).map((pref, idx) => (
                  <span
                    key={idx}
                    style={{
                      display: "inline-flex",
                      alignItems: "center",
                      gap: "4px",
                      padding: "4px 10px",
                      borderRadius: "999px",
                      fontSize: "0.78rem",
                      fontWeight: 500,
                      background: "rgba(255, 255, 255, 0.05)",
                      color: "#94A3B8",
                      border: "1px solid rgba(255, 255, 255, 0.08)",
                    }}
                  >
                    ✨ {pref}
                  </span>
                ))}
            </div>

            {/* QUICK STATS STRIP - PURE CSS GRID (NOT BROKEN TAILWIND) */}
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))",
                gap: "14px",
                paddingTop: "18px",
                borderTop: "1px solid rgba(255, 255, 255, 0.10)",
              }}
            >
              <div
                style={{
                  padding: "14px 16px",
                  borderRadius: "16px",
                  background: "rgba(255, 255, 255, 0.04)",
                  border: "1px solid rgba(255, 255, 255, 0.08)",
                }}
              >
                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "6px",
                    fontSize: "0.78rem",
                    color: "#94A3B8",
                    marginBottom: "4px",
                  }}
                >
                  <Compass size={14} color="#38BDF8" />
                  <span>Journeys Planned</span>
                </div>
                <div
                  style={{
                    fontSize: "1.45rem",
                    fontWeight: 800,
                    color: "#FFFFFF",
                  }}
                >
                  {user.total_trips || 4}
                </div>
              </div>

              <div
                style={{
                  padding: "14px 16px",
                  borderRadius: "16px",
                  background: "rgba(255, 255, 255, 0.04)",
                  border: "1px solid rgba(255, 255, 255, 0.08)",
                }}
              >
                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "6px",
                    fontSize: "0.78rem",
                    color: "#94A3B8",
                    marginBottom: "4px",
                  }}
                >
                  <Bookmark size={14} color="#FBBF24" />
                  <span>Saved Plans</span>
                </div>
                <div
                  style={{
                    fontSize: "1.45rem",
                    fontWeight: 800,
                    color: "#FFFFFF",
                  }}
                >
                  {user.saved_trips || 0}
                </div>
              </div>

              <div
                style={{
                  padding: "14px 16px",
                  borderRadius: "16px",
                  background: "rgba(255, 255, 255, 0.04)",
                  border: "1px solid rgba(255, 255, 255, 0.08)",
                }}
              >
                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "6px",
                    fontSize: "0.78rem",
                    color: "#94A3B8",
                    marginBottom: "4px",
                  }}
                >
                  <Leaf size={14} color="#34D399" />
                  <span>Eco Rating</span>
                </div>
                <div
                  style={{
                    fontSize: "1.45rem",
                    fontWeight: 800,
                    color: "#34D399",
                  }}
                >
                  {user.eco_score ? `${user.eco_score}%` : "92%"}
                </div>
              </div>

              <div
                style={{
                  padding: "14px 16px",
                  borderRadius: "16px",
                  background: "rgba(255, 255, 255, 0.04)",
                  border: "1px solid rgba(255, 255, 255, 0.08)",
                }}
              >
                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "6px",
                    fontSize: "0.78rem",
                    color: "#94A3B8",
                    marginBottom: "4px",
                  }}
                >
                  <Globe2 size={14} color="#C084FC" />
                  <span>Regions Explored</span>
                </div>
                <div
                  style={{
                    fontSize: "1.45rem",
                    fontWeight: 800,
                    color: "#FFFFFF",
                  }}
                >
                  {user.countries_visited || 3}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
