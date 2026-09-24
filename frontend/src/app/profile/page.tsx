"use client";

import { useEffect, useState } from "react";
import ProfileHeader from "../../components/profile/ProfileHeader";
import ProfileTabs from "../../components/profile/ProfileTabs";
import ProfileGrid from "../../components/profile/ProfileGrid";
import ProfileSettingsModal from "../../components/profile/ProfileSettingsModal";
import EditProfileModal from "../../components/profile/EditProfileModal";
import { tripService } from "../../services/trip.service";

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

interface Achievement {
  id: number;
  title: string;
  icon: string;
  description: string;
  unlocked: boolean;
  progress?: string;
}

const DEFAULT_ACHIEVEMENTS: Achievement[] = [
  {
    id: 1,
    title: "First Journey",
    icon: "✈️",
    description: "Generated your first AI-crafted travel itinerary",
    unlocked: true,
  },
  {
    id: 2,
    title: "Eco Explorer",
    icon: "🌱",
    description: "Maintained a sustainability score above 75%",
    unlocked: true,
  },
  {
    id: 3,
    title: "Highland Trailblazer",
    icon: "🏔️",
    description: "Explored scenic hill stations like Munnar or Coorg",
    unlocked: true,
  },
  {
    id: 4,
    title: "Budget Architect",
    icon: "💰",
    description: "Planned and paced trips within optimal budget tiers",
    unlocked: false,
  },
  {
    id: 5,
    title: "Coastal Nomad",
    icon: "🌊",
    description: "Planned beach and seaside journeys like Varkala",
    unlocked: false,
  },
  {
    id: 6,
    title: "Global Voyager",
    icon: "🌍",
    description: "Planned itineraries across multiple regional corridors",
    unlocked: false,
  },
];

