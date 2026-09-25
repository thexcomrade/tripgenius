"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import Image from "next/image";
import { useRouter } from "next/navigation";
import toast from "react-hot-toast";
import {
  Sparkles,
  Compass,
  Leaf,
  Shield,
  TrendingUp,
  MapPin,
  ArrowRight,
  Star,
  Calendar,
  Users,
  Search,
  Plane,
  Utensils,
  Hotel,
  CloudSun,
  X,
  ChevronDown,
  ChevronUp,
} from "lucide-react";
import Button from "../components/ui/Button";
import Badge from "../components/ui/Badge";
import { GlassCard, SectionHeader } from "../components/ui/Card";

export default function HomePage() {
  const router = useRouter();
  const [quickDestination, setQuickDestination] = useState("");

  const handleQuickLaunch = (e: React.FormEvent) => {
    e.preventDefault();
    if (quickDestination.trim()) {
      router.push(
        `/planner?destination=${encodeURIComponent(quickDestination.trim())}`,
      );
    } else {
      router.push("/planner");
    }
  };

  const features = [
    {
      icon: <Sparkles size={24} color="#38BDF8" />,
      title: "Bespoke AI Synthesis",
      description:
        "Deep neural itinerary engine personalized to budget, travel style, and specific group dynamics.",
    },
    {
      icon: <CloudSun size={24} color="#FBBF24" />,
      title: "Live Weather Intelligence",
      description:
        "Adaptive suggestions factoring seasonal microclimates, humidity levels, and packing essentials.",
    },
    {
      icon: <Leaf size={24} color="#34D399" />,
      title: "Eco-Score & Carbon Metric",
      description:
        "Actionable sustainability scoring that tracks and minimizes your carbon footprint while traveling.",
    },
    {
      icon: <Hotel size={24} color="#C084FC" />,
      title: "Curated Stays & Dining",
      description:
        "Selected accommodations and authentic local eateries verified against regional tourism databases.",
    },
    {
      icon: <Utensils size={24} color="#FB923C" />,
      title: "Authentic Food & Culture",
      description:
        "Must-try regional cuisines, secret viewpoints, and heritage trails off the conventional path.",
    },
    {
      icon: <Shield size={24} color="#60A5FA" />,
      title: "Offline Fallback Engine",
      description:
        "Resilient algorithmic backup ensures you always receive a complete itinerary even in offline conditions.",
    },
  ];

  const trendingDestinations = [
    {
      name: "Munnar",
      state: "Kerala, India",
      category: "Highland Tea Hills",
      rating: 4.9,
      image: "/destinations/munnar.jpg",
      tag: "Trending",
    },
    {
      name: "Hampi",
      state: "Karnataka, India",
      category: "UNESCO Stone Chariot & Ruins",
      rating: 4.9,
      image: "/destinations/hampi.jpg",
      tag: "Heritage",
    },
    {
      name: "Gokarna",
      state: "Karnataka, India",
      category: "Crescent Om Beach",
      rating: 4.8,
      image: "/destinations/gokarna.jpg",
      tag: "Beaches",
    },
    {
      name: "Thekkady",
      state: "Kerala, India",
      category: "Periyar Lake & Wild Elephants",
      rating: 4.9,
      image: "/destinations/thekkady.jpg",
      tag: "Eco Wildlife",
    },
    {
      name: "Kovalam",
      state: "Kerala, India",
      category: "Iconic Lighthouse Coast",
      rating: 4.8,
      image: "/destinations/kovalam.jpg",
      tag: "Coastal",
    },
    {
      name: "Paris",
      state: "Île-de-France, France",
      category: "The City of Light",
      rating: 4.9,
      image: "/destinations/paris.jpg",
      tag: "Abroad",
    },
    {
      name: "Tokyo",
      state: "Kanto, Japan",
      category: "Senso-ji & Cherry Blossoms",
      rating: 4.9,
      image: "/destinations/tokyo.jpg",
      tag: "Abroad",
    },
    {
      name: "Bali",
      state: "Lesser Sunda, Indonesia",
      category: "Tanah Lot Sea Temple",
      rating: 4.8,
      image: "/destinations/bali.jpg",
      tag: "Tropical",
    },
    {
      name: "Dubai",
      state: "United Arab Emirates",
      category: "Burj Khalifa & Marina",
      rating: 4.8,
      image: "/destinations/dubai.jpg",
      tag: "Luxury",
    },
  ];

  const initialTestimonials = [
    {
      name: "Arjun Nair",
      location: "Bangalore",
      role: "Adventure Traveler",
      text: "TripGenius built an authentic 4-day Western Ghats itinerary with exact budget allocation and carbon estimates in seconds. The restaurant recommendations were unbelievable.",
      rating: 5,
    },
    {
      name: "Sivya Babu",
      location: "Trivandrum",
      role: "Nurse",
      text: "The sustainability metrics, real Google-rated stays, and weather-aware packing suggestions make this genuinely innovative. It feels like an intelligent concierge, not a generic booking tool.",
      rating: 5,
    },
    {
      name: "Rahul Krishna",
      location: "Chennai",
      role: "Family Vacationer",
      text: "Customized for our family of four with elderly parents. The day-by-day morning/afternoon/evening pace was spot on. Absolute 10/10.",
      rating: 5,
    },
  ];

  const [reviewsList, setReviewsList] = useState(initialTestimonials);
  const [isReviewModalOpen, setIsReviewModalOpen] = useState(false);
  const [reviewName, setReviewName] = useState("");
  const [reviewProfession, setReviewProfession] = useState("Family Vacationer");
  const [reviewPlace, setReviewPlace] = useState("Chennai");
  const [reviewRating, setReviewRating] = useState(5);
  const [hoveredStar, setHoveredStar] = useState<number | null>(null);
  const [reviewDescription, setReviewDescription] = useState("");

  useEffect(() => {
    const saved = localStorage.getItem("tripgenius_user_reviews");
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        if (Array.isArray(parsed) && parsed.length > 0) {
          setReviewsList([...parsed, ...initialTestimonials]);
        }
      } catch {
        // ignore
      }
    }

    const storedUser = localStorage.getItem("tripgenius_user");
    if (storedUser) {
      try {
        const u = JSON.parse(storedUser);
        if (u.full_name) setReviewName(u.full_name);
        if (u.location || u.city) setReviewPlace(u.location || u.city);
      } catch {
        // ignore
      }
    }
  }, []);

  const handleReviewSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!reviewName.trim()) {
      toast.error("Please enter your name.");
      return;
    }
    if (!reviewDescription.trim()) {
      toast.error("Please enter your review description.");
      return;
    }

    const newRev = {
      name: reviewName.trim(),
      role: reviewProfession.trim() || "Traveler",
      location: reviewPlace.trim() || "India",
      rating: reviewRating,
      text: reviewDescription.trim(),
    };

    const updated = [newRev, ...reviewsList];
    setReviewsList(updated);

    const existing = JSON.parse(
      localStorage.getItem("tripgenius_user_reviews") || "[]",
    );
    existing.unshift(newRev);
    localStorage.setItem("tripgenius_user_reviews", JSON.stringify(existing));

    toast.success("Thank you! Your travel review has been published.");
    setIsReviewModalOpen(false);
    setReviewDescription("");
  };

  const [showAllReviews, setShowAllReviews] = useState(false);

  // Priority sorting: 5-star reviews first, verified travelers, sorted by highest rating & detail
  const prioritySortedReviews = [...reviewsList].sort((a, b) => {
    // 1. Higher rating first (5 stars before 4 stars, etc.)
    if (b.rating !== a.rating) return b.rating - a.rating;
    // 2. Longer and more informative descriptions get higher priority
    return (b.text?.length || 0) - (a.text?.length || 0);
  });

  const MAX_DEFAULT_REVIEWS = 4;
  const displayedReviews = showAllReviews
    ? prioritySortedReviews
    : prioritySortedReviews.slice(0, MAX_DEFAULT_REVIEWS);

  return (
    <div style={{ position: "relative", overflow: "hidden" }}>
      {/* HERO SECTION */}
      <section
        style={{
          position: "relative",
          padding: "90px 24px 70px 24px",
          maxWidth: "1440px",
          margin: "0 auto",
          textAlign: "center",
        }}
      >
        {/* AMBIENT GLOW BACKDROP */}
        <div
          style={{
            position: "absolute",
            top: "5%",
            left: "50%",
            transform: "translateX(-50%)",
            width: "800px",
            height: "400px",
            background:
              "radial-gradient(circle, rgba(14, 165, 233, 0.18) 0%, rgba(20, 184, 166, 0.12) 40%, transparent 70%)",
            filter: "blur(60px)",
            pointerEvents: "none",
            zIndex: -1,
          }}
        />

        <div style={{ display: "inline-flex", marginBottom: "24px" }}>
          <Badge variant="ai" size="md" icon={<Sparkles size={14} />}>
            Next-Gen Travel AI Engine 2.0
          </Badge>
        </div>

        <h1
          style={{
            fontSize: "clamp(2.5rem, 6vw, 4.8rem)",
            fontWeight: 900,
            lineHeight: 1.15,
            letterSpacing: "-1.5px",
            maxWidth: "1050px",
            margin: "0 auto 24px auto",
          }}
        >
          Plan Extraordinary Journeys with{" "}
          <span className="gradient-text">Intelligent Precision</span>
        </h1>

        <p
          style={{
            fontSize: "clamp(1.05rem, 2vw, 1.25rem)",
            color: "#94A3B8",
            maxWidth: "760px",
            margin: "0 auto 40px auto",
            lineHeight: 1.7,
          }}
        >
          Synthesize personalized, data-backed itineraries with live weather
          intelligence, carbon footprint tracking, and curated local culinary
          trails in seconds.
        </p>

        {/* HERO QUICK LAUNCH BAR */}
        <form
          onSubmit={handleQuickLaunch}
          style={{
            maxWidth: "680px",
            margin: "0 auto 40px auto",
            display: "flex",
            alignItems: "center",
            gap: "10px",
            padding: "8px 10px 8px 20px",
            background: "rgba(15, 23, 42, 0.85)",
            backdropFilter: "blur(20px)",
            border: "1px solid rgba(14, 165, 233, 0.35)",
            borderRadius: "999px",
            boxShadow:
              "0 12px 36px rgba(0, 0, 0, 0.40), 0 0 24px rgba(14, 165, 233, 0.20)",
          }}
        >
          <MapPin size={20} color="#38BDF8" style={{ flexShrink: 0 }} />
          <input
            type="text"
            value={quickDestination}
            onChange={(e) => setQuickDestination(e.target.value)}
            placeholder="Where to? (e.g. Munnar, Coorg, Ooty, Varkala...)"
            style={{
              flex: 1,
              background: "transparent",
              border: "none",
              color: "#FFFFFF",
              fontSize: "1rem",
              outline: "none",
            }}
          />
          <Button
            type="submit"
            variant="primary"
            size="md"
            rightIcon={<ArrowRight size={16} />}
          >
            Generate Itinerary
          </Button>
        </form>

        {/* TRUST / METRICS PILLS */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: "30px",
            flexWrap: "wrap",
            color: "#94A3B8",
            fontSize: "0.9rem",
          }}
        >
          <span style={{ display: "flex", alignItems: "center", gap: "8px" }}>
            <Sparkles size={16} color="#38BDF8" /> <strong>700+</strong> Curated
            Tourism Spots
          </span>
          <span style={{ display: "flex", alignItems: "center", gap: "8px" }}>
            <CloudSun size={16} color="#FBBF24" /> Real-Time Weather Integration
          </span>
          <span style={{ display: "flex", alignItems: "center", gap: "8px" }}>
            <Leaf size={16} color="#34D399" /> 100% Eco-Scored Itineraries
          </span>
        </div>
      </section>

      {/* VALUE PROPOSITION GRID */}
      <section
        style={{ maxWidth: "1440px", margin: "0 auto", padding: "40px 24px" }}
      >
        <SectionHeader
          badge="Intelligent Architecture"
          title="Engineered for Conscious Exploration"
          subtitle="Every itinerary is dynamically calibrated against real-world tourism datasets, weather APIs, and sustainability parameters."
        />

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))",
            gap: "24px",
          }}
        >
          {features.map((feat, idx) => (
            <GlassCard
              key={idx}
              interactive
              style={{
                padding: "32px 28px",
                display: "flex",
                flexDirection: "column",
                gap: "16px",
              }}
            >
              <div
                style={{
                  width: "48px",
                  height: "48px",
                  borderRadius: "14px",
                  background: "rgba(255, 255, 255, 0.05)",
                  border: "1px solid rgba(255, 255, 255, 0.10)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                {feat.icon}
              </div>
              <h3
                style={{
                  fontSize: "1.25rem",
                  fontWeight: 700,
                  color: "#FFFFFF",
                }}
              >
                {feat.title}
              </h3>
              <p
                style={{
                  color: "#94A3B8",
                  fontSize: "0.95rem",
                  lineHeight: 1.7,
                }}
              >
                {feat.description}
              </p>
            </GlassCard>
          ))}
        </div>
      </section>

      {/* CURATED DESTINATIONS SPOTLIGHT */}
      <section
        style={{
          maxWidth: "1440px",
          margin: "40px auto",
          padding: "40px 24px",
        }}
      >
        <SectionHeader
          badge="Curated Destinations"
          title="Trending Handcrafted Escapes"
          subtitle="Discover regional sanctuaries analyzed with optimal travel seasons and cost distributions."
          action={
            <Link href="/explore" style={{ textDecoration: "none" }}>
              <Button
                variant="secondary"
                size="sm"
                rightIcon={<ArrowRight size={14} />}
              >
                View All Destinations
              </Button>
            </Link>
          }
        />

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(340px, 1fr))",
            gap: "24px",
          }}
        >
          {trendingDestinations.map((dest) => (
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
                style={{ position: "relative", height: "230px", width: "100%" }}
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
                <div
                  style={{ position: "absolute", top: "14px", left: "14px" }}
                >
                  <Badge variant="amber" size="sm">
                    {dest.tag}
                  </Badge>
                </div>
                <div
                  style={{ position: "absolute", top: "14px", right: "14px" }}
                >
                  <span
                    style={{
                      display: "inline-flex",
                      alignItems: "center",
                      gap: "4px",
                      background: "rgba(0, 0, 0, 0.60)",
                      backdropFilter: "blur(10px)",
                      padding: "4px 8px",
                      borderRadius: "8px",
                      fontSize: "0.8rem",
                      fontWeight: 700,
                      color: "#FBBF24",
                    }}
                  >
                    <Star size={12} fill="#FBBF24" /> {dest.rating}
                  </span>
                </div>
                <div
                  style={{
                    position: "absolute",
                    bottom: "16px",
                    left: "18px",
                    right: "18px",
                  }}
                >
                  <h3
                    style={{
                      fontSize: "1.45rem",
                      fontWeight: 800,
                      color: "#FFFFFF",
                    }}
                  >
                    {dest.name}
                  </h3>
                  <p style={{ color: "#CBD5E1", fontSize: "0.85rem" }}>
                    {dest.state} • {dest.category}
                  </p>
                </div>
              </div>

              <div
                style={{
                  padding: "18px",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                  background: "rgba(15, 23, 42, 0.60)",
                }}
              >
                <span
                  style={{
                    fontSize: "0.85rem",
                    color: "#38BDF8",
                    fontWeight: 600,
                  }}
                >
                  Click to plan trip
                </span>
                <div
                  style={{
                    width: "32px",
                    height: "32px",
                    borderRadius: "50%",
                    background: "rgba(14, 165, 233, 0.15)",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    color: "#38BDF8",
                  }}
                >
                  <ArrowRight size={14} />
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* SOCIAL PROOF & TESTIMONIALS */}
      <section
        style={{
          maxWidth: "1440px",
          margin: "40px auto",
          padding: "40px 24px",
        }}
      >
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "flex-end",
            flexWrap: "wrap",
            gap: "16px",
            marginBottom: "32px",
          }}
        >
          <div>
            <div style={{ display: "inline-flex", marginBottom: "8px" }}>
              <Badge
                variant="neutral"
                size="sm"
                icon={<Star size={12} fill="#FBBF24" color="#FBBF24" />}
              >
                Verified Travelers
              </Badge>
            </div>
            <h2
              style={{
                fontSize: "clamp(1.8rem, 3vw, 2.5rem)",
                fontWeight: 800,
                color: "#FFFFFF",
                marginTop: "4px",
              }}
            >
              Real Travelers. Sustainable Journeys.
            </h2>
            <p
              style={{
                color: "#94A3B8",
                fontSize: "0.95rem",
                marginTop: "4px",
              }}
            >
              Top experiences and authentic feedback from travelers around the world.
            </p>
          </div>

          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "10px",
              background: "rgba(15, 23, 42, 0.6)",
              border: "1px solid rgba(255, 255, 255, 0.08)",
              padding: "8px 16px",
              borderRadius: "999px",
            }}
          >
            <div style={{ display: "flex", gap: "2px" }}>
              {[...Array(5)].map((_, i) => (
                <Star key={i} size={14} fill="#FBBF24" color="#FBBF24" />
              ))}
            </div>
            <span
              style={{
                fontSize: "0.88rem",
                fontWeight: 700,
                color: "#FFFFFF",
              }}
            >
              4.9/5
            </span>
            <span style={{ fontSize: "0.82rem", color: "#94A3B8" }}>
              ({prioritySortedReviews.length} verified reviews)
            </span>
          </div>
        </div>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
            gap: "24px",
          }}
        >
          {displayedReviews.map((t, idx) => (
            <GlassCard
              key={idx}
              style={{
                padding: "28px",
                display: "flex",
                flexDirection: "column",
                justifyContent: "space-between",
                gap: "18px",
                border:
                  idx === 0
                    ? "1px solid rgba(14, 165, 233, 0.35)"
                    : "1px solid rgba(255, 255, 255, 0.08)",
                background:
                  idx === 0
                    ? "linear-gradient(135deg, rgba(14, 165, 233, 0.08), rgba(15, 23, 42, 0.75))"
                    : "rgba(15, 23, 42, 0.60)",
              }}
            >
              <div>
                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                    marginBottom: "14px",
                  }}
                >
                  <div style={{ display: "flex", gap: "4px" }}>
                    {[...Array(t.rating)].map((_, i) => (
                      <Star key={i} size={15} fill="#FBBF24" color="#FBBF24" />
                    ))}
                  </div>
                  {t.rating === 5 && (
                    <span
                      style={{
                        fontSize: "0.72rem",
                        fontWeight: 700,
                        color: "#34D399",
                        background: "rgba(16, 185, 129, 0.12)",
                        padding: "2px 8px",
                        borderRadius: "999px",
                        border: "1px solid rgba(16, 185, 129, 0.25)",
                      }}
                    >
                      ★ Top Review
                    </span>
                  )}
                </div>
                <p
                  style={{
                    color: "#E2E8F0",
                    fontSize: "0.95rem",
                    lineHeight: 1.65,
                    fontStyle: "italic",
                  }}
                >
                  &ldquo;{t.text}&rdquo;
                </p>
              </div>
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "12px",
                  borderTop: "1px solid rgba(255, 255, 255, 0.08)",
                  paddingTop: "16px",
                }}
              >
                <div
                  style={{
                    width: "40px",
                    height: "40px",
                    borderRadius: "50%",
                    background:
                      idx % 2 === 0
                        ? "linear-gradient(135deg, #0EA5E9, #14B8A6)"
                        : "linear-gradient(135deg, #8B5CF6, #EC4899)",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontWeight: 800,
                    color: "#FFFFFF",
                    fontSize: "0.95rem",
                    flexShrink: 0,
                  }}
                >
                  {t.name.charAt(0).toUpperCase()}
                </div>
                <div style={{ minWidth: 0, flex: 1 }}>
                  <h4
                    style={{
                      color: "#FFFFFF",
                      fontSize: "0.94rem",
                      fontWeight: 700,
                      whiteSpace: "nowrap",
                      overflow: "hidden",
                      textOverflow: "ellipsis",
                    }}
                  >
                    {t.name}
                  </h4>
                  <p
                    style={{
                      color: "#94A3B8",
                      fontSize: "0.82rem",
                      whiteSpace: "nowrap",
                      overflow: "hidden",
                      textOverflow: "ellipsis",
                    }}
                  >
                    {t.role} • {t.location}
                  </p>
                </div>
              </div>
            </GlassCard>
          ))}
        </div>

        {prioritySortedReviews.length > MAX_DEFAULT_REVIEWS && (
          <div
            style={{
              display: "flex",
              justifyContent: "center",
              marginTop: "32px",
            }}
          >
            <Button
              variant="outline"
              size="md"
              leftIcon={
                showAllReviews ? (
                  <ChevronUp size={16} />
                ) : (
                  <ChevronDown size={16} />
                )
              }
              onClick={() => setShowAllReviews(!showAllReviews)}
              style={{
                borderColor: "rgba(255, 255, 255, 0.16)",
                color: "#E2E8F0",
                background: "rgba(255, 255, 255, 0.05)",
                padding: "10px 22px",
                borderRadius: "12px",
              }}
            >
              {showAllReviews
                ? `Show Top ${MAX_DEFAULT_REVIEWS} Reviews`
                : `View All Reviews (${prioritySortedReviews.length})`}
            </Button>
          </div>
        )}
      </section>

      {/* CALL TO ACTION BANNER */}
      <section
        style={{
          maxWidth: "1440px",
          margin: "60px auto 30px auto",
          padding: "0 24px",
        }}
      >
        <div
          style={{
            background:
              "linear-gradient(135deg, rgba(14, 165, 233, 0.20) 0%, rgba(20, 184, 166, 0.18) 50%, rgba(245, 158, 11, 0.12) 100%)",
            border: "1px solid rgba(14, 165, 233, 0.35)",
            borderRadius: "28px",
            padding: "70px 30px",
            textAlign: "center",
            position: "relative",
            overflow: "hidden",
            boxShadow: "0 20px 60px rgba(0, 0, 0, 0.40)",
          }}
        >
          <h2
            style={{
              fontSize: "clamp(2rem, 4vw, 3.2rem)",
              fontWeight: 900,
              color: "#FFFFFF",
              marginBottom: "18px",
              letterSpacing: "-1px",
            }}
          >
            Ready for Smarter, Greener Travel?
          </h2>
          <p
            style={{
              color: "#CBD5E1",
              fontSize: "1.1rem",
              maxWidth: "620px",
              margin: "0 auto 32px auto",
              lineHeight: 1.7,
            }}
          >
            Join thousands of travelers who rely on TripGenius to eliminate
            planning fatigue and unlock unforgettable experiences.
          </p>
          <div
            style={{
              display: "flex",
              gap: "14px",
              justifyContent: "center",
              flexWrap: "wrap",
            }}
          >
            <Link href="/planner" style={{ textDecoration: "none" }}>
              <Button
                variant="primary"
                size="lg"
                leftIcon={<Sparkles size={18} />}
              >
                Launch Free AI Planner
              </Button>
            </Link>
            <Link href="/explore" style={{ textDecoration: "none" }}>
              <Button
                variant="secondary"
                size="lg"
                leftIcon={<Compass size={18} />}
              >
                Explore Destinations
              </Button>
            </Link>
            <Button
              variant="outline"
              size="lg"
              leftIcon={<Star size={18} fill="#FBBF24" color="#FBBF24" />}
              onClick={() => setIsReviewModalOpen(true)}
              style={{
                borderColor: "rgba(251, 191, 36, 0.45)",
                color: "#FDE68A",
                background: "rgba(251, 191, 36, 0.10)",
                fontWeight: 700,
              }}
            >
              Share Your Experience
            </Button>
          </div>
        </div>
      </section>

      {/* REVIEW SUBMISSION MODAL */}
      {isReviewModalOpen && (
        <div
          role="dialog"
          aria-modal="true"
          style={{
            position: "fixed",
            inset: 0,
            zIndex: 99999,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            padding: "20px",
            background: "rgba(3, 7, 18, 0.80)",
            backdropFilter: "blur(12px)",
            WebkitBackdropFilter: "blur(12px)",
          }}
          onClick={(e) => {
            if (e.target === e.currentTarget) setIsReviewModalOpen(false);
          }}
        >
          <div
            style={{
              position: "relative",
              width: "100%",
              maxWidth: "540px",
              background:
                "linear-gradient(135deg, rgba(15, 23, 42, 0.98), rgba(30, 41, 59, 0.96))",
              border: "1px solid rgba(255, 255, 255, 0.14)",
              boxShadow:
                "0 25px 60px -15px rgba(0, 0, 0, 0.8), 0 0 40px rgba(14, 165, 233, 0.15)",
              borderRadius: "24px",
              padding: "32px",
              color: "#FFFFFF",
            }}
          >
            {/* Close Button */}
            <button
              type="button"
              onClick={() => setIsReviewModalOpen(false)}
              style={{
                position: "absolute",
                top: "20px",
                right: "20px",
                background: "rgba(255, 255, 255, 0.08)",
                border: "1px solid rgba(255, 255, 255, 0.12)",
                borderRadius: "50%",
                width: "36px",
                height: "36px",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                color: "#94A3B8",
                cursor: "pointer",
                transition: "all 0.2s",
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.color = "#FFFFFF";
                e.currentTarget.style.background = "rgba(255, 255, 255, 0.15)";
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.color = "#94A3B8";
                e.currentTarget.style.background = "rgba(255, 255, 255, 0.08)";
              }}
            >
              <X size={18} />
            </button>

            {/* Modal Header */}
            <div style={{ marginBottom: "20px" }}>
              <div style={{ display: "inline-flex", marginBottom: "8px" }}>
                <Badge
                  variant="amber"
                  size="sm"
                  icon={<Star size={12} fill="#FBBF24" color="#FBBF24" />}
                >
                  Traveler Feedback
                </Badge>
              </div>
              <h3
                style={{
                  fontSize: "1.5rem",
                  fontWeight: 800,
                  color: "#FFFFFF",
                  margin: "4px 0",
                }}
              >
                Share Your Experience
              </h3>
              <p
                style={{
                  color: "#94A3B8",
                  fontSize: "0.88rem",
                  lineHeight: 1.5,
                }}
              >
                Share your journey or planning experience with fellow travelers.
              </p>
            </div>

            <form onSubmit={handleReviewSubmit}>
              {/* Star Rating Picker */}
              <div style={{ marginBottom: "18px" }}>
                <label
                  style={{
                    display: "block",
                    fontSize: "0.85rem",
                    fontWeight: 600,
                    color: "#CBD5E1",
                    marginBottom: "8px",
                  }}
                >
                  Rating
                </label>
                <div
                  style={{ display: "flex", alignItems: "center", gap: "8px" }}
                >
                  {[1, 2, 3, 4, 5].map((star) => {
                    const active = (hoveredStar ?? reviewRating) >= star;
                    return (
                      <button
                        key={star}
                        type="button"
                        onClick={() => setReviewRating(star)}
                        onMouseEnter={() => setHoveredStar(star)}
                        onMouseLeave={() => setHoveredStar(null)}
                        style={{
                          background: "none",
                          border: "none",
                          cursor: "pointer",
                          padding: "4px",
                          display: "inline-flex",
                          alignItems: "center",
                          justifyContent: "center",
                          transform: active ? "scale(1.15)" : "scale(1)",
                          transition: "transform 0.15s ease",
                        }}
                      >
                        <Star
                          size={28}
                          fill={active ? "#FBBF24" : "transparent"}
                          color={active ? "#FBBF24" : "#64748B"}
                        />
                      </button>
                    );
                  })}
                  <span
                    style={{
                      marginLeft: "8px",
                      fontSize: "0.9rem",
                      fontWeight: 700,
                      color: "#FDE68A",
                    }}
                  >
                    {reviewRating} of 5 Stars
                  </span>
                </div>
              </div>

              {/* Name Input */}
              <div style={{ marginBottom: "16px" }}>
                <label
                  style={{
                    display: "block",
                    fontSize: "0.85rem",
                    fontWeight: 600,
                    color: "#CBD5E1",
                    marginBottom: "6px",
                  }}
                >
                  Your Name
                </label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Rahul Krishna"
                  value={reviewName}
                  onChange={(e) => setReviewName(e.target.value)}
                  style={{
                    width: "100%",
                    padding: "12px 14px",
                    borderRadius: "12px",
                    background: "rgba(15, 23, 42, 0.7)",
                    border: "1px solid rgba(255, 255, 255, 0.14)",
                    color: "#FFFFFF",
                    fontSize: "0.95rem",
                    outline: "none",
                    boxSizing: "border-box",
                  }}
                />
              </div>

              {/* Tag Inputs: Profession & Place */}
              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "1fr 1fr",
                  gap: "12px",
                  marginBottom: "8px",
                }}
              >
                <div>
                  <label
                    style={{
                      display: "block",
                      fontSize: "0.85rem",
                      fontWeight: 600,
                      color: "#CBD5E1",
                      marginBottom: "6px",
                    }}
                  >
                    Role / Profession
                  </label>
                  <input
                    type="text"
                    placeholder="e.g. Family Vacationer"
                    value={reviewProfession}
                    onChange={(e) => setReviewProfession(e.target.value)}
                    style={{
                      width: "100%",
                      padding: "10px 14px",
                      borderRadius: "12px",
                      background: "rgba(15, 23, 42, 0.7)",
                      border: "1px solid rgba(255, 255, 255, 0.14)",
                      color: "#FFFFFF",
                      fontSize: "0.9rem",
                      outline: "none",
                      boxSizing: "border-box",
                    }}
                  />
                </div>
                <div>
                  <label
                    style={{
                      display: "block",
                      fontSize: "0.85rem",
                      fontWeight: 600,
                      color: "#CBD5E1",
                      marginBottom: "6px",
                    }}
                  >
                    Place / City
                  </label>
                  <input
                    type="text"
                    placeholder="e.g. Chennai"
                    value={reviewPlace}
                    onChange={(e) => setReviewPlace(e.target.value)}
                    style={{
                      width: "100%",
                      padding: "10px 14px",
                      borderRadius: "12px",
                      background: "rgba(15, 23, 42, 0.7)",
                      border: "1px solid rgba(255, 255, 255, 0.14)",
                      color: "#FFFFFF",
                      fontSize: "0.9rem",
                      outline: "none",
                      boxSizing: "border-box",
                    }}
                  />
                </div>
              </div>

              {/* Tag Preview */}
              <div
                style={{
                  marginBottom: "16px",
                  display: "flex",
                  alignItems: "center",
                  gap: "8px",
                }}
              >
                <span style={{ fontSize: "0.78rem", color: "#94A3B8" }}>
                  Tag Preview:
                </span>
                <span
                  style={{
                    fontSize: "0.8rem",
                    fontWeight: 600,
                    color: "#38BDF8",
                    background: "rgba(14, 165, 233, 0.12)",
                    padding: "3px 10px",
                    borderRadius: "999px",
                    border: "1px solid rgba(14, 165, 233, 0.3)",
                  }}
                >
                  ({reviewProfession.trim() || "Family Vacationer"} •{" "}
                  {reviewPlace.trim() || "Chennai"})
                </span>
              </div>

              {/* Description Input */}
              <div style={{ marginBottom: "22px" }}>
                <label
                  style={{
                    display: "block",
                    fontSize: "0.85rem",
                    fontWeight: 600,
                    color: "#CBD5E1",
                    marginBottom: "6px",
                  }}
                >
                  Review Description
                </label>
                <textarea
                  required
                  rows={4}
                  placeholder="Tell us what you liked about TripGenius, the AI itinerary, eco-recommendations, or hidden places..."
                  value={reviewDescription}
                  onChange={(e) => setReviewDescription(e.target.value)}
                  style={{
                    width: "100%",
                    padding: "12px 14px",
                    borderRadius: "12px",
                    background: "rgba(15, 23, 42, 0.7)",
                    border: "1px solid rgba(255, 255, 255, 0.14)",
                    color: "#FFFFFF",
                    fontSize: "0.92rem",
                    lineHeight: 1.6,
                    resize: "vertical",
                    outline: "none",
                    boxSizing: "border-box",
                  }}
                />
              </div>

              {/* Actions */}
              <div
                style={{
                  display: "flex",
                  justifyContent: "flex-end",
                  gap: "12px",
                }}
              >
                <Button
                  type="button"
                  variant="ghost"
                  size="md"
                  onClick={() => setIsReviewModalOpen(false)}
                >
                  Cancel
                </Button>
                <Button
                  type="submit"
                  variant="primary"
                  size="md"
                  leftIcon={<Star size={16} fill="#FBBF24" color="#FBBF24" />}
                >
                  Publish Review
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
