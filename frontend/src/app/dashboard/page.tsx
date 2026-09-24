"use client";

import { useEffect, useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  Sparkles,
  Plane,
  Compass,
  Calendar,
  Heart,
  Leaf,
  Award,
  TrendingUp,
  MapPin,
  ArrowRight,
  CloudSun,
  Bot,
  Clock,
  DollarSign,
  BarChart3,
  Settings,
  History,
  ChevronRight,
} from "lucide-react";
import Button from "../../components/ui/Button";
import Badge from "../../components/ui/Badge";
import { GlassCard, MetricCard, SectionHeader } from "../../components/ui/Card";
import tripService from "../../services/trip.service";
import { parseDestinationQuery } from "../../utils/queryParser";

interface SavedTripSummary {
  id?: string;
  trip_title?: string;
  destination: string;
  duration_days: number;
  budget: number;
  sustainability_score?: number;
  saved_at?: string;
  created_at?: string;
}

export default function DashboardPage() {
  const router = useRouter();

  const [greeting, setGreeting] = useState("Welcome");
  const [userName, setUserName] = useState("Sivya Babu");
  const [tripGeniusId, setTripGeniusId] = useState("TG-SB8842");
  const [totalTrips, setTotalTrips] = useState(4);
  const [savedTrips, setSavedTrips] = useState(0);
  const [ecoScore, setEcoScore] = useState(92);
  const [recentTrips, setRecentTrips] = useState<SavedTripSummary[]>([]);
  const [promptInput, setPromptInput] = useState("");
  const [loading, setLoading] = useState(true);
  const [destFilter, setDestFilter] = useState<"all" | "india" | "abroad">("all");

  const [weatherCity, setWeatherCity] = useState("Trivandrum");
  const [weatherLoading, setWeatherLoading] = useState(false);
  const [weatherData, setWeatherData] = useState<{
    city: string;
    temperature: number;
    condition: string;
    description: string;
    humidity: number;
    wind_speed: number;
    travel_recommendation?: string;
  }>({
    city: "Trivandrum (Thiruvananthapuram)",
    temperature: 29,
    condition: "Partly Sunny",
    description: "Pleasant coastal breeze along Shankhumukham and Kovalam",
    humidity: 74,
    wind_speed: 14,
    travel_recommendation: "Great conditions for coastal exploration and sunset photography.",
  });

  useEffect(() => {
    const hour = new Date().getHours();
    if (hour < 12) setGreeting("Good morning");
    else if (hour < 17) setGreeting("Good afternoon");
    else if (hour < 21) setGreeting("Good evening");
    else setGreeting("Good night");

    // Load user profile
    const storedUser = localStorage.getItem("tripgenius_user");
    if (storedUser) {
      try {
        const user = JSON.parse(storedUser);
        if (user.full_name && user.full_name !== "Traveler") {
          setUserName(user.full_name);
        } else {
          setUserName("Sivya Babu");
        }
        if (user.tripgenius_id) setTripGeniusId(user.tripgenius_id);
        if (user.eco_score !== undefined) setEcoScore(user.eco_score);
      } catch {
        // ignore
      }
    }

    // Fetch backend trips / history
    const loadDashboardData = async () => {
      const token = localStorage.getItem("tripgenius_token");
      if (token) {
        try {
          const stats = await tripService.getStatistics();
          if (stats) {
            setTotalTrips(stats.total_trips || 0);
            setSavedTrips(stats.favorite_trips || 0);
          }

          const hist = await tripService.getHistory();
          if (hist && hist.trips) {
            setRecentTrips(hist.trips.slice(0, 3));
            if (!stats) setTotalTrips(hist.total_trips || hist.trips.length);
          }
        } catch {
          // Fallback to local storage
          loadFromLocalStorage();
        }
      } else {
        loadFromLocalStorage();
      }
      setLoading(false);
    };

    const loadFromLocalStorage = () => {
      try {
        const storedTrips = localStorage.getItem("saved_trips");
        if (storedTrips) {
          const parsed = JSON.parse(storedTrips);
          setRecentTrips(parsed.slice(0, 3));
          setSavedTrips(parsed.length);
          setTotalTrips(parsed.length);
        }
      } catch {
        // ignore
      }
    };

    loadDashboardData();
  }, []);

  // Fetch live weather data for selected city
  useEffect(() => {
    const fetchWeather = async () => {
      setWeatherLoading(true);
      try {
        const res = await fetch(
          `http://127.0.0.1:8000/api/weather?city=${encodeURIComponent(weatherCity)}`,
        );
        if (res.ok) {
          const data = await res.json();
          if (data && data.temperature !== undefined) {
            setWeatherData({
              city: data.city || weatherCity,
              temperature: Math.round(data.temperature),
              condition: data.condition || "Pleasant",
              description: data.description || "Clear skies with light breeze",
              humidity: data.humidity || 70,
              wind_speed: Math.round(data.wind_speed || 12),
              travel_recommendation: data.travel_recommendation,
            });
          }
        }
      } catch {
        // keep fallback
      } finally {
        setWeatherLoading(false);
      }
    };
    fetchWeather();
  }, [weatherCity]);

  const handlePromptSubmit = (
    e?: React.FormEvent,
    customDest?: string,
    customDuration?: number,
  ) => {
    if (e) e.preventDefault();
    const query = customDest || promptInput;
    if (query.trim()) {
      const parsed = parseDestinationQuery(query);
      const dest = customDest || parsed.destination || query.trim();
      const dur =
        customDuration !== undefined ? customDuration : parsed.duration;
      router.push(
        `/planner?destination=${encodeURIComponent(dest)}&duration=${dur}`,
      );
    } else {
      router.push("/planner");
    }
  };

  const curatedDestinations = [
    {
      name: "Munnar",
      region: "india",
      state: "Kerala, India",
      days: "3-4 Days",
      image: "/destinations/munnar.jpg",
      eco: "92/100",
    },
    {
      name: "Hampi",
      region: "india",
      state: "Karnataka, India",
      days: "3-4 Days",
      image: "/destinations/hampi.jpg",
      eco: "90/100",
    },
    {
      name: "Gokarna",
      region: "india",
      state: "Karnataka, India",
      days: "2-4 Days",
      image: "/destinations/gokarna.jpg",
      eco: "87/100",
    },
    {
      name: "Thekkady",
      region: "india",
      state: "Kerala, India",
      days: "2-3 Days",
      image: "/destinations/thekkady.jpg",
      eco: "96/100",
    },
    {
      name: "Kovalam",
      region: "india",
      state: "Kerala, India",
      days: "2-3 Days",
      image: "/destinations/kovalam.jpg",
      eco: "86/100",
    },
    {
      name: "Coorg",
      region: "india",
      state: "Karnataka, India",
      days: "3-5 Days",
      image: "/destinations/coorg.jpg",
      eco: "94/100",
    },
    {
      name: "Paris",
      region: "abroad",
      state: "France",
      days: "4-6 Days",
      image: "/destinations/paris.jpg",
      eco: "84/100",
    },
    {
      name: "Tokyo",
      region: "abroad",
      state: "Japan",
      days: "5-7 Days",
      image: "/destinations/tokyo.jpg",
      eco: "89/100",
    },
    {
      name: "Bali",
      region: "abroad",
      state: "Indonesia",
      days: "4-6 Days",
      image: "/destinations/bali.jpg",
      eco: "91/100",
    },
    {
      name: "Dubai",
      region: "abroad",
      state: "United Arab Emirates",
      days: "3-5 Days",
      image: "/destinations/dubai.jpg",
      eco: "80/100",
    },
  ];

  return (
    <div
      className="page-container"
      style={{ display: "flex", flexDirection: "column", gap: "36px" }}
    >
      {/* TOP COMMAND CENTER HERO */}
      <section
        style={{
          background:
            "linear-gradient(135deg, rgba(14, 165, 233, 0.15) 0%, rgba(20, 184, 166, 0.12) 50%, rgba(15, 23, 42, 0.85) 100%)",
          border: "1px solid rgba(14, 165, 233, 0.25)",
          borderRadius: "28px",
          padding: "36px 32px",
          position: "relative",
          overflow: "hidden",
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
              <Badge variant="ai" size="sm" icon={<Sparkles size={12} />}>
                AI Command Center
              </Badge>
              <span style={{ fontSize: "0.82rem", color: "#94A3B8" }}>
                ID: <strong style={{ color: "#E2E8F0" }}>{tripGeniusId}</strong>
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
              {greeting}, {userName.split(" ")[0]}!
            </h1>
            <p style={{ color: "#94A3B8", fontSize: "1rem", marginTop: "4px" }}>
              Where should TripGenius take you next? Select a curated escape or
              generate a bespoke itinerary.
            </p>
          </div>

          <div style={{ display: "flex", gap: "10px" }}>
            <Link href="/planner" style={{ textDecoration: "none" }}>
              <Button
                variant="primary"
                size="md"
                leftIcon={<Sparkles size={16} />}
              >
                Plan New Itinerary
              </Button>
            </Link>
            <Link href="/explore" style={{ textDecoration: "none" }}>
              <Button
                variant="secondary"
                size="md"
                leftIcon={<Compass size={16} />}
              >
                Explore
              </Button>
            </Link>
          </div>
        </div>

        {/* AI PROMPT LAUNCH BAR */}
        <form
          onSubmit={(e) => handlePromptSubmit(e)}
          style={{
            display: "flex",
            alignItems: "center",
            gap: "10px",
            background: "rgba(15, 23, 42, 0.85)",
            backdropFilter: "blur(20px)",
            border: "1px solid rgba(255, 255, 255, 0.12)",
            borderRadius: "16px",
            padding: "8px 12px 8px 18px",
            boxShadow: "0 8px 24px rgba(0, 0, 0, 0.30)",
          }}
        >
          <Bot size={20} color="#38BDF8" style={{ flexShrink: 0 }} />
          <input
            type="text"
            value={promptInput}
            onChange={(e) => setPromptInput(e.target.value)}
            placeholder="Type any trip: '3 days goa', '5 days munnar', 'varkala', 'coorg'..."
            style={{
              flex: 1,
              background: "transparent",
              border: "none",
              color: "#FFFFFF",
              fontSize: "0.95rem",
              outline: "none",
            }}
          />
          <Button
            type="submit"
            variant="primary"
            size="sm"
            rightIcon={<ArrowRight size={14} />}
          >
            Generate
          </Button>
        </form>

        {/* LIVE QUERY AUTO-DETECTION PILL */}
        {(() => {
          const parsed = parseDestinationQuery(promptInput);
          if (promptInput.trim().length >= 2 && parsed.destination) {
            return (
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                  marginTop: "12px",
                  padding: "8px 14px",
                  borderRadius: "12px",
                  background: "rgba(14, 165, 233, 0.15)",
                  border: "1px solid rgba(14, 165, 233, 0.35)",
                  fontSize: "0.85rem",
                  flexWrap: "wrap",
                  gap: "8px",
                }}
              >
                <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                  <Sparkles size={14} color="#38BDF8" />
                  <span style={{ color: "#E2E8F0" }}>
                    Detected Destination:{" "}
                    <strong style={{ color: "#38BDF8" }}>
                      {parsed.destination}
                    </strong>{" "}
                    • Duration:{" "}
                    <strong style={{ color: "#34D399" }}>
                      {parsed.duration} Days
                    </strong>
                  </span>
                </div>
                <button
                  type="button"
                  onClick={() =>
                    handlePromptSubmit(
                      undefined,
                      parsed.destination,
                      parsed.duration,
                    )
                  }
                  style={{
                    background:
                      "linear-gradient(135deg, #0EA5E9 0%, #10B981 100%)",
                    border: "none",
                    borderRadius: "8px",
                    padding: "5px 12px",
                    color: "#FFFFFF",
                    fontSize: "0.78rem",
                    fontWeight: 700,
                    cursor: "pointer",
                    boxShadow: "0 2px 8px rgba(14, 165, 233, 0.35)",
                  }}
                >
                  Select & Plan →
                </button>
              </div>
            );
          }
          return null;
        })()}

        {/* QUICK SUGGESTION CHIPS */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "8px",
            marginTop: "12px",
            flexWrap: "wrap",
          }}
        >
          <span style={{ fontSize: "0.78rem", color: "#94A3B8", fontWeight: 500 }}>
            Quick Select:
          </span>
          {[
            { dest: "Goa", days: 3 },
            { dest: "Varkala", days: 3 },
            { dest: "Munnar", days: 4 },
            { dest: "Coorg", days: 3 },
            { dest: "Hampi", days: 3 },
            { dest: "Kovalam", days: 3 },
            { dest: "Paris", days: 5 },
          ].map((chip) => (
            <button
              key={chip.dest}
              type="button"
              onClick={() => {
                setPromptInput(`${chip.days} days ${chip.dest}`);
                handlePromptSubmit(undefined, chip.dest, chip.days);
              }}
              style={{
                background: "rgba(255, 255, 255, 0.05)",
                border: "1px solid rgba(255, 255, 255, 0.10)",
                borderRadius: "999px",
                padding: "4px 11px",
                color: "#CBD5E1",
                fontSize: "0.78rem",
                cursor: "pointer",
                transition: "all 0.15s ease",
              }}
              onMouseOver={(e) => {
                e.currentTarget.style.background = "rgba(14, 165, 233, 0.20)";
                e.currentTarget.style.borderColor = "rgba(14, 165, 233, 0.40)";
                e.currentTarget.style.color = "#FFFFFF";
              }}
              onMouseOut={(e) => {
                e.currentTarget.style.background = "rgba(255, 255, 255, 0.05)";
                e.currentTarget.style.borderColor = "rgba(255, 255, 255, 0.10)";
                e.currentTarget.style.color = "#CBD5E1";
              }}
            >
              🌴 {chip.dest} ({chip.days} Days)
            </button>
          ))}
        </div>
      </section>

      {/* KEY METRICS GRID */}
      <section
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))",
          gap: "20px",
        }}
      >
        <MetricCard
          title="Total Trips Created"
          value={totalTrips}
          icon={<Plane size={20} />}
          subtitle="Generated with AI engine"
          onClick={() => router.push("/trip/history")}
        />
        <MetricCard
          title="Saved Escapes"
          value={savedTrips}
          icon={<Heart size={20} />}
          subtitle="Saved in bucket list"
          onClick={() => router.push("/favorites")}
        />
        <MetricCard
          title="Eco Travel Score"
          value={`${ecoScore}/100`}
          icon={<Leaf size={20} color="#34D399" />}
          change="+5% vs avg"
          changeType="positive"
          subtitle="Sustainable travel impact"
          onClick={() => router.push("/analytics")}
        />
        <MetricCard
          title="Explorer Rank"
          value="Level 3"
          icon={<Award size={20} color="#FBBF24" />}
          subtitle="Western Ghats Pathfinder"
          onClick={() => router.push("/achievements")}
        />
      </section>

      {/* SECONDARY ROW: WEATHER & QUICK NAVIGATION */}
      <section
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))",
          gap: "24px",
        }}
      >
        {/* LIVE WEATHER SNAPSHOT */}
        <GlassCard
          style={{
            padding: "26px",
            display: "flex",
            flexDirection: "column",
            justifyContent: "space-between",
            gap: "16px",
          }}
        >
          <div>
            <div
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                marginBottom: "14px",
                flexWrap: "wrap",
                gap: "8px",
              }}
            >
              <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                <CloudSun size={20} color="#FBBF24" />
                <h3
                  style={{
                    fontSize: "1.1rem",
                    fontWeight: 700,
                    color: "#FFFFFF",
                  }}
                >
                  Live Weather Intelligence
                </h3>
              </div>
              <Badge variant="amber" size="sm">
                {weatherLoading ? "Updating..." : "Real-time"}
              </Badge>
            </div>

            {/* QUICK CITY SWITCHER TABS */}
            <div
              style={{
                display: "flex",
                gap: "6px",
                marginBottom: "16px",
                overflowX: "auto",
                paddingBottom: "4px",
              }}
            >
              {[
                { label: "Trivandrum", city: "Thiruvananthapuram" },
                { label: "Varkala", city: "Varkala" },
                { label: "Munnar", city: "Munnar" },
                { label: "Goa", city: "Goa" },
                { label: "Kochi", city: "Kochi" },
              ].map((loc) => {
                const isActive =
                  weatherCity.toLowerCase() === loc.city.toLowerCase() ||
                  weatherCity.toLowerCase() === loc.label.toLowerCase();
                return (
                  <button
                    key={loc.label}
                    type="button"
                    onClick={() => setWeatherCity(loc.city)}
                    style={{
                      background: isActive
                        ? "rgba(14, 165, 233, 0.25)"
                        : "rgba(255, 255, 255, 0.05)",
                      border: isActive
                        ? "1px solid rgba(14, 165, 233, 0.50)"
                        : "1px solid rgba(255, 255, 255, 0.08)",
                      borderRadius: "8px",
                      padding: "4px 10px",
                      color: isActive ? "#38BDF8" : "#94A3B8",
                      fontSize: "0.78rem",
                      fontWeight: isActive ? 700 : 500,
                      cursor: "pointer",
                      whiteSpace: "nowrap",
                      transition: "all 0.15s ease",
                    }}
                  >
                    {loc.label}
                  </button>
                );
              })}
            </div>

            <div
              style={{
                display: "flex",
                alignItems: "baseline",
                justifyContent: "space-between",
                marginBottom: "14px",
              }}
            >
              <div>
                <span
                  style={{
                    fontSize: "2.6rem",
                    fontWeight: 800,
                    color: "#FFFFFF",
                  }}
                >
                  {weatherData.temperature}°C
                </span>
                <p style={{ color: "#94A3B8", fontSize: "0.9rem", marginTop: "2px" }}>
                  {weatherData.city} • {weatherData.condition}
                </p>
                <p style={{ color: "#64748B", fontSize: "0.8rem" }}>
                  {weatherData.description}
                </p>
              </div>
              <div
                style={{
                  textAlign: "right",
                  fontSize: "0.85rem",
                  color: "#CBD5E1",
                }}
              >
                <p>
                  Humidity: <strong>{weatherData.humidity}%</strong>
                </p>
                <p>
                  Wind: <strong>{weatherData.wind_speed} km/h</strong>
                </p>
              </div>
            </div>
          </div>

          <div
            style={{
              background: "rgba(255, 255, 255, 0.04)",
              padding: "12px 14px",
              borderRadius: "12px",
              border: "1px solid rgba(255, 255, 255, 0.08)",
            }}
          >
            <p
              style={{ color: "#38BDF8", fontSize: "0.85rem", fontWeight: 500 }}
            >
              💡 {weatherData.travel_recommendation ||
                "Favorable weather conditions for travel exploration and outdoor activities."}
            </p>
          </div>
        </GlassCard>

        {/* AI TRAVEL COMPANION CARD */}
        <GlassCard
          style={{
            padding: "26px",
            display: "flex",
            flexDirection: "column",
            justifyContent: "space-between",
          }}
        >
          <div>
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "10px",
                marginBottom: "12px",
              }}
            >
              <div
                style={{
                  width: "36px",
                  height: "36px",
                  borderRadius: "10px",
                  background: "rgba(14, 165, 233, 0.15)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                <Bot size={20} color="#38BDF8" />
              </div>
              <div>
                <h3
                  style={{
                    fontSize: "1.1rem",
                    fontWeight: 700,
                    color: "#FFFFFF",
                  }}
                >
                  AI Travel Companion
                </h3>
                <p style={{ fontSize: "0.82rem", color: "#94A3B8" }}>
                  Real-time itinerary assistant
                </p>
              </div>
            </div>
            <p
              style={{
                color: "#CBD5E1",
                fontSize: "0.92rem",
                lineHeight: 1.6,
                marginBottom: "18px",
              }}
            >
              Have questions about local food trails, hidden spots, or train
              connections? Ask the TripGenius AI Assistant anytime.
            </p>
          </div>

          <Link href="/ai-chat" style={{ textDecoration: "none" }}>
            <Button
              variant="outline"
              size="md"
              rightIcon={<ArrowRight size={14} />}
              style={{ width: "100%" }}
            >
              Start Conversation
            </Button>
          </Link>
        </GlassCard>
      </section>

      {/* CURATED RECOMMENDED DESTINATIONS */}
      <section>
        <SectionHeader
          badge="Handpicked for You"
          title="Curated Travel Escapes"
          subtitle="Handpicked regional and international destinations with optimal travel windows and eco ratings."
          action={
            <Link href="/explore" style={{ textDecoration: "none" }}>
              <Button
                variant="ghost"
                size="sm"
                rightIcon={<ChevronRight size={14} />}
              >
                View All (1,300+)
              </Button>
            </Link>
          }
        />

        {/* REGION FILTER PILLS */}
        <div
          style={{
            display: "flex",
            gap: "8px",
            marginBottom: "18px",
            overflowX: "auto",
            paddingBottom: "4px",
          }}
        >
          {[
            { id: "all", label: "All Destinations" },
            { id: "india", label: "India & Regional" },
            { id: "abroad", label: "International / Abroad" },
          ].map((pill) => {
            const isActive = destFilter === pill.id;
            return (
              <button
                key={pill.id}
                type="button"
                onClick={() => setDestFilter(pill.id as any)}
                style={{
                  padding: "8px 16px",
                  borderRadius: "999px",
                  background: isActive
                    ? "linear-gradient(135deg, #0EA5E9, #14B8A6)"
                    : "rgba(255, 255, 255, 0.05)",
                  border: isActive
                    ? "1px solid rgba(14, 165, 233, 0.5)"
                    : "1px solid rgba(255, 255, 255, 0.08)",
                  color: isActive ? "#FFFFFF" : "#94A3B8",
                  fontSize: "0.85rem",
                  fontWeight: isActive ? 700 : 500,
                  cursor: "pointer",
                  transition: "all 0.2s ease",
                  whiteSpace: "nowrap",
                }}
              >
                {pill.label}
              </button>
            );
          })}
        </div>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
            gap: "20px",
          }}
        >
          {curatedDestinations
            .filter((d) => destFilter === "all" || d.region === destFilter)
            .map((dest) => (
            <div
              key={dest.name}
              className="glass-card-interactive"
              onClick={() =>
                router.push(
                  `/planner?destination=${encodeURIComponent(dest.name)}`,
                )
              }
              style={{
                overflow: "hidden",
                borderRadius: "20px",
                display: "flex",
                flexDirection: "column",
              }}
            >
              <div
                style={{ position: "relative", height: "180px", width: "100%" }}
              >
                <Image
                  src={dest.image}
                  alt={dest.name}
                  fill
                  sizes="300px"
                  style={{ objectFit: "cover" }}
                />
                <div
                  style={{
                    position: "absolute",
                    inset: 0,
                    background:
                      "linear-gradient(to top, rgba(3, 7, 18, 0.85) 0%, transparent 60%)",
                  }}
                />
                <div
                  style={{ position: "absolute", top: "12px", right: "12px" }}
                >
                  <Badge variant="eco" size="sm" icon={<Leaf size={10} />}>
                    {dest.eco}
                  </Badge>
                </div>
                <div
                  style={{
                    position: "absolute",
                    bottom: "14px",
                    left: "16px",
                    right: "16px",
                  }}
                >
                  <h4
                    style={{
                      fontSize: "1.25rem",
                      fontWeight: 800,
                      color: "#FFFFFF",
                    }}
                  >
                    {dest.name}
                  </h4>
                  <p style={{ color: "#CBD5E1", fontSize: "0.82rem" }}>
                    {dest.state} • {dest.days}
                  </p>
                </div>
              </div>
              <div
                style={{
                  padding: "14px 16px",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                  background: "rgba(15, 23, 42, 0.5)",
                }}
              >
                <span
                  style={{
                    fontSize: "0.82rem",
                    color: "#38BDF8",
                    fontWeight: 600,
                  }}
                >
                  Plan this escape
                </span>
                <ArrowRight size={14} color="#38BDF8" />
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* RECENT TRIPS HUB */}
      <section>
        <SectionHeader
          badge="Your Archive"
          title="Recent Itineraries"
          subtitle="Review your generated trips or jump back into planning."
          action={
            <Link href="/trip/history" style={{ textDecoration: "none" }}>
              <Button variant="secondary" size="sm">
                Full History
              </Button>
            </Link>
          }
        />

        {recentTrips.length > 0 ? (
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))",
              gap: "20px",
            }}
          >
            {recentTrips.map((trip, idx) => (
              <GlassCard
                key={trip.id || idx}
                interactive
                onClick={() => router.push("/trip/generated")}
                style={{ padding: "22px" }}
              >
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "flex-start",
                    marginBottom: "12px",
                  }}
                >
                  <div>
                    <h4
                      style={{
                        fontSize: "1.2rem",
                        fontWeight: 800,
                        color: "#FFFFFF",
                      }}
                    >
                      {trip.trip_title || `${trip.destination} Trip`}
                    </h4>
                    <p
                      style={{
                        color: "#94A3B8",
                        fontSize: "0.85rem",
                        display: "flex",
                        alignItems: "center",
                        gap: "4px",
                        marginTop: "4px",
                      }}
                    >
                      <MapPin size={13} color="#38BDF8" /> {trip.destination}
                    </p>
                  </div>
                  {trip.sustainability_score !== undefined && (
                    <Badge variant="eco" size="sm">
                      {trip.sustainability_score}/100
                    </Badge>
                  )}
                </div>

                <div
                  style={{
                    display: "flex",
                    gap: "16px",
                    fontSize: "0.85rem",
                    color: "#CBD5E1",
                    borderTop: "1px solid rgba(255, 255, 255, 0.08)",
                    paddingTop: "14px",
                    marginTop: "14px",
                  }}
                >
                  <span>📅 {trip.duration_days} Days</span>
                  <span>💰 ₹{trip.budget.toLocaleString()}</span>
                </div>
              </GlassCard>
            ))}
          </div>
        ) : (
          <GlassCard style={{ padding: "48px", textAlign: "center" }}>
            <div
              style={{
                width: "54px",
                height: "54px",
                borderRadius: "16px",
                background: "rgba(14, 165, 233, 0.12)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                margin: "0 auto 16px auto",
                color: "#38BDF8",
              }}
            >
              <Plane size={24} />
            </div>
            <h3
              style={{
                fontSize: "1.3rem",
                fontWeight: 700,
                color: "#FFFFFF",
                marginBottom: "8px",
              }}
            >
              No Itineraries Created Yet
            </h3>
            <p
              style={{
                color: "#94A3B8",
                fontSize: "0.95rem",
                maxWidth: "450px",
                margin: "0 auto 24px auto",
              }}
            >
              Use our AI Planner to generate your first custom trip with live
              weather, stays, restaurants, and eco scores.
            </p>
            <Link href="/planner" style={{ textDecoration: "none" }}>
              <Button
                variant="primary"
                size="md"
                leftIcon={<Sparkles size={16} />}
              >
                Create Your First Trip
              </Button>
            </Link>
          </GlassCard>
        )}
      </section>
    </div>
  );
}
