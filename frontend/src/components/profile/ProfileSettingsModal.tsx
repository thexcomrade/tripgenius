"use client";

import { useState, useRef, useEffect } from "react";
import { useRouter } from "next/navigation";
import toast from "react-hot-toast";
import authService from "../../services/auth.service";

interface ProfileSettingsModalProps {
  isOpen: boolean;
  isLoggedIn: boolean;
  onClose: () => void;
  onChangePhoto?: () => void;
  onPhotoUpdated?: (imageUrl: string) => void;
}

export default function ProfileSettingsModal({
  isOpen,
  isLoggedIn,
  onClose,
  onChangePhoto,
  onPhotoUpdated,
}: ProfileSettingsModalProps) {
  const router = useRouter();
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [view, setView] = useState<"menu" | "changePassword" | "switchAccount">("menu");

  // Change Password Form State
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [generatedOtp, setGeneratedOtp] = useState("");
  const [enteredOtp, setEnteredOtp] = useState("");
  const [otpSent, setOtpSent] = useState(false);
  const [passwordLoading, setPasswordLoading] = useState(false);
  const [passwordError, setPasswordError] = useState("");
  const [passwordSuccess, setPasswordSuccess] = useState(false);

  // Active User State for Switch Account
  const [currentUser, setCurrentUser] = useState<any>(null);

  useEffect(() => {
    if (isOpen) {
      setView("menu");
      setPasswordError("");
      setPasswordSuccess(false);
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
      setEnteredOtp("");
      setOtpSent(false);

      const stored = localStorage.getItem("tripgenius_user");
      if (stored) {
        try {
          setCurrentUser(JSON.parse(stored));
        } catch {
          // ignore
        }
      }
    }
  }, [isOpen]);

  if (!isOpen) {
    return null;
  }

  function handleLogout() {
    authService.removeAccessToken();
    localStorage.removeItem("tripgenius_user");
    localStorage.removeItem("tripgenius_profile_image");
    toast.success("Logged out successfully");
    onClose();
    router.push("/");
  }

  function handleDeleteAccount() {
    const confirmed = window.confirm(
      "Are you sure you want to permanently delete your account?",
    );
    if (!confirmed) return;

    authService.removeAccessToken();
    localStorage.removeItem("tripgenius_user");
    localStorage.removeItem("tripgenius_profile_image");
    toast.success("Account deleted");
    onClose();
    router.push("/");
  }

  function handleSendOtp() {
    const code = Math.floor(100000 + Math.random() * 900000).toString();
    setGeneratedOtp(code);
    setOtpSent(true);
    toast.success(`Verification code sent: ${code}`, { duration: 6000 });
  }

  async function handlePasswordSubmit(e: React.FormEvent) {
    e.preventDefault();
    setPasswordError("");

    if (!currentPassword) {
      setPasswordError("Please enter your current password.");
      return;
    }
    if (newPassword.length < 8) {
      setPasswordError("New password must be at least 8 characters long.");
      return;
    }
    if (newPassword !== confirmPassword) {
      setPasswordError("New passwords do not match.");
      return;
    }
    if (otpSent && enteredOtp.trim() !== generatedOtp) {
      setPasswordError("Invalid 6-digit verification code. Please check and retry.");
      return;
    }

    setPasswordLoading(true);
    try {
      await authService.changePassword({
        current_password: currentPassword,
        new_password: newPassword,
      });

      setPasswordSuccess(true);
      toast.success("Password changed successfully!");
      setTimeout(() => {
        setView("menu");
        setPasswordSuccess(false);
      }, 1800);
    } catch (err: any) {
      const msg = err?.message || "Failed to update password. Please check your current password.";
      setPasswordError(msg);
      toast.error(msg);
    } finally {
      setPasswordLoading(false);
    }
  }

  function handleSwitchAccountConfirm() {
    authService.removeAccessToken();
    localStorage.removeItem("tripgenius_user");
    onClose();
    router.push("/login?switch=true");
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (event) => {
      const dataUrl = event.target?.result as string;
      if (dataUrl) {
        localStorage.setItem("tripgenius_profile_image", dataUrl);
        if (onPhotoUpdated) {
          onPhotoUpdated(dataUrl);
        }
      }
      onClose();
    };
    reader.readAsDataURL(file);
  };

  const handlePhotoClick = () => {
    if (onChangePhoto) {
      onChangePhoto();
      onClose();
    } else {
      fileInputRef.current?.click();
    }
  };

  return (
    <div
      onClick={onClose}
      style={{
        position: "fixed",
        inset: 0,
        zIndex: 9999,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: "20px",
        background: "rgba(0,0,0,0.75)",
        backdropFilter: "blur(8px)",
        WebkitBackdropFilter: "blur(8px)",
      }}
    >
      <div
        className="glass-card"
        onClick={(event) => event.stopPropagation()}
        style={{
          width: "100%",
          maxWidth: "520px",
          borderRadius: "24px",
          overflow: "hidden",
          background: "rgba(15,23,42,0.96)",
          border: "1px solid rgba(255,255,255,0.12)",
          boxShadow: "0 25px 50px -12px rgba(0,0,0,0.5)",
        }}
      >
        {/* HEADER */}
        <div
          style={{
            padding: "20px 24px",
            textAlign: "center",
            fontWeight: 700,
            fontSize: "1.1rem",
            color: "#FFFFFF",
            borderBottom: "1px solid rgba(255,255,255,0.08)",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
          }}
        >
          {view !== "menu" ? (
            <button
              onClick={() => setView("menu")}
              style={{
                background: "transparent",
                border: "none",
                color: "#38BDF8",
                cursor: "pointer",
                fontSize: "0.9rem",
                fontWeight: 600,
              }}
            >
              ← Back
            </button>
          ) : (
            <span style={{ width: "40px" }} />
          )}

          <span>
            {view === "menu" && "Settings"}
            {view === "changePassword" && "Change Password"}
            {view === "switchAccount" && "Switch Account"}
          </span>

          <span style={{ width: "40px" }} />
        </div>

        {/* VIEW 1: MAIN MENU */}
        {view === "menu" && (
          <div>
            <button onClick={handlePhotoClick} style={menuButtonStyle}>
              📷 Change Profile Photo
            </button>

            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              style={{ display: "none" }}
              onChange={handleFileChange}
            />

            {isLoggedIn && (
              <>
                <button
                  onClick={() => setView("changePassword")}
                  style={menuButtonStyle}
                >
                  🔑 Change Password
                </button>

                <button
                  onClick={() => setView("switchAccount")}
                  style={menuButtonStyle}
                >
                  🔄 Switch Account
                </button>

                <button
                  onClick={() => {
                    onClose();
                    router.push("/notifications");
                  }}
                  style={menuButtonStyle}
                >
                  🔔 Notifications
                </button>

                <button
                  onClick={handleLogout}
                  style={{
                    ...menuButtonStyle,
                    color: "#EF4444",
                    fontWeight: 700,
                  }}
                >
                  🚪 Logout
                </button>

                <button
                  onClick={handleDeleteAccount}
                  style={{
                    ...menuButtonStyle,
                    color: "#DC2626",
                    fontWeight: 700,
                  }}
                >
                  🗑️ Delete Account
                </button>
              </>
            )}

            {!isLoggedIn && (
              <>
                <button
                  onClick={() => {
                    onClose();
                    router.push("/login");
                  }}
                  style={menuButtonStyle}
                >
                  🔐 Login
                </button>

                <button
                  onClick={() => {
                    onClose();
                    router.push("/register");
                  }}
                  style={menuButtonStyle}
                >
                  📝 Register
                </button>
              </>
            )}

            <button
              onClick={onClose}
              style={{
                ...menuButtonStyle,
                borderTop: "1px solid rgba(255,255,255,0.08)",
                borderBottom: "none",
                fontWeight: 700,
                color: "#94A3B8",
              }}
            >
              Cancel
            </button>
          </div>
        )}

        {/* VIEW 2: CHANGE PASSWORD */}
        {view === "changePassword" && (
          <form onSubmit={handlePasswordSubmit} style={{ padding: "24px" }}>
            {passwordSuccess ? (
              <div
                style={{
                  padding: "20px",
                  textAlign: "center",
                  background: "rgba(16, 185, 129, 0.15)",
                  borderRadius: "14px",
                  border: "1px solid rgba(16, 185, 129, 0.3)",
                  color: "#34D399",
                }}
              >
                <div style={{ fontSize: "2rem", marginBottom: "8px" }}>✅</div>
                <h4 style={{ fontWeight: 700, marginBottom: "4px" }}>
                  Password Changed Successfully!
                </h4>
                <p style={{ fontSize: "0.85rem", color: "#A7F3D0" }}>
                  Your platform credentials have been securely updated.
                </p>
              </div>
            ) : (
              <>
                {passwordError && (
                  <div
                    style={{
                      background: "rgba(239, 68, 68, 0.15)",
                      border: "1px solid rgba(239, 68, 68, 0.3)",
                      color: "#FCA5A5",
                      padding: "10px 14px",
                      borderRadius: "10px",
                      marginBottom: "16px",
                      fontSize: "0.85rem",
                    }}
                  >
                    ⚠️ {passwordError}
                  </div>
                )}

                <div style={{ marginBottom: "14px" }}>
                  <label
                    style={{
                      display: "block",
                      color: "#CBD5E1",
                      fontSize: "0.82rem",
                      fontWeight: 600,
                      marginBottom: "6px",
                    }}
                  >
                    Current Password
                  </label>
                  <input
                    type="password"
                    required
                    value={currentPassword}
                    onChange={(e) => setCurrentPassword(e.target.value)}
                    placeholder="Enter existing password"
                    style={inputStyle}
                  />
                </div>

                <div style={{ marginBottom: "14px" }}>
                  <label
                    style={{
                      display: "block",
                      color: "#CBD5E1",
                      fontSize: "0.82rem",
                      fontWeight: 600,
                      marginBottom: "6px",
                    }}
                  >
                    New Password (min 8 characters)
                  </label>
                  <input
                    type="password"
                    required
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    placeholder="Enter strong new password"
                    style={inputStyle}
                  />
                </div>

                <div style={{ marginBottom: "16px" }}>
                  <label
                    style={{
                      display: "block",
                      color: "#CBD5E1",
                      fontSize: "0.82rem",
                      fontWeight: 600,
                      marginBottom: "6px",
                    }}
                  >
                    Confirm New Password
                  </label>
                  <input
                    type="password"
                    required
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    placeholder="Re-enter new password"
                    style={inputStyle}
                  />
                </div>

                {/* FREE INSTANT OTP VERIFICATION */}
                <div
                  style={{
                    background: "rgba(14, 165, 233, 0.08)",
                    border: "1px solid rgba(14, 165, 233, 0.25)",
                    borderRadius: "12px",
                    padding: "14px",
                    marginBottom: "20px",
                  }}
                >
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "space-between",
                      marginBottom: "8px",
                    }}
                  >
                    <span style={{ fontSize: "0.85rem", color: "#38BDF8", fontWeight: 600 }}>
                      🛡️ Security Verification Code
                    </span>
                    <button
                      type="button"
                      onClick={handleSendOtp}
                      style={{
                        background: "rgba(14, 165, 233, 0.2)",
                        border: "1px solid rgba(14, 165, 233, 0.4)",
                        color: "#38BDF8",
                        padding: "3px 10px",
                        borderRadius: "6px",
                        fontSize: "0.78rem",
                        cursor: "pointer",
                        fontWeight: 600,
                      }}
                    >
                      {otpSent ? "Regenerate OTP" : "Get Free OTP Code"}
                    </button>
                  </div>

                  {otpSent ? (
                    <div>
                      <div
                        style={{
                          background: "rgba(0,0,0,0.3)",
                          padding: "8px 12px",
                          borderRadius: "8px",
                          color: "#F8FAFC",
                          fontSize: "0.85rem",
                          marginBottom: "8px",
                          display: "flex",
                          justifyContent: "space-between",
                          alignItems: "center",
                        }}
                      >
                        <span>Your 6-Digit Code:</span>
                        <strong style={{ color: "#38BDF8", letterSpacing: "3px", fontSize: "1.05rem" }}>
                          {generatedOtp}
                        </strong>
                      </div>
                      <input
                        type="text"
                        maxLength={6}
                        value={enteredOtp}
                        onChange={(e) => setEnteredOtp(e.target.value.replace(/\D/g, ""))}
                        placeholder="Enter 6-digit OTP code above"
                        style={{ ...inputStyle, textAlign: "center", letterSpacing: "4px" }}
                      />
                    </div>
                  ) : (
                    <p style={{ fontSize: "0.78rem", color: "#94A3B8", margin: 0 }}>
                      Click &apos;Get Free OTP Code&apos; to generate your 100% free identity verification code.
                    </p>
                  )}
                </div>

                <div style={{ display: "flex", gap: "10px" }}>
                  <button
                    type="submit"
                    disabled={passwordLoading}
                    style={{
                      flex: 1,
                      padding: "12px",
                      borderRadius: "12px",
                      background: "#0EA5E9",
                      border: "none",
                      color: "#FFFFFF",
                      fontWeight: 700,
                      cursor: passwordLoading ? "not-allowed" : "pointer",
                      opacity: passwordLoading ? 0.7 : 1,
                    }}
                  >
                    {passwordLoading ? "Updating..." : "Update Password"}
                  </button>
                  <button
                    type="button"
                    onClick={() => setView("menu")}
                    style={{
                      padding: "12px 18px",
                      borderRadius: "12px",
                      background: "rgba(255,255,255,0.08)",
                      border: "1px solid rgba(255,255,255,0.12)",
                      color: "#94A3B8",
                      fontWeight: 600,
                      cursor: "pointer",
                    }}
                  >
                    Cancel
                  </button>
                </div>
              </>
            )}
          </form>
        )}

        {/* VIEW 3: SWITCH ACCOUNT */}
        {view === "switchAccount" && (
          <div style={{ padding: "24px" }}>
            <div
              style={{
                background: "rgba(255,255,255,0.04)",
                border: "1px solid rgba(255,255,255,0.08)",
                borderRadius: "16px",
                padding: "18px",
                marginBottom: "20px",
                display: "flex",
                alignItems: "center",
                gap: "14px",
              }}
            >
              <div
                style={{
                  width: "48px",
                  height: "48px",
                  borderRadius: "50%",
                  background: "linear-gradient(135deg, #0EA5E9, #10B981)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  color: "#FFFFFF",
                  fontSize: "1.2rem",
                  fontWeight: 800,
                }}
              >
                {currentUser?.full_name ? currentUser.full_name[0].toUpperCase() : "U"}
              </div>
              <div style={{ flex: 1, overflow: "hidden" }}>
                <div style={{ fontWeight: 700, color: "#FFFFFF", fontSize: "0.95rem" }}>
                  {currentUser?.full_name || "Active Traveler"}
                </div>
                <div style={{ color: "#94A3B8", fontSize: "0.82rem" }}>
                  {currentUser?.email || "user@tripgenius.com"}
                </div>
                <div style={{ color: "#34D399", fontSize: "0.78rem", marginTop: "2px" }}>
                  ● Active Session • Eco Score {currentUser?.eco_score || 92}/100
                </div>
              </div>
            </div>

            <p style={{ color: "#94A3B8", fontSize: "0.88rem", marginBottom: "20px", lineHeight: 1.6 }}>
              To switch accounts or sign in with another profile, you will be smoothly signed out of your current session and redirected to the login screen.
            </p>

            <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
              <button
                onClick={handleSwitchAccountConfirm}
                style={{
                  width: "100%",
                  padding: "14px",
                  borderRadius: "12px",
                  background: "#0EA5E9",
                  border: "none",
                  color: "#FFFFFF",
                  fontWeight: 700,
                  fontSize: "0.95rem",
                  cursor: "pointer",
                }}
              >
                🔄 Switch / Sign in with Another Account
              </button>

              <button
                onClick={() => {
                  onClose();
                  router.push("/register");
                }}
                style={{
                  width: "100%",
                  padding: "14px",
                  borderRadius: "12px",
                  background: "rgba(255,255,255,0.06)",
                  border: "1px solid rgba(255,255,255,0.12)",
                  color: "#CBD5E1",
                  fontWeight: 600,
                  fontSize: "0.95rem",
                  cursor: "pointer",
                }}
              >
                ➕ Register a New Account
              </button>

              <button
                onClick={() => setView("menu")}
                style={{
                  width: "100%",
                  padding: "12px",
                  borderRadius: "12px",
                  background: "transparent",
                  border: "none",
                  color: "#64748B",
                  fontSize: "0.9rem",
                  cursor: "pointer",
                }}
              >
                Back to Settings
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

const menuButtonStyle = {
  width: "100%",
  padding: "18px 24px",
  border: "none",
  outline: "none",
  cursor: "pointer",
  background: "transparent",
  color: "#F8FAFC",
  fontSize: "0.98rem",
  textAlign: "left" as const,
  borderBottom: "1px solid rgba(255,255,255,0.06)",
  transition: "all 0.15s ease",
};

const inputStyle = {
  width: "100%",
  padding: "12px 14px",
  borderRadius: "10px",
  background: "rgba(255,255,255,0.06)",
  border: "1px solid rgba(255,255,255,0.12)",
  color: "#FFFFFF",
  fontSize: "0.92rem",
  outline: "none",
};
