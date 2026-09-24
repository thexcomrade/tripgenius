"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  Compass,
  Calendar,
  IndianRupee,
  MapPin,
  Trash2,
  ExternalLink,
  PlusCircle,
  Award,
  CheckCircle2,
  Lock,
  Sparkles,
  BookmarkCheck,
  Check,
} from "lucide-react";

interface Achievement {
  id: number;
  title: string;
  icon: string;
  description: string;
  unlocked: boolean;
  progress?: string;
}

interface SavedTrip {
  id: string;
  destination: string;
  trip_title?: string;
  duration_days: number;
  budget: number;
  created_at?: string;
  image?: string;
  travel_style?: string;
}

interface ProfileGridProps {
  activeTab: string;
  achievements: Achievement[];
  totalTrips: number;
  savedTrips: number;
  savedTripsList?: SavedTrip[];
  onDeleteSavedTrip?: (id: string) => void;
  userPreferences?: string[];
  onSavePreferences?: (prefs: string[]) => void;
}

const SAMPLE_INSPIRATIONS: SavedTrip[] = [
  {
    id: "sample-1",
    trip_title: "Varkala Cliffside Coastal Retreat",
    destination: "Varkala, Kerala",
    duration_days: 3,
    budget: 18000,
    image: "/destinations/varkala.jpg",
    travel_style: "Beach & Wellness",
  },
  {
    id: "sample-2",
    trip_title: "Munnar Misty Tea Highlands",
    destination: "Munnar, Kerala",
    duration_days: 4,
    budget: 24000,
    image: "/destinations/munnar.jpg",
    travel_style: "Scenic Nature & Tea Hills",
  },
  {
    id: "sample-3",
    trip_title: "Goa Beach & Portuguese Heritage",
    destination: "Goa",
    duration_days: 3,
    budget: 22000,
    image: "/destinations/goa.jpg",
    travel_style: "Coastal Leisure & Culture",
  },
];

const PREFERENCE_OPTIONS = [
  "Adventure & Trekking",
  "Scenic Highlands & Tea Hills",
  "Coastal & Beach Escapes",
  "Eco Tourism & Sustainable",
  "Local Food & Street Dining",
  "Heritage, Temples & Culture",
  "Wildlife & Nature Reserves",
  "Ayurveda & Wellness Retreats",
  "Photography & Drone Spots",
  "Budget-Conscious Backpacking",
  "Boutique Luxury Resorts",
  "Road Trips & Scenic Drives",
];