function generateTripGeniusId() {
  const chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
  let id = "TG-";
  for (let i = 0; i < 6; i++) {
    id += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return id;
}

function generateUID() {
  return "user_" + Date.now() + "_" + Math.random().toString(36).substring(2, 8);
}

export default function ProfilePage() {
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("trips");
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [editProfileOpen, setEditProfileOpen] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [savedTripsList, setSavedTripsList] = useState<any[]>([]);

  const [achievements] = useState<Achievement[]>(DEFAULT_ACHIEVEMENTS);

  const [user, setUser] = useState<UserProfile>({
    uid: generateUID(),
    tripgenius_id: "TG-SB8842",
    full_name: "Sivya Babu",
    username: "sivyababu",
    email: "sivya.babu@tripgenius.com",
    bio: "Passionate traveler based in Trivandrum / Kochi. Loves mindful journeys, peaceful coastal getaways, and exploring authentic cultural sanctuaries.",
    country: "Trivandrum, Kerala, India",
    profile_image: "",
    total_trips: 4,
    saved_trips: 0,
    eco_score: 92,
    countries_visited: 3,
    is_verified: true,
    created_at: new Date().toISOString(),
    travel_preferences: [
      "Scenic Highlands & Tea Hills",
      "Coastal & Beach Escapes",
      "Eco Tourism & Sustainable",
      "Local Food & Street Dining",
      "Peaceful Wellness Retreats",
    ],
  });

  useEffect(() => {
    loadProfile();
  }, []);

  async function loadProfile() {
    try {
      const token = localStorage.getItem("tripgenius_token");
      const storedUser = localStorage.getItem("tripgenius_user");
      const image = localStorage.getItem("tripgenius_profile_image");
      const storedSaved = localStorage.getItem("tripgenius_saved_trips");

      let parsedSaved: any[] = [];
      if (storedSaved) {
        try {
          parsedSaved = JSON.parse(storedSaved);
          if (Array.isArray(parsedSaved)) {
            setSavedTripsList(parsedSaved);
          }
        } catch {
          parsedSaved = [];
        }
      }

      if (token && storedUser) {
        const parsed = JSON.parse(storedUser);
        setIsLoggedIn(true);

        // Fetch statistics if available
        let liveTotalTrips =
          parsed.total_trips ?? (parsedSaved.length > 0 ? parsedSaved.length : 4);
        try {
          const stats = await tripService.getStatistics();
          if (stats && typeof stats.total_trips === "number") {
            liveTotalTrips = stats.total_trips;
          }
        } catch {
          // Keep local fallback
        }

        const name =
          parsed.full_name && parsed.full_name !== "Traveler"
            ? parsed.full_name
            : "Sivya Babu";

        setUser({
          uid: parsed.uid ?? generateUID(),
          tripgenius_id: parsed.tripgenius_id ?? "TG-SB8842",
          full_name: name,
          username: parsed.username && parsed.username !== "voyager" ? parsed.username : "sivyababu",
          email: parsed.email || "sivya.babu@tripgenius.com",
          bio:
            parsed.bio &&
            !parsed.bio.includes("Dr. Sivya Menon") &&
            !parsed.bio.includes("Healthcare Professional")
              ? parsed.bio
              : "Passionate traveler based in Trivandrum / Kochi. Loves mindful journeys, peaceful coastal getaways, and exploring authentic cultural sanctuaries.",
          country:
            parsed.country && parsed.country !== "India"
              ? parsed.country
              : "Trivandrum, Kerala, India",
          profile_image: image || parsed.profile_image || "",
          total_trips: liveTotalTrips,
          saved_trips: parsedSaved.length,
          eco_score: parsed.eco_score ?? 92,
          countries_visited: parsed.countries_visited ?? 3,
          is_verified: parsed.is_verified ?? true,
          created_at: parsed.created_at ?? new Date().toISOString(),
          travel_preferences:
            parsed.travel_preferences && parsed.travel_preferences.length > 0
              ? parsed.travel_preferences
              : [
                  "Scenic Highlands & Tea Hills",
                  "Coastal & Beach Escapes",
                  "Eco Tourism & Sustainable",
                  "Local Food & Street Dining",
                  "Peaceful Wellness Retreats",
                ],
        });
      } else {
        // Fallback for guest visitor
        if (storedUser) {
          const parsed = JSON.parse(storedUser);
          const name =
            parsed.full_name && parsed.full_name !== "Traveler"
              ? parsed.full_name
              : "Sivya Babu";

          setUser((prev) => ({
            ...prev,
            ...parsed,
            full_name: name,
            saved_trips: parsedSaved.length,
          }));
        } else {
          setUser((prev) => ({
            ...prev,
            saved_trips: parsedSaved.length,
          }));
        }
      }
    } catch (error) {
      console.error("Error loading profile:", error);
    } finally {
      setLoading(false);
    }
  }

  function handleProfileSave(updatedProfile: Partial<UserProfile>) {
    const updatedUser = {
      ...user,
      ...updatedProfile,
    };
    setUser(updatedUser);
    localStorage.setItem("tripgenius_user", JSON.stringify(updatedUser));
  }

  function handleDeleteSavedTrip(id: string) {
    const updated = savedTripsList.filter((trip) => trip.id !== id);
    setSavedTripsList(updated);
    localStorage.setItem("tripgenius_saved_trips", JSON.stringify(updated));
    setUser((prev) => ({ ...prev, saved_trips: updated.length }));
  }

  function handleSavePreferences(newPreferences: string[]) {
    const updatedUser = {
      ...user,
      travel_preferences: newPreferences,
    };
    setUser(updatedUser);
    localStorage.setItem("tripgenius_user", JSON.stringify(updatedUser));
  }

  if (loading) {
    return (
      <div className="min-h-[75vh] flex flex-col items-center justify-center gap-3">
        <div className="w-10 h-10 rounded-full border-2 border-sky-400 border-t-transparent animate-spin" />
        <p className="text-sm font-medium text-slate-400">Loading Traveler Profile...</p>
      </div>
    );
  }

  return (
    <>
      <main className="min-h-screen py-10 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <ProfileHeader
          user={user}
          onSettingsClick={() => setSettingsOpen(true)}
          onEditProfileClick={() => setEditProfileOpen(true)}
        />

        <ProfileTabs
          activeTab={activeTab}
          onTabChange={setActiveTab}
          tripsCount={user.total_trips}
          savedCount={savedTripsList.length}
          achievementsCount={achievements.filter((a) => a.unlocked).length}
        />

        <ProfileGrid
          activeTab={activeTab}
          achievements={achievements}
          totalTrips={user.total_trips}
          savedTrips={savedTripsList.length}
          savedTripsList={savedTripsList}
          onDeleteSavedTrip={handleDeleteSavedTrip}
          userPreferences={user.travel_preferences}
          onSavePreferences={handleSavePreferences}
        />
      </main>

      <ProfileSettingsModal
        isOpen={settingsOpen}
        isLoggedIn={isLoggedIn}
        onClose={() => setSettingsOpen(false)}
        onPhotoUpdated={(img) =>
          setUser((prev) => ({ ...prev, profile_image: img }))
        }
      />

      <EditProfileModal
        isOpen={editProfileOpen}
        onClose={() => setEditProfileOpen(false)}
        user={user}
        onSave={handleProfileSave}
      />
    </>
  );
}
