from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import field_validator


# ============================================================
# Weather Schema
# ============================================================


class WeatherSummarySchema(BaseModel):
    temperature: float | None = None
    condition: str | None = None
    humidity: int | None = None
    wind_speed: float | None = None
    visibility: int | None = None
    recommendation: str | None = None


# ============================================================
# Hotel Schema
# ============================================================


class HotelRecommendationSchema(BaseModel):
    name: str
    category: str
    estimated_price: float
    rating: float | None = None
    location: str | None = None
    amenities: list[str] = Field(default_factory=list)


# ============================================================
# Restaurant Schema
# ============================================================


class RestaurantRecommendationSchema(BaseModel):
    name: str
    cuisine: str
    rating: float | None = None
    speciality: str | None = None


# ============================================================
# Attraction Schema
# ============================================================


class AttractionSchema(BaseModel):
    name: str
    description: str | None = None
    category: str | None = None
    estimated_duration_hours: float | None = None


# ============================================================
# Cost Breakdown
# ============================================================


class CostBreakdownSchema(BaseModel):
    accommodation_cost: float = 0.0
    transportation_cost: float = 0.0
    food_cost: float = 0.0
    miscellaneous_cost: float = 0.0
    total_cost: float = 0.0


# ============================================================
# Sustainability
# ============================================================


class SustainabilitySchema(BaseModel):
    sustainability_score: int = 0
    carbon_footprint_estimate: float = 0.0
    eco_friendly_recommendations: list[str] = Field(default_factory=list)


# ============================================================
# Day Itinerary
# ============================================================


class DayItinerarySchema(BaseModel):
    day: int

    title: str

    activities: list[str] = Field(default_factory=list)

    attractions: list[str] = Field(default_factory=list)

    meals: list[str] = Field(default_factory=list)

    accommodation: str | None = None

    transportation: str | None = None

    notes: str | None = None


# ============================================================
# AI Trip Generation Request
# ============================================================


class AITripGenerationRequest(BaseModel):
    destination: str = Field(min_length=2, max_length=200)

    duration_days: int = Field(ge=1, le=30)

    budget: float = Field(gt=0)

    travelers_count: int = Field(default=1, ge=1, le=500)

    travel_style: str | None = None

    interests: list[str] = Field(default_factory=list)

    transportation_mode: str | None = None

    preferred_accommodation: str | None = None

    @field_validator("destination")
    @classmethod
    def validate_destination(cls, value: str) -> str:

        value = value.strip()

        if len(value) < 2:
            raise ValueError("Destination must contain at least 2 characters.")

        return value


# ============================================================
# Trip Create Request
# ============================================================


class TripCreateRequest(BaseModel):
    trip_title: str = Field(min_length=2, max_length=200)

    destination: str = Field(min_length=2, max_length=200)

    duration_days: int = Field(ge=1, le=30)

    budget: float = Field(gt=0)

    travelers_count: int = Field(default=1, ge=1, le=500)

    travel_style: str | None = None

    interests: list[str] = Field(default_factory=list)

    transportation_mode: str | None = None

    preferred_accommodation: str | None = None


# ============================================================
# Trip Update Request
# ============================================================


class TripUpdateRequest(BaseModel):
    trip_title: str | None = None

    destination: str | None = None

    duration_days: int | None = Field(default=None, ge=1, le=30)

    budget: float | None = Field(default=None, gt=0)

    travelers_count: int | None = Field(default=None, ge=1, le=500)

    travel_style: str | None = None

    interests: list[str] | None = None

    transportation_mode: str | None = None

    preferred_accommodation: str | None = None

    status: str | None = None

    is_favorite: bool | None = None

    is_public: bool | None = None

    # ============================================================


# Trip Response
# ============================================================


class TripResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID | str

    user_id: str

    trip_title: str

    destination: str

    state: str | None = None

    district: str | None = None

    duration_days: int

    travelers_count: int

    budget: float

    travel_style: str | None = None

    interests: list[Any] = Field(default_factory=list)

    transportation_mode: str | None = None

    preferred_accommodation: str | None = None

    ai_itinerary: dict[str, Any] | list[Any] | None = None

    itinerary_summary: str | None = None

    attractions: list[Any] = Field(default_factory=list)

    recommended_hotels: list[Any] = Field(default_factory=list)

    recommended_restaurants: list[Any] = Field(default_factory=list)

    local_cuisines: list[str] = Field(default_factory=list)

    beverages_to_try: list[str] = Field(default_factory=list)

    weather_summary: dict[str, Any] = Field(default_factory=dict)

    weather_alerts: list[str] = Field(default_factory=list)

    packing_checklist: list[str] = Field(default_factory=list)

    travel_tips: list[str] = Field(default_factory=list)

    estimated_trip_cost: float = 0.0

    accommodation_cost: float = 0.0

    food_cost: float = 0.0

    transportation_cost: float = 0.0

    miscellaneous_cost: float = 0.0

    sustainability_score: int = 0

    carbon_footprint_estimate: float = 0.0

    eco_friendly_recommendations: list[str] = Field(default_factory=list)

    ai_confidence_score: float = 0.0

    is_favorite: bool = False

    is_public: bool = False

    status: str = "draft"

    generated_by_ai: bool = True

    generation_model: str | None = None

    created_at: datetime

    updated_at: datetime