export default function ProfileGrid({
  activeTab,
  achievements,
  totalTrips,
  savedTrips,
  savedTripsList = [],
  onDeleteSavedTrip,
  userPreferences = [],
  onSavePreferences,
}: ProfileGridProps) {
  const router = useRouter();
  const [selectedPrefs, setSelectedPrefs] = useState<string[]>(
    userPreferences.length > 0
      ? userPreferences
      : [
          "Scenic Highlands & Tea Hills",
          "Coastal & Beach Escapes",
          "Eco Tourism & Sustainable",
          "Local Food & Street Dining",
        ],
  );
  const [prefsSaved, setPrefsSaved] = useState(false);

  const togglePreference = (pref: string) => {
    if (selectedPrefs.includes(pref)) {
      setSelectedPrefs(selectedPrefs.filter((p) => p !== pref));
    } else {
      setSelectedPrefs([...selectedPrefs, pref]);
    }
  };

  const handleSavePreferences = () => {
    if (onSavePreferences) {
      onSavePreferences(selectedPrefs);
      setPrefsSaved(true);
      setTimeout(() => setPrefsSaved(false), 2500);
    }
  };

  // 1. My Journeys Tab
  const renderTripsTab = () => {
    const hasSaved = savedTripsList.length > 0;
    const tripsToDisplay = hasSaved ? savedTripsList : SAMPLE_INSPIRATIONS;

    return (
      <div style={{ display: "flex", flexDirection: "column", gap: "24px" }}>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            flexWrap: "wrap",
            gap: "12px",
          }}
        >
          <div>
            <h2
              style={{
                fontSize: "1.25rem",
                fontWeight: 800,
                color: "#FFFFFF",
                display: "flex",
                alignItems: "center",
                gap: "8px",
              }}
            >
              <Compass size={20} color="#38BDF8" />
              <span>
                {hasSaved
                  ? "Your Planned & Generated Journeys"
                  : "Curated Journeys & Sample Itineraries"}
              </span>
            </h2>
            <p style={{ fontSize: "0.88rem", color: "#94A3B8", marginTop: "4px" }}>
              {hasSaved
                ? `You have ${savedTripsList.length} customized itinerary plans saved.`
                : "Explore sample journeys or synthesize your own with TripGenius AI."}
            </p>
          </div>

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
                boxShadow: "0 4px 12px rgba(14, 165, 233, 0.35)",
              }}
            >
              <PlusCircle size={16} />
              <span>New Journey</span>
            </button>
          </Link>
        </div>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))",
            gap: "24px",
          }}
        >
          {/* CREATE NEW ADVENTURE ACTION CARD */}
          <Link
            href="/planner"
            style={{
              textDecoration: "none",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              padding: "36px 24px",
              borderRadius: "20px",
              border: "2px dashed rgba(14, 165, 233, 0.35)",
              background: "rgba(14, 165, 233, 0.04)",
              textAlign: "center",
              minHeight: "260px",
              transition: "all 0.2s ease",
            }}
          >
            <div
              style={{
                width: "56px",
                height: "56px",
                borderRadius: "50%",
                background: "rgba(14, 165, 233, 0.15)",
                color: "#38BDF8",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                marginBottom: "14px",
              }}
            >
              <PlusCircle size={28} />
            </div>
            <h3
              style={{
                fontSize: "1.1rem",
                fontWeight: 700,
                color: "#FFFFFF",
                marginBottom: "6px",
              }}
            >
              Plan New Adventure
            </h3>
            <p
              style={{
                fontSize: "0.82rem",
                color: "#94A3B8",
                maxWidth: "240px",
                lineHeight: 1.5,
              }}
            >
              Synthesize an AI itinerary with live weather, exact expenses, and real Google-rated stays.
            </p>
          </Link>

          {/* TRIP CARDS */}
          {tripsToDisplay.map((trip: any, idx: number) => {
            const fallbackImg =
              idx === 0
                ? "/destinations/varkala.jpg"
                : idx === 1
                  ? "/destinations/munnar.jpg"
                  : "/destinations/goa.jpg";
            const image = trip.image || fallbackImg;

            return (
              <div
                key={trip.id || idx}
                style={{
                  display: "flex",
                  flexDirection: "column",
                  borderRadius: "20px",
                  overflow: "hidden",
                  border: "1px solid rgba(255, 255, 255, 0.10)",
                  background: "rgba(15, 23, 42, 0.75)",
                  backdropFilter: "blur(16px)",
                  boxShadow: "0 8px 24px rgba(0, 0, 0, 0.30)",
                  transition: "all 0.25s ease",
                }}
              >
                {/* COVER IMAGE */}
                <div
                  style={{
                    position: "relative",
                    height: "170px",
                    width: "100%",
                    overflow: "hidden",
                  }}
                >
                  <img
                    src={image}
                    alt={trip.destination || trip.trip_title}
                    style={{
                      width: "100%",
                      height: "100%",
                      objectFit: "cover",
                    }}
                    onError={(e) => {
                      (e.currentTarget as HTMLImageElement).src =
                        "/destinations/munnar.jpg";
                    }}
                  />
                  <div
                    style={{
                      position: "absolute",
                      inset: 0,
                      background:
                        "linear-gradient(to top, rgba(11, 17, 32, 0.95) 0%, rgba(11, 17, 32, 0.2) 60%, transparent 100%)",
                    }}
                  />

                  {/* BADGES */}
                  <div
                    style={{
                      position: "absolute",
                      top: "12px",
                      left: "12px",
                      display: "flex",
                      alignItems: "center",
                      gap: "6px",
                    }}
                  >
                    <span
                      style={{
                        padding: "3px 10px",
                        borderRadius: "999px",
                        fontSize: "0.75rem",
                        fontWeight: 700,
                        background: "rgba(15, 23, 42, 0.85)",
                        color: "#FFFFFF",
                        border: "1px solid rgba(255, 255, 255, 0.15)",
                        display: "flex",
                        alignItems: "center",
                        gap: "4px",
                      }}
                    >
                      <Calendar size={12} color="#38BDF8" />
                      {trip.duration_days} Days
                    </span>
                  </div>

                  <div
                    style={{
                      position: "absolute",
                      top: "12px",
                      right: "12px",
                    }}
                  >
                    <span
                      style={{
                        padding: "3px 10px",
                        borderRadius: "999px",
                        fontSize: "0.75rem",
                        fontWeight: 700,
                        background: "rgba(16, 185, 129, 0.85)",
                        color: "#FFFFFF",
                        display: "flex",
                        alignItems: "center",
                        gap: "2px",
                      }}
                    >
                      <IndianRupee size={12} />
                      {trip.budget
                        ? Number(trip.budget).toLocaleString("en-IN")
                        : "18,000"}
                    </span>
                  </div>

                  <div
                    style={{
                      position: "absolute",
                      bottom: "10px",
                      left: "14px",
                      display: "flex",
                      alignItems: "center",
                      gap: "6px",
                      fontSize: "0.82rem",
                      fontWeight: 600,
                      color: "#38BDF8",
                    }}
                  >
                    <MapPin size={13} color="#FB7185" />
                    <span>{trip.destination}</span>
                  </div>
                </div>

                {/* CARD BODY */}
                <div
                  style={{
                    padding: "18px",
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "space-between",
                    flex: 1,
                  }}
                >
                  <div>
                    <h3
                      style={{
                        fontSize: "1rem",
                        fontWeight: 700,
                        color: "#FFFFFF",
                        marginBottom: "6px",
                      }}
                    >
                      {trip.trip_title || `${trip.destination} Experience`}
                    </h3>
                    <p
                      style={{
                        fontSize: "0.8rem",
                        color: "#94A3B8",
                        lineHeight: 1.5,
                      }}
                    >
                      {trip.travel_style ||
                        "Curated multi-day scenic exploration with tailored dining and activity pacing."}
                    </p>
                  </div>

                  {/* ACTION FOOTER */}
                  <div
                    style={{
                      marginTop: "16px",
                      paddingTop: "12px",
                      borderTop: "1px solid rgba(255, 255, 255, 0.08)",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "space-between",
                    }}
                  >
                    <button
                      type="button"
                      onClick={() => {
                        if (hasSaved) {
                          localStorage.setItem(
                            "tripgenius_generated_trip",
                            JSON.stringify(trip),
                          );
                          router.push("/trip/generated");
                        } else {
                          router.push(
                            `/planner?destination=${encodeURIComponent(trip.destination)}&duration=${trip.duration_days}`,
                          );
                        }
                      }}
                      style={{
                        display: "inline-flex",
                        alignItems: "center",
                        gap: "6px",
                        background: "transparent",
                        border: "none",
                        color: "#38BDF8",
                        fontSize: "0.82rem",
                        fontWeight: 700,
                        cursor: "pointer",
                      }}
                    >
                      <span>View Itinerary</span>
                      <ExternalLink size={13} />
                    </button>

                    {hasSaved && onDeleteSavedTrip && (
                      <button
                        type="button"
                        onClick={() => onDeleteSavedTrip(trip.id)}
                        style={{
                          background: "transparent",
                          border: "none",
                          color: "#EF4444",
                          cursor: "pointer",
                          padding: "4px",
                        }}
                        title="Delete from saved"
                      >
                        <Trash2 size={14} />
                      </button>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    );
  };

  // 2. Saved Plans Tab
  const renderSavedTab = () => {
    if (savedTripsList.length === 0) {
      return (
        <div
          style={{
            textAlign: "center",
            padding: "48px 24px",
            borderRadius: "24px",
            border: "1px solid rgba(255, 255, 255, 0.10)",
            background: "rgba(15, 23, 42, 0.65)",
            backdropFilter: "blur(16px)",
          }}
        >
          <div
            style={{
              width: "60px",
              height: "60px",
              borderRadius: "50%",
              background: "rgba(245, 158, 11, 0.15)",
              color: "#FBBF24",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              margin: "0 auto 16px",
              border: "1px solid rgba(245, 158, 11, 0.25)",
            }}
          >
            <BookmarkCheck size={30} />
          </div>
          <h3
            style={{
              fontSize: "1.2rem",
              fontWeight: 800,
              color: "#FFFFFF",
              marginBottom: "8px",
            }}
          >
            No Saved Trips Yet
          </h3>
          <p
            style={{
              fontSize: "0.88rem",
              color: "#94A3B8",
              maxWidth: "420px",
              margin: "0 auto 24px",
              lineHeight: 1.6,
            }}
          >
            When you generate personalized itineraries in the Trip Planner, bookmark your favorites to access them anytime offline or on the go.
          </p>
          <Link href="/planner" style={{ textDecoration: "none" }}>
            <button
              type="button"
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: "6px",
                padding: "10px 22px",
                borderRadius: "12px",
                fontSize: "0.88rem",
                fontWeight: 700,
                background:
                  "linear-gradient(135deg, #0EA5E9 0%, #14B8A6 100%)",
                border: "none",
                color: "#FFFFFF",
                cursor: "pointer",
              }}
            >
              <Sparkles size={16} color="#FDE047" />
              <span>Generate First Trip</span>
            </button>
          </Link>
        </div>
      );
    }

    return (
      <div style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
        <h2
          style={{
            fontSize: "1.25rem",
            fontWeight: 800,
            color: "#FFFFFF",
            display: "flex",
            alignItems: "center",
            gap: "8px",
          }}
        >
          <BookmarkCheck size={20} color="#FBBF24" />
          <span>Bookmarked Itineraries ({savedTripsList.length})</span>
        </h2>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
            gap: "20px",
          }}
        >
          {savedTripsList.map((trip) => (
            <div
              key={trip.id}
              style={{
                borderRadius: "18px",
                border: "1px solid rgba(255, 255, 255, 0.10)",
                background: "rgba(15, 23, 42, 0.70)",
                padding: "20px",
                display: "flex",
                flexDirection: "column",
                justifyContent: "space-between",
                gap: "14px",
              }}
            >
              <div
                style={{
                  display: "flex",
                  alignItems: "flex-start",
                  justifyContent: "space-between",
                  gap: "10px",
                }}
              >
                <div>
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: "4px",
                      fontSize: "0.8rem",
                      color: "#FBBF24",
                      fontWeight: 600,
                      marginBottom: "4px",
                    }}
                  >
                    <MapPin size={13} />
                    <span>{trip.destination}</span>
                  </div>
                  <h3
                    style={{
                      fontSize: "1.05rem",
                      fontWeight: 700,
                      color: "#FFFFFF",
                    }}
                  >
                    {trip.trip_title || `${trip.destination} Adventure`}
                  </h3>
                </div>

                {onDeleteSavedTrip && (
                  <button
                    type="button"
                    onClick={() => onDeleteSavedTrip(trip.id)}
                    style={{
                      background: "transparent",
                      border: "none",
                      color: "#EF4444",
                      cursor: "pointer",
                      padding: "4px",
                    }}
                    title="Delete Saved Trip"
                  >
                    <Trash2 size={15} />
                  </button>
                )}
              </div>

              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "10px",
                  fontSize: "0.78rem",
                }}
              >
                <span
                  style={{
                    padding: "3px 10px",
                    borderRadius: "999px",
                    background: "rgba(30, 41, 59, 0.8)",
                    border: "1px solid rgba(255, 255, 255, 0.08)",
                    color: "#E2E8F0",
                    display: "flex",
                    alignItems: "center",
                    gap: "4px",
                  }}
                >
                  <Calendar size={12} color="#38BDF8" />
                  {trip.duration_days} Days
                </span>
                <span
                  style={{
                    padding: "3px 10px",
                    borderRadius: "999px",
                    background: "rgba(30, 41, 59, 0.8)",
                    border: "1px solid rgba(255, 255, 255, 0.08)",
                    color: "#34D399",
                    display: "flex",
                    alignItems: "center",
                    gap: "2px",
                  }}
                >
                  <IndianRupee size={12} />
                  ₹{Number(trip.budget).toLocaleString("en-IN")}
                </span>
              </div>

              <button
                type="button"
                onClick={() => {
                  localStorage.setItem(
                    "tripgenius_generated_trip",
                    JSON.stringify(trip),
                  );
                  router.push("/trip/generated");
                }}
                style={{
                  width: "100%",
                  padding: "8px",
                  borderRadius: "10px",
                  fontSize: "0.82rem",
                  fontWeight: 600,
                  background: "rgba(255, 255, 255, 0.08)",
                  border: "1px solid rgba(255, 255, 255, 0.12)",
                  color: "#FFFFFF",
                  cursor: "pointer",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  gap: "6px",
                }}
              >
                <span>View Full Itinerary</span>
                <ExternalLink size={13} />
              </button>
            </div>
          ))}
        </div>
      </div>
    );
  };

  // 3. Achievements Tab
  const renderAchievementsTab = () => {
    return (
      <div style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
        <div>
          <h2
            style={{
              fontSize: "1.25rem",
              fontWeight: 800,
              color: "#FFFFFF",
              display: "flex",
              alignItems: "center",
              gap: "8px",
            }}
          >
            <Award size={20} color="#FBBF24" />
            <span>Traveler Badges & Milestones</span>
          </h2>
          <p style={{ fontSize: "0.88rem", color: "#94A3B8", marginTop: "4px" }}>
            Unlock achievements as you plan sustainable journeys and explore new destinations.
          </p>
        </div>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))",
            gap: "20px",
          }}
        >
          {achievements.map((ach) => (
            <div
              key={ach.id}
              style={{
                borderRadius: "18px",
                border: ach.unlocked
                  ? "1px solid rgba(14, 165, 233, 0.35)"
                  : "1px solid rgba(255, 255, 255, 0.08)",
                background: ach.unlocked
                  ? "linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(14, 165, 233, 0.12) 100%)"
                  : "rgba(15, 23, 42, 0.45)",
                padding: "20px",
                display: "flex",
                flexDirection: "column",
                justifyContent: "space-between",
                gap: "12px",
              }}
            >
              <div
                style={{
                  display: "flex",
                  alignItems: "flex-start",
                  justifyContent: "space-between",
                }}
              >
                <div
                  style={{
                    width: "48px",
                    height: "48px",
                    borderRadius: "14px",
                    background: "rgba(255, 255, 255, 0.06)",
                    border: "1px solid rgba(255, 255, 255, 0.12)",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontSize: "1.5rem",
                  }}
                >
                  {ach.icon}
                </div>

                {ach.unlocked ? (
                  <span
                    style={{
                      display: "inline-flex",
                      alignItems: "center",
                      gap: "4px",
                      padding: "3px 9px",
                      borderRadius: "999px",
                      fontSize: "0.72rem",
                      fontWeight: 700,
                      background: "rgba(16, 185, 129, 0.15)",
                      color: "#34D399",
                      border: "1px solid rgba(16, 185, 129, 0.35)",
                    }}
                  >
                    <CheckCircle2 size={12} />
                    Unlocked
                  </span>
                ) : (
                  <span
                    style={{
                      display: "inline-flex",
                      alignItems: "center",
                      gap: "4px",
                      padding: "3px 9px",
                      borderRadius: "999px",
                      fontSize: "0.72rem",
                      fontWeight: 600,
                      background: "rgba(30, 41, 59, 0.8)",
                      color: "#94A3B8",
                      border: "1px solid rgba(255, 255, 255, 0.08)",
                    }}
                  >
                    <Lock size={12} />
                    In Progress
                  </span>
                )}
              </div>

              <div>
                <h3
                  style={{
                    fontSize: "1rem",
                    fontWeight: 700,
                    color: "#FFFFFF",
                    marginBottom: "4px",
                  }}
                >
                  {ach.title}
                </h3>
                <p
                  style={{
                    fontSize: "0.8rem",
                    color: "#94A3B8",
                    lineHeight: 1.5,
                  }}
                >
                  {ach.description}
                </p>
              </div>

              {/* Progress bar */}
              <div
                style={{
                  width: "100%",
                  height: "5px",
                  borderRadius: "999px",
                  background: "rgba(255, 255, 255, 0.08)",
                  overflow: "hidden",
                }}
              >
                <div
                  style={{
                    height: "100%",
                    width: ach.unlocked ? "100%" : "35%",
                    borderRadius: "999px",
                    background: ach.unlocked
                      ? "linear-gradient(90deg, #0EA5E9, #10B981)"
                      : "#475569",
                  }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  // 4. Preferences Tab
  const renderPreferencesTab = () => {
    return (
      <div
        style={{
          maxWidth: "750px",
          margin: "0 auto",
          borderRadius: "24px",
          border: "1px solid rgba(255, 255, 255, 0.10)",
          background: "rgba(15, 23, 42, 0.70)",
          backdropFilter: "blur(16px)",
          padding: "28px",
          display: "flex",
          flexDirection: "column",
          gap: "20px",
        }}
      >
        <div>
          <h2
            style={{
              fontSize: "1.25rem",
              fontWeight: 800,
              color: "#FFFFFF",
              display: "flex",
              alignItems: "center",
              gap: "8px",
            }}
          >
            <Sparkles size={20} color="#38BDF8" />
            <span>Customize Travel Interests & Vibe</span>
          </h2>
          <p style={{ fontSize: "0.88rem", color: "#94A3B8", marginTop: "4px" }}>
            TripGenius AI incorporates your selected travel styles to personalize recommended activities, stays, and packing essentials.
          </p>
        </div>

        <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
          {PREFERENCE_OPTIONS.map((option) => {
            const isSelected = selectedPrefs.includes(option);

            return (
              <button
                key={option}
                type="button"
                onClick={() => togglePreference(option)}
                style={{
                  display: "inline-flex",
                  alignItems: "center",
                  gap: "6px",
                  padding: "8px 14px",
                  borderRadius: "12px",
                  fontSize: "0.82rem",
                  fontWeight: isSelected ? 700 : 500,
                  cursor: "pointer",
                  background: isSelected
                    ? "rgba(14, 165, 233, 0.20)"
                    : "rgba(255, 255, 255, 0.05)",
                  color: isSelected ? "#38BDF8" : "#CBD5E1",
                  border: isSelected
                    ? "1px solid rgba(14, 165, 233, 0.50)"
                    : "1px solid rgba(255, 255, 255, 0.08)",
                  transition: "all 0.15s ease",
                }}
              >
                {isSelected && <Check size={14} color="#38BDF8" />}
                <span>{option}</span>
              </button>
            );
          })}
        </div>

        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            paddingTop: "16px",
            borderTop: "1px solid rgba(255, 255, 255, 0.08)",
          }}
        >
          <span style={{ fontSize: "0.82rem", color: "#94A3B8" }}>
            {selectedPrefs.length} style{selectedPrefs.length === 1 ? "" : "s"} active
          </span>

          <button
            type="button"
            onClick={handleSavePreferences}
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: "6px",
              padding: "10px 20px",
              borderRadius: "12px",
              fontSize: "0.85rem",
              fontWeight: 700,
              background: "linear-gradient(135deg, #0EA5E9 0%, #14B8A6 100%)",
              border: "none",
              color: "#FFFFFF",
              cursor: "pointer",
              boxShadow: "0 4px 14px rgba(14, 165, 233, 0.35)",
            }}
          >
            {prefsSaved ? (
              <>
                <Check size={16} color="#34D399" />
                <span>Saved Successfully!</span>
              </>
            ) : (
              <>
                <Sparkles size={16} color="#FDE047" />
                <span>Save Preferences</span>
              </>
            )}
          </button>
        </div>
      </div>
    );
  };

  return (
    <section style={{ width: "100%", maxWidth: "1200px", margin: "0 auto", padding: "0 8px" }}>
      {activeTab === "trips" && renderTripsTab()}
      {activeTab === "saved" && renderSavedTab()}
      {activeTab === "achievements" && renderAchievementsTab()}
      {activeTab === "preferences" && renderPreferencesTab()}
    </section>
  );
}
