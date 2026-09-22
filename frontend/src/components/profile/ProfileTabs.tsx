"use client";

import React from "react";
import { Compass, Bookmark, Award, Sliders } from "lucide-react";

interface ProfileTabsProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
  tripsCount?: number;
  savedCount?: number;
  achievementsCount?: number;
}

const TABS = [
  {
    id: "trips",
    label: "My Journeys",
    icon: Compass,
    countKey: "trips",
  },
  {
    id: "saved",
    label: "Saved Plans",
    icon: Bookmark,
    countKey: "saved",
  },
  {
    id: "achievements",
    label: "Achievements",
    icon: Award,
    countKey: "achievements",
  },
  {
    id: "preferences",
    label: "Travel Styles",
    icon: Sliders,
  },
];

export default function ProfileTabs({
  activeTab,
  onTabChange,
  tripsCount,
  savedCount,
  achievementsCount,
}: ProfileTabsProps) {
  const getCount = (key?: string) => {
    if (key === "trips" && typeof tripsCount === "number") return tripsCount;
    if (key === "saved" && typeof savedCount === "number") return savedCount;
    if (key === "achievements" && typeof achievementsCount === "number")
      return achievementsCount;
    return undefined;
  };

  return (
    <section className="max-w-6xl mx-auto mb-8 px-2">
      <div
        className="flex items-center justify-start sm:justify-center gap-2 p-1.5 rounded-2xl border border-white/10 overflow-x-auto no-scrollbar"
        style={{
          background: "rgba(15, 23, 42, 0.70)",
          backdropFilter: "blur(16px)",
          WebkitBackdropFilter: "blur(16px)",
        }}
      >
        {TABS.map((tab) => {
          const isActive = activeTab === tab.id;
          const Icon = tab.icon;
          const count = getCount(tab.countKey);

          return (
            <button
              key={tab.id}
              onClick={() => onTabChange(tab.id)}
              className={`flex items-center gap-2.5 px-4 sm:px-5 py-2.5 rounded-xl font-medium text-xs sm:text-sm transition-all whitespace-nowrap cursor-pointer ${
                isActive
                  ? "text-white shadow-lg font-semibold"
                  : "text-slate-400 hover:text-slate-200 hover:bg-white/5"
              }`}
              style={{
                background: isActive
                  ? "linear-gradient(135deg, rgba(14, 165, 233, 0.3) 0%, rgba(20, 184, 166, 0.3) 100%)"
                  : "transparent",
                border: isActive
                  ? "1px solid rgba(14, 165, 233, 0.45)"
                  : "1px solid transparent",
              }}
            >
              <Icon
                className={`w-4 h-4 ${
                  isActive ? "text-sky-400" : "text-slate-400"
                }`}
              />
              <span>{tab.label}</span>

              {typeof count === "number" && (
                <span
                  className={`text-[10px] px-1.5 py-0.5 rounded-full font-mono ${
                    isActive
                      ? "bg-sky-500/20 text-sky-300 border border-sky-400/30"
                      : "bg-white/10 text-slate-400"
                  }`}
                >
                  {count}
                </span>
              )}
            </button>
          );
        })}
      </div>
    </section>
  );
}
