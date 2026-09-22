"use client";

import { useEffect, useState, useMemo } from "react";
import Link from "next/link";
import {
  Bell,
  Check,
  Trash2,
  Sparkles,
  Calendar,
  DollarSign,
  MapPin,
  AlertCircle,
  Clock,
  ArrowRight,
} from "lucide-react";
import Button from "../../components/ui/Button";
import Badge from "../../components/ui/Badge";
import { GlassCard, SectionHeader } from "../../components/ui/Card";

interface NotificationItem {
  id: number;
  title: string;
  message: string;
  type: "trip" | "ai" | "budget" | "destination";
  read: boolean;
  created_at: string;
  link?: string;
}

const DEFAULT_NOTIFICATIONS: NotificationItem[] = [
  {
    id: 1,
    title: "Upcoming Munnar Trip Departure",
    message:
      "Your 3-day Munnar tea sanctuary itinerary starts in 48 hours. Check live mountain weather updates.",
    type: "trip",
    read: false,
    created_at: "2 hours ago",
    link: "/trip/history",
  },
  {
    id: 2,
    title: "AI Itinerary Insight: Coorg",
    message:
      "Based on your interest in mountain treks, coffee blossom season in Coorg is currently peaking.",
    type: "ai",
    read: false,
    created_at: "Yesterday",
    link: "/planner?destination=Coorg",
  },
  {
    id: 3,
    title: "Eco Score Milestone Reached",
    message:
      "You maintained an average sustainability score of 86/100 across all journeys this season!",
    type: "trip",
    read: true,
    created_at: "3 days ago",
    link: "/achievements",
  },
  {
    id: 4,
    title: "Monsoon Weather Advisory",
    message:
      "Coastal Kerala expects moderate rainfall next week. Light water-resistant packing recommended.",
    type: "destination",
    read: true,
    created_at: "5 days ago",
  },
];

