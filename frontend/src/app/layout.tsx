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
  title: "Trip Geni — AI-Powered Sustainable Travel Intelligence",
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
  authors: [{ name: "Trip Geni" }],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link
          rel="preconnect"
          href="https://fonts.gstatic.com"
          crossOrigin="anonymous"
        />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&display=swap"
          rel="stylesheet"
        />
      </head>
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
