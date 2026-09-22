from uuid import uuid4

from sqlalchemy.orm import Session

from app.models.trip import Trip

from app.services.weather_service import WeatherService

from app.services.recommendation_service import RecommendationService


class TripService:
    def __init__(self, db: Session) -> None:

        self.db = db

        self.weather_service = WeatherService()

        self.recommendation_service = RecommendationService()

    def create_trip(self, trip_data: dict) -> Trip:

        trip = Trip(id=str(uuid4()), **trip_data)

        self.db.add(trip)

        self.db.commit()

        self.db.refresh(trip)

        return trip

    def get_trip_by_id(self, trip_id: str) -> Trip | None:

        return self.db.query(Trip).filter(Trip.id == trip_id).first()

    def get_user_trips(self, user_id: str) -> list[Trip]:

        return (
            self.db.query(Trip)
            .filter(Trip.user_id == user_id)
            .order_by(Trip.created_at.desc())
            .all()
        )

    def update_trip(self, trip_id: str, update_data: dict) -> Trip:

        trip = self.get_trip_by_id(trip_id)

        if not trip:
            raise ValueError("Trip not found")

        for key, value in update_data.items():
            if hasattr(trip, key):
                setattr(trip, key, value)

        self.db.commit()

        self.db.refresh(trip)

        return trip

    def delete_trip(self, trip_id: str) -> bool:

        trip = self.get_trip_by_id(trip_id)

        if not trip:
            raise ValueError("Trip not found")

        self.db.delete(trip)

        self.db.commit()

        return True

    def favorite_trip(self, trip_id: str) -> Trip:

        trip = self.get_trip_by_id(trip_id)

        if not trip:
            raise ValueError("Trip not found")

        trip.is_favorite = True

        self.db.commit()

        self.db.refresh(trip)

        return trip

    def unfavorite_trip(self, trip_id: str) -> Trip:

        trip = self.get_trip_by_id(trip_id)

        if not trip:
            raise ValueError("Trip not found")

        trip.is_favorite = False

        self.db.commit()

        self.db.refresh(trip)

        return trip

    def get_trip_history(self, user_id: str) -> list[Trip]:

        return self.get_user_trips(user_id)

    def save_generated_itinerary(self, trip_id: str, itinerary: dict) -> Trip:

        trip = self.get_trip_by_id(trip_id)

        if not trip:
            raise ValueError("Trip not found")

        trip.ai_itinerary = itinerary

        self.db.commit()

        self.db.refresh(trip)

        return trip

    def generate_trip_context(
        self, destination: str, interests: list[str], budget: float
    ) -> dict:

        weather = self.weather_service.get_weather_summary(destination)

        recommendations = self.recommendation_service.recommend_by_interest(interests)

        budget_plan = self.recommendation_service.recommend_by_budget(budget)

        return {
            "destination": destination,
            "weather": weather,
            "recommendations": recommendations,
            "budget": budget_plan,
        }

    def get_trip_statistics(self, user_id: str) -> dict:

        trips = self.get_user_trips(user_id)

        total_trips = len(trips)

        favorites = len([trip for trip in trips if trip.is_favorite])

        total_budget = sum(trip.budget for trip in trips)

        average_budget = 0

        if total_trips > 0:
            average_budget = total_budget / total_trips

        destinations = list({trip.destination for trip in trips})

        return {
            "total_trips": total_trips,
            "favorite_trips": favorites,
            "average_budget": round(average_budget, 2),
            "destinations": destinations,
        }

    def get_favorite_trips(self, user_id: str) -> list[Trip]:

        return (
            self.db.query(Trip)
            .filter(Trip.user_id == user_id, Trip.is_favorite == True)
            .all()
        )
