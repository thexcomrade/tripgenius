"use client";

import { FormEvent, useEffect, useState, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import {
  Sparkles,
  MapPin,
  Calendar,
  Users,
  IndianRupee,
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
import { parseDestinationQuery } from "../../utils/queryParser";

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
    id: "Bike",
    label: "Bike",
    desc: "Two-wheeler rental across local spots",
    icon: "🏍️",
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
    id: "NoStay",
    label: "No Stay / Day Trip",
    desc: "Single-day outing — no overnight accommodation needed",
    icon: "🌅",
  },
  {
    id: "Hotel",
    label: "Comfort Hotel",
    desc: "Modern amenities & central access",
    icon: "🏨",
  },
  {
    id: "Resort",
    label: "Boutique Resort",
    desc: "Scenic vistas & premium relaxation",
    icon: "🏖️",
  },
  {
    id: "Homestay",
    label: "Authentic Homestay",
    desc: "Warm hospitality & regional cooking",
    icon: "🏡",
  },
  {
    id: "Eco-Lodge",
    label: "Eco Lodge / Farmstay",
    desc: "Solar powered & tranquil nature immersion",
    icon: "🌿",
  },
  {
    id: "Hostel",
    label: "Backpacker Hostel",
    desc: "Budget friendly & social backpacker hubs",
    icon: "🎒",
  },
];

const DEFAULT_FOCUS_POINTS = [
  "Scenic Landscapes & Horizons",
  "Heritage, Temples & Forts",
  "Local Food Tasting & Street Cuisines",
  "Nature & Green Trails",
  "Photography Spots & Sunsets",
  "Handicrafts & Artisan Markets",
  "Panoramic Viewpoints",
  "Cultural Immersion & Traditions",
  "Waterfalls & Scenic Lakes",
  "Wildlife Safaris & Sanctuaries",
];

