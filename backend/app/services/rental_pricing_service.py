"""
TripGenius — Rental Vehicle Pricing & Intelligence Service.

Provides realistic, localized daily rental vehicle rate calculations,
fuel consumption estimates, security deposits, and vehicle recommendations
across Indian and international tourist destinations.
"""

from typing import Any
import re


# Base daily rates (INR) across vehicle categories
VEHICLE_RENTAL_TIERS: dict[str, dict[str, Any]] = {
    "scooter": {
        "label": "Rental Scooter / Two-Wheeler",
        "example_models": "Honda Activa 6G, TVS Jupiter, Vespa 125",
        "daily_rate_min": 400,
        "daily_rate_max": 700,
        "default_daily_rate": 500,
        "fuel_type": "Petrol",
        "avg_km_per_day": 45,
        "mileage_kmpl": 45,
        "fuel_cost_per_liter": 105,
        "security_deposit": "₹1,000 – ₹2,000 (Refundable)",
        "suitability": "Solo or Couples exploring beaches and narrow town lanes",
    },
    "bike_cruiser": {
        "label": "Rental Cruiser / Royal Enfield",
        "example_models": "Royal Enfield Classic 350, Hunter 350, Himalayan",
        "daily_rate_min": 900,
        "daily_rate_max": 1500,
        "default_daily_rate": 1200,
        "fuel_type": "Petrol",
        "avg_km_per_day": 65,
        "mileage_kmpl": 32,
        "fuel_cost_per_liter": 105,
        "security_deposit": "₹2,000 – ₹3,500 (Refundable)",
        "suitability": "Scenic highland ghats and coastal road trips",
    },
    "self_drive_hatchback": {
        "label": "Self-Drive Compact / Hatchback",
        "example_models": "Maruti Swift, Hyundai Grand i10 Nios, Tata Tiago",
        "daily_rate_min": 1200,
        "daily_rate_max": 1800,
        "default_daily_rate": 1500,
        "fuel_type": "Petrol",
        "avg_km_per_day": 75,
        "mileage_kmpl": 17,
        "fuel_cost_per_liter": 105,
        "security_deposit": "₹3,000 – ₹5,000 (Refundable)",
        "suitability": "Budget couples & small groups up to 4 travelers",
    },
    "self_drive_sedan": {
        "label": "Self-Drive Sedan",
        "example_models": "Honda City, Hyundai Verna, Maruti Dzire",
        "daily_rate_min": 1800,
        "daily_rate_max": 2500,
        "default_daily_rate": 2100,
        "fuel_type": "Petrol",
        "avg_km_per_day": 85,
        "mileage_kmpl": 16,
        "fuel_cost_per_liter": 105,
        "security_deposit": "₹4,000 – ₹6,000 (Refundable)",
        "suitability": "Comfortable family cruising & long highway drives",
    },
    "self_drive_suv": {
        "label": "Self-Drive SUV / Hill Explorer",
        "example_models": "Mahindra Thar 4x4, Hyundai Creta, Mahindra Scorpio-N",
        "daily_rate_min": 2500,
        "daily_rate_max": 3800,
        "default_daily_rate": 3000,
        "fuel_type": "Diesel",
        "avg_km_per_day": 90,
        "mileage_kmpl": 14,
        "fuel_cost_per_liter": 95,
        "security_deposit": "₹5,000 – ₹8,000 (Refundable)",
        "suitability": "Mountain ghats, tea estate trails, and group adventures",
    },
    "private_cab": {
        "label": "Dedicated Chauffeur Cab Rental",
        "example_models": "Toyota Innova Crysta / Ertiga with Chauffeur",
        "daily_rate_min": 2400,
        "daily_rate_max": 3500,
        "default_daily_rate": 2800,
        "fuel_type": "Diesel (Driver + Fuel incl. up to 100 km/day)",
        "avg_km_per_day": 100,
        "mileage_kmpl": 13,
        "fuel_cost_per_liter": 95,
        "security_deposit": "Nil (Daily driver beta included)",
        "suitability": "Stress-free family and leisure travel without self-driving",
    },
    "tempo_traveller": {
        "label": "Rental Tempo Traveller (17–26 Seater)",
        "example_models": "Force Urbania, Force Traveller 3350 AC",
        "daily_rate_min": 3500,
        "daily_rate_max": 5200,
        "default_daily_rate": 4200,
        "fuel_type": "Diesel (Driver + running allowance)",
        "avg_km_per_day": 120,
        "mileage_kmpl": 10,
        "fuel_cost_per_liter": 95,
        "security_deposit": "₹2,000 (Advance booking token)",
        "suitability": "Small college batches, student clubs, and groups of 10–25",
    },
    "college_tour_bus": {
        "label": "Deluxe 40–50 Seater Tour Coach / Bus",
        "example_models": "BharatBenz / Tata Starbus / Volvo 9600 AC Coach",
        "daily_rate_min": 8500,
        "daily_rate_max": 13500,
        "default_daily_rate": 10500,
        "fuel_type": "Diesel (Commercial Tourist Permit + Driver)",
        "avg_km_per_day": 150,
        "mileage_kmpl": 5,
        "fuel_cost_per_liter": 95,
        "security_deposit": "₹5,000 (Advance deposit)",
        "suitability": "College class trips, industrial visits (IVs), and 30–60 students",
    },
    "multi_bus_fleet": {
        "label": "Multi-Bus Fleet for Mega College Tours (100+ Students)",
        "example_models": "Fleet of 2–3 Deluxe 50-Seater Tourist Coaches",
        "daily_rate_min": 17000,
        "daily_rate_max": 28000,
        "default_daily_rate": 21000,
        "fuel_type": "Diesel (Dual/Triple Coach Fleet with Dedicated Drivers)",
        "avg_km_per_day": 150,
        "mileage_kmpl": 5,
        "fuel_cost_per_liter": 95,
        "security_deposit": "₹10,000 (Institutional booking deposit)",
        "suitability": "Large college departments, university tours & mega groups of 80–200+ students",
    },
    "luxury_rental": {
        "label": "Premium / Luxury Rental",
        "example_models": "BMW 3 Series, Mercedes C-Class, Audi A4",
        "daily_rate_min": 5000,
        "daily_rate_max": 9500,
        "default_daily_rate": 6500,
        "fuel_type": "Premium Petrol",
        "avg_km_per_day": 100,
        "mileage_kmpl": 11,
        "fuel_cost_per_liter": 110,
        "security_deposit": "₹15,000 – ₹25,000 (Refundable)",
        "suitability": "Luxury leisure and celebratory getaways",
    },
}

