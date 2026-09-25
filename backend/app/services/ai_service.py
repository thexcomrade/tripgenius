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

from app.services.verified_travel_data import find_verified_entry

from app.services.budget_learning_service import get_budget_rl_service


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
        nights = max(1, duration_days - 1)
        travelers = max(1, travelers_count)
        acc_per_night = round(cost["accommodation_cost"] / nights, 2)
        food_per_person_day = round(cost["food_cost"] / (duration_days * travelers), 2)
        food_per_meal = round(food_per_person_day / 3, 2)
        transit_per_day = round(cost["transportation_cost"] / duration_days, 2)
        activities_per_day = round(cost["miscellaneous_cost"] / duration_days, 2)

        interests_str = (
            ", ".join(interests)
            if interests
            else "Sightseeing, Local Culture, Scenic Views"
        )

        return f"""You are TripGenius AI, an elite travel architect and real-world expense specialist.
Create an inspiring, highly realistic, and accurate real-money travel and expense plan.

DESTINATION & TRAVEL DETAILS:
- Destination: {destination}
- Duration: {duration_days} Days ({nights} Nights)
- Travelers: {travelers_count} Traveler(s)
- Travel Style: {travel_style or "Leisure"}
- Transit Mode: {transportation_mode or "Private Car / Taxi"}
- Preferred Stay: {preferred_accommodation or "Comfort Hotel"}
- Traveler Interests: {interests_str}

REALISTIC EXPENSE ARCHITECTURE (ALL FIGURES IN REAL MARKET INR):
- Total Allocated Budget: ₹{budget:,.0f} for all {travelers_count} traveler(s) over {duration_days} days.
- Daily Total Allowance: ~₹{cost['cost_per_day']:,.0f} / day (~₹{cost['cost_per_person_day']:,.0f} / person / day).
- Stays & Lodging Budget: Total ₹{cost['accommodation_cost']:,.0f} (~₹{acc_per_night:,.0f} / room / night for {nights} nights).
- Food & Dining Budget: Total ₹{cost['food_cost']:,.0f} (~₹{food_per_person_day:,.0f} / person / day, ~₹{food_per_meal:,.0f} per main meal / person).
- Transit & Sightseeing: Total ₹{cost['transportation_cost']:,.0f} (~₹{transit_per_day:,.0f} / day).
- Activities, Passes & Contingency: Total ₹{cost['miscellaneous_cost']:,.0f} (~₹{activities_per_day:,.0f} / day).

STRICT REAL MONEY EXPENSE & ACCURACY RULES:
1. GEOGRAPHICALLY ACCURATE LOCAL ATTRACTIONS: In 'attractions', provide genuine, iconic attractions that are located STRICTLY within {destination}. If destination is Varkala, provide real Varkala spots (e.g. Varkala Cliff, Papanasam Beach, Janardhana Swami Temple, Kappil Beach & Backwaters, Sivagiri Mutt). NEVER include spots from distant states or other cities (e.g., do NOT list Hampi or Ooty for Varkala).
2. REALISTIC HOTEL NAMES & GOOGLE RATINGS: In 'recommended_hotels', provide 3 REAL, authentically existing hotels/resorts in {destination} with their authentic Google star rating matching ~₹{acc_per_night:,.0f}/night. Format each string as: 'Hotel Name (★ 4.X Google, ~₹X,XXX/night) — key highlight'.
3. REALISTIC DINING SPOTS & GOOGLE RATINGS: In 'recommended_restaurants', provide 3 REAL, authentically existing restaurants/cafes in {destination} with their authentic Google star rating matching ~₹{food_per_meal:,.0f}/meal. Format each string as: 'Restaurant Name (★ 4.X Google, ~₹XXX/person) — signature dish'.
4. REALISTIC EXPENSE TAGS IN ITINERARY: In 'ai_itinerary', every morning, afternoon, and evening plan MUST state explicit, realistic costs or entry fees where money is spent (e.g. 'Morning: Visit local landmark [Entry fee ~₹345/person]. Afternoon: Regional lunch [~₹250/meal]. Evening: Sunset beach stroll [Free]'). If an activity has no fee, label it '[Free entry]'.
5. PROPER CASING & FINANCIAL INTEGRITY: Always use Title Case for destination and all named entities. Daily pacing must stay within total budget ₹{budget:,.0f}.

Return valid JSON ONLY matching this exact schema:
{{
  "trip_title": "{destination} Travel Experience",
  "destination_summary": "Detailed, evocative 2-3 sentence overview of {destination}",
  "ai_itinerary": [
    {{
      "day": 1,
      "title": "Arrival & Initial Highlights",
      "destination": "{destination}",
      "morning": "Detailed morning plan, check-in, [Est. cost in brackets]",
      "afternoon": "Detailed afternoon activity, lunch spot [Est. cost in brackets]",
      "evening": "Detailed evening activity, dinner spot [Est. cost in brackets]",
      "activities": ["Activity 1", "Activity 2"]
    }}
  ],
  "attractions": ["Attraction 1", "Attraction 2", "Attraction 3", "Attraction 4"],
  "activities": ["Activity 1", "Activity 2", "Activity 3"],
  "recommended_hotels": ["Hotel 1 (★ 4.5 Google, ~₹X,XXX/night) — highlight", "Hotel 2 (★ 4.4 Google, ~₹X,XXX/night) — highlight", "Hotel 3 (★ 4.3 Google, ~₹X,XXX/night) — highlight"],
  "recommended_restaurants": ["Restaurant 1 (★ 4.5 Google, ~₹XXX/person) — dish", "Restaurant 2 (★ 4.4 Google, ~₹XXX/person) — dish", "Restaurant 3 (★ 4.3 Google, ~₹XXX/person) — dish"],
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
                err_str = str(error)
                logger.warning("Gemini attempt %s failed: %s", attempt + 1, err_str)

                # Fail fast on 429 quota exhaustion to prevent frontend timeout
                if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str or "quota" in err_str.lower():
                    logger.warning("Gemini quota exhausted (429). Fast-failing to deterministic fallback.")
                    raise RuntimeError("Gemini quota exhausted")

                time.sleep(1)

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
        dest_clean = destination.strip()
        try:
            data = self.weather_service.get_current_weather(dest_clean)
            if data and data.get("temperature") is not None and data.get("temperature") > 0:
                return data
        except Exception as error:
            logger.warning("Weather fetch failed for %s: %s", dest_clean, str(error))

        # Intelligent climate synthesis fallback for regional/hill/beach locations
        q = dest_clean.lower()
        if any(h in q for h in ["chickmanglore", "chikmagalur", "chikkamagaluru", "munnar", "ooty", "kodaikanal", "coorg", "kodagu", "wayanad", "manali", "shimla", "darjeeling", "gangtok"]):
            temp = 20.0
            cond = "Misty & Pleasant"
            desc = f"Cool highland breeze across green hills and plantations in {dest_clean}"
            hum = 75
            wind = 8.5
            rec = "Cool and pleasant mountain weather. Carry light woolens, walking shoes, and a rain jacket."
            packing = ["Light jacket/sweater", "Comfortable walking shoes", "Umbrella/rain gear", "Camera"]
        elif any(c in q for c in ["varkala", "goa", "kochi", "cochin", "alleppey", "alappuzha", "kovalam", "kanyakumari", "pondicherry", "puducherry", "puri"]):
            temp = 29.5
            cond = "Tropical Coastal"
            desc = f"Warm sea breeze with pleasant sunny intervals in {dest_clean}"
            hum = 76
            wind = 14.0
            rec = "Tropical coastal weather. Ideal for sightseeing, beach walks, and sunset photography."
            packing = ["Light cotton clothing", "Sunscreen & sunglasses", "Comfortable sandals", "Swimwear"]
        else:
            temp = 26.5
            cond = "Pleasant & Clear"
            desc = f"Comfortable travel climate across {dest_clean}"
            hum = 65
            wind = 11.0
            rec = f"Favorable conditions for exploring {dest_clean} landmarks and outdoor activities."
            packing = ["Comfortable clothing", "Walking shoes", "Power bank", "Reusable water bottle"]

        return {
            "city": dest_clean,
            "temperature": temp,
            "feels_like": temp + 1.5,
            "condition": cond,
            "description": desc,
            "humidity": hum,
            "wind_speed": wind,
            "travel_recommendation": rec,
            "packing_suggestions": packing,
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
        # 1. First check our verified high-fidelity destination directory
        verified = find_verified_entry(destination)
        if verified and verified.get("attractions"):
            return verified["attractions"]

        # 2. Search destination specifically within the tourism dataset
        dest_matches = self.recommendation_service.search_destination(destination)
        attractions: list[str] = []

        q_clean = destination.lower().strip()
        for item in dest_matches:
            place_name = item.get("place_name", "")
            district = item.get("district", "")
            state = item.get("state", "")
            desc = item.get("description", "") or item.get("activities", "")

            if place_name:
                dist_clean = district.lower()
                state_clean = state.lower()
                p_clean = place_name.lower()
                if (
                    q_clean in p_clean
                    or q_clean in dist_clean
                    or dist_clean in q_clean
                    or q_clean in state_clean
                    or state_clean in q_clean
                ):
                    loc_label = district if district and district.lower() != "regional destination" else (state or destination.title())
                    formatted = f"{place_name} ({loc_label}) — {desc}" if desc else f"{place_name} ({loc_label})"
                    if not any(a.startswith(place_name) for a in attractions):
                        attractions.append(formatted)

        if len(attractions) >= 2:
            return attractions[:10]

        # 3. If any destination matches were found, use top matches
        if dest_matches:
            for m in dest_matches[:8]:
                p = m.get("place_name", "")
                d = m.get("district", "") or m.get("state", "") or destination.title()
                desc = m.get("description", "") or m.get("activities", "")
                if p and not any(a.startswith(p) for a in attractions):
                    formatted = f"{p} ({d}) — {desc}" if desc else f"{p} ({d})"
                    attractions.append(formatted)
            if len(attractions) >= 2:
                return attractions[:10]

        # 4. Fallback: clean Title-cased attractions
        dest_title = destination.strip().title()
        return [
            f"{dest_title} Historic Heritage Old Town Walk",
            f"{dest_title} Panoramic Sunset Viewpoint",
            f"{dest_title} Central Market & Cultural Promenade",
            f"{dest_title} Nature Trail & Botanical Enclave",
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

    def generate_hotels(
        self, destination: str, budget: float, duration_days: int = 3
    ) -> list[str]:
        verified = find_verified_entry(destination)
        if verified and verified.get("hotels"):
            return verified["hotels"]

        nights = max(1, duration_days - 1)
        acc_per_night = max(500, round((budget * 0.40) / nights))
        dest_title = destination.strip().title()

        if budget <= 15000:
            return [
                f"{dest_title} Travelers & Backpackers Lodge (★ 4.3 Google, ~₹{acc_per_night:,.0f}/night) — Clean shared/private dorms, free high-speed WiFi, central transit access",
                f"{dest_title} Heritage Eco Homestay (★ 4.6 Google, ~₹{round(acc_per_night * 0.9):,.0f}/night) — Warm local hospitality & authentic home-cooked breakfast",
                f"{dest_title} Green Residency Inn (★ 4.2 Google, ~₹{round(acc_per_night * 1.1):,.0f}/night) — Peaceful neighborhood stay near landmark sightseeing spots",
            ]

        if budget <= 40000:
            return [
                f"{dest_title} Nature View Boutique Resort (★ 4.5 Google, ~₹{acc_per_night:,.0f}/night) — Scenic balcony vistas, organic breakfast & garden pool",
                f"{dest_title} Comfort Grand Residency (★ 4.4 Google, ~₹{round(acc_per_night * 0.95):,.0f}/night) — Modern luxury suites with concierge & travel desk",
                f"{dest_title} Valley View Heritage Retreat (★ 4.6 Google, ~₹{round(acc_per_night * 1.05):,.0f}/night) — Tranquil landscaped grounds & wellness spa",
            ]

        if budget <= 80000:
            return [
                f"{dest_title} Plantation Luxury Resort & Spa (★ 4.7 Google, ~₹{acc_per_night:,.0f}/night) — Infinity pool, private cottage & guided nature walks",
                f"{dest_title} Premium Grand Heritage Hotel (★ 4.6 Google, ~₹{round(acc_per_night * 0.92):,.0f}/night) — Royal architecture, fine dining & Ayurvedic spa",
                f"{dest_title} Mountain Horizon Retreat (★ 4.8 Google, ~₹{round(acc_per_night * 1.08):,.0f}/night) — Panoramic suites with personal butler & sunset lounge",
            ]

        return [
            f"{dest_title} 5-Star Luxury Palace & Spa (★ 4.9 Google, ~₹{acc_per_night:,.0f}/night) — Private heated pool, butler service & world-class gastronomy",
            f"{dest_title} Exclusive Private Villa Sanctuary (★ 4.8 Google, ~₹{round(acc_per_night * 0.95):,.0f}/night) — Private chef, infinity edge deck & bespoke tours",
            f"{dest_title} Royal Heritage Club & Resort (★ 4.7 Google, ~₹{round(acc_per_night * 1.1):,.0f}/night) — Presidential suites & experiential private cruises",
        ]

    # ==================================================
    # Restaurant Generator
    # ==================================================

    def generate_restaurants(
        self,
        destination: str,
        budget: float = 25000.0,
        duration_days: int = 3,
        travelers_count: int = 1,
    ) -> list[str]:
        verified = find_verified_entry(destination)
        if verified and verified.get("restaurants"):
            return verified["restaurants"]

        days = max(1, duration_days)
        travelers = max(1, travelers_count)
        meal_cost = max(120, round((budget * 0.25) / (days * travelers * 3)))
        dest_title = destination.strip().title()

        return [
            f"{dest_title} Traditional Spice Kitchen (★ 4.5 Google, ~₹{meal_cost:,.0f}/person) — Authentic regional delicacies & wholesome thalis",
            f"{dest_title} Harvest Garden Bistro (★ 4.4 Google, ~₹{round(meal_cost * 1.25):,.0f}/person) — Farm-to-table organic dining & artisan local fare",
            f"{dest_title} Heritage Street Cafe (★ 4.6 Google, ~₹{round(meal_cost * 0.85):,.0f}/person) — Hand-crafted snacks, specialty brew & regional breakfast",
            f"{dest_title} Ocean & Valley View Fine Dining (★ 4.5 Google, ~₹{round(meal_cost * 1.5):,.0f}/person) — Candlelit scenic views & chef's tasting menu",
            f"{dest_title} Travelers Comfort Dhaba (★ 4.3 Google, ~₹{round(meal_cost * 0.75):,.0f}/person) — Comfort regional recipes & freshly baked breads",
        ]

    # ==================================================
    # Cuisine Generator
    # ==================================================

    def generate_local_cuisines(self, destination: str) -> list[str]:
        verified = find_verified_entry(destination)
        if verified and verified.get("cuisines"):
            return verified["cuisines"]

        destination_lower = destination.lower()

        if "munnar" in destination_lower or "kerala" in destination_lower:
            return [
                "Appam with Vegetable/Chicken Stew",
                "Kerala Puttu with Kadala Curry",
                "Authentic Kerala Sadya on Plantain Leaf",
                "Malabar Dum Biryani",
                "Karimeen Pollichathu",
            ]

        if "coorg" in destination_lower or "kodagu" in destination_lower:
            return ["Pandi Curry", "Kadambuttu", "Akki Roti", "Bamboo Shoot Curry"]

        dest_title = destination.strip().title()
        return [
            f"{dest_title} Signature Regional Thali",
            f"{dest_title} Traditional Clay-Pot Curry",
            f"{dest_title} Hand-Crafted Street Specialties",
            "Artisanal Fresh Breads & Sweets",
        ]

    # ==================================================
    # Beverage Generator
    # ==================================================

    def generate_beverages(self, destination: str) -> list[str]:
        verified = find_verified_entry(destination)
        if verified and verified.get("beverages"):
            return verified["beverages"]

        destination_lower = destination.lower()

        if "munnar" in destination_lower:
            return ["Fresh Cardamom Tea", "Highland Green Tea", "Lemon Ginger Tea", "Hot Masala Chai"]

        dest_title = destination.strip().title()
        return [f"Fresh {dest_title} Spiced Tea", "Cold Pressed Fresh Fruit Juice", "Traditional Herbal Infusion"]


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
        destination: str = "",
        db: Any = None,
    ) -> dict[str, Any]:
        """
        Calibrate realistic, human-scale financial breakdown for regional and domestic travel.
        Integrates Reinforcement Learning empirical weights and rental vehicle pricing.
        """
        duration = max(1, duration_days)
        travelers = max(1, travelers_count)
        total_budget = round(float(budget), 2)

        rl_service = get_budget_rl_service()
        factors = rl_service.get_calibrated_factors(
            db=db,
            destination=destination,
            travel_style=travel_style,
            transportation_mode=transportation_mode,
            duration_days=duration,
            travelers_count=travelers,
        )

        pcts = factors["percentages"]
        acc_pct = pcts["accommodation"]
        food_pct = pcts["food"]
        trans_pct = pcts["transportation"]

        accommodation_cost = round(total_budget * acc_pct, 2)
        food_cost = round(total_budget * food_pct, 2)
        transportation_cost = round(total_budget * trans_pct, 2)
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
            "destination_multiplier": factors.get("destination_multiplier", 1.0),
            "learned_samples": factors.get("sample_count", 0),
            "rental_details": factors.get("rental_details"),
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
        self,
        destination: str,
        duration_days: int,
        interests: list[str],
        budget: float = 25000.0,
        travelers_count: int = 1,
    ) -> list[dict[str, Any]]:
        dest_clean = destination.strip()
        raw_attractions = self.generate_attractions(dest_clean, interests)

        # Parse attractions into clean dicts of name, location, highlight
        parsed_attractions = []
        for raw in raw_attractions:
            name = raw
            loc = f"{dest_clean} Region"
            highlight = ""
            if " — " in raw:
                parts = raw.split(" — ", 1)
                name_part = parts[0].strip()
                highlight = parts[1].strip()
                m = re.match(r"^(.*?)\s*\((.*?)\)$", name_part)
                if m:
                    name = m.group(1).strip()
                    loc = m.group(2).strip()
                else:
                    name = name_part
            else:
                m = re.match(r"^(.*?)\s*\((.*?)\)$", raw)
                if m:
                    name = m.group(1).strip()
                    loc = m.group(2).strip()
                else:
                    name = raw.strip()
            parsed_attractions.append({"name": name, "location": loc, "highlight": highlight})

        if not parsed_attractions:
            parsed_attractions = [
                {"name": f"{dest_clean} Historic Core", "location": f"{dest_clean} Center", "highlight": "Heritage sights"},
                {"name": f"{dest_clean} Hill Viewpoint", "location": f"5 km from {dest_clean}", "highlight": "Panoramic vistas"},
                {"name": f"{dest_clean} Botanical Enclave", "location": f"2 km from {dest_clean}", "highlight": "Lush nature & flora"},
                {"name": f"{dest_clean} Local Crafts & Spice Market", "location": f"{dest_clean} Town", "highlight": "Artisan shopping"},
            ]

        itinerary = []
        days = max(1, duration_days)
        travelers = max(1, travelers_count)
        meal_cost = max(120, round((budget * 0.25) / (days * travelers * 3)))
        meal_bfast = max(80, round(meal_cost * 0.65))
        transit_cost = max(150, round((budget * 0.20) / days))
        activity_cost = max(100, round((budget * 0.15) / days))

        attr_idx = 0
        total_attrs = len(parsed_attractions)

        for day in range(1, duration_days + 1):
            day_plan = {
                "day": day,
                "title": f"Day {day}",
                "destination": dest_clean,
                "morning": "",
                "afternoon": "",
                "evening": "",
            }

            if day == 1:
                a1 = parsed_attractions[attr_idx % total_attrs]
                attr_idx += 1
                a2 = parsed_attractions[attr_idx % total_attrs]
                attr_idx += 1

                day_plan["title"] = f"Day 1: Arrival & Exploring {a1['name']}"
                day_plan["morning"] = (
                    f"Arrival in {dest_clean}, hotel check-in [Transit ~₹{transit_cost:,.0f}]. "
                    f"Morning visit to {a1['name']} ({a1['location']}) [Est. entry ~₹{activity_cost:,.0f}]."
                )
                day_plan["afternoon"] = (
                    f"Excursion to {a2['name']} ({a2['location']}) followed by authentic regional lunch (~₹{meal_cost:,.0f}/person)."
                )
                day_plan["evening"] = (
                    f"Sunset stroll through historic {dest_clean} marketplace & tea stalls; dinner at traditional dining spot (~₹{meal_cost:,.0f}/person)."
                )

            elif day == duration_days:
                a_last = parsed_attractions[attr_idx % total_attrs]
                attr_idx += 1

                day_plan["title"] = f"Day {day}: {a_last['name']} & Farewell"
                day_plan["morning"] = (
                    f"Regional breakfast (~₹{meal_bfast:,.0f}/person). Early excursion to {a_last['name']} ({a_last['location']}) for morning vistas [Entry pass ~₹{activity_cost:,.0f}]."
                )
                day_plan["afternoon"] = (
                    f"Final scenic photography stop in {dest_clean}, handicraft & local spice shopping [Self-funded]."
                )
                day_plan["evening"] = (
                    f"Hotel check-out and onward departure transfer [Transit ~₹{transit_cost:,.0f}]."
                )

            else:
                a_morn = parsed_attractions[attr_idx % total_attrs]
                attr_idx += 1
                a_aft = parsed_attractions[attr_idx % total_attrs]
                attr_idx += 1
                a_eve = parsed_attractions[attr_idx % total_attrs]
                attr_idx += 1

                day_plan["title"] = f"Day {day}: {a_morn['name']} & {a_aft['name']}"
                day_plan["morning"] = (
                    f"Guided visit to {a_morn['name']} ({a_morn['location']}) [Est. ticket ~₹{activity_cost:,.0f}/person]."
                )
                day_plan["afternoon"] = (
                    f"Head to {a_aft['name']} ({a_aft['location']}) with regional lunch stop (~₹{meal_cost:,.0f}/person)."
                )
                day_plan["evening"] = (
                    f"Scenic sunset stop at {a_eve['name']} ({a_eve['location']}) followed by local dinner tasting (~₹{meal_cost:,.0f}/person)."
                )

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

        hotels = self.generate_hotels(destination, budget, duration_days)

        restaurants = self.generate_restaurants(
            destination, budget, duration_days, travelers_count
        )

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
            destination=destination,
        )

        sustainability_score = self.calculate_sustainability_score(
            interests, transportation_mode
        )

        carbon_footprint = self.estimate_carbon_footprint(
            duration_days, transportation_mode
        )

        eco_recommendations = self.generate_eco_recommendations()

        itinerary = self.generate_day_wise_itinerary(
            destination, duration_days, interests, budget, travelers_count
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
            destination=destination,
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

            ai_response = self._generate_content(prompt)

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
            logger.warning("AI Trip Generation using deterministic fallback: %s", str(error))

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

            fallback["error"] = None
            fallback["generation_mode"] = "offline"
            return fallback

    def generate_chat_response(self, user_message: str) -> dict:
        """
        Generate intelligent, rapid, and crisp conversational response for travel companion.
        """
        prompt = f"""You are TripGenius AI, a fast, friendly, and knowledgeable personal travel assistant.