export default function NotificationsPage() {
  const [notifications, setNotifications] = useState<NotificationItem[]>([]);
  const [filter, setFilter] = useState<"all" | "unread" | "trip" | "ai">("all");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    try {
      const stored = localStorage.getItem("tripgenius_notifications");
      if (stored) {
        setNotifications(JSON.parse(stored));
      } else {
        setNotifications(DEFAULT_NOTIFICATIONS);
        localStorage.setItem(
          "tripgenius_notifications",
          JSON.stringify(DEFAULT_NOTIFICATIONS),
        );
      }
    } catch {
      setNotifications(DEFAULT_NOTIFICATIONS);
    }
    setLoading(false);
  }, []);

  const saveNotifications = (items: NotificationItem[]) => {
    setNotifications(items);
    localStorage.setItem("tripgenius_notifications", JSON.stringify(items));
  };

  const markAllAsRead = () => {
    const updated = notifications.map((n) => ({ ...n, read: true }));
    saveNotifications(updated);
  };

  const clearAll = () => {
    saveNotifications([]);
  };

  const toggleRead = (id: number) => {
    const updated = notifications.map((n) =>
      n.id === id ? { ...n, read: !n.read } : n,
    );
    saveNotifications(updated);
  };

  const deleteNotification = (id: number) => {
    const updated = notifications.filter((n) => n.id !== id);
    saveNotifications(updated);
  };

  const filtered = useMemo(() => {
    return notifications.filter((n) => {
      if (filter === "unread") return !n.read;
      if (filter === "trip") return n.type === "trip";
      if (filter === "ai") return n.type === "ai";
      return true;
    });
  }, [notifications, filter]);

  const unreadCount = notifications.filter((n) => !n.read).length;

  const getIcon = (type: string) => {
    switch (type) {
      case "trip":
        return <Calendar size={18} color="#0EA5E9" />;
      case "ai":
        return <Sparkles size={18} color="#FBBF24" />;
      case "budget":
        return <DollarSign size={18} color="#34D399" />;
      default:
        return <MapPin size={18} color="#C084FC" />;
    }
  };

  return (
    <div
      className="page-container"
      style={{
        maxWidth: "960px",
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
            <Badge variant="ai" size="sm" icon={<Bell size={12} />}>
              Notification Hub
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
            Notifications ({unreadCount} New)
          </h1>
          <p
            style={{ color: "#94A3B8", fontSize: "0.95rem", marginTop: "4px" }}
          >
            Stay informed on upcoming itinerary dates, weather updates, and AI
            destination alerts.
          </p>
        </div>

        <div style={{ display: "flex", gap: "10px" }}>
          {unreadCount > 0 && (
            <Button
              variant="secondary"
              size="sm"
              leftIcon={<Check size={14} />}
              onClick={markAllAsRead}
            >
              Mark All Read
            </Button>
          )}
          {notifications.length > 0 && (
            <Button
              variant="ghost"
              size="sm"
              leftIcon={<Trash2 size={14} />}
              onClick={clearAll}
            >
              Clear All
            </Button>
          )}
        </div>
      </div>

      {/* FILTER TABS */}
      <div
        style={{
          display: "flex",
          gap: "8px",
          borderBottom: "1px solid rgba(255, 255, 255, 0.08)",
          paddingBottom: "12px",
        }}
      >
        {[
          { id: "all", label: "All Alerts" },
          { id: "unread", label: `Unread (${unreadCount})` },
          { id: "trip", label: "Trip Schedules" },
          { id: "ai", label: "AI Insights" },
        ].map((tab) => (
          <button
            key={tab.id}
            type="button"
            onClick={() => setFilter(tab.id as any)}
            style={{
              padding: "8px 16px",
              borderRadius: "10px",
              background:
                filter === tab.id ? "rgba(14, 165, 233, 0.15)" : "transparent",
              border:
                filter === tab.id
                  ? "1px solid rgba(14, 165, 233, 0.3)"
                  : "1px solid transparent",
              color: filter === tab.id ? "#38BDF8" : "#94A3B8",
              fontSize: "0.88rem",
              fontWeight: filter === tab.id ? 700 : 500,
              cursor: "pointer",
              transition: "all 0.2s ease",
            }}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* NOTIFICATIONS LIST */}
      {filtered.length > 0 ? (
        <div style={{ display: "flex", flexDirection: "column", gap: "14px" }}>
          {filtered.map((item) => (
            <GlassCard
              key={item.id}
              style={{
                padding: "20px 24px",
                display: "flex",
                alignItems: "flex-start",
                gap: "16px",
                background: item.read
                  ? "rgba(15, 23, 42, 0.55)"
                  : "rgba(15, 23, 42, 0.85)",
                border: item.read
                  ? "1px solid rgba(255, 255, 255, 0.06)"
                  : "1px solid rgba(14, 165, 233, 0.30)",
                position: "relative",
              }}
            >
              <div
                style={{
                  width: "40px",
                  height: "40px",
                  borderRadius: "12px",
                  background: "rgba(255, 255, 255, 0.05)",
                  border: "1px solid rgba(255, 255, 255, 0.10)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  flexShrink: 0,
                }}
              >
                {getIcon(item.type)}
              </div>

              <div style={{ flex: 1 }}>
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "baseline",
                    marginBottom: "4px",
                  }}
                >
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: "8px",
                    }}
                  >
                    <h3
                      style={{
                        fontSize: "1.05rem",
                        fontWeight: 700,
                        color: item.read ? "#CBD5E1" : "#FFFFFF",
                      }}
                    >
                      {item.title}
                    </h3>
                    {!item.read && (
                      <span
                        style={{
                          width: "8px",
                          height: "8px",
                          borderRadius: "50%",
                          background: "#0EA5E9",
                        }}
                      />
                    )}
                  </div>
                  <span style={{ fontSize: "0.78rem", color: "#64748B" }}>
                    {item.created_at}
                  </span>
                </div>

                <p
                  style={{
                    color: "#94A3B8",
                    fontSize: "0.9rem",
                    lineHeight: 1.6,
                    marginBottom: item.link ? "12px" : "0",
                  }}
                >
                  {item.message}
                </p>

                {item.link && (
                  <Link
                    href={item.link}
                    style={{
                      textDecoration: "none",
                      display: "inline-flex",
                      alignItems: "center",
                      gap: "4px",
                      color: "#38BDF8",
                      fontSize: "0.85rem",
                      fontWeight: 600,
                    }}
                  >
                    <span>View Details</span> <ArrowRight size={13} />
                  </Link>
                )}
              </div>

              <div
                style={{ display: "flex", gap: "8px", alignItems: "center" }}
              >
                <button
                  type="button"
                  onClick={() => toggleRead(item.id)}
                  title={item.read ? "Mark as unread" : "Mark as read"}
                  style={{
                    background: "transparent",
                    border: "none",
                    color: item.read ? "#64748B" : "#38BDF8",
                    cursor: "pointer",
                    padding: "4px",
                  }}
                >
                  <Check size={16} />
                </button>
                <button
                  type="button"
                  onClick={() => deleteNotification(item.id)}
                  title="Delete notification"
                  style={{
                    background: "transparent",
                    border: "none",
                    color: "#64748B",
                    cursor: "pointer",
                    padding: "4px",
                  }}
                >
                  <Trash2 size={16} />
                </button>
              </div>
            </GlassCard>
          ))}
        </div>
      ) : (
        <GlassCard style={{ padding: "60px 20px", textAlign: "center" }}>
          <div
            style={{
              width: "56px",
              height: "56px",
              borderRadius: "18px",
              background: "rgba(14, 165, 233, 0.12)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              margin: "0 auto 16px auto",
              color: "#38BDF8",
            }}
          >
            <Bell size={24} />
          </div>
          <h3
            style={{
              fontSize: "1.3rem",
              fontWeight: 700,
              color: "#FFFFFF",
              marginBottom: "6px",
            }}
          >
            No Notifications
          </h3>
          <p style={{ color: "#94A3B8", fontSize: "0.92rem" }}>
            You are all caught up! New trip reminders and AI alerts will appear
            here.
          </p>
        </GlassCard>
      )}
    </div>
  );
}