# Regional rate multipliers for specific tourist hubs
DESTINATION_RENTAL_MULTIPLIERS: dict[str, float] = {
    "goa": 1.10,        # High seasonal tourist demand
    "munnar": 1.15,     # Hill terrain and ghat driving
    "varkala": 0.95,    # Coastal competitive rates
    "coorg": 1.12,      # Plantation & hill roads
    "ooty": 1.15,       # Ghat terrain
    "wayanad": 1.10,    # Hill roads
    "hampi": 0.90,      # Compact heritage town
    "gokarna": 0.92,    # Beach scooter friendly
    "delhi": 1.05,      # Metro self-drive
    "paris": 2.50,      # Euro equivalent conversion
    "tokyo": 2.80,      # JPY equivalent conversion
    "dubai": 1.80,      # AED equivalent conversion
    "bali": 0.85,       # IDR affordable scooter market
}


def detect_rental_category(transport_mode: str | None, travelers_count: int = 1) -> str | None:
    """
    Determines if the transportation mode is rental-based, and returns the appropriate category.
    """
    if not transport_mode:
        return None

    mode = transport_mode.lower().strip()

    # Keywords indicating a rental setup
    rental_keywords = [
        "rental", "rent", "self-drive", "self drive", "scooter",
        "bike", "two_wheeler", "two wheeler", "two-wheeler", "motorcycle",
        "cab", "taxi", "chauffeur", "car hire", "hired car",
        "tempo", "traveller", "bus", "coach", "tour bus", "van"
    ]

    is_rental = any(kw in mode for kw in rental_keywords) or travelers_count >= 10
    if not is_rental:
        # Also check common transportation strings like "car" or "two wheeler"
        if mode in ["car", "own car"]:
            # If specified as generic "car" with high travel or tourist setting, could be rental
            return None
        return None

    # Determine specific tier based on mode keywords and party size (supporting college/100+ tours)
    if "fleet" in mode or ("bus" in mode and travelers_count >= 70) or travelers_count >= 80:
        return "multi_bus_fleet"
    if "bus" in mode or "coach" in mode or travelers_count >= 28:
        return "college_tour_bus"
    if "tempo" in mode or "traveller" in mode or travelers_count >= 9:
        return "tempo_traveller"
    if "scooter" in mode or "activa" in mode or "moped" in mode or "two_wheeler" in mode or "two-wheeler" in mode or "two wheeler" in mode:
        return "scooter"
    if "enfield" in mode or "bullet" in mode or "cruiser" in mode or "bike" in mode or "motorcycle" in mode:
        return "bike_cruiser" if travelers_count <= 2 else "self_drive_hatchback"
    if "suv" in mode or "thar" in mode or "creta" in mode or "4x4" in mode:
        return "self_drive_suv"
    if "sedan" in mode:
        return "self_drive_sedan"
    if "luxury" in mode or "premium" in mode:
        return "luxury_rental"
    if "cab" in mode or "taxi" in mode or "chauffeur" in mode or "driver" in mode:
        return "private_cab"
    
    # Generic "rental car" / "self drive" -> choose based on group size
    if travelers_count > 4:
        return "self_drive_suv"
    elif travelers_count > 2:
        return "self_drive_sedan"
    elif travelers_count == 1:
        return "scooter"
    else:
        return "self_drive_hatchback"


