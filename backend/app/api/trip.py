from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Header
from fastapi import HTTPException
from fastapi import status

import logging

from sqlalchemy.orm import Session

from app.database.db import get_db

from app.core.security import get_token_subject

from app.models.trip import Trip

from app.models.user import User

from app.services.auth_service import AuthService

from app.services.trip_service import TripService

from app.services.ai_service import get_ai_service

from app.schemas.trip_schema import (
    TripCreateRequest,
    TripUpdateRequest,
    TripResponse,
    TripHistoryItem,
    TripHistoryResponse,
    TripStatisticsResponse,
    AITripGenerationRequest,
    AITripGenerationResponse,
)


router = APIRouter(prefix="/api/trips", tags=["Trips"])


# =====================================================
# Dependencies
# =====================================================


def get_trip_service(db: Session = Depends(get_db)) -> TripService:

    return TripService(db)


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:

    return AuthService(db)


def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
    auth_service: AuthService = Depends(get_auth_service),
) -> User:

    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header",
        )

    token = authorization.replace("Bearer ", "")

    try:
        user_id = get_token_subject(token)

        user = auth_service.get_user_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
            )

        return user

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


# =====================================================
# Helpers
# =====================================================


def serialize_trip(trip: Trip) -> dict:

    return {
        "id": trip.id,
        "user_id": trip.user_id,
        "trip_title": trip.trip_title,
        "destination": trip.destination,
        "state": trip.state,
        "district": trip.district,
        "duration_days": trip.duration_days,
        "travelers_count": trip.travelers_count,
        "budget": trip.budget,
        "travel_style": trip.travel_style,
        "interests": trip.interests,
        "transportation_mode": trip.transportation_mode,
        "preferred_accommodation": trip.preferred_accommodation,
        "ai_itinerary": trip.ai_itinerary,
        "itinerary_summary": trip.itinerary_summary,
        "attractions": trip.attractions,
        "recommended_hotels": trip.recommended_hotels,
        "recommended_restaurants": trip.recommended_restaurants,
        "local_cuisines": trip.local_cuisines,
        "beverages_to_try": trip.beverages_to_try,
        "weather_summary": trip.weather_summary,
        "weather_alerts": trip.weather_alerts,
        "packing_checklist": trip.packing_checklist,
        "travel_tips": trip.travel_tips,
        "estimated_trip_cost": trip.estimated_trip_cost,
        "accommodation_cost": trip.accommodation_cost,
        "food_cost": trip.food_cost,
        "transportation_cost": trip.transportation_cost,
        "miscellaneous_cost": trip.miscellaneous_cost,
        "sustainability_score": trip.sustainability_score,
        "carbon_footprint_estimate": trip.carbon_footprint_estimate,
        "eco_friendly_recommendations": trip.eco_friendly_recommendations,
        "ai_confidence_score": trip.ai_confidence_score,
        "is_favorite": trip.is_favorite,
        "is_public": trip.is_public,
        "status": trip.status,
        "generated_by_ai": trip.generated_by_ai,
        "generation_model": trip.generation_model,
        "created_at": trip.created_at,
        "updated_at": trip.updated_at,
    }


# =====================================================
# AI Itinerary Generation
# =====================================================


@router.post("/generate-ai-itinerary", response_model=AITripGenerationResponse)
def generate_ai_itinerary(
    payload: AITripGenerationRequest, current_user: User = Depends(get_current_user)
):
    logger = logging.getLogger(__name__)
    logger.info(
        "AI itinerary request: user=%s destination=%s",
        current_user.id,
        payload.destination,
    )

    try:
        ai_service = get_ai_service()

        result = ai_service.generate_trip_plan(
            destination=payload.destination,
            duration_days=payload.duration_days,
            budget=payload.budget,
            interests=payload.interests,
            travelers_count=payload.travelers_count,
            travel_style=payload.travel_style,
            transportation_mode=payload.transportation_mode,
            preferred_accommodation=payload.preferred_accommodation,
        )

        result["destination"] = payload.destination
        result["duration_days"] = payload.duration_days
        result["budget"] = payload.budget
        result["travelers_count"] = payload.travelers_count
        result["travel_style"] = payload.travel_style
        result["transportation_mode"] = payload.transportation_mode
        result["preferred_accommodation"] = payload.preferred_accommodation
        result["interests"] = payload.interests

        logger.info(
            "AI generation complete for %s — mode=%s confidence=%s",
            payload.destination,
            result.get("generation_mode", "live"),
            result.get("ai_confidence_score", "N/A"),
        )

        return AITripGenerationResponse(**result)

    except HTTPException:
        raise

    except Exception as exc:
        logger.exception("generate_ai_itinerary failed: %s", str(exc))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI itinerary generation failed: {str(exc)}",
        )