const DESTINATION_FOCUS_POINTS_MAP: Record<string, string[]> = {
  varanasi: [
    "Ganga Aarti & Ghats",
    "Ancient Temples & Jyotirlingas",
    "Morning Ganges Boat Ride",
    "Spiritual Walking Trails",
    "Banarasi Street Food & Chaat",
    "Banarasi Silk & Handlooms",
    "Sarnath Buddhist Stupas & Museum",
    "Subah-e-Banaras Classical Music",
    "Ghat Photography & Sunrises",
    "Heritage Havelis & Cultural Walks",
  ],
  munnar: [
    "Tea Plantation Walks & Museum",
    "Eravikulam National Park & Nilgiri Tahr",
    "Attukad & Lakkam Waterfalls",
    "Anamudi Peak & Mountain Treks",
    "Mattupetty Dam & Speedboating",
    "Kundala Lake Shikara Rides",
    "Organic Spice Garden Tours",
    "Top Station Panoramic Cloud Views",
    "Authentic Kerala Sadhya Tasting",
    "Valley Photography Spots",
  ],
  goa: [
    "Golden Sand Beaches & Sunsets",
    "Scuba Diving & Water Sports",
    "Aguada & Chapora Forts",
    "Old Goa UNESCO Heritage Churches",
    "Beach Shacks & Nightlife",
    "Fontainhas Latin Quarter Walk",
    "Mandovi River Cruise & Music",
    "Dudhsagar Waterfalls Trek",
    "Goan Seafood & Feni Tasting",
    "Spice Plantation Tour",
  ],
  thenkasi: [
    "Herbal Waterfalls Hydrotherapy",
    "Courtallam Main & Five Falls",
    "Kasi Viswanathar Temple (180ft Gopuram)",
    "Shenkottai Border Pepper Chicken",
    "Gundar Dam & Western Ghats",
    "Wild Forest Honey & Fruit Groves",
    "Herbal Sukku Kaapi Trails",
    "Spiritual & Nature Walks",
  ],
  courtallam: [
    "Herbal Waterfalls Hydrotherapy",
    "Courtallam Main & Five Falls",
    "Old Courtallam & Tiger Falls",
    "Kasi Viswanathar Temple (180ft Gopuram)",
    "Shenkottai Border Pepper Chicken",
    "Gundar Dam & Western Ghats",
    "Wild Forest Honey & Fruit Groves",
    "Herbal Sukku Kaapi Trails",
  ],
  varkala: [
    "Varkala Red Cliff Walks",
    "Papanasam Beach Holy Dip",
    "Kappil Lake & Mangrove Kayaking",
    "Janardhana Swamy 2000-Year Temple",
    "Black Sand Beach Sunsets",
    "Ayurvedic Massages & Spas",
    "Cliffside Seafood Cafes",
    "Surfing & Dolphin Spotting",
  ],
  ooty: [
    "Government Botanical Garden",
    "Nilgiri Mountain Toy Train",
    "Doddabetta Peak Panoramas",
    "Pykara Lake & Waterfalls",
    "Ooty Lake Boating",
    "Homemade Chocolate Tasting",
    "Tea Factory & CTC Museum",
    "Pine Forest Nature Walks",
  ],
  paris: [
    "Eiffel Tower & Seine Cruise",
    "Louvre & Musée d'Orsay Art",
    "Montmartre & Sacré-Cœur",
    "French Patisseries & Wine Bistros",
    "Palace of Versailles Day Trip",
    "Champs-Élysées & Arc de Triomphe",
    "Latin Quarter & Historic Bookstores",
    "Gourmet Cheese & Baguette Trails",
  ],
  tokyo: [
    "Shinjuku & Shibuya Neon Crossings",
    "Sensō-ji Historic Asakusa Temple",
    "Tsukiji Outer Market Fresh Sushi",
    "Akihabara Tech & Anime Culture",
    "Tokyo Skytree Panoramic Observatories",
    "Meiji Shrine & Forest Walk",
    "Authentic Ramen & Izakaya Crawls",
    "Cherry Blossom Parks & Gardens",
  ],
  dubai: [
    "Burj Khalifa Observation Deck",
    "Desert Safari & Dune Bashing",
    "Dubai Mall & Fountain Show",
    "Dubai Marina Yacht Cruise",
    "Gold & Spice Souks Exploration",
    "Palm Jumeirah & Beach Clubs",
    "Traditional Abra Boat Crossing",
    "Miracle Garden & Frame Views",
  ],
  coorg: [
    "Coffee Plantation & Bean Roasting",
    "Abbey & Iruppu Waterfalls",
    "Namdroling Golden Temple (Bylakuppe)",
    "Raja's Seat Sunset Viewpoint",
    "Dubare Elephant Camp",
    "Coorg Pandi Curry Tasting",
    "Tadiandamol Peak Trek",
    "Mandalpatti 4x4 Jeep Safari",
  ],
  wayanad: [
    "Banasura Sagar Dam Speedboating",
    "Edakkal Prehistoric Caves",
    "Chembra Peak & Heart Lake Trek",
    "Soochipara Waterfalls",
    "Wayanad Wildlife Sanctuary Safari",
    "Bamboo Forest Trails",
    "Kuruva Island River Rafting",
    "Pookode Lake Pedal Boating",
  ],
  kodaikanal: [
    "Kodaikanal Star Lake Boating",
    "Coaker's Walk Valley Vistas",
    "Pillar Rocks & Guna Caves",
    "Silver Cascade & Bear Shola Falls",
    "Pine Forest Cinematic Trails",
    "Bryant Park Floral Displays",
    "Dolphin's Nose Cliff Trek",
    "Homemade Chocolates & Spices",
  ],
  hampi: [
    "Virupaksha Temple Heritage",
    "Vijaya Vittala Stone Chariot",
    "Matanga Hill Sunrise Panorama",
    "Coracle Boat Ride on Tungabhadra",
    "Royal Enclosure & Lotus Mahal",
    "Sanapur Lake Bouldering & Cliff Jumps",
    "Hippie Island Cafes & Biking",
    "Sunset at Hemakuta Hill",
  ],
  jaipur: [
    "Amber Fort & Palace Architecture",
    "Hawa Mahal (Palace of Winds)",
    "City Palace Royal Courtyards",
    "Jantar Mantar Astronomical Marvel",
    "Nahargarh Fort Sunset Views",
    "Johari Bazaar Gem & Textile Shopping",
    "Authentic Dal Baati Churma Feast",
    "Chokhi Dhani Cultural Village",
  ],
  agra: [
    "Taj Mahal Sunrise Experience",
    "Agra Fort Mughal Palaces",
    "Mehtab Bagh Reflection View",
    "Fatehpur Sikri Imperial City",
    "Petha Tasting in Sadar Bazaar",
    "Mughlai Cuisine & Biryani Trail",
    "Marble Inlay Handicraft Workshops",
  ],
  manali: [
    "Solang Valley Paragliding & Zorbing",
    "Rohtang Pass Snow Experience",
    "Old Manali Cafes & Live Music",
    "Hadimba Temple Cedar Forest",
    "Jogini Waterfalls Nature Trek",
    "Vashisht Natural Hot Springs",
    "River Rafting in Beas River",
    "Mall Road Shopping & Trout Fish",
  ],
  bali: [
    "Ubud Monkey Forest & Rice Terraces",
    "Tanah Lot & Uluwatu Sunset Temples",
    "Mount Batur Sunrise Volcano Trek",
    "Kecak Fire Dance Performance",
    "Nusa Penida Kelingking Beach Tour",
    "Tegallalang Giant Jungle Swing",
    "Seminyak & Canggu Beach Clubs",
    "Balinese Coffee & Luwak Tasting",
  ],
  singapore: [
    "Gardens by the Bay & Supertree Grove",
    "Marina Bay Sands SkyPark Observation",
    "Sentosa Island & Universal Studios",
    "Chinatown & Little India Food Trails",
    "Jewel Changi Rain Vortex",
    "Night Safari Wildlife Tram",
    "Singapore Flyer Giant Wheel",
    "Clarke Quay Riverside Dining",
  ],
  london: [
    "Big Ben & Palace of Westminster",
    "Tower of London & Tower Bridge",
    "British Museum World Artifacts",
    "London Eye Thames Panorama",
    "Buckingham Palace Changing of Guard",
    "West End Theatre Musicals",
    "Borough Market Street Food",
    "Hyde Park & Kensington Gardens",
  ],
  alleppey: [
    "Traditional Houseboat Cruise",
    "Backwater Kayaking & Canals",
    "Marari Beach Serenity",
    "Village Coir & Canoe Making",
    "Toddy Shop Fresh Karimeen Fish",
    "Kuttanad Below-Sea Farming",
    "Alappuzha Lighthouse & Pier",
  ],
};

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
  const [selectedInterests, setSelectedInterests] = useState<string[]>([]);
  const [customInterestInput, setCustomInterestInput] = useState("");
  const [customInterestsList, setCustomInterestsList] = useState<string[]>([]);
  const [focusPoints, setFocusPoints] = useState<string[]>(DEFAULT_FOCUS_POINTS);
  const [focusSource, setFocusSource] = useState<string>("default");

  const [loading, setLoading] = useState(false);
  const [aiProcessingStage, setAiProcessingStage] = useState(0);
  const [error, setError] = useState("");

  // Dynamically calibrate Activity & Interest Focus Points based on Google Travel Ideas & Dataset
  useEffect(() => {
    const dest = destination.trim().toLowerCase();
    if (!dest) {
      setFocusPoints(DEFAULT_FOCUS_POINTS);
      setFocusSource("default");
      return;
    }

    // 1. Instant client-side lookup from Google Travel Ideas map (0ms latency)
    let matchedPreset: string[] | null = null;
    for (const [key, points] of Object.entries(DESTINATION_FOCUS_POINTS_MAP)) {
      if (dest.includes(key) || key.includes(dest)) {
        matchedPreset = points;
        break;
      }
    }

    if (matchedPreset) {
      setFocusPoints(matchedPreset);
      setFocusSource("google_ideas");
    } else {
      const destTitle = destination.trim();
      setFocusPoints([
        `${destTitle} Heritage & Historic Old Town`,
        `${destTitle} Panoramic Sunset Viewpoints`,
        `Regional Street Food & Local Cuisines`,
        `Local Artisan Handicrafts & Bazaars`,
        `${destTitle} Nature Trails & Green Enclaves`,
        `Iconic Landmarks & Photo Spots`,
        `Cultural Traditions & Folk Highlights`,
        `Waterfront & Scenic Promenade`,
      ]);
      setFocusSource("synthesized");
    }

    // 2. Enrich from backend dataset API
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    fetch(`${apiUrl}/api/destinations/focus-points?destination=${encodeURIComponent(destination.trim())}`)
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => {
        if (data && Array.isArray(data.focus_points) && data.focus_points.length > 0) {
          setFocusPoints(data.focus_points);
          setFocusSource(data.source || "dataset");
        }
      })
      .catch(() => {
        // preserve current instant lookup
      });
  }, [destination]);

  // Auth guard & destination param pre-fill
  useEffect(() => {
    const token = localStorage.getItem("tripgenius_token");
    if (!token) {
      router.push("/login");
    }

    const paramDest = searchParams?.get("destination");
    const paramDuration = searchParams?.get("duration");

    if (paramDest) {
      const parsed = parseDestinationQuery(paramDest);
      setDestination(parsed.destination || paramDest);
      if (paramDuration) {
        const d = parseInt(paramDuration);
        if (!isNaN(d) && d > 0) setDurationDays(d);
      } else if (parsed.isCustomDuration) {
        setDurationDays(parsed.duration);
      }
    } else if (paramDuration) {
      const d = parseInt(paramDuration);
      if (!isNaN(d) && d > 0) setDurationDays(d);
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
    <div
      className="page-container"
      style={{
        maxWidth: "780px",
        width: "90%",
        margin: "0 auto",
        padding: "24px 16px",
      }}
    >
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
          { step: 2, stepName: "Duration & Budget", icon: IndianRupee },
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
        <GlassCard style={{ padding: "30px 24px" }}>
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
                  gridTemplateColumns: "1fr",
                  gap: "24px",
                }}
              >
                {/* DURATION (DAYS) */}
                <div>
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "space-between",
                      marginBottom: "10px",
                    }}
                  >
                    <label
                      style={{
                        fontSize: "0.90rem",
                        fontWeight: 600,
                        color: "#E2E8F0",
                      }}
                    >
                      Duration (Days)
                    </label>
                    <span style={{ fontSize: "0.82rem", color: "#38BDF8", fontWeight: 700 }}>
                      {durationDays} Day{durationDays > 1 ? "s" : ""} Selected
                    </span>
                  </div>

                  <div
                    style={{
                      display: "flex",
                      flexWrap: "wrap",
                      gap: "10px",
                      alignItems: "center",
                    }}
                  >
                    {[
                      { label: "3 Days (Weekend)", days: 3 },
                      { label: "5 Days (Standard)", days: 5 },
                      { label: "7 Days (Week)", days: 7 },
                    ].map((item) => {
                      const isSelected = durationDays === item.days;
                      return (
                        <button
                          key={item.days}
                          type="button"
                          onClick={() => setDurationDays(item.days)}
                          style={{
                            padding: "9px 16px",
                            borderRadius: "10px",
                            background: isSelected
                              ? "rgba(14, 165, 233, 0.22)"
                              : "rgba(255, 255, 255, 0.05)",
                            border: isSelected
                              ? "1px solid #38BDF8"
                              : "1px solid rgba(255, 255, 255, 0.12)",
                            color: isSelected ? "#38BDF8" : "#94A3B8",
                            fontSize: "0.85rem",
                            fontWeight: isSelected ? 700 : 500,
                            cursor: "pointer",
                            transition: "all 0.18s ease",
                          }}
                        >
                          {item.label}
                        </button>
                      );
                    })}

                    {/* Custom Days Input without +/- icons */}
                    <div
                      style={{
                        display: "inline-flex",
                        alignItems: "center",
                        gap: "6px",
                        background: "rgba(255, 255, 255, 0.04)",
                        border: "1px solid rgba(255, 255, 255, 0.12)",
                        borderRadius: "10px",
                        padding: "4px 10px",
                      }}
                    >
                      <span style={{ fontSize: "0.78rem", color: "#94A3B8" }}>Custom:</span>
                      <input
                        type="number"
                        min="1"
                        max="30"
                        value={durationDays === 0 ? "" : durationDays}
                        onFocus={(e) => e.target.select()}
                        onChange={(e) => {
                          const str = e.target.value;
                          if (!str) {
                            setDurationDays(0);
                            return;
                          }
                          const val = parseInt(str);
                          if (!isNaN(val)) {
                            setDurationDays(Math.max(1, Math.min(30, val)));
                          }
                        }}
                        onBlur={() => {
                          if (!durationDays || durationDays < 1) {
                            setDurationDays(1);
                          }
                        }}
                        style={{
                          width: "55px",
                          textAlign: "center",
                          fontSize: "0.95rem",
                          fontWeight: 700,
                          background: "transparent",
                          border: "none",
                          color: "#FFFFFF",
                          outline: "none",
                        }}
                      />
                      <span style={{ fontSize: "0.78rem", color: "#64748B" }}>days</span>
                    </div>
                  </div>
                </div>

                {/* TRAVELERS COUNT */}
                <div>
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "space-between",
                      marginBottom: "10px",
                    }}
                  >
                    <label
                      style={{
                        fontSize: "0.90rem",
                        fontWeight: 600,
                        color: "#E2E8F0",
                      }}
                    >
                      Travelers Count
                    </label>
                    <span style={{ fontSize: "0.82rem", color: "#38BDF8", fontWeight: 700 }}>
                      {travelersCount} Traveler{travelersCount > 1 ? "s" : ""}
                    </span>
                  </div>

                  <div
                    style={{
                      display: "flex",
                      flexWrap: "wrap",
                      gap: "8px",
                      alignItems: "center",
                    }}
                  >
                    {[
                      { label: "Solo (1)", count: 1 },
                      { label: "Couple (2)", count: 2 },
                      { label: "Friends (6)", count: 6 },
                      { label: "Group (15)", count: 15 },
                      { label: "🎓 College (50)", count: 50 },
                      { label: "🚌 Mega Tour (100+)", count: 100 },
                    ].map((preset) => {
                      const isSelected = travelersCount === preset.count;
                      return (
                        <button
                          key={preset.count}
                          type="button"
                          onClick={() => setTravelersCount(preset.count)}
                          style={{
                            fontSize: "0.82rem",
                            padding: "8px 14px",
                            borderRadius: "10px",
                            border: isSelected
                              ? "1px solid #38BDF8"
                              : "1px solid rgba(255, 255, 255, 0.12)",
                            background: isSelected
                              ? "rgba(14, 165, 233, 0.22)"
                              : "rgba(255, 255, 255, 0.05)",
                            color: isSelected ? "#38BDF8" : "#CBD5E1",
                            cursor: "pointer",
                            fontWeight: isSelected ? 700 : 500,
                            transition: "all 0.18s ease",
                          }}
                        >
                          {preset.label}
                        </button>
                      );
                    })}

                    {/* Custom Travelers Input without +/- icons */}
                    <div
                      style={{
                        display: "inline-flex",
                        alignItems: "center",
                        gap: "6px",
                        background: "rgba(255, 255, 255, 0.04)",
                        border: "1px solid rgba(255, 255, 255, 0.12)",
                        borderRadius: "10px",
                        padding: "4px 10px",
                      }}
                    >
                      <span style={{ fontSize: "0.78rem", color: "#94A3B8" }}>Custom:</span>
                      <input
                        type="number"
                        min="1"
                        max="500"
                        value={travelersCount === 0 ? "" : travelersCount}
                        onFocus={(e) => e.target.select()}
                        onChange={(e) => {
                          const str = e.target.value;
                          if (!str) {
                            setTravelersCount(0);
                            return;
                          }
                          const val = parseInt(str);
                          if (!isNaN(val)) {
                            setTravelersCount(Math.max(1, Math.min(500, val)));
                          }
                        }}
                        onBlur={() => {
                          if (!travelersCount || travelersCount < 1) {
                            setTravelersCount(1);
                          }
                        }}
                        style={{
                          width: "55px",
                          textAlign: "center",
                          fontSize: "0.95rem",
                          fontWeight: 700,
                          background: "transparent",
                          border: "none",
                          color: "#FFFFFF",
                          outline: "none",
                        }}
                      />
                      <span style={{ fontSize: "0.78rem", color: "#64748B" }}>people</span>
                    </div>
                  </div>

                  {travelersCount >= 30 && (
                    <div
                      style={{
                        marginTop: "10px",
                        padding: "8px 12px",
                        borderRadius: "8px",
                        background: "rgba(14, 165, 233, 0.1)",
                        border: "1px solid rgba(14, 165, 233, 0.25)",
                        fontSize: "0.78rem",
                        color: "#38BDF8",
                      }}
                    >
                      🎓 <b>Large Group / College Trip Mode:</b> Accommodations & transport will auto-scale for bulk coach fleets and group stays.
                    </div>
                  )}
                </div>
              </div>

              {/* TOTAL ESTIMATED BUDGET (₹) WITH 3 OPTIONS (NO DRAG SLIDER) */}
              <div className="space-y-4">
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "flex-end",
                    marginBottom: "8px",
                    flexWrap: "wrap",
                    gap: "10px",
                  }}
                >
                  <div>
                    <label
                      style={{
                        fontSize: "0.90rem",
                        fontWeight: 600,
                        color: "#E2E8F0",
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
                    <span style={{ color: "#38BDF8", fontWeight: 700, fontSize: "1.1rem" }}>₹</span>
                    <input
                      type="number"
                      min="1000"
                      max="5000000"
                      step="500"
                      value={budget === 0 ? "" : budget}
                      onFocus={(e) => e.target.select()}
                      onChange={(e) => {
                        const str = e.target.value;
                        if (!str) {
                          setBudget(0);
                          return;
                        }
                        const val = parseInt(str);
                        if (!isNaN(val)) {
                          setBudget(Math.max(0, val));
                        }
                      }}
                      onBlur={() => {
                        if (!budget || budget < 1000) {
                          setBudget(1000);
                        }
                      }}
                      className="input-base"
                      style={{
                        width: "140px",
                        textAlign: "right",
                        fontSize: "1.15rem",
                        fontWeight: 800,
                        color: "#38BDF8",
                        padding: "8px 14px",
                        borderRadius: "10px",
                      }}
                    />
                  </div>
                </div>

                {/* THREE BUDGET OPTIONS */}
                <div>
                  <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: "10px" }}>
                    {[
                      { label: "🎒 Budget", perDayPerson: 1500, style: "Hostels, trains, local dining", desc: "Best for smart travelers" },
                      { label: "🌟 Comfort", perDayPerson: 3500, style: "3-star hotels, cabs, restaurants", desc: "Most popular choice" },
                      { label: "💎 Luxury", perDayPerson: 8000, style: "5-star resorts, private cars, fine dining", desc: "Premium experience" },
                    ].map((tier) => {
                      const calculatedTotal = tier.perDayPerson * durationDays * travelersCount;
                      const isSelected = Math.abs(budget - calculatedTotal) < 1500;

                      return (
                        <button
                          key={tier.label}
                          type="button"
                          onClick={() => setBudget(calculatedTotal)}
                          style={{
                            padding: "12px 16px",
                            borderRadius: "12px",
                            background: isSelected
                              ? "rgba(14, 165, 233, 0.22)"
                              : "rgba(255, 255, 255, 0.05)",
                            border: isSelected
                              ? "1px solid #38BDF8"
                              : "1px solid rgba(255, 255, 255, 0.10)",
                            color: isSelected ? "#38BDF8" : "#CBD5E1",
                            cursor: "pointer",
                            transition: "all 0.2s ease",
                            textAlign: "left",
                          }}
                        >
                          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "4px" }}>
                            <span style={{ fontWeight: 700, fontSize: "0.90rem" }}>{tier.label}</span>
                            <span style={{ color: "#10B981", fontSize: "0.85rem", fontWeight: 700 }}>
                              ₹{calculatedTotal.toLocaleString("en-IN")}
                            </span>
                          </div>
                          <div style={{ fontSize: "0.75rem", color: "#94A3B8" }}>
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
                    const isNoStay = acc.id === "NoStay";
                    return (
                      <div
                        key={acc.id}
                        onClick={() => setPreferredAccommodation(acc.id)}
                        style={{
                          padding: "14px",
                          borderRadius: "12px",
                          background: isSelected
                            ? isNoStay
                              ? "rgba(251, 146, 60, 0.15)"
                              : "rgba(14, 165, 233, 0.15)"
                            : "rgba(255, 255, 255, 0.04)",
                          border: isSelected
                            ? isNoStay
                              ? "1px solid #FB923C"
                              : "1px solid #38BDF8"
                            : isNoStay
                            ? "1px dashed rgba(251, 146, 60, 0.35)"
                            : "1px solid rgba(255, 255, 255, 0.08)",
                          cursor: "pointer",
                          transition: "all 0.2s ease",
                        }}
                      >
                        <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "4px" }}>
                          <span style={{ fontSize: "1.1rem" }}>{acc.icon}</span>
                          <h5
                            style={{
                              fontSize: "0.9rem",
                              fontWeight: 700,
                              color: isSelected
                                ? isNoStay ? "#FB923C" : "#38BDF8"
                                : "#FFFFFF",
                            }}
                          >
                            {acc.label}
                          </h5>
                        </div>
                        <p
                          style={{
                            fontSize: "0.75rem",
                            color: isNoStay ? "#94A3B8" : "#94A3B8",
                            marginTop: "2px",
                          }}
                        >
                          {acc.desc}
                        </p>
                        {isNoStay && (
                          <p style={{ fontSize: "0.68rem", color: "#FB923C", marginTop: "4px", fontStyle: "italic" }}>
                            💡 Budget will exclude hotel costs
                          </p>
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>

              <div>
                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                    flexWrap: "wrap",
                    gap: "8px",
                    marginBottom: "12px",
                  }}
                >
                  <label
                    style={{
                      fontSize: "0.92rem",
                      fontWeight: 700,
                      color: "#FFFFFF",
                      margin: 0,
                    }}
                  >
                    Activity & Interest Focus{" "}
                    {destination ? (
                      <span style={{ color: "#38BDF8" }}>for {destination}</span>
                    ) : null}{" "}
                    {selectedInterests.length > 0 ? (
                      <span style={{ color: "#34D399", fontSize: "0.82rem" }}>
                        ({selectedInterests.length} selected)
                      </span>
                    ) : (
                      <span style={{ color: "#94A3B8", fontWeight: 400, fontSize: "0.82rem" }}>
                        (Pick focus points or add your own)
                      </span>
                    )}
                  </label>

                  <Badge variant="overlay" size="sm">
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
                    {focusSource === "google_ideas"
                      ? "Google Ideas & Verified Intelligence"
                      : focusSource === "dataset"
                      ? "Tourism Dataset Focus Points"
                      : "Dynamic Focus Intelligence"}
                  </Badge>
                </div>

                <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
                  {[...focusPoints, ...customInterestsList].map((tag) => {
                    const isSelected = selectedInterests.includes(tag);
                    const isCustom = customInterestsList.includes(tag);
                    return (
                      <button
                        key={tag}
                        type="button"
                        onClick={() => toggleInterest(tag)}
                        style={{
                          padding: "8px 16px",
                          borderRadius: "999px",
                          background: isSelected
                            ? "linear-gradient(135deg, rgba(14, 165, 233, 0.35), rgba(20, 184, 166, 0.35))"
                            : "rgba(255, 255, 255, 0.05)",
                          border: isSelected
                            ? "1px solid #38BDF8"
                            : "1px solid rgba(255, 255, 255, 0.12)",
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
                        {isSelected ? (
                          <Check size={14} color="#38BDF8" />
                        ) : (
                          <Sparkles size={12} color="rgba(255, 255, 255, 0.3)" />
                        )}
                        <span>{tag}</span>
                        {isCustom && (
                          <span
                            onClick={(e) => {
                              e.stopPropagation();
                              setCustomInterestsList((prev) =>
                                prev.filter((t) => t !== tag),
                              );
                              setSelectedInterests((prev) =>
                                prev.filter((t) => t !== tag),
                              );
                            }}
                            style={{
                              marginLeft: "4px",
                              color: "#94A3B8",
                              fontSize: "1rem",
                              lineHeight: 1,
                              padding: "0 2px",
                            }}
                            title="Remove custom idea"
                          >
                            ×
                          </span>
                        )}
                      </button>
                    );
                  })}
                </div>

                {/* ADD USER'S OWN IDEAS INPUT */}
                <form
                  onSubmit={(e) => {
                    e.preventDefault();
                    const trimmed = customInterestInput.trim();
                    if (trimmed) {
                      if (
                        !customInterestsList.includes(trimmed) &&
                        !focusPoints.includes(trimmed)
                      ) {
                        setCustomInterestsList((prev) => [...prev, trimmed]);
                      }
                      if (!selectedInterests.includes(trimmed)) {
                        setSelectedInterests((prev) => [...prev, trimmed]);
                      }
                      setCustomInterestInput("");
                    }
                  }}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "8px",
                    marginTop: "14px",
                    maxWidth: "460px",
                  }}
                >
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: "8px",
                      flex: 1,
                      background: "rgba(255, 255, 255, 0.05)",
                      border: "1px solid rgba(255, 255, 255, 0.12)",
                      borderRadius: "999px",
                      padding: "6px 14px",
                    }}
                  >
                    <Sparkles size={14} color="#38BDF8" />
                    <input
                      type="text"
                      value={customInterestInput}
                      onChange={(e) => setCustomInterestInput(e.target.value)}
                      placeholder="Add your own ideas (e.g. Campfire, Scuba, Stargazing)..."
                      style={{
                        background: "transparent",
                        border: "none",
                        outline: "none",
                        color: "#FFFFFF",
                        fontSize: "0.82rem",
                        width: "100%",
                      }}
                    />
                  </div>
                  <button
                    type="submit"
                    disabled={!customInterestInput.trim()}
                    style={{
                      background: customInterestInput.trim()
                        ? "linear-gradient(135deg, #0EA5E9, #14B8A6)"
                        : "rgba(255, 255, 255, 0.06)",
                      color: customInterestInput.trim() ? "#FFFFFF" : "#64748B",
                      border: "none",
                      borderRadius: "999px",
                      padding: "8px 16px",
                      fontSize: "0.82rem",
                      fontWeight: 600,
                      cursor: customInterestInput.trim()
                        ? "pointer"
                        : "default",
                      whiteSpace: "nowrap",
                      transition: "all 0.15s ease",
                    }}
                  >
                    + Add Idea
                  </button>
                </form>
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
