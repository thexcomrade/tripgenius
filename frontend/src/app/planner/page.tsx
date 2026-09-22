"use client";

import { FormEvent, useEffect, useState, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import {
  Sparkles,
  MapPin,
  Calendar,
  Users,
  DollarSign,
  Compass,
  Car,
  Hotel,
  Heart,
  ArrowRight,
  ArrowLeft,
  Check,
  AlertCircle,
  Leaf,
  Shield,
  Loader2,
} from "lucide-react";
import Button from "../../components/ui/Button";
import Badge from "../../components/ui/Badge";
import { GlassCard, SectionHeader } from "../../components/ui/Card";
import tripService from "../../services/trip.service";

const POPULAR_DESTINATIONS = [
  "Munnar",
  "Coorg",
  "Ooty",
  "Varkala",
  "Wayanad",
  "Kodaikanal",
  "Mysore",
  "Alleppey",
  "Goa",
];

const TRAVEL_STYLES = [
  {
    id: "Leisure",
    label: "Leisure & Relax",
    desc: "Laid-back sightseeing & scenic views",
    icon: "🌴",
  },
  {
    id: "Adventure",
    label: "Adventure & Trek",
    desc: "Highlands, hikes & thrilling activities",
    icon: "🧗‍♂️",
  },
  {
    id: "Eco-Friendly",
    label: "Eco & Nature",
    desc: "Green trails, flora, fauna & low impact",
    icon: "🌱",
  },
  {
    id: "Cultural",
    label: "Heritage & Culture",
    desc: "Historic temples, royal sites & local arts",
    icon: "🏛️",
  },
  {
    id: "Romantic",
    label: "Romantic Getaway",
    desc: "Intimate views, cozy stays & sunsets",
    icon: "✨",
  },
  {
    id: "Family",
    label: "Family Vacation",
    desc: "Comfortable pacing & all-ages attractions",
    icon: "👨‍👩‍👧‍👦",
  },
];

const TRANSPORT_MODES = [
  {
    id: "Car",
    label: "Private Car / Taxi",
    desc: "Maximum flexibility on scenic roads",
    icon: "🚗",
  },
  {
    id: "Train",
    label: "Scenic Train",
    desc: "Eco-conscious & scenic regional transit",
    icon: "🚆",
  },
  {
    id: "Bus",
    label: "Express Bus",
    desc: "Budget-friendly intercity transit",
    icon: "🚌",
  },
  {
    id: "Flight",
    label: "Flight + Transit",
    desc: "Fast travel for long distances",
    icon: "✈️",
  },
  {
    id: "Cycling",
    label: "Bicycle / Walking",
    desc: "Zero carbon footprint slow travel",
    icon: "🚲",
  },
];

const ACCOMMODATIONS = [
  {
    id: "Hotel",
    label: "Comfort Hotel",
    desc: "Modern amenities & central access",
  },
  {
    id: "Resort",
    label: "Boutique Resort",
    desc: "Scenic vistas & premium relaxation",
  },
  {
    id: "Homestay",
    label: "Authentic Homestay",
    desc: "Warm hospitality & regional cooking",
  },
  {
    id: "Eco-Lodge",
    label: "Eco Lodge / Farmstay",
    desc: "Solar powered & tranquil nature immersion",
  },
  {
    id: "Hostel",
    label: "Backpacker Hostel",
    desc: "Budget friendly & social backpacker hubs",
  },
];

const INTEREST_TAGS = [
  "Tea Gardens",
  "Waterfalls",
  "Mountain Treks",
  "Wildlife Safaris",
  "Beaches & Sunsets",
  "Local Food Tasting",
  "Historic Forts",
  "Ayurvedic Spas",
  "Birdwatching",
  "Photography Spots",
  "Handicrafts & Markets",
  "Boating & Lakes",
];

const AI_GENERATION_STEPS = [
  "Connecting to TripGenius Neural Synthesizer...",
  "Querying live OpenWeather microclimate data...",
  "Scanning 700+ regional tourism points of interest...",
  "Calibrating morning, afternoon & evening schedule...",
  "Computing eco-score & carbon footprint matrix...",
  "Curating authentic regional cuisines & stays...",
];

function PlannerContent() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const [currentStep, setCurrentStep] = useState(1);
  const [destination, setDestination] = useState("");
  const [durationDays, setDurationDays] = useState(3);
  const [budget, setBudget] = useState(15000);
  const [travelersCount, setTravelersCount] = useState(2);
  const [travelStyle, setTravelStyle] = useState("Leisure");
  const [transportationMode, setTransportationMode] = useState("Car");
  const [preferredAccommodation, setPreferredAccommodation] = useState("Hotel");
  const [selectedInterests, setSelectedInterests] = useState<string[]>([
    "Tea Gardens",
    "Local Food Tasting",
  ]);

  const [loading, setLoading] = useState(false);
  const [aiProcessingStage, setAiProcessingStage] = useState(0);
  const [error, setError] = useState("");

  // Auth guard & destination param pre-fill
  useEffect(() => {
    const token = localStorage.getItem("tripgenius_token");
    if (!token) {
      router.push("/login");
    }

    const paramDest = searchParams?.get("destination");
    if (paramDest) {
      setDestination(paramDest);
    }
  }, [router, searchParams]);

  const toggleInterest = (interest: string) => {
    if (selectedInterests.includes(interest)) {
      setSelectedInterests(selectedInterests.filter((i) => i !== interest));
    } else {
      setSelectedInterests([...selectedInterests, interest]);
    }
  };

  const handleGenerateTrip = async (e?: FormEvent) => {
    if (e) e.preventDefault();
    setError("");

    if (!destination.trim()) {
      setCurrentStep(1);
      setError("Please enter a destination to begin.");
      return;
    }

    setLoading(true);
    setAiProcessingStage(0);

    // Advance AI processing stages sequentially for delightful UX
    const interval = setInterval(() => {
      setAiProcessingStage((prev) => {
        if (prev < AI_GENERATION_STEPS.length - 1) {
          return prev + 1;
        }
        return prev;
      });
    }, 800);

    try {
      const response = await tripService.generateAIItinerary({
        destination: destination.trim(),
        duration_days: durationDays,
        budget: budget,
        travelers_count: travelersCount,
        travel_style: travelStyle,
        transportation_mode: transportationMode,
        preferred_accommodation: preferredAccommodation,
        interests: selectedInterests,
      });

      clearInterval(interval);
      setAiProcessingStage(AI_GENERATION_STEPS.length - 1);

      // Store authoritative response merged with trip planning parameters
      const fullTripData = {
        destination: destination.trim(),
        duration_days: durationDays,
        budget: budget,
        travelers_count: travelersCount,
        travel_style: travelStyle,
        transportation_mode: transportationMode,
        preferred_accommodation: preferredAccommodation,
        interests: selectedInterests,
        generated_at: new Date().toISOString(),
        ...response,
      };
      localStorage.setItem("latest_trip", JSON.stringify(fullTripData));

      setTimeout(() => {
        router.push("/trip/generated");
      }, 600);
    } catch (err) {
      clearInterval(interval);
      const message =
        err instanceof Error
          ? err.message
          : "Unable to generate trip. Please try again.";
      setError(message);
      setLoading(false);
    }
  };

  return (
    <div className="page-container" style={{ maxWidth: "1140px" }}>
      {/* HEADER */}
      <div style={{ textAlign: "center", marginBottom: "36px" }}>
        <div style={{ display: "inline-flex", marginBottom: "12px" }}>
          <Badge variant="ai" size="md" icon={<Sparkles size={14} />}>
            AI Travel Studio
          </Badge>
        </div>
        <h1
          style={{
            fontSize: "clamp(2rem, 4vw, 3rem)",
            fontWeight: 900,
            color: "#FFFFFF",
            letterSpacing: "-0.5px",
          }}
        >
          Craft Your Bespoke Itinerary
        </h1>
        <p
          style={{
            color: "#94A3B8",
            fontSize: "1.05rem",
            maxWidth: "600px",
            margin: "8px auto 0 auto",
          }}
        >
          Follow 4 quick steps or jump straight to AI synthesis.
        </p>
      </div>

      {/* STEP PROGRESS INDICATOR */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          position: "relative",
          marginBottom: "40px",
          padding: "0 10px",
        }}
      >
        <div
          style={{
            position: "absolute",
            top: "20px",
            left: "40px",
            right: "40px",
            height: "2px",
            background: "rgba(255, 255, 255, 0.10)",
            zIndex: 0,
          }}
        />
        <div
          style={{
            position: "absolute",
            top: "20px",
            left: "40px",
            width: `${((currentStep - 1) / 3) * 100}%`,
            maxWidth: "calc(100% - 80px)",
            height: "2px",
            background: "linear-gradient(90deg, #0EA5E9, #14B8A6)",
            zIndex: 0,
            transition: "width 0.3s ease",
          }}
        />

        {[
          { step: 1, title: "Destination", icon: MapPin },
          { step: 2, stepName: "Duration & Budget", icon: DollarSign },
          { step: 3, stepName: "Style & Transit", icon: Compass },
          { step: 4, stepName: "Stay & Interests", icon: Heart },
        ].map((s, idx) => {
          const Icon = s.icon;
          const stepNum = idx + 1;
          const isPassed = currentStep > stepNum;
          const isCurrent = currentStep === stepNum;

          return (
            <div
              key={stepNum}
              onClick={() => !loading && setCurrentStep(stepNum)}
              style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                gap: "8px",
                position: "relative",
                zIndex: 1,
                cursor: "pointer",
              }}
            >
              <div
                style={{
                  width: "42px",
                  height: "42px",
                  borderRadius: "50%",
                  background:
                    isPassed || isCurrent
                      ? "linear-gradient(135deg, #0EA5E9, #14B8A6)"
                      : "rgba(15, 23, 42, 0.95)",
                  border: isCurrent
                    ? "2px solid #38BDF8"
                    : "2px solid rgba(255, 255, 255, 0.12)",
                  color: isPassed || isCurrent ? "#FFFFFF" : "#64748B",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  boxShadow: isCurrent
                    ? "0 0 16px rgba(14, 165, 233, 0.50)"
                    : "none",
                  transition: "all 0.25s ease",
                }}
              >
                {isPassed ? (
                  <Check size={18} strokeWidth={3} />
                ) : (
                  <Icon size={18} />
                )}
              </div>
              <span
                style={{
                  fontSize: "0.82rem",
                  fontWeight: isCurrent ? 700 : 500,
                  color: isCurrent
                    ? "#38BDF8"
                    : isPassed
                      ? "#CBD5E1"
                      : "#64748B",
                }}
              >
                Step {stepNum}
              </span>
            </div>
          );
        })}
      </div>

      {/* ERROR ALERT */}
      {error && (
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "12px",
            background: "rgba(239, 68, 68, 0.15)",
            border: "1px solid rgba(239, 68, 68, 0.35)",
            color: "#FCA5A5",
            padding: "14px 20px",
            borderRadius: "14px",
            marginBottom: "24px",
            fontSize: "0.95rem",
          }}
        >
          <AlertCircle size={20} style={{ flexShrink: 0 }} />
          <span>{error}</span>
        </div>
      )}

      {/* AI PROCESSING MODAL / OVERLAY */}
      {loading ? (
        <GlassCard style={{ padding: "50px 30px", textAlign: "center" }}>
          <div
            style={{
              width: "70px",
              height: "70px",
              borderRadius: "20px",
              background: "linear-gradient(135deg, #0EA5E9, #14B8A6)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              margin: "0 auto 24px auto",
              boxShadow: "0 0 32px rgba(14, 165, 233, 0.50)",
            }}
            className="ai-pulse-glow"
          >
            <Sparkles size={34} color="#FFFFFF" />
          </div>

          <h2
            style={{
              fontSize: "1.8rem",
              fontWeight: 800,
              color: "#FFFFFF",
              marginBottom: "10px",
            }}
          >
            Synthesizing Itinerary for {destination}...
          </h2>
          <p
            style={{
              color: "#94A3B8",
              fontSize: "0.95rem",
              maxWidth: "500px",
              margin: "0 auto 36px auto",
            }}
          >
            Our multi-agent system is parsing meteorological forecasts,
            historical footfalls, and regional routes.
          </p>

          <div
            style={{
              maxWidth: "480px",
              margin: "0 auto",
              display: "flex",
              flexDirection: "column",
              gap: "14px",
              textAlign: "left",
            }}
          >
            {AI_GENERATION_STEPS.map((stepText, idx) => {
              const isDone = aiProcessingStage > idx;
              const isCurrent = aiProcessingStage === idx;

              return (
                <div
                  key={idx}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "12px",
                    padding: "10px 14px",
                    borderRadius: "10px",
                    background: isCurrent
                      ? "rgba(14, 165, 233, 0.12)"
                      : "transparent",
                    border: isCurrent
                      ? "1px solid rgba(14, 165, 233, 0.25)"
                      : "1px solid transparent",
                    transition: "all 0.3s ease",
                  }}
                >
                  <div
                    style={{
                      width: "22px",
                      height: "22px",
                      borderRadius: "50%",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      background: isDone
                        ? "#10B981"
                        : isCurrent
                          ? "#0EA5E9"
                          : "rgba(255, 255, 255, 0.10)",
                      color: "#FFFFFF",
                      fontSize: "0.75rem",
                      flexShrink: 0,
                    }}
                  >
                    {isDone ? (
                      <Check size={14} />
                    ) : isCurrent ? (
                      <Loader2 size={12} className="ai-spin" />
                    ) : (
                      idx + 1
                    )}
                  </div>
                  <span
                    style={{
                      fontSize: "0.92rem",
                      color: isDone
                        ? "#E2E8F0"
                        : isCurrent
                          ? "#38BDF8"
                          : "#64748B",
                      fontWeight: isCurrent ? 700 : 500,
                    }}
                  >
                    {stepText}
                  </span>
                </div>
              );
            })}
          </div>
        </GlassCard>
      ) : (
        /* STEP CARD FORM */
        <GlassCard style={{ padding: "36px 32px" }}>
          {/* STEP 1: DESTINATION */}
          {currentStep === 1 && (
            <div
              style={{ display: "flex", flexDirection: "column", gap: "28px" }}
            >
              <div>
                <h3
                  style={{
                    fontSize: "1.4rem",
                    fontWeight: 800,
                    color: "#FFFFFF",
                    marginBottom: "6px",
                  }}
                >
                  Where would you like to travel?
                </h3>
                <p style={{ color: "#94A3B8", fontSize: "0.92rem" }}>
                  Type any destination in India or worldwide, or pick a popular
                  sanctuary below.
                </p>
              </div>

              <div>
                <label
                  style={{
                    display: "block",
                    fontSize: "0.88rem",
                    fontWeight: 600,
                    color: "#CBD5E1",
                    marginBottom: "8px",
                  }}
                >
                  Destination City / Region
                </label>
                <div style={{ position: "relative" }}>
                  <MapPin
                    size={20}
                    color="#38BDF8"
                    style={{
                      position: "absolute",
                      left: "16px",
                      top: "50%",
                      transform: "translateY(-50%)",
                    }}
                  />
                  <input
                    type="text"
                    value={destination}
                    onChange={(e) => setDestination(e.target.value)}
                    placeholder="e.g. Munnar, Coorg, Ooty, Varkala, Wayanad..."
                    className="input-base"
                    style={{ paddingLeft: "48px", fontSize: "1.1rem" }}
                    autoFocus
                  />
                </div>
              </div>

              <div>
                <span
                  style={{
                    fontSize: "0.82rem",
                    fontWeight: 700,
                    color: "#64748B",
                    textTransform: "uppercase",
                    letterSpacing: "0.5px",
                    display: "block",
                    marginBottom: "10px",
                  }}
                >
                  Quick Picks
                </span>
                <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
                  {POPULAR_DESTINATIONS.map((dest) => (
                    <button
                      key={dest}
                      type="button"
                      onClick={() => setDestination(dest)}
                      style={{
                        padding: "7px 14px",
                        borderRadius: "999px",
                        background:
                          destination.toLowerCase() === dest.toLowerCase()
                            ? "rgba(14, 165, 233, 0.25)"
                            : "rgba(255, 255, 255, 0.05)",
                        border:
                          destination.toLowerCase() === dest.toLowerCase()
                            ? "1px solid #38BDF8"
                            : "1px solid rgba(255, 255, 255, 0.10)",
                        color:
                          destination.toLowerCase() === dest.toLowerCase()
                            ? "#38BDF8"
                            : "#CBD5E1",
                        fontSize: "0.88rem",
                        fontWeight: 600,
                        cursor: "pointer",
                        transition: "all 0.2s ease",
                      }}
                    >
                      {dest}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* STEP 2: DURATION & BUDGET */}
          {currentStep === 2 && (
            <div
              style={{ display: "flex", flexDirection: "column", gap: "28px" }}
            >
              <div>
                <h3
                  style={{
                    fontSize: "1.4rem",
                    fontWeight: 800,
                    color: "#FFFFFF",
                    marginBottom: "6px",
                  }}
                >
                  Trip Duration & Budget Allocation
                </h3>
                <p style={{ color: "#94A3B8", fontSize: "0.92rem" }}>
                  Define the duration, group size, and total estimated spending
                  limit.
                </p>
              </div>

              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))",
                  gap: "24px",
                }}
              >
                <div>
                  <label
                    style={{
                      display: "block",
                      fontSize: "0.88rem",
                      fontWeight: 600,
                      color: "#CBD5E1",
                      marginBottom: "8px",
                    }}
                  >
                    Duration (Days)
                  </label>
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: "10px",
                    }}
                  >
                    <button
                      type="button"
                      onClick={() =>
                        setDurationDays(Math.max(1, durationDays - 1))
                      }
                      style={{
                        width: "42px",
                        height: "42px",
                        borderRadius: "10px",
                        background: "rgba(255, 255, 255, 0.08)",
                        border: "1px solid rgba(255, 255, 255, 0.15)",
                        color: "#FFFFFF",
                        fontSize: "1.2rem",
                        cursor: "pointer",
                      }}
                    >
                      -
                    </button>
                    <input
                      type="number"
                      min="1"
                      max="30"
                      value={durationDays}
                      onChange={(e) =>
                        setDurationDays(
                          Math.max(1, Math.min(30, Number(e.target.value))),
                        )
                      }
                      className="input-base"
                      style={{
                        textAlign: "center",
                        fontSize: "1.2rem",
                        fontWeight: 700,
                      }}
                    />
                    <button
                      type="button"
                      onClick={() =>
                        setDurationDays(Math.min(30, durationDays + 1))
                      }
                      style={{
                        width: "42px",
                        height: "42px",
                        borderRadius: "10px",
                        background: "rgba(255, 255, 255, 0.08)",
                        border: "1px solid rgba(255, 255, 255, 0.15)",
                        color: "#FFFFFF",
                        fontSize: "1.2rem",
                        cursor: "pointer",
                      }}
                    >
                      +
                    </button>
                  </div>
                </div>

                <div>
                  <label
                    style={{
                      display: "block",
                      fontSize: "0.88rem",
                      fontWeight: 600,
                      color: "#CBD5E1",
                      marginBottom: "8px",
                    }}
                  >
                    Travelers Count
                  </label>
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: "10px",
                    }}
                  >
                    <button
                      type="button"
                      onClick={() =>
                        setTravelersCount(Math.max(1, travelersCount - 1))
                      }
                      style={{
                        width: "42px",
                        height: "42px",
                        borderRadius: "10px",
                        background: "rgba(255, 255, 255, 0.08)",
                        border: "1px solid rgba(255, 255, 255, 0.15)",
                        color: "#FFFFFF",
                        fontSize: "1.2rem",
                        cursor: "pointer",
                      }}
                    >
                      -
                    </button>
                    <input
                      type="number"
                      min="1"
                      max="20"
                      value={travelersCount}
                      onChange={(e) =>
                        setTravelersCount(
                          Math.max(1, Math.min(20, Number(e.target.value))),
                        )
                      }
                      className="input-base"
                      style={{
                        textAlign: "center",
                        fontSize: "1.2rem",
                        fontWeight: 700,
                      }}
                    />
                    <button
                      type="button"
                      onClick={() =>
                        setTravelersCount(Math.min(20, travelersCount + 1))
                      }
                      style={{
                        width: "42px",
                        height: "42px",
                        borderRadius: "10px",
                        background: "rgba(255, 255, 255, 0.08)",
                        border: "1px solid rgba(255, 255, 255, 0.15)",
                        color: "#FFFFFF",
                        fontSize: "1.2rem",
                        cursor: "pointer",
                      }}
                    >
                      +
                    </button>
                  </div>
                </div>
              </div>

              <div className="space-y-4">
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "flex-end",
                    marginBottom: "4px",
                  }}
                >
                  <div>
                    <label
                      style={{
                        fontSize: "0.88rem",
                        fontWeight: 600,
                        color: "#CBD5E1",
                        display: "block",
                      }}
                    >
                      Total Estimated Budget (₹)
                    </label>
                    <span style={{ fontSize: "0.80rem", color: "#94A3B8" }}>
                      ~₹{Math.round(budget / Math.max(1, durationDays)).toLocaleString("en-IN")}/day · ~₹{Math.round(budget / Math.max(1, durationDays * travelersCount)).toLocaleString("en-IN")}/person/day
                    </span>
                  </div>
                  <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
                    <span style={{ color: "#38BDF8", fontWeight: 700 }}>₹</span>
                    <input
                      type="number"
                      min="2000"
                      max="300000"
                      step="500"
                      value={budget}
                      onChange={(e) => setBudget(Math.max(1000, Number(e.target.value)))}
                      className="input-base"
                      style={{
                        width: "120px",
                        textAlign: "right",
                        fontSize: "1.1rem",
                        fontWeight: 800,
                        color: "#38BDF8",
                        padding: "6px 12px",
                      }}
                    />
                  </div>
                </div>

                <input
                  type="range"
                  min="3000"
                  max="150000"
                  step="1000"
                  value={budget}
                  onChange={(e) => setBudget(Number(e.target.value))}
                  style={{
                    width: "100%",
                    accentColor: "#0EA5E9",
                    cursor: "pointer",
                  }}
                />

                {/* DYNAMIC REALISTIC PRESETS */}
                <div>
                  <span
                    style={{
                      fontSize: "0.75rem",
                      fontWeight: 700,
                      color: "#64748B",
                      textTransform: "uppercase",
                      letterSpacing: "0.5px",
                      display: "block",
                      marginBottom: "8px",
                    }}
                  >
                    Recommended Budget Tiers (Calculated for {durationDays} Days · {travelersCount} Traveler{travelersCount > 1 ? "s" : ""})
                  </span>
                  <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
                    {[
                      { label: "Backpacker", perDayPerson: 1500, style: "Hostel / Transit" },
                      { label: "Comfort", perDayPerson: 3000, style: "3-Star Hotel / Cabs" },
                      { label: "Romantic", perDayPerson: 4500, style: "Resort / Fine Dining" },
                      { label: "Luxury", perDayPerson: 8000, style: "5-Star Heritage / Private" },
                    ].map((tier) => {
                      const calculatedTotal = tier.perDayPerson * durationDays * travelersCount;
                      const isSelected = Math.abs(budget - calculatedTotal) < 1500;

                      return (
                        <button
                          key={tier.label}
                          type="button"
                          onClick={() => setBudget(calculatedTotal)}
                          style={{
                            padding: "8px 14px",
                            borderRadius: "12px",
                            background: isSelected
                              ? "rgba(14, 165, 233, 0.25)"
                              : "rgba(255, 255, 255, 0.05)",
                            border: isSelected
                              ? "1px solid #38BDF8"
                              : "1px solid rgba(255, 255, 255, 0.10)",
                            color: isSelected ? "#38BDF8" : "#CBD5E1",
                            fontSize: "0.82rem",
                            fontWeight: 600,
                            cursor: "pointer",
                            transition: "all 0.2s ease",
                            textAlign: "left",
                          }}
                        >
                          <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
                            <span>{tier.label}</span>
                            <span style={{ color: "#10B981", fontSize: "0.75rem" }}>
                              ₹{calculatedTotal.toLocaleString("en-IN")}
                            </span>
                          </div>
                          <div style={{ fontSize: "0.70rem", color: "#94A3B8" }}>
                            {tier.style}
                          </div>
                        </button>
                      );
                    })}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* STEP 3: STYLE & TRANSIT */}
          {currentStep === 3 && (
            <div
              style={{ display: "flex", flexDirection: "column", gap: "28px" }}
            >
              <div>
                <h3
                  style={{
                    fontSize: "1.4rem",
                    fontWeight: 800,
                    color: "#FFFFFF",
                    marginBottom: "6px",
                  }}
                >
                  Travel Style & Primary Transit
                </h3>
                <p style={{ color: "#94A3B8", fontSize: "0.92rem" }}>
                  The AI adjusts pace and routes based on your preferred
                  mobility.
                </p>
              </div>

              <div>
                <label
                  style={{
                    display: "block",
                    fontSize: "0.88rem",
                    fontWeight: 600,
                    color: "#CBD5E1",
                    marginBottom: "12px",
                  }}
                >
                  Travel Style
                </label>
                <div
                  style={{
                    display: "grid",
                    gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
                    gap: "12px",
                  }}
                >
                  {TRAVEL_STYLES.map((style) => {
                    const isSelected = travelStyle === style.id;
                    return (
                      <div
                        key={style.id}
                        onClick={() => setTravelStyle(style.id)}
                        style={{
                          padding: "16px",
                          borderRadius: "14px",
                          background: isSelected
                            ? "rgba(14, 165, 233, 0.15)"
                            : "rgba(255, 255, 255, 0.04)",
                          border: isSelected
                            ? "1px solid #38BDF8"
                            : "1px solid rgba(255, 255, 255, 0.08)",
                          cursor: "pointer",
                          transition: "all 0.2s ease",
                        }}
                      >
                        <div
                          style={{ fontSize: "1.5rem", marginBottom: "6px" }}
                        >
                          {style.icon}
                        </div>
                        <h4
                          style={{
                            fontSize: "0.95rem",
                            fontWeight: 700,
                            color: isSelected ? "#38BDF8" : "#FFFFFF",
                          }}
                        >
                          {style.label}
                        </h4>
                        <p
                          style={{
                            fontSize: "0.78rem",
                            color: "#94A3B8",
                            marginTop: "3px",
                          }}
                        >
                          {style.desc}
                        </p>
                      </div>
                    );
                  })}
                </div>
              </div>

              <div>
                <label
                  style={{
                    display: "block",
                    fontSize: "0.88rem",
                    fontWeight: 600,
                    color: "#CBD5E1",
                    marginBottom: "12px",
                  }}
                >
                  Transportation Mode
                </label>
                <div
                  style={{
                    display: "grid",
                    gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
                    gap: "10px",
                  }}
                >
                  {TRANSPORT_MODES.map((t) => {
                    const isSelected = transportationMode === t.id;
                    return (
                      <div
                        key={t.id}
                        onClick={() => setTransportationMode(t.id)}
                        style={{
                          padding: "14px",
                          borderRadius: "12px",
                          background: isSelected
                            ? "rgba(20, 184, 166, 0.15)"
                            : "rgba(255, 255, 255, 0.04)",
                          border: isSelected
                            ? "1px solid #2DD4BF"
                            : "1px solid rgba(255, 255, 255, 0.08)",
                          cursor: "pointer",
                          display: "flex",
                          alignItems: "center",
                          gap: "10px",
                          transition: "all 0.2s ease",
                        }}
                      >
                        <span style={{ fontSize: "1.3rem" }}>{t.icon}</span>
                        <div>
                          <h5
                            style={{
                              fontSize: "0.88rem",
                              fontWeight: 700,
                              color: isSelected ? "#2DD4BF" : "#FFFFFF",
                            }}
                          >
                            {t.label}
                          </h5>
                          <p style={{ fontSize: "0.72rem", color: "#94A3B8" }}>
                            {t.desc}
                          </p>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          )}

          {/* STEP 4: STAY & INTERESTS */}
          {currentStep === 4 && (
            <div
              style={{ display: "flex", flexDirection: "column", gap: "28px" }}
            >
              <div>
                <h3
                  style={{
                    fontSize: "1.4rem",
                    fontWeight: 800,
                    color: "#FFFFFF",
                    marginBottom: "6px",
                  }}
                >
                  Accommodations & Specific Interests
                </h3>
                <p style={{ color: "#94A3B8", fontSize: "0.92rem" }}>
                  Select what excites you most to fine-tune daily activities and
                  dining suggestions.
                </p>
              </div>

              <div>
                <label
                  style={{
                    display: "block",
                    fontSize: "0.88rem",
                    fontWeight: 600,
                    color: "#CBD5E1",
                    marginBottom: "12px",
                  }}
                >
                  Preferred Accommodation
                </label>
                <div
                  style={{
                    display: "grid",
                    gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
                    gap: "10px",
                  }}
                >
                  {ACCOMMODATIONS.map((acc) => {
                    const isSelected = preferredAccommodation === acc.id;
                    return (
                      <div
                        key={acc.id}
                        onClick={() => setPreferredAccommodation(acc.id)}
                        style={{
                          padding: "14px",
                          borderRadius: "12px",
                          background: isSelected
                            ? "rgba(14, 165, 233, 0.15)"
                            : "rgba(255, 255, 255, 0.04)",
                          border: isSelected
                            ? "1px solid #38BDF8"
                            : "1px solid rgba(255, 255, 255, 0.08)",
                          cursor: "pointer",
                        }}
                      >
                        <h5
                          style={{
                            fontSize: "0.9rem",
                            fontWeight: 700,
                            color: isSelected ? "#38BDF8" : "#FFFFFF",
                          }}
                        >
                          {acc.label}
                        </h5>
                        <p
                          style={{
                            fontSize: "0.75rem",
                            color: "#94A3B8",
                            marginTop: "2px",
                          }}
                        >
                          {acc.desc}
                        </p>
                      </div>
                    );
                  })}
                </div>
              </div>

              <div>
                <label
                  style={{
                    display: "block",
                    fontSize: "0.88rem",
                    fontWeight: 600,
                    color: "#CBD5E1",
                    marginBottom: "12px",
                  }}
                >
                  Activity & Interest Focus ({selectedInterests.length}{" "}
                  selected)
                </label>
                <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
                  {INTEREST_TAGS.map((tag) => {
                    const isSelected = selectedInterests.includes(tag);
                    return (
                      <button
                        key={tag}
                        type="button"
                        onClick={() => toggleInterest(tag)}
                        style={{
                          padding: "8px 16px",
                          borderRadius: "999px",
                          background: isSelected
                            ? "linear-gradient(135deg, rgba(14, 165, 233, 0.3), rgba(20, 184, 166, 0.3))"
                            : "rgba(255, 255, 255, 0.05)",
                          border: isSelected
                            ? "1px solid #38BDF8"
                            : "1px solid rgba(255, 255, 255, 0.10)",
                          color: isSelected ? "#FFFFFF" : "#CBD5E1",
                          fontSize: "0.85rem",
                          fontWeight: 600,
                          cursor: "pointer",
                          display: "inline-flex",
                          alignItems: "center",
                          gap: "6px",
                          transition: "all 0.2s ease",
                        }}
                      >
                        {isSelected && <Check size={14} color="#38BDF8" />}
                        <span>{tag}</span>
                      </button>
                    );
                  })}
                </div>
              </div>
            </div>
          )}

          {/* NAVIGATION & ACTION FOOTER */}
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              borderTop: "1px solid rgba(255, 255, 255, 0.08)",
              paddingTop: "24px",
              marginTop: "32px",
              flexWrap: "wrap",
              gap: "12px",
            }}
          >
            {currentStep > 1 ? (
              <Button
                type="button"
                variant="secondary"
                size="md"
                leftIcon={<ArrowLeft size={16} />}
                onClick={() => setCurrentStep(currentStep - 1)}
              >
                Back
              </Button>
            ) : (
              <div />
            )}

            <div style={{ display: "flex", gap: "10px" }}>
              {currentStep < 4 ? (
                <Button
                  type="button"
                  variant="primary"
                  size="md"
                  rightIcon={<ArrowRight size={16} />}
                  onClick={() => {
                    if (currentStep === 1 && !destination.trim()) {
                      setError("Please enter a destination to proceed.");
                      return;
                    }
                    setError("");
                    setCurrentStep(currentStep + 1);
                  }}
                >
                  Continue
                </Button>
              ) : (
                <Button
                  type="button"
                  variant="primary"
                  size="lg"
                  leftIcon={<Sparkles size={18} />}
                  onClick={() => handleGenerateTrip()}
                >
                  Generate AI Itinerary
                </Button>
              )}
            </div>
          </div>
        </GlassCard>
      )}
    </div>
  );
}

export default function PlannerPage() {
  return (
    <Suspense
      fallback={
        <div
          className="page-container"
          style={{ textAlign: "center", padding: "100px 20px" }}
        >
          <div
            style={{
              color: "var(--tg-primary)",
              fontSize: "1.2rem",
              fontWeight: 600,
              marginBottom: "12px",
            }}
          >
            Loading Planner...
          </div>
        </div>
      }
    >
      <PlannerContent />
    </Suspense>
  );
}
