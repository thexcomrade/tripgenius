"use client";

import { useState } from "react";
import Link from "next/link";
import {
  Award,
  Sparkles,
  Leaf,
  Compass,
  MapPin,
  Check,
  Lock,
  TrendingUp,
  Shield,
  Star,
  Flame,
  ArrowRight,
} from "lucide-react";
import Button from "../../components/ui/Button";
import Badge from "../../components/ui/Badge";
import { GlassCard, SectionHeader } from "../../components/ui/Card";

interface AchievementItem {
  id: number;
  title: string;
  description: string;
  icon: string;
  tier: "Bronze" | "Silver" | "Gold" | "Platinum";
  category: "General" | "Eco" | "Exploration" | "Budget";
  unlocked: boolean;
  progress: number;
  total: number;
  xp: number;
  unlockedDate?: string;
}

const ACHIEVEMENTS: AchievementItem[] = [
  {
    id: 1,
    title: "Pioneer Traveler",
    description:
      "Generate your first bespoke travel itinerary with TripGenius AI.",
    icon: "✈️",
    tier: "Bronze",
    category: "General",
    unlocked: true,
    progress: 1,
    total: 1,
    xp: 100,
    unlockedDate: "Jan 15, 2026",
  },
  {
    id: 2,
    title: "Green Pathfinder",
    description:
      "Synthesize an itinerary with a sustainability score above 85/100.",
    icon: "🌱",
    tier: "Gold",
    category: "Eco",
    unlocked: true,
    progress: 1,
    total: 1,
    xp: 350,
    unlockedDate: "Feb 02, 2026",
  },
  {
    id: 3,
    title: "Western Ghats Connoisseur",
    description:
      "Plan trips to Munnar, Coorg, and Ooty within one travel season.",
    icon: "⛰️",
    tier: "Silver",
    category: "Exploration",
    unlocked: false,
    progress: 2,
    total: 3,
    xp: 250,
  },
  {
    id: 4,
    title: "Frugal Nomad",
    description:
      "Plan a comprehensive 3+ day trip with an estimated cost under ₹10,000.",
    icon: "💰",
    tier: "Silver",
    category: "Budget",
    unlocked: true,
    progress: 1,
    total: 1,
    xp: 200,
    unlockedDate: "Mar 10, 2026",
  },
  {
    id: 5,
    title: "Carbon Reducer",
    description:
      "Select low-emission transit (Train or EV) across 3 generated journeys.",
    icon: "🍃",
    tier: "Gold",
    category: "Eco",
    unlocked: false,
    progress: 2,
    total: 3,
    xp: 300,
  },
  {
    id: 6,
    title: "Bucket List Collector",
    description:
      "Save 5 or more curated destinations to your personal favorites.",
    icon: "❤️",
    tier: "Bronze",
    category: "General",
    unlocked: true,
    progress: 5,
    total: 5,
    xp: 150,
    unlockedDate: "Mar 18, 2026",
  },
  {
    id: 7,
    title: "Culinary Explorer",
    description:
      "Explore traditional local food recommendations across 4 distinct regions.",
    icon: "🍜",
    tier: "Silver",
    category: "Exploration",
    unlocked: false,
    progress: 3,
    total: 4,
    xp: 250,
  },
  {
    id: 8,
    title: "Master Globetrotter",
    description:
      "Generate 15 complete itineraries and visit all top sanctuaries.",
    icon: "👑",
    tier: "Platinum",
    category: "General",
    unlocked: false,
    progress: 4,
    total: 15,
    xp: 500,
  },
];

