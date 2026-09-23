"use client";

import { useMemo, useState, useEffect } from "react";
import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  Search,
  MapPin,
  Star,
  Compass,
  Sparkles,
  Heart,
  ArrowRight,
  Leaf,
  Calendar,
  DollarSign,
} from "lucide-react";
import Button from "../../components/ui/Button";
import Badge from "../../components/ui/Badge";
import { GlassCard, SectionHeader } from "../../components/ui/Card";

interface DestinationItem {
  id: number;
  name: string;
  location: string;
  image: string;
  category: string;
  description: string;
  rating: number;
  season: string;
  budgetEst: string;
  featured?: boolean;
}

const DESTINATIONS: DestinationItem[] = [
  {
    id: 1,
    name: "Munnar",
    location: "Kerala, India",
    image: "/destinations/munnar.jpg",
    category: "Hill Stations",
    description:
      "Rolling emerald tea plantations, cool misty mornings, and majestic peaks.",
    rating: 4.9,
    season: "Sep – Mar",
    budgetEst: "₹12,000",
    featured: true,
  },
  {
    id: 2,
    name: "Varkala",
    location: "Kerala, India",
    image: "/destinations/varkala.jpg",
    category: "Beaches",
    description:
      "Stunning cliffside red rocks overlooking the Arabian Sea with laid-back beach cafes.",
    rating: 4.8,
    season: "Oct – Apr",
    budgetEst: "₹10,000",
  },
  {
    id: 3,
    name: "Alleppey",
    location: "Kerala, India",
    image: "/destinations/alleppey.jpg",
    category: "Backwaters",
    description:
      "Slow, tranquil backwaters and luxury traditional houseboats through palm canopies.",
    rating: 4.9,
    season: "Nov – Feb",
    budgetEst: "₹15,000",
  },
  {
    id: 4,
    name: "Wayanad",
    location: "Kerala, India",
    image: "/destinations/wayanad.jpg",
    category: "Nature & Wildlife",
    description:
      "Lush Western Ghats rainforests, historic caves, cascading waterfalls, and treehouses.",
    rating: 4.8,
    season: "Oct – May",
    budgetEst: "₹11,000",
  },
  {
    id: 5,
    name: "Ooty",
    location: "Tamil Nadu, India",
    image: "/destinations/ooty.jpg",
    category: "Hill Stations",
    description:
      "Classic Nilgiri mountain railway, botanical gardens, and pine-clad hills.",
    rating: 4.8,
    season: "All Year",
    budgetEst: "₹12,500",
  },
  {
    id: 6,
    name: "Kodaikanal",
    location: "Tamil Nadu, India",
    image: "/destinations/kodaikanal.jpg",
    category: "Hill Stations",
    description:
      "Serene mountain lakes, walking trails, Pillar Rocks, and pine forests.",
    rating: 4.7,
    season: "Sep – May",
    budgetEst: "₹10,500",
  },
  {
    id: 7,
    name: "Mysore",
    location: "Karnataka, India",
    image: "/destinations/mysore.jpg",
    category: "Heritage & Royal",
    description:
      "Magnificent illuminated royal palaces, sandalwood scents, and historic silk bazaars.",
    rating: 4.9,
    season: "Oct – Mar",
    budgetEst: "₹9,000",
  },
  {
    id: 8,
    name: "Coorg",
    location: "Karnataka, India",
    image: "/destinations/coorg.jpg",
    category: "Nature & Wildlife",
    description:
      "Aromatic coffee and spice plantations, misty abbey waterfalls, and estate stays.",
    rating: 4.9,
    season: "Oct – Apr",
    budgetEst: "₹13,500",
    featured: true,
  },
  {
    id: 9,
    name: "Hampi",
    location: "Karnataka, India",
    image: "/destinations/hampi.jpg",
    category: "Heritage & Royal",
    description:
      "Breathtaking boulder-strewn landscape with ancient Vijayanagara ruins and stone chariot temples.",
    rating: 4.8,
    season: "Nov – Feb",
    budgetEst: "₹9,500",
  },
  {
    id: 10,
    name: "Gokarna",
    location: "Karnataka, India",
    image: "/destinations/gokarna.jpg",
    category: "Beaches",
    description:
      "Untouched crescent beaches, Om beach trekking, and spiritual coastal sanctuaries.",
    rating: 4.7,
    season: "Oct – Mar",
    budgetEst: "₹8,500",
  },
  {
    id: 11,
    name: "Thekkady",
    location: "Kerala, India",
    image: "/destinations/thekkady.jpg",
    category: "Nature & Wildlife",
    description:
      "Periyar National Park boat safaris, spice gardens, and wild elephant reserves.",
    rating: 4.8,
    season: "Sep – Mar",
    budgetEst: "₹7,500",
  },
  {
    id: 12,
    name: "Kovalam",
    location: "Kerala, India",
    image: "/destinations/kovalam.jpg",
    category: "Beaches",
    description:
      "Iconic lighthouse beach with golden sands, shallow waters, and seaside ayurvedic retreats.",
    rating: 4.7,
    season: "Nov – Mar",
    budgetEst: "₹10,500",
  },
  {
    id: 13,
    name: "Paris",
    location: "Île-de-France, France",
    image: "/destinations/paris.jpg",
    category: "International / Abroad",
    description:
      "The City of Light — illuminated Eiffel Tower, Seine river cruises, world-class art, and bistros.",
    rating: 4.9,
    season: "Apr – Oct",
    budgetEst: "₹65,000",
    featured: true,
  },
  {
    id: 14,
    name: "Tokyo",
    location: "Kanto, Japan",
    image: "/destinations/tokyo.jpg",
    category: "International / Abroad",
    description:
      "Futuristic metropolis meets ancient Edo culture — Senso-ji temple, cherry blossoms, and neon culinary lanes.",
    rating: 4.9,
    season: "Mar – May / Sep – Nov",
    budgetEst: "₹75,000",
    featured: true,
  },
  {
    id: 15,
    name: "Bali",
    location: "Lesser Sunda, Indonesia",
    image: "/destinations/bali.jpg",
    category: "International / Abroad",
    description:
      "Island of the Gods — dramatic Tanah Lot sea temples, lush jungle terraces, and tropical surf retreats.",
    rating: 4.8,
    season: "Apr – Oct",
    budgetEst: "₹38,000",
  },
  {
    id: 16,
    name: "Dubai",
    location: "Dubai, United Arab Emirates",
    image: "/destinations/dubai.jpg",
    category: "International / Abroad",
    description:
      "Futuristic architectural marvels — soaring Burj Khalifa, desert luxury safaris, and illuminated yacht marinas.",
    rating: 4.8,
    season: "Nov – Mar",
    budgetEst: "₹45,000",
  },
];

