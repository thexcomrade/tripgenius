"use client";

import { useEffect, useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  Sparkles,
  Calendar,
  Users,
  DollarSign,
  Leaf,
  MapPin,
  Bookmark,
  Share2,
  Printer,
  Sun,
  CloudSun,
  Utensils,
  Hotel,
  Check,
  AlertCircle,
  ArrowRight,
  Clock,
  Compass,
  Coffee,
  Luggage,
  Shield,
  Heart,
} from "lucide-react";
import Button from "../../../components/ui/Button";
import Badge from "../../../components/ui/Badge";
import { GlassCard, SectionHeader } from "../../../components/ui/Card";
import tripService from "../../../services/trip.service";

interface DayPlan {
  day: number;
  title: string;
  destination?: string;
  morning?: string;
  afternoon?: string;
  evening?: string;
  activities?: string[];
}

interface WeatherSummary {
  city?: string;
  temperature?: number;
  condition?: string;
  humidity?: number;
  wind_speed?: number;
  travel_recommendation?: string;
  packing_suggestions?: string[];
}

interface TripData {
  destination: string;
  duration_days: number;
  budget: number;
  travelers_count: number;
  travel_style: string;
  transportation_mode: string;
  preferred_accommodation: string;
  interests: string[];
  generated_at?: string;

  trip_title?: string;
  destination_summary?: string;
  weather_summary?: WeatherSummary;
  attractions?: string[];
  activities?: string[];
  recommended_hotels?: string[];
  recommended_restaurants?: string[];
  local_cuisines?: string[];
  beverages_to_try?: string[];
  packing_checklist?: string[];
  travel_tips?: string[];
  ai_itinerary?: DayPlan[];
  sustainability_score?: number;
  carbon_footprint_estimate?: number;
  estimated_trip_cost?: number;
  accommodation_cost?: number;
  food_cost?: number;
  transportation_cost?: number;
  miscellaneous_cost?: number;
  ai_confidence_score?: number;
  eco_friendly_recommendations?: string[];
  generation_mode?: string;
  error?: string;
}

const DESTINATION_IMAGES: Record<string, string> = {
  Munnar: "/destinations/munnar.jpg",
  Varkala: "/destinations/varkala.jpg",
  Ooty: "/destinations/ooty.jpg",
  Kodaikanal: "/destinations/kodaikanal.jpg",
  Mysore: "/destinations/mysore.jpg",
  Coorg: "/destinations/coorg.jpg",
};

