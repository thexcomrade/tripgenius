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
  {
    id: 17,
    name: "Egypt",
    location: "Cairo & Giza, Egypt",
    image: "/destinations/egypt.jpg",
    category: "International / Abroad",
    description:
      "Majestic Pyramids of Giza, Great Sphinx, Nile River felucca cruises, and ancient pharaoh tombs. 4N/5D complete guided package.",
    rating: 4.9,
    season: "Oct – Apr",
    budgetEst: "₹60,000",
    featured: true,
  },
  {
    id: 18,
    name: "Vietnam",
    location: "Da Nang, Phu Quoc & Hanoi, Vietnam",
    image: "/destinations/vietnam.jpg",
    category: "International / Abroad",
    description:
      "Golden Bridge in Ba Na Hills, pristine Phu Quoc island beaches, Hanoi train street, and lantern-lit ancient town. 3N/4D getaway.",
    rating: 4.8,
    season: "Nov – Apr",
    budgetEst: "₹23,000",
    featured: true,
  },
  {
    id: 19,
    name: "Uzbekistan",
    location: "Samarkand & Bukhara, Uzbekistan",
    image: "/destinations/uzbekistan.jpg",
    category: "International / Abroad",
    description:
      "Silk Road splendour — turquoise majolica domes of Registan, Shah-i-Zinda necropolis, ancient Bukhara citadels, and rich plov gastronomy. 4N/5D holiday.",
    rating: 4.9,
    season: "Mar – Jun / Sep – Nov",
    budgetEst: "₹39,900",
    featured: true,
  },
  {
    id: 20,
    name: "Georgia",
    location: "Tbilisi & Kazbegi, Georgia",
    image: "/destinations/georgia.jpg",
    category: "International / Abroad",
    description:
      "Breathtaking Greater Caucasus alpine vistas, historic Ananuri Fortress, Gergeti Trinity mountain church, and Old Tbilisi sulfur baths. 3N/4D tour.",
    rating: 4.8,
    season: "May – Oct",
    budgetEst: "₹40,000",
    featured: true,
  },
  {
    id: 21,
    name: "Azerbaijan",
    location: "Baku & Caspian Coast, Azerbaijan",
    image: "/destinations/azerbaijan.jpg",
    category: "International / Abroad",
    description:
      "The Land of Fire — ancient Icherisheher walled fortress, futuristic Flame Towers, Gobustan mud volcanoes, and Caspian seaside promenade. 4N/5D package.",
    rating: 4.8,
    season: "Apr – Jun / Sep – Oct",
    budgetEst: "₹25,800",
    featured: true,
  },
  {
    id: 22,
    name: "Malaysia",
    location: "Kuala Lumpur & Putrajaya, Malaysia",
    image: "/destinations/malaysia.jpg",
    category: "International / Abroad",
    description:
      "Sky-high Petronas Twin Towers, iconic pink domed Putra Mosque, sacred limestone Batu Caves, and bustling night street markets. 3N/4D holiday.",
    rating: 4.8,
    season: "All Year",
    budgetEst: "₹22,500",
    featured: true,
  },
  {
    id: 23,
    name: "Thailand",
    location: "Bangkok, Chiang Mai & Phuket, Thailand",
    image: "/destinations/thailand.jpg",
    category: "International / Abroad",
    description:
      "Gilded Buddhist temples, emerald Buddha sanctuaries in Chiang Mai, tropical Phi Phi islands, and world-famous street food. 4N/5D escape.",
    rating: 4.9,
    season: "Nov – Apr",
    budgetEst: "₹23,000",
    featured: true,
  },
  {
    id: 24,
    name: "Lakshadweep",
    location: "Agatti & Bangaram, Lakshadweep, India",
    image: "/destinations/lakshadweep.jpg",
    category: "Beaches",
    description:
      "Untouched Indian Ocean coral atolls — translucent turquoise lagoons, vibrant reef scuba diving, sea turtle snorkeling, and secluded white sandbanks. 3N/4D.",
    rating: 4.9,
    season: "Oct – May",
    budgetEst: "₹13,500",
    featured: true,
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
    <div style={{ width: "100%", display: "flex", flexDirection: "column" }}>
      {/* SPOTLIGHT DESTINATION FULL-WIDTH HERO BANNER */}
      <section
        style={{
          position: "relative",
          width: "100%",
          minHeight: "460px",
          overflow: "hidden",
          borderBottom: "1px solid rgba(255, 255, 255, 0.12)",
          boxShadow: "0 20px 60px rgba(0, 0, 0, 0.65)",
        }}
      >
        <div style={{ position: "relative", height: "480px", width: "100%" }}>
          <Image
            src={spotlight.image}
            alt={spotlight.name}
            fill
            priority
            style={{ objectFit: "cover", objectPosition: "center 40%" }}
          />
          <div
            style={{
              position: "absolute",
              inset: 0,
              background:
                "linear-gradient(to top, rgba(3, 7, 18, 0.98) 0%, rgba(3, 7, 18, 0.45) 55%, rgba(3, 7, 18, 0.2) 100%), linear-gradient(to right, rgba(3, 7, 18, 0.75) 0%, transparent 65%)",
            }}
          />

          <div
            style={{
              position: "absolute",
              top: "32px",
              left: "0",
              right: "0",
              maxWidth: "1440px",
              margin: "0 auto",
              padding: "0 clamp(20px, 4vw, 48px)",
              pointerEvents: "none",
            }}
          >
            <div style={{ pointerEvents: "auto" }}>
              <Badge
                variant="amber"
                size="md"
                icon={<Star size={14} fill="#FBBF24" />}
              >
                Curator&apos;s Pick of the Month
              </Badge>
            </div>
          </div>

          <div
            style={{
              position: "absolute",
              bottom: "40px",
              left: "0",
              right: "0",
              maxWidth: "1440px",
              margin: "0 auto",
              padding: "0 clamp(20px, 4vw, 48px)",
            }}
          >
            <h1
              style={{
                fontSize: "clamp(2.2rem, 4.5vw, 3.8rem)",
                fontWeight: 700,
                color: "#FFFFFF",
                letterSpacing: "-0.03em",
                marginBottom: "10px",
                lineHeight: 1.15,
                textShadow: "0 4px 20px rgba(0,0,0,0.6)",
              }}
            >
              {spotlight.name} <span style={{ opacity: 0.6, fontWeight: 400 }}>•</span> {spotlight.location}
            </h1>
            <p
              style={{
                color: "#E2E8F0",
                fontSize: "1.1rem",
                maxWidth: "750px",
                lineHeight: 1.6,
                marginBottom: "24px",
                textShadow: "0 2px 10px rgba(0,0,0,0.7)",
              }}
            >
              {spotlight.description}
            </p>
            <div
              style={{
                display: "flex",
                gap: "14px",
                alignItems: "center",
                flexWrap: "wrap",
                marginBottom: "16px",
              }}
            >
              <button
                type="button"
                onClick={() =>
                  router.push(
                    `/planner?destination=${encodeURIComponent(spotlight.name)}`,
                  )
                }
                style={{
                  display: "inline-flex",
                  alignItems: "center",
                  justifyContent: "center",
                  gap: "10px",
                  padding: "14px 28px",
                  borderRadius: "14px",
                  background:
                    "linear-gradient(135deg, #0284C7 0%, #0EA5E9 50%, #38BDF8 100%)",
                  color: "#FFFFFF",
                  fontSize: "1rem",
                  fontWeight: 700,
                  letterSpacing: "-0.01em",
                  border: "1px solid rgba(255, 255, 255, 0.35)",
                  boxShadow:
                    "0 0 28px rgba(14, 165, 233, 0.55), 0 8px 20px rgba(0, 0, 0, 0.4)",
                  cursor: "pointer",
                  transition: "all 0.25s cubic-bezier(0.16, 1, 0.3, 1)",
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = "translateY(-2px) scale(1.02)";
                  e.currentTarget.style.boxShadow =
                    "0 0 36px rgba(14, 165, 233, 0.75), 0 12px 28px rgba(0, 0, 0, 0.5)";
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = "translateY(0) scale(1)";
                  e.currentTarget.style.boxShadow =
                    "0 0 28px rgba(14, 165, 233, 0.55), 0 8px 20px rgba(0, 0, 0, 0.4)";
                }}
              >
                <Sparkles size={18} fill="#FFFFFF" color="#FFFFFF" />
                <span>Plan Trip to {spotlight.name}</span>
                <ArrowRight size={17} color="#FFFFFF" />
              </button>

              <button
                type="button"
                onClick={() => {
                  const el = document.getElementById("destinations-grid-anchor");
                  if (el) el.scrollIntoView({ behavior: "smooth" });
                }}
                style={{
                  display: "inline-flex",
                  alignItems: "center",
                  gap: "8px",
                  padding: "14px 22px",
                  borderRadius: "14px",
                  background: "rgba(255, 255, 255, 0.08)",
                  backdropFilter: "blur(16px)",
                  WebkitBackdropFilter: "blur(16px)",
                  border: "1px solid rgba(255, 255, 255, 0.18)",
                  color: "#F8FAFC",
                  fontSize: "0.95rem",
                  fontWeight: 600,
                  cursor: "pointer",
                  transition: "all 0.2s ease",
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.background = "rgba(255, 255, 255, 0.14)";
                  e.currentTarget.style.borderColor = "rgba(255, 255, 255, 0.3)";
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.background = "rgba(255, 255, 255, 0.08)";
                  e.currentTarget.style.borderColor = "rgba(255, 255, 255, 0.18)";
                }}
              >
                <Compass size={17} color="#38BDF8" />
                <span>Explore All Escapes</span>
              </button>
            </div>

            {/* QUICK STATS PILLS */}
            <div
              style={{
                display: "flex",
                gap: "10px",
                alignItems: "center",
                flexWrap: "wrap",
              }}
            >
              <div
                style={{
                  display: "inline-flex",
                  alignItems: "center",
                  gap: "6px",
                  padding: "6px 14px",
                  borderRadius: "10px",
                  background: "rgba(3, 7, 18, 0.75)",
                  backdropFilter: "blur(12px)",
                  WebkitBackdropFilter: "blur(12px)",
                  border: "1px solid rgba(255, 255, 255, 0.12)",
                  fontSize: "0.85rem",
                  color: "#CBD5E1",
                }}
              >
                <Calendar size={14} color="#38BDF8" />
                <span>
                  Best Season:{" "}
                  <strong style={{ color: "#FFFFFF" }}>{spotlight.season}</strong>
                </span>
              </div>

              <div
                style={{
                  display: "inline-flex",
                  alignItems: "center",
                  gap: "6px",
                  padding: "6px 14px",
                  borderRadius: "10px",
                  background: "rgba(3, 7, 18, 0.75)",
                  backdropFilter: "blur(12px)",
                  WebkitBackdropFilter: "blur(12px)",
                  border: "1px solid rgba(52, 211, 153, 0.25)",
                  fontSize: "0.85rem",
                  color: "#CBD5E1",
                }}
              >
                <DollarSign size={14} color="#34D399" />
                <span>
                  Avg Est:{" "}
                  <strong style={{ color: "#34D399" }}>
                    {spotlight.budgetEst}
                  </strong>
                </span>
              </div>

              <div
                style={{
                  display: "inline-flex",
                  alignItems: "center",
                  gap: "6px",
                  padding: "6px 14px",
                  borderRadius: "10px",
                  background: "rgba(3, 7, 18, 0.75)",
                  backdropFilter: "blur(12px)",
                  WebkitBackdropFilter: "blur(12px)",
                  border: "1px solid rgba(245, 158, 11, 0.25)",
                  fontSize: "0.85rem",
                  color: "#CBD5E1",
                }}
              >
                <Star size={14} fill="#FBBF24" color="#FBBF24" />
                <span>
                  Rating:{" "}
                  <strong style={{ color: "#FFFFFF" }}>
                    {spotlight.rating}
                  </strong>{" "}
                  / 5.0
                </span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* MAIN EXPLORE CONTENT CONTAINER */}
      <div
        style={{
          width: "94%",
          maxWidth: "1440px",
          margin: "0 auto",
          padding: "36px 16px 64px",
          display: "flex",
          flexDirection: "column",
          gap: "36px",
        }}
      >

      {/* SEARCH & CATEGORY FILTERING */}
      <section
        id="destinations-grid-anchor"
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
              style={{ fontSize: "1.75rem", fontWeight: 600, color: "#FFFFFF", letterSpacing: "-0.025em" }}
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
          <div className="grid-3-col">
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
                      <Badge
                        variant="overlay"
                        size="sm"
                        style={{
                          letterSpacing: "0.03em",
                          textTransform: "uppercase",
                          fontSize: "0.72rem",
                        }}
                      >
                        <span
                          style={{
                            width: "6px",
                            height: "6px",
                            borderRadius: "50%",
                            background: "#38BDF8",
                            display: "inline-block",
                            marginRight: "6px",
                            boxShadow: "0 0 6px #38BDF8",
                          }}
                        />
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
                            fontSize: "1.3rem",
                            fontWeight: 600,
                            letterSpacing: "-0.02em",
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
    </div>
  );
}
