"use client";

import { useRef } from "react";
import { useRouter } from "next/navigation";

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

  function handleLogout() {
    localStorage.removeItem("tripgenius_token");

    localStorage.removeItem("tripgenius_user");

    localStorage.removeItem("tripgenius_profile_image");

    router.push("/");
  }

  function handleDeleteAccount() {
    const confirmed = window.confirm(
      "Are you sure you want to permanently delete your account?",
    );

    if (!confirmed) {
      return;
    }

    localStorage.removeItem("tripgenius_token");

    localStorage.removeItem("tripgenius_user");

    localStorage.removeItem("tripgenius_profile_image");

    router.push("/");
  }

  function handleChangePassword() {
    alert(
      "Change Password feature will be connected to backend authentication later.",
    );
  }

  function handleSwitchAccount() {
    alert("Multi-account support will be added in a future update.");
  }

  if (!isOpen) {
    return null;
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
          background: "rgba(15,23,42,0.95)",
        }}
      >
        <div
          style={{
            padding: "22px",
            textAlign: "center",
            fontWeight: 700,
            fontSize: "1.1rem",
            borderBottom: "1px solid rgba(255,255,255,0.08)",
          }}
        >
          Settings
        </div>

        <button
          onClick={handlePhotoClick}
          style={menuButtonStyle}
        >
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
            <button onClick={handleChangePassword} style={menuButtonStyle}>
              🔑 Change Password
            </button>

            <button onClick={handleSwitchAccount} style={menuButtonStyle}>
              🔄 Switch Account
            </button>

            <button
              onClick={() => router.push("/notifications")}
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
              Logout
            </button>

            <button
              onClick={handleDeleteAccount}
              style={{
                ...menuButtonStyle,
                color: "#DC2626",
                fontWeight: 700,
              }}
            >
              Delete Account
            </button>
          </>
        )}

        {!isLoggedIn && (
          <>
            <button
              onClick={() => router.push("/login")}
              style={menuButtonStyle}
            >
              🔐 Login
            </button>

            <button
              onClick={() => router.push("/register")}
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
            fontWeight: 700,
          }}
        >
          Cancel
        </button>
      </div>
    </div>
  );
}

const menuButtonStyle = {
  width: "100%",
  padding: "18px",
  border: "none",
  outline: "none",
  cursor: "pointer",
  background: "transparent",
  color: "#F8FAFC",
  fontSize: "1rem",
  borderBottom: "1px solid rgba(255,255,255,0.06)",
  transition: "all 0.2s ease",
} as const;