# =====================================================
# Create Trip
# =====================================================


@router.post(
    "/create", response_model=TripResponse, status_code=status.HTTP_201_CREATED
)
def create_trip(
    payload: TripCreateRequest,
    current_user: User = Depends(get_current_user),
    trip_service: TripService = Depends(get_trip_service),
    auth_service: AuthService = Depends(get_auth_service),
):

    trip_data = payload.model_dump()

    trip_data["user_id"] = current_user.id

    trip = trip_service.create_trip(trip_data)

    auth_service.increment_trip_count(current_user.id)

    return TripResponse(**serialize_trip(trip))


# =====================================================
# Trip History  (must be before /{trip_id} GET)
# =====================================================


@router.get("/history/list", response_model=TripHistoryResponse)
def trip_history(
    current_user: User = Depends(get_current_user),
    trip_service: TripService = Depends(get_trip_service),
):

    trips = trip_service.get_trip_history(current_user.id)

    return TripHistoryResponse(
        total_trips=len(trips),
        trips=[
            TripHistoryItem(
                id=trip.id,
                trip_title=trip.trip_title,
                destination=trip.destination,
                duration_days=trip.duration_days,
                budget=trip.budget,
                sustainability_score=trip.sustainability_score or 0,
                status=trip.status or "draft",
                created_at=trip.created_at,
            )
            for trip in trips
        ],
    )


# =====================================================
# Statistics  (must be before /{trip_id} GET)
# =====================================================


@router.get("/statistics/summary", response_model=TripStatisticsResponse)
def trip_statistics(
    current_user: User = Depends(get_current_user),
    trip_service: TripService = Depends(get_trip_service),
):

    stats = trip_service.get_trip_statistics(current_user.id)

    return TripStatisticsResponse(**stats)


# =====================================================
# Get Trip  (parameterized — must be AFTER specific paths)
# =====================================================


@router.get("/{trip_id}", response_model=TripResponse)
def get_trip(
    trip_id: str,
    current_user: User = Depends(get_current_user),
    trip_service: TripService = Depends(get_trip_service),
):

    trip = trip_service.get_trip_by_id(trip_id)

    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    if trip.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    return TripResponse(**serialize_trip(trip))


# =====================================================
# Update Trip
# =====================================================


@router.put("/{trip_id}", response_model=TripResponse)
def update_trip(
    trip_id: str,
    payload: TripUpdateRequest,
    current_user: User = Depends(get_current_user),
    trip_service: TripService = Depends(get_trip_service),
):

    existing_trip = trip_service.get_trip_by_id(trip_id)

    if not existing_trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    if existing_trip.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    trip = trip_service.update_trip(trip_id, payload.model_dump(exclude_unset=True))

    return TripResponse(**serialize_trip(trip))


# =====================================================
# Delete Trip
# =====================================================


@router.delete("/{trip_id}")
def delete_trip(
    trip_id: str,
    current_user: User = Depends(get_current_user),
    trip_service: TripService = Depends(get_trip_service),
):

    trip = trip_service.get_trip_by_id(trip_id)

    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    if trip.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    trip_service.delete_trip(trip_id)

    return {"message": "Trip deleted successfully"}


# =====================================================
# Favorite Trip
# =====================================================


@router.post("/{trip_id}/favorite")
def favorite_trip(
    trip_id: str,
    current_user: User = Depends(get_current_user),
    trip_service: TripService = Depends(get_trip_service),
):

    trip = trip_service.get_trip_by_id(trip_id)

    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    if trip.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    trip_service.favorite_trip(trip_id)

    return {"message": "Trip added to favorites"}


# =====================================================
# Unfavorite Trip
# =====================================================


@router.post("/{trip_id}/unfavorite")
def unfavorite_trip(
    trip_id: str,
    current_user: User = Depends(get_current_user),
    trip_service: TripService = Depends(get_trip_service),
):

    trip = trip_service.get_trip_by_id(trip_id)

    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    if trip.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    trip_service.unfavorite_trip(trip_id)

    return {"message": "Trip removed from favorites"}
