"use client";

import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import {
  Bot,
  User,
  Send,
  Sparkles,
  Trash2,
  Copy,
  Check,
  Compass,
  ArrowRight,
  MapPin,
} from "lucide-react";
import Button from "../../components/ui/Button";
import Badge from "../../components/ui/Badge";
import { GlassCard } from "../../components/ui/Card";

interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: string;
  suggestedDestination?: string;
}

const PROMPT_SUGGESTIONS = [
  "Plan a 4-day scenic trip to Munnar under ₹18,000",
  "Best offbeat waterfalls and viewpoints near Wayanad",
  "Eco-friendly homestays and coffee trails in Coorg",
  "Relaxing 3-day beach escape to Varkala with seafood spots",
  "What is the best season and weather for visiting Ooty?",
];

export default function AIChatPage() {
  const router = useRouter();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [copiedId, setCopiedId] = useState<string | null>(null);

  useEffect(() => {
    const stored = localStorage.getItem("tripgenius_ai_chat");
    if (stored) {
      try {
        setMessages(JSON.parse(stored));
      } catch {
        setMessages([]);
      }
    } else {
      const welcome: ChatMessage = {
        id: "welcome-msg",
        role: "assistant",
        content:
          "👋 Welcome! I am your TripGenius AI Travel Companion.\n\nI can help you analyze seasonal weather, estimate travel budgets, suggest eco-certified sanctuaries, and draft day-by-day itineraries across the Western Ghats and worldwide.\n\nWhere would you like to explore?",
        timestamp: new Date().toISOString(),
      };
      setMessages([welcome]);
    }
  }, []);

  useEffect(() => {
    if (messages.length > 0) {
      localStorage.setItem("tripgenius_ai_chat", JSON.stringify(messages));
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  const handleClearChat = () => {
    const welcome: ChatMessage = {
      id: crypto.randomUUID(),
      role: "assistant",
      content: "👋 Chat refreshed. Where can I help plan your next adventure?",
      timestamp: new Date().toISOString(),
    };
    setMessages([welcome]);
    localStorage.removeItem("tripgenius_ai_chat");
  };

  const handleCopy = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const extractDestination = (text: string): string | undefined => {
    const keywords = [
      "Munnar",
      "Coorg",
      "Ooty",
      "Varkala",
      "Wayanad",
      "Kodaikanal",
      "Mysore",
      "Alleppey",
      "Goa",
    ];
    return keywords.find((k) => text.toLowerCase().includes(k.toLowerCase()));
  };

  const handleSendMessage = async (msgText?: string) => {
    const textToSend = (msgText || input).trim();
    if (!textToSend || loading) return;

    const userMsg: ChatMessage = {
      id: crypto.randomUUID(),
      role: "user",
      content: textToSend,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    const dest = extractDestination(textToSend);

    try {
      const apiBase =
        process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
      const res = await fetch(`${apiBase}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: textToSend }),
      });

      if (res.ok) {
        const data = await res.json();
        const assistantMsg: ChatMessage = {
          id: crypto.randomUUID(),
          role: "assistant",
          content: data.reply || "I am ready to help plan your trip!",
          timestamp: new Date().toISOString(),
          suggestedDestination: dest,
        };
        setMessages((prev) => [...prev, assistantMsg]);
        setLoading(false);
        return;
      }
    } catch (e) {
      console.warn(
        "Backend chat endpoint unreachable, using client knowledge fallback:",
        e,
      );
    }

    // Intelligent client-side fallback
    setTimeout(() => {
      let aiReply = "";
      if (dest) {
        aiReply =
          `🌿 **TripGenius Guide for ${dest}**\n\n` +
          `• **Recommended Pacing**: 3 to 4 days for a complete, scenic immersion.\n` +
          `• **Optimal Travel Window**: September through March for pleasant temperatures and clear views.\n` +
          `• **Estimated Budget**: ~₹3,500 – ₹5,500 per day for 2 travelers (including boutique stay, authentic meals, and regional transit).\n` +
          `• **Must-See Highlights**: Scenic mountain trails, tea/spice plantations, local waterfalls, and cultural heritage viewpoints.\n` +
          `• **Culinary Specialties**: Freshly brewed highland teas, regional thali, and authentic delicacies.\n` +
          `• **Eco Travel Tip**: Choose certified green homestays and minimize single-use plastics.\n\n` +
          `👉 *You can use the TripGenius AI Planner to synthesize a full day-by-day itinerary with exact cost breakdown.*`;
      } else {
        aiReply =
          `✈️ **TripGenius Travel Advice for "${textToSend}"**\n\n` +
          `• **Top Destinations**: Munnar (highland tea gardens), Coorg (coffee hills & waterfalls), Varkala (cliffside beaches), and Wayanad (rainforest trails).\n` +
          `• **Planning Recommendation**: Allocate ~40% of budget to accommodations, 25% to regional dining, and 20% to low-carbon transit.\n` +
          `• **Pacing**: Dedicate at least 3 days per destination to balance travel transit with relaxed exploration.\n\n` +
          `👉 *Tap 'Open Planner' below to generate your complete bespoke itinerary.*`;
      }

      const assistantMsg: ChatMessage = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: aiReply,
        timestamp: new Date().toISOString(),
        suggestedDestination: dest,
      };

      setMessages((prev) => [...prev, assistantMsg]);
      setLoading(false);
    }, 800);
  };

  return (
    <div
      className="page-container"
      style={{
        maxWidth: "1000px",
        display: "flex",
        flexDirection: "column",
        height: "calc(100vh - 180px)",
        minHeight: "650px",
      }}
    >
      {/* CHAT HEADER */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          paddingBottom: "16px",
          borderBottom: "1px solid rgba(255, 255, 255, 0.08)",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
          <div
            style={{
              width: "42px",
              height: "42px",
              borderRadius: "12px",
              background: "linear-gradient(135deg, #0EA5E9, #14B8A6)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "#FFFFFF",
              boxShadow: "0 0 16px rgba(14, 165, 233, 0.40)",
            }}
          >
            <Bot size={22} />
          </div>
          <div>
            <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
              <h2
                style={{
                  fontSize: "1.25rem",
                  fontWeight: 800,
                  color: "#FFFFFF",
                }}
              >
                TripGenius AI Companion
              </h2>
              <span
                style={{
                  width: "8px",
                  height: "8px",
                  borderRadius: "50%",
                  background: "#10B981",
                  boxShadow: "0 0 8px #10B981",
                }}
              />
            </div>
            <p style={{ fontSize: "0.82rem", color: "#94A3B8" }}>
              Powered by Google Gemini & Regional Tourism Datasets
            </p>
          </div>
        </div>

        <button
          type="button"
          onClick={handleClearChat}
          title="Clear Conversation"
          style={{
            padding: "8px 14px",
            borderRadius: "10px",
            background: "rgba(255, 255, 255, 0.05)",
            border: "1px solid rgba(255, 255, 255, 0.10)",
            color: "#94A3B8",
            fontSize: "0.85rem",
            cursor: "pointer",
            display: "flex",
            alignItems: "center",
            gap: "6px",
          }}
        >
          <Trash2 size={14} /> Clear
        </button>
      </div>

      {/* PROMPT SUGGESTION CHIPS */}
      <div
        style={{
          display: "flex",
          gap: "8px",
          overflowX: "auto",
          padding: "14px 0 10px 0",
        }}
      >
        {PROMPT_SUGGESTIONS.map((prompt, idx) => (
          <button
            key={idx}
            type="button"
            onClick={() => handleSendMessage(prompt)}
            style={{
              padding: "6px 14px",
              borderRadius: "999px",
              background: "rgba(14, 165, 233, 0.08)",
              border: "1px solid rgba(14, 165, 233, 0.20)",
              color: "#CBD5E1",
              fontSize: "0.8rem",
              cursor: "pointer",
              whiteSpace: "nowrap",
              transition: "all 0.2s ease",
            }}
          >
            {prompt}
          </button>
        ))}
      </div>

      {/* MESSAGE STREAM */}
      <div
        style={{
          flex: 1,
          overflowY: "auto",
          padding: "16px 4px",
          display: "flex",
          flexDirection: "column",
          gap: "20px",
        }}
      >
        {messages.map((msg) => {
          const isUser = msg.role === "user";
          return (
            <div
              key={msg.id}
              style={{
                display: "flex",
                justifyContent: isUser ? "flex-end" : "flex-start",
                gap: "12px",
                maxWidth: "100%",
              }}
            >
              {!isUser && (
                <div
                  style={{
                    width: "34px",
                    height: "34px",
                    borderRadius: "10px",
                    background: "linear-gradient(135deg, #0EA5E9, #14B8A6)",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    color: "#FFFFFF",
                    flexShrink: 0,
                    marginTop: "4px",
                  }}
                >
                  <Bot size={18} />
                </div>
              )}

              <div
                style={{
                  maxWidth: "80%",
                  display: "flex",
                  flexDirection: "column",
                  gap: "8px",
                }}
              >
                <div
                  style={{
                    padding: "16px 20px",
                    borderRadius: isUser
                      ? "20px 20px 4px 20px"
                      : "4px 20px 20px 20px",
                    background: isUser
                      ? "linear-gradient(135deg, #0284C7, #0D9488)"
                      : "rgba(15, 23, 42, 0.85)",
                    border: isUser
                      ? "none"
                      : "1px solid rgba(255, 255, 255, 0.10)",
                    color: "#F8FAFC",
                    fontSize: "0.95rem",
                    lineHeight: 1.65,
                    whiteSpace: "pre-wrap",
                    boxShadow: "0 4px 16px rgba(0, 0, 0, 0.25)",
                  }}
                >
                  {msg.content}
                </div>

                {/* QUICK ACTIONS FOR ASSISTANT RESPONSES */}
                {!isUser && (
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: "10px",
                    }}
                  >
                    <button
                      type="button"
                      onClick={() => handleCopy(msg.content, msg.id)}
                      style={{
                        background: "transparent",
                        border: "none",
                        color: copiedId === msg.id ? "#34D399" : "#64748B",
                        fontSize: "0.78rem",
                        cursor: "pointer",
                        display: "flex",
                        alignItems: "center",
                        gap: "4px",
                      }}
                    >
                      {copiedId === msg.id ? (
                        <Check size={12} />
                      ) : (
                        <Copy size={12} />
                      )}
                      <span>{copiedId === msg.id ? "Copied" : "Copy"}</span>
                    </button>

                    {msg.suggestedDestination && (
                      <button
                        type="button"
                        onClick={() =>
                          router.push(
                            `/planner?destination=${encodeURIComponent(msg.suggestedDestination!)}`,
                          )
                        }
                        style={{
                          background: "rgba(14, 165, 233, 0.15)",
                          border: "1px solid rgba(14, 165, 233, 0.30)",
                          color: "#38BDF8",
                          borderRadius: "6px",
                          padding: "2px 8px",
                          fontSize: "0.78rem",
                          fontWeight: 600,
                          cursor: "pointer",
                          display: "flex",
                          alignItems: "center",
                          gap: "4px",
                        }}
                      >
                        <Sparkles size={11} /> Open {msg.suggestedDestination}{" "}
                        in Planner
                      </button>
                    )}
                  </div>
                )}
              </div>
            </div>
          );
        })}

        {loading && (
          <div style={{ display: "flex", gap: "12px", alignItems: "center" }}>
            <div
              style={{
                width: "34px",
                height: "34px",
                borderRadius: "10px",
                background: "rgba(14, 165, 233, 0.2)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                color: "#38BDF8",
              }}
            >
              <Bot size={18} />
            </div>
            <div
              style={{
                background: "rgba(15, 23, 42, 0.8)",
                padding: "12px 18px",
                borderRadius: "14px",
                border: "1px solid rgba(255, 255, 255, 0.08)",
                display: "flex",
                gap: "6px",
                alignItems: "center",
              }}
            >
              <span
                style={{
                  width: "6px",
                  height: "6px",
                  borderRadius: "50%",
                  background: "#38BDF8",
                  animation: "bounce 1.4s infinite",
                }}
              />
              <span
                style={{
                  width: "6px",
                  height: "6px",
                  borderRadius: "50%",
                  background: "#38BDF8",
                  animation: "bounce 1.4s infinite 0.2s",
                }}
              />
              <span
                style={{
                  width: "6px",
                  height: "6px",
                  borderRadius: "50%",
                  background: "#38BDF8",
                  animation: "bounce 1.4s infinite 0.4s",
                }}
              />
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* CHAT INPUT COMPOSER */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSendMessage();
        }}
        style={{
          display: "flex",
          alignItems: "center",
          gap: "10px",
          background: "rgba(15, 23, 42, 0.95)",
          backdropFilter: "blur(20px)",
          border: "1px solid rgba(255, 255, 255, 0.12)",
          borderRadius: "16px",
          padding: "8px 12px 8px 18px",
          boxShadow: "0 8px 24px rgba(0, 0, 0, 0.35)",
          marginTop: "12px",
        }}
      >
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask anything about destinations, budgets, stays, or packing..."
          style={{
            flex: 1,
            background: "transparent",
            border: "none",
            color: "#FFFFFF",
            fontSize: "0.95rem",
            outline: "none",
          }}
        />
        <Button
          type="submit"
          variant="primary"
          size="sm"
          disabled={!input.trim() || loading}
          rightIcon={<Send size={14} />}
        >
          Send
        </Button>
      </form>

      <style jsx>{`
        @keyframes bounce {
          0%,
          80%,
          100% {
            transform: scale(0);
          }
          40% {
            transform: scale(1);
          }
        }
      `}</style>
    </div>
  );
}
