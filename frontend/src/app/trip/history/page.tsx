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
  CheckSquare,
  Square,
} from "lucide-react";
import toast from "react-hot-toast";
import Button from "../../../components/ui/Button";
import Badge from "../../../components/ui/Badge";
import { GlassCard, SectionHeader } from "../../../components/ui/Card";
import tripService from "../../../services/trip.service";
import {
  ensureTripItinerary,
  getDestinationImage,
} from "../../../utils/itineraryHelper";

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
  ai_itinerary?: any;
  attractions?: string[];
  recommended_hotels?: string[];
  recommended_restaurants?: string[];
  local_cuisines?: string[];
  weather_summary?: any;
  packing_checklist?: string[];
  travel_tips?: string[];
}

const DESTINATION_IMAGES: Record<string, string> = {
  Munnar: "/destinations/munnar.jpg",
  Varkala: "/destinations/varkala.jpg",
  Ooty: "/destinations/ooty.jpg",
  Kodaikanal: "/destinations/kodaikanal.jpg",
  Mysore: "/destinations/mysore.jpg",
  Coorg: "/destinations/coorg.jpg",
  Hampi: "/destinations/hampi.jpg",
  Gokarna: "/destinations/gokarna.jpg",
  Thekkady: "/destinations/thekkady.jpg",
  Kovalam: "/destinations/kovalam.jpg",
  Alleppey: "/destinations/alleppey.jpg",
  Wayanad: "/destinations/wayanad.jpg",
  Paris: "/destinations/paris.jpg",
  Tokyo: "/destinations/tokyo.jpg",
  Bali: "/destinations/bali.jpg",
  Dubai: "/destinations/dubai.jpg",
};

