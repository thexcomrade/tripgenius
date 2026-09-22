"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

export default function TripDetailsPage() {
  const params = useParams();

  const [trip, setTrip] = useState<any>(null);

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    try {
      const storedTrip = localStorage.getItem("latest_trip");

      if (storedTrip) {
        setTrip(JSON.parse(storedTrip));
      }
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  }, []);

  if (loading) {
    return (
      <div
        style={{
          padding: "40px",
        }}
      >
        Loading trip...
      </div>
    );
  }

  if (!trip) {
    return (
      <div
        style={{
          padding: "40px",
        }}
      >
        No trip data found.
      </div>
    );
  }

  return (
    <div
      style={{
        maxWidth: "1400px",
        margin: "0 auto",
        padding: "30px",
      }}
    >
      <h1
        style={{
          fontSize: "42px",
          marginBottom: "10px",
        }}
      >
        {trip.trip_title ?? "AI Generated Trip"}
      </h1>

      <p
        style={{
          color: "#64748b",
          marginBottom: "30px",
        }}
      >
        Destination: {trip.destination}
      </p>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit,minmax(250px,1fr))",
          gap: "20px",
          marginBottom: "30px",
        }}
      >
        <div style={cardStyle}>
          <h3>🌱 Sustainability</h3>

          <h1>{trip.sustainability_score}</h1>
        </div>

        <div style={cardStyle}>
          <h3>🤖 AI Confidence</h3>

          <h1>{trip.ai_confidence_score}</h1>
        </div>

        <div style={cardStyle}>
          <h3>💰 Estimated Cost</h3>

          <h1>₹{trip.estimated_trip_cost}</h1>
        </div>
      </div>

      <section style={sectionStyle}>
        <h2>📝 Summary</h2>

        <p>{trip.itinerary_summary}</p>
      </section>

      <section style={sectionStyle}>
        <h2>☀️ Weather</h2>

        <pre>{JSON.stringify(trip.weather_summary, null, 2)}</pre>
      </section>

      <section style={sectionStyle}>
        <h2>🏞 Attractions</h2>

        <ul>
          {(trip.attractions ?? []).map((item: any, index: number) => (
            <li key={index}>{typeof item === "string" ? item : item.name}</li>
          ))}
        </ul>
      </section>

      <section style={sectionStyle}>
        <h2>🏨 Hotels</h2>

        <ul>
          {(trip.recommended_hotels ?? []).map((hotel: any, index: number) => (
            <li key={index}>
              {typeof hotel === "string" ? hotel : hotel.name}
            </li>
          ))}
        </ul>
      </section>

      <section style={sectionStyle}>
        <h2>🍽 Restaurants</h2>

        <ul>
          {(trip.recommended_restaurants ?? []).map(
            (restaurant: any, index: number) => (
              <li key={index}>
                {typeof restaurant === "string" ? restaurant : restaurant.name}
              </li>
            ),
          )}
        </ul>
      </section>

      <section style={sectionStyle}>
        <h2>🍛 Local Cuisine</h2>

        <ul>
          {(trip.local_cuisines ?? []).map((item: string, index: number) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
      </section>

      <section style={sectionStyle}>
        <h2>🎒 Packing Checklist</h2>

        <ul>
          {(trip.packing_checklist ?? []).map((item: string, index: number) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
      </section>

      <section style={sectionStyle}>
        <h2>💡 Travel Tips</h2>

        <ul>
          {(trip.travel_tips ?? []).map((item: string, index: number) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
      </section>

      <section style={sectionStyle}>
        <h2>📅 Day-wise Itinerary</h2>

        <pre>{JSON.stringify(trip.ai_itinerary, null, 2)}</pre>
      </section>
    </div>
  );
}

const cardStyle = {
  background: "#ffffff",
  padding: "20px",
  borderRadius: "12px",
  boxShadow: "0 2px 12px rgba(0,0,0,0.08)",
};

const sectionStyle = {
  background: "rgb(241, 80, 80)",
  padding: "24px",
  borderRadius: "12px",
  marginBottom: "20px",
  boxShadow: "0 2px 12px rgba(0,0,0,0.08)",
};
