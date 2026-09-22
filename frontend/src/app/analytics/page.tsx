"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import {
  BarChart3,
  TrendingUp,
  DollarSign,
  Leaf,
  Calendar,
  Plane,
  Sparkles,
  Shield,
  PieChart,
  ArrowUpRight,
} from "lucide-react";
import Button from "../../components/ui/Button";
import Badge from "../../components/ui/Badge";
import { GlassCard, MetricCard, SectionHeader } from "../../components/ui/Card";
import tripService from "../../services/trip.service";

export default function AnalyticsPage() {
  const [timeRange, setTimeRange] = useState("All Time");
  const [stats, setStats] = useState({
    totalTrips: 4,
    totalBudget: 62000,
    avgEcoScore: 86,
    carbonSavedKg: 142,
  });

  useEffect(() => {
    async function loadAnalytics() {
      const token = localStorage.getItem("tripgenius_token");
      if (token) {
        try {
          const data = await tripService.getStatistics();
          if (data) {
            setStats((prev) => ({
              ...prev,
              totalTrips: data.total_trips || prev.totalTrips,
              totalBudget:
                data.total_budget || data.average_budget
                  ? data.average_budget * (data.total_trips || 1)
                  : prev.totalBudget,
            }));
          }
        } catch {
          // ignore
        }
      }
    }

    loadAnalytics();
  }, []);

  const monthlyActivity = [
    { month: "Jan", trips: 1, budget: 14000 },
    { month: "Feb", trips: 0, budget: 0 },
    { month: "Mar", trips: 2, budget: 28000 },
    { month: "Apr", trips: 1, budget: 12000 },
    { month: "May", trips: 0, budget: 0 },
    { month: "Jun", trips: 1, budget: 15000 },
  ];

  const budgetDistribution = [
    {
      category: "Accommodations",
      percentage: 40,
      color: "#38BDF8",
      est: "₹24,800",
    },
    {
      category: "Regional Dining",
      percentage: 25,
      color: "#FBBF24",
      est: "₹15,500",
    },
    {
      category: "Transit & Mobility",
      percentage: 20,
      color: "#34D399",
      est: "₹12,400",
    },
    {
      category: "Activities & Heritage",
      percentage: 15,
      color: "#C084FC",
      est: "₹9,300",
    },
  ];

  const topDestinations = [
    {
      name: "Munnar",
      state: "Kerala",
      visits: 2,
      ecoScore: 92,
      style: "Leisure & Nature",
    },
    {
      name: "Coorg",
      state: "Karnataka",
      visits: 1,
      ecoScore: 88,
      style: "Plantation Trails",
    },
    {
      name: "Varkala",
      state: "Kerala",
      visits: 1,
      ecoScore: 84,
      style: "Beach & Cliffs",
    },
  ];

  return (
    <div
      className="page-container"
      style={{ display: "flex", flexDirection: "column", gap: "36px" }}
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
            <Badge variant="ai" size="sm" icon={<BarChart3 size={12} />}>
              Travel Intelligence & Insights
            </Badge>
          </div>
          <h1
            style={{
              fontSize: "clamp(2rem, 4vw, 2.8rem)",
              fontWeight: 900,
              color: "#FFFFFF",
              letterSpacing: "-0.5px",
            }}
          >
            Travel Analytics
          </h1>
          <p
            style={{ color: "#94A3B8", fontSize: "0.95rem", marginTop: "4px" }}
          >
            Comprehensive metrics on your travel spending, regional
            explorations, and carbon savings.
          </p>
        </div>

        {/* TIME RANGE FILTER */}
        <div
          style={{
            display: "flex",
            background: "rgba(255, 255, 255, 0.05)",
            borderRadius: "12px",
            padding: "4px",
            border: "1px solid rgba(255, 255, 255, 0.08)",
          }}
        >
          {["All Time", "This Year", "Last 6 Months"].map((range) => (
            <button
              key={range}
              type="button"
              onClick={() => setTimeRange(range)}
              style={{
                padding: "6px 14px",
                borderRadius: "8px",
                background: timeRange === range ? "#0EA5E9" : "transparent",
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

      {/* KEY METRIC CARDS */}
      <section
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))",
          gap: "20px",
        }}
      >
        <MetricCard
          title="Total Spending Allocated"
          value={`₹${stats.totalBudget.toLocaleString()}`}
          icon={<DollarSign size={20} />}
          change="+12% vs last period"
          changeType="positive"
          subtitle="Aggregated across itineraries"
        />
        <MetricCard
          title="Itineraries Synthesized"
          value={stats.totalTrips}
          icon={<Plane size={20} />}
          subtitle="100% data-verified"
        />
        <MetricCard
          title="Average Eco Score"
          value={`${stats.avgEcoScore}/100`}
          icon={<Leaf size={20} color="#34D399" />}
          change="High Sustainability"
          changeType="positive"
          subtitle="Low emission profile"
        />
        <MetricCard
          title="Est. Carbon Offset"
          value={`${stats.carbonSavedKg} kg`}
          icon={<Sparkles size={20} color="#38BDF8" />}
          subtitle="CO₂ saved via green transit"
        />
      </section>

      {/* CHARTS SECTION */}
      <section
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(340px, 1fr))",
          gap: "24px",
        }}
      >
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
                }}
              >
                Planning Activity & Volume
              </h3>
              <p style={{ color: "#94A3B8", fontSize: "0.85rem" }}>
                Trips scheduled by month
              </p>
            </div>
            <Badge variant="neutral" size="sm">
              2026 Trend
            </Badge>
          </div>

          {/* SIMPLE CUSTOM SVG BAR CHART */}
          <div
            style={{
              height: "200px",
              display: "flex",
              alignItems: "flex-end",
              gap: "18px",
              paddingBottom: "24px",
              borderBottom: "1px solid rgba(255, 255, 255, 0.08)",
            }}
          >
            {monthlyActivity.map((item, idx) => {
              const barHeight =
                item.trips > 0 ? `${item.trips * 45 + 15}%` : "8px";
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
                  <div
                    style={{
                      width: "100%",
                      maxWidth: "36px",
                      height: barHeight,
                      borderRadius: "8px 8px 0 0",
                      background:
                        item.trips > 0
                          ? "linear-gradient(180deg, #0EA5E9 0%, #14B8A6 100%)"
                          : "rgba(255, 255, 255, 0.05)",
                      boxShadow:
                        item.trips > 0
                          ? "0 0 12px rgba(14, 165, 233, 0.3)"
                          : "none",
                      transition: "height 0.4s ease",
                    }}
                    title={`${item.month}: ${item.trips} trips planned`}
                  />
                  <span
                    style={{
                      fontSize: "0.8rem",
                      color: item.trips > 0 ? "#E2E8F0" : "#64748B",
                      fontWeight: 600,
                    }}
                  >
                    {item.month}
                  </span>
                </div>
              );
            })}
          </div>
        </GlassCard>

        {/* BUDGET BREAKDOWN CATEGORIES */}
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
                }}
              >
                Expense Category Distribution
              </h3>
              <p style={{ color: "#94A3B8", fontSize: "0.85rem" }}>
                Share of total vacation budget
              </p>
            </div>
            <PieChart size={18} color="#38BDF8" />
          </div>

          <div
            style={{ display: "flex", flexDirection: "column", gap: "16px" }}
          >
            {budgetDistribution.map((item, idx) => (
              <div
                key={idx}
                style={{ display: "flex", flexDirection: "column", gap: "6px" }}
              >
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
                      }}
                    />
                    {item.category}
                  </span>
                  <span style={{ color: "#94A3B8" }}>
                    <strong style={{ color: "#FFFFFF" }}>
                      {item.percentage}%
                    </strong>{" "}
                    ({item.est})
                  </span>
                </div>
                <div
                  style={{
                    width: "100%",
                    height: "6px",
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

      {/* TOP DESTINATIONS TABLE */}
      <section>
        <SectionHeader
          badge="Geographic Distribution"
          title="Top Explored Sanctuaries"
          subtitle="Destinations with the highest itinerary generation frequency and average ratings."
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
                <th style={{ padding: "14px 18px" }}>Itineraries</th>
                <th style={{ padding: "14px 18px" }}>Travel Style</th>
                <th style={{ padding: "14px 18px" }}>Eco Rating</th>
                <th style={{ padding: "14px 18px", textAlign: "right" }}>
                  Action
                </th>
              </tr>
            </thead>
            <tbody>
              {topDestinations.map((dest, idx) => (
                <tr
                  key={idx}
                  style={{
                    borderBottom: "1px solid rgba(255, 255, 255, 0.05)",
                  }}
                >
                  <td
                    style={{
                      padding: "14px 18px",
                      fontWeight: 700,
                      color: "#FFFFFF",
                    }}
                  >
                    {dest.name}
                  </td>
                  <td style={{ padding: "14px 18px", color: "#CBD5E1" }}>
                    {dest.state}
                  </td>
                  <td
                    style={{
                      padding: "14px 18px",
                      color: "#38BDF8",
                      fontWeight: 600,
                    }}
                  >
                    {dest.visits} Planned
                  </td>
                  <td style={{ padding: "14px 18px", color: "#CBD5E1" }}>
                    {dest.style}
                  </td>
                  <td style={{ padding: "14px 18px" }}>
                    <Badge variant="eco" size="sm">
                      {dest.ecoScore}/100
                    </Badge>
                  </td>
                  <td style={{ padding: "14px 18px", textAlign: "right" }}>
                    <Link
                      href={`/planner?destination=${encodeURIComponent(dest.name)}`}
                      style={{ textDecoration: "none" }}
                    >
                      <span
                        style={{
                          color: "#38BDF8",
                          fontSize: "0.82rem",
                          fontWeight: 600,
                          display: "inline-flex",
                          alignItems: "center",
                          gap: "4px",
                        }}
                      >
                        Re-Plan <ArrowUpRight size={14} />
                      </span>
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
