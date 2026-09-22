"use client";

import { FormEvent, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import axios from "axios";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

export default function ForgotPasswordPage() {
  const router = useRouter();

  const [email, setEmail] = useState("");

  const [loading, setLoading] = useState(false);

  const [success, setSuccess] = useState("");

  const [error, setError] = useState("");

  const [emailSent, setEmailSent] = useState(false);

  async function handleForgotPassword(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setLoading(true);
    setError("");
    setSuccess("");

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailRegex.test(email)) {
      setLoading(false);
      setError("Please enter a valid email address.");
      return;
    }

    try {
      const response = await axios.post(
        `${API_BASE_URL}/api/auth/forgot-password`,
        {
          email,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        },
      );

      setSuccess(
        response.data?.message ?? "Password reset link sent successfully.",
      );

      setEmailSent(true);
    } catch (err: any) {
      setError(
        err?.response?.data?.detail ??
          err?.response?.data?.message ??
          err?.message ??
          "Unable to send password reset email.",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main
      style={{
        minHeight: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        padding: "30px",
        background: "linear-gradient(135deg,#020617,#0F172A,#111827)",
      }}
    >
      <section
        className="glass-card"
        style={{
          width: "100%",
          maxWidth: "600px",
          padding: "45px",
          borderRadius: "28px",
        }}
      >
        <div
          style={{
            textAlign: "center",
            marginBottom: "35px",
          }}
        >
          <h1
            style={{
              fontSize: "2.6rem",
              fontWeight: 800,
              marginBottom: "10px",
            }}
          >
            🔑 Forgot Password
          </h1>

          <p
            style={{
              color: "#CBD5E1",
              lineHeight: 1.7,
            }}
          >
            Enter your registered email address and TripGenius will send you a
            secure password reset link.
          </p>
        </div>

        {error && (
          <div
            style={{
              background: "rgba(239,68,68,0.15)",
              color: "#FCA5A5",
              padding: "15px",
              borderRadius: "14px",
              marginBottom: "20px",
              border: "1px solid rgba(239,68,68,0.25)",
            }}
          >
            {error}
          </div>
        )}

        {success && (
          <div
            style={{
              background: "rgba(34,197,94,0.15)",
              color: "#86EFAC",
              padding: "15px",
              borderRadius: "14px",
              marginBottom: "20px",
              border: "1px solid rgba(34,197,94,0.25)",
            }}
          >
            {success}
          </div>
        )}

        <form onSubmit={handleForgotPassword}>
          <div
            style={{
              marginBottom: "25px",
            }}
          >
            <label
              style={{
                display: "block",
                marginBottom: "10px",
                fontWeight: 600,
              }}
            >
              📧 Email Address
            </label>

            <input
              type="email"
              required
              autoComplete="email"
              value={email}
              disabled={emailSent}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your registered email"
              className="newsletter-input"
              style={{
                width: "100%",
                background: "#0F172A",
                color: "#FFFFFF",
                border: "1px solid rgba(255,255,255,0.15)",
              }}
            />
          </div>
          <button
            type="submit"
            disabled={loading || emailSent}
            className="btn-primary"
            style={{
              width: "100%",
              border: "none",
              cursor: loading || emailSent ? "not-allowed" : "pointer",
              opacity: loading || emailSent ? 0.7 : 1,
              padding: "15px",
            }}
          >
            {loading
              ? "Sending Reset Link..."
              : emailSent
                ? "✅ Reset Link Sent"
                : "Send Reset Link"}
          </button>
        </form>

        {emailSent && (
          <button
            onClick={() => {
              setEmailSent(false);
              setSuccess("");
              setError("");
            }}
            style={{
              marginTop: "18px",
              width: "100%",
              padding: "14px",
              border: "none",
              borderRadius: "12px",
              background: "#1E293B",
              color: "#FFFFFF",
              cursor: "pointer",
              fontWeight: 600,
            }}
          >
            🔄 Send Another Reset Link
          </button>
        )}

        <div
          style={{
            marginTop: "35px",
            padding: "20px",
            borderRadius: "18px",
            background: "rgba(255,255,255,0.05)",
          }}
        >
          <h3
            style={{
              marginBottom: "12px",
            }}
          >
            🔒 Security Tips
          </h3>

          <ul
            style={{
              color: "#CBD5E1",
              lineHeight: 1.9,
              paddingLeft: "20px",
            }}
          >
            <li>Never share your password with anyone.</li>

            <li>Reset links expire after a limited time.</li>

            <li>Check your Spam or Junk folder if the email doesn't arrive.</li>

            <li>
              Use a strong password with uppercase, lowercase, numbers and
              symbols.
            </li>

            <li>
              Contact TripGenius support if you didn't request a password reset.
            </li>
          </ul>
        </div>

        <div
          style={{
            marginTop: "35px",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            flexWrap: "wrap",
            gap: "15px",
          }}
        >
          <Link
            href="/login"
            style={{
              color: "#38BDF8",
              textDecoration: "none",
              fontWeight: 600,
            }}
          >
            ← Back to Login
          </Link>

          <Link
            href="/register"
            style={{
              color: "#38BDF8",
              textDecoration: "none",
              fontWeight: 600,
            }}
          >
            Create New Account →
          </Link>
        </div>

        <div
          style={{
            marginTop: "40px",
            textAlign: "center",
            color: "#94A3B8",
            fontSize: "0.9rem",
            lineHeight: 1.7,
          }}
        >
          By continuing, you agree to TripGenius' security practices for
          password recovery and account protection.
        </div>

        <div
          style={{
            marginTop: "25px",
            display: "flex",
            justifyContent: "center",
          }}
        >
          <button
            onClick={() => router.push("/")}
            style={{
              border: "none",
              background: "transparent",
              color: "#64748B",
              cursor: "pointer",
              fontSize: "0.9rem",
            }}
          >
            🏠 Return to Home
          </button>
        </div>
      </section>
    </main>
  );
}
