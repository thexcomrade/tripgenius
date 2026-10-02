"use client";

import { useEffect, useState } from "react";
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
  Zap,
  CheckCircle2,
} from "lucide-react";
import Button from "../../components/ui/Button";
import Badge from "../../components/ui/Badge";
import { GlassCard, SectionHeader } from "../../components/ui/Card";

interface AchievementItem {
  id: number;
  title: string;
  description: string;
  icon: string;
  tier: "Bronze" | "Silver" | "Gold" | "Platinum" | "Diamond";
  category: "General" | "Eco" | "Exploration" | "Budget" | "Culture";
  unlocked: boolean;
  progress: number;
  total: number;
  xp: number;
  unlockedDate?: string;
  secretHint?: string;
}

const INITIAL_ACHIEVEMENTS: AchievementItem[] = [
  {
    id: 1,
    title: "Pioneer Traveler",
    description: "Generate your first bespoke travel itinerary with TripGenius AI Engine.",
    icon: "✈️",
    tier: "Bronze",
    category: "General",
    unlocked: true,
    progress: 1,
    total: 1,
    xp: 100,
    unlockedDate: "Verified",
  },
  {
    id: 2,
    title: "Green Pathfinder",
    description: "Synthesize an itinerary with a sustainability eco score above 85/100.",
    icon: "🌱",
    tier: "Gold",
    category: "Eco",
    unlocked: true,
    progress: 1,
    total: 1,
    xp: 350,
    unlockedDate: "Verified",
  },
  {
    id: 3,
    title: "Western Ghats Connoisseur",
    description: "Plan trips to Munnar, Coorg, or Ooty with high scenic rating.",
    icon: "⛰️",
    tier: "Silver",
    category: "Exploration",
    unlocked: true,
    progress: 3,
    total: 3,
    xp: 250,
    unlockedDate: "Verified",
  },
  {
    id: 4,
    title: "Bucket List Collector",
    description: "Save 3 or more curated sanctuaries to your personal bucket list.",
    icon: "❤️",
    tier: "Bronze",
    category: "General",
    unlocked: true,
    progress: 3,
    total: 3,
    xp: 150,
    unlockedDate: "Verified",
  },
  {
    id: 5,
    title: "Frugal Nomad",
    description: "Plan 2 comprehensive trips with an estimated cost under ₹15,000.",
    icon: "💰",
    tier: "Silver",
    category: "Budget",
    unlocked: false,
    progress: 1,
    total: 2,
    xp: 200,
    secretHint: "Calibrate stay & transit under ₹15k",
  },
  {
    id: 6,
    title: "Carbon Reducer",
    description: "Select low-emission transit (Scenic Train, Bus, or EV) across 3 journeys.",
    icon: "🍃",
    tier: "Gold",
    category: "Eco",
    unlocked: false,
    progress: 2,
    total: 3,
    xp: 300,
    secretHint: "Select Train or EV in 1 more plan",
  },
  {
    id: 7,
    title: "Spiritual & Heritage Seeker",
    description: "Explore sacred ghats, temple corridors, and ancient civilizations like Varanasi or Hampi.",
    icon: "🛕",
    tier: "Gold",
    category: "Culture",
    unlocked: false,
    progress: 1,
    total: 2,
    xp: 350,
    secretHint: "Plan a trip to Kashi or Hampi ruins",
  },
  {
    id: 8,
    title: "Sacred Ganga Dawn Pilgrim",
    description: "Witness the Subah-e-Banaras dawn rowboat cruise and Dashashwamedh Aarti in Varanasi.",
    icon: "🛶",
    tier: "Gold",
    category: "Culture",
    unlocked: false,
    progress: 0,
    total: 1,
    xp: 400,
    secretHint: "Craft a cultural itinerary for Varanasi",
  },
  {
    id: 9,
    title: "Courtallam Waterfalls Chaser",
    description: "Plan a rejuvenating waterfall trip to Thenkasi & Courtallam during peak Saaral season.",
    icon: "🌊",
    tier: "Silver",
    category: "Exploration",
    unlocked: false,
    progress: 0,
    total: 1,
    xp: 300,
    secretHint: "Explore Thenkasi mineral water cascades",
  },
  {
    id: 10,
    title: "Culinary Trailblazer",
    description: "Savor or bookmark 4 verified regional food trails (Border Parotta, Banarasi Chaat, Malabar Thali, Kodava Curry).",
    icon: "🍲",
    tier: "Gold",
    category: "Culture",
    unlocked: false,
    progress: 2,
    total: 4,
    xp: 350,
    secretHint: "Discover local delicacies in 2 more escapes",
  },
  {
    id: 11,
    title: "Highland Peak Conqueror",
    description: "Summit cloud viewpoints above 2,000m (Kolukkumalai, Doddabetta, or Tadiandamol).",
    icon: "🧗‍♂️",
    tier: "Silver",
    category: "Exploration",
    unlocked: false,
    progress: 1,
    total: 3,
    xp: 300,
    secretHint: "Trek the highest tea estates & peaks",
  },
  {
    id: 12,
    title: "Zero Carbon Champion",
    description: "Complete 5 zero-emission trips using trains, EV mobility, or walking eco-trails.",
    icon: "⚡",
    tier: "Platinum",
    category: "Eco",
    unlocked: false,
    progress: 2,
    total: 5,
    xp: 600,
    secretHint: "Maintain eco score above 90/100",
  },
  {
    id: 13,
    title: "Grand Heritage Maven",
    description: "Synthesize itineraries across 3 UNESCO World Heritage architectural marvels.",
    icon: "🏛️",
    tier: "Platinum",
    category: "Exploration",
    unlocked: false,
    progress: 1,
    total: 3,
    xp: 500,
    secretHint: "Explore Hampi, Taj Mahal, or Paris",
  },
  {
    id: 14,
    title: "Solo Wanderer",
    description: "Plan a solo adventure itinerary tailored with offbeat walking trails and quiet homestays.",
    icon: "🎒",
    tier: "Bronze",
    category: "General",
    unlocked: false,
    progress: 0,
    total: 1,
    xp: 200,
    secretHint: "Select 'Solo Traveler' in AI Planner",
  },
  {
    id: 15,
    title: "Master Explorer Crest",
    description: "Earn 10 total milestones to claim the ultimate Platinum Explorer Crest and VIP traveler rank.",
    icon: "👑",
    tier: "Diamond",
    category: "General",
    unlocked: false,
    progress: 4,
    total: 10,
    xp: 1000,
    secretHint: "Unlock 6 more milestones to earn this crown",
  },
];

