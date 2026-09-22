"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import toast from "react-hot-toast";
import {
  Settings,
  User,
  Shield,
  Bell,
  Sparkles,
  Lock,
  Globe,
  LogOut,
  Trash2,
  Check,
  Save,
} from "lucide-react";
import Button from "../../components/ui/Button";
import Badge from "../../components/ui/Badge";
import { GlassCard, SectionHeader } from "../../components/ui/Card";

export default function SettingsPage() {
  const router = useRouter();

  const [userName, setUserName] = useState("Traveler");
  const [email, setEmail] = useState("user@tripgenius.com");
  const [tripGeniusId, setTripGeniusId] = useState("TG-000000");
  const [isVerified, setIsVerified] = useState(false);

  // Settings states
  const [notifications, setNotifications] = useState(true);
  const [emailUpdates, setEmailUpdates] = useState(true);
  const [tripReminders, setTripReminders] = useState(true);
  const [privateProfile, setPrivateProfile] = useState(false);
  const [showTravelStats, setShowTravelStats] = useState(true);
  const [shareItineraries, setShareItineraries] = useState(false);
  const [ecoPriority, setEcoPriority] = useState(true);
  const [defaultTransit, setDefaultTransit] = useState("Car");

  useEffect(() => {
    const storedUser = localStorage.getItem("tripgenius_user");
    if (storedUser) {
      try {
        const user = JSON.parse(storedUser);
        if (user.full_name) setUserName(user.full_name);
        if (user.email) setEmail(user.email);
        if (user.tripgenius_id) setTripGeniusId(user.tripgenius_id);
        if (user.is_verified) setIsVerified(user.is_verified);
      } catch {
        // ignore
      }
    }

    const savedSettings = localStorage.getItem("tripgenius_settings");
    if (savedSettings) {
      try {
        const s = JSON.parse(savedSettings);
        if (s.notifications !== undefined) setNotifications(s.notifications);
        if (s.emailUpdates !== undefined) setEmailUpdates(s.emailUpdates);
        if (s.tripReminders !== undefined) setTripReminders(s.tripReminders);
        if (s.privateProfile !== undefined) setPrivateProfile(s.privateProfile);
        if (s.showTravelStats !== undefined)
          setShowTravelStats(s.showTravelStats);
        if (s.shareItineraries !== undefined)
          setShareItineraries(s.shareItineraries);
        if (s.ecoPriority !== undefined) setEcoPriority(s.ecoPriority);
        if (s.defaultTransit) setDefaultTransit(s.defaultTransit);
      } catch {
        // ignore
      }
    }
  }, []);

  const handleSaveSettings = () => {
    localStorage.setItem(
      "tripgenius_settings",
      JSON.stringify({
        notifications,
        emailUpdates,
        tripReminders,
        privateProfile,
        showTravelStats,
        shareItineraries,
        ecoPriority,
        defaultTransit,
      }),
    );
    toast.success("Preferences updated successfully");
  };

  const handleLogout = () => {
    localStorage.removeItem("tripgenius_token");
    localStorage.removeItem("tripgenius_user");
    localStorage.removeItem("tripgenius_profile_image");
    router.push("/login");
  };

  const handleDeleteAccount = () => {
    if (
      confirm(
        "Are you sure you want to delete your account? This action is irreversible.",
      )
    ) {
      localStorage.clear();
      router.push("/");
    }
  };

  const Toggle = ({
    checked,
    onChange,
  }: {
    checked: boolean;
    onChange: () => void;
  }) => (
    <div
      onClick={onChange}
      style={{
        width: "44px",
        height: "24px",
        borderRadius: "999px",
        background: checked ? "#0EA5E9" : "rgba(255, 255, 255, 0.15)",
        padding: "2px",
        cursor: "pointer",
        transition: "background 0.2s ease",
        display: "flex",
        alignItems: "center",
      }}
    >
      <div
        style={{
          width: "20px",
          height: "20px",
          borderRadius: "50%",
          background: "#FFFFFF",
          transform: checked ? "translateX(20px)" : "translateX(0px)",
          transition: "transform 0.2s ease",
        }}
      />
    </div>
  );

  return (
    <div
      className="page-container"
      style={{
        maxWidth: "1000px",
        display: "flex",
        flexDirection: "column",
        gap: "32px",
      }}
    >
      {/* HEADER */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "flex-end",
          flexWrap: "wrap",
          gap: "16px",
        }}
      >
        <div>
          <div style={{ display: "inline-flex", marginBottom: "8px" }}>
            <Badge variant="neutral" size="sm" icon={<Settings size={12} />}>
              System Preferences
            </Badge>
          </div>
          <h1
            style={{
              fontSize: "clamp(2rem, 4vw, 2.8rem)",
              fontWeight: 900,
              color: "#FFFFFF",
              letterSpacing: "-0.5px",
            }}
          >
            Account & Platform Settings
          </h1>
          <p
            style={{ color: "#94A3B8", fontSize: "0.95rem", marginTop: "4px" }}
          >
            Manage account credentials, AI planner defaults, notification
            preferences, and privacy controls.
          </p>
        </div>

        <Button
          variant="primary"
          size="md"
          leftIcon={<Save size={16} />}
          onClick={handleSaveSettings}
        >
          Save All Changes
        </Button>
      </div>

      {/* 1. ACCOUNT OVERVIEW CARD */}
      <GlassCard style={{ padding: "28px" }}>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "12px",
            marginBottom: "20px",
          }}
        >
          <div
            style={{
              width: "36px",
              height: "36px",
              borderRadius: "10px",
              background: "rgba(14, 165, 233, 0.15)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "#38BDF8",
            }}
          >
            <User size={20} />
          </div>
          <div>
            <h3
              style={{ fontSize: "1.2rem", fontWeight: 700, color: "#FFFFFF" }}
            >
              Account Identity
            </h3>
            <p style={{ fontSize: "0.82rem", color: "#94A3B8" }}>
              Your TripGenius platform credentials
            </p>
          </div>
        </div>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))",
            gap: "20px",
          }}
        >
          <div>
            <label
              style={{
                display: "block",
                fontSize: "0.82rem",
                fontWeight: 600,
                color: "#CBD5E1",
                marginBottom: "6px",
              }}
            >
              Full Name
            </label>
            <input
              type="text"
              value={userName}
              disabled
              className="input-base"
              style={{ opacity: 0.8 }}
            />
          </div>
          <div>
            <label
              style={{
                display: "block",
                fontSize: "0.82rem",
                fontWeight: 600,
                color: "#CBD5E1",
                marginBottom: "6px",
              }}
            >
              Email Address
            </label>
            <input
              type="email"
              value={email}
              disabled
              className="input-base"
              style={{ opacity: 0.8 }}
            />
          </div>
          <div>
            <label
              style={{
                display: "block",
                fontSize: "0.82rem",
                fontWeight: 600,
                color: "#CBD5E1",
                marginBottom: "6px",
              }}
            >
              TripGenius ID
            </label>
            <input
              type="text"
              value={tripGeniusId}
              disabled
              className="input-base"
              style={{ opacity: 0.8 }}
            />
          </div>
          <div>
            <label
              style={{
                display: "block",
                fontSize: "0.82rem",
                fontWeight: 600,
                color: "#CBD5E1",
                marginBottom: "6px",
              }}
            >
              Verification Status
            </label>
            <div
              style={{ height: "46px", display: "flex", alignItems: "center" }}
            >
              <Badge variant={isVerified ? "eco" : "amber"} size="md">
                {isVerified ? "Verified Traveler" : "Standard Account"}
              </Badge>
            </div>
          </div>
        </div>
      </GlassCard>

      {/* 2. TRAVEL & AI PREFERENCES */}
      <GlassCard style={{ padding: "28px" }}>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "12px",
            marginBottom: "20px",
          }}
        >
          <div
            style={{
              width: "36px",
              height: "36px",
              borderRadius: "10px",
              background: "rgba(20, 184, 166, 0.15)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "#2DD4BF",
            }}
          >
            <Sparkles size={20} />
          </div>
          <div>
            <h3
              style={{ fontSize: "1.2rem", fontWeight: 700, color: "#FFFFFF" }}
            >
              AI & Travel Defaults
            </h3>
            <p style={{ fontSize: "0.82rem", color: "#94A3B8" }}>
              Automate itinerary synthesis parameters
            </p>
          </div>
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: "18px" }}>
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              paddingBottom: "14px",
              borderBottom: "1px solid rgba(255, 255, 255, 0.06)",
            }}
          >
            <div>
              <h4
                style={{
                  fontSize: "0.95rem",
                  fontWeight: 600,
                  color: "#FFFFFF",
                }}
              >
                Prioritize Eco-Certified Sanctuaries
              </h4>
              <p style={{ fontSize: "0.82rem", color: "#94A3B8" }}>
                Auto-weight low-emission stays and electric transit options
              </p>
            </div>
            <Toggle
              checked={ecoPriority}
              onChange={() => setEcoPriority(!ecoPriority)}
            />
          </div>

          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
          >
            <div>
              <h4
                style={{
                  fontSize: "0.95rem",
                  fontWeight: 600,
                  color: "#FFFFFF",
                }}
              >
                Default Transportation Mode
              </h4>
              <p style={{ fontSize: "0.82rem", color: "#94A3B8" }}>
                Initial vehicle selection when opening the planner
              </p>
            </div>
            <select
              value={defaultTransit}
              onChange={(e) => setDefaultTransit(e.target.value)}
              style={{
                padding: "8px 14px",
                borderRadius: "10px",
                background: "rgba(15, 23, 42, 0.85)",
                border: "1px solid rgba(255, 255, 255, 0.12)",
                color: "#FFFFFF",
                outline: "none",
              }}
            >
              <option value="Car">Private Car / Taxi</option>
              <option value="Train">Scenic Train</option>
              <option value="Bus">Express Bus</option>
              <option value="Flight">Flight + Transit</option>
            </select>
          </div>
        </div>
      </GlassCard>

      {/* 3. NOTIFICATION CONTROLS */}
      <GlassCard style={{ padding: "28px" }}>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "12px",
            marginBottom: "20px",
          }}
        >
          <div
            style={{
              width: "36px",
              height: "36px",
              borderRadius: "10px",
              background: "rgba(245, 158, 11, 0.15)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "#FBBF24",
            }}
          >
            <Bell size={20} />
          </div>
          <div>
            <h3
              style={{ fontSize: "1.2rem", fontWeight: 700, color: "#FFFFFF" }}
            >
              Notifications & Alerts
            </h3>
            <p style={{ fontSize: "0.82rem", color: "#94A3B8" }}>
              Manage push and email delivery preferences
            </p>
          </div>
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: "18px" }}>
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              paddingBottom: "14px",
              borderBottom: "1px solid rgba(255, 255, 255, 0.06)",
            }}
          >
            <div>
              <h4
                style={{
                  fontSize: "0.95rem",
                  fontWeight: 600,
                  color: "#FFFFFF",
                }}
              >
                Trip Schedule Reminders
              </h4>
              <p style={{ fontSize: "0.82rem", color: "#94A3B8" }}>
                Alerts before your scheduled itinerary departure
              </p>
            </div>
            <Toggle
              checked={tripReminders}
              onChange={() => setTripReminders(!tripReminders)}
            />
          </div>

          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              paddingBottom: "14px",
              borderBottom: "1px solid rgba(255, 255, 255, 0.06)",
            }}
          >
            <div>
              <h4
                style={{
                  fontSize: "0.95rem",
                  fontWeight: 600,
                  color: "#FFFFFF",
                }}
              >
                AI Recommendation Updates
              </h4>
              <p style={{ fontSize: "0.82rem", color: "#94A3B8" }}>
                Periodic suggestions based on your destination history
              </p>
            </div>
            <Toggle
              checked={notifications}
              onChange={() => setNotifications(!notifications)}
            />
          </div>

          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
          >
            <div>
              <h4
                style={{
                  fontSize: "0.95rem",
                  fontWeight: 600,
                  color: "#FFFFFF",
                }}
              >
                Weekly Digest & Weather Warnings
              </h4>
              <p style={{ fontSize: "0.82rem", color: "#94A3B8" }}>
                Receive monsoon and seasonal climate previews
              </p>
            </div>
            <Toggle
              checked={emailUpdates}
              onChange={() => setEmailUpdates(!emailUpdates)}
            />
          </div>
        </div>
      </GlassCard>

      {/* 4. PRIVACY & SECURITY */}
      <GlassCard style={{ padding: "28px" }}>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "12px",
            marginBottom: "20px",
          }}
        >
          <div
            style={{
              width: "36px",
              height: "36px",
              borderRadius: "10px",
              background: "rgba(168, 85, 247, 0.15)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "#C084FC",
            }}
          >
            <Shield size={20} />
          </div>
          <div>
            <h3
              style={{ fontSize: "1.2rem", fontWeight: 700, color: "#FFFFFF" }}
            >
              Privacy & Data Control
            </h3>
            <p style={{ fontSize: "0.82rem", color: "#94A3B8" }}>
              Manage itinerary visibility and profile privacy
            </p>
          </div>
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: "18px" }}>
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              paddingBottom: "14px",
              borderBottom: "1px solid rgba(255, 255, 255, 0.06)",
            }}
          >
            <div>
              <h4
                style={{
                  fontSize: "0.95rem",
                  fontWeight: 600,
                  color: "#FFFFFF",
                }}
              >
                Private Profile
              </h4>
              <p style={{ fontSize: "0.82rem", color: "#94A3B8" }}>
                Hide your profile from community search
              </p>
            </div>
            <Toggle
              checked={privateProfile}
              onChange={() => setPrivateProfile(!privateProfile)}
            />
          </div>

          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
          >
            <div>
              <h4
                style={{
                  fontSize: "0.95rem",
                  fontWeight: 600,
                  color: "#FFFFFF",
                }}
              >
                Allow Public Itinerary Links
              </h4>
              <p style={{ fontSize: "0.82rem", color: "#94A3B8" }}>
                Enable sharing your synthesized trips via direct URL
              </p>
            </div>
            <Toggle
              checked={shareItineraries}
              onChange={() => setShareItineraries(!shareItineraries)}
            />
          </div>
        </div>
      </GlassCard>

      {/* 5. SESSION & DANGER ZONE */}
      <GlassCard
        style={{ padding: "28px", borderColor: "rgba(239, 68, 68, 0.25)" }}
      >
        <h3
          style={{
            fontSize: "1.2rem",
            fontWeight: 700,
            color: "#FCA5A5",
            marginBottom: "16px",
          }}
        >
          Session & Danger Zone
        </h3>

        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            flexWrap: "wrap",
            gap: "16px",
          }}
        >
          <Button
            variant="secondary"
            size="md"
            leftIcon={<LogOut size={16} />}
            onClick={handleLogout}
          >
            Sign Out of TripGenius
          </Button>

          <Button
            variant="danger"
            size="md"
            leftIcon={<Trash2 size={16} />}
            onClick={handleDeleteAccount}
          >
            Delete Account Permanently
          </Button>
        </div>
      </GlassCard>
    </div>
  );
}