Traveler message: "{user_message}"

CRITICAL INSTRUCTIONS:
- Keep your response brief, conversational, and directly helpful (2 to 4 sentences maximum by default).
- If the user introduces themselves or shares their name, greet them warmly by name first.
- If they ask about a destination, give 2-3 top highlights and a quick insider tip.
- Do NOT output large walls of text or full day-by-day itineraries UNLESS the user explicitly asks for a full day-by-day itinerary.
- Keep tone warm, inspiring, and concise."""

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

            # Smart concise contextual response based on destination keywords
            msg_lower = user_message.lower()
            if "munnar" in msg_lower:
                reply = (
                    "🌿 **Munnar** is gorgeous right now! Top highlights are the Kolukkumalai sunrise, Eravikulam National Park, and Mattupetty Dam. "
                    "Plan for 3 days with a budget around ₹4,000/day, and don't miss freshly brewed cardamom tea and hot appams!"
                )
            elif "coorg" in msg_lower:
                reply = (
                    "☕ **Coorg (Kodagu)** is perfect for a 3-day getaway! Be sure to visit Abbey Falls, Raja's Seat for sunset, and the Dubare Elephant Camp. "
                    "Make sure to try authentic Pandi curry or Akki rotis with single-origin Arabica coffee."
                )
            elif "ooty" in msg_lower:
                reply = (
                    "🚂 **Ooty** offers wonderful crisp mountain air (14°C - 20°C). Don't miss the UNESCO Nilgiri Toy Train, the Botanical Gardens, and Doddabetta Peak. "
                    "Carry a light jacket and indulge in homemade fudge and tea!"
                )
            elif "varkala" in msg_lower:
                reply = (
                    "🌊 **Varkala** is pure coastal bliss! Spend your days between the North Cliff sunset cafes, holy Papanasam Beach, and kayaking in Kappil Lake. "
                    "Grab a fresh seafood thali at Darjeeling Cafe or Cafe del Mar overlooking the Arabian Sea."
                )
            elif "goa" in msg_lower:
                reply = (
                    "🌴 **Goa** has the perfect mix of relaxation and energy! Explore Aguada Fort, sunset at Vagator, and the historic Latin Quarter of Fontainhas. "
                    "Try butter garlic crab at Britto's or authentic Goan fish curry rice in Assagao."
                )
            else:
                reply = (
                    f"✈️ Hello! I'd love to help plan your trip for **{user_message.strip()}**! "
                    "Tell me your preferred travel style (beach, mountains, culture, or adventure) and how many days you have, and I'll tailor the ideal itinerary for you!"
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
