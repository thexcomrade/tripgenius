"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

interface SavedTrip {
  id: string;
  destination: string;
  duration_days: number;
  budget: number;
  travel_style: string;
  created_at: string;
}

export default function SavedTripsPage() {
  const router = useRouter();

  const [savedTrips, setSavedTrips] = useState<SavedTrip[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadSavedTrips();
  }, []);

  function loadSavedTrips() {
    try {
      const storedTrips = localStorage.getItem("tripgenius_saved_trips");

      if (storedTrips) {
        setSavedTrips(JSON.parse(storedTrips));
      }
    } catch (error) {
      console.error("Failed to load saved trips:", error);
    } finally {
      setLoading(false);
    }
  }

  function deleteTrip(id: string) {
    const updatedTrips = savedTrips.filter((trip) => trip.id !== id);

    setSavedTrips(updatedTrips);

    localStorage.setItem(
      "tripgenius_saved_trips",
      JSON.stringify(updatedTrips),
    );
  }

  if (loading) {
    return (
      <main
        style={{
          minHeight: "80vh",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        Loading Saved Trips...
      </main>
    );
  }

  return (
    <main
      style={{
        maxWidth: "1400px",
        margin: "0 auto",
        padding: "40px 20px 80px",
      }}
    >
      {/* HEADER */}

      <section
        className="glass-card"
        style={{
          padding: "40px",
          marginBottom: "30px",
        }}
      >
        <h1
          className="hero-title"
          style={{
            fontSize: "3rem",
            marginBottom: "12px",
          }}
        >
          ❤️ Saved Trips
        </h1>

        <p
          style={{
            color: "#CBD5E1",
            lineHeight: 1.8,
          }}
        >
          Access all your saved travel plans in one place.
        </p>
      </section>

      {/* STATS */}

      <section
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit,minmax(220px,1fr))",
          gap: "20px",
          marginBottom: "30px",
        }}
      >
        <div className="stat-card">
          <h2>{savedTrips.length}</h2>
          <p>Saved Trips</p>
        </div>

        <div className="stat-card">
          <h2>
            ₹
            {savedTrips
              .reduce((total, trip) => total + trip.budget, 0)
              .toLocaleString()}
          </h2>
          <p>Total Budget</p>
        </div>

        <div className="stat-card">
          <h2>{new Set(savedTrips.map((trip) => trip.destination)).size}</h2>
          <p>Destinations</p>
        </div>
      </section>

      {/* EMPTY STATE */}

      {savedTrips.length === 0 && (
        <section
          className="glass-card"
          style={{
            padding: "60px",
            textAlign: "center",
          }}
        >
          <div
            style={{
              fontSize: "5rem",
              marginBottom: "20px",
            }}
          >
            ✈️
          </div>

          <h2
            style={{
              marginBottom: "15px",
            }}
          >
            No Saved Trips Yet
          </h2>

          <p
            style={{
              color: "#CBD5E1",
              marginBottom: "30px",
            }}
          >
            Create and save your first AI-generated travel plan.
          </p>

          <button
            onClick={() => router.push("/planner")}
            className="btn-primary"
            style={{
              border: "none",
              cursor: "pointer",
            }}
          >
            Create Trip
          </button>
        </section>
      )}

      {/* TRIPS GRID */}

      {savedTrips.length > 0 && (
        <section
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit,minmax(320px,1fr))",
            gap: "24px",
          }}
        >
          {savedTrips.map((trip) => (
            <div
              key={trip.id}
              className="glass-card"
              style={{
                padding: "24px",
              }}
            >
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  marginBottom: "20px",
                }}
              >
                <h2>📍 {trip.destination}</h2>
              </div>

              <div
                style={{
                  display: "grid",
                  gap: "10px",
                  color: "#CBD5E1",
                }}
              >
                <p>🗓️ {trip.duration_days} Days</p>

                <p>💰 ₹{trip.budget.toLocaleString()}</p>

                <p>🎒 {trip.travel_style}</p>

                <p>📅 {new Date(trip.created_at).toLocaleDateString()}</p>
              </div>

              <div
                style={{
                  display: "flex",
                  gap: "10px",
                  marginTop: "25px",
                }}
              >
                <button
                  onClick={() => router.push("/trip/generated")}
                  className="btn-primary"
                  style={{
                    flex: 1,
                    border: "none",
                    cursor: "pointer",
                  }}
                >
                  View
                </button>

                <button
                  onClick={() => deleteTrip(trip.id)}
                  style={{
                    flex: 1,
                    padding: "14px",
                    border: "none",
                    borderRadius: "999px",
                    cursor: "pointer",
                    background: "#DC2626",
                    color: "#ffffff",
                    fontWeight: 700,
                  }}
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </section>
      )}
    </main>
  );
}
