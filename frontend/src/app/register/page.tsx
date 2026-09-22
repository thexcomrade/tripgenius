"use client";

import { useState } from "react";
import Link from "next/link";
import Image from "next/image";
import { useRouter } from "next/navigation";
import {
  User,
  Mail,
  Lock,
  Eye,
  EyeOff,
  Sparkles,
  AlertCircle,
  ArrowRight,
} from "lucide-react";
import Button from "../../components/ui/Button";
import { GlassCard } from "../../components/ui/Card";
import authService from "../../services/auth.service";

interface RegisterForm {
  full_name: string;
  username: string;
  email: string;
  password: string;
  confirm_password: string;
}

export default function RegisterPage() {
  const router = useRouter();

  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const [form, setForm] = useState<RegisterForm>({
    full_name: "",
    username: "",
    email: "",
    password: "",
    confirm_password: "",
  });

  function updateField(field: keyof RegisterForm, value: string) {
    setForm((prev) => ({
      ...prev,
      [field]: value,
    }));
  }

  async function handleRegister(event: React.FormEvent) {
    event.preventDefault();
    setErrorMsg("");

    if (form.password !== form.confirm_password) {
      setErrorMsg("Passwords do not match.");
      return;
    }

    if (form.password.length < 8) {
      setErrorMsg("Password must be at least 8 characters long.");
      return;
    }

    setLoading(true);

    try {
      // Register user in backend
      await authService.register({
        full_name: form.full_name,
        email: form.email,
        password: form.password,
      });

      // Automatically log in newly registered user
      await authService.login({
        email: form.email,
        password: form.password,
      });

      // Fetch and cache profile
      try {
        const profile = await authService.getProfile();
        localStorage.setItem(
          "tripgenius_user",
          JSON.stringify({
            uid: profile.id,
            full_name: profile.full_name,
            email: profile.email,
            is_verified: profile.is_verified,
            eco_score: profile.eco_travel_score,
            total_trips: profile.total_trips,
            saved_trips: 0,
          }),
        );
      } catch {
        // Non-critical fallback
      }

      router.push("/dashboard");
    } catch (err) {
      const message =
        err instanceof Error
          ? err.message
          : "Registration failed. Please try again with another email.";
      setErrorMsg(message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div
      style={{
        minHeight: "calc(100vh - 200px)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: "40px 20px",
      }}
    >
      <GlassCard
        style={{
          width: "100%",
          maxWidth: "520px",
          padding: "44px 36px",
          borderRadius: "28px",
          boxShadow: "0 24px 60px rgba(0, 0, 0, 0.50)",
        }}
      >
        {/* BRAND LOGO HEADER */}
        <div style={{ textAlign: "center", marginBottom: "28px" }}>
          <div
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: "10px",
              marginBottom: "16px",
            }}
          >
            <Image
              src="/logo/logo.svg"
              alt="TripGenius Logo"
              width={42}
              height={42}
              priority
            />
            <span
              style={{
                fontSize: "1.7rem",
                fontWeight: 800,
                color: "#FFFFFF",
                letterSpacing: "-0.5px",
              }}
            >
              TripGenius
            </span>
          </div>

          <h1
            style={{
              fontSize: "1.8rem",
              fontWeight: 800,
              color: "#FFFFFF",
              marginBottom: "6px",
            }}
          >
            Create Your Traveler Account
          </h1>
          <p style={{ color: "#94A3B8", fontSize: "0.92rem", lineHeight: 1.5 }}>
            Join TripGenius to unlock AI-synthesized itineraries, weather
            intelligence, and eco-travel tracking.
          </p>
        </div>

        {/* ERROR BANNER */}
        {errorMsg && (
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "10px",
              background: "rgba(239, 68, 68, 0.15)",
              border: "1px solid rgba(239, 68, 68, 0.35)",
              color: "#FCA5A5",
              padding: "12px 16px",
              borderRadius: "12px",
              marginBottom: "20px",
              fontSize: "0.88rem",
            }}
          >
            <AlertCircle size={18} style={{ flexShrink: 0 }} />
            <span>{errorMsg}</span>
          </div>
        )}

        {/* FORM */}
        <form
          onSubmit={handleRegister}
          style={{ display: "flex", flexDirection: "column", gap: "16px" }}
        >
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr",
              gap: "14px",
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
              <div style={{ position: "relative" }}>
                <User
                  size={16}
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
                  required
                  value={form.full_name}
                  onChange={(e) => updateField("full_name", e.target.value)}
                  placeholder="Your Name"
                  className="input-base"
                  style={{ paddingLeft: "38px" }}
                />
              </div>
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
                Username
              </label>
              <input
                type="text"
                value={form.username}
                onChange={(e) => updateField("username", e.target.value)}
                placeholder="traveler_01"
                className="input-base"
              />
            </div>
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
            <div style={{ position: "relative" }}>
              <Mail
                size={16}
                color="#94A3B8"
                style={{
                  position: "absolute",
                  left: "14px",
                  top: "50%",
                  transform: "translateY(-50%)",
                }}
              />
              <input
                type="email"
                required
                value={form.email}
                onChange={(e) => updateField("email", e.target.value)}
                placeholder="name@example.com"
                className="input-base"
                style={{ paddingLeft: "38px" }}
              />
            </div>
          </div>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr",
              gap: "14px",
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
                Password
              </label>
              <div style={{ position: "relative" }}>
                <Lock
                  size={16}
                  color="#94A3B8"
                  style={{
                    position: "absolute",
                    left: "14px",
                    top: "50%",
                    transform: "translateY(-50%)",
                  }}
                />
                <input
                  type={showPassword ? "text" : "password"}
                  required
                  value={form.password}
                  onChange={(e) => updateField("password", e.target.value)}
                  placeholder="Min 8 chars"
                  className="input-base"
                  style={{ paddingLeft: "38px", paddingRight: "36px" }}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  style={{
                    position: "absolute",
                    right: "10px",
                    top: "50%",
                    transform: "translateY(-50%)",
                    background: "transparent",
                    border: "none",
                    color: "#94A3B8",
                    cursor: "pointer",
                  }}
                >
                  {showPassword ? <EyeOff size={14} /> : <Eye size={14} />}
                </button>
              </div>
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
                Confirm Password
              </label>
              <input
                type={showPassword ? "text" : "password"}
                required
                value={form.confirm_password}
                onChange={(e) =>
                  updateField("confirm_password", e.target.value)
                }
                placeholder="Re-enter password"
                className="input-base"
              />
            </div>
          </div>

          <Button
            type="submit"
            variant="primary"
            size="lg"
            isLoading={loading}
            rightIcon={<ArrowRight size={16} />}
            style={{ width: "100%", marginTop: "12px" }}
          >
            Create Account
          </Button>
        </form>

        {/* FOOTER SWITCH */}
        <div
          style={{
            textAlign: "center",
            marginTop: "24px",
            paddingTop: "20px",
            borderTop: "1px solid rgba(255, 255, 255, 0.08)",
            fontSize: "0.9rem",
            color: "#94A3B8",
          }}
        >
          Already have an account?{" "}
          <Link
            href="/login"
            style={{
              color: "#38BDF8",
              fontWeight: 700,
              textDecoration: "none",
            }}
          >
            Sign in here
          </Link>
        </div>
      </GlassCard>
    </div>
  );
}
