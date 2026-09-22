"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

interface TripHistoryItem {
  id?: string;
  trip_title?: string;
  destination?: string;
  duration_days?: number;
  budget?: number;
  sustainability_score?: number;
  status?: string;
  created_at?: string;
}

export default function HistoryPage() {
  const router = useRouter();

  const [trips, setTrips] = useState<TripHistoryItem[]>([]);

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadTrips();
  }, []);

  function loadTrips() {
    try {
      const savedTrips = localStorage.getItem("trip_history");

      if (savedTrips) {
        setTrips(JSON.parse(savedTrips));
      } else {
        setTrips([]);
      }
    } catch (error) {
      console.error(error);
      setTrips([]);
    } finally {
      setLoading(false);
    }
  }

  function deleteTrip(index: number) {
    const updatedTrips = [...trips];

    updatedTrips.splice(index, 1);

    setTrips(updatedTrips);

    localStorage.setItem("trip_history", JSON.stringify(updatedTrips));
  }

  function viewTrip(trip: TripHistoryItem) {
    localStorage.setItem("latest_trip", JSON.stringify(trip));

    router.push(`/trip/${trip.id ?? "generated"}`);
  }

  if (loading) {
    return (
      <div
        style={{
          padding: "40px",
        }}
      >
        Loading history...
      </div>
    );
  }

  return (
    <div
      style={{
        maxWidth: "1300px",
        margin: "0 auto",
        padding: "30px",
      }}
    >
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "30px",
        }}
      >
        <div>
          <h1
            style={{
              fontSize: "42px",
              marginBottom: "10px",
            }}
          >
            📜 Trip History
          </h1>

          <p
            style={{
              color: "#64748b",
            }}
          >
            View all your generated trips.
          </p>
        </div>

        <button
          onClick={() => router.push("/planner")}
          style={{
            background: "#2563eb",
            color: "#ffffff",
            border: "none",
            borderRadius: "10px",
            padding: "12px 20px",
          }}
        >
          New Trip
        </button>
      </div>

      {trips.length === 0 ? (
        <div
          style={{
            background: "#ffffff",
            padding: "40px",
            borderRadius: "15px",
            textAlign: "center",
            boxShadow: "0 2px 12px rgba(0,0,0,0.08)",
          }}
        >
          <h2>No Trips Found</h2>

          <p>Generate your first AI trip.</p>

          <button
            onClick={() => router.push("/planner")}
            style={{
              marginTop: "20px",
              background: "#16a34a",
              color: "#ffffff",
              border: "none",
              borderRadius: "10px",
              padding: "12px 20px",
            }}
          >
            Create Trip
          </button>
        </div>
      ) : (
        <div
          style={{
            display: "grid",
            gap: "20px",
          }}
        >
          {trips.map((trip, index) => (
            <div
              key={index}
              style={{
                background: "#ffffff",
                borderRadius: "15px",
                padding: "24px",
                boxShadow: "0 2px 12px rgba(0,0,0,0.08)",
              }}
            >
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  flexWrap: "wrap",
                  gap: "20px",
                }}
              >
                <div>
                  <h2>{trip.trip_title ?? "AI Trip"}</h2>

                  <p>📍 {trip.destination ?? "Unknown"}</p>

                  <p>⏳ {trip.duration_days ?? 0} Days</p>

                  <p>💰 ₹{trip.budget ?? 0}</p>

                  <p>🌱 Eco Score: {trip.sustainability_score ?? 0}</p>

                  <p>Status: {trip.status ?? "Generated"}</p>
                </div>

                <div
                  style={{
                    display: "flex",
                    flexDirection: "column",
                    gap: "10px",
                  }}
                >
                  <button
                    onClick={() => viewTrip(trip)}
                    style={{
                      background: "#2563eb",
                      color: "#ffffff",
                      border: "none",
                      borderRadius: "8px",
                      padding: "10px 18px",
                    }}
                  >
                    View
                  </button>

                  <button
                    onClick={() => deleteTrip(index)}
                    style={{
                      background: "#dc2626",
                      color: "#ffffff",
                      border: "none",
                      borderRadius: "8px",
                      padding: "10px 18px",
                    }}
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
