"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  ShieldCheck,
  Camera,
  Settings,
  Edit3,
  Sparkles,
  MapPin,
  Compass,
  Bookmark,
  Leaf,
  Globe2,
  Copy,
  Check,
} from "lucide-react";

interface UserProfile {
  uid: string;
  tripgenius_id: string;
  full_name: string;
  username: string;
  email: string;
  bio: string;
  country: string;
  profile_image: string;
  total_trips: number;
  saved_trips: number;
  eco_score: number;
  countries_visited: number;
  is_verified: boolean;
  created_at: string;
  travel_preferences: string[];
}

interface ProfileHeaderProps {
  user: UserProfile;
  onSettingsClick: () => void;
  onEditProfileClick: () => void;
  onPhotoClick: () => void;
}

export default function ProfileHeader({
  user,
  onSettingsClick,
  onEditProfileClick,
  onPhotoClick,
}: ProfileHeaderProps) {
  const [copied, setCopied] = useState(false);

  const handleCopyId = () => {
    if (user.tripgenius_id) {
      navigator.clipboard.writeText(user.tripgenius_id);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  // Humanize eco badge rating
  const getEcoRank = (score: number) => {
    if (score >= 80) return { label: "Eco Sentinel", color: "#10B981" };
    if (score >= 60) return { label: "Green Traveler", color: "#14B8A6" };
    return { label: "Conscious Explorer", color: "#38BDF8" };
  };

  const ecoRank = getEcoRank(user.eco_score || 72);

  return (
    <section className="w-full max-w-6xl mx-auto mb-10">
      {/* Background Banner with Ambient Glow */}
      <div
        className="relative overflow-hidden rounded-3xl border border-white/10 p-8 sm:p-10"
        style={{
          background:
            "linear-gradient(135deg, rgba(15, 23, 42, 0.90) 0%, rgba(11, 17, 32, 0.95) 100%)",
          backdropFilter: "blur(24px)",
          WebkitBackdropFilter: "blur(24px)",
          boxShadow: "0 20px 50px rgba(0, 0, 0, 0.4)",
        }}
      >
        {/* Subtle Ambient Radial Accents */}
        <div
          className="absolute -top-24 -right-24 w-80 h-80 rounded-full pointer-events-none opacity-25"
          style={{
            background: "radial-gradient(circle, #0EA5E9 0%, transparent 70%)",
            filter: "blur(50px)",
          }}
        />
        <div
          className="absolute -bottom-24 -left-24 w-80 h-80 rounded-full pointer-events-none opacity-20"
          style={{
            background: "radial-gradient(circle, #10B981 0%, transparent 70%)",
            filter: "blur(50px)",
          }}
        />

        <div className="relative z-10 flex flex-col md:flex-row items-center md:items-start gap-8">
          {/* AVATAR WITH INTERACTIVE CAMERA OVERLAY */}
          <div className="relative group">
            <div
              className="w-32 h-32 sm:w-36 sm:h-36 rounded-full overflow-hidden flex items-center justify-center p-1"
              style={{
                background:
                  "linear-gradient(135deg, #0EA5E9 0%, #14B8A6 50%, #10B981 100%)",
                boxShadow: "0 0 25px rgba(14, 165, 233, 0.35)",
              }}
            >
              <div className="w-full h-full rounded-full overflow-hidden bg-slate-900 flex items-center justify-center">
                {user.profile_image ? (
                  <img
                    src={user.profile_image}
                    alt={user.full_name}
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <span className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-tr from-sky-400 to-teal-200">
                    {(user.full_name || "T").charAt(0).toUpperCase()}
                  </span>
                )}
              </div>
            </div>

            {/* Photo Upload Floating Button */}
            <button
              onClick={onPhotoClick}
              title="Upload new profile picture"
              className="absolute bottom-1 right-1 p-2.5 rounded-full bg-sky-500 hover:bg-sky-400 text-white shadow-lg transition-all transform hover:scale-110 active:scale-95 border-2 border-slate-900 cursor-pointer"
            >
              <Camera className="w-4 h-4" />
            </button>
          </div>

          {/* USER INFO & METRICS */}
          <div className="flex-1 text-center md:text-left">
            {/* TOP ROW: Name + Verified + Action Buttons */}
            <div className="flex flex-col sm:flex-row items-center justify-between gap-4 mb-3">
              <div>
                <div className="flex items-center justify-center md:justify-start gap-2.5 flex-wrap">
                  <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
                    {user.full_name || "Traveler"}
                  </h1>

                  <span
                    className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold"
                    style={{
                      background: "rgba(14, 165, 233, 0.15)",
                      color: "#38BDF8",
                      border: "1px solid rgba(14, 165, 233, 0.3)",
                    }}
                  >
                    <ShieldCheck className="w-3.5 h-3.5 text-sky-400" />
                    Verified Traveler
                  </span>
                </div>

                <div className="flex items-center justify-center md:justify-start gap-3 mt-1 text-sm text-slate-400">
                  <span>@{user.username || "traveler"}</span>
                  <span className="text-slate-600">•</span>
                  <button
                    onClick={handleCopyId}
                    className="inline-flex items-center gap-1.5 text-xs font-mono px-2 py-0.5 rounded bg-slate-800/80 hover:bg-slate-700/80 text-sky-400 border border-white/5 transition-colors cursor-pointer"
                    title="Click to copy Passport ID"
                  >
                    <span>{user.tripgenius_id || "TG-VOYAGER"}</span>
                    {copied ? (
                      <Check className="w-3 h-3 text-emerald-400" />
                    ) : (
                      <Copy className="w-3 h-3 text-slate-400" />
                    )}
                  </button>
                </div>
              </div>

              {/* Header Action Buttons */}
              <div className="flex items-center gap-2.5">
                <button
                  onClick={onEditProfileClick}
                  className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold bg-white/10 hover:bg-white/15 text-white border border-white/10 transition-all cursor-pointer"
                >
                  <Edit3 className="w-4 h-4 text-sky-400" />
                  <span>Edit Profile</span>
                </button>

                <button
                  onClick={onSettingsClick}
                  className="p-2 rounded-xl bg-white/10 hover:bg-white/15 text-slate-300 hover:text-white border border-white/10 transition-all cursor-pointer"
                  title="Account Settings"
                >
                  <Settings className="w-4 h-4" />
                </button>

                <Link
                  href="/planner"
                  className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold text-white transition-all transform hover:scale-[1.02] active:scale-98 shadow-md"
                  style={{
                    background: "linear-gradient(135deg, #0EA5E9 0%, #14B8A6 100%)",
                  }}
                >
                  <Sparkles className="w-4 h-4 text-amber-300" />
                  <span>Plan Trip</span>
                </Link>
              </div>
            </div>

            {/* BIO */}
            <p className="text-slate-300 text-sm sm:text-base leading-relaxed max-w-2xl mt-3 font-normal">
              {user.bio || "Crafting sustainable and scenic adventures across the world with TripGenius AI."}
            </p>

            {/* TAGS & LOCATION */}
            <div className="flex flex-wrap items-center justify-center md:justify-start gap-2 mt-4">
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-slate-800/80 text-slate-300 border border-white/5">
                <MapPin className="w-3.5 h-3.5 text-rose-400" />
                {user.country || "India"}
              </span>

              <span
                className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium"
                style={{
                  background: "rgba(16, 185, 129, 0.15)",
                  color: "#34D399",
                  border: "1px solid rgba(16, 185, 129, 0.3)",
                }}
              >
                <Leaf className="w-3.5 h-3.5 text-emerald-400" />
                {ecoRank.label}
              </span>

              {user.travel_preferences &&
                user.travel_preferences.slice(0, 3).map((pref, idx) => (
                  <span
                    key={idx}
                    className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-slate-800/60 text-slate-400 border border-white/5"
                  >
                    ✨ {pref}
                  </span>
                ))}
            </div>

            {/* QUICK STATS STRIP */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-4 mt-6 pt-6 border-t border-white/10">
              <div className="p-3.5 rounded-2xl bg-white/[0.04] border border-white/5 text-center sm:text-left">
                <div className="flex items-center justify-center sm:justify-start gap-1.5 text-xs text-slate-400 mb-1">
                  <Compass className="w-3.5 h-3.5 text-sky-400" />
                  <span>Journeys Planned</span>
                </div>
                <div className="text-xl sm:text-2xl font-bold text-white">
                  {user.total_trips || 0}
                </div>
              </div>

              <div className="p-3.5 rounded-2xl bg-white/[0.04] border border-white/5 text-center sm:text-left">
                <div className="flex items-center justify-center sm:justify-start gap-1.5 text-xs text-slate-400 mb-1">
                  <Bookmark className="w-3.5 h-3.5 text-amber-400" />
                  <span>Saved Plans</span>
                </div>
                <div className="text-xl sm:text-2xl font-bold text-white">
                  {user.saved_trips || 0}
                </div>
              </div>

              <div className="p-3.5 rounded-2xl bg-white/[0.04] border border-white/5 text-center sm:text-left">
                <div className="flex items-center justify-center sm:justify-start gap-1.5 text-xs text-slate-400 mb-1">
                  <Leaf className="w-3.5 h-3.5 text-emerald-400" />
                  <span>Eco Rating</span>
                </div>
                <div className="text-xl sm:text-2xl font-bold text-emerald-400">
                  {user.eco_score ? `${user.eco_score}%` : "85%"}
                </div>
              </div>

              <div className="p-3.5 rounded-2xl bg-white/[0.04] border border-white/5 text-center sm:text-left">
                <div className="flex items-center justify-center sm:justify-start gap-1.5 text-xs text-slate-400 mb-1">
                  <Globe2 className="w-3.5 h-3.5 text-purple-400" />
                  <span>Regions Explored</span>
                </div>
                <div className="text-xl sm:text-2xl font-bold text-white">
                  {user.countries_visited || 3}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