def calculate_rental_estimate(
    transport_mode: str | None,
    duration_days: int,
    destination: str,
    travelers_count: int = 1,
) -> dict[str, Any] | None:
    """
    Calculates detailed rental vehicle price estimate, fuel consumption,
    and security deposit for the trip duration.
    """
    category = detect_rental_category(transport_mode, travelers_count)
    if not category or category not in VEHICLE_RENTAL_TIERS:
        return None

    tier = VEHICLE_RENTAL_TIERS[category]
    days = max(1, duration_days)
    travelers = max(1, travelers_count)

    dest_key = destination.lower().strip()
    multiplier = DESTINATION_RENTAL_MULTIPLIERS.get(dest_key, 1.0)

    # Base daily rate scaled by location index
    daily_rate = round(tier["default_daily_rate"] * multiplier)
    total_rental_cost = round(daily_rate * days)

    # Estimated fuel calculation (for self-drive vehicles)
    if category != "private_cab":
        total_estimated_km = tier["avg_km_per_day"] * days
        liters_needed = round(total_estimated_km / tier["mileage_kmpl"], 1)
        fuel_estimate = round(liters_needed * tier["fuel_cost_per_liter"])
    else:
        # Cab rate already covers basic local running up to 100km/day
        fuel_estimate = round(days * 350)  # Driver allowance / tolls estimate

    total_transport_estimate = total_rental_cost + fuel_estimate
    per_person_share = round(total_transport_estimate / travelers)

    return {
        "is_rental": True,
        "category": category,
        "vehicle_category": category,
        "vehicle_type": tier["label"],
        "suggested_model": tier["example_models"],
        "example_models": tier["example_models"],
        "capacity": tier["suitability"],
        "daily_rate": daily_rate,
        "daily_rental_rate": daily_rate,
        "rental_days": days,
        "total_rental_cost": total_rental_cost,
        "estimated_fuel_cost": fuel_estimate,
        "estimated_security_deposit": tier["security_deposit"],
        "total_transport_cost": total_transport_estimate,
        "per_person_rental_share": per_person_share,
        "fuel_type": tier["fuel_type"],
        "security_deposit": tier["security_deposit"],
        "suitability": tier["suitability"],
        "booking_tips": "Carry valid Driving License, Govt ID and verify zero-dep insurance coverage.",
        "formatted_summary": (
            f"{tier['label']} ({tier['example_models']}) — "
            f"~₹{daily_rate:,}/day × {days} days = ₹{total_rental_cost:,} "
            f"(+ ~₹{fuel_estimate:,} fuel/tolls). Deposit: {tier['security_deposit']}"
        ),
    }
