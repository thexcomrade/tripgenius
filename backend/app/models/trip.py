from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import JSON
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

from app.database.db import Base


class Trip(Base):
    __tablename__ = "trips"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4()), index=True
    )

    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    trip_title: Mapped[str] = mapped_column(String(200), nullable=False)

    destination: Mapped[str] = mapped_column(String(200), nullable=False, index=True)

    state: Mapped[str | None] = mapped_column(String(100), nullable=True)

    district: Mapped[str | None] = mapped_column(String(100), nullable=True)

    duration_days: Mapped[int] = mapped_column(Integer, nullable=False)

    travelers_count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    budget: Mapped[float] = mapped_column(Float, nullable=False)

    travel_style: Mapped[str | None] = mapped_column(String(100), nullable=True)

    interests: Mapped[list] = mapped_column(JSON, default=list, nullable=False)

    transportation_mode: Mapped[str | None] = mapped_column(String(100), nullable=True)

    preferred_accommodation: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )

    ai_itinerary: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    itinerary_summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    attractions: Mapped[list] = mapped_column(JSON, default=list, nullable=False)

    recommended_hotels: Mapped[list] = mapped_column(JSON, default=list, nullable=False)

    recommended_restaurants: Mapped[list] = mapped_column(
        JSON, default=list, nullable=False
    )

    local_cuisines: Mapped[list] = mapped_column(JSON, default=list, nullable=False)

    beverages_to_try: Mapped[list] = mapped_column(JSON, default=list, nullable=False)

    weather_summary: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    weather_alerts: Mapped[list] = mapped_column(JSON, default=list, nullable=False)

    packing_checklist: Mapped[list] = mapped_column(JSON, default=list, nullable=False)

    travel_tips: Mapped[list] = mapped_column(JSON, default=list, nullable=False)

    estimated_trip_cost: Mapped[float] = mapped_column(
        Float, default=0.0, nullable=False
    )

    accommodation_cost: Mapped[float] = mapped_column(
        Float, default=0.0, nullable=False
    )

    food_cost: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    transportation_cost: Mapped[float] = mapped_column(
        Float, default=0.0, nullable=False
    )

    miscellaneous_cost: Mapped[float] = mapped_column(
        Float, default=0.0, nullable=False
    )

    sustainability_score: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False
    )

    carbon_footprint_estimate: Mapped[float] = mapped_column(
        Float, default=0.0, nullable=False
    )

    eco_friendly_recommendations: Mapped[list] = mapped_column(
        JSON, default=list, nullable=False
    )

    ai_confidence_score: Mapped[float] = mapped_column(
        Float, default=0.0, nullable=False
    )

    is_favorite: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    is_public: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    status: Mapped[str] = mapped_column(String(50), default="draft", nullable=False)

    generated_by_ai: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    generation_model: Mapped[str | None] = mapped_column(String(100), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return (
            f"Trip("
            f"id='{self.id}', "
            f"destination='{self.destination}', "
            f"duration_days={self.duration_days}, "
            f"budget={self.budget}"
            f")"
        )
