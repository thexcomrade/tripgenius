"use client";

import { useEffect, useMemo, useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  Search,
  Calendar,
  DollarSign,
  Leaf,
  MapPin,
  Trash2,
  Heart,
  ArrowRight,
  LayoutGrid,
  List,
  Sparkles,
  Eye,
  Plus,
} from "lucide-react";
import Button from "../../../components/ui/Button";
import Badge from "../../../components/ui/Badge";
import { GlassCard, SectionHeader } from "../../../components/ui/Card";
import tripService from "../../../services/trip.service";

interface SavedTrip {
  id?: string;
  trip_title?: string;
  destination: string;
  duration_days: number;
  budget: number;
  travelers_count?: number;
  travel_style?: string;
  transportation_mode?: string;
  preferred_accommodation?: string;
  interests?: string[];
  saved_at?: string;
  created_at?: string;
  favorite?: boolean;
  is_favorite?: boolean;
  sustainability_score?: number;
  status?: string;
}

const DESTINATION_IMAGES: Record<string, string> = {
  Munnar: "/destinations/munnar.jpg",
  Varkala: "/destinations/varkala.jpg",
  Ooty: "/destinations/ooty.jpg",
  Kodaikanal: "/destinations/kodaikanal.jpg",
  Mysore: "/destinations/mysore.jpg",
  Coorg: "/destinations/coorg.jpg",
};

