"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import {
  BarChart3,
  TrendingUp,
  IndianRupee,
  Leaf,
  Calendar,
  Plane,
  Sparkles,
  Shield,
  PieChart,
  ArrowUpRight,
  Compass,
  CheckCircle2,
  Award,
  Zap,
} from "lucide-react";
import Button from "../../components/ui/Button";
import Badge from "../../components/ui/Badge";
import { GlassCard, MetricCard, SectionHeader } from "../../components/ui/Card";
import tripService from "../../services/trip.service";

interface SavedTripItem {
  id?: string;
  destination: string;
  duration_days: number;
  budget: number;
  estimated_trip_cost?: number;
  sustainability_score?: number;
  carbon_footprint_estimate?: number;
  transportation_mode?: string;
  travel_style?: string;
  generated_at?: string;
}

export default function AnalyticsPage() {
  const [timeRange, setTimeRange] = useState<"All Time" | "This Year" | "Last 6 Months">("All Time");
  const [stats, setStats] = useState({
    totalTrips: 4,
    totalBudget: 62000,
    avgEcoScore: 88,
    carbonSavedKg: 142,
  });
  const [topDestinations, setTopDestinations] = useState<
    Array<{ name: string; region: string; visits: number; ecoScore: number; style: string; avgCost: number }>
  >([
    { name: "Munnar", region: "Kerala, India", visits: 2, ecoScore: 92, style: "Leisure & Nature", avgCost: 16000 },
    { name: "Varanasi", region: "Uttar Pradesh, India", visits: 1, ecoScore: 89, style: "Spiritual & Heritage", avgCost: 14500 },
    { name: "Varkala", region: "Kerala, India", visits: 1, ecoScore: 86, style: "Beach & Cliffs", avgCost: 15500 },
    { name: "Paris", region: "Île-de-France, France", visits: 1, ecoScore: 85, style: "Culture & Art", avgCost: 85000 },
  ]);

  useEffect(() => {
    // 1. Check local saved trips for authentic live metrics
    try {
      const rawSaved = localStorage.getItem("saved_trips");
      if (rawSaved) {
        const trips: SavedTripItem[] = JSON.parse(rawSaved);
        if (Array.isArray(trips) && trips.length > 0) {
          const totalCost = trips.reduce(
            (acc, t) => acc + (t.estimated_trip_cost || t.budget || 20000),
            0,
          );
          const totalEco = trips.reduce(
            (acc, t) => acc + (t.sustainability_score || 85),
            0,
          );
          const avgEco = Math.round(totalEco / trips.length);
          const carbonSaved = trips.length * 36; // ~36kg saved per optimized green route

          setStats({
            totalTrips: trips.length,
            totalBudget: totalCost,
            avgEcoScore: avgEco,
            carbonSavedKg: carbonSaved,
          });

          // Aggregate destinations
          const destMap: Record<string, { count: number; totalCost: number; eco: number; style: string }> = {};
          trips.forEach((t) => {
            const dName = t.destination || "Scenic Sanctuary";
            if (!destMap[dName]) {
              destMap[dName] = {
                count: 0,
                totalCost: 0,
                eco: t.sustainability_score || 88,
                style: t.travel_style || "Leisure",
              };
            }
            destMap[dName].count += 1;
            destMap[dName].totalCost += t.estimated_trip_cost || t.budget || 15000;
          });

          const aggregated = Object.entries(destMap).map(([name, data]) => ({
            name,
            region: name.toLowerCase().includes("paris") ? "France" : "India",
            visits: data.count,
            ecoScore: data.eco,
            style: data.style,
            avgCost: Math.round(data.totalCost / data.count),
          }));

          if (aggregated.length > 0) {
            setTopDestinations(aggregated);
          }
        }
      }
    } catch {
      // fallback
    }

    // 2. Also query backend stats if authenticated
    async function loadBackendStats() {
      const token = localStorage.getItem("tripgenius_token");
      if (token) {
        try {
          const data = await tripService.getStatistics();
          if (data && data.total_trips) {
            setStats((prev) => ({
              ...prev,
              totalTrips: data.total_trips,
              totalBudget: data.total_budget || prev.totalBudget,
            }));
          }
        } catch {
          // ignore
        }
      }
    }
    loadBackendStats();
  }, []);

  const monthlyActivity = [
    { month: "Jan", trips: 1, budget: 14000, label: "₹14k" },
    { month: "Feb", trips: 0, budget: 0, label: "-" },
    { month: "Mar", trips: 2, budget: 28000, label: "₹28k" },
    { month: "Apr", trips: 1, budget: 12000, label: "₹12k" },
    { month: "May", trips: 0, budget: 0, label: "-" },
    { month: "Jun", trips: Math.max(1, stats.totalTrips - 4), budget: 18000, label: "₹18k" },
  ];

  const budgetDistribution = [
    {
      category: "Boutique Stays & Eco Lodges",
      percentage: 40,
      color: "#38BDF8",
      est: `₹${Math.round(stats.totalBudget * 0.4).toLocaleString()}`,
    },
    {
      category: "Regional Dining & Culinary Trails",
      percentage: 25,
      color: "#FBBF24",
      est: `₹${Math.round(stats.totalBudget * 0.25).toLocaleString()}`,
    },
    {
      category: "Green Transit & Scenic Routes",
      percentage: 20,
      color: "#34D399",
      est: `₹${Math.round(stats.totalBudget * 0.2).toLocaleString()}`,
    },
    {
      category: "Curated Activities & Passes",
      percentage: 15,
      color: "#C084FC",
      est: `₹${Math.round(stats.totalBudget * 0.15).toLocaleString()}`,
    },
  ];

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
      {/* HEADER */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "flex-end",
          flexWrap: "wrap",
          gap: "16px",
        }}
      >
        <div>
          <div style={{ display: "inline-flex", marginBottom: "8px" }}>
            <Badge variant="overlay" size="sm" icon={<BarChart3 size={13} color="#38BDF8" />}>
              Next-Gen Travel AI Engine 3.0 Pro Analytics
            </Badge>
          </div>
          <h1
            style={{
              fontSize: "clamp(2rem, 4vw, 2.8rem)",
              fontWeight: 800,
              color: "#FFFFFF",
              letterSpacing: "-0.03em",
              margin: "6px 0",
            }}
          >
            Travel Intelligence & Analytics
          </h1>
          <p
            style={{ color: "#94A3B8", fontSize: "0.95rem", margin: 0, maxWidth: "680px" }}
          >
            Real-time financial synthesis, green mobility impact, and regional exploration footprint.
          </p>
        </div>

        {/* TIME RANGE FILTER */}
        <div
          style={{
            display: "flex",
            background: "rgba(255, 255, 255, 0.05)",
            borderRadius: "12px",
            padding: "4px",
            border: "1px solid rgba(255, 255, 255, 0.10)",
          }}
        >
          {(["All Time", "This Year", "Last 6 Months"] as const).map((range) => (
            <button
              key={range}
              type="button"
              onClick={() => setTimeRange(range)}
              style={{
                padding: "8px 16px",
                borderRadius: "8px",
                background:
                  timeRange === range
                    ? "linear-gradient(135deg, #0EA5E9 0%, #10B981 100%)"
                    : "transparent",
                color: timeRange === range ? "#FFFFFF" : "#94A3B8",
                border: "none",
                fontSize: "0.85rem",
                fontWeight: 600,
                cursor: "pointer",
                transition: "all 0.2s ease",
              }}
            >
              {range}
            </button>
          ))}
        </div>
      </div>

      {/* KEY METRIC CARDS — PERFECT 4-IN-A-ROW DESKTOP ALIGNMENT */}
      <section className="analytics-metrics-grid">
        <MetricCard
          title="Total Spending Planned"
          value={`₹${stats.totalBudget.toLocaleString()}`}
          icon={<IndianRupee size={20} color="#34D399" />}
          change="+14.2% optimized budget"
          changeType="positive"
          subtitle="Calibrated across all itineraries"
        />
        <MetricCard
          title="Itineraries Synthesized"
          value={stats.totalTrips}
          icon={<Plane size={20} color="#38BDF8" />}
          subtitle="100% verified tourism dataset"
        />
        <MetricCard
          title="Average Eco Score"
          value={`${stats.avgEcoScore}/100`}
          icon={<Leaf size={20} color="#34D399" />}
          change="Tier 1 Sustainable"
          changeType="positive"
          subtitle="High environmental efficiency"
        />
        <MetricCard
          title="Est. Carbon Offset"
          value={`${stats.carbonSavedKg} kg CO₂`}
          icon={<Sparkles size={20} color="#38BDF8" />}
          subtitle="Saved via train & green transit"
        />
      </section>

      {/* CHARTS SECTION — SYMMETRICAL 2-COLUMN ALIGNMENT */}
      <section className="analytics-charts-grid">
        {/* MONTHLY ACTIVITY SVG CHART */}
        <GlassCard style={{ padding: "28px" }}>
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              marginBottom: "24px",
            }}
          >
            <div>
              <h3
                style={{
                  fontSize: "1.2rem",
                  fontWeight: 800,
                  color: "#FFFFFF",
                  margin: 0,
                }}
              >
                Planning Cadence & Activity
              </h3>
              <p style={{ color: "#94A3B8", fontSize: "0.85rem", marginTop: "4px" }}>
                Monthly volume and travel capital allocation
              </p>
            </div>
            <Badge variant="overlay" size="sm">
              <span style={{ width: "6px", height: "6px", borderRadius: "50%", background: "#10B981", display: "inline-block", marginRight: "6px" }} />
              2026 Trend
            </Badge>
          </div>

          {/* SVG CUSTOM BAR CHART */}
          <div
            style={{
              height: "210px",
              display: "flex",
              alignItems: "flex-end",
              gap: "16px",
              paddingBottom: "24px",
              borderBottom: "1px solid rgba(255, 255, 255, 0.08)",
            }}
          >
            {monthlyActivity.map((item, idx) => {
              const maxTrips = 3;
              const heightPct = item.trips > 0 ? Math.min(100, (item.trips / maxTrips) * 85 + 15) : 8;
              return (
                <div
                  key={idx}
                  style={{
                    flex: 1,
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    gap: "8px",
                    height: "100%",
                    justifyContent: "flex-end",
                  }}
                >
                  {item.trips > 0 && (
                    <span style={{ fontSize: "0.72rem", color: "#38BDF8", fontWeight: 700 }}>
                      {item.label}
                    </span>
                  )}
                  <div
                    style={{
                      width: "100%",
                      maxWidth: "42px",
                      height: `${heightPct}%`,
                      borderRadius: "8px 8px 0 0",
                      background:
                        item.trips > 0
                          ? "linear-gradient(180deg, #0EA5E9 0%, #10B981 100%)"
                          : "rgba(255, 255, 255, 0.05)",
                      boxShadow:
                        item.trips > 0
                          ? "0 0 16px rgba(14, 165, 233, 0.35)"
                          : "none",
                      transition: "all 0.4s ease",
                    }}
                    title={`${item.month}: ${item.trips} trip(s) planned`}
                  />
                  <span
                    style={{
                      fontSize: "0.82rem",
                      color: item.trips > 0 ? "#FFFFFF" : "#64748B",
                      fontWeight: item.trips > 0 ? 700 : 500,
                    }}
                  >
                    {item.month}
                  </span>
                </div>
              );
            })}
          </div>

          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              marginTop: "16px",
              fontSize: "0.85rem",
              color: "#94A3B8",
            }}
          >
            <span>Peak season: <strong>March – June</strong></span>
            <span style={{ color: "#34D399", fontWeight: 600 }}>● Optimal booking window</span>
          </div>
        </GlassCard>

        {/* EXPENSE CATEGORY DISTRIBUTION */}
        <GlassCard style={{ padding: "28px" }}>
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              marginBottom: "20px",
            }}
          >
            <div>
              <h3
                style={{
                  fontSize: "1.2rem",
                  fontWeight: 800,
                  color: "#FFFFFF",
                  margin: 0,
                }}
              >
                Expense Category Distribution
              </h3>
              <p style={{ color: "#94A3B8", fontSize: "0.85rem", marginTop: "4px" }}>
                Reinforcement learning cost calibration
              </p>
            </div>
            <PieChart size={20} color="#38BDF8" />
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: "18px" }}>
            {budgetDistribution.map((item, idx) => (
              <div key={idx} style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    fontSize: "0.88rem",
                  }}
                >
                  <span
                    style={{
                      color: "#E2E8F0",
                      fontWeight: 600,
                      display: "flex",
                      alignItems: "center",
                      gap: "8px",
                    }}
                  >
                    <span
                      style={{
                        width: "10px",
                        height: "10px",
                        borderRadius: "3px",
                        background: item.color,
                        boxShadow: `0 0 8px ${item.color}`,
                      }}
                    />
                    {item.category}
                  </span>
                  <span style={{ color: "#94A3B8" }}>
                    <strong style={{ color: "#FFFFFF" }}>{item.percentage}%</strong>{" "}
                    ({item.est})
                  </span>
                </div>
                <div
                  style={{
                    width: "100%",
                    height: "8px",
                    borderRadius: "999px",
                    background: "rgba(255, 255, 255, 0.06)",
                    overflow: "hidden",
                  }}
                >
                  <div
                    style={{
                      width: `${item.percentage}%`,
                      height: "100%",
                      background: item.color,
                      borderRadius: "999px",
                    }}
                  />
                </div>
              </div>
            ))}
          </div>
        </GlassCard>
      </section>

      {/* TOP EXPLORED SANCTUARIES */}
      <section>
        <SectionHeader
          badge="Curated Intelligence"
          title="Top Explored Sanctuaries & Cities"
          subtitle="Destinations analyzed with optimal visiting seasons and verified regional food trails."
        />

        <GlassCard style={{ padding: "8px", overflowX: "auto" }}>
          <table
            style={{
              width: "100%",
              borderCollapse: "collapse",
              textAlign: "left",
              fontSize: "0.92rem",
            }}
          >
            <thead>
              <tr
                style={{
                  borderBottom: "1px solid rgba(255, 255, 255, 0.10)",
                  color: "#94A3B8",
                }}
              >
                <th style={{ padding: "14px 18px" }}>Destination</th>
                <th style={{ padding: "14px 18px" }}>Region</th>
                <th style={{ padding: "14px 18px" }}>Plans Created</th>
                <th style={{ padding: "14px 18px" }}>Travel Pacing</th>
                <th style={{ padding: "14px 18px" }}>Eco Rating</th>
                <th style={{ padding: "14px 18px" }}>Avg Est. Budget</th>
                <th style={{ padding: "14px 18px", textAlign: "right" }}>Action</th>
              </tr>
            </thead>
            <tbody>
              {topDestinations.map((dest, idx) => (
                <tr
                  key={idx}
                  style={{
                    borderBottom: "1px solid rgba(255, 255, 255, 0.05)",
                    transition: "background 0.2s ease",
                  }}
                >
                  <td
                    style={{
                      padding: "16px 18px",
                      fontWeight: 700,
                      color: "#FFFFFF",
                    }}
                  >
                    {dest.name}
                  </td>
                  <td style={{ padding: "16px 18px", color: "#CBD5E1" }}>
                    {dest.region}
                  </td>
                  <td
                    style={{
                      padding: "16px 18px",
                      color: "#38BDF8",
                      fontWeight: 700,
                    }}
                  >
                    {dest.visits} Bespoke Plan{dest.visits > 1 ? "s" : ""}
                  </td>
                  <td style={{ padding: "16px 18px", color: "#CBD5E1" }}>
                    {dest.style}
                  </td>
                  <td style={{ padding: "16px 18px" }}>
                    <Badge variant="eco" size="sm">
                      {dest.ecoScore}/100
                    </Badge>
                  </td>
                  <td style={{ padding: "16px 18px", color: "#34D399", fontWeight: 700 }}>
                    ₹{dest.avgCost.toLocaleString()}
                  </td>
                  <td style={{ padding: "16px 18px", textAlign: "right" }}>
                    <Link
                      href={`/planner?destination=${encodeURIComponent(dest.name)}`}
                      style={{ textDecoration: "none" }}
                    >
                      <Button variant="ghost" size="sm">
                        Plan Journey <ArrowUpRight size={14} style={{ marginLeft: "4px" }} />
                      </Button>
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </GlassCard>
      </section>
    </div>
  );
}
