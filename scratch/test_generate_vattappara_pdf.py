# scratch/test_generate_vattappara_pdf.py
import sys
sys.path.insert(0, r'd:\tripgenius\backend')
from app.services.pdf_service import get_pdf_generator, compute_pdf_filename

gen = get_pdf_generator()

filename = compute_pdf_filename("test", "Vattappara")
print("Computed filename:", filename)

payload = {
    "destination": "Vattappara",
    "trip_title": "Vattappara: Misty Hills & Serene Retreat (3 Days, 2 Nights)",
    "duration_days": 3,
    "budget": 12000,
    "travelers_count": 4,
    "travel_style": "Comfort",
    "destination_summary": "A curated 3-day bespoke family retreat to Vattappara exploring mist-laden Western Ghats tea plantations, spice trails, and authentic Kerala cuisine within ₹12,000.",
    "ai_itinerary": [
        {
            "day": 1,
            "theme": "Arrival & Local Charm",
            "morning": "Arrival in Vattappara — Check into cozy family homestay, settle in and soak up the fresh mountain breeze [Check-in free].",
            "afternoon": "Tea Plantation Stroll — Leisurely walk through verdant tea garden paths and gentle slopes with panoramic valley views [Free entry].",
            "evening": "Sunset Viewpoint & Village Dinner — Head to Vattappara ridge for stunning Western Ghats sunset followed by authentic dinner [~₹250/meal]."
        },
        {
            "day": 2,
            "theme": "Misty Peaks & Nature Trails",
            "morning": "Vattappara Peak Sunrise Trek — Early morning gentle hill trek through misty woods and cloud inversion viewpoints [Guided trail ~₹300].",
            "afternoon": "Spice Garden & Traditional Thali — Guided cardamom, pepper and cinnamon plantation walkthrough followed by traditional Kerala banana leaf meals [~₹350/person].",
            "evening": "Campfire & Stargazing — Relax at homestay with evening tea, small garden campfire, and homemade Kerala fish curry meals [~₹300/meal]."
        },
        {
            "day": 3,
            "theme": "Serene Farewell & Local Markets",
            "morning": "Heritage Village Walk — Crisp morning village walk, local tea stall visit for hot cardamom tea, and breakfast with Puttu and Kadala Curry [~₹80/person].",
            "afternoon": "Spice & Souvenir Shopping — Visit local village market for organic farm-fresh spices and homemade chocolates before departure [Flexible shopping]."
        }
    ],
    "recommended_hotels": [
        "Green Valley Homestay (★ 4.5 Google, ~₹2,800/night) — Peaceful family rooms surrounded by tea shrubs with homecooked breakfast",
        "Misty Mountain Cottages (★ 4.4 Google, ~₹3,200/night) — Wooden eco-cottages nestled amidst cardamom groves with valley view balconies",
        "Vattappara View Guesthouse (★ 4.3 Google, ~₹2,200/night) — Budget-friendly family retreat with warm local hosts and campfire space"
    ],
    "recommended_restaurants": [
        "Hill Top Family Thattukada (★ 4.6 Google, ~₹150/person) — Piping hot Appam with Vegetable Stew & Malabar Parotta with chicken roast",
        "Gramam Traditional Meals House (★ 4.5 Google, ~₹180/person) — Authentic Kerala Sadya, Chemmeen (prawn) roast & fresh river fish curry",
        "Misty Valley Tea Stall & Bakery (★ 4.4 Google, ~₹80/person) — Freshly steamed hot Puttu with Kadala Curry and authentic Kerala filter coffee"
    ],
    "local_cuisines": [
        "Appam with Creamy Coconut Vegetable Stew",
        "Steamed Puttu with Kadala Curry & Pappadam",
        "Traditional Kerala Fish Curry Meals on Banana Leaf",
        "Malabar Parotta with Pepper Chicken Roast",
        "Parippu Vada with Spiced Cardamom Tea"
    ],
    "beverages_to_try": [
        "Fresh Cardamom Spiced Nilgiri/Kerala Black Tea",
        "Kerala Filter Kaapi (Coffee)",
        "Spiced Sambharam (Buttermilk with ginger & curry leaves)",
        "Tender Coconut Water"
    ],
    "weather_summary": {
        "temperature_celsius": 21,
        "condition": "Mist & Gentle Mountain Breeze",
        "advisory": "Expected pleasant cool conditions in Vattappara. Carry a light cardigan or shawl for dawn and late evening."
    },
    "user_name": "test"
}

pdf_bytes = gen.build_pdf(payload)
with open(f"d:/tripgenius/{filename}", "wb") as f:
    f.write(pdf_bytes)

print(f"Successfully generated {filename} ({len(pdf_bytes)} bytes)!")
