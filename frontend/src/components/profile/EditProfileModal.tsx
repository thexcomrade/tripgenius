"use client";

import { useEffect, useState } from "react";

interface UserProfile {
  uid?: string;
  tripgenius_id?: string;
  full_name: string;
  username: string;
  email?: string;
  bio: string;
  country: string;
  profile_image?: string;
  total_trips?: number;
  saved_trips?: number;
  eco_score?: number;
  countries_visited?: number;
  is_verified?: boolean;
  created_at?: string;
  travel_preferences: string[];
}

interface EditProfileModalProps {
  isOpen: boolean;
  onClose: () => void;
  user: UserProfile;
  onSave: (updatedProfile: Partial<UserProfile>) => void;
}

const AVAILABLE_PREFERENCES = [
  "Adventure",
  "Beach",
  "Luxury",
  "Budget",
  "Road Trips",
  "Eco Tourism",
  "Wildlife",
  "Food",
  "Photography",
  "Mountains",
  "Camping",
  "Backpacking",
];

export default function EditProfileModal({
  isOpen,
  onClose,
  user: initialUser,
  onSave,
}: EditProfileModalProps) {
  const [user, setUser] = useState<UserProfile>({
    full_name: "",
    username: "",
    bio: "",
    country: "",
    travel_preferences: [],
  });

  useEffect(() => {
    if (!isOpen) return;

    setUser({
      full_name: initialUser.full_name ?? "",

      username: initialUser.username ?? "",

      bio:
        initialUser.bio &&
        !initialUser.bio.includes("Healthcare Professional") &&
        !initialUser.bio.includes("Dr. Sivya Menon")
          ? initialUser.bio
          : "Passionate traveler based in Trivandrum / Kochi. Loves mindful journeys, peaceful coastal getaways, and exploring authentic cultural sanctuaries.",

      country: initialUser.country ?? "India",

      travel_preferences: initialUser.travel_preferences ?? [],
    });
  }, [isOpen, initialUser]);

  function updateField(field: keyof UserProfile, value: string | string[]) {
    setUser((previous) => ({
      ...previous,
      [field]: value,
    }));
  }

  function togglePreference(preference: string) {
    const exists = user.travel_preferences.includes(preference);

    if (exists) {
      updateField(
        "travel_preferences",
        user.travel_preferences.filter((item) => item !== preference),
      );
    } else {
      updateField("travel_preferences", [
        ...user.travel_preferences,
        preference,
      ]);
    }
  }

  function handleSave() {
    onSave({
      full_name: user.full_name,
      username: user.username,
      bio: user.bio,
      country: user.country,
      travel_preferences: user.travel_preferences,
    });

    onClose();
  }

  if (!isOpen) {
    return null;
  }

  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        zIndex: 9999,
        background: "rgba(0,0,0,0.75)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: "20px",
      }}
    >
      <div
        className="glass-card"
        style={{
          width: "100%",
          maxWidth: "700px",
          maxHeight: "90vh",
          overflowY: "auto",
          padding: "30px",
        }}
      >
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: "25px",
          }}
        >
          <h2>Edit Profile</h2>

          <button
            onClick={onClose}
            style={{
              border: "none",
              background: "transparent",
              color: "#ffffff",
              fontSize: "1.4rem",
              cursor: "pointer",
            }}
          >
            ✕
          </button>
        </div>

        <div
          style={{
            display: "grid",
            gap: "18px",
          }}
        >
          <div>
            <label>Full Name</label>

            <input
              type="text"
              value={user.full_name}
              onChange={(event) => updateField("full_name", event.target.value)}
              className="newsletter-input"
              style={{
                width: "100%",
                marginTop: "8px",
              }}
            />
          </div>

          <div>
            <label>Username</label>

            <input
              type="text"
              value={user.username}
              onChange={(event) => updateField("username", event.target.value)}
              className="newsletter-input"
              style={{
                width: "100%",
                marginTop: "8px",
              }}
            />
          </div>

          <div>
            <label>Bio</label>

            <textarea
              value={user.bio}
              onChange={(event) => updateField("bio", event.target.value)}
              rows={4}
              className="newsletter-input"
              style={{
                width: "100%",
                marginTop: "8px",
                resize: "vertical",
              }}
            />
          </div>

          <div>
            <label>Country</label>

            <input
              type="text"
              value={user.country}
              onChange={(event) => updateField("country", event.target.value)}
              className="newsletter-input"
              style={{
                width: "100%",
                marginTop: "8px",
              }}
            />
          </div>

          <div>
            <label>Travel Preferences</label>

            <div
              style={{
                display: "flex",
                flexWrap: "wrap",
                gap: "10px",
                marginTop: "12px",
              }}
            >
              {AVAILABLE_PREFERENCES.map((preference) => (
                <button
                  key={preference}
                  type="button"
                  onClick={() => togglePreference(preference)}
                  style={{
                    padding: "10px 16px",
                    borderRadius: "999px",
                    border: "none",
                    cursor: "pointer",
                    background: user.travel_preferences.includes(preference)
                      ? "#0EA5E9"
                      : "rgba(255,255,255,0.08)",
                    color: "#ffffff",
                  }}
                >
                  {preference}
                </button>
              ))}
            </div>
          </div>
        </div>

        <div
          style={{
            display: "flex",
            justifyContent: "flex-end",
            gap: "12px",
            marginTop: "30px",
          }}
        >
          <button
            type="button"
            onClick={onClose}
            style={{
              padding: "12px 20px",
              borderRadius: "12px",
              border: "1px solid rgba(255,255,255,0.15)",
              background: "transparent",
              color: "#ffffff",
              cursor: "pointer",
            }}
          >
            Cancel
          </button>

          <button
            type="button"
            onClick={handleSave}
            className="btn-primary"
            style={{
              border: "none",
              cursor: "pointer",
            }}
          >
            Save Changes
          </button>
        </div>
      </div>
    </div>
  );
}