const CATEGORIES = [
  "All Escapes",
  "Hill Stations",
  "Beaches",
  "Backwaters",
  "Heritage & Royal",
  "Nature & Wildlife",
  "International / Abroad",
];

export default function ExplorePage() {
  const router = useRouter();

  const [search, setSearch] = useState("");
  const [activeCategory, setActiveCategory] = useState("All Escapes");
  const [favorites, setFavorites] = useState<string[]>([]);

  useEffect(() => {
    try {
      const stored = localStorage.getItem("favorite_trips");
      if (stored) {
        const parsed = JSON.parse(stored);
        setFavorites(parsed.map((f: any) => f.destination));
      }
    } catch {
      // ignore
    }
  }, []);

  const toggleFavorite = (dest: DestinationItem, e: React.MouseEvent) => {
    e.stopPropagation();
    let updated: string[];
    let storedList: any[] = [];
    try {
      storedList = JSON.parse(localStorage.getItem("favorite_trips") || "[]");
    } catch {
      storedList = [];
    }

    if (favorites.includes(dest.name)) {
      updated = favorites.filter((name) => name !== dest.name);
      storedList = storedList.filter((item) => item.destination !== dest.name);
    } else {
      updated = [...favorites, dest.name];
      storedList.push({
        destination: dest.name,
        duration_days: 3,
        budget: parseInt(dest.budgetEst.replace(/[^\d]/g, ""), 10) || 10000,
        travelers_count: 2,
        travel_style: "Leisure",
        transportation_mode: "Car",
        preferred_accommodation: "Hotel",
        interests: [dest.category],
        saved_at: new Date().toISOString(),
        favorite_at: new Date().toISOString(),
        is_favorite: true,
      });
    }

    setFavorites(updated);
    localStorage.setItem("favorite_trips", JSON.stringify(storedList));
  };

  const filteredDestinations = useMemo(() => {
    return DESTINATIONS.filter((item) => {
      const matchesSearch =
        item.name.toLowerCase().includes(search.toLowerCase()) ||
        item.location.toLowerCase().includes(search.toLowerCase()) ||
        item.description.toLowerCase().includes(search.toLowerCase());

      const matchesCategory =
        activeCategory === "All Escapes" || item.category === activeCategory;

      return matchesSearch && matchesCategory;
    });
  }, [search, activeCategory]);

  const spotlight = DESTINATIONS[0];

  return (
    <div
      className="page-container"
      style={{ display: "flex", flexDirection: "column", gap: "36px" }}
    >
      {/* SPOTLIGHT DESTINATION BANNER */}
      <section
        style={{
          position: "relative",
          borderRadius: "28px",
          overflow: "hidden",
          border: "1px solid rgba(255, 255, 255, 0.10)",
          boxShadow: "0 16px 48px rgba(0, 0, 0, 0.40)",
        }}
      >
        <div style={{ position: "relative", height: "360px", width: "100%" }}>
          <Image
            src={spotlight.image}
            alt={spotlight.name}
            fill
            priority
            style={{ objectFit: "cover" }}
          />
          <div
            style={{
              position: "absolute",
              inset: 0,
              background:
                "linear-gradient(to top, rgba(3, 7, 18, 0.95) 0%, rgba(3, 7, 18, 0.40) 60%, rgba(3, 7, 18, 0.15) 100%)",
            }}
          />

          <div style={{ position: "absolute", top: "24px", left: "24px" }}>
            <Badge
              variant="amber"
              size="md"
              icon={<Star size={14} fill="#FBBF24" />}
            >
              Curator&apos;s Pick of the Month
            </Badge>
          </div>

          <div
            style={{
              position: "absolute",
              bottom: "30px",
              left: "30px",
              right: "30px",
            }}
          >
            <h1
              style={{
                fontSize: "clamp(2rem, 4vw, 3.2rem)",
                fontWeight: 900,
                color: "#FFFFFF",
                letterSpacing: "-1px",
                marginBottom: "8px",
              }}
            >
              {spotlight.name} • {spotlight.location}
            </h1>
            <p
              style={{
                color: "#CBD5E1",
                fontSize: "1.05rem",
                maxWidth: "700px",
                lineHeight: 1.6,
                marginBottom: "20px",
              }}
            >
              {spotlight.description}
            </p>
            <div
              style={{
                display: "flex",
                gap: "12px",
                alignItems: "center",
                flexWrap: "wrap",
              }}
            >
              <Button
                variant="primary"
                size="md"
                leftIcon={<Sparkles size={16} />}
                onClick={() =>
                  router.push(
                    `/planner?destination=${encodeURIComponent(spotlight.name)}`,
                  )
                }
              >
                Plan Trip to {spotlight.name}
              </Button>
              <span style={{ fontSize: "0.9rem", color: "#94A3B8" }}>
                Recommended season:{" "}
                <strong style={{ color: "#FFFFFF" }}>{spotlight.season}</strong>{" "}
                • Avg Est:{" "}
                <strong style={{ color: "#34D399" }}>
                  {spotlight.budgetEst}
                </strong>
              </span>
            </div>
          </div>
        </div>
      </section>

      {/* SEARCH & CATEGORY FILTERING */}
      <section
        style={{ display: "flex", flexDirection: "column", gap: "20px" }}
      >
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
            <h2
              style={{ fontSize: "1.8rem", fontWeight: 800, color: "#FFFFFF" }}
            >
              Explore Sanctuaries ({filteredDestinations.length})
            </h2>
            <p style={{ color: "#94A3B8", fontSize: "0.92rem" }}>
              Discover curated destinations analyzed with optimal visiting
              seasons and verified regional food trails.
            </p>
          </div>

          {/* SEARCH INPUT */}
          <div style={{ position: "relative", minWidth: "280px" }}>
            <Search
              size={18}
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
              placeholder="Search city, hills, beach..."
              className="input-base"
              style={{ paddingLeft: "42px", paddingRight: "16px" }}
            />
          </div>
        </div>

        {/* CATEGORY FILTER CHIPS */}
        <div
          style={{
            display: "flex",
            gap: "8px",
            overflowX: "auto",
            paddingBottom: "6px",
          }}
        >
          {CATEGORIES.map((cat) => {
            const active = activeCategory === cat;
            return (
              <button
                key={cat}
                type="button"
                onClick={() => setActiveCategory(cat)}
                style={{
                  padding: "8px 18px",
                  borderRadius: "999px",
                  background: active
                    ? "rgba(14, 165, 233, 0.20)"
                    : "rgba(255, 255, 255, 0.04)",
                  border: active
                    ? "1px solid #38BDF8"
                    : "1px solid rgba(255, 255, 255, 0.08)",
                  color: active ? "#38BDF8" : "#CBD5E1",
                  fontSize: "0.88rem",
                  fontWeight: active ? 700 : 500,
                  cursor: "pointer",
                  whiteSpace: "nowrap",
                  transition: "all 0.2s ease",
                }}
              >
                {cat}
              </button>
            );
          })}
        </div>
      </section>

      {/* DESTINATIONS GRID */}
      <section>
        {filteredDestinations.length > 0 ? (
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))",
              gap: "24px",
            }}
          >
            {filteredDestinations.map((dest) => {
              const isFav = favorites.includes(dest.name);
              return (
                <div
                  key={dest.id}
                  className="glass-card-interactive"
                  onClick={() =>
                    router.push(
                      `/planner?destination=${encodeURIComponent(dest.name)}`,
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
                      height: "220px",
                      width: "100%",
                    }}
                  >
                    <Image
                      src={dest.image}
                      alt={dest.name}
                      fill
                      sizes="(max-width: 768px) 100vw, 33vw"
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

                    {/* CATEGORY TAG */}
                    <div
                      style={{
                        position: "absolute",
                        top: "14px",
                        left: "14px",
                      }}
                    >
                      <Badge variant="neutral" size="sm">
                        {dest.category}
                      </Badge>
                    </div>

                    {/* FAVORITE BUTTON */}
                    <button
                      type="button"
                      onClick={(e) => toggleFavorite(dest, e)}
                      title={
                        isFav
                          ? "Remove from bucket list"
                          : "Save to bucket list"
                      }
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
                        color: isFav ? "#EF4444" : "#FFFFFF",
                      }}
                    >
                      <Heart
                        size={16}
                        fill={isFav ? "#EF4444" : "transparent"}
                      />
                    </button>

                    {/* BOTTOM TITLE & RATING */}
                    <div
                      style={{
                        position: "absolute",
                        bottom: "14px",
                        left: "18px",
                        right: "18px",
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "baseline",
                      }}
                    >
                      <div>
                        <h3
                          style={{
                            fontSize: "1.4rem",
                            fontWeight: 800,
                            color: "#FFFFFF",
                          }}
                        >
                          {dest.name}
                        </h3>
                        <p style={{ color: "#CBD5E1", fontSize: "0.82rem" }}>
                          {dest.location}
                        </p>
                      </div>
                      <span
                        style={{
                          display: "flex",
                          alignItems: "center",
                          gap: "4px",
                          fontSize: "0.85rem",
                          fontWeight: 700,
                          color: "#FBBF24",
                        }}
                      >
                        <Star size={13} fill="#FBBF24" /> {dest.rating}
                      </span>
                    </div>
                  </div>

                  <div
                    style={{
                      padding: "20px",
                      display: "flex",
                      flexDirection: "column",
                      gap: "14px",
                      flex: 1,
                      justifyContent: "space-between",
                    }}
                  >
                    <p
                      style={{
                        color: "#94A3B8",
                        fontSize: "0.9rem",
                        lineHeight: 1.6,
                      }}
                    >
                      {dest.description}
                    </p>

                    <div
                      style={{
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "center",
                        fontSize: "0.85rem",
                        color: "#CBD5E1",
                        borderTop: "1px solid rgba(255, 255, 255, 0.08)",
                        paddingTop: "12px",
                      }}
                    >
                      <span>🗓️ {dest.season}</span>
                      <span>
                        Est:{" "}
                        <strong style={{ color: "#34D399" }}>
                          {dest.budgetEst}
                        </strong>
                      </span>
                    </div>

                    <div
                      style={{
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "space-between",
                        color: "#38BDF8",
                        fontSize: "0.88rem",
                        fontWeight: 600,
                      }}
                    >
                      <span>Plan AI Itinerary</span>
                      <ArrowRight size={15} />
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        ) : (
          <GlassCard style={{ padding: "60px 20px", textAlign: "center" }}>
            <h3
              style={{
                fontSize: "1.3rem",
                fontWeight: 700,
                color: "#FFFFFF",
                marginBottom: "8px",
              }}
            >
              No destinations matched &ldquo;{search}&rdquo;
            </h3>
            <p style={{ color: "#94A3B8", marginBottom: "20px" }}>
              Try searching for another city, hill station, or clear your
              category filter.
            </p>
            <Button
              variant="secondary"
              size="md"
              onClick={() => {
                setSearch("");
                setActiveCategory("All Escapes");
              }}
            >
              Reset Search Filters
            </Button>
          </GlassCard>
        )}
      </section>
    </div>
  );
}
