from __future__ import annotations

import json
import logging
import re
import time
from functools import lru_cache
from typing import Any

from google import genai

from app.core.config import settings

from app.services.weather_service import WeatherService

from app.services.recommendation_service import RecommendationService


logger = logging.getLogger(__name__)


class AIService:
    """
    ==================================================
    TripGenius AI Engine
    ==================================================

    Responsibilities

    ✓ Gemini Initialization
    ✓ Prompt Templates
    ✓ Destination Summary Generator
    ✓ Weather Integration
    ✓ Recommendation Integration
    ✓ Attraction Generator
    ✓ Activity Generator
    ✓ Hotel Generator
    ✓ Restaurant Generator
    ✓ Cuisine Generator
    ✓ Beverage Generator
    ✓ Packing Generator
    ✓ Travel Tips Generator
    ✓ Cost Estimator
    ✓ Sustainability Scoring
    ✓ Carbon Footprint Estimator
    ✓ Eco Recommendation Generator
    ✓ AI Confidence Scoring
    ✓ Day Wise Itinerary Generator
    ✓ Response Validation
    ✓ Retry Logic
    ✓ Offline Fallback
    ✓ Cache Layer
    ✓ JSON Formatter
    """

    MAX_RETRIES = 3

    def __init__(self) -> None:

        self.weather_service = WeatherService()

        self.recommendation_service = RecommendationService()

        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

        self.model_name = "gemini-2.5-flash"

    # ==================================================
    # Prompt Templates
    # ==================================================

    def _build_master_prompt(
        self,
        destination: str,
        duration_days: int,
        budget: float,
        interests: list[str],
        travelers_count: int = 1,
        travel_style: str | None = None,
        transportation_mode: str | None = None,
        preferred_accommodation: str | None = None,
        cost_data: dict[str, float] | None = None,
    ) -> str:
        cost = cost_data or self.estimate_trip_cost(
            budget, duration_days, travelers_count, travel_style
        )
        acc_per_night = round(
            cost["accommodation_cost"] / max(1, duration_days - 1), 2
        )
        food_per_day = round(cost["food_cost"] / max(1, duration_days), 2)

        interests_str = (
            ", ".join(interests)
            if interests
            else "Sightseeing, Local Culture, Scenic Views"
        )

        return f"""You are TripGenius AI, an elite travel architect and regional specialist.
Create an inspiring, highly realistic, and budget-tailored travel plan.

DESTINATION & TRAVEL DETAILS:
- Destination: {destination}
- Duration: {duration_days} Days ({max(1, duration_days - 1)} Nights)
- Travelers: {travelers_count} Traveler(s)
- Travel Style: {travel_style or "Leisure"}
- Transit Mode: {transportation_mode or "Private Car / Taxi"}
- Preferred Stay: {preferred_accommodation or "Comfort Hotel"}
- Traveler Interests: {interests_str}

FINANCIAL BUDGET ARCHITECTURE (TOTAL BUDGET: ₹{budget:,.0f}):
- Daily Total Allowance: ~₹{cost['cost_per_day']:,.0f} / day for all {travelers_count} travelers (~₹{cost['cost_per_person_day']:,.0f} / person / day)
- Stays & Lodging Budget: ₹{cost['accommodation_cost']:,.0f} total (~₹{acc_per_night:,.0f} / night for room)
- Food & Dining Budget: ₹{cost['food_cost']:,.0f} total (~₹{food_per_day:,.0f} / day for {travelers_count} people)
- Transit & Sightseeing: ₹{cost['transportation_cost']:,.0f} total
- Activities & Miscellaneous: ₹{cost['miscellaneous_cost']:,.0f} total

BUDGET-ALIGNED SYNTHESIS RULES:
1. Every day in 'ai_itinerary' MUST contain specific, realistic morning, afternoon, and evening activities in {destination} that fit this exact budget tier.
2. In 'recommended_hotels', provide 3 specific real/realistic hotel or homestay names in {destination} that strictly match ~₹{acc_per_night:,.0f}/night.
3. In 'recommended_restaurants', suggest authentic dining spots in {destination} fitting the ~₹{food_per_day:,.0f}/day food budget.
4. Include authentic local attractions, scenic viewpoints, eco-friendly tips, and regional culinary dishes.

Return valid JSON ONLY matching this exact schema:
{{
  "trip_title": "{destination} Travel Experience",
  "destination_summary": "Detailed, evocative 2-3 sentence overview of {destination}",
  "ai_itinerary": [
    {{
      "day": 1,
      "title": "Arrival & Initial Highlights",
      "destination": "{destination}",
      "morning": "Detailed morning plan, check-in, viewpoint",
      "afternoon": "Detailed afternoon activity and lunch suggestion",
      "evening": "Detailed sunset or evening walk, dinner spot",
      "activities": ["Activity 1", "Activity 2"]
    }}
  ],
  "attractions": ["Attraction 1", "Attraction 2", "Attraction 3", "Attraction 4"],
  "activities": ["Activity 1", "Activity 2", "Activity 3"],
  "recommended_hotels": ["Hotel 1", "Hotel 2", "Hotel 3"],
  "recommended_restaurants": ["Restaurant 1", "Restaurant 2", "Restaurant 3"],
  "local_cuisines": ["Dish 1", "Dish 2", "Dish 3"],
  "beverages_to_try": ["Beverage 1", "Beverage 2"],
  "packing_checklist": ["Item 1", "Item 2", "Item 3", "Item 4"],
  "travel_tips": ["Tip 1", "Tip 2", "Tip 3"],
  "eco_friendly_recommendations": ["Eco tip 1", "Eco tip 2"]
}}"""

    def _build_itinerary_prompt(
        self, destination: str, duration_days: int, interests: list[str]
    ) -> str:

        return f"""
Create a detailed day-wise itinerary.

Destination:
{destination}

Duration:
{duration_days}

Interests:
{", ".join(interests)}

Return JSON.
"""

    def _build_hotel_prompt(self, destination: str, budget: float) -> str:

        return f"""
Recommend hotels for:

Destination:
{destination}

Budget:
₹{budget}

Return list only.
"""

    def _build_food_prompt(self, destination: str) -> str:

        return f"""
Recommend local cuisines,
restaurants and beverages.

Destination:
{destination}

Return JSON.
"""

    # ==================================================
    # Gemini Communication Layer
    # ==================================================

    def _generate_content(self, prompt: str) -> str:

        last_error = None

        for attempt in range(self.MAX_RETRIES):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name, contents=prompt
                )

                if response and response.text:
                    return response.text

            except Exception as error:
                last_error = error

                logger.warning(
                    ("Gemini attempt %s failed: %s"), attempt + 1, str(error)
                )

                time.sleep(2)

        raise RuntimeError(f"Gemini generation failed: {last_error}")

    # ==================================================
    # JSON Parsing Utilities
    # ==================================================

    def _safe_json_parse(self, content: str) -> dict[str, Any]:
        """
        Robustly extracts JSON dictionary from raw model text output,
        handling direct JSON, markdown code fences, and embedded substrings.
        """
        if not content or not isinstance(content, str):
            return {}

        raw = content.strip()

        # Strategy 1: Direct JSON parsing
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            pass

        # Strategy 2: Markdown code fence ```json ... ``` or ``` ... ```
        fence_pattern = r"```(?:json)?\s*([\s\S]*?)\s*```"
        matches = re.findall(fence_pattern, raw, re.IGNORECASE)
        for candidate in matches:
            try:
                parsed = json.loads(candidate.strip())
                if isinstance(parsed, dict):
                    return parsed
            except Exception:
                continue

        # Strategy 3: Substring between first '{' and last '}'
        start = raw.find("{")
        end = raw.rfind("}")
        if start != -1 and end != -1 and end > start:
            snippet = raw[start : end + 1]
            try:
                parsed = json.loads(snippet)
                if isinstance(parsed, dict):
                    return parsed
            except Exception:
                pass

        return {}

    # ==================================================
    # Cache Layer
    # ==================================================

    @lru_cache(maxsize=100)
    def _cached_destination_profile(self, destination: str) -> dict[str, Any] | None:

        return self.recommendation_service.generate_destination_profile(destination)

    # ==================================================
    # Weather Integration
    # ==================================================

    def get_weather_context(self, destination: str) -> dict[str, Any]:

        try:
            return self.weather_service.get_current_weather(destination)

        except Exception as error:
            logger.warning("Weather fetch failed: %s", str(error))

            return {
                "city": destination,
                "temperature": 0,
                "condition": "Unknown",
                "humidity": 0,
                "travel_recommendation": "Weather data unavailable.",
                "packing_suggestions": [],
            }

    # ==================================================
    # Recommendation Integration
    # ==================================================

    def get_recommendation_context(
        self, destination: str, interests: list[str], budget: float
    ) -> dict[str, Any]:

        recommendations = self.recommendation_service.recommend_by_interest(interests)

        budget_plan = self.recommendation_service.recommend_by_budget(budget)

        destination_profile = self._cached_destination_profile(destination)

        return {
            "destination_profile": destination_profile,
            "recommendations": recommendations,
            "budget_plan": budget_plan,
        }

    # ==================================================
    # Destination Summary Generator
    # ==================================================

    def generate_destination_summary(self, destination: str) -> str:

        profile = self._cached_destination_profile(destination)

        if profile:
            return profile.get("description", "")

        return (
            f"{destination} is a wonderful "
            f"travel destination offering "
            f"culture, attractions and "
            f"memorable experiences."
        )

    # ==================================================
    # Attraction Generator
    # ==================================================

    def generate_attractions(self, destination: str, interests: list[str]) -> list[str]:

        recommendations = self.recommendation_service.recommend_by_interest(interests)

        attractions: list[str] = []

        for item in recommendations[:10]:
            place_name = item.get("place_name", "")

            if place_name and place_name not in attractions:
                attractions.append(place_name)

        if attractions:
            return attractions

        return [
            f"{destination} Town Center",
            f"{destination} View Point",
            f"{destination} Cultural Area",
        ]

    # ==================================================
    # Activity Generator
    # ==================================================

    def generate_activities(self, interests: list[str]) -> list[str]:

        activity_map = {
            "nature": ["Nature Walk", "Forest Exploration", "Wildlife Observation"],
            "trekking": ["Mountain Trekking", "Hill Hiking", "Adventure Trails"],
            "photography": [
                "Sunrise Photography",
                "Landscape Photography",
                "Street Photography",
            ],
            "food": ["Food Tour", "Local Cuisine Experience"],
            "culture": ["Temple Visits", "Museum Tours", "Cultural Shows"],
            "adventure": ["Zipline", "Camping", "Rock Climbing"],
        }

        activities: list[str] = []

        for interest in interests:
            matched = activity_map.get(interest.lower(), [])

            activities.extend(matched)

        if not activities:
            activities = ["Sightseeing", "Local Exploration", "Photography"]

        return list(dict.fromkeys(activities))

    # ==================================================
    # Hotel Generator
    # ==================================================

    def generate_hotels(self, destination: str, budget: float) -> list[str]:

        if budget <= 10000:
            return [
                f"{destination} Budget Inn",
                f"{destination} Backpackers Hostel",
                f"{destination} Guest House",
            ]

        if budget <= 30000:
            return [
                f"{destination} Eco Residency",
                f"{destination} Nature Resort",
                f"{destination} Comfort Stay",
            ]

        if budget <= 60000:
            return [
                f"{destination} Premium Resort",
                f"{destination} Hill View Resort",
                f"{destination} Boutique Hotel",
            ]

        return [
            f"{destination} Luxury Resort",
            f"{destination} Grand Palace Hotel",
            f"{destination} Five Star Retreat",
        ]

    # ==================================================
    # Restaurant Generator
    # ==================================================

    def generate_restaurants(self, destination: str) -> list[str]:

        return [
            f"{destination} Spice Garden",
            f"{destination} Traditional Kitchen",
            f"{destination} Family Restaurant",
            f"{destination} Food Court",
            f"{destination} Heritage Dining",
        ]

    # ==================================================
    # Cuisine Generator
    # ==================================================

    def generate_local_cuisines(self, destination: str) -> list[str]:

        destination_lower = destination.lower()

        if "munnar" in destination_lower or "kerala" in destination_lower:
            return [
                "Appam",
                "Puttu",
                "Kerala Sadya",
                "Malabar Biryani",
                "Karimeen Pollichathu",
            ]

        if "coorg" in destination_lower or "kodagu" in destination_lower:
            return ["Pandi Curry", "Kadambuttu", "Akki Roti", "Bamboo Shoot Curry"]

        return [
            "Regional Cuisine",
            "Traditional Meals",
            "Street Food",
            "Local Specialities",
        ]

    # ==================================================
    # Beverage Generator
    # ==================================================

    def generate_beverages(self, destination: str) -> list[str]:

        destination_lower = destination.lower()

        if "munnar" in destination_lower:
            return ["Fresh Tea", "Cardamom Tea", "Lemon Tea", "Herbal Tea"]

        return ["Fresh Juice", "Local Tea", "Traditional Drinks"]

    # ==================================================
    # Packing Checklist Generator
    # ==================================================

    def generate_packing_checklist(self, destination: str) -> list[str]:

        weather = self.get_weather_context(destination)

        checklist = [
            "Government ID",
            "Mobile Charger",
            "Power Bank",
            "Water Bottle",
            "Personal Medicines",
            "Cash",
            "Travel Documents",
        ]

        checklist.extend(weather.get("packing_suggestions", []))

        return list(dict.fromkeys(checklist))

    # ==================================================
    # Travel Tips Generator
    # ==================================================

    def generate_travel_tips(self, destination: str) -> list[str]:

        return [
            "Book accommodations early.",
            "Carry valid identification.",
            "Respect local culture.",
            "Keep emergency contacts handy.",
            "Use reusable water bottles.",
            "Avoid littering.",
            "Check weather forecasts daily.",
            "Keep digital copies of documents.",
        ]

    # ==================================================
    # Cost Estimator
    # ==================================================

    def estimate_trip_cost(
        self,
        budget: float,
        duration_days: int,
        travelers_count: int = 1,
        travel_style: str | None = None,
        transportation_mode: str | None = None,
        preferred_accommodation: str | None = None,
    ) -> dict[str, float]:
        """
        Calibrate realistic, human-scale financial breakdown for regional and domestic travel.
        The user's budget represents the TOTAL budget for the trip. It is NEVER multiplied
        by travelers_count. Costs are allocated realistically by travel style and duration.
        """
        duration = max(1, duration_days)
        travelers = max(1, travelers_count)
        total_budget = round(float(budget), 2)

        # Style-aware realistic cost distribution
        style = (travel_style or "").lower()
        if "romantic" in style:
            # Romantic prioritizes intimate boutique stays & culinary dinners
            acc_pct, food_pct, trans_pct, misc_pct = 0.42, 0.25, 0.18, 0.15
        elif "adventure" in style or "eco" in style:
            # Eco / Adventure prioritizes trails, activities, guides
            acc_pct, food_pct, trans_pct, misc_pct = 0.35, 0.22, 0.23, 0.20
        elif "family" in style:
            # Family prioritizes comfortable transport and food
            acc_pct, food_pct, trans_pct, misc_pct = 0.38, 0.26, 0.22, 0.14
        else:  # Leisure, Cultural, General
            acc_pct, food_pct, trans_pct, misc_pct = 0.40, 0.24, 0.21, 0.15

        accommodation_cost = round(total_budget * acc_pct, 2)
        food_cost = round(total_budget * food_pct, 2)
        transportation_cost = round(total_budget * trans_pct, 2)
        # Ensure exact sum matching total_budget
        miscellaneous_cost = round(
            total_budget - (accommodation_cost + food_cost + transportation_cost), 2
        )

        cost_per_day = round(total_budget / duration, 2)
        cost_per_person_day = round(total_budget / (duration * travelers), 2)

        return {
            "estimated_trip_cost": total_budget,
            "accommodation_cost": accommodation_cost,
            "food_cost": food_cost,
            "transportation_cost": transportation_cost,
            "miscellaneous_cost": miscellaneous_cost,
            "cost_per_day": cost_per_day,
            "cost_per_person_day": cost_per_person_day,
        }

    # ==================================================
    # Sustainability Score Engine
    # ==================================================

    def calculate_sustainability_score(
        self, interests: list[str], transportation_mode: str | None = None
    ) -> int:

        score = 50

        eco_interests = {"nature", "eco", "wildlife", "trekking", "photography"}

        for interest in interests:
            if interest.lower() in eco_interests:
                score += 5

        if transportation_mode:
            transport = transportation_mode.lower()

            if transport in ["walking", "cycling"]:
                score += 20

            elif transport in ["train", "bus"]:
                score += 10

            elif transport in ["car"]:
                score += 5

            elif transport in ["flight", "air"]:
                score -= 10

        return max(0, min(score, 100))

    # ==================================================
    # Carbon Footprint Estimator
    # ==================================================

    def estimate_carbon_footprint(
        self, duration_days: int, transportation_mode: str | None
    ) -> float:

        transport_factor = {
            "walking": 1.0,
            "cycling": 1.5,
            "bus": 3.0,
            "train": 4.0,
            "car": 8.0,
            "flight": 25.0,
            "air": 25.0,
        }

        factor = transport_factor.get((transportation_mode or "car").lower(), 8.0)

        footprint = factor * duration_days

        return round(footprint, 2)

    # ==================================================
    # Eco Friendly Recommendation Generator
    # ==================================================

    def generate_eco_recommendations(self) -> list[str]:

        return [
            "Carry a reusable water bottle.",
            "Avoid single-use plastics.",
            "Use public transportation whenever possible.",
            "Support local businesses and guides.",
            "Follow Leave No Trace principles.",
            "Respect wildlife and natural habitats.",
            "Use eco-friendly accommodations.",
            "Reduce food waste during travel.",
        ]

    # ==================================================
    # AI Confidence Calculator
    # ==================================================

    def calculate_ai_confidence(
        self,
        weather_available: bool,
        recommendations_count: int,
        destination_profile_found: bool,
    ) -> float:

        confidence = 60.0

        if weather_available:
            confidence += 15.0

        if recommendations_count >= 5:
            confidence += 15.0

        elif recommendations_count >= 2:
            confidence += 10.0

        if destination_profile_found:
            confidence += 10.0

        return round(min(confidence, 100.0), 2)

    # ==================================================
    # Day Wise Itinerary Generator
    # ==================================================

    def generate_day_wise_itinerary(
        self, destination: str, duration_days: int, interests: list[str]
    ) -> list[dict[str, Any]]:

        activities = self.generate_activities(interests)

        itinerary = []

        activity_index = 0

        for day in range(1, duration_days + 1):
            day_plan = {
                "day": day,
                "title": f"Day {day}",
                "destination": destination,
                "morning": "",
                "afternoon": "",
                "evening": "",
            }

            if day == 1:
                day_plan["title"] = "Arrival & Exploration"

                day_plan["morning"] = "Arrival and hotel check-in"

                day_plan["afternoon"] = "Local sightseeing"

                day_plan["evening"] = "Relax and explore local markets"

            elif day == duration_days:
                day_plan["title"] = "Departure Day"

                day_plan["morning"] = "Breakfast and souvenir shopping"

                day_plan["afternoon"] = "Visit nearby attraction"

                day_plan["evening"] = "Departure"

            else:
                morning_activity = activities[activity_index % len(activities)]

                afternoon_activity = activities[(activity_index + 1) % len(activities)]

                evening_activity = activities[(activity_index + 2) % len(activities)]

                day_plan["morning"] = morning_activity

                day_plan["afternoon"] = afternoon_activity

                day_plan["evening"] = evening_activity

                activity_index += 3

            itinerary.append(day_plan)

        return itinerary

    # ==================================================
    # Gemini Response Parser
    # ==================================================

    def parse_gemini_response(self, response_text: str) -> dict[str, Any]:

        parsed = self._safe_json_parse(response_text)

        if parsed:
            return parsed

        return {"raw_response": response_text}

    # ==================================================
    # Offline Fallback Generator
    # ==================================================

    def generate_offline_trip_plan(
        self,
        destination: str,
        duration_days: int,
        budget: float,
        interests: list[str],
        travelers_count: int = 1,
        travel_style: str | None = None,
        transportation_mode: str | None = None,
        preferred_accommodation: str | None = None,
    ) -> dict[str, Any]:
        """
        Full-fidelity structured fallback plan when external AI services are unavailable.
        Uses deterministic local domain datasets, weather heuristics, and financial pacing.
        """
        response = self.build_complete_response(
            destination=destination,
            duration_days=duration_days,
            budget=budget,
            travelers_count=travelers_count,
            interests=interests,
            travel_style=travel_style,
            transportation_mode=transportation_mode,
            preferred_accommodation=preferred_accommodation,
        )
        response["generation_mode"] = "curated_offline"
        return response

    # ==================================================
    # Validation Methods
    # ==================================================

    def validate_trip_input(
        self, destination: str, duration_days: int, budget: float
    ) -> None:

        if not destination:
            raise ValueError("Destination is required.")

        if duration_days <= 0:
            raise ValueError("Duration must be greater than zero.")

        if budget <= 0:
            raise ValueError("Budget must be greater than zero.")

    # ==================================================
    # Retry Logic
    # ==================================================

    def execute_with_retry(self, function, *args, **kwargs):

        last_error = None

        for _ in range(self.MAX_RETRIES):
            try:
                return function(*args, **kwargs)

            except Exception as error:
                last_error = error

                time.sleep(1)

        raise RuntimeError(f"Operation failed: {last_error}")

    # ==================================================
    # JSON Formatter
    # ==================================================

    def format_trip_response(self, data: dict[str, Any]) -> dict[str, Any]:

        return {key: value for key, value in data.items() if value is not None}

    # ==================================================
    # Final AI Response Builder
    # ==================================================

    def build_complete_response(
        self,
        destination: str,
        duration_days: int,
        budget: float,
        travelers_count: int,
        interests: list[str],
        travel_style: str | None = None,
        transportation_mode: str | None = None,
        preferred_accommodation: str | None = None,
    ) -> dict[str, Any]:

        weather = self.get_weather_context(destination)

        recommendation_context = self.get_recommendation_context(
            destination, interests, budget
        )

        attractions = self.generate_attractions(destination, interests)

        activities = self.generate_activities(interests)

        hotels = self.generate_hotels(destination, budget)

        restaurants = self.generate_restaurants(destination)

        cuisines = self.generate_local_cuisines(destination)

        beverages = self.generate_beverages(destination)

        packing = self.generate_packing_checklist(destination)

        tips = self.generate_travel_tips(destination)

        cost_data = self.estimate_trip_cost(
            budget=budget,
            duration_days=duration_days,
            travelers_count=travelers_count,
            travel_style=travel_style,
            transportation_mode=transportation_mode,
            preferred_accommodation=preferred_accommodation,
        )

        sustainability_score = self.calculate_sustainability_score(
            interests, transportation_mode
        )

        carbon_footprint = self.estimate_carbon_footprint(
            duration_days, transportation_mode
        )

        eco_recommendations = self.generate_eco_recommendations()

        itinerary = self.generate_day_wise_itinerary(
            destination, duration_days, interests
        )

        destination_profile = recommendation_context.get("destination_profile")

        confidence = self.calculate_ai_confidence(
            weather_available=True,
            recommendations_count=len(
                recommendation_context.get("recommendations", [])
            ),
            destination_profile_found=destination_profile is not None,
        )

        return {
            "trip_title": f"{destination} Travel Experience",
            "destination_summary": self.generate_destination_summary(destination),
            "weather_summary": weather,
            "attractions": attractions,
            "activities": activities,
            "recommended_hotels": hotels,
            "recommended_restaurants": restaurants,
            "local_cuisines": cuisines,
            "beverages_to_try": beverages,
            "packing_checklist": packing,
            "travel_tips": tips,
            "ai_itinerary": itinerary,
            "sustainability_score": sustainability_score,
            "carbon_footprint_estimate": carbon_footprint,
            "eco_friendly_recommendations": eco_recommendations,
            "ai_confidence_score": confidence,
            **cost_data,
        }

    # ==================================================
    # Master Trip Plan Generator
    # ==================================================

    def generate_trip_plan(
        self,
        destination: str,
        duration_days: int,
        budget: float,
        interests: list[str],
        travelers_count: int = 1,
        travel_style: str | None = None,
        transportation_mode: str | None = None,
        preferred_accommodation: str | None = None,
    ) -> dict[str, Any]:

        self.validate_trip_input(destination, duration_days, budget)

        cost_data = self.estimate_trip_cost(
            budget=budget,
            duration_days=duration_days,
            travelers_count=travelers_count,
            travel_style=travel_style,
            transportation_mode=transportation_mode,
            preferred_accommodation=preferred_accommodation,
        )

        try:
            prompt = self._build_master_prompt(
                destination=destination,
                duration_days=duration_days,
                budget=budget,
                interests=interests,
                travelers_count=travelers_count,
                travel_style=travel_style,
                transportation_mode=transportation_mode,
                preferred_accommodation=preferred_accommodation,
                cost_data=cost_data,
            )

            ai_response = self.execute_with_retry(self._generate_content, prompt)

            parsed_ai_response = self.parse_gemini_response(ai_response)

            base_response = self.build_complete_response(
                destination=destination,
                duration_days=duration_days,
                budget=budget,
                travelers_count=travelers_count,
                interests=interests,
                travel_style=travel_style,
                transportation_mode=transportation_mode,
                preferred_accommodation=preferred_accommodation,
            )

            if parsed_ai_response and isinstance(parsed_ai_response, dict):
                # Ensure the synthesized itinerary directly overrides the fallback template
                raw_itinerary = parsed_ai_response.get("ai_itinerary")
                if raw_itinerary and isinstance(raw_itinerary, list) and len(raw_itinerary) > 0:
                    base_response["ai_itinerary"] = raw_itinerary
                    base_response["itinerary"] = raw_itinerary

                # Override title & summary with AI curated version if present
                if parsed_ai_response.get("trip_title"):
                    base_response["trip_title"] = str(parsed_ai_response["trip_title"])
                if parsed_ai_response.get("destination_summary"):
                    base_response["destination_summary"] = str(parsed_ai_response["destination_summary"])

                # Override hotels, restaurants, attractions if provided by Gemini
                for list_field in [
                    "recommended_hotels",
                    "recommended_restaurants",
                    "attractions",
                    "activities",
                    "local_cuisines",
                    "beverages_to_try",
                    "packing_checklist",
                    "travel_tips",
                    "eco_friendly_recommendations",
                ]:
                    val = parsed_ai_response.get(list_field)
                    if val and isinstance(val, list) and len(val) > 0:
                        base_response[list_field] = [str(item) for item in val if item]

                base_response["gemini_response"] = parsed_ai_response
                base_response["generation_mode"] = "ai_synthesized"

            return self.format_trip_response(base_response)

        except Exception as error:
            logger.exception("AI Trip Generation Failed: %s", str(error))

            fallback = self.generate_offline_trip_plan(
                destination=destination,
                duration_days=duration_days,
                budget=budget,
                interests=interests,
                travelers_count=travelers_count,
                travel_style=travel_style,
                transportation_mode=transportation_mode,
                preferred_accommodation=preferred_accommodation,
            )

            fallback["error"] = str(error)
            fallback["generation_mode"] = "offline"
            return fallback

    def generate_chat_response(self, user_message: str) -> dict:
        """
        Generate intelligent conversational response for travel companion.
        """
        prompt = f"""You are TripGenius AI, an elite intelligent travel companion.
A traveler asks: "{user_message}"

Provide an inspiring, knowledgeable, practical, and highly detailed response.
If the traveler mentions a destination (like Munnar, Coorg, Ooty, Varkala, Wayanad, etc.), include:
- Best highlights & scenic spots to experience
- Optimal travel timing & weather notes
- Practical budget estimates & recommended duration
- Eco-conscious travel advice (green stays, electric transit, trail etiquette)
- Regional culinary specialties to taste

Format with clear headers and bullet points. Keep it engaging, authentic, and concise."""

        try:
            response = self.client.models.generate_content(
                model=self.model_name, contents=prompt
            )
            reply_text = response.text.strip()
            return {"reply": reply_text, "source": "gemini"}
        except Exception as err:
            logger.warning(
                "Gemini chat error: %s. Using intelligent offline travel knowledge.",
                err,
            )

            # Smart contextual response based on destination keywords
            msg_lower = user_message.lower()
            if "munnar" in msg_lower:
                reply = (
                    "🌿 **TripGenius Guide for Munnar**\n\n"
                    "• **Recommended Duration**: 3 to 4 days for a relaxed highland retreat.\n"
                    "• **Must-Visit Highlights**: Kolukkumalai Sunrise (highest tea estate), Eravikulam National Park (Nilgiri Tahr), Mattupetty Dam, Top Station & Rose Garden.\n"
                    "• **Weather & Climate**: Cool and misty (15°C - 22°C). Carry light woolens, a windcheater, and sturdy walking shoes.\n"
                    "• **Estimated Budget**: ~₹3,500 - ₹5,500 per day for 2 travelers (including boutique resort/homestay, meals & local cab).\n"
                    "• **Culinary Treats**: Freshly plucked spiced cardamom tea, Appam with vegetable stew, Karimeen Pollichathu, and homemade chocolates.\n"
                    "• **Eco Tip**: Choose certified tea estate homestays and avoid single-use plastics along the trekking trails.\n\n"
                    "👉 *Tip: You can use the TripGenius AI Planner to synthesize a full day-by-day itinerary with exact cost breakdown.*"
                )
            elif "coorg" in msg_lower:
                reply = (
                    "☕ **TripGenius Guide for Coorg (Kodagu)**\n\n"
                    "• **Recommended Duration**: 3 days.\n"
                    "• **Must-Visit Highlights**: Abbey Falls, Raja's Seat sunset, Dubare Elephant Camp, Namdroling Monastery (Bylakuppe), and Tadiandamol Trek.\n"
                    "• **Weather**: Pleasant and breezy (18°C - 26°C). Lush green coffee plantations.\n"
                    "• **Culinary Specialties**: Traditional Pandi Curry (or bamboo shoot curry), Kadambuttu, and freshly roasted Arabica coffee.\n"
                    "• **Estimated Budget**: ~₹4,000 - ₹6,000/day for 2."
                )
            elif "ooty" in msg_lower:
                reply = (
                    "🚂 **TripGenius Guide for Ooty (Nilgiris)**\n\n"
                    "• **Recommended Duration**: 3 to 4 days.\n"
                    "• **Must-Visit Highlights**: Nilgiri Mountain Toy Train, Botanical Gardens, Ooty Lake boating, Doddabetta Peak, and Pykara Waterfalls.\n"
                    "• **Weather**: Crisp and cool (12°C - 20°C). Warm jackets recommended for mornings and evenings.\n"
                    "• **Estimated Budget**: ~₹3,800 - ₹5,200/day for 2."
                )
            elif "varkala" in msg_lower:
                reply = (
                    "🌊 **TripGenius Guide for Varkala**\n\n"
                    "• **Recommended Duration**: 2 to 3 days.\n"
                    "• **Must-Visit Highlights**: North Cliff sunset walks, Papanasam Beach natural spring, Janardhana Swamy Temple, and Kappil Lake estuary.\n"
                    "• **Weather**: Warm coastal breeze (24°C - 30°C). Light cottons and sunscreen.\n"
                    "• **Estimated Budget**: ~₹3,000 - ₹4,500/day for 2."
                )
            else:
                reply = (
                    f"✈️ **TripGenius Travel Insight for your journey**\n\n"
                    f'Based on your query: *"{user_message}"*\n\n'
                    "• **Top Regional Recommendations**: Consider Western Ghats sanctuaries (Munnar, Coorg, Wayanad) for mountain greenery, or Coastal Malabar for pristine beaches.\n"
                    "• **Trip Planning Advice**: For multi-day trips, we recommend allocating ~40% of budget to accommodations, 25% to regional dining, and 20% to low-carbon transit.\n"
                    "• **Pacing**: Dedicate at least 3 days to each major destination to minimize transit fatigue.\n\n"
                    "👉 *You can jump to the Planner page to create a complete bespoke itinerary with live weather and cost distribution.*"
                )

            return {"reply": reply, "source": "knowledge_engine"}


# ==================================================
# Singleton Instance
# ==================================================

_ai_service_instance = None


def get_ai_service() -> AIService:

    global _ai_service_instance

    if _ai_service_instance is None:
        _ai_service_instance = AIService()

    return _ai_service_instance
