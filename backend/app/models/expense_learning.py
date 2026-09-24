"""
TripGenius — Trip Expense Learning Model for Adaptive Reinforcement Learning.

Persists empirical traveler expenditures (chelavakkiya budget) alongside
AI predictions to fuel contextual bandit / RL calibration.
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import JSON
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

from app.database.db import Base


class TripExpenseLearning(Base):
    __tablename__ = "trip_expense_learnings"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4()), index=True
    )

    trip_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("trips.id", ondelete="CASCADE"), nullable=False, index=True
    )

    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    destination: Mapped[str] = mapped_column(String(100), nullable=False, index=True)

    travel_style: Mapped[str] = mapped_column(String(100), default="leisure", index=True)

    transportation_mode: Mapped[str | None] = mapped_column(String(100), nullable=True)

    duration_days: Mapped[int] = mapped_column(Integer, nullable=False)

    travelers_count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    # Budget comparison
    ai_estimated_total: Mapped[float] = mapped_column(Float, nullable=False)

    actual_spent_total: Mapped[float] = mapped_column(Float, nullable=False)

    variance_amount: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    variance_ratio: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)

    reward_score: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)

    # Itemized actuals
    category_actuals: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    # Contextual Multiplier after this update step
    learned_multiplier_after: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)

    user_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