export default function TripHistoryPage() {
  const router = useRouter();

  const [loading, setLoading] = useState(true);
  const [trips, setTrips] = useState<SavedTrip[]>([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [sortBy, setSortBy] = useState("Newest");
  const [viewMode, setViewMode] = useState<"grid" | "list">("grid");
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [isDeleting, setIsDeleting] = useState(false);

  useEffect(() => {
    async function loadHistory() {
      const token = localStorage.getItem("tripgenius_token");
      let backendList: SavedTrip[] = [];
      if (token) {
        try {
          const data = await tripService.getHistory();
          if (data && data.trips && data.trips.length > 0) {
            backendList = data.trips.map((t: SavedTrip) => ({
              ...t,
              saved_at: t.created_at,
            }));
          }
        } catch {
          // ignore backend failure, fallback to localStorage
        }
      }

      // Merge with localStorage sources of truth so morning/afternoon/evening plans are never lost
      try {
        const localSaved: SavedTrip[] = JSON.parse(
          localStorage.getItem("saved_trips") ||
            localStorage.getItem("tripgenius_saved_trips") ||
            "[]"
        );
        if (backendList.length === 0) {
          setTrips(localSaved.map((t) => ensureTripItinerary(t)));
        } else {
          const merged = backendList.map((bt) => {
            const localMatch = localSaved.find(
              (lt) =>
                lt.id === bt.id ||
                (lt.destination?.toLowerCase() === bt.destination.toLowerCase() &&
                  lt.duration_days === bt.duration_days)
            );
            const base = localMatch ? { ...localMatch, ...bt } : { ...bt };
            if (
              Array.isArray(localMatch?.ai_itinerary) &&
              localMatch.ai_itinerary.length > 0 &&
              (!Array.isArray(bt?.ai_itinerary) || bt.ai_itinerary.length === 0)
            ) {
              base.ai_itinerary = localMatch.ai_itinerary;
            }
            return ensureTripItinerary(base);
          });
          setTrips(merged);
        }
      } catch {
        setTrips(backendList.map((t) => ensureTripItinerary(t)));
      }
      setLoading(false);
    }

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
    localStorage.setItem("trip_history", JSON.stringify(updated));
    toast.success("Trip removed from archive");
  };

  const handleOpenTrip = async (trip: SavedTrip) => {
    let fullTrip: any = { ...trip };

    // Check localStorage (saved_trips & tripgenius_saved_trips) for rich DayPlan morning/afternoon/evening schedule
    try {
      const localProfiles = JSON.parse(
        localStorage.getItem("tripgenius_saved_trips") || "[]"
      );
      const localHistory = JSON.parse(
        localStorage.getItem("saved_trips") || "[]"
      );
      const combined = [...localProfiles, ...localHistory];
      const match = combined.find(
        (t: any) =>
          (trip.id && t.id === trip.id) ||
          (t.destination?.toLowerCase() === trip.destination.toLowerCase() &&
            t.duration_days === trip.duration_days &&
            Array.isArray(t.ai_itinerary) &&
            t.ai_itinerary.length > 0)
      );
      if (match && Array.isArray(match.ai_itinerary) && match.ai_itinerary.length > 0) {
        fullTrip = { ...match, ...trip, ai_itinerary: match.ai_itinerary };
      }
    } catch {}

    // If ai_itinerary is still not populated and trip has a backend ID, fetch complete record
    if (
      (!fullTrip.ai_itinerary ||
        (Array.isArray(fullTrip.ai_itinerary) &&
          fullTrip.ai_itinerary.length === 0)) &&
      trip.id &&
      !trip.id.startsWith("tg-")
    ) {
      try {
        const backendRecord = await tripService.getTrip(trip.id);
        if (backendRecord && backendRecord.ai_itinerary) {
          fullTrip = { ...fullTrip, ...backendRecord };
        }
      } catch (err) {
        console.warn("Could not fetch full trip details:", err);
      }
    }

    // Guarantee full Morning, Afternoon, Evening, and Key Stops itinerary is present
    fullTrip = ensureTripItinerary(fullTrip);

    localStorage.setItem("latest_trip", JSON.stringify(fullTrip));
    localStorage.setItem("tripgenius_generated_trip", JSON.stringify(fullTrip));
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
        return matchQuery;
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
  }, [trips, searchQuery, sortBy]);

  const getTripKey = (trip: SavedTrip, idx: number) =>
    trip.id || `trip-${idx}-${trip.destination}-${trip.created_at || ""}`;

  const isAllSelected =
    filteredTrips.length > 0 &&
    filteredTrips.every((t, i) => selectedIds.includes(getTripKey(t, i)));

  const handleToggleSelectAll = () => {
    if (isAllSelected) {
      setSelectedIds([]);
    } else {
      setSelectedIds(filteredTrips.map((t, i) => getTripKey(t, i)));
    }
  };

  const handleToggleSelect = (key: string) => {
    setSelectedIds((prev) =>
      prev.includes(key) ? prev.filter((id) => id !== key) : [...prev, key]
    );
  };

  const handleBulkDelete = async () => {
    if (selectedIds.length === 0) return;
    const count = selectedIds.length;
    const isAll = count === trips.length;
    const confirmMsg = isAll
      ? `Are you sure you want to delete ALL ${count} trips from your archive? This cannot be undone.`
      : `Are you sure you want to delete ${count} selected trip(s) from your archive?`;

    if (!confirm(confirmMsg)) return;

    setIsDeleting(true);
    try {
      if (isAll) {
        try {
          await tripService.deleteAllTrips();
        } catch {
          // ignore
        }
        setTrips([]);
        setSelectedIds([]);
        localStorage.removeItem("saved_trips");
        localStorage.removeItem("trip_history");
        toast.success(`All ${count} trips deleted from archive!`);
      } else {
        const backendIds = trips
          .filter((t, i) => selectedIds.includes(getTripKey(t, i)) && t.id)
          .map((t) => t.id as string);

        if (backendIds.length > 0) {
          try {
            await tripService.bulkDeleteTrips(backendIds);
          } catch {
            await Promise.allSettled(
              backendIds.map((id) => tripService.deleteTrip(id))
            );
          }
        }

        const remaining = trips.filter(
          (t, i) => !selectedIds.includes(getTripKey(t, i))
        );
        setTrips(remaining);
        setSelectedIds([]);
        localStorage.setItem("saved_trips", JSON.stringify(remaining));
        localStorage.setItem("trip_history", JSON.stringify(remaining));
        toast.success(`${count} trip(s) deleted successfully!`);
      }
    } catch {
      toast.error("Failed to delete selected trips. Please try again.");
    } finally {
      setIsDeleting(false);
    }
  };

  return (
    <div
      className="page-container"
      style={{
        display: "flex",
        flexDirection: "column",
        gap: "32px",
        position: "relative",
      }}
    >
      {/* AMBIENT GLOW BACKDROP */}
      <div
        aria-hidden="true"
        style={{
          position: "fixed",
          inset: 0,
          pointerEvents: "none",
          zIndex: 0,
          background:
            "radial-gradient(ellipse 80% 50% at 20% -10%, rgba(14, 165, 233, 0.16), transparent 70%), " +
            "radial-gradient(ellipse 60% 40% at 85% 25%, rgba(20, 184, 166, 0.13), transparent 60%), " +
            "radial-gradient(ellipse 80% 60% at 50% 100%, rgba(14, 165, 233, 0.10), transparent 70%)",
        }}
      />
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

      {/* CONTROLS BAR: SELECT ALL, DELETE, SEARCH, FILTERS, SORT, VIEW */}
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
          {/* LEFT CONTROLS: SELECT ALL + DELETE BUTTON + SEARCH */}
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "14px",
              flex: 1,
              flexWrap: "wrap",
              minWidth: "280px",
            }}
          >
            {/* SELECT ALL & DELETE OPTION (MATCHING USER'S SKETCH) */}
            <div
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: "10px",
                paddingRight: "14px",
                borderRight: "1px solid rgba(255, 255, 255, 0.12)",
              }}
            >
              <label
                style={{
                  display: "inline-flex",
                  alignItems: "center",
                  gap: "8px",
                  cursor: "pointer",
                  userSelect: "none",
                  fontSize: "0.88rem",
                  fontWeight: 600,
                  color: isAllSelected ? "#38BDF8" : "#94A3B8",
                }}
                title={isAllSelected ? "Deselect All" : "Select All"}
              >
                <input
                  type="checkbox"
                  checked={isAllSelected}
                  onChange={handleToggleSelectAll}
                  style={{
                    width: "18px",
                    height: "18px",
                    cursor: "pointer",
                    accentColor: "#0EA5E9",
                    borderRadius: "4px",
                  }}
                />
                <span>Select All</span>
              </label>

              <button
                type="button"
                onClick={handleBulkDelete}
                disabled={selectedIds.length === 0 || isDeleting}
                style={{
                  display: "inline-flex",
                  alignItems: "center",
                  gap: "6px",
                  padding: "8px 14px",
                  borderRadius: "10px",
                  fontSize: "0.85rem",
                  fontWeight: 700,
                  background:
                    selectedIds.length > 0
                      ? "rgba(239, 68, 68, 0.22)"
                      : "rgba(255, 255, 255, 0.04)",
                  border:
                    selectedIds.length > 0
                      ? "1px solid rgba(239, 68, 68, 0.55)"
                      : "1px solid rgba(255, 255, 255, 0.08)",
                  color: selectedIds.length > 0 ? "#FCA5A5" : "#64748B",
                  cursor:
                    selectedIds.length > 0 && !isDeleting
                      ? "pointer"
                      : "not-allowed",
                  transition: "all 0.15s ease",
                }}
                title={
                  selectedIds.length > 0
                    ? `Delete ${selectedIds.length} selected trip(s)`
                    : "Select trips to delete"
                }
              >
                <Trash2 size={15} />
                <span>
                  {isDeleting
                    ? "Deleting..."
                    : `Delete${selectedIds.length > 0 ? ` (${selectedIds.length})` : ""}`}
                </span>
              </button>
            </div>

            {/* SEARCH */}
            <div
              style={{
                position: "relative",
                minWidth: "220px",
                flex: 1,
                maxWidth: "380px",
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
          </div>

          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "12px",
              flexWrap: "wrap",
            }}
          >


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
          <div className="grid-3-col">
            {filteredTrips.map((trip, idx) => {
              const img = getDestinationImage(trip.destination);
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
                    {/* CARD SELECT CHECKBOX */}
                    <div
                      style={{
                        position: "absolute",
                        top: "12px",
                        left: "12px",
                        zIndex: 10,
                        background: "rgba(15, 23, 42, 0.75)",
                        borderRadius: "6px",
                        padding: "4px",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                      }}
                      onClick={(e) => e.stopPropagation()}
                    >
                      <input
                        type="checkbox"
                        checked={selectedIds.includes(getTripKey(trip, idx))}
                        onChange={() => handleToggleSelect(getTripKey(trip, idx))}
                        style={{
                          width: "18px",
                          height: "18px",
                          cursor: "pointer",
                          accentColor: "#0EA5E9",
                          borderRadius: "4px",
                        }}
                      />
                    </div>
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
                  <th style={{ padding: "14px 16px", width: "44px" }}>
                    <input
                      type="checkbox"
                      checked={isAllSelected}
                      onChange={handleToggleSelectAll}
                      style={{
                        width: "17px",
                        height: "17px",
                        cursor: "pointer",
                        accentColor: "#0EA5E9",
                      }}
                      title={isAllSelected ? "Deselect All" : "Select All"}
                    />
                  </th>
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
                {filteredTrips.map((trip, idx) => {
                  const tripKey = getTripKey(trip, idx);
                  const isSelected = selectedIds.includes(tripKey);
                  return (
                    <tr
                      key={tripKey}
                      style={{
                        borderBottom: "1px solid rgba(255, 255, 255, 0.05)",
                        background: isSelected
                          ? "rgba(14, 165, 233, 0.09)"
                          : "transparent",
                        cursor: "pointer",
                        transition: "background 0.2s",
                      }}
                      onClick={() => handleOpenTrip(trip)}
                    >
                      <td
                        style={{ padding: "14px 16px", width: "44px" }}
                        onClick={(e) => e.stopPropagation()}
                      >
                        <input
                          type="checkbox"
                          checked={isSelected}
                          onChange={() => handleToggleSelect(tripKey)}
                          style={{
                            width: "17px",
                            height: "17px",
                            cursor: "pointer",
                            accentColor: "#0EA5E9",
                          }}
                        />
                      </td>
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
                          title="Delete trip"
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
                  );
                })}
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
