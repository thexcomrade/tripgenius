"use client";

import { useState } from "react";
import Link from "next/link";
import Image from "next/image";
import { useRouter } from "next/navigation";
import {
  Mail,
  Lock,
  Eye,
  EyeOff,
  Sparkles,
  AlertCircle,
  ArrowRight,
} from "lucide-react";
import Button from "../../components/ui/Button";
import Badge from "../../components/ui/Badge";
import { GlassCard } from "../../components/ui/Card";
import authService from "../../services/auth.service";

export default function LoginPage() {
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleLogin(event: React.FormEvent) {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      await authService.login({ email, password });

      // Fetch and cache profile for dashboard/profile pages
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
        // Non-critical: token already stored by authService.login()
      }

      router.push("/dashboard");
    } catch (err) {
      const message =
        err instanceof Error
          ? err.message
          : "Login failed. Please check your credentials.";
      setError(message);
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
          maxWidth: "460px",
          padding: "44px 36px",
          borderRadius: "28px",
          boxShadow: "0 24px 60px rgba(0, 0, 0, 0.50)",
        }}
      >
        {/* BRAND LOGO HEADER */}
        <div style={{ textAlign: "center", marginBottom: "32px" }}>
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
            Welcome Back
          </h1>
          <p style={{ color: "#94A3B8", fontSize: "0.92rem", lineHeight: 1.5 }}>
            Sign in to continue planning smarter, eco-conscious journeys.
          </p>
        </div>

        {/* ERROR BANNER */}
        {error && (
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
            <span>{error}</span>
          </div>
        )}

        {/* LOGIN FORM */}
        <form
          onSubmit={handleLogin}
          style={{ display: "flex", flexDirection: "column", gap: "18px" }}
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
              Email Address
            </label>
            <div style={{ position: "relative" }}>
              <Mail
                size={18}
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
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="name@example.com"
                className="input-base"
                style={{ paddingLeft: "42px" }}
              />
            </div>
          </div>

          <div>
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                marginBottom: "6px",
              }}
            >
              <label
                style={{
                  fontSize: "0.82rem",
                  fontWeight: 600,
                  color: "#CBD5E1",
                }}
              >
                Password
              </label>
              <Link
                href="/forgot-password"
                style={{
                  color: "#38BDF8",
                  fontSize: "0.8rem",
                  fontWeight: 500,
                  textDecoration: "none",
                }}
              >
                Forgot password?
              </Link>
            </div>
            <div style={{ position: "relative" }}>
              <Lock
                size={18}
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
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter your password"
                className="input-base"
                style={{ paddingLeft: "42px", paddingRight: "42px" }}
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                style={{
                  position: "absolute",
                  right: "14px",
                  top: "50%",
                  transform: "translateY(-50%)",
                  background: "transparent",
                  border: "none",
                  color: "#94A3B8",
                  cursor: "pointer",
                  display: "flex",
                  alignItems: "center",
                }}
              >
                {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
              </button>
            </div>
          </div>

          <Button
            type="submit"
            variant="primary"
            size="lg"
            isLoading={loading}
            rightIcon={<ArrowRight size={16} />}
            style={{ width: "100%", marginTop: "10px" }}
          >
            Sign In
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
          Don&apos;t have an account?{" "}
          <Link
            href="/register"
            style={{
              color: "#38BDF8",
              fontWeight: 700,
              textDecoration: "none",
            }}
          >
            Create one for free
          </Link>
        </div>
      </GlassCard>
    </div>
  );
}
