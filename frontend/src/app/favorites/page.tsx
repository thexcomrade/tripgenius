"use client";

import { useEffect, useMemo, useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  Heart,
  Search,
  Compass,
  Sparkles,
  Trash2,
  ArrowRight,
  MapPin,
  Calendar,
  DollarSign,
  Leaf,
} from "lucide-react";
import Button from "../../components/ui/Button";
import Badge from "../../components/ui/Badge";
import { GlassCard, SectionHeader } from "../../components/ui/Card";
import tripService from "../../services/trip.service";

interface FavoriteTrip {
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
  favorite_at?: string;
  sustainability_score?: number;
  status?: string;
  is_favorite?: boolean;
}

const DESTINATION_IMAGES: Record<string, string> = {
  Munnar: "/destinations/munnar.jpg",
  Varkala: "/destinations/varkala.jpg",
  Ooty: "/destinations/ooty.jpg",
  Kodaikanal: "/destinations/kodaikanal.jpg",
  Mysore: "/destinations/mysore.jpg",
  Coorg: "/destinations/coorg.jpg",
};

export default function FavoritesPage() {
  const router = useRouter();

  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [favoriteTrips, setFavoriteTrips] = useState<FavoriteTrip[]>([]);

  useEffect(() => {
    async function loadFavorites() {
      const token = localStorage.getItem("tripgenius_token");
      if (token) {
        try {
          const data = await tripService.getHistory();
          if (data && data.trips) {
            const favorites = data.trips.filter(
              (t: FavoriteTrip) => t.is_favorite,
            );
            if (favorites.length > 0) {
              setFavoriteTrips(favorites);
              setLoading(false);
              return;
            }
          }
        } catch {
          // ignore
        }
      }

      // Fallback to local storage
      try {
        const stored = localStorage.getItem("favorite_trips");
        if (stored) {
          setFavoriteTrips(JSON.parse(stored));
        }
      } catch {
        // ignore
      }
      setLoading(false);
    }

    loadFavorites();
  }, []);

  const removeFavorite = (destName: string, id?: string) => {
    const updated = favoriteTrips.filter((t) =>
      id ? t.id !== id : t.destination !== destName,
    );
    setFavoriteTrips(updated);
    localStorage.setItem("favorite_trips", JSON.stringify(updated));
  };

  const filteredTrips = useMemo(() => {
    return favoriteTrips.filter((trip) => {
      const dest = (trip.destination || "").toLowerCase();
      const title = (trip.trip_title || "").toLowerCase();
      const style = (trip.travel_style || "").toLowerCase();
      const q = search.toLowerCase();
      return dest.includes(q) || title.includes(q) || style.includes(q);
    });
  }, [favoriteTrips, search]);

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
            <Badge
              variant="amber"
              size="sm"
              icon={<Heart size={12} fill="#FBBF24" />}
            >
              Saved Bucket List
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
            Favorite Escapes ({favoriteTrips.length})
          </h1>
          <p
            style={{ color: "#94A3B8", fontSize: "0.95rem", marginTop: "4px" }}
          >
            Handpicked sanctuaries and custom itineraries you have pinned for
            upcoming journeys.
          </p>
        </div>

        <Link href="/explore" style={{ textDecoration: "none" }}>
          <Button
            variant="secondary"
            size="md"
            leftIcon={<Compass size={16} />}
          >
            Explore More Destinations
          </Button>
        </Link>
      </div>

      {/* SEARCH BAR */}
      {favoriteTrips.length > 0 && (
        <GlassCard style={{ padding: "14px 20px" }}>
          <div style={{ position: "relative", maxWidth: "460px" }}>
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
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Filter saved bucket list..."
              className="input-base"
              style={{
                paddingLeft: "40px",
                paddingRight: "14px",
                height: "42px",
              }}
            />
          </div>
        </GlassCard>
      )}

      {/* FAVORITES GRID */}
      {loading ? (
        <div style={{ textAlign: "center", padding: "60px" }}>
          <p style={{ color: "#94A3B8" }}>Loading favorites...</p>
        </div>
      ) : filteredTrips.length > 0 ? (
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
                onClick={() =>
                  router.push(
                    `/planner?destination=${encodeURIComponent(trip.destination)}`,
                  )
                }
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
                    height: "200px",
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

                  {/* REMOVE FAVORITE BUTTON */}
                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation();
                      removeFavorite(trip.destination, trip.id);
                    }}
                    title="Remove from favorites"
                    style={{
                      position: "absolute",
                      top: "14px",
                      right: "14px",
                      width: "36px",
                      height: "36px",
                      borderRadius: "50%",
                      background: "rgba(0, 0, 0, 0.60)",
                      backdropFilter: "blur(10px)",
                      border: "1px solid rgba(255, 255, 255, 0.20)",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      cursor: "pointer",
                      color: "#EF4444",
                    }}
                  >
                    <Heart size={16} fill="#EF4444" />
                  </button>

                  <div
                    style={{
                      position: "absolute",
                      bottom: "14px",
                      left: "18px",
                      right: "18px",
                    }}
                  >
                    <h3
                      style={{
                        fontSize: "1.35rem",
                        fontWeight: 800,
                        color: "#FFFFFF",
                      }}
                    >
                      {trip.destination}
                    </h3>
                    <p style={{ color: "#CBD5E1", fontSize: "0.82rem" }}>
                      {trip.travel_style || "Scenic Getaway"}
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
                  </div>

                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "space-between",
                      color: "#38BDF8",
                      fontSize: "0.88rem",
                      fontWeight: 600,
                      borderTop: "1px solid rgba(255, 255, 255, 0.08)",
                      paddingTop: "12px",
                    }}
                  >
                    <span>Plan Itinerary Now</span>
                    <ArrowRight size={15} />
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        /* EMPTY STATE */
        <GlassCard style={{ padding: "60px 20px", textAlign: "center" }}>
          <div
            style={{
              width: "56px",
              height: "56px",
              borderRadius: "18px",
              background: "rgba(245, 158, 11, 0.12)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              margin: "0 auto 16px auto",
              color: "#FBBF24",
            }}
          >
            <Heart size={24} />
          </div>
          <h3
            style={{
              fontSize: "1.4rem",
              fontWeight: 800,
              color: "#FFFFFF",
              marginBottom: "8px",
            }}
          >
            Your Bucket List is Empty
          </h3>
          <p
            style={{
              color: "#94A3B8",
              maxWidth: "460px",
              margin: "0 auto 24px auto",
              lineHeight: 1.6,
            }}
          >
            Explore curated destinations and tap the heart icon on any sanctuary
            to save it for quick itinerary planning.
          </p>
          <Link href="/explore" style={{ textDecoration: "none" }}>
            <Button
              variant="primary"
              size="md"
              leftIcon={<Compass size={16} />}
            >
              Discover Destinations
            </Button>
          </Link>
        </GlassCard>
      )}
    </div>
  );
}