export default function TripHistoryPage() {
  const router = useRouter();

  const [loading, setLoading] = useState(true);
  const [trips, setTrips] = useState<SavedTrip[]>([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [filterStyle, setFilterStyle] = useState("All");
  const [sortBy, setSortBy] = useState("Newest");
  const [viewMode, setViewMode] = useState<"grid" | "list">("grid");

  useEffect(() => {
    async function loadHistory() {
      const token = localStorage.getItem("tripgenius_token");
      if (token) {
        try {
          const data = await tripService.getHistory();
          if (data && data.trips) {
            const backendTrips: SavedTrip[] = data.trips.map(
              (t: SavedTrip) => ({
                ...t,
                saved_at: t.created_at,
              }),
            );
            setTrips(backendTrips);
          }
        } catch {
          loadFromLocalStorage();
        }
      } else {
        loadFromLocalStorage();
      }
      setLoading(false);
    }

    const loadFromLocalStorage = () => {
      try {
        const stored = localStorage.getItem("saved_trips");
        if (stored) {
          setTrips(JSON.parse(stored));
        }
      } catch {
        // ignore
      }
    };

    loadHistory();
  }, []);

  const handleDelete = async (tripId?: string, index?: number) => {
    if (
      !confirm("Are you sure you want to remove this trip from your archive?")
    )
      return;

    if (tripId) {
      try {
        await tripService.deleteTrip(tripId);
      } catch {
        // local fallback
      }
    }

    const updated = trips.filter((t, i) =>
      tripId ? t.id !== tripId : i !== index,
    );
    setTrips(updated);
    localStorage.setItem("saved_trips", JSON.stringify(updated));
  };

  const handleOpenTrip = (trip: SavedTrip) => {
    localStorage.setItem("latest_trip", JSON.stringify(trip));
    router.push("/trip/generated");
  };

  const filteredTrips = useMemo(() => {
    return trips
      .filter((t) => {
        const matchQuery =
          (t.trip_title || "")
            .toLowerCase()
            .includes(searchQuery.toLowerCase()) ||
          t.destination.toLowerCase().includes(searchQuery.toLowerCase());
        const matchStyle =
          filterStyle === "All" ||
          (t.travel_style || "").toLowerCase() === filterStyle.toLowerCase();
        return matchQuery && matchStyle;
      })
      .sort((a, b) => {
        if (sortBy === "Budget High") return (b.budget || 0) - (a.budget || 0);
        if (sortBy === "Budget Low") return (a.budget || 0) - (b.budget || 0);
        if (sortBy === "Duration")
          return (b.duration_days || 0) - (a.duration_days || 0);
        return (
          new Date(b.created_at || b.saved_at || 0).getTime() -
          new Date(a.created_at || a.saved_at || 0).getTime()
        );
      });
  }, [trips, searchQuery, filterStyle, sortBy]);

  return (
    <div
      className="page-container"
      style={{ display: "flex", flexDirection: "column", gap: "32px" }}
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
            <Badge variant="ai" size="sm">
              Personal Travel Archive
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
            Trip History ({trips.length})
          </h1>
          <p
            style={{ color: "#94A3B8", fontSize: "0.95rem", marginTop: "4px" }}
          >
            Review, reopen, or manage all previously synthesized travel
            itineraries.
          </p>
        </div>

        <Link href="/planner" style={{ textDecoration: "none" }}>
          <Button variant="primary" size="md" leftIcon={<Plus size={16} />}>
            Plan New Trip
          </Button>
        </Link>
      </div>

      {/* CONTROLS BAR: SEARCH, FILTERS, SORT, VIEW */}
      <GlassCard style={{ padding: "16px 20px" }}>
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            flexWrap: "wrap",
            gap: "16px",
          }}
        >
          {/* SEARCH */}
          <div
            style={{
              position: "relative",
              minWidth: "260px",
              flex: 1,
              maxWidth: "420px",
            }}
          >
            <Search
              size={16}
              color="#94A3B8"
              style={{
                position: "absolute",
                left: "14px",
                top: "50%",
                transform: "translateY(-50%)",
              }}
            />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search by destination or title..."
              className="input-base"
              style={{
                paddingLeft: "40px",
                paddingRight: "14px",
                height: "42px",
              }}
            />
          </div>

          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "12px",
              flexWrap: "wrap",
            }}
          >
            {/* STYLE FILTER */}
            <select
              value={filterStyle}
              onChange={(e) => setFilterStyle(e.target.value)}
              style={{
                padding: "10px 14px",
                borderRadius: "10px",
                background: "rgba(15, 23, 42, 0.85)",
                border: "1px solid rgba(255, 255, 255, 0.12)",
                color: "#F8FAFC",
                fontSize: "0.88rem",
                outline: "none",
                cursor: "pointer",
              }}
            >
              <option value="All">All Travel Styles</option>
              <option value="Leisure">Leisure</option>
              <option value="Adventure">Adventure</option>
              <option value="Eco-Friendly">Eco-Friendly</option>
              <option value="Cultural">Cultural</option>
              <option value="Romantic">Romantic</option>
            </select>

            {/* SORT BY */}
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              style={{
                padding: "10px 14px",
                borderRadius: "10px",
                background: "rgba(15, 23, 42, 0.85)",
                border: "1px solid rgba(255, 255, 255, 0.12)",
                color: "#F8FAFC",
                fontSize: "0.88rem",
                outline: "none",
                cursor: "pointer",
              }}
            >
              <option value="Newest">Newest First</option>
              <option value="Budget High">Budget: High to Low</option>
              <option value="Budget Low">Budget: Low to High</option>
              <option value="Duration">Longest Duration</option>
            </select>

            {/* VIEW MODE TOGGLE */}
            <div
              style={{
                display: "flex",
                background: "rgba(255, 255, 255, 0.05)",
                borderRadius: "10px",
                padding: "3px",
                border: "1px solid rgba(255, 255, 255, 0.08)",
              }}
            >
              <button
                type="button"
                onClick={() => setViewMode("grid")}
                style={{
                  padding: "6px 10px",
                  borderRadius: "8px",
                  background: viewMode === "grid" ? "#0EA5E9" : "transparent",
                  color: viewMode === "grid" ? "#FFFFFF" : "#94A3B8",
                  border: "none",
                  cursor: "pointer",
                  display: "flex",
                  alignItems: "center",
                }}
              >
                <LayoutGrid size={16} />
              </button>
              <button
                type="button"
                onClick={() => setViewMode("list")}
                style={{
                  padding: "6px 10px",
                  borderRadius: "8px",
                  background: viewMode === "list" ? "#0EA5E9" : "transparent",
                  color: viewMode === "list" ? "#FFFFFF" : "#94A3B8",
                  border: "none",
                  cursor: "pointer",
                  display: "flex",
                  alignItems: "center",
                }}
              >
                <List size={16} />
              </button>
            </div>
          </div>
        </div>
      </GlassCard>

      {/* TRIPS CONTENT */}
      {loading ? (
        <div style={{ textAlign: "center", padding: "60px" }}>
          <p style={{ color: "#94A3B8" }}>Loading travel archive...</p>
        </div>
      ) : filteredTrips.length > 0 ? (
        viewMode === "grid" ? (
          /* GRID CARDS VIEW */
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))",
              gap: "24px",
            }}
          >
            {filteredTrips.map((trip, idx) => {
              const img =
                DESTINATION_IMAGES[trip.destination] ||
                "/destinations/munnar.jpg";
              return (
                <div
                  key={trip.id || idx}
                  className="glass-card-interactive"
                  onClick={() => handleOpenTrip(trip)}
                  style={{
                    borderRadius: "20px",
                    overflow: "hidden",
                    display: "flex",
                    flexDirection: "column",
                  }}
                >
                  <div
                    style={{
                      position: "relative",
                      height: "180px",
                      width: "100%",
                    }}
                  >
                    <Image
                      src={img}
                      alt={trip.destination}
                      fill
                      sizes="(max-width: 768px) 100vw, 33vw"
                      style={{ objectFit: "cover" }}
                    />
                    <div
                      style={{
                        position: "absolute",
                        inset: 0,
                        background:
                          "linear-gradient(to top, rgba(3, 7, 18, 0.9) 0%, transparent 60%)",
                      }}
                    />
                    <div
                      style={{
                        position: "absolute",
                        top: "12px",
                        right: "12px",
                      }}
                    >
                      {trip.sustainability_score !== undefined && (
                        <Badge variant="eco" size="sm">
                          {trip.sustainability_score}/100 Eco
                        </Badge>
                      )}
                    </div>
                    <div
                      style={{
                        position: "absolute",
                        bottom: "12px",
                        left: "16px",
                        right: "16px",
                      }}
                    >
                      <h3
                        style={{
                          fontSize: "1.25rem",
                          fontWeight: 800,
                          color: "#FFFFFF",
                        }}
                      >
                        {trip.trip_title || `${trip.destination} Trip`}
                      </h3>
                      <p
                        style={{
                          color: "#CBD5E1",
                          fontSize: "0.82rem",
                          display: "flex",
                          alignItems: "center",
                          gap: "4px",
                        }}
                      >
                        <MapPin size={12} color="#38BDF8" /> {trip.destination}
                      </p>
                    </div>
                  </div>

                  <div
                    style={{
                      padding: "18px",
                      display: "flex",
                      flexDirection: "column",
                      gap: "14px",
                      flex: 1,
                      justifyContent: "space-between",
                    }}
                  >
                    <div
                      style={{
                        display: "flex",
                        justifyContent: "space-between",
                        fontSize: "0.85rem",
                        color: "#CBD5E1",
                      }}
                    >
                      <span>📅 {trip.duration_days} Days</span>
                      <span>💰 ₹{trip.budget.toLocaleString()}</span>
                      <span>🚗 {trip.transportation_mode || "Car"}</span>
                    </div>

                    <div
                      style={{
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "center",
                        borderTop: "1px solid rgba(255, 255, 255, 0.08)",
                        paddingTop: "12px",
                      }}
                    >
                      <span
                        style={{
                          fontSize: "0.82rem",
                          color: "#38BDF8",
                          fontWeight: 600,
                          display: "flex",
                          alignItems: "center",
                          gap: "4px",
                        }}
                      >
                        <Eye size={14} /> Open Itinerary
                      </span>
                      <button
                        type="button"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleDelete(trip.id, idx);
                        }}
                        title="Delete from archive"
                        style={{
                          background: "transparent",
                          border: "none",
                          color: "#F87171",
                          cursor: "pointer",
                          padding: "4px",
                        }}
                      >
                        <Trash2 size={16} />
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        ) : (
          /* COMPACT LIST VIEW */
          <GlassCard style={{ padding: "10px", overflowX: "auto" }}>
            <table
              style={{
                width: "100%",
                borderCollapse: "collapse",
                textAlign: "left",
                fontSize: "0.9rem",
              }}
            >
              <thead>
                <tr
                  style={{
                    borderBottom: "1px solid rgba(255, 255, 255, 0.10)",
                    color: "#94A3B8",
                  }}
                >
                  <th style={{ padding: "14px 16px" }}>Trip Title</th>
                  <th style={{ padding: "14px 16px" }}>Destination</th>
                  <th style={{ padding: "14px 16px" }}>Duration</th>
                  <th style={{ padding: "14px 16px" }}>Budget</th>
                  <th style={{ padding: "14px 16px" }}>Eco Score</th>
                  <th style={{ padding: "14px 16px", textAlign: "right" }}>
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody>
                {filteredTrips.map((trip, idx) => (
                  <tr
                    key={trip.id || idx}
                    style={{
                      borderBottom: "1px solid rgba(255, 255, 255, 0.05)",
                      cursor: "pointer",
                      transition: "background 0.2s",
                    }}
                    onClick={() => handleOpenTrip(trip)}
                  >
                    <td
                      style={{
                        padding: "14px 16px",
                        fontWeight: 700,
                        color: "#FFFFFF",
                      }}
                    >
                      {trip.trip_title || `${trip.destination} Expedition`}
                    </td>
                    <td style={{ padding: "14px 16px", color: "#CBD5E1" }}>
                      {trip.destination}
                    </td>
                    <td style={{ padding: "14px 16px", color: "#CBD5E1" }}>
                      {trip.duration_days} Days
                    </td>
                    <td
                      style={{
                        padding: "14px 16px",
                        color: "#34D399",
                        fontWeight: 600,
                      }}
                    >
                      ₹{trip.budget.toLocaleString()}
                    </td>
                    <td style={{ padding: "14px 16px" }}>
                      <Badge variant="eco" size="sm">
                        {trip.sustainability_score ?? 80}/100
                      </Badge>
                    </td>
                    <td style={{ padding: "14px 16px", textAlign: "right" }}>
                      <button
                        type="button"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleDelete(trip.id, idx);
                        }}
                        style={{
                          background: "transparent",
                          border: "none",
                          color: "#F87171",
                          cursor: "pointer",
                        }}
                      >
                        <Trash2 size={16} />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </GlassCard>
        )
      ) : (
        /* EMPTY STATE */
        <GlassCard style={{ padding: "60px 20px", textAlign: "center" }}>
          <div
            style={{
              width: "56px",
              height: "56px",
              borderRadius: "18px",
              background: "rgba(14, 165, 233, 0.12)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              margin: "0 auto 16px auto",
              color: "#38BDF8",
            }}
          >
            <Sparkles size={24} />
          </div>
          <h3
            style={{
              fontSize: "1.4rem",
              fontWeight: 800,
              color: "#FFFFFF",
              marginBottom: "8px",
            }}
          >
            No Itineraries in Your Archive
          </h3>
          <p
            style={{
              color: "#94A3B8",
              maxWidth: "460px",
              margin: "0 auto 24px auto",
              lineHeight: 1.6,
            }}
          >
            Generate your first intelligent trip plan with weather alerts,
            curated hotels, and dining recommendations.
          </p>
          <Link href="/planner" style={{ textDecoration: "none" }}>
            <Button variant="primary" size="md" leftIcon={<Plus size={16} />}>
              Launch AI Travel Studio
            </Button>
          </Link>
        </GlassCard>
      )}
    </div>
  );
}