# ============================================================
# Complete Trip Response
# ============================================================


class CompleteTripResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID | str

    user_id: str

    trip_title: str

    destination: str

    state: str | None = None

    district: str | None = None

    duration_days: int

    travelers_count: int

    budget: float

    travel_style: str | None = None

    interests: list[Any] = Field(default_factory=list)

    transportation_mode: str | None = None

    preferred_accommodation: str | None = None

    ai_itinerary: dict[str, Any] | list[Any] = Field(default_factory=dict)

    itinerary_summary: str | None = None

    attractions: list[Any] = Field(default_factory=list)

    recommended_hotels: list[Any] = Field(default_factory=list)

    recommended_restaurants: list[Any] = Field(default_factory=list)

    local_cuisines: list[str] = Field(default_factory=list)

    beverages_to_try: list[str] = Field(default_factory=list)

    weather_summary: dict[str, Any] = Field(default_factory=dict)

    weather_alerts: list[str] = Field(default_factory=list)

    packing_checklist: list[str] = Field(default_factory=list)

    travel_tips: list[str] = Field(default_factory=list)

    accommodation_cost: float = 0.0

    transportation_cost: float = 0.0

    food_cost: float = 0.0

    miscellaneous_cost: float = 0.0

    estimated_trip_cost: float = 0.0

    sustainability_score: int = 0

    carbon_footprint_estimate: float = 0.0

    eco_friendly_recommendations: list[str] = Field(default_factory=list)

    ai_confidence_score: float = 0.0

    is_favorite: bool = False

    is_public: bool = False

    status: str = "draft"

    generated_by_ai: bool = True

    generation_model: str | None = None

    created_at: datetime

    updated_at: datetime

    # ============================================================


# Trip History Response
# ============================================================


class TripHistoryItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID | str

    trip_title: str

    destination: str

    duration_days: int

    budget: float

    sustainability_score: int

    status: str

    created_at: datetime


class TripHistoryResponse(BaseModel):
    total_trips: int

    trips: list[TripHistoryItem] = Field(default_factory=list)


# ============================================================
# Trip Statistics Response
# ============================================================


class TripStatisticsResponse(BaseModel):
    total_trips: int = 0

    favorite_trips: int = 0

    average_budget: float = 0.0

    destinations: list[str] = Field(default_factory=list)


# ============================================================
# Destination Recommendation
# ============================================================


class DestinationRecommendationResponse(BaseModel):
    destination: str

    description: str

    activities: list[str] = Field(default_factory=list)

    suitability_score: float


# ============================================================
# Generic Message
# ============================================================


class MessageResponse(BaseModel):
    message: str


# ============================================================
# AI Trip Generation Response
# ============================================================


class AITripGenerationResponse(BaseModel):
    trip_title: str | None = None

    destination: str | None = None

    duration_days: int | None = None

    budget: float | None = None

    travelers_count: int | None = None

    travel_style: str | None = None

    transportation_mode: str | None = None

    preferred_accommodation: str | None = None

    interests: list[str] = Field(default_factory=list)

    destination_summary: str | None = None

    weather_summary: dict[str, Any] | None = None

    attractions: list[Any] = Field(default_factory=list)

    activities: list[str] = Field(default_factory=list)

    recommended_hotels: list[Any] = Field(default_factory=list)

    recommended_restaurants: list[Any] = Field(default_factory=list)

    local_cuisines: list[str] = Field(default_factory=list)

    beverages_to_try: list[str] = Field(default_factory=list)

    packing_checklist: list[str] = Field(default_factory=list)

    travel_tips: list[str] = Field(default_factory=list)

    ai_itinerary: list[dict[str, Any]] | None = None

    estimated_trip_cost: float | None = None

    accommodation_cost: float | None = None

    transportation_cost: float | None = None

    food_cost: float | None = None

    miscellaneous_cost: float | None = None

    cost_per_day: float | None = None

    cost_per_person_day: float | None = None

    sustainability_score: int | None = None

    carbon_footprint_estimate: float | None = None

    eco_friendly_recommendations: list[str] = Field(default_factory=list)

    ai_confidence_score: float | None = None

    gemini_response: dict[str, Any] | None = None

    generation_mode: str | None = None

    error: str | None = None