export default function GeneratedTripPage() {
  const router = useRouter();

  const [trip, setTrip] = useState<TripData | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<
    "itinerary" | "stays" | "budget" | "weather" | "eco"
  >("itinerary");
  const [saving, setSaving] = useState(false);
  const [saveFeedback, setSaveFeedback] = useState<
    "" | "success" | "duplicate" | "error"
  >("");
  const [checkedItems, setCheckedItems] = useState<Record<string, boolean>>({});

  useEffect(() => {
    try {
      const storedTrip = localStorage.getItem("latest_trip");
      if (storedTrip) {
        setTrip(JSON.parse(storedTrip));
      }
    } catch (error) {
      console.error("Trip loading error:", error);
    } finally {
      setLoading(false);
    }
  }, []);

  const toggleCheckItem = (item: string) => {
    setCheckedItems((prev) => ({
      ...prev,
      [item]: !prev[item],
    }));
  };

  const handleSaveTrip = async () => {
    if (!trip) return;
    setSaving(true);
    setSaveFeedback("");

    try {
      const token = localStorage.getItem("tripgenius_token");
      if (token) {
        await tripService.createTrip({
          trip_title: trip.trip_title || `${trip.destination} AI Itinerary`,
          destination: trip.destination,
          duration_days: trip.duration_days,
          budget: trip.budget,
          travelers_count: trip.travelers_count,
          travel_style: trip.travel_style,
          interests: trip.interests || [],
          transportation_mode: trip.transportation_mode,
          preferred_accommodation: trip.preferred_accommodation,
        });
        setSaveFeedback("success");
      } else {
        // LocalStorage save
        const existing = JSON.parse(
          localStorage.getItem("saved_trips") || "[]",
        );
        const tripId = `${trip.destination}-${trip.generated_at || Date.now()}`;
        const duplicate = existing.some(
          (s: TripData & { generated_at?: string }) =>
            `${s.destination}-${s.generated_at}` === tripId,
        );
        if (duplicate) {
          setSaveFeedback("duplicate");
          setSaving(false);
          return;
        }
        existing.unshift({ ...trip, saved_at: new Date().toISOString() });
        localStorage.setItem("saved_trips", JSON.stringify(existing));
        setSaveFeedback("success");
      }
    } catch (err) {
      console.error(err);
      setSaveFeedback("error");
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div
        className="page-container"
        style={{ textAlign: "center", padding: "100px 20px" }}
      >
        <div
          style={{
            width: "60px",
            height: "60px",
            borderRadius: "50%",
            border: "3px solid rgba(14, 165, 233, 0.2)",
            borderTopColor: "#0EA5E9",
            animation: "spin 0.8s linear infinite",
            margin: "0 auto 20px auto",
          }}
        />
        <h2 style={{ fontSize: "1.5rem", fontWeight: 700, color: "#FFFFFF" }}>
          Loading your generated itinerary...
        </h2>
        <style jsx>{`
          @keyframes spin {
            to {
              transform: rotate(360deg);
            }
          }
        `}</style>
      </div>
    );
  }

  if (!trip) {
    return (
      <div
        className="page-container"
        style={{ maxWidth: "700px", textAlign: "center", padding: "80px 20px" }}
      >
        <GlassCard style={{ padding: "50px 30px" }}>
          <div
            style={{
              width: "60px",
              height: "60px",
              borderRadius: "18px",
              background: "rgba(14, 165, 233, 0.12)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              margin: "0 auto 20px auto",
              color: "#38BDF8",
            }}
          >
            <Compass size={28} />
          </div>
          <h2
            style={{
              fontSize: "1.8rem",
              fontWeight: 800,
              color: "#FFFFFF",
              marginBottom: "12px",
            }}
          >
            No Itinerary Loaded
          </h2>
          <p
            style={{
              color: "#94A3B8",
              fontSize: "1rem",
              lineHeight: 1.6,
              marginBottom: "28px",
            }}
          >
            We couldn&apos;t find an active trip plan in your session. Launch
            the AI Planner to craft a personalized escape.
          </p>
          <Link href="/planner" style={{ textDecoration: "none" }}>
            <Button
              variant="primary"
              size="lg"
              leftIcon={<Sparkles size={18} />}
            >
              Open AI Planner
            </Button>
          </Link>
        </GlassCard>
      </div>
    );
  }

  const imageSrc =
    DESTINATION_IMAGES[trip.destination] || "/destinations/munnar.jpg";
  const isOffline = trip.generation_mode === "offline";

  return (
    <div
      className="page-container"
      style={{ display: "flex", flexDirection: "column", gap: "32px" }}
    >
      {/* OFFLINE NOTICE BANNER */}
      {isOffline && (
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "12px",
            background: "rgba(245, 158, 11, 0.15)",
            border: "1px solid rgba(245, 158, 11, 0.35)",
            color: "#FDE68A",
            padding: "14px 20px",
            borderRadius: "14px",
            fontSize: "0.92rem",
          }}
        >
          <AlertCircle size={20} style={{ flexShrink: 0 }} />
          <span>
            Generated via Offline Algorithmic Fallback. Live Gemini AI was
            temporarily unreachable.
            {trip.error && ` (${trip.error})`}
          </span>
        </div>
      )}

      {/* SAVE FEEDBACK TOASTS */}
      {saveFeedback === "success" && (
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "10px",
            background: "rgba(16, 185, 129, 0.15)",
            border: "1px solid rgba(16, 185, 129, 0.35)",
            color: "#6EE7B7",
            padding: "14px 20px",
            borderRadius: "14px",
          }}
        >
          <Check size={18} />
          <span>
            Trip itinerary saved successfully to your profile archive!
          </span>
        </div>
      )}
      {saveFeedback === "duplicate" && (
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "10px",
            background: "rgba(14, 165, 233, 0.15)",
            border: "1px solid rgba(14, 165, 233, 0.35)",
            color: "#7DD3FC",
            padding: "14px 20px",
            borderRadius: "14px",
          }}
        >
          <AlertCircle size={18} />
          <span>This trip is already in your saved collection.</span>
        </div>
      )}
      {saveFeedback === "error" && (
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "10px",
            background: "rgba(239, 68, 68, 0.15)",
            border: "1px solid rgba(239, 68, 68, 0.35)",
            color: "#FCA5A5",
            padding: "14px 20px",
            borderRadius: "14px",
          }}
        >
          <AlertCircle size={18} />
          <span>Unable to save trip right now. Please try again.</span>
        </div>
      )}

      {/* CINEMATIC HERO SECTION */}
      <section
        style={{
          position: "relative",
          borderRadius: "28px",
          overflow: "hidden",
          border: "1px solid rgba(255, 255, 255, 0.10)",
          boxShadow: "0 20px 60px rgba(0, 0, 0, 0.50)",
        }}
      >
        <div style={{ position: "relative", height: "420px", width: "100%" }}>
          <Image
            src={imageSrc}
            alt={trip.destination}
            fill
            priority
            style={{ objectFit: "cover" }}
          />
          <div
            style={{
              position: "absolute",
              inset: 0,
              background:
                "linear-gradient(to top, rgba(3, 7, 18, 0.95) 0%, rgba(3, 7, 18, 0.50) 50%, rgba(3, 7, 18, 0.20) 100%)",
            }}
          />

          {/* FLOATING TOP BADGES */}
          <div
            style={{
              position: "absolute",
              top: "24px",
              left: "24px",
              display: "flex",
              gap: "10px",
              flexWrap: "wrap",
            }}
          >
            <Badge variant="ai" size="md" icon={<Sparkles size={14} />}>
              {trip.ai_confidence_score
                ? `${trip.ai_confidence_score}% AI Confidence`
                : "Synthesized Itinerary"}
            </Badge>
            {trip.sustainability_score !== undefined && (
              <Badge variant="eco" size="md" icon={<Leaf size={14} />}>
                {trip.sustainability_score}/100 Eco Score
              </Badge>
            )}
          </div>

          {/* HERO ACTIONS */}
          <div
            style={{
              position: "absolute",
              top: "24px",
              right: "24px",
              display: "flex",
              gap: "10px",
            }}
          >
            <button
              type="button"
              onClick={() => window.print()}
              title="Print / Save PDF"
              style={{
                width: "42px",
                height: "42px",
                borderRadius: "12px",
                background: "rgba(0, 0, 0, 0.60)",
                backdropFilter: "blur(12px)",
                border: "1px solid rgba(255, 255, 255, 0.20)",
                color: "#FFFFFF",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                cursor: "pointer",
              }}
            >
              <Printer size={18} />
            </button>
            <Button
              variant="primary"
              size="md"
              isLoading={saving}
              leftIcon={<Bookmark size={16} />}
              onClick={handleSaveTrip}
            >
              Save Itinerary
            </Button>
          </div>

          {/* BOTTOM HERO CONTENT */}
          <div
            style={{
              position: "absolute",
              bottom: "30px",
              left: "32px",
              right: "32px",
            }}
          >
            <h1
              style={{
                fontSize: "clamp(2.2rem, 5vw, 3.6rem)",
                fontWeight: 900,
                color: "#FFFFFF",
                letterSpacing: "-1px",
                marginBottom: "8px",
              }}
            >
              {trip.trip_title || `${trip.destination} Custom Expedition`}
            </h1>
            <p
              style={{
                color: "#CBD5E1",
                fontSize: "1.05rem",
                maxWidth: "800px",
                lineHeight: 1.6,
                marginBottom: "20px",
              }}
            >
              {trip.destination_summary ||
                `A bespoke ${trip.duration_days}-day itinerary crafted for ${trip.travelers_count} travelers, optimizing scenic landscapes, heritage spots, and regional tastes.`}
            </p>

            <div
              style={{
                display: "flex",
                flexWrap: "wrap",
                gap: "20px",
                color: "#E2E8F0",
                fontSize: "0.95rem",
              }}
            >
              <span
                style={{ display: "flex", alignItems: "center", gap: "6px" }}
              >
                <Calendar size={16} color="#38BDF8" />{" "}
                <strong>{trip.duration_days} Days</strong>
              </span>
              <span
                style={{ display: "flex", alignItems: "center", gap: "6px" }}
              >
                <Users size={16} color="#38BDF8" />{" "}
                <strong>{trip.travelers_count} Travelers</strong>
              </span>
              <span
                style={{ display: "flex", alignItems: "center", gap: "6px" }}
              >
                <DollarSign size={16} color="#34D399" />{" "}
                <strong>
                  ₹{(trip.estimated_trip_cost ?? trip.budget).toLocaleString()}{" "}
                  Est. Budget
                </strong>
              </span>
              <span
                style={{ display: "flex", alignItems: "center", gap: "6px" }}
              >
                <Compass size={16} color="#FBBF24" />{" "}
                <strong>{trip.travel_style} Pacing</strong>
              </span>
              {trip.carbon_footprint_estimate !== undefined && (
                <span
                  style={{ display: "flex", alignItems: "center", gap: "6px" }}
                >
                  <Leaf size={16} color="#34D399" />{" "}
                  <strong>{trip.carbon_footprint_estimate} kg CO₂</strong>
                </span>
              )}
            </div>
          </div>
        </div>
      </section>

      {/* TABBED NAVIGATION BAR */}
      <div
        style={{
          display: "flex",
          gap: "8px",
          borderBottom: "1px solid rgba(255, 255, 255, 0.08)",
          paddingBottom: "12px",
          overflowX: "auto",
          whiteSpace: "nowrap",
        }}
      >
        {[
          { id: "itinerary", label: "Day-by-Day Timeline", icon: Calendar },
          { id: "stays", label: "Stays & Food", icon: Hotel },
          { id: "budget", label: "Cost Breakdown", icon: DollarSign },
          { id: "weather", label: "Weather & Packing", icon: Sun },
          { id: "eco", label: "Eco & Sustainability", icon: Leaf },
        ].map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              type="button"
              onClick={() => setActiveTab(tab.id as any)}
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: "8px",
                padding: "10px 18px",
                borderRadius: "12px",
                background: isActive
                  ? "rgba(14, 165, 233, 0.15)"
                  : "transparent",
                border: isActive
                  ? "1px solid rgba(14, 165, 233, 0.35)"
                  : "1px solid transparent",
                color: isActive ? "#38BDF8" : "#94A3B8",
                fontSize: "0.92rem",
                fontWeight: isActive ? 700 : 500,
                cursor: "pointer",
                transition: "all 0.2s ease",
              }}
            >
              <Icon size={16} />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* TAB 1: DAY-BY-DAY ITINERARY */}
      {activeTab === "itinerary" && (
        <div style={{ display: "flex", flexDirection: "column", gap: "24px" }}>
          <SectionHeader
            badge="Sequential Timeline"
            title="Your Daily Journey"
            subtitle="Optimized schedule factoring travel transit, attraction visiting hours, and peak scenery windows."
          />

          {trip.ai_itinerary && trip.ai_itinerary.length > 0 ? (
            <div
              style={{ display: "flex", flexDirection: "column", gap: "20px" }}
            >
              {trip.ai_itinerary.map((day) => (
                <GlassCard key={day.day} style={{ padding: "28px" }}>
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: "12px",
                      marginBottom: "20px",
                    }}
                  >
                    <div
                      style={{
                        padding: "6px 14px",
                        borderRadius: "10px",
                        background: "linear-gradient(135deg, #0EA5E9, #14B8A6)",
                        color: "#FFFFFF",
                        fontWeight: 800,
                        fontSize: "0.95rem",
                      }}
                    >
                      Day {day.day}
                    </div>
                    <h3
                      style={{
                        fontSize: "1.3rem",
                        fontWeight: 800,
                        color: "#FFFFFF",
                      }}
                    >
                      {day.title}
                    </h3>
                  </div>

                  <div
                    style={{
                      display: "grid",
                      gridTemplateColumns:
                        "repeat(auto-fit, minmax(280px, 1fr))",
                      gap: "16px",
                    }}
                  >
                    {day.morning && (
                      <div
                        style={{
                          background: "rgba(255, 255, 255, 0.03)",
                          padding: "18px",
                          borderRadius: "14px",
                          border: "1px solid rgba(255, 255, 255, 0.06)",
                        }}
                      >
                        <div
                          style={{
                            display: "flex",
                            alignItems: "center",
                            gap: "8px",
                            color: "#FBBF24",
                            fontWeight: 700,
                            fontSize: "0.9rem",
                            marginBottom: "8px",
                          }}
                        >
                          <Sun size={16} /> Morning
                        </div>
                        <p
                          style={{
                            color: "#CBD5E1",
                            fontSize: "0.9rem",
                            lineHeight: 1.6,
                          }}
                        >
                          {day.morning}
                        </p>
                      </div>
                    )}

                    {day.afternoon && (
                      <div
                        style={{
                          background: "rgba(255, 255, 255, 0.03)",
                          padding: "18px",
                          borderRadius: "14px",
                          border: "1px solid rgba(255, 255, 255, 0.06)",
                        }}
                      >
                        <div
                          style={{
                            display: "flex",
                            alignItems: "center",
                            gap: "8px",
                            color: "#38BDF8",
                            fontWeight: 700,
                            fontSize: "0.9rem",
                            marginBottom: "8px",
                          }}
                        >
                          <CloudSun size={16} /> Afternoon
                        </div>
                        <p
                          style={{
                            color: "#CBD5E1",
                            fontSize: "0.9rem",
                            lineHeight: 1.6,
                          }}
                        >
                          {day.afternoon}
                        </p>
                      </div>
                    )}

                    {day.evening && (
                      <div
                        style={{
                          background: "rgba(255, 255, 255, 0.03)",
                          padding: "18px",
                          borderRadius: "14px",
                          border: "1px solid rgba(255, 255, 255, 0.06)",
                        }}
                      >
                        <div
                          style={{
                            display: "flex",
                            alignItems: "center",
                            gap: "8px",
                            color: "#C084FC",
                            fontWeight: 700,
                            fontSize: "0.9rem",
                            marginBottom: "8px",
                          }}
                        >
                          <Coffee size={16} /> Evening & Sunset
                        </div>
                        <p
                          style={{
                            color: "#CBD5E1",
                            fontSize: "0.9rem",
                            lineHeight: 1.6,
                          }}
                        >
                          {day.evening}
                        </p>
                      </div>
                    )}
                  </div>

                  {day.activities && day.activities.length > 0 && (
                    <div
                      style={{
                        marginTop: "18px",
                        display: "flex",
                        alignItems: "center",
                        gap: "8px",
                        flexWrap: "wrap",
                      }}
                    >
                      <span
                        style={{
                          fontSize: "0.82rem",
                          color: "#94A3B8",
                          fontWeight: 600,
                        }}
                      >
                        Key Stops:
                      </span>
                      {day.activities.map((act, i) => (
                        <Badge key={i} variant="neutral" size="sm">
                          {act}
                        </Badge>
                      ))}
                    </div>
                  )}
                </GlassCard>
              ))}
            </div>
          ) : (
            /* Fallback days */
            <div
              style={{ display: "flex", flexDirection: "column", gap: "16px" }}
            >
              {Array.from({ length: trip.duration_days }).map((_, idx) => (
                <GlassCard key={idx} style={{ padding: "24px" }}>
                  <h4
                    style={{
                      fontSize: "1.2rem",
                      fontWeight: 800,
                      color: "#38BDF8",
                      marginBottom: "8px",
                    }}
                  >
                    Day {idx + 1} • Explore {trip.destination}
                  </h4>
                  <p style={{ color: "#CBD5E1", lineHeight: 1.7 }}>
                    Discover curated viewpoints, local tea plantations,
                    authentic dining spots, and cultural heritage across{" "}
                    {trip.destination}.
                  </p>
                </GlassCard>
              ))}
            </div>
          )}

          {/* ATTRACTIONS CHIPS */}
          {trip.attractions && trip.attractions.length > 0 && (
            <GlassCard style={{ padding: "26px", marginTop: "12px" }}>
              <h3
                style={{
                  fontSize: "1.15rem",
                  fontWeight: 700,
                  color: "#FFFFFF",
                  marginBottom: "14px",
                }}
              >
                🏛️ Featured Attractions in {trip.destination}
              </h3>
              <div style={{ display: "flex", flexWrap: "wrap", gap: "10px" }}>
                {trip.attractions.map((attraction, i) => (
                  <Badge key={i} variant="ai" size="md">
                    {attraction}
                  </Badge>
                ))}
              </div>
            </GlassCard>
          )}
        </div>
      )}

      {/* TAB 2: STAYS & FOOD */}
      {activeTab === "stays" && (
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(340px, 1fr))",
            gap: "24px",
          }}
        >
          {/* RECOMMENDED HOTELS */}
          <GlassCard style={{ padding: "28px" }}>
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "10px",
                marginBottom: "20px",
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
                  color: "#38BDF8",
                }}
              >
                <Hotel size={20} />
              </div>
              <h3
                style={{
                  fontSize: "1.25rem",
                  fontWeight: 800,
                  color: "#FFFFFF",
                }}
              >
                Recommended Accommodations
              </h3>
            </div>

            {trip.recommended_hotels && trip.recommended_hotels.length > 0 ? (
              <div
                style={{
                  display: "flex",
                  flexDirection: "column",
                  gap: "14px",
                }}
              >
                {trip.recommended_hotels.map((hotel, idx) => (
                  <div
                    key={idx}
                    style={{
                      padding: "16px",
                      borderRadius: "14px",
                      background: "rgba(255, 255, 255, 0.04)",
                      border: "1px solid rgba(255, 255, 255, 0.08)",
                    }}
                  >
                    <h4
                      style={{
                        color: "#F8FAFC",
                        fontSize: "1rem",
                        fontWeight: 700,
                      }}
                    >
                      {hotel}
                    </h4>
                    <p
                      style={{
                        color: "#94A3B8",
                        fontSize: "0.82rem",
                        marginTop: "4px",
                      }}
                    >
                      Matched to style: {trip.preferred_accommodation}
                    </p>
                  </div>
                ))}
              </div>
            ) : (
              <p style={{ color: "#94A3B8" }}>
                Recommended stays matching your budget and style are being
                gathered.
              </p>
            )}
          </GlassCard>

          {/* RESTAURANTS & CUISINES */}
          <GlassCard style={{ padding: "28px" }}>
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "10px",
                marginBottom: "20px",
              }}
            >
              <div
                style={{
                  width: "36px",
                  height: "36px",
                  borderRadius: "10px",
                  background: "rgba(245, 158, 11, 0.15)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  color: "#FBBF24",
                }}
              >
                <Utensils size={20} />
              </div>
              <h3
                style={{
                  fontSize: "1.25rem",
                  fontWeight: 800,
                  color: "#FFFFFF",
                }}
              >
                Regional Dining & Eateries
              </h3>
            </div>

            {trip.recommended_restaurants &&
            trip.recommended_restaurants.length > 0 ? (
              <div
                style={{
                  display: "flex",
                  flexDirection: "column",
                  gap: "14px",
                  marginBottom: "24px",
                }}
              >
                {trip.recommended_restaurants.map((rest, idx) => (
                  <div
                    key={idx}
                    style={{
                      padding: "16px",
                      borderRadius: "14px",
                      background: "rgba(255, 255, 255, 0.04)",
                      border: "1px solid rgba(255, 255, 255, 0.08)",
                    }}
                  >
                    <h4
                      style={{
                        color: "#F8FAFC",
                        fontSize: "1rem",
                        fontWeight: 700,
                      }}
                    >
                      {rest}
                    </h4>
                    <p
                      style={{
                        color: "#94A3B8",
                        fontSize: "0.82rem",
                        marginTop: "4px",
                      }}
                    >
                      Local flavors & verified cleanliness
                    </p>
                  </div>
                ))}
              </div>
            ) : null}

            {trip.local_cuisines && trip.local_cuisines.length > 0 && (
              <div>
                <h4
                  style={{
                    fontSize: "0.95rem",
                    fontWeight: 700,
                    color: "#E2E8F0",
                    marginBottom: "10px",
                  }}
                >
                  Must-Try Delicacies:
                </h4>
                <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
                  {trip.local_cuisines.map((c, idx) => (
                    <Badge key={idx} variant="amber" size="sm">
                      {c}
                    </Badge>
                  ))}
                </div>
              </div>
            )}
          </GlassCard>
        </div>
      )}

      {/* TAB 3: BUDGET BREAKDOWN */}
      {activeTab === "budget" && (
        <GlassCard style={{ padding: "32px" }}>
          <SectionHeader
            badge="Financial Modeling"
            title="Estimated Trip Expense Breakdown"
            subtitle="Estimated costs for 100% of travelers across accommodations, dining, transit, and activities."
          />

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
              gap: "20px",
              marginBottom: "36px",
            }}
          >
            <div
              style={{
                padding: "20px",
                borderRadius: "16px",
                background: "rgba(255, 255, 255, 0.04)",
                border: "1px solid rgba(255, 255, 255, 0.08)",
              }}
            >
              <span style={{ fontSize: "0.85rem", color: "#94A3B8" }}>
                🏨 Accommodations
              </span>
              <h3
                style={{
                  fontSize: "1.8rem",
                  fontWeight: 800,
                  color: "#38BDF8",
                  marginTop: "6px",
                }}
              >
                ₹
                {(
                  trip.accommodation_cost ?? Math.round(trip.budget * 0.4)
                ).toLocaleString()}
              </h3>
              <p style={{ fontSize: "0.78rem", color: "#64748B", marginTop: "4px" }}>
                ~₹{Math.round((trip.accommodation_cost ?? (trip.budget * 0.4)) / Math.max(1, trip.duration_days - 1)).toLocaleString("en-IN")}/night ({Math.max(1, trip.duration_days - 1)} night{trip.duration_days - 1 > 1 ? "s" : ""})
              </p>
            </div>

            <div
              style={{
                padding: "20px",
                borderRadius: "16px",
                background: "rgba(255, 255, 255, 0.04)",
                border: "1px solid rgba(255, 255, 255, 0.08)",
              }}
            >
              <span style={{ fontSize: "0.85rem", color: "#94A3B8" }}>
                🍽️ Food & Dining
              </span>
              <h3
                style={{
                  fontSize: "1.8rem",
                  fontWeight: 800,
                  color: "#FBBF24",
                  marginTop: "6px",
                }}
              >
                ₹
                {(
                  trip.food_cost ?? Math.round(trip.budget * 0.25)
                ).toLocaleString()}
              </h3>
              <p style={{ fontSize: "0.78rem", color: "#64748B", marginTop: "4px" }}>
                ~₹{Math.round((trip.food_cost ?? (trip.budget * 0.25)) / Math.max(1, trip.duration_days)).toLocaleString("en-IN")}/day ({trip.travelers_count} traveler{trip.travelers_count > 1 ? "s" : ""})
              </p>
            </div>

            <div
              style={{
                padding: "20px",
                borderRadius: "16px",
                background: "rgba(255, 255, 255, 0.04)",
                border: "1px solid rgba(255, 255, 255, 0.08)",
              }}
            >
              <span style={{ fontSize: "0.85rem", color: "#94A3B8" }}>
                🚗 Transit & Mobility
              </span>
              <h3
                style={{
                  fontSize: "1.8rem",
                  fontWeight: 800,
                  color: "#34D399",
                  marginTop: "6px",
                }}
              >
                ₹
                {(
                  trip.transportation_cost ?? Math.round(trip.budget * 0.2)
                ).toLocaleString()}
              </h3>
              <p style={{ fontSize: "0.78rem", color: "#64748B", marginTop: "4px" }}>
                Sightseeing transit, fuel, & local cab fares
              </p>
            </div>

            <div
              style={{
                padding: "20px",
                borderRadius: "16px",
                background: "rgba(255, 255, 255, 0.04)",
                border: "1px solid rgba(255, 255, 255, 0.08)",
              }}
            >
              <span style={{ fontSize: "0.85rem", color: "#94A3B8" }}>
                🎫 Activities & Misc
              </span>
              <h3
                style={{
                  fontSize: "1.8rem",
                  fontWeight: 800,
                  color: "#C084FC",
                  marginTop: "6px",
                }}
              >
                ₹
                {(
                  trip.miscellaneous_cost ?? Math.round(trip.budget * 0.15)
                ).toLocaleString()}
              </h3>
              <p style={{ fontSize: "0.78rem", color: "#64748B", marginTop: "4px" }}>
                Attraction passes, permits, & emergency contingency
              </p>
            </div>
          </div>

          <div
            style={{
              padding: "20px",
              borderRadius: "16px",
              background: "rgba(14, 165, 233, 0.08)",
              border: "1px solid rgba(14, 165, 233, 0.20)",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              flexWrap: "wrap",
              gap: "16px",
            }}
          >
            <div>
              <h4
                style={{
                  color: "#FFFFFF",
                  fontSize: "1.1rem",
                  fontWeight: 700,
                }}
              >
                Total Allocated Budget: ₹{(trip.estimated_trip_cost ?? trip.budget).toLocaleString("en-IN")}
              </h4>
              <p style={{ color: "#94A3B8", fontSize: "0.85rem", marginTop: "2px" }}>
                Paced at ~₹{Math.round((trip.estimated_trip_cost ?? trip.budget) / Math.max(1, trip.duration_days)).toLocaleString("en-IN")}/day (~₹{Math.round((trip.estimated_trip_cost ?? trip.budget) / Math.max(1, trip.duration_days * trip.travelers_count)).toLocaleString("en-IN")}/person/day)
              </p>
            </div>
            <span
              style={{ fontSize: "2rem", fontWeight: 900, color: "#38BDF8" }}
            >
              ₹{(trip.estimated_trip_cost ?? trip.budget).toLocaleString()}
            </span>
          </div>
        </GlassCard>
      )}

      {/* TAB 4: WEATHER & PACKING */}
      {activeTab === "weather" && (
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(340px, 1fr))",
            gap: "24px",
          }}
        >
          <GlassCard style={{ padding: "28px" }}>
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "10px",
                marginBottom: "18px",
              }}
            >
              <CloudSun size={24} color="#FBBF24" />
              <h3
                style={{
                  fontSize: "1.25rem",
                  fontWeight: 800,
                  color: "#FFFFFF",
                }}
              >
                Live Climate Snapshot
              </h3>
            </div>

            {trip.weather_summary ? (
              <div>
                <div
                  style={{
                    display: "flex",
                    alignItems: "baseline",
                    gap: "12px",
                    marginBottom: "16px",
                  }}
                >
                  <span
                    style={{
                      fontSize: "3rem",
                      fontWeight: 900,
                      color: "#FFFFFF",
                    }}
                  >
                    {trip.weather_summary.temperature ?? 21}°C
                  </span>
                  <span
                    style={{
                      color: "#38BDF8",
                      fontWeight: 600,
                      fontSize: "1.1rem",
                    }}
                  >
                    {trip.weather_summary.condition || "Partly Cloudy"}
                  </span>
                </div>
                <div
                  style={{
                    display: "flex",
                    gap: "20px",
                    color: "#94A3B8",
                    fontSize: "0.9rem",
                    marginBottom: "20px",
                  }}
                >
                  <span>
                    Humidity:{" "}
                    <strong>{trip.weather_summary.humidity ?? 65}%</strong>
                  </span>
                  <span>
                    Wind:{" "}
                    <strong>
                      {trip.weather_summary.wind_speed ?? 10} km/h
                    </strong>
                  </span>
                </div>
                {trip.weather_summary.travel_recommendation && (
                  <p
                    style={{
                      color: "#CBD5E1",
                      fontSize: "0.92rem",
                      lineHeight: 1.6,
                      background: "rgba(255, 255, 255, 0.04)",
                      padding: "14px",
                      borderRadius: "12px",
                    }}
                  >
                    💡 {trip.weather_summary.travel_recommendation}
                  </p>
                )}
              </div>
            ) : (
              <p style={{ color: "#94A3B8" }}>
                Weather data preview unavailable for this location.
              </p>
            )}
          </GlassCard>

          {/* INTERACTIVE PACKING CHECKLIST */}
          <GlassCard style={{ padding: "28px" }}>
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "10px",
                marginBottom: "18px",
              }}
            >
              <Luggage size={24} color="#38BDF8" />
              <h3
                style={{
                  fontSize: "1.25rem",
                  fontWeight: 800,
                  color: "#FFFFFF",
                }}
              >
                Packing Checklist
              </h3>
            </div>

            {trip.packing_checklist && trip.packing_checklist.length > 0 ? (
              <div
                style={{
                  display: "flex",
                  flexDirection: "column",
                  gap: "10px",
                }}
              >
                {trip.packing_checklist.map((item, idx) => {
                  const isChecked = !!checkedItems[item];
                  return (
                    <div
                      key={idx}
                      onClick={() => toggleCheckItem(item)}
                      style={{
                        display: "flex",
                        alignItems: "center",
                        gap: "12px",
                        padding: "10px 14px",
                        borderRadius: "10px",
                        background: isChecked
                          ? "rgba(16, 185, 129, 0.12)"
                          : "rgba(255, 255, 255, 0.04)",
                        border: isChecked
                          ? "1px solid rgba(16, 185, 129, 0.30)"
                          : "1px solid rgba(255, 255, 255, 0.08)",
                        cursor: "pointer",
                        transition: "all 0.2s ease",
                      }}
                    >
                      <div
                        style={{
                          width: "20px",
                          height: "20px",
                          borderRadius: "6px",
                          background: isChecked ? "#10B981" : "transparent",
                          border: isChecked
                            ? "none"
                            : "2px solid rgba(255, 255, 255, 0.2)",
                          display: "flex",
                          alignItems: "center",
                          justifyContent: "center",
                          color: "#FFFFFF",
                        }}
                      >
                        {isChecked && <Check size={14} />}
                      </div>
                      <span
                        style={{
                          color: isChecked ? "#94A3B8" : "#E2E8F0",
                          textDecoration: isChecked ? "line-through" : "none",
                          fontSize: "0.9rem",
                        }}
                      >
                        {item}
                      </span>
                    </div>
                  );
                })}
              </div>
            ) : (
              <p style={{ color: "#94A3B8" }}>
                Carry light cottons, walking shoes, sunscreen, and raincoat.
              </p>
            )}
          </GlassCard>
        </div>
      )}

      {/* TAB 5: ECO & SUSTAINABILITY */}
      {activeTab === "eco" && (
        <GlassCard style={{ padding: "32px" }}>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "10px",
              marginBottom: "20px",
            }}
          >
            <Leaf size={24} color="#34D399" />
            <h3
              style={{ fontSize: "1.4rem", fontWeight: 800, color: "#FFFFFF" }}
            >
              Sustainability & Footprint Analysis
            </h3>
          </div>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))",
              gap: "20px",
              marginBottom: "30px",
            }}
          >
            <div
              style={{
                padding: "20px",
                borderRadius: "16px",
                background: "rgba(16, 185, 129, 0.10)",
                border: "1px solid rgba(16, 185, 129, 0.25)",
              }}
            >
              <span style={{ fontSize: "0.85rem", color: "#6EE7B7" }}>
                Eco Travel Score
              </span>
              <h2
                style={{
                  fontSize: "2.5rem",
                  fontWeight: 900,
                  color: "#34D399",
                  marginTop: "6px",
                }}
              >
                {trip.sustainability_score ?? 84}/100
              </h2>
              <p
                style={{
                  color: "#94A3B8",
                  fontSize: "0.82rem",
                  marginTop: "4px",
                }}
              >
                High environmental efficiency
              </p>
            </div>

            <div
              style={{
                padding: "20px",
                borderRadius: "16px",
                background: "rgba(255, 255, 255, 0.04)",
                border: "1px solid rgba(255, 255, 255, 0.08)",
              }}
            >
              <span style={{ fontSize: "0.85rem", color: "#94A3B8" }}>
                Est. Carbon Emissions
              </span>
              <h2
                style={{
                  fontSize: "2.5rem",
                  fontWeight: 900,
                  color: "#FFFFFF",
                  marginTop: "6px",
                }}
              >
                {trip.carbon_footprint_estimate ?? 110}{" "}
                <span style={{ fontSize: "1.2rem", fontWeight: 600 }}>
                  kg CO₂
                </span>
              </h2>
              <p
                style={{
                  color: "#94A3B8",
                  fontSize: "0.82rem",
                  marginTop: "4px",
                }}
              >
                Calculated for {trip.transportation_mode} transit
              </p>
            </div>
          </div>

          {trip.eco_friendly_recommendations &&
            trip.eco_friendly_recommendations.length > 0 && (
              <div>
                <h4
                  style={{
                    fontSize: "1.1rem",
                    fontWeight: 700,
                    color: "#FFFFFF",
                    marginBottom: "14px",
                  }}
                >
                  🌱 Actionable Green Recommendations:
                </h4>
                <div
                  style={{
                    display: "flex",
                    flexDirection: "column",
                    gap: "10px",
                  }}
                >
                  {trip.eco_friendly_recommendations.map((tip, i) => (
                    <div
                      key={i}
                      style={{
                        display: "flex",
                        alignItems: "flex-start",
                        gap: "10px",
                        padding: "12px",
                        borderRadius: "10px",
                        background: "rgba(255, 255, 255, 0.03)",
                      }}
                    >
                      <Check
                        size={16}
                        color="#34D399"
                        style={{ marginTop: "3px", flexShrink: 0 }}
                      />
                      <span
                        style={{
                          color: "#CBD5E1",
                          fontSize: "0.92rem",
                          lineHeight: 1.6,
                        }}
                      >
                        {tip}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
        </GlassCard>
      )}

      {/* BOTTOM QUICK ACTIONS */}
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          gap: "14px",
          flexWrap: "wrap",
          marginTop: "10px",
        }}
      >
        <Button
          variant="primary"
          size="md"
          leftIcon={<Bookmark size={16} />}
          isLoading={saving}
          onClick={handleSaveTrip}
        >
          Save Itinerary
        </Button>
        <Link href="/planner" style={{ textDecoration: "none" }}>
          <Button
            variant="secondary"
            size="md"
            leftIcon={<Sparkles size={16} />}
          >
            Generate Another Trip
          </Button>
        </Link>
        <Link href="/dashboard" style={{ textDecoration: "none" }}>
          <Button variant="ghost" size="md">
            Dashboard
          </Button>
        </Link>
      </div>
    </div>
  );
}
