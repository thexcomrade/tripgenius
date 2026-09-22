"use client";
import { FormEvent, useEffect, useState, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";
function ResetPasswordForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [token, setToken] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  useEffect(() => {
    const tokenFromUrl = searchParams.get("token");
    if (tokenFromUrl) {
      setToken(tokenFromUrl);
    }
  }, [searchParams]);
  function validatePassword(value: string) {
    const hasUppercase = /[A-Z]/.test(value);
    const hasLowercase = /[a-z]/.test(value);
    const hasNumber = /\d/.test(value);
    const hasSpecial = /[^A-Za-z0-9]/.test(value);
    return (
      value.length >= 8 &&
      hasUppercase &&
      hasLowercase &&
      hasNumber &&
      hasSpecial
    );
  }
  async function handleResetPassword(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setSuccess("");
    if (!token.trim()) {
      setError("Reset token is missing.");
      return;
    }
    if (!password.trim()) {
      setError("Please enter a new password.");
      return;
    }
    if (!validatePassword(password)) {
      setError(
        "Password must contain at least 8 characters, one uppercase letter, one lowercase letter, one number and one special character.",
      );
      return;
    }
    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }
    try {
      setLoading(true);
      /*
            await authService.resetPassword({
                token,
                password
            });
            */
      await new Promise((resolve) => setTimeout(resolve, 1800));
      setSuccess("Password reset successful. Redirecting to login...");
      setTimeout(() => {
        router.push("/login");
      }, 2000);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Unable to reset password.",
      );
    } finally {
      setLoading(false);
    }
  }
  return (
    <main
      style={{
        minHeight: "100vh",
        maxWidth: "650px",
        margin: "0 auto",
        padding: "40px 20px",
        display: "flex",
        alignItems: "center",
      }}
    >
      <section
        className="glass-card"
        style={{
          width: "100%",
          padding: "40px",
        }}
      >
        <h1
          className="hero-title"
          style={{
            textAlign: "center",
            marginBottom: "15px",
          }}
        >
          🔒 Reset Password
        </h1>
        <p
          style={{
            textAlign: "center",
            color: "#CBD5E1",
            lineHeight: 1.8,
            marginBottom: "30px",
          }}
        >
          Create a strong new password for your TripGenius account.
        </p>
        {error && (
          <div
            style={{
              background: "rgba(239,68,68,0.15)",
              color: "#FCA5A5",
              padding: "14px",
              borderRadius: "12px",
              marginBottom: "20px",
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
              padding: "14px",
              borderRadius: "12px",
              marginBottom: "20px",
            }}
          >
            {success}
          </div>
        )}
        <form onSubmit={handleResetPassword}>
          <div
            style={{
              marginBottom: "20px",
            }}
          >
            <label>Reset Token</label>
            <input
              type="text"
              value={token}
              onChange={(e) => setToken(e.target.value)}
              placeholder="Paste reset token"
              className="newsletter-input"
              style={{
                width: "100%",
                marginTop: "8px",
                background: "#0F172A",
                color: "#FFFFFF",
                border: "1px solid rgba(255,255,255,0.15)",
              }}
            />
          </div>
          <div
            style={{
              marginBottom: "20px",
            }}
          >
            <label>New Password</label>
            <div
              style={{
                position: "relative",
                marginTop: "8px",
              }}
            >
              <input
                type={showPassword ? "text" : "password"}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter new password"
                className="newsletter-input"
                style={{
                  width: "100%",
                  background: "#0F172A",
                  color: "#FFFFFF",
                  border: "1px solid rgba(255,255,255,0.15)",
                  paddingRight: "60px",
                }}
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                style={{
                  position: "absolute",
                  right: "15px",
                  top: "50%",
                  transform: "translateY(-50%)",
                  border: "none",
                  background: "transparent",
                  cursor: "pointer",
                  padding: 0,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                <img
                  src={
                    showPassword
                      ? "/assets/icons/eye-closed.svg"
                      : "/assets/icons/eye-open.svg"
                  }
                  alt={showPassword ? "Hide Password" : "Show Password"}
                  width={22}
                  height={22}
                />
              </button>
            </div>
          </div>
          <div
            style={{
              marginBottom: "20px",
            }}
          >
            <label>Confirm Password</label>
            <div
              style={{
                position: "relative",
                marginTop: "8px",
              }}
            >
              <input
                type={showConfirmPassword ? "text" : "password"}
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="Confirm new password"
                className="newsletter-input"
                style={{
                  width: "100%",
                  background: "#0F172A",
                  color: "#FFFFFF",
                  border: "1px solid rgba(255,255,255,0.15)",
                  paddingRight: "60px",
                }}
              />
              <button
                type="button"
                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                style={{
                  position: "absolute",
                  right: "15px",
                  top: "50%",
                  transform: "translateY(-50%)",
                  border: "none",
                  background: "transparent",
                  cursor: "pointer",
                  padding: 0,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                <img
                  src={
                    showConfirmPassword
                      ? "/assets/icons/eye-closed.svg"
                      : "/assets/icons/eye-open.svg"
                  }
                  alt={showConfirmPassword ? "Hide Password" : "Show Password"}
                  width={22}
                  height={22}
                />
              </button>
            </div>
          </div>
          <div
            style={{
              marginBottom: "30px",
              padding: "18px",
              borderRadius: "12px",
              background: "rgba(255,255,255,0.05)",
              color: "#CBD5E1",
              lineHeight: 1.8,
              fontSize: "0.95rem",
            }}
          >
            <strong>Password Requirements</strong>
            <ul
              style={{
                marginTop: "10px",
                paddingLeft: "20px",
              }}
            >
              <li>Minimum 8 characters</li>
              <li>One uppercase letter</li>
              <li>One lowercase letter</li>
              <li>One number</li>
              <li>One special character</li>
            </ul>
          </div>
          <button
            type="submit"
            disabled={loading}
            className="btn-primary"
            style={{
              width: "100%",
              border: "none",
              cursor: "pointer",
              fontSize: "1rem",
            }}
          >
            {loading ? "Resetting Password..." : "Reset Password"}
          </button>
        </form>
        <div
          style={{
            marginTop: "30px",
            textAlign: "center",
            color: "#CBD5E1",
          }}
        >
          Remember your password?{" "}
          <Link
            href="/login"
            style={{
              color: "#38BDF8",
              textDecoration: "none",
              fontWeight: 700,
            }}
          >
            Back to Login
          </Link>
        </div>
        <div
          style={{
            marginTop: "15px",
            textAlign: "center",
          }}
        >
          <Link
            href="/forgot-password"
            style={{
              color: "#94A3B8",
              textDecoration: "none",
              fontSize: "0.9rem",
            }}
          >
            Request a new reset link
          </Link>
        </div>
        <div
          style={{
            marginTop: "30px",
            padding: "18px",
            borderRadius: "12px",
            background: "rgba(56,189,248,0.08)",
            border: "1px solid rgba(56,189,248,0.15)",
          }}
        >
          <h3
            style={{
              marginBottom: "10px",
              color: "#38BDF8",
            }}
          >
            🔐 Security Tips
          </h3>
          <ul
            style={{
              color: "#CBD5E1",
              lineHeight: 1.8,
              paddingLeft: "20px",
            }}
          >
            <li>Never share your password with anyone.</li>
            <li>Use a unique password for TripGenius.</li>
            <li>Enable two-factor authentication when available.</li>
            <li>Change your password regularly.</li>
            <li>
              Avoid using easily guessed information such as your birthday.
            </li>
          </ul>
        </div>
        <div
          style={{
            marginTop: "25px",
            textAlign: "center",
            fontSize: "0.85rem",
            color: "#64748B",
          }}
        >
          If you didn't request this password reset, you can safely ignore this
          page and your existing password will remain unchanged.
        </div>
      </section>
    </main>
  );
}
export default function ResetPasswordPage() {
  return (
    <Suspense
      fallback={
        <main
          style={{
            minHeight: "100vh",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <div style={{ color: "#FFFFFF", fontSize: "1.2rem" }}>Loading...</div>
        </main>
      }
    >
      <ResetPasswordForm />
    </Suspense>
  );
}
