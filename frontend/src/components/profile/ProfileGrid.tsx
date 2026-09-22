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

const SAMPLE_INSPIRATIONS = [
  {
    id: "sample-1",
    title: "Munnar Misty Tea Highlands",
    destination: "Munnar, Kerala",
    duration_days: 3,
    budget: 24000,
    image: "https://images.unsplash.com/photo-1593693397690-362cb9666fc2?auto=format&fit=crop&w=800&q=80",
    travel_style: "Scenic Nature",
  },
  {
    id: "sample-2",
    title: "Varkala Cliffside Coastal Retreat",
    destination: "Varkala, Kerala",
    duration_days: 4,
    budget: 32000,
    image: "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=800&q=80",
    travel_style: "Eco Relaxation",
  },
  {
    id: "sample-3",
    title: "Coorg Coffee & Waterfalls Trail",
    destination: "Coorg, Karnataka",
    duration_days: 3,
    budget: 28000,
    image: "https://images.unsplash.com/photo-1573843981267-be1999ff37cd?auto=format&fit=crop&w=800&q=80",
    travel_style: "Adventure & Heritage",
  },
];

const PREFERENCE_OPTIONS = [
  "Adventure & Trekking",
  "Scenic Highlands & Tea Hills",
  "Coastal & Beaches",
  "Eco Tourism & Sustainable",
  "Local Food & Street Dining",
  "Heritage, Temples & Culture",
  "Wildlife & Nature Reserves",
  "Relaxation & Ayurveda",
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
  const [selectedPrefs, setSelectedPrefs] = useState<string[]>(userPreferences);
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

  // Render My Journeys Tab
  const renderTripsTab = () => {
    const hasSaved = savedTripsList.length > 0;
    const tripsToDisplay = hasSaved ? savedTripsList : SAMPLE_INSPIRATIONS;

    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <Compass className="w-5 h-5 text-sky-400" />
              <span>{hasSaved ? "Your Planned & Generated Journeys" : "Curated Journeys & Inspirations"}</span>
            </h2>
            <p className="text-sm text-slate-400 mt-0.5">
              {hasSaved
                ? `You have ${savedTripsList.length} customized itinerary plans saved.`
                : "Plan your first custom journey with TripGenius AI or browse suggestions."}
            </p>
          </div>

          <Link
            href="/planner"
            className="hidden sm:inline-flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold text-white transition-all transform hover:scale-[1.02]"
            style={{
              background: "linear-gradient(135deg, #0EA5E9 0%, #14B8A6 100%)",
            }}
          >
            <PlusCircle className="w-4 h-4" />
            <span>New Journey</span>
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* CREATE NEW JOURNEY ACTION CARD */}
          <Link
            href="/planner"
            className="group flex flex-col items-center justify-center p-8 rounded-2xl border-2 border-dashed border-sky-500/30 hover:border-sky-400 bg-sky-500/[0.03] hover:bg-sky-500/[0.08] transition-all text-center min-h-[260px]"
          >
            <div className="w-14 h-14 rounded-full bg-sky-500/20 text-sky-400 flex items-center justify-center mb-4 group-hover:scale-110 group-hover:bg-sky-500 group-hover:text-white transition-all">
              <PlusCircle className="w-7 h-7" />
            </div>
            <h3 className="text-lg font-bold text-white group-hover:text-sky-300 transition-colors">
              Plan New Adventure
            </h3>
            <p className="text-xs text-slate-400 max-w-xs mt-1 leading-relaxed">
              Synthesize a day-by-day itinerary tailored to your exact budget, style, and destination.
            </p>
          </Link>

          {/* TRIP CARDS */}
          {tripsToDisplay.map((trip: any, idx: number) => {
            const image =
              trip.image ||
              `https://images.unsplash.com/photo-1593693397690-362cb9666fc2?auto=format&fit=crop&w=800&q=80`;

            return (
              <div
                key={trip.id || idx}
                className="group relative flex flex-col overflow-hidden rounded-2xl border border-white/10 bg-slate-900/60 backdrop-blur-xl hover:border-sky-500/50 transition-all duration-300 hover:shadow-2xl hover:shadow-sky-500/10"
              >
                {/* IMAGE COVER */}
                <div className="relative h-44 w-full overflow-hidden">
                  <img
                    src={image}
                    alt={trip.destination || trip.title}
                    className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/40 to-transparent" />

                  {/* Top Badges */}
                  <div className="absolute top-3 left-3 flex items-center gap-2">
                    <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-slate-950/80 text-white backdrop-blur-md border border-white/10 flex items-center gap-1">
                      <Calendar className="w-3 h-3 text-sky-400" />
                      {trip.duration_days} Days
                    </span>
                  </div>

                  <div className="absolute top-3 right-3">
                    <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-500/80 text-white backdrop-blur-md flex items-center gap-0.5">
                      <IndianRupee className="w-3 h-3" />
                      {trip.budget ? Number(trip.budget).toLocaleString("en-IN") : "Optimized"}
                    </span>
                  </div>

                  {/* Destination Tag bottom left */}
                  <div className="absolute bottom-3 left-3 flex items-center gap-1.5 text-xs text-sky-300 font-medium">
                    <MapPin className="w-3.5 h-3.5 text-rose-400" />
                    <span>{trip.destination}</span>
                  </div>
                </div>

                {/* CARD BODY */}
                <div className="flex-1 p-5 flex flex-col justify-between">
                  <div>
                    <h3 className="text-base font-bold text-white line-clamp-1 group-hover:text-sky-300 transition-colors">
                      {trip.trip_title || trip.title || `${trip.destination} Experience`}
                    </h3>
                    <p className="text-xs text-slate-400 mt-1 line-clamp-2 leading-relaxed">
                      {trip.travel_style || "Curated multi-day scenic exploration with tailored dining and activity pacing."}
                    </p>
                  </div>

                  {/* CARD ACTIONS */}
                  <div className="mt-5 pt-4 border-t border-white/10 flex items-center justify-between">
                    <button
                      onClick={() => {
                        if (hasSaved) {
                          localStorage.setItem("tripgenius_generated_trip", JSON.stringify(trip));
                          router.push("/trip/generated");
                        } else {
                          router.push(`/planner?destination=${encodeURIComponent(trip.destination)}`);
                        }
                      }}
                      className="inline-flex items-center gap-1.5 text-xs font-semibold text-sky-400 hover:text-sky-300 transition-colors cursor-pointer"
                    >
                      <span>View Itinerary</span>
                      <ExternalLink className="w-3.5 h-3.5" />
                    </button>

                    {hasSaved && onDeleteSavedTrip && (
                      <button
                        onClick={() => onDeleteSavedTrip(trip.id)}
                        className="p-1.5 rounded-lg text-slate-500 hover:text-rose-400 hover:bg-rose-500/10 transition-colors cursor-pointer"
                        title="Remove from saved"
                      >
                        <Trash2 className="w-4 h-4" />
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

  // Render Saved Tab
  const renderSavedTab = () => {
    if (savedTripsList.length === 0) {
      return (
        <div className="text-center py-16 px-4 rounded-3xl border border-white/10 bg-slate-900/50 backdrop-blur-xl">
          <div className="w-16 h-16 rounded-full bg-amber-500/10 text-amber-400 flex items-center justify-center mx-auto mb-4 border border-amber-500/20">
            <BookmarkCheck className="w-8 h-8" />
          </div>
          <h3 className="text-lg font-bold text-white mb-2">No Saved Trips Yet</h3>
          <p className="text-sm text-slate-400 max-w-md mx-auto mb-6 leading-relaxed">
            When you generate personalized itineraries in the Trip Planner, bookmark your favorites to access them anytime offline or on the go.
          </p>
          <Link
            href="/planner"
            className="inline-flex items-center gap-2 px-6 py-2.5 rounded-xl text-sm font-semibold text-white transition-all shadow-lg"
            style={{
              background: "linear-gradient(135deg, #0EA5E9 0%, #14B8A6 100%)",
            }}
          >
            <Sparkles className="w-4 h-4 text-amber-300" />
            <span>Generate First Trip</span>
          </Link>
        </div>
      );
    }

    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <BookmarkCheck className="w-5 h-5 text-amber-400" />
              <span>Bookmarked Itineraries ({savedTripsList.length})</span>
            </h2>
            <p className="text-sm text-slate-400 mt-0.5">
              Saved plans saved directly to your TripGenius account.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {savedTripsList.map((trip) => (
            <div
              key={trip.id}
              className="group relative flex flex-col rounded-2xl border border-white/10 bg-slate-900/60 backdrop-blur-xl p-5 hover:border-amber-500/40 transition-all hover:shadow-xl hover:shadow-amber-500/5"
            >
              <div className="flex items-start justify-between gap-3">
                <div>
                  <div className="flex items-center gap-1.5 text-xs text-amber-400 font-semibold mb-1">
                    <MapPin className="w-3.5 h-3.5" />
                    <span>{trip.destination}</span>
                  </div>
                  <h3 className="text-base font-bold text-white group-hover:text-amber-300 transition-colors">
                    {trip.trip_title || `${trip.destination} Adventure`}
                  </h3>
                </div>

                {onDeleteSavedTrip && (
                  <button
                    onClick={() => onDeleteSavedTrip(trip.id)}
                    className="p-1.5 rounded-lg text-slate-500 hover:text-rose-400 hover:bg-rose-500/10 transition-colors cursor-pointer"
                    title="Delete Saved Trip"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                )}
              </div>

              <div className="flex items-center gap-3 my-4 text-xs text-slate-300">
                <span className="px-2.5 py-1 rounded-full bg-slate-800 border border-white/5 flex items-center gap-1">
                  <Calendar className="w-3 h-3 text-sky-400" />
                  {trip.duration_days} Days
                </span>
                <span className="px-2.5 py-1 rounded-full bg-slate-800 border border-white/5 flex items-center gap-1">
                  <IndianRupee className="w-3 h-3 text-emerald-400" />
                  ₹{Number(trip.budget).toLocaleString("en-IN")}
                </span>
              </div>

              <button
                onClick={() => {
                  localStorage.setItem("tripgenius_generated_trip", JSON.stringify(trip));
                  router.push("/trip/generated");
                }}
                className="mt-auto w-full py-2 px-4 rounded-xl text-xs font-semibold bg-white/10 hover:bg-white/15 text-white border border-white/10 transition-all flex items-center justify-center gap-1.5 cursor-pointer"
              >
                <span>View Full Itinerary</span>
                <ExternalLink className="w-3.5 h-3.5" />
              </button>
            </div>
          ))}
        </div>
      </div>
    );
  };

  // Render Achievements Tab
  const renderAchievementsTab = () => {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <Award className="w-5 h-5 text-amber-400" />
              <span>Traveler Badges & Milestones</span>
            </h2>
            <p className="text-sm text-slate-400 mt-0.5">
              Unlock achievements as you plan sustainable journeys and explore new destinations.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {achievements.map((ach) => (
            <div
              key={ach.id}
              className={`relative p-6 rounded-2xl border transition-all ${
                ach.unlocked
                  ? "bg-gradient-to-br from-slate-900/90 to-sky-950/40 border-sky-500/30 shadow-lg shadow-sky-500/5"
                  : "bg-slate-900/40 border-white/5 opacity-70"
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="w-12 h-12 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center text-2xl mb-4">
                  {ach.icon}
                </div>

                {ach.unlocked ? (
                  <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[11px] font-semibold bg-emerald-500/15 text-emerald-400 border border-emerald-500/30">
                    <CheckCircle2 className="w-3 h-3" />
                    Unlocked
                  </span>
                ) : (
                  <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[11px] font-medium bg-slate-800 text-slate-400 border border-white/5">
                    <Lock className="w-3 h-3" />
                    In Progress
                  </span>
                )}
              </div>

              <h3 className="text-base font-bold text-white mb-1">{ach.title}</h3>
              <p className="text-xs text-slate-400 leading-relaxed mb-4">{ach.description}</p>

              {/* Status bar */}
              <div className="w-full bg-slate-800/80 rounded-full h-1.5 overflow-hidden">
                <div
                  className={`h-full rounded-full ${
                    ach.unlocked
                      ? "bg-gradient-to-r from-sky-400 to-teal-400 w-full"
                      : "bg-slate-600 w-1/3"
                  }`}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  // Render Preferences Tab
  const renderPreferencesTab = () => {
    return (
      <div className="max-w-3xl mx-auto rounded-3xl border border-white/10 bg-slate-900/60 backdrop-blur-xl p-6 sm:p-8 space-y-6">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-sky-400" />
            <span>Customize Travel Interests & Vibe</span>
          </h2>
          <p className="text-sm text-slate-400 mt-1">
            TripGenius AI incorporates your selected travel preferences to personalize recommended activities, hotels, and itineraries.
          </p>
        </div>

        <div className="flex flex-wrap gap-2.5 pt-2">
          {PREFERENCE_OPTIONS.map((option) => {
            const isSelected = selectedPrefs.includes(option);

            return (
              <button
                key={option}
                type="button"
                onClick={() => togglePreference(option)}
                className={`inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs sm:text-sm font-medium transition-all cursor-pointer ${
                  isSelected
                    ? "bg-sky-500/20 text-sky-300 border border-sky-400/50 shadow-sm shadow-sky-500/20"
                    : "bg-slate-800/60 hover:bg-slate-800 text-slate-300 border border-white/5"
                }`}
              >
                {isSelected && <Check className="w-3.5 h-3.5 text-sky-400" />}
                <span>{option}</span>
              </button>
            );
          })}
        </div>

        <div className="pt-4 border-t border-white/10 flex items-center justify-between">
          <span className="text-xs text-slate-400">
            {selectedPrefs.length} preference{selectedPrefs.length === 1 ? "" : "s"} selected
          </span>

          <button
            onClick={handleSavePreferences}
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-semibold text-white transition-all transform hover:scale-[1.02] active:scale-98 cursor-pointer"
            style={{
              background: "linear-gradient(135deg, #0EA5E9 0%, #14B8A6 100%)",
            }}
          >
            {prefsSaved ? (
              <>
                <Check className="w-4 h-4 text-emerald-300" />
                <span>Saved Successfully!</span>
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4 text-amber-300" />
                <span>Save Travel Preferences</span>
              </>
            )}
          </button>
        </div>
      </div>
    );
  };

  return (
    <section className="w-full max-w-6xl mx-auto px-4">
      {activeTab === "trips" && renderTripsTab()}
      {activeTab === "saved" && renderSavedTab()}
      {activeTab === "achievements" && renderAchievementsTab()}
      {activeTab === "preferences" && renderPreferencesTab()}
    </section>
  );
}