export default function AchievementsPage() {
  const [filter, setFilter] = useState<
    "All" | "Unlocked" | "In Progress" | "Eco"
  >("All");

  const filtered = ACHIEVEMENTS.filter((item) => {
    if (filter === "Unlocked") return item.unlocked;
    if (filter === "In Progress") return !item.unlocked;
    if (filter === "Eco") return item.category === "Eco";
    return true;
  });

  const unlockedCount = ACHIEVEMENTS.filter((a) => a.unlocked).length;
  const totalXP = ACHIEVEMENTS.filter((a) => a.unlocked).reduce(
    (sum, a) => sum + a.xp,
    0,
  );

  const getTierBadge = (tier: string) => {
    switch (tier) {
      case "Platinum":
        return (
          <Badge variant="purple" size="sm">
            Platinum Tier
          </Badge>
        );
      case "Gold":
        return (
          <Badge variant="amber" size="sm">
            Gold Tier
          </Badge>
        );
      case "Silver":
        return (
          <Badge variant="neutral" size="sm">
            Silver Tier
          </Badge>
        );
      default:
        return (
          <Badge variant="neutral" size="sm">
            Bronze Tier
          </Badge>
        );
    }
  };

  return (
    <div
      className="page-container"
      style={{ display: "flex", flexDirection: "column", gap: "36px" }}
    >
      {/* LEVEL & XP PROGRESS BANNER */}
      <section
        style={{
          background:
            "linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(14, 165, 233, 0.15) 50%, rgba(15, 23, 42, 0.85) 100%)",
          border: "1px solid rgba(245, 158, 11, 0.30)",
          borderRadius: "28px",
          padding: "36px 32px",
          boxShadow: "0 16px 48px rgba(0, 0, 0, 0.40)",
        }}
      >
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "flex-start",
            flexWrap: "wrap",
            gap: "20px",
            marginBottom: "24px",
          }}
        >
          <div>
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "10px",
                marginBottom: "8px",
              }}
            >
              <Badge
                variant="amber"
                size="sm"
                icon={<Award size={12} fill="#FBBF24" />}
              >
                Traveler Gamification
              </Badge>
              <span
                style={{
                  fontSize: "0.85rem",
                  color: "#FBBF24",
                  fontWeight: 700,
                  display: "flex",
                  alignItems: "center",
                  gap: "4px",
                }}
              >
                <Flame size={14} fill="#F59E0B" /> 2 Week Streak
              </span>
            </div>
            <h1
              style={{
                fontSize: "clamp(1.8rem, 3.5vw, 2.6rem)",
                fontWeight: 900,
                color: "#FFFFFF",
                letterSpacing: "-0.5px",
              }}
            >
              Level 3: Western Ghats Pathfinder
            </h1>
            <p
              style={{
                color: "#94A3B8",
                fontSize: "0.98rem",
                marginTop: "4px",
              }}
            >
              Earn XP by synthesizing custom itineraries, lowering carbon
              impact, and saving escapes.
            </p>
          </div>

          <div style={{ textAlign: "right" }}>
            <span
              style={{ fontSize: "2.4rem", fontWeight: 900, color: "#FBBF24" }}
            >
              {totalXP}{" "}
              <span style={{ fontSize: "1.1rem", fontWeight: 600 }}>XP</span>
            </span>
            <p style={{ fontSize: "0.82rem", color: "#94A3B8" }}>
              Next Level at 1,500 XP
            </p>
          </div>
        </div>

        {/* PROGRESS BAR */}
        <div>
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              fontSize: "0.82rem",
              color: "#CBD5E1",
              marginBottom: "8px",
            }}
          >
            <span>Progress to Level 4 (Globetrotter)</span>
            <span>
              <strong>{Math.round((totalXP / 1500) * 100)}%</strong> ({totalXP}{" "}
              / 1,500 XP)
            </span>
          </div>
          <div
            style={{
              width: "100%",
              height: "10px",
              borderRadius: "999px",
              background: "rgba(255, 255, 255, 0.08)",
              overflow: "hidden",
            }}
          >
            <div
              style={{
                width: `${Math.min(100, (totalXP / 1500) * 100)}%`,
                height: "100%",
                background: "linear-gradient(90deg, #F59E0B 0%, #0EA5E9 100%)",
                borderRadius: "999px",
              }}
            />
          </div>
        </div>
      </section>

      {/* FILTER BUTTONS */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          flexWrap: "wrap",
          gap: "16px",
        }}
      >
        <div>
          <h2 style={{ fontSize: "1.6rem", fontWeight: 800, color: "#FFFFFF" }}>
            Milestones & Badges ({unlockedCount}/{ACHIEVEMENTS.length} Unlocked)
          </h2>
          <p style={{ color: "#94A3B8", fontSize: "0.9rem" }}>
            Unlock rewards as you explore regional destinations sustainably.
          </p>
        </div>

        <div
          style={{
            display: "flex",
            background: "rgba(255, 255, 255, 0.05)",
            borderRadius: "12px",
            padding: "4px",
            border: "1px solid rgba(255, 255, 255, 0.08)",
          }}
        >
          {(["All", "Unlocked", "In Progress", "Eco"] as const).map((tab) => (
            <button
              key={tab}
              type="button"
              onClick={() => setFilter(tab)}
              style={{
                padding: "6px 14px",
                borderRadius: "8px",
                background: filter === tab ? "#0EA5E9" : "transparent",
                color: filter === tab ? "#FFFFFF" : "#94A3B8",
                border: "none",
                fontSize: "0.85rem",
                fontWeight: 600,
                cursor: "pointer",
                transition: "all 0.2s ease",
              }}
            >
              {tab}
            </button>
          ))}
        </div>
      </div>

      {/* ACHIEVEMENTS GRID */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
          gap: "20px",
        }}
      >
        {filtered.map((item) => (
          <GlassCard
            key={item.id}
            style={{
              padding: "24px",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
              gap: "18px",
              opacity: item.unlocked ? 1 : 0.75,
              border: item.unlocked
                ? "1px solid rgba(14, 165, 233, 0.25)"
                : "1px solid rgba(255, 255, 255, 0.06)",
            }}
          >
            <div>
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "flex-start",
                  marginBottom: "14px",
                }}
              >
                <div
                  style={{
                    width: "48px",
                    height: "48px",
                    borderRadius: "14px",
                    background: item.unlocked
                      ? "linear-gradient(135deg, rgba(14, 165, 233, 0.2), rgba(20, 184, 166, 0.2))"
                      : "rgba(255, 255, 255, 0.04)",
                    border: item.unlocked
                      ? "1px solid rgba(14, 165, 233, 0.4)"
                      : "1px solid rgba(255, 255, 255, 0.1)",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontSize: "1.6rem",
                  }}
                >
                  {item.icon}
                </div>
                {getTierBadge(item.tier)}
              </div>

              <h3
                style={{
                  fontSize: "1.15rem",
                  fontWeight: 700,
                  color: "#FFFFFF",
                  marginBottom: "6px",
                }}
              >
                {item.title}
              </h3>
              <p
                style={{
                  color: "#94A3B8",
                  fontSize: "0.85rem",
                  lineHeight: 1.6,
                }}
              >
                {item.description}
              </p>
            </div>

            <div>
              {/* PROGRESS OR UNLOCK BADGE */}
              <div
                style={{
                  borderTop: "1px solid rgba(255, 255, 255, 0.08)",
                  paddingTop: "14px",
                }}
              >
                {item.unlocked ? (
                  <div
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center",
                    }}
                  >
                    <span
                      style={{
                        fontSize: "0.8rem",
                        color: "#34D399",
                        fontWeight: 600,
                        display: "flex",
                        alignItems: "center",
                        gap: "4px",
                      }}
                    >
                      <Check size={14} /> Unlocked on {item.unlockedDate}
                    </span>
                    <Badge variant="amber" size="sm">
                      +{item.xp} XP
                    </Badge>
                  </div>
                ) : (
                  <div>
                    <div
                      style={{
                        display: "flex",
                        justifyContent: "space-between",
                        fontSize: "0.78rem",
                        color: "#94A3B8",
                        marginBottom: "6px",
                      }}
                    >
                      <span>
                        Progress: {item.progress}/{item.total}
                      </span>
                      <span>+{item.xp} XP reward</span>
                    </div>
                    <div
                      style={{
                        width: "100%",
                        height: "6px",
                        borderRadius: "999px",
                        background: "rgba(255, 255, 255, 0.08)",
                        overflow: "hidden",
                      }}
                    >
                      <div
                        style={{
                          width: `${(item.progress / item.total) * 100}%`,
                          height: "100%",
                          background: "#0EA5E9",
                          borderRadius: "999px",
                        }}
                      />
                    </div>
                  </div>
                )}
              </div>
            </div>
          </GlassCard>
        ))}
      </div>
    </div>
  );
}
