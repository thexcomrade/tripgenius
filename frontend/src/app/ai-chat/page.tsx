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
  Mic,
  MicOff,
  Volume2,
  VolumeX,
  Radio,
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
  "Plan a 3-day scenic trip to Thenkasi & Courtallam under ₹12,000",
  "Plan a 4-day scenic trip to Munnar under ₹18,000",
  "Best offbeat waterfalls and viewpoints near Wayanad",
  "Eco-friendly homestays and coffee trails in Coorg",
  "Relaxing 3-day beach escape to Varkala with seafood spots",
  "Romantic 5-day cultural holiday in Paris with top cafes",
];

// Safe UUID generator that works across all browser environments and non-HTTPS contexts
const generateMsgId = () => {
  if (typeof crypto !== "undefined" && typeof crypto.randomUUID === "function") {
    try {
      return crypto.randomUUID();
    } catch {
      // fallback
    }
  }
  return `msg-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
};

export default function AIChatPage() {
  const router = useRouter();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const [userName, setUserName] = useState<string>("Traveler");

  // In-Built 2026 Voice Assistant States
  const [isListening, setIsListening] = useState(false);
  const [speechSupported, setSpeechSupported] = useState(true);
  const [speakingId, setSpeakingId] = useState<string | null>(null);
  const [autoSendCountdown, setAutoSendCountdown] = useState<number | null>(null);
  const recognitionRef = useRef<any>(null);
  const silenceTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const countdownIntervalRef = useRef<NodeJS.Timeout | null>(null);
  const latestTranscriptRef = useRef<string>("");
  const handleSendMessageRef = useRef<(msgText?: string) => Promise<void>>(
    async () => {}
  );

  const cancelAutoSend = () => {
    if (silenceTimeoutRef.current) {
      clearTimeout(silenceTimeoutRef.current);
      silenceTimeoutRef.current = null;
    }
    if (countdownIntervalRef.current) {
      clearInterval(countdownIntervalRef.current);
      countdownIntervalRef.current = null;
    }
    setAutoSendCountdown(null);
  };

  // Load user name
  useEffect(() => {
    let name = "Traveler";
    const storedUser = localStorage.getItem("tripgenius_user");
    if (storedUser) {
      try {
        const parsed = JSON.parse(storedUser);
        name = parsed.full_name || parsed.name || parsed.username || "Traveler";
      } catch {
        // fallback
      }
    }
    setUserName(name);

    // Initialize or load chat
    const stored = localStorage.getItem("tripgenius_ai_chat");
    if (stored) {
      try {
        const parsed = JSON.parse(stored);
        if (Array.isArray(parsed) && parsed.length > 0) {
          // If first message has legacy misty Western Ghats intro, refresh it to the new clean greeting
          if (
            parsed[0].content &&
            parsed[0].content.includes("misty Western Ghats waterfalls")
          ) {
            parsed[0].content =
              `Namaskaram ${name}! 🙏 DASAPPAN here, your AI travel companion.\n\n` +
              `How may I help you today?\n\n` +
              `Tell me your dream destination, budget, or travel style, and I'll analyze your requirements to craft the perfect plan with verified stays and costs in ₹.\n\n` +
              `🎙️ **Voice Command Enabled**: You can speak with me using the microphone button below, or type your message. Trip Geni automatically sends your message after you finish speaking.\n\n` +
              `❓ Where would you like to travel, or what would you like me to plan for you?`;
            localStorage.setItem("tripgenius_ai_chat", JSON.stringify(parsed));
          }
          setMessages(parsed);
          return;
        }
      } catch {
        // ignore
      }
    }

    const welcome: ChatMessage = {
      id: "welcome-msg",
      role: "assistant",
      content:
        `Namaskaram ${name}! 🙏 DASAPPAN here, your AI travel companion.\n\n` +
        `How may I help you today?\n\n` +
        `Tell me your dream destination, budget, or travel style, and I'll analyze your requirements to craft the perfect plan with verified stays and costs in ₹.\n\n` +
        `🎙️ **Voice Command Enabled**: You can speak with me using the microphone button below, or type your message. Trip Geni automatically sends your message after you finish speaking.\n\n` +
        `❓ Where would you like to travel, or what would you like me to plan for you?`,
      timestamp: new Date().toISOString(),
    };
    setMessages([welcome]);
  }, []);

  // Web Speech API: English Voice Recognition Setup with Auto-Send on Silence
  useEffect(() => {
    if (typeof window !== "undefined") {
      const SpeechRecognition =
        (window as any).SpeechRecognition ||
        (window as any).webkitSpeechRecognition;

      if (SpeechRecognition) {
        try {
          const recognition = new SpeechRecognition();
          recognition.continuous = true;
          recognition.interimResults = true;
          recognition.lang = "en-US";

          recognition.onstart = () => {
            setIsListening(true);
          };

          recognition.onresult = (event: any) => {
            let transcript = "";
            for (let i = 0; i < event.results.length; i++) {
              transcript += event.results[i][0].transcript;
            }
            const clean = transcript.trim();
            if (clean) {
              setInput(clean);
              latestTranscriptRef.current = clean;

              // Reset any ongoing timers
              if (silenceTimeoutRef.current) {
                clearTimeout(silenceTimeoutRef.current);
              }
              if (countdownIntervalRef.current) {
                clearInterval(countdownIntervalRef.current);
              }

              // Start visual countdown for smooth user feedback
              setAutoSendCountdown(2);
              let remaining = 2;
              countdownIntervalRef.current = setInterval(() => {
                remaining -= 1;
                if (remaining > 0) {
                  setAutoSendCountdown(remaining);
                } else {
                  if (countdownIntervalRef.current) {
                    clearInterval(countdownIntervalRef.current);
                  }
                  setAutoSendCountdown(null);
                }
              }, 900);

              // 1.8s silence detector: if user stops speaking for 1.8s, automatically send!
              silenceTimeoutRef.current = setTimeout(() => {
                if (countdownIntervalRef.current) {
                  clearInterval(countdownIntervalRef.current);
                }
                setAutoSendCountdown(null);
                const textToSend = latestTranscriptRef.current.trim();
                if (textToSend) {
                  if (recognitionRef.current) {
                    try {
                      recognitionRef.current.stop();
                    } catch {}
                  }
                  setIsListening(false);
                  handleSendMessageRef.current?.(textToSend);
                }
              }, 1800);
            }
          };

          recognition.onerror = (event: any) => {
            console.warn("Speech recognition error:", event.error);
            cancelAutoSend();
            setIsListening(false);
          };

          recognition.onend = () => {
            setIsListening(false);
          };

          recognitionRef.current = recognition;
        } catch (e) {
          console.warn("Could not initialize SpeechRecognition:", e);
          setSpeechSupported(false);
        }
      } else {
        setSpeechSupported(false);
      }
    }
  }, []);

  useEffect(() => {
    if (messages.length > 0) {
      localStorage.setItem("tripgenius_ai_chat", JSON.stringify(messages));
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    } else {
      localStorage.removeItem("tripgenius_ai_chat");
    }
  }, [messages]);

  const toggleListening = () => {
    if (!recognitionRef.current) {
      alert("Voice input is not supported in this browser. Please use Chrome, Edge, or Safari.");
      return;
    }

    cancelAutoSend();

    if (isListening) {
      try {
        recognitionRef.current.stop();
      } catch {}
      setIsListening(false);
    } else {
      try {
        latestTranscriptRef.current = "";
        recognitionRef.current.start();
        setIsListening(true);
      } catch (err) {
        console.warn("Recognition start failed:", err);
      }
    }
  };

  // Text-To-Speech (TTS Voice Narration with Dasappan Male Voice & Brisk Pace)
  const handleSpeak = (text: string, msgId: string) => {
    if (typeof window === "undefined" || !("speechSynthesis" in window)) {
      return;
    }

    if (speakingId === msgId) {
      window.speechSynthesis.cancel();
      setSpeakingId(null);
      return;
    }

    window.speechSynthesis.cancel();

    // Clean markdown and symbols for crisp English speech
    const cleanSpeech = text
      .replace(/[*#_~`>•]/g, " ")
      .replace(/[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]/gu, "")
      .replace(/₹/g, " Rupees ")
      .replace(/\s+/g, " ")
      .trim();

    const utterance = new SpeechSynthesisUtterance(cleanSpeech);
    utterance.rate = 1.15; // Brisk, fluid, responsive reading pace
    utterance.pitch = 0.98; // Grounded, warm male tone
    utterance.lang = "en-US";

    const voices = window.speechSynthesis.getVoices();
    // Prioritize authentic, clear male English voices suitable for Dasappan
    const maleVoice =
      voices.find(
        (v) =>
          v.lang.startsWith("en") &&
          (v.name.toLowerCase().includes("male") ||
            v.name.toLowerCase().includes("david") ||
            v.name.toLowerCase().includes("george") ||
            v.name.toLowerCase().includes("guy") ||
            v.name.toLowerCase().includes("mark") ||
            v.name.toLowerCase().includes("prabhat") ||
            v.name.toLowerCase().includes("ravi") ||
            v.name.toLowerCase().includes("google uk english male") ||
            v.name.toLowerCase().includes("natural") ||
            v.name.toLowerCase().includes("ryan"))
      ) ||
      voices.find(
        (v) =>
          v.lang.startsWith("en") &&
          !v.name.toLowerCase().includes("female") &&
          !v.name.toLowerCase().includes("zira") &&
          !v.name.toLowerCase().includes("samantha") &&
          !v.name.toLowerCase().includes("victoria") &&
          !v.name.toLowerCase().includes("karen")
      ) ||
      voices.find((v) => v.lang.startsWith("en"));

    if (maleVoice) {
      utterance.voice = maleVoice;
    }

    utterance.onend = () => setSpeakingId(null);
    utterance.onerror = () => setSpeakingId(null);

    setSpeakingId(msgId);
    window.speechSynthesis.speak(utterance);
  };

  const handleClearChat = () => {
    if (speakingId && typeof window !== "undefined") {
      window.speechSynthesis.cancel();
      setSpeakingId(null);
    }
    cancelAutoSend();
    setInput("");
    setMessages([]);
    localStorage.removeItem("tripgenius_ai_chat");
  };

  const handleCopy = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const extractDestination = (text: string): string | undefined => {
    const keywords = [
      "Varanasi",
      "Kashi",
      "Banaras",
      "Benares",
      "Thenkasi",
      "Tenkasi",
      "Courtallam",
      "Vattavada",
      "Munnar",
      "Coorg",
      "Ooty",
      "Varkala",
      "Wayanad",
      "Kodaikanal",
      "Mysore",
      "Alleppey",
      "Goa",
      "Delhi",
      "Jaipur",
      "Manali",
      "Ladakh",
      "Paris",
      "Tokyo",
      "Bali",
      "Dubai",
    ];
    return keywords.find((k) => text.toLowerCase().includes(k.toLowerCase()));
  };

  const handleSendMessage = async (msgText?: string) => {
    cancelAutoSend();
    const textToSend = (msgText || input).trim();
    if (!textToSend || loading) return;

    if (isListening && recognitionRef.current) {
      try {
        recognitionRef.current.stop();
      } catch {}
      setIsListening(false);
    }

    const userMsg: ChatMessage = {
      id: generateMsgId(),
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

      const historyPayload = messages.slice(-6).map((m) => ({
        role: m.role,
        content: m.content,
      }));

      const res = await fetch(`${apiBase}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: textToSend,
          history: historyPayload,
          user_name: userName,
        }),
      });

      if (res.ok) {
        const data = await res.json();
        const assistantMsg: ChatMessage = {
          id: generateMsgId(),
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
        e
      );
    }

    // Intelligent client-side fallback matching Next-Gen Travel AI Engine 2.0
    setTimeout(() => {
      let aiReply = "";
      const lower = textToSend.toLowerCase();
      const greetingWords = ["hi", "hai", "hello", "hey", "namaskaram", "namaste"];
      const daysMatch = lower.match(/\b(\d+)\s*(?:day|days|d)\b/);
      const numDays = daysMatch ? parseInt(daysMatch[1], 10) : null;
      const hasTravelers = ["solo", "couple", "family", "friends", "group", "people", "person", "pax"].some((w) => lower.includes(w));
      const hasBudget = ["budget", "comfort", "luxury", "₹", "rs", "rupee", "cheap"].some((w) => lower.includes(w));

      if (greetingWords.some((g) => lower === g || lower.startsWith(g + " "))) {
        aiReply =
          `Namaskaram ${userName}! 🙏 DASAPPAN here, your AI travel companion.\n\n` +
          `How may I help you today?\n\n` +
          `Tell me your dream destination, budget, or the travel vibe you have in mind, and I'll analyze it to craft the ideal itinerary for you!\n\n` +
          `❓ Where would you like to travel, or what can I help you plan?`;
      } else if (dest && !numDays && !hasTravelers && !hasBudget) {
        // Consultative discovery: User said a destination without enough details -> Ask questions!
        aiReply =
          `Namaskaram ${userName}! 🙏\n\n` +
          `**${dest}** is an incredible choice! A deeply captivating journey awaits you.\n\n` +
          `To help me craft your personalized, day-by-day plan with verified stays and costs in ₹, could you tell me:\n\n` +
          `• 🗓️ **How many days** are you planning to spend? (e.g. 2–3 days for highlights or 4–5 days for deep immersion?)\n` +
          `• 👥 **How many travelers** will be joining you? (Solo, couple, family, or friends?)\n` +
          `• 💰 What is your approximate **budget tier**? (Budget backpacker, comfortable heritage stay, or luxury?)\n` +
          `• ✨ Any **must-have experiences**? (Temple darshan, morning boat rides, street food trails, silk shopping, or peaceful relaxation?)\n\n` +
          `Drop your details below, and I'll synthesize a comprehensive day-by-day plan with timings, authentic stays, food spots, and costs in ₹ for you!`;
      } else if (dest && (numDays || hasTravelers || hasBudget)) {
        // Full plan generation
        const days = numDays || 5;
        if (dest.toLowerCase().includes("varanasi") || dest.toLowerCase().includes("kashi") || dest.toLowerCase().includes("banaras")) {
          aiReply =
            `Namaskaram ${userName}! 🙏\n\n` +
            `Here is your bespoke **${days}-Day Varanasi (Kashi) Spiritual & Cultural Immersion Plan**:\n\n` +
            `### 🗓️ Day-by-Day Journey\n` +
            `• **Day 1: Arrival & The Sacred Evening Ganga Aarti** — Settle into your riverside haveli. Stroll from Assi Ghat to Dashashwamedh Ghat. At dusk, witness the hypnotic Ganga Aarti from a wooden boat on the river.\n` +
            `• **Day 2: Subah-e-Banaras & Kashi Vishwanath Corridor** — 5:30 AM rowboat cruise from Assi to Manikarnika Ghat at sunrise. Breakfast at Ram Bhandar (kachori-jalebi). Darshan at Kashi Vishwanath Corridor and Annapurna Temple.\n` +
            `• **Day 3: Sarnath & Buddhist Heritage** — Morning excursion to Sarnath (Dhamek Stupa & Archaeological Museum) where Lord Buddha gave his first sermon. Return for sunset reflections at Chet Singh Ghat.\n` +
            `• **Day 4: Heritage Galis, Silk Weaving & Ramnagar Fort** — Explore Madanpura handloom silk-weaving lanes. Visit Kal Bhairav Temple. Take a local boat to 18th-century sandstone Ramnagar Fort across the river.\n` +
            `• **Day 5: Northern Ghats & Culinary Farewell** — Gentle morning meditation at Panchganga Ghat. Savor famous Tamatar Chaat at Kashi Chaat Bhandar and clay-cup Blue Lassi before departure.\n\n` +
            `### 🏨 Recommended Stays\n` +
            `• Heritage Riverside Haveli on Ghats (~₹3,200 – ₹5,500/night)\n` +
            `• Boutique Comfort Stay near Godowlia (~₹1,800 – ₹2,800/night)\n\n` +
            `### 🍲 Iconic Food Trail\n` +
            `• Morning Kachori-Sabzi with hot Jalebis at Ram Bhandar\n` +
            `• Tamatar Chaat and Palak Patta Chaat at Kashi Chaat Bhandar\n` +
            `• Authentic saffron-topped Kulhad Lassi at Blue Lassi Shop\n` +
            `• Legendary Banarasi Meetha Paan at Keshav Paan\n\n` +
            `### 💰 Estimated Budget (in ₹)\n` +
            `• Daily Average: ~₹1,800 – ₹3,200 per person/day (stays, meals, hand-rowed boats, and transit)\n\n` +
            `### 💡 Dasappan's Local Insider Secret\n` +
            `Always hire a hand-rowed wooden boat (₹400–₹600) rather than a motorboat at dawn. The silence on the misty river at 5:45 AM is unforgettable.\n\n` +
            `Would you like hotel recommendations or help with temple darshan timings?`;
        } else {
          aiReply =
            `Namaskaram ${userName}! 🙏\n\n` +
            `Here is your tailored **${days}-Day ${dest} Travel Blueprint**:\n\n` +
            `### 🗓️ Curated ${days}-Day Itinerary\n` +
            `• **Day 1: Arrival & Local Immersion** — Check in, explore central heritage streets, enjoy local sunset viewpoints and authentic regional dinner.\n` +
            `• **Day 2: Iconic Landmarks & Scenic Exploration** — Guided exploration of prime natural and architectural wonders, panoramic photo stops, and signature cultural visits.\n` +
            `• **Day 3: Offbeat Trails & Cuisine** — Discover hidden nature trails, local artisan markets, and heritage dining.\n` +
            (days > 3 ? `• **Days 4–${days}: Leisure & Unique Excursions** — Deep dive into neighboring villages, scenic valleys or waterfronts, and souvenir shopping.\n\n` : `\n`) +
            `### 🏨 Stays & Dining\n` +
            `• Boutique stays & eco-resorts: ~₹2,200 – ₹4,500/night\n` +
            `• Authentic regional delicacies, fresh thalis, and local street treats\n\n` +
            `### 💰 Estimated Budget\n` +
            `• ~₹2,000 – ₹4,000 per person per day (covering stay, meals, and local transit in ₹)\n\n` +
            `Would you like me to refine this with specific hotel options or flight/train transit details?`;
        }
      } else {
        aiReply =
          `Namaskaram ${userName}! 🙏 I am here to help you plan an unforgettable trip.\n\n` +
          `Tell me your dream destination (e.g. Varanasi, Munnar, Goa, Paris, Tokyo), or ask me anything about budgets, stays, or packing essentials!`;
      }

      const assistantMsg: ChatMessage = {
        id: generateMsgId(),
        role: "assistant",
        content: aiReply,
        timestamp: new Date().toISOString(),
        suggestedDestination: dest,
      };

      setMessages((prev) => [...prev, assistantMsg]);
      setLoading(false);
    }, 400);
  };

  handleSendMessageRef.current = handleSendMessage;

  return (
    <div
      className="page-container"
      style={{
        maxWidth: "1000px",
        display: "flex",
        flexDirection: "column",
        height: "calc(100vh - 80px)",
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
        <div style={{ display: "flex", alignItems: "center", gap: "14px" }}>
          <div
            style={{
              width: "48px",
              height: "48px",
              borderRadius: "50%",
              background:
                "radial-gradient(circle, rgba(14, 165, 233, 0.25) 0%, rgba(2, 132, 199, 0.1) 100%)",
              border: "2.5px solid #0EA5E9",
              boxShadow:
                "0 0 16px rgba(14, 165, 233, 0.50), inset 0 0 8px rgba(14, 165, 233, 0.25)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              overflow: "hidden",
              flexShrink: 0,
            }}
          >
            <img
              src="/images/das.ico"
              alt="DASAPPAN"
              style={{
                width: "100%",
                height: "100%",
                objectFit: "cover",
                borderRadius: "50%",
              }}
              onError={(e) => {
                (e.target as HTMLImageElement).src = "/images/das.png";
              }}
            />
          </div>
          <div>
            <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
              <h2
                style={{
                  fontSize: "1.2rem",
                  fontWeight: 800,
                  color: "#FFFFFF",
                  margin: 0,
                }}
              >
                DASAPPAN
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
            <p
              style={{
                fontSize: "0.8rem",
                color: "#94A3B8",
                margin: "2px 0 0 0",
              }}
            >
              AI Travel Companion • Voice Enabled • Global Planning
            </p>
          </div>
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
          <Button
            variant="ghost"
            size="sm"
            onClick={handleClearChat}
            leftIcon={<Trash2 size={14} />}
          >
            Clear
          </Button>
        </div>
      </div>

      {/* QUICK SUGGESTIONS CAROUSEL */}
      <div
        style={{
          display: "flex",
          gap: "8px",
          padding: "12px 0",
          overflowX: "auto",
          scrollbarWidth: "none",
        }}
      >
        {PROMPT_SUGGESTIONS.map((s, idx) => (
          <button
            key={idx}
            type="button"
            onClick={() => handleSendMessage(s)}
            style={{
              background: "rgba(255, 255, 255, 0.04)",
              border: "1px solid rgba(255, 255, 255, 0.08)",
              borderRadius: "999px",
              padding: "6px 14px",
              fontSize: "0.8rem",
              color: "#CBD5E1",
              cursor: "pointer",
              whiteSpace: "nowrap",
              transition: "all 0.2s",
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = "rgba(14, 165, 233, 0.15)";
              e.currentTarget.style.borderColor = "#0EA5E9";
              e.currentTarget.style.color = "#FFFFFF";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = "rgba(255, 255, 255, 0.04)";
              e.currentTarget.style.borderColor = "rgba(255, 255, 255, 0.08)";
              e.currentTarget.style.color = "#CBD5E1";
            }}
          >
            {s}
          </button>
        ))}
      </div>

      {/* MESSAGES CONTAINER */}
      <div
        style={{
          flex: 1,
          overflowY: "auto",
          display: "flex",
          flexDirection: "column",
          gap: "18px",
          padding: "12px 4px",
        }}
      >
        {messages.length === 0 && (
          <div
            style={{
              flex: 1,
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              gap: "12px",
              color: "#64748B",
              padding: "60px 20px",
              textAlign: "center",
            }}
          >
            <Sparkles size={36} color="#38BDF8" style={{ opacity: 0.7 }} />
            <div style={{ fontSize: "1.1rem", fontWeight: 600, color: "#94A3B8" }}>
              Conversation Cleared
            </div>
            <p style={{ fontSize: "0.88rem", maxWidth: "420px", color: "#64748B", lineHeight: 1.5 }}>
              Ask DASAPPAN anything about destinations worldwide, budgets, stays, or tap any suggestion above to start fresh.
            </p>
          </div>
        )}

        {messages.map((msg) => {
          const isUser = msg.role === "user";
          return (
            <div
              key={msg.id}
              style={{
                display: "flex",
                gap: "12px",
                alignItems: "flex-start",
                justifyContent: isUser ? "flex-end" : "flex-start",
              }}
            >
              {!isUser && (
                <div
                  style={{
                    width: "36px",
                    height: "36px",
                    borderRadius: "50%",
                    background: "rgba(14, 165, 233, 0.15)",
                    border: "2px solid #0EA5E9",
                    boxShadow: "0 0 10px rgba(14, 165, 233, 0.40)",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    overflow: "hidden",
                    flexShrink: 0,
                    marginTop: "2px",
                  }}
                >
                  <img
                    src="/images/das.ico"
                    alt="DASAPPAN"
                    style={{
                      width: "100%",
                      height: "100%",
                      objectFit: "cover",
                      borderRadius: "50%",
                    }}
                    onError={(e) => {
                      (e.target as HTMLImageElement).src = "/images/das.png";
                    }}
                  />
                </div>
              )}

              <div
                style={{
                  maxWidth: "75%",
                  display: "flex",
                  flexDirection: "column",
                  gap: "6px",
                  alignItems: isUser ? "flex-end" : "flex-start",
                }}
              >
                <div
                  style={{
                    padding: "14px 18px",
                    borderRadius: isUser
                      ? "18px 18px 4px 18px"
                      : "18px 18px 18px 4px",
                    background: isUser
                      ? "linear-gradient(135deg, #0EA5E9, #0284C7)"
                      : "rgba(15, 23, 42, 0.85)",
                    backdropFilter: "blur(12px)",
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
                      gap: "12px",
                      marginTop: "2px",
                    }}
                  >
                    {/* TTS VOICE PLAYBACK BUTTON */}
                    <button
                      type="button"
                      onClick={() => handleSpeak(msg.content, msg.id)}
                      style={{
                        background:
                          speakingId === msg.id
                            ? "rgba(14, 165, 233, 0.2)"
                            : "transparent",
                        border:
                          speakingId === msg.id
                            ? "1px solid rgba(14, 165, 233, 0.5)"
                            : "none",
                        borderRadius: "6px",
                        padding: "2px 6px",
                        color: speakingId === msg.id ? "#38BDF8" : "#94A3B8",
                        fontSize: "0.78rem",
                        cursor: "pointer",
                        display: "flex",
                        alignItems: "center",
                        gap: "4px",
                        transition: "all 0.2s",
                      }}
                      title={
                        speakingId === msg.id
                          ? "Stop voice playback"
                          : "Listen in English voice (TTS)"
                      }
                    >
                      {speakingId === msg.id ? (
                        <VolumeX size={13} color="#38BDF8" />
                      ) : (
                        <Volume2 size={13} />
                      )}
                      <span>
                        {speakingId === msg.id ? "Stop Voice" : "Voice Readout"}
                      </span>
                    </button>

                    {/* COPY BUTTON */}
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
                            `/planner?destination=${encodeURIComponent(msg.suggestedDestination!)}`
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
                        <Sparkles size={11} /> Open {msg.suggestedDestination} in Planner
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
                width: "36px",
                height: "36px",
                borderRadius: "50%",
                background: "rgba(14, 165, 233, 0.20)",
                border: "2px solid #0EA5E9",
                boxShadow: "0 0 10px rgba(14, 165, 233, 0.40)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                overflow: "hidden",
                flexShrink: 0,
              }}
            >
              <img
                src="/images/das.ico"
                alt="DASAPPAN"
                style={{
                  width: "100%",
                  height: "100%",
                  objectFit: "cover",
                  borderRadius: "50%",
                }}
                onError={(e) => {
                  (e.target as HTMLImageElement).src = "/images/das.png";
                }}
              />
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

      {/* LISTENING INDICATOR BANNER */}
      {isListening && (
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            background:
              "linear-gradient(90deg, rgba(239, 68, 68, 0.20), rgba(14, 165, 233, 0.20))",
            border: "1px solid rgba(239, 68, 68, 0.40)",
            borderRadius: "12px",
            padding: "8px 16px",
            marginBottom: "6px",
            animation: "pulseAura 2s infinite",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
            <span
              style={{
                width: "10px",
                height: "10px",
                borderRadius: "50%",
                background: "#EF4444",
                boxShadow: "0 0 10px #EF4444",
                animation: "blink 1s infinite",
              }}
            />
            <span style={{ fontSize: "0.85rem", color: "#F8FAFC", fontWeight: 600 }}>
              Listening to your voice in English... Speak your question or destination
            </span>
          </div>
          <button
            type="button"
            onClick={toggleListening}
            style={{
              background: "rgba(239, 68, 68, 0.3)",
              border: "1px solid rgba(239, 68, 68, 0.6)",
              color: "#FFFFFF",
              borderRadius: "6px",
              padding: "2px 8px",
              fontSize: "0.75rem",
              cursor: "pointer",
            }}
          >
            Done
          </button>
        </div>
      )}

      {/* VOICE NLP AUTO-SEND COUNTDOWN BANNER */}
      {autoSendCountdown !== null && (
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            background:
              "linear-gradient(135deg, rgba(14, 165, 233, 0.18), rgba(20, 184, 166, 0.18))",
            border: "1px solid rgba(56, 189, 248, 0.45)",
            borderRadius: "14px",
            padding: "8px 14px",
            marginBottom: "8px",
            fontSize: "0.85rem",
            color: "#E0F2FE",
            backdropFilter: "blur(12px)",
            animation: "fadeIn 0.2s ease-in-out",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
            <span
              style={{
                width: "9px",
                height: "9px",
                borderRadius: "50%",
                background: "#10B981",
                boxShadow: "0 0 10px #10B981",
                display: "inline-block",
                animation: "blink 1s infinite",
              }}
            />
            <span>
              Voice recognized. Auto-sending in <b>{autoSendCountdown}s</b> after silence...
            </span>
          </div>

          <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
            <button
              type="button"
              onClick={cancelAutoSend}
              style={{
                background: "rgba(239, 68, 68, 0.2)",
                border: "1px solid rgba(239, 68, 68, 0.4)",
                color: "#FCA5A5",
                borderRadius: "8px",
                padding: "3px 10px",
                fontSize: "0.75rem",
                cursor: "pointer",
                fontWeight: 600,
                transition: "all 0.15s ease",
              }}
            >
              Cancel Auto-send
            </button>
            <button
              type="button"
              onClick={() => {
                cancelAutoSend();
                if (recognitionRef.current) {
                  try {
                    recognitionRef.current.stop();
                  } catch {}
                }
                setIsListening(false);
                handleSendMessage(latestTranscriptRef.current || input);
              }}
              style={{
                background: "#0EA5E9",
                border: "none",
                color: "#FFFFFF",
                borderRadius: "8px",
                padding: "3px 12px",
                fontSize: "0.75rem",
                fontWeight: 700,
                cursor: "pointer",
                boxShadow: "0 0 10px rgba(14, 165, 233, 0.5)",
              }}
            >
              Send Now
            </button>
          </div>
        </div>
      )}

      {/* CHAT INPUT COMPOSER WITH VOICE MIC BUTTON */}
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
          border: isListening
            ? "1.5px solid #0EA5E9"
            : "1px solid rgba(255, 255, 255, 0.12)",
          borderRadius: "16px",
          padding: "8px 12px 8px 14px",
          boxShadow: isListening
            ? "0 0 20px rgba(14, 165, 233, 0.4)"
            : "0 8px 24px rgba(0, 0, 0, 0.35)",
          marginTop: "8px",
          transition: "all 0.2s",
        }}
      >
        {/* VOICE INPUT MIC BUTTON */}
        <button
          type="button"
          onClick={toggleListening}
          title={
            isListening
              ? "Stop listening"
              : "Voice Command: Speak your destination or question in English"
          }
          style={{
            background: isListening
              ? "rgba(239, 68, 68, 0.25)"
              : "rgba(14, 165, 233, 0.12)",
            border: isListening
              ? "1.5px solid #EF4444"
              : "1.5px solid rgba(14, 165, 233, 0.35)",
            color: isListening ? "#F87171" : "#38BDF8",
            borderRadius: "50%",
            width: "36px",
            height: "36px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            cursor: "pointer",
            flexShrink: 0,
            boxShadow: isListening ? "0 0 12px rgba(239, 68, 68, 0.6)" : "none",
            transition: "all 0.2s ease",
          }}
        >
          {isListening ? <MicOff size={17} /> : <Mic size={17} />}
        </button>

        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={
            isListening
              ? "Listening to your voice..."
              : "Ask anything about destinations worldwide, budgets, stays, or packing..."
          }
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
        @keyframes blink {
          0%,
          100% {
            opacity: 1;
          }
          50% {
            opacity: 0.3;
          }
        }
        @keyframes pulseAura {
          0%,
          100% {
            box-shadow: 0 0 8px rgba(14, 165, 233, 0.2);
          }
          50% {
            box-shadow: 0 0 16px rgba(14, 165, 233, 0.4);
          }
        }
      `}</style>
    </div>
  );
}