export default function AchievementsPage() {
  const [filter, setFilter] = useState<"All" | "Unlocked" | "In Progress" | "Locked" | "Eco" | "Exploration">("All");
  const [achievements, setAchievements] = useState<AchievementItem[]>(INITIAL_ACHIEVEMENTS);

  useEffect(() => {
    // Sync with actual local storage activity
    try {
      const rawSaved = localStorage.getItem("saved_trips");
      const tripCount = rawSaved ? JSON.parse(rawSaved).length : 2;

      setAchievements((prev) =>
        prev.map((a) => {
          if (a.id === 1) return { ...a, unlocked: tripCount >= 1, progress: Math.min(1, tripCount) };
          if (a.id === 15) {
            const unlockedTotal = prev.filter((item) => item.unlocked && item.id !== 15).length;
            return { ...a, progress: unlockedTotal, unlocked: unlockedTotal >= 10 };
          }
          return a;
        }),
      );
    } catch {
      // fallback
    }
  }, []);

  const filtered = achievements.filter((item) => {
    if (filter === "Unlocked") return item.unlocked;
    if (filter === "In Progress") return !item.unlocked && item.progress > 0;
    if (filter === "Locked") return !item.unlocked;
    if (filter === "Eco") return item.category === "Eco";
    if (filter === "Exploration") return item.category === "Exploration" || item.category === "Culture";
    return true;
  });

  const unlockedCount = achievements.filter((a) => a.unlocked).length;
  const totalXP = achievements
    .filter((a) => a.unlocked)
    .reduce((sum, a) => sum + a.xp, 0);

  const level = totalXP >= 2000 ? 5 : totalXP >= 1400 ? 4 : totalXP >= 800 ? 3 : totalXP >= 400 ? 2 : 1;
  const levelTitle =
    level === 5
      ? "Level 5: Grand Legend Pathfinder"
      : level === 4
      ? "Level 4: Global Expedition Master"
      : level === 3
      ? "Level 3: Western Ghats Pathfinder"
      : level === 2
      ? "Level 2: Eco Explorer"
      : "Level 1: Novice Voyager";

  const nextLevelXP = 2500;
  const progressPct = Math.min(100, Math.round((totalXP / nextLevelXP) * 100));

  const getTierBadge = (tier: string) => {
    switch (tier) {
      case "Diamond":
        return (
          <span
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: "4px",
              padding: "4px 10px",
              borderRadius: "8px",
              fontSize: "0.75rem",
              fontWeight: 800,
              background: "linear-gradient(135deg, rgba(56, 189, 248, 0.3), rgba(168, 85, 247, 0.3))",
              border: "1px solid rgba(168, 85, 247, 0.5)",
              color: "#E0E7FF",
              boxShadow: "0 0 14px rgba(168, 85, 247, 0.4)",
            }}
          >
            💎 Diamond Tier
          </span>
        );
      case "Platinum":
        return (
          <span
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: "4px",
              padding: "4px 10px",
              borderRadius: "8px",
              fontSize: "0.75rem",
              fontWeight: 700,
              background: "rgba(168, 85, 247, 0.20)",
              border: "1px solid rgba(168, 85, 247, 0.50)",
              color: "#E9D5FF",
              boxShadow: "0 0 12px rgba(168, 85, 247, 0.35)",
            }}
          >
            ★ Platinum
          </span>
        );
      case "Gold":
        return (
          <span
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: "4px",
              padding: "4px 10px",
              borderRadius: "8px",
              fontSize: "0.75rem",
              fontWeight: 700,
              background: "rgba(245, 158, 11, 0.20)",
              border: "1px solid rgba(245, 158, 11, 0.50)",
              color: "#FEF3C7",
              boxShadow: "0 0 12px rgba(245, 158, 11, 0.30)",
            }}
          >
            ★ Gold Tier
          </span>
        );
      case "Silver":
        return (
          <span
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: "4px",
              padding: "4px 10px",
              borderRadius: "8px",
              fontSize: "0.75rem",
              fontWeight: 700,
              background: "rgba(148, 163, 184, 0.20)",
              border: "1px solid rgba(148, 163, 184, 0.40)",
              color: "#F8FAFC",
            }}
          >
            ★ Silver Tier
          </span>
        );
      default:
        return (
          <span
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: "4px",
              padding: "4px 10px",
              borderRadius: "8px",
              fontSize: "0.75rem",
              fontWeight: 700,
              background: "rgba(217, 119, 6, 0.20)",
              border: "1px solid rgba(217, 119, 6, 0.40)",
              color: "#FED7AA",
            }}
          >
            ★ Bronze Tier
          </span>
        );
    }
  };

  return (
    <div
      style={{
        width: "92%",
        maxWidth: "1360px",
        margin: "0 auto",
        padding: "28px 16px",
        display: "flex",
        flexDirection: "column",
        gap: "32px",
      }}
    >
      {/* LEVEL & XP PROGRESS BANNER */}
      <section
        style={{
          background:
            "linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.90) 100%)",
          border: "1px solid rgba(56, 189, 248, 0.35)",
          borderRadius: "24px",
          padding: "36px 32px",
          boxShadow: "0 16px 48px rgba(0, 0, 0, 0.45)",
          position: "relative",
          overflow: "hidden",
        }}
      >
        {/* GLOW DECORATION */}
        <div
          style={{
            position: "absolute",
            top: "-50px",
            right: "-50px",
            width: "250px",
            height: "250px",
            background: "radial-gradient(circle, rgba(14, 165, 233, 0.25) 0%, transparent 70%)",
            filter: "blur(40px)",
            pointerEvents: "none",
          }}
        />

        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "flex-start",
            flexWrap: "wrap",
            gap: "20px",
            marginBottom: "24px",
            position: "relative",
            zIndex: 1,
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
              <Badge variant="overlay" size="sm" icon={<Award size={13} color="#FBBF24" />}>
                Traveler Gamification & Honors
              </Badge>
              <span
                style={{
                  fontSize: "0.85rem",
                  color: "#FBBF24",
                  fontWeight: 700,
                  display: "flex",
                  alignItems: "center",
                  gap: "4px",
                  background: "rgba(245, 158, 11, 0.15)",
                  padding: "3px 10px",
                  borderRadius: "999px",
                  border: "1px solid rgba(245, 158, 11, 0.30)",
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
                letterSpacing: "-0.03em",
                margin: "4px 0",
              }}
            >
              {levelTitle}
            </h1>
            <p
              style={{
                color: "#94A3B8",
                fontSize: "0.95rem",
                margin: 0,
                maxWidth: "600px",
              }}
            >
              Earn travel experience points (XP) by synthesizing itineraries, selecting green transit, and exploring regional heritage.
            </p>
          </div>

          <div style={{ textAlign: "right" }}>
            <span
              style={{
                fontSize: "2.6rem",
                fontWeight: 900,
                color: "#38BDF8",
                letterSpacing: "-0.03em",
              }}
            >
              {totalXP}{" "}
              <span style={{ fontSize: "1.2rem", fontWeight: 700, color: "#94A3B8" }}>
                XP
              </span>
            </span>
            <p style={{ fontSize: "0.82rem", color: "#64748B", margin: "2px 0 0 0" }}>
              Next Rank at {nextLevelXP} XP
            </p>
          </div>
        </div>

        {/* PROGRESS BAR */}
        <div style={{ position: "relative", zIndex: 1 }}>
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              fontSize: "0.85rem",
              color: "#CBD5E1",
              marginBottom: "8px",
            }}
          >
            <span>Progress to Next Rank</span>
            <span>
              <strong style={{ color: "#38BDF8" }}>{progressPct}%</strong> ({totalXP} / {nextLevelXP} XP)
            </span>
          </div>
          <div
            style={{
              width: "100%",
              height: "12px",
              borderRadius: "999px",
              background: "rgba(255, 255, 255, 0.08)",
              overflow: "hidden",
            }}
          >
            <div
              style={{
                width: `${progressPct}%`,
                height: "100%",
                background: "linear-gradient(90deg, #0EA5E9 0%, #10B981 100%)",
                borderRadius: "999px",
                boxShadow: "0 0 12px rgba(16, 185, 129, 0.5)",
                transition: "width 0.6s ease",
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
          <h2 style={{ fontSize: "1.5rem", fontWeight: 800, color: "#FFFFFF", margin: 0 }}>
            Milestones & Honors ({unlockedCount}/{achievements.length} Unlocked • {achievements.length - unlockedCount} to Earn)
          </h2>
          <p style={{ color: "#94A3B8", fontSize: "0.88rem", marginTop: "4px" }}>
            Unlock achievements as you discover new sanctuaries and travel responsibly.
          </p>
        </div>

        <div
          style={{
            display: "flex",
            background: "rgba(255, 255, 255, 0.05)",
            borderRadius: "12px",
            padding: "4px",
            border: "1px solid rgba(255, 255, 255, 0.10)",
            flexWrap: "wrap",
            gap: "4px",
          }}
        >
          {(["All", "Unlocked", "In Progress", "Locked", "Eco", "Exploration"] as const).map((tab) => (
            <button
              key={tab}
              type="button"
              onClick={() => setFilter(tab)}
              style={{
                padding: "7px 14px",
                borderRadius: "8px",
                background:
                  filter === tab
                    ? "linear-gradient(135deg, #0EA5E9 0%, #10B981 100%)"
                    : "transparent",
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

      {/* ACHIEVEMENTS GRID — 3 BOXES IN A ROW */}
      <div className="grid-3-col">
        {filtered.map((item) => (
          <GlassCard
            key={item.id}
            style={{
              padding: "24px",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
              gap: "18px",
              opacity: item.unlocked ? 1 : 0.88,
              border: item.unlocked
                ? "1px solid rgba(14, 165, 233, 0.35)"
                : item.progress > 0
                ? "1px solid rgba(245, 158, 11, 0.35)"
                : "1px solid rgba(255, 255, 255, 0.08)",
              background: item.unlocked
                ? "rgba(15, 23, 42, 0.85)"
                : item.progress > 0
                ? "rgba(15, 23, 42, 0.70)"
                : "rgba(15, 23, 42, 0.45)",
              boxShadow: item.unlocked
                ? "0 8px 24px rgba(14, 165, 233, 0.15)"
                : item.progress > 0
                ? "0 8px 24px rgba(245, 158, 11, 0.10)"
                : "none",
              transition: "transform 0.2s ease, border-color 0.2s ease",
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
                    width: "50px",
                    height: "50px",
                    borderRadius: "14px",
                    background: item.unlocked
                      ? "linear-gradient(135deg, rgba(14, 165, 233, 0.25), rgba(20, 184, 166, 0.25))"
                      : item.progress > 0
                      ? "rgba(245, 158, 11, 0.15)"
                      : "rgba(255, 255, 255, 0.04)",
                    border: item.unlocked
                      ? "1px solid rgba(14, 165, 233, 0.45)"
                      : item.progress > 0
                      ? "1px solid rgba(245, 158, 11, 0.35)"
                      : "1px solid rgba(255, 255, 255, 0.10)",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontSize: "1.7rem",
                    boxShadow: item.unlocked
                      ? "0 0 16px rgba(14, 165, 233, 0.25)"
                      : "none",
                    position: "relative",
                  }}
                >
                  {item.icon}
                  {!item.unlocked && item.progress === 0 && (
                    <div
                      style={{
                        position: "absolute",
                        bottom: "-4px",
                        right: "-4px",
                        width: "18px",
                        height: "18px",
                        borderRadius: "50%",
                        background: "#0F172A",
                        border: "1px solid rgba(245, 158, 11, 0.6)",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                      }}
                    >
                      <Lock size={10} color="#FBBF24" />
                    </div>
                  )}
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
                  margin: 0,
                }}
              >
                {item.description}
              </p>

              {item.secretHint && !item.unlocked && (
                <div
                  style={{
                    marginTop: "8px",
                    fontSize: "0.76rem",
                    color: "#FBBF24",
                    display: "flex",
                    alignItems: "center",
                    gap: "5px",
                  }}
                >
                  <Sparkles size={11} color="#FBBF24" />
                  <span>Tip: {item.secretHint}</span>
                </div>
              )}
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
                        gap: "5px",
                      }}
                    >
                      <CheckCircle2 size={15} color="#34D399" /> Unlocked & Active
                    </span>
                    <span
                      style={{
                        display: "inline-flex",
                        alignItems: "center",
                        gap: "3px",
                        background: "rgba(56, 189, 248, 0.15)",
                        border: "1px solid rgba(56, 189, 248, 0.35)",
                        color: "#38BDF8",
                        borderRadius: "999px",
                        padding: "3px 10px",
                        fontSize: "0.78rem",
                        fontWeight: 700,
                      }}
                    >
                      +{item.xp} XP
                    </span>
                  </div>
                ) : item.progress === 0 ? (
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
                        color: "#FBBF24",
                        fontWeight: 600,
                        display: "flex",
                        alignItems: "center",
                        gap: "5px",
                      }}
                    >
                      <Lock size={13} color="#FBBF24" /> Locked Reward
                    </span>
                    <span
                      style={{
                        display: "inline-flex",
                        alignItems: "center",
                        gap: "3px",
                        background: "rgba(245, 158, 11, 0.15)",
                        border: "1px solid rgba(245, 158, 11, 0.35)",
                        color: "#FBBF24",
                        borderRadius: "999px",
                        padding: "3px 10px",
                        fontSize: "0.78rem",
                        fontWeight: 700,
                      }}
                    >
                      +{item.xp} XP
                    </span>
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
                      <span style={{ color: "#38BDF8", fontWeight: 600 }}>
                        {item.progress}/{item.total} Completed
                      </span>
                      <span style={{ color: "#FBBF24", fontWeight: 700 }}>+{item.xp} XP reward</span>
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
                          width: `${Math.min(100, Math.round((item.progress / item.total) * 100))}%`,
                          height: "100%",
                          background: "linear-gradient(90deg, #0EA5E9, #10B981)",
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
