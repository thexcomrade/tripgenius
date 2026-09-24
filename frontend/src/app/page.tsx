"use client";

import { useState } from "react";
import Link from "next/link";
import Image from "next/image";
import { useRouter } from "next/navigation";
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

  const testimonials = [
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
        <SectionHeader
          badge="Verified Travelers"
          title="Real Travelers. Sustainable Journeys."
          subtitle="See how TripGenius changes the vacation planning paradigm."
        />

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))",
            gap: "24px",
          }}
        >
          {testimonials.map((t, idx) => (
            <GlassCard
              key={idx}
              style={{
                padding: "30px",
                display: "flex",
                flexDirection: "column",
                justifyContent: "space-between",
                gap: "20px",
              }}
            >
              <div>
                <div
                  style={{ display: "flex", gap: "4px", marginBottom: "14px" }}
                >
                  {[...Array(t.rating)].map((_, i) => (
                    <Star key={i} size={16} fill="#FBBF24" color="#FBBF24" />
                  ))}
                </div>
                <p
                  style={{
                    color: "#E2E8F0",
                    fontSize: "0.98rem",
                    lineHeight: 1.7,
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
                    background: "linear-gradient(135deg, #0EA5E9, #14B8A6)",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontWeight: 800,
                    color: "#FFFFFF",
                    fontSize: "1rem",
                  }}
                >
                  {t.name.charAt(0)}
                </div>
                <div>
                  <h4
                    style={{
                      color: "#FFFFFF",
                      fontSize: "0.95rem",
                      fontWeight: 700,
                    }}
                  >
                    {t.name}
                  </h4>
                  <p style={{ color: "#94A3B8", fontSize: "0.82rem" }}>
                    {t.role} • {t.location}
                  </p>
                </div>
              </div>
            </GlassCard>
          ))}
        </div>
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
          </div>
        </div>
      </section>
    </div>
  );
}
