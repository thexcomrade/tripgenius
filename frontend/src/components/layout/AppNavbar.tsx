"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import Image from "next/image";
import { usePathname, useRouter } from "next/navigation";
import {
  Compass,
  Sparkles,
  LayoutDashboard,
  History,
  Heart,
  Bot,
  BarChart3,
  Award,
  Bell,
  User,
  Menu,
  X,
  ChevronDown,
  LogOut,
} from "lucide-react";

export default function AppNavbar() {
  const pathname = usePathname();
  const router = useRouter();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [moreOpen, setMoreOpen] = useState(false);
  const moreRef = useRef<HTMLDivElement>(null);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userName, setUserName] = useState("Traveler");
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const checkAuth = () => {
      const token = localStorage.getItem("tripgenius_token");
      setIsLoggedIn(!!token);
      const storedUser = localStorage.getItem("tripgenius_user");
      if (storedUser) {
        try {
          const u = JSON.parse(storedUser);
          if (u.full_name) setUserName(u.full_name);
        } catch {
          // ignore
        }
      }
    };

    checkAuth();
    window.addEventListener("storage", checkAuth);

    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener("scroll", handleScroll);

    const handleClickOutside = (event: MouseEvent) => {
      if (moreRef.current && !moreRef.current.contains(event.target as Node)) {
        setMoreOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      window.removeEventListener("storage", checkAuth);
      window.removeEventListener("scroll", handleScroll);
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  // Close menus on route change
  useEffect(() => {
    setMobileMenuOpen(false);
    setMoreOpen(false);
  }, [pathname]);

  const handleLogout = () => {
    localStorage.removeItem("tripgenius_token");
    localStorage.removeItem("tripgenius_user");
    setIsLoggedIn(false);
    router.push("/login");
  };

  const mainNav = [
    { name: "Home", href: "/" },
    { name: "Planner", href: "/planner", highlight: true },
    { name: "Explore", href: "/explore" },
    { name: "Dashboard", href: "/dashboard" },
    { name: "History", href: "/trip/history" },
    { name: "Favorites", href: "/favorites" },
  ];

  const moreNav = [
    { name: "AI Travel Chat", href: "/ai-chat", icon: Bot },
    { name: "Analytics", href: "/analytics", icon: BarChart3 },
    { name: "Achievements", href: "/achievements", icon: Award },
  ];

  const isActive = (path: string) => {
    if (path === "/") return pathname === "/";
    return pathname.startsWith(path);
  };

  return (
    <header
      style={{
        position: "sticky",
        top: 0,
        zIndex: 100,
        backdropFilter: "blur(20px)",
        WebkitBackdropFilter: "blur(20px)",
        background: scrolled ? "rgba(3, 7, 18, 0.88)" : "rgba(3, 7, 18, 0.72)",
        borderBottom: "1px solid rgba(255, 255, 255, 0.08)",
        transition: "background 0.3s ease, border-color 0.3s ease",
      }}
    >
      <div
        style={{
          maxWidth: "1520px",
          margin: "0 auto",
          padding: "14px 24px",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          gap: "20px",
        }}
      >
        {/* BRAND LOGO */}
        <Link
          href="/"
          style={{
            display: "flex",
            alignItems: "center",
            gap: "12px",
            textDecoration: "none",
            flexShrink: 0,
          }}
        >
          <Image
            src="/logo/logo.svg"
            alt="TripGenius Logo"
            width={38}
            height={38}
            priority
          />
          <span
            style={{
              color: "#FFFFFF",
              fontSize: "1.8rem",
              fontWeight: 800,
              letterSpacing: "-0.5px",
            }}
          >
            TripGenius
          </span>
        </Link>

        {/* DESKTOP NAVIGATION */}
        <nav
          style={{
            display: "none",
            alignItems: "center",
            gap: "6px",
            flexWrap: "nowrap",
          }}
          className="desktop-nav-container"
        >
          {mainNav.map((item) => {
            const active = isActive(item.href);
            return (
              <Link
                key={item.href}
                href={item.href}
                style={{
                  padding: "8px 14px",
                  borderRadius: "10px",
                  fontSize: "0.92rem",
                  fontWeight: active ? 700 : 500,
                  color: active ? "#38BDF8" : "#CBD5E1",
                  background: active
                    ? "rgba(14, 165, 233, 0.12)"
                    : "transparent",
                  border: active
                    ? "1px solid rgba(14, 165, 233, 0.25)"
                    : "1px solid transparent",
                  transition: "all 0.2s ease",
                  textDecoration: "none",
                }}
              >
                {item.name}
              </Link>
            );
          })}

          {/* MORE APPS DROPDOWN */}
          <div
            ref={moreRef}
            style={{ position: "relative" }}
            onMouseEnter={() => setMoreOpen(true)}
            onMouseLeave={() => setMoreOpen(false)}
          >
            {(() => {
              const isMoreActive = moreNav.some((item) => isActive(item.href));
              return (
                <>
                  <button
                    type="button"
                    onClick={() => setMoreOpen((prev) => !prev)}
                    style={{
                      padding: "8px 12px",
                      borderRadius: "10px",
                      fontSize: "0.92rem",
                      fontWeight: isMoreActive ? 700 : 500,
                      color: isMoreActive || moreOpen ? "#38BDF8" : "#CBD5E1",
                      background:
                        isMoreActive || moreOpen
                          ? "rgba(14, 165, 233, 0.12)"
                          : "transparent",
                      border:
                        isMoreActive || moreOpen
                          ? "1px solid rgba(14, 165, 233, 0.25)"
                          : "1px solid transparent",
                      cursor: "pointer",
                      display: "flex",
                      alignItems: "center",
                      gap: "6px",
                      transition: "all 0.2s ease",
                    }}
                  >
                    <span>More</span>
                    <ChevronDown
                      size={14}
                      style={{
                        transition: "transform 0.2s ease",
                        transform: moreOpen ? "rotate(180deg)" : "none",
                      }}
                    />
                  </button>

                  {moreOpen && (
                    <div
                      style={{
                        position: "absolute",
                        top: "100%",
                        left: 0,
                        paddingTop: "6px",
                        zIndex: 150,
                      }}
                    >
                      <div
                        style={{
                          width: "210px",
                          background: "rgba(15, 23, 42, 0.96)",
                          backdropFilter: "blur(20px)",
                          WebkitBackdropFilter: "blur(20px)",
                          border: "1px solid rgba(255, 255, 255, 0.12)",
                          borderRadius: "14px",
                          padding: "6px",
                          boxShadow: "0 18px 40px rgba(0, 0, 0, 0.55)",
                        }}
                      >
                        {moreNav.map((item) => {
                          const Icon = item.icon;
                          const active = isActive(item.href);
                          return (
                            <Link
                              key={item.href}
                              href={item.href}
                              onClick={() => setMoreOpen(false)}
                              style={{
                                display: "flex",
                                alignItems: "center",
                                gap: "10px",
                                padding: "10px 12px",
                                borderRadius: "8px",
                                color: active ? "#38BDF8" : "#E2E8F0",
                                background: active
                                  ? "rgba(14, 165, 233, 0.12)"
                                  : "transparent",
                                fontSize: "0.88rem",
                                fontWeight: active ? 600 : 500,
                                textDecoration: "none",
                                transition: "all 0.15s ease",
                              }}
                            >
                              <Icon
                                size={16}
                                color={active ? "#38BDF8" : "#94A3B8"}
                              />
                              <span>{item.name}</span>
                            </Link>
                          );
                        })}
                      </div>
                    </div>
                  )}
                </>
              );
            })()}
          </div>
        </nav>

        {/* RIGHT ACTION CONTROLS */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "12px",
          }}
        >
          {/* NOTIFICATIONS BELL */}
          <Link
            href="/notifications"
            title="Notifications"
            style={{
              width: "38px",
              height: "38px",
              borderRadius: "10px",
              background: "rgba(255, 255, 255, 0.05)",
              border: "1px solid rgba(255, 255, 255, 0.10)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "#CBD5E1",
              position: "relative",
              transition: "all 0.2s ease",
            }}
          >
            <Bell size={18} />
            <span
              style={{
                position: "absolute",
                top: "8px",
                right: "8px",
                width: "7px",
                height: "7px",
                borderRadius: "50%",
                background: "#0EA5E9",
                boxShadow: "0 0 6px #0EA5E9",
              }}
            />
          </Link>

          {/* PLAN TRIP CTA */}
          <Link
            href="/planner"
            className="btn-primary"
            style={{
              padding: "8px 18px",
              fontSize: "0.88rem",
              display: "none",
            }}
            id="nav-plan-trip-cta"
          >
            <Sparkles size={15} />
            <span>Plan Trip</span>
          </Link>

          {/* USER PROFILE OR LOGIN */}
          {isLoggedIn ? (
            <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
              <Link
                href="/profile"
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "8px",
                  padding: "6px 14px",
                  borderRadius: "999px",
                  background: "rgba(14, 165, 233, 0.12)",
                  border: "1px solid rgba(14, 165, 233, 0.25)",
                  color: "#F8FAFC",
                  fontSize: "0.88rem",
                  fontWeight: 600,
                  textDecoration: "none",
                }}
              >
                <User size={15} color="#38BDF8" />
                <span
                  className="profile-name-trunc"
                  style={{
                    maxWidth: "110px",
                    overflow: "hidden",
                    textOverflow: "ellipsis",
                    whiteSpace: "nowrap",
                  }}
                >
                  {userName.split(" ")[0]}
                </span>
              </Link>
              <button
                onClick={handleLogout}
                title="Sign Out"
                style={{
                  background: "rgba(255, 255, 255, 0.05)",
                  border: "1px solid rgba(255, 255, 255, 0.10)",
                  borderRadius: "10px",
                  width: "38px",
                  height: "38px",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  cursor: "pointer",
                  color: "#94A3B8",
                }}
              >
                <LogOut size={16} />
              </button>
            </div>
          ) : (
            <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
              <Link
                href="/login"
                style={{
                  color: "#CBD5E1",
                  fontSize: "0.9rem",
                  fontWeight: 600,
                  padding: "8px 14px",
                  textDecoration: "none",
                }}
              >
                Sign In
              </Link>
              <Link
                href="/register"
                className="btn-primary"
                style={{
                  padding: "8px 16px",
                  fontSize: "0.88rem",
                }}
              >
                Register
              </Link>
            </div>
          )}

          {/* MOBILE HAMBURGER BUTTON */}
          <button
            type="button"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            aria-label="Toggle navigation menu"
            style={{
              width: "38px",
              height: "38px",
              borderRadius: "10px",
              background: "rgba(255, 255, 255, 0.05)",
              border: "1px solid rgba(255, 255, 255, 0.10)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "#FFFFFF",
              cursor: "pointer",
            }}
            className="mobile-hamburger-btn"
          >
            {mobileMenuOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>
      </div>

      {/* MOBILE SLIDE-OUT DRAWER */}
      {mobileMenuOpen && (
        <div
          style={{
            position: "fixed",
            top: "66px",
            left: 0,
            right: 0,
            bottom: 0,
            background: "rgba(3, 7, 18, 0.95)",
            backdropFilter: "blur(24px)",
            borderTop: "1px solid rgba(255, 255, 255, 0.08)",
            zIndex: 99,
            padding: "24px",
            overflowY: "auto",
            display: "flex",
            flexDirection: "column",
            gap: "18px",
          }}
        >
          <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
            <span
              style={{
                fontSize: "0.75rem",
                fontWeight: 700,
                color: "#64748B",
                textTransform: "uppercase",
                letterSpacing: "1px",
                marginBottom: "4px",
              }}
            >
              Navigation
            </span>
            {[...mainNav, ...moreNav].map((item) => {
              const active = isActive(item.href);
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                    padding: "14px 18px",
                    borderRadius: "14px",
                    color: active ? "#38BDF8" : "#F1F5F9",
                    background: active
                      ? "rgba(14, 165, 233, 0.12)"
                      : "rgba(255, 255, 255, 0.03)",
                    border: active
                      ? "1px solid rgba(14, 165, 233, 0.30)"
                      : "1px solid rgba(255, 255, 255, 0.06)",
                    fontSize: "1.05rem",
                    fontWeight: active ? 700 : 500,
                    textDecoration: "none",
                  }}
                >
                  <span>{item.name}</span>
                  {active && (
                    <span
                      style={{
                        width: "6px",
                        height: "6px",
                        borderRadius: "50%",
                        background: "#38BDF8",
                      }}
                    />
                  )}
                </Link>
              );
            })}
          </div>

          <div
            style={{
              marginTop: "auto",
              paddingTop: "20px",
              display: "flex",
              flexDirection: "column",
              gap: "10px",
            }}
          >
            <Link
              href="/planner"
              className="btn-primary"
              style={{ width: "100%", padding: "14px", fontSize: "1rem" }}
            >
              <Sparkles size={18} />
              <span>Launch AI Planner</span>
            </Link>

            {isLoggedIn ? (
              <button
                onClick={handleLogout}
                className="btn-secondary"
                style={{
                  width: "100%",
                  padding: "12px",
                  justifyContent: "center",
                }}
              >
                <LogOut size={16} />
                <span>Sign Out</span>
              </button>
            ) : (
              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "1fr 1fr",
                  gap: "10px",
                }}
              >
                <Link
                  href="/login"
                  className="btn-secondary"
                  style={{ padding: "12px", textAlign: "center" }}
                >
                  Sign In
                </Link>
                <Link
                  href="/register"
                  className="btn-primary"
                  style={{ padding: "12px", textAlign: "center" }}
                >
                  Register
                </Link>
              </div>
            )}
          </div>
        </div>
      )}

      {/* RESPONSIVE MEDIA STYLES */}
      <style jsx>{`
        @media (min-width: 1024px) {
          .desktop-nav-container {
            display: flex !important;
          }
          #nav-plan-trip-cta {
            display: inline-flex !important;
          }
          .mobile-hamburger-btn {
            display: none !important;
          }
        }
      `}</style>
    </header>
  );
}
