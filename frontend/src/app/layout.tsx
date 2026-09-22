import type { Metadata, Viewport } from "next";
import { Toaster } from "react-hot-toast";
import "./globals.css";
import AppNavbar from "../components/layout/AppNavbar";
import AppFooter from "../components/layout/AppFooter";

export const viewport: Viewport = {
  themeColor: "#030712",
  width: "device-width",
  initialScale: 1,
};

export const metadata: Metadata = {
  title: "TripGenius — AI-Powered Sustainable Travel Intelligence",
  description:
    "Next-generation travel platform generating personalized, eco-conscious, data-backed travel itineraries.",
  keywords: [
    "travel",
    "ai travel planner",
    "sustainable tourism",
    "itinerary generator",
    "eco travel score",
    "personalized vacation",
  ],
  authors: [{ name: "TripGenius" }],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <Toaster
          position="top-right"
          toastOptions={{
            style: {
              background: "rgba(15, 23, 42, 0.95)",
              color: "#F8FAFC",
              border: "1px solid rgba(255, 255, 255, 0.12)",
              backdropFilter: "blur(16px)",
              borderRadius: "12px",
              fontSize: "0.9rem",
            },
            success: {
              iconTheme: {
                primary: "#10B981",
                secondary: "#FFFFFF",
              },
            },
            error: {
              iconTheme: {
                primary: "#EF4444",
                secondary: "#FFFFFF",
              },
            },
          }}
        />
        <AppNavbar />
        <main
          style={{
            minHeight: "calc(100vh - 350px)",
            position: "relative",
            zIndex: 1,
          }}
        >
          {children}
        </main>
        <AppFooter />
      </body>
    </html>
  );
}
