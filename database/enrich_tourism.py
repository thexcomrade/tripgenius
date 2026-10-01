"""
TripGenius Tourism Dataset Integration & Enrichment Engine.
Analyzes D:\\tripgenius\\database\\india.csv and integrates all tourist spots,
regional attractions, and international destinations into D:\\tripgenius\\database\\tourism.csv
and D:\\tripgenius\\backend\\tourism.csv.
"""

import re
import sys
import pandas as pd
from pathlib import Path

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding="utf-8")

INDIA_CSV_PATH = Path("D:/tripgenius/database/india.csv")
TOURISM_CSV_PATH = Path("D:/tripgenius/database/tourism.csv")
BACKEND_TOURISM_CSV_PATH = Path("D:/tripgenius/backend/tourism.csv")

TARGET_COLUMNS = [
    "Name of the Place",
    "District",
    "Famous_For",
    "Activities",
    "State",
    "Country",
    "Category",
    "Travel_Style",
    "Best_Season",
    "Budget_Category",
    "Duration_Days",
]


def clean_str(val: any) -> str:
    if val is None or pd.isna(val):
        return ""
    s = str(val).strip()
    s = re.sub(r"\s+", " ", s)
    return s


def normalize_place_key(name: str) -> str:
    """Normalize a place name for deduplication lookup."""
    s = clean_str(name).lower()
    s = re.sub(r"[^\w\s]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def standardize_season(season_raw: str, months_raw: str) -> str:
    s = clean_str(season_raw).lower()
    m = clean_str(months_raw).lower()
    combined = f"{s} {m}"

    if "year-round" in s or "year round" in s or "all year" in s:
        return "Year-round"
    if "oct" in s and "mar" in s:
        return "October to March"
    if "oct" in s and "feb" in s:
        return "October to February"
    if "nov" in s and "feb" in s:
        return "November to February"
    if "nov" in s and "mar" in s:
        return "November to March"
    if "nov" in s and "apr" in s:
        return "November to April"
    if "apr" in s and "oct" in s:
        return "April to October"
    if "apr" in s and "jun" in s:
        return "April to June"
    if "may" in s and "oct" in s:
        return "May to October"
    if "dec" in s and "feb" in s:
        return "December to February"
    if "jul" in s and "sep" in s:
        return "July to September"
    if "mar" in s and "may" in s:
        return "March to May"
    if "sep" in s and "nov" in s:
        return "September to November"
    if "dry season" in combined:
        return "April to October"
    if "winter" in combined:
        return "October to March"
    if "summer" in combined:
        return "April to June"

    return "October to March"


def map_category_and_style(
    category_raw: str, spot_type_raw: str, chars_raw: str, place_name: str
) -> tuple[str, str]:
    text = f"{category_raw} {spot_type_raw} {chars_raw} {place_name}".lower()

    if any(k in text for k in ["temple", "mandir", "basilica", "cathedral", "church", "synagogue", "monastery", "stupa", "shrine", "mosque", "dargah", "gurudwara", "religious", "spiritual"]):
        return "Temple/Religious", "Spiritual, Cultural, Photography"
    
    if any(k in text for k in ["fort", "palace", "monument", "heritage", "historical", "unesco", "ruins", "castle", "chariot", "mutt", "gateway", "mahal", "tower", "pyramid", "colosseum"]):
        return "Heritage", "Cultural, Heritage, Photography"
    
    if any(k in text for k in ["museum", "gallery", "exhibit", "aviation centre", "planetarium"]):
        return "Heritage", "Cultural, Educational, Photography"
    
    if any(k in text for k in ["beach", "coast", "cliff", "shore", "cove", "bay"]):
        return "Beach", "Beach, Relaxation, Photography"
    
    if any(k in text for k in ["waterfall", "falls", "cascade"]):
        return "Waterfall", "Eco, Adventure, Photography"
    
    if any(k in text for k in ["lake", "dam", "backwater", "river", "lagoon", "reservoir", "boat", "canal", "ghat"]):
        return "Lake/Water", "Eco, Leisure, Photography"
    
    if any(k in text for k in ["island", "atoll", "reef"]):
        return "Island", "Beach, Island, Leisure, Photography"
    
    if any(k in text for k in ["wildlife", "safari", "sanctuary", "national park", "tiger", "lion", "rhino", "crocodile", "zoo", "bird"]):
        return "Wildlife", "Wildlife, Adventure, Photography"
    
    if any(k in text for k in ["peak", "mountain", "hill", "trek", "hike", "ridge", "valley", "ghat", "alp", "fuji", "volcano"]):
        return "Mountain/Hill", "Adventure, Nature, Photography"
    
    if any(k in text for k in ["cave", "rock-cut", "petroglyph", "geological"]):
        return "Cave/Geological", "Adventure, Heritage, Photography"
    
    if any(k in text for k in ["garden", "botanical", "park", "forest", "tree", "tea", "coffee", "plantation", "nature", "alam"]):
        return "Garden/Nature", "Eco, Nature, Leisure, Photography"
    
    if any(k in text for k in ["shopping", "mall", "market", "bazaar", "street"]):
        return "Shopping", "Leisure, Shopping, Cultural"
    
    if any(k in text for k in ["amusement", "theme park", "aquarium", "water park", "resort"]):
        return "Theme Park", "Leisure, Family, Adventure"

    return "Sightseeing", "Cultural, Leisure, Photography"


def derive_activities(category: str, place_name: str, chars: str) -> str:
    c_lower = category.lower()
    text = f"{category} {place_name} {chars}".lower()

    if "temple" in c_lower or "religious" in c_lower:
        return "Temple darshan, Spiritual meditation, Architectural photography, Cultural heritage walk"
    if "beach" in c_lower:
        return "Beach walking, Sunset viewing, Coastal photography, Watersports, Seaside relaxation"
    if "waterfall" in c_lower:
        return "Waterfall trekking, Nature photography, Forest hiking, Scenic viewpoint visit"
    if "lake" in c_lower or "water" in c_lower:
        return "Boating, Scenic lakeside stroll, Sunset photography, Bird watching, Relaxing cruise"
    if "mountain" in c_lower or "hill" in c_lower:
        return "Mountain trekking, Panoramic photography, Sunrise viewpoint visit, Highland hiking"
    if "heritage" in c_lower:
        return "Historical guided tour, Architecture photography, Monument exploration, Cultural walk"
    if "wildlife" in c_lower:
        return "Wildlife safari, Jeep exploration, Animal sighting, Birdwatching, Nature photography"
    if "garden" in c_lower or "nature" in c_lower:
        return "Nature walk, Botanical photography, Peaceful stroll, Picnicking, Flora observation"
    if "island" in c_lower:
        return "Island exploration, Snorkeling, Beach sunbathing, Sunset cruise, Marine photography"
    if "cave" in c_lower:
        return "Cave exploration, Archaeological study, Geological photography, Trekking"
    if "shopping" in c_lower:
        return "Local handicraft shopping, Street food tasting, Evening promenade, Souvenir buying"
    
    return "Sightseeing, Guided cultural tour, Photography, Local exploration, Scenic leisure walk"


def build_famous_for(row: pd.Series) -> str:
    significance = clean_str(row.get("Significance", ""))
    chars = clean_str(row.get("Characteristics", ""))
    spot_type = clean_str(row.get("Spot_Type", ""))
    name = clean_str(row.get("Tourist_Spot_Name", ""))

    # If it's a Bali Indonesian spot with generic terms
    if spot_type in ["Umum", "Alam", "Budaya", "Rekreasi"]:
        type_labels = {
            "Alam": "Breathtaking natural landscape, tropical greenery and scenic viewpoints",
            "Budaya": "Rich Balinese cultural heritage, traditional arts and architectural splendor",
            "Rekreasi": "Vibrant recreational destination, family fun and leisure tourism activities",
            "Umum": "Popular public landmark, gathering area and iconic Balinese sightseeing spot",
        }
        base_desc = type_labels.get(spot_type, "Renowned tourist landmark in Bali")
        if chars and "bali tourism" not in chars.lower():
            return f"{chars.capitalize()} — {base_desc}"
        return f"{name} — {base_desc}"

    # For other spots
    parts = []
    if significance and significance.lower() not in ["tourist attraction", "scenic", "environmental", "historical", "modern", "religious"]:
        parts.append(significance)
    elif significance:
        parts.append(f"{significance.capitalize()} attraction")

    if chars:
        parts.append(chars)

    if parts:
        desc = " — ".join(parts)
        # Capitalize first letter
        return desc[:1].upper() + desc[1:]

    return f"Renowned landmark in {clean_str(row.get('City', ''))}, famous for cultural significance and sightseeing"


def determine_budget_and_duration(row: pd.Series) -> tuple[str, int]:
    fee_val = row.get("Entry_Fee_INR_Numeric", 0)
    try:
        fee = float(fee_val) if not pd.isna(fee_val) else 0.0
    except (ValueError, TypeError):
        fee = 0.0

    duration_val = str(row.get("Visit_Duration_hrs", "1")).strip()
    try:
        dur_hrs = float(re.findall(r"\d+", duration_val)[0]) if re.findall(r"\d+", duration_val) else 1.0
    except (ValueError, IndexError):
        dur_hrs = 1.0

    # Determine budget category
    if fee >= 2000 or "luxury" in str(row.get("Accommodation_Options", "")).lower():
        budget = "Luxury"
    elif fee >= 500:
        budget = "Moderate"
    elif fee > 0:
        budget = "Budget"
    else:
        budget = "Budget"

    # Determine duration days
    if dur_hrs >= 8 or any(k in str(row.get("Spot_Type", "")).lower() for k in ["national park", "trek", "mountain", "hill station"]):
        duration_days = 2
    else:
        duration_days = 1

    return budget, duration_days


def main():
    print(f"Loading existing {TOURISM_CSV_PATH}...")
    df_tour = pd.read_csv(TOURISM_CSV_PATH)
    print(f"Current tourism.csv rows: {len(df_tour)}")

    print(f"Loading {INDIA_CSV_PATH}...")
    df_india = pd.read_csv(INDIA_CSV_PATH)
    print(f"Current india.csv rows: {len(df_india)}")

    # Map existing rows into a dictionary indexed by normalized place name
    existing_map = {}
    for idx, row in df_tour.iterrows():
        key = normalize_place_key(row["Name of the Place"])
        if key:
            existing_map[key] = row.to_dict()

    print(f"Unique existing keys in tourism: {len(existing_map)}")

    # 1. Transform and add records from india.csv
    added_from_india = 0
    for _, row in df_india.iterrows():
        name = clean_str(row.get("Tourist_Spot_Name", ""))
        if not name:
            continue
        
        key = normalize_place_key(name)
        if key in existing_map:
            continue

        city = clean_str(row.get("City", ""))
        state = clean_str(row.get("State", ""))
        country_raw = clean_str(row.get("Country", "India"))
        country = "Indonesia" if "Indonesia" in country_raw else (country_raw or "India")

        district = city if city else state

        cat, style = map_category_and_style(
            clean_str(row.get("Category", "")),
            clean_str(row.get("Spot_Type", "")),
            clean_str(row.get("Characteristics", "")),
            name
        )

        famous_for = build_famous_for(row)
        activities = derive_activities(cat, name, clean_str(row.get("Characteristics", "")))
        season = standardize_season(row.get("Best_Season", ""), row.get("Best_Months", ""))
        budget, duration = determine_budget_and_duration(row)

        record = {
            "Name of the Place": name,
            "District": district,
            "Famous_For": famous_for,
            "Activities": activities,
            "State": state,
            "Country": country,
            "Category": cat,
            "Travel_Style": style,
            "Best_Season": season,
            "Budget_Category": budget,
            "Duration_Days": duration,
        }

        existing_map[key] = record
        added_from_india += 1

    print(f"Added {added_from_india} new records from india.csv.")

    # 2. Explicit prompt-targeted curated records
    PROMPT_CURATED_SPOTS = [
        # Kerala - Thiruvananthapuram & Varkala
        {
            "Name of the Place": "Padmanabhaswamy Temple",
            "District": "Thiruvananthapuram",
            "Famous_For": "Ancient Travancore royal temple dedicated to Lord Vishnu, world's richest Hindu shrine with Dravidian stone gopuram",
            "Activities": "Temple darshan, Traditional puja, Architecture photography, Heritage walk around temple pond",
            "State": "Kerala",
            "Country": "India",
            "Category": "Temple/Religious",
            "Travel_Style": "Spiritual, Cultural, Photography",
            "Best_Season": "October to March",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Kovalam Beach",
            "District": "Thiruvananthapuram",
            "Famous_For": "Internationally acclaimed crescent beaches, Vizhinjam lighthouse beacon and Ayurvedic coastal wellness retreats",
            "Activities": "Lighthouse climbing, Beach walking, Catamaran boat cruise, Sunset viewing, Ayurvedic massage",
            "State": "Kerala",
            "Country": "India",
            "Category": "Beach",
            "Travel_Style": "Beach, Relaxation, Photography",
            "Best_Season": "October to March",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Napier Museum",
            "District": "Thiruvananthapuram",
            "Famous_For": "19th-century Indo-Saracenic architectural masterpiece housing rare historical bronze idols, ancient ornaments and royal ivory carvings",
            "Activities": "Museum tour, Art and archaeology study, Botanical garden stroll, Cultural photography",
            "State": "Kerala",
            "Country": "India",
            "Category": "Heritage",
            "Travel_Style": "Cultural, Educational, Photography",
            "Best_Season": "October to March",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Kuthiramalika Palace Museum",
            "District": "Thiruvananthapuram",
            "Famous_For": "Travancore royal palace featuring 122 carved wooden horses, pure teakwood ceilings, royal thrones and Belgian mirrors",
            "Activities": "Palace guided tour, Royal artifact viewing, Classical music festival visit, Heritage photography",
            "State": "Kerala",
            "Country": "India",
            "Category": "Heritage",
            "Travel_Style": "Cultural, Heritage, Photography",
            "Best_Season": "October to March",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Varkala Cliff Beach",
            "District": "Thiruvananthapuram",
            "Famous_For": "Dramatic red laterite sedimentary cliffs overlooking the Arabian Sea, bohemian sunset cafes and holistic yoga hubs",
            "Activities": "Cliff walkway stroll, Sunset viewing, Bohemian cafe hopping, Parasailing, Beach yoga",
            "State": "Kerala",
            "Country": "India",
            "Category": "Beach",
            "Travel_Style": "Beach, Relaxation, Adventure, Photography",
            "Best_Season": "October to March",
            "Budget_Category": "Budget",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Poovar Island",
            "District": "Thiruvananthapuram",
            "Famous_For": "Enchanting coastal estuary where river, lake, sea and golden sand beach converge amongst mangrove forests",
            "Activities": "Country boat safari, Mangrove forest cruise, Floating restaurant dining, Golden beach stroll",
            "State": "Kerala",
            "Country": "India",
            "Category": "Island",
            "Travel_Style": "Eco, Leisure, Boating, Photography",
            "Best_Season": "October to March",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Agasthyakoodam Peak",
            "District": "Thiruvananthapuram",
            "Famous_For": "Sacred 1,868m Western Ghats summit renowned for rare medicinal herbs, Neelakurinji blooms and bird biodiversity",
            "Activities": "Mountain trekking, Forest exploration, Birdwatching, Panoramic summit photography",
            "State": "Kerala",
            "Country": "India",
            "Category": "Mountain/Hill",
            "Travel_Style": "Adventure, Trekking, Eco, Photography",
            "Best_Season": "January to March",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
        # Kerala - Kochi & Alappuzha
        {
            "Name of the Place": "Fort Kochi",
            "District": "Kochi",
            "Famous_For": "Historic maritime precinct featuring giant Chinese fishing nets, colonial Portuguese mansions and artisan cafes",
            "Activities": "Chinese fishing net sunset watch, Colonial heritage cycling tour, Art gallery visits, Seafood dining",
            "State": "Kerala",
            "Country": "India",
            "Category": "Heritage",
            "Travel_Style": "Cultural, Heritage, Leisure, Photography",
            "Best_Season": "October to March",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Mattancherry Dutch Palace",
            "District": "Kochi",
            "Famous_For": "1555 Portuguese-built and Dutch-renovated palace renowned for exquisite Hindu Ramayana murals and royal palanquins",
            "Activities": "Mural art appreciation, Palace heritage walk, Royal portrait gallery tour, History photography",
            "State": "Kerala",
            "Country": "India",
            "Category": "Heritage",
            "Travel_Style": "Cultural, Educational, Photography",
            "Best_Season": "October to March",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Paradesi Synagogue",
            "District": "Kochi",
            "Famous_For": "Oldest active Commonwealth synagogue built in 1568 in Jew Town, adorned with hand-painted Chinese porcelain tiles and Belgian chandeliers",
            "Activities": "Heritage synagogue tour, Jew Town spice market walk, Antique shopping, Historical photography",
            "State": "Kerala",
            "Country": "India",
            "Category": "Heritage",
            "Travel_Style": "Cultural, Heritage, Spiritual",
            "Best_Season": "October to March",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Cherai Beach",
            "District": "Kochi",
            "Famous_For": "10-kilometer golden coastline bordered by tranquil backwaters on Vypin Island with frequent dolphin sightings",
            "Activities": "Swimming, Dolphin watching, Shell collecting, Beachside fresh coconut water, Sunset stroll",
            "State": "Kerala",
            "Country": "India",
            "Category": "Beach",
            "Travel_Style": "Beach, Leisure, Family",
            "Best_Season": "October to March",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Alleppey Backwaters & Houseboat circuits",
            "District": "Alappuzha",
            "Famous_For": "Vast labyrinth of emerald canals, lagoons, and paddy fields navigated on traditional luxury thatched Kettuvallam houseboats",
            "Activities": "Overnight houseboat cruise, Village canoe tours, Toddy shop lunch, Paddy field photography",
            "State": "Kerala",
            "Country": "India",
            "Category": "Lake/Water",
            "Travel_Style": "Eco, Leisure, Boating, Photography",
            "Best_Season": "October to March",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Alleppey Beach",
            "District": "Alappuzha",
            "Famous_For": "Historic coastal beach featuring a 150-year-old landmark sea pier and an antique red-and-white colonial lighthouse",
            "Activities": "Old pier walk, Lighthouse climbing, Beach camel rides, Sunset photography, Evening sea breeze",
            "State": "Kerala",
            "Country": "India",
            "Category": "Beach",
            "Travel_Style": "Beach, Leisure, Photography",
            "Best_Season": "October to March",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Kumarakom Bird Sanctuary",
            "District": "Kottayam",
            "Famous_For": "14-acre wetland bird sanctuary on the banks of Vembanad Lake, seasonal refuge for migratory Siberian cranes and kingfishers",
            "Activities": "Birdwatching boat safari, Nature trail walking, Canopy photography, Vembanad lake cruising",
            "State": "Kerala",
            "Country": "India",
            "Category": "Wildlife",
            "Travel_Style": "Wildlife, Eco, Nature, Photography",
            "Best_Season": "November to February",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        # Kerala - Wayanad & Idukki
        {
            "Name of the Place": "Chembra Peak",
            "District": "Wayanad",
            "Famous_For": "Highest summit in Wayanad (2,100m) renowned for its natural mist-clad heart-shaped mountain lake (Hridaya Saras)",
            "Activities": "Highland trekking, Heart lake photography, Mountain camping, Western Ghats ridge walking",
            "State": "Kerala",
            "Country": "India",
            "Category": "Mountain/Hill",
            "Travel_Style": "Adventure, Trekking, Nature, Photography",
            "Best_Season": "October to May",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Edakkal Prehistoric Caves",
            "District": "Wayanad",
            "Famous_For": "Neolithic rock shelters perched 1,200m on Ambukuthi Mala, adorned with 6,000-year-old Stone Age petroglyphs and engravings",
            "Activities": "Rock cliff climbing, Prehistoric petroglyph study, Cave photography, Panoramic valley viewing",
            "State": "Kerala",
            "Country": "India",
            "Category": "Cave/Geological",
            "Travel_Style": "Heritage, Adventure, Educational, Photography",
            "Best_Season": "October to May",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Pookode Lake",
            "District": "Wayanad",
            "Famous_For": "Picturesque natural freshwater lake naturally shaped like the map of India, surrounded by evergreen rainforest hills and blue water lilies",
            "Activities": "Pedal boating, Freshwater aquarium visit, Lakeside cycling, Spices shopping",
            "State": "Kerala",
            "Country": "India",
            "Category": "Lake/Water",
            "Travel_Style": "Eco, Leisure, Boating, Family",
            "Best_Season": "October to May",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Banasura Sagar Earthen Dam",
            "District": "Wayanad",
            "Famous_For": "Largest earthen dam in India and second largest in Asia, with scenic islands dotting the massive reservoir against Banasura hills",
            "Activities": "Speed boating, Ziplining, Reservoir island photography, Dam crest walking",
            "State": "Kerala",
            "Country": "India",
            "Category": "Lake/Water",
            "Travel_Style": "Adventure, Eco, Boating, Photography",
            "Best_Season": "September to May",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Thirunelli Ancient Temple",
            "District": "Wayanad",
            "Famous_For": "Ancient Vishnu shrine known as the Kashi of the South, nestled in Brahmagiri hills with granite aqueduct and holy Papanasini stream",
            "Activities": "Ancestral rituals at Papanasini stream, Sacred darshan, Forest mountain photography, Temple heritage walk",
            "State": "Kerala",
            "Country": "India",
            "Category": "Temple/Religious",
            "Travel_Style": "Spiritual, Cultural, Heritage",
            "Best_Season": "October to March",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Idukki Arch Dam",
            "District": "Idukki",
            "Famous_For": "Asia's first and largest double curvature parabolic arch dam built between Kuravan and Kurathi granite hills over the Periyar River",
            "Activities": "Dam engineering tour, Speed boating, Mountain reservoir photography, Kuravan hill viewpoints",
            "State": "Kerala",
            "Country": "India",
            "Category": "Lake/Water",
            "Travel_Style": "Sightseeing, Educational, Photography",
            "Best_Season": "October to March",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        # Kerala - Thrissur & Kozhikode
        {
            "Name of the Place": "Thrissur Pooram Grounds",
            "District": "Thrissur",
            "Famous_For": "Historic Thekkinkadu Maidan, host of the world-famous Thrissur Pooram festival featuring caparisoned elephants and Ilanjithara Melam percussion",
            "Activities": "Pooram festival attendance, Cultural photography, Temple ground walking, Traditional percussion listening",
            "State": "Kerala",
            "Country": "India",
            "Category": "Heritage",
            "Travel_Style": "Cultural, Spiritual, Photography",
            "Best_Season": "April to May",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Vadakkumnathan Temple",
            "District": "Thrissur",
            "Famous_For": "Ancient UNESCO-honored Kerala architectural gem dedicated to Lord Shiva with monumental multi-tiered gopurams and massive ghee-covered lingam",
            "Activities": "Temple darshan, Kerala wood architecture study, Mural art viewing, Sacred inner courtyard walk",
            "State": "Kerala",
            "Country": "India",
            "Category": "Temple/Religious",
            "Travel_Style": "Spiritual, Cultural, Heritage",
            "Best_Season": "October to March",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Guruvayur Temple",
            "District": "Thrissur",
            "Famous_For": "Celebrated 5,000-year-old pilgrimage shrine worshipped as Bhuloka Vaikuntha (Lord Krishna on Earth), famous for royal elephant sanctuary Punnathur Kotta",
            "Activities": "Nirmalya darshan, Elephant sanctuary visit, Cultural temple rituals, Traditional prasadam tasting",
            "State": "Kerala",
            "Country": "India",
            "Category": "Temple/Religious",
            "Travel_Style": "Spiritual, Cultural, Heritage",
            "Best_Season": "October to March",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Athirappilly Falls",
            "District": "Thrissur",
            "Famous_For": "The Niagara of India — majestic 80-foot wide roaring cascade crashing through dense Sholayar rainforest canopy",
            "Activities": "Waterfall base trekking, Rain forest photography, Bamboo rafting, Scenic overlook viewing",
            "State": "Kerala",
            "Country": "India",
            "Category": "Waterfall",
            "Travel_Style": "Eco, Adventure, Nature, Photography",
            "Best_Season": "September to January",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Kappad Beach",
            "District": "Kozhikode",
            "Famous_For": "Historic rocky shore where Portuguese explorer Vasco da Gama first landed in India on May 20, 1498, changing world maritime trade",
            "Activities": "Historical monument visit, Promenade walking, Rocky headland photography, Sunset viewing",
            "State": "Kerala",
            "Country": "India",
            "Category": "Beach",
            "Travel_Style": "Heritage, Beach, Leisure, Photography",
            "Best_Season": "October to March",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Beypore Beach",
            "District": "Kozhikode",
            "Famous_For": "Historic port town famed for centuries-old artisanal Uru (wooden Arabian dhow) shipbuilding yard and a 2km stone sea bridge",
            "Activities": "2km sea bridge walk into ocean, Traditional Uru shipbuilding yard tour, Malabar seafood tasting",
            "State": "Kerala",
            "Country": "India",
            "Category": "Beach",
            "Travel_Style": "Cultural, Beach, Heritage, Leisure",
            "Best_Season": "October to March",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        # Kerala - Kannur & Kasaragod
        {
            "Name of the Place": "Bekal Fort",
            "District": "Kasaragod",
            "Famous_For": "Largest and best-preserved 17th-century coastal fortress in Kerala, featuring observation towers looking out over breaking Arabian Sea waves",
            "Activities": "Fort rampart walking, Sea viewpoint photography, Observation tower climbing, Beach strolling",
            "State": "Kerala",
            "Country": "India",
            "Category": "Heritage",
            "Travel_Style": "Heritage, Cultural, Beach, Photography",
            "Best_Season": "October to March",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Payyambalam Beach",
            "District": "Kannur",
            "Famous_For": "Secluded, impeccably clean golden shoreline featuring lush coastal gardens and monumental mother-and-child seaside sculpture",
            "Activities": "Sunset stroll, Seaside park leisure, Beachside coconut water, Photography",
            "State": "Kerala",
            "Country": "India",
            "Category": "Beach",
            "Travel_Style": "Beach, Leisure, Relaxation",
            "Best_Season": "October to March",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Ezhimala Beach",
            "District": "Kannur",
            "Famous_For": "Historic headland and former capital of the Mooshika kings, home to Indian Naval Academy and isolated pristine beaches",
            "Activities": "Coastal ridge viewing, Lighthouse photography, Marine heritage study, Quiet beach walking",
            "State": "Kerala",
            "Country": "India",
            "Category": "Beach",
            "Travel_Style": "Beach, Nature, Heritage, Photography",
            "Best_Season": "October to March",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        # Karnataka Region
        {
            "Name of the Place": "Coorg (Kodagu)",
            "District": "Coorg",
            "Famous_For": "Scotland of India — rolling mist-clad coffee and spice plantations, Raja's Seat sunsets and Kodava martial heritage",
            "Activities": "Coffee plantation plantation walks, Abbey Falls trekking, River Cauvery rafting, Kodava pork curry tasting",
            "State": "Karnataka",
            "Country": "India",
            "Category": "Mountain/Hill",
            "Travel_Style": "Eco, Nature, Adventure, Photography",
            "Best_Season": "October to May",
            "Budget_Category": "Moderate",
            "Duration_Days": 3,
        },
        {
            "Name of the Place": "Hampi (Vijayanagara UNESCO ruins)",
            "District": "Ballari",
            "Famous_For": "UNESCO World Heritage site showcasing monumental 14th-century Vijayanagara Empire stone temples, monolithic chariot and musical pillars",
            "Activities": "Coracle boat ride on Tungabhadra, Stone Chariot photography, Matanga Hill sunrise trek, Temple exploration",
            "State": "Karnataka",
            "Country": "India",
            "Category": "Heritage",
            "Travel_Style": "Cultural, Heritage, Spiritual, Photography",
            "Best_Season": "October to March",
            "Budget_Category": "Moderate",
            "Duration_Days": 3,
        },
        {
            "Name of the Place": "Belur & Halebidu (Hoysala architecture)",
            "District": "Hassan",
            "Famous_For": "UNESCO World Heritage marvels of 12th-century Hoysala soapstone architecture, intricate filigree sculptures and star-shaped Chennakeshava temple",
            "Activities": "Soapstone sculpture appreciation, Architectural photography, Guided history tour, Hoysaleswara temple visit",
            "State": "Karnataka",
            "Country": "India",
            "Category": "Heritage",
            "Travel_Style": "Cultural, Heritage, Educational, Photography",
            "Best_Season": "October to March",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Badami Cave Temples",
            "District": "Bagalkot",
            "Famous_For": "6th-century Chalukyan rock-cut sandstone cave temples overlooking Agastya Lake, famed for 18-armed dancing Nataraja carvings",
            "Activities": "Cave temple climbing, Agastya Lake boating, Bhutanatha temple photography, Chalukyan history tour",
            "State": "Karnataka",
            "Country": "India",
            "Category": "Cave/Geological",
            "Travel_Style": "Heritage, Cultural, Adventure, Photography",
            "Best_Season": "October to March",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Jog Falls",
            "District": "Shimoga",
            "Famous_For": "Second-highest plunge waterfall in India where the Sharavathi River thunders down 830 feet in four distinct cascades: Raja, Rani, Roarer and Rocket",
            "Activities": "Cascade viewing from Watkins platform, 1,400-step trek to gorge base, Rainbow mist photography, Sharavathi hydro walk",
            "State": "Karnataka",
            "Country": "India",
            "Category": "Waterfall",
            "Travel_Style": "Eco, Adventure, Nature, Photography",
            "Best_Season": "July to December",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Murudeshwar Shiva Temple",
            "District": "Uttara Kannada",
            "Famous_For": "Colossal 123-foot Lord Shiva statue, the world's second-tallest, and a 20-story Raja Gopuram jutting into the Arabian Sea on Kanduka Hill",
            "Activities": "Raja Gopuram elevator ride, Shiva statue photography, Arabian Sea coastal walk, Netrani Island scuba diving",
            "State": "Karnataka",
            "Country": "India",
            "Category": "Temple/Religious",
            "Travel_Style": "Spiritual, Cultural, Beach, Photography",
            "Best_Season": "October to March",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Chikmagalur (Mullayanagiri)",
            "District": "Chikmagalur",
            "Famous_For": "Coffee capital of India crowned by Mullayanagiri (1,930m), highest peak in Karnataka, with Bababudan Giri and Baba Budan coffee shrines",
            "Activities": "Peak summit trek, Coffee estate tasting tour, Hebbe Falls jeep safari, Western Ghats road trip",
            "State": "Karnataka",
            "Country": "India",
            "Category": "Mountain/Hill",
            "Travel_Style": "Adventure, Trekking, Eco, Photography",
            "Best_Season": "September to May",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Kabini Tiger Reserve",
            "District": "Mysore",
            "Famous_For": "World-famous biodiversity hub on the Kabini River in Nagarhole National Park, known for black panthers, wild elephant herds and Royal Bengal tigers",
            "Activities": "Kabini river boat safari, Jungle jeep safari, Wildlife photography, Coracle rides on Kabini reservoir",
            "State": "Karnataka",
            "Country": "India",
            "Category": "Wildlife",
            "Travel_Style": "Wildlife, Adventure, Eco, Photography",
            "Best_Season": "October to May",
            "Budget_Category": "Luxury",
            "Duration_Days": 2,
        },
        # Tamil Nadu Region
        {
            "Name of the Place": "Mahabalipuram Shore Temple & Rathas",
            "District": "Chengalpattu",
            "Famous_For": "UNESCO World Heritage 7th-century coastal Pallava granite shrines, monolithic Pancha Rathas and Arjuna's Penance bas-relief",
            "Activities": "Shore Temple photography, Monolithic ratha exploration, Rock carving art study, Coastal seafood tasting",
            "State": "Tamil Nadu",
            "Country": "India",
            "Category": "Heritage",
            "Travel_Style": "Cultural, Heritage, Beach, Photography",
            "Best_Season": "October to March",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "DakshinaChitra",
            "District": "Chennai",
            "Famous_For": "Living heritage museum showcasing 18 authentic traditional heritage homes transported from Kerala, Tamil Nadu, Andhra Pradesh and Karnataka",
            "Activities": "Folk craft demonstrations, Traditional pottery making, South Indian architecture walk, Cultural workshops",
            "State": "Tamil Nadu",
            "Country": "India",
            "Category": "Heritage",
            "Travel_Style": "Cultural, Educational, Photography",
            "Best_Season": "November to February",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Madras Crocodile Bank",
            "District": "Chennai",
            "Famous_For": "Pioneering reptile conservation zoo housing over 2,400 reptiles including endangered mugger, saltwater crocodiles and gharials",
            "Activities": "Night safari, Crocodile feeding demonstrations, Venom extraction viewing, Educational conservation tour",
            "State": "Tamil Nadu",
            "Country": "India",
            "Category": "Wildlife",
            "Travel_Style": "Wildlife, Eco, Educational, Family",
            "Best_Season": "November to February",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Vedanthangal Bird Sanctuary",
            "District": "Chengalpattu",
            "Famous_For": "Oldest water bird sanctuary in India (1798), migratory winter breeding ground for 40,000 birds including pintails, pelicans and egrets",
            "Activities": "Tower birdwatching, Telephoto wildlife photography, Wetland nature walk, Lake sanctuary tour",
            "State": "Tamil Nadu",
            "Country": "India",
            "Category": "Wildlife",
            "Travel_Style": "Wildlife, Eco, Nature, Photography",
            "Best_Season": "November to February",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Pulicat Lake",
            "District": "Tiruvallur",
            "Famous_For": "Second largest brackish water lagoon in India, famous for annual winter flamingo festival and serene fishing hamlets",
            "Activities": "Flamingo watching boat rides, Dutch cemetery heritage walk, Lagoon bird photography, Lighthouse visit",
            "State": "Tamil Nadu",
            "Country": "India",
            "Category": "Lake/Water",
            "Travel_Style": "Wildlife, Eco, Boating, Photography",
            "Best_Season": "October to March",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Kanchipuram",
            "District": "Kanchipuram",
            "Famous_For": "City of a Thousand Temples and world-famed epicenter of pure mulberry silk Kanchipuram sarees, housing Kailasanathar and Ekambareswarar shrines",
            "Activities": "Ancient Dravidian temple darshan, Silk handloom weaving demonstration, Saree shopping, Architectural photography",
            "State": "Tamil Nadu",
            "Country": "India",
            "Category": "Temple/Religious",
            "Travel_Style": "Spiritual, Cultural, Heritage, Shopping",
            "Best_Season": "October to March",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Madurai Meenakshi Temple",
            "District": "Madurai",
            "Famous_For": "Legendary historic temple complex with 14 soaring sculptured gopurams and Hall of Thousand Pillars dedicated to Goddess Meenakshi and Lord Sundareswarar",
            "Activities": "Temple darshan, Evening night ceremony procession, Thousand Pillar Hall tour, Madurai Jigarthanda tasting",
            "State": "Tamil Nadu",
            "Country": "India",
            "Category": "Temple/Religious",
            "Travel_Style": "Spiritual, Cultural, Heritage, Photography",
            "Best_Season": "October to March",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Rameswaram Temple & Dhanushkodi",
            "District": "Ramanathapuram",
            "Famous_For": "Sacred Ramanathaswamy Temple featuring the world's longest corridor of sculpted granite pillars and the ghost town dunes of Dhanushkodi at Ram Setu",
            "Activities": "22 holy well water bath ritual, Pamban sea bridge viewing, Dhanushkodi ghost town 4x4 safari, Ram Setu beach walk",
            "State": "Tamil Nadu",
            "Country": "India",
            "Category": "Temple/Religious",
            "Travel_Style": "Spiritual, Cultural, Adventure, Photography",
            "Best_Season": "October to April",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Ooty & Nilgiri Toy Train",
            "District": "Nilgiris",
            "Famous_For": "Queen of Hill Stations connected by UNESCO World Heritage Nilgiri Mountain Railway rack-and-pinion steam toy train across 250 bridges",
            "Activities": "Heritage toy train ride, Doddabetta peak viewing, Botanical gardens walk, Homemade chocolate tasting, Pykara lake boating",
            "State": "Tamil Nadu",
            "Country": "India",
            "Category": "Mountain/Hill",
            "Travel_Style": "Eco, Leisure, Adventure, Photography",
            "Best_Season": "April to June",
            "Budget_Category": "Moderate",
            "Duration_Days": 3,
        },
        {
            "Name of the Place": "Kodaikanal Lake",
            "District": "Dindigul",
            "Famous_For": "Man-made star-shaped lake created in 1863 set amidst Palani Hills pine forests, Coaker's Walk and Pillar Rocks",
            "Activities": "Star lake pedal boating, Lakeside cycling, Coaker's Walk valley viewing, Pillar Rocks photography",
            "State": "Tamil Nadu",
            "Country": "India",
            "Category": "Lake/Water",
            "Travel_Style": "Eco, Leisure, Boating, Family",
            "Best_Season": "September to May",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Thanjavur Brihadeeswara Temple",
            "District": "Thanjavur",
            "Famous_For": "UNESCO World Heritage Great Living Chola temple built in 1010 CE by Raja Raja Chola I with a 216-foot vimana and 80-ton granite capstone",
            "Activities": "Vimana shadow exploration, Monolithic Nandi photography, Chola fresco study, Thanjavur doll and painting shopping",
            "State": "Tamil Nadu",
            "Country": "India",
            "Category": "Temple/Religious",
            "Travel_Style": "Cultural, Heritage, Spiritual, Photography",
            "Best_Season": "October to March",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Chettinad Heritage Mansions",
            "District": "Sivaganga",
            "Famous_For": "Palatial ancestral merchant mansions constructed with Italian marble, Burmese teak, Belgian glass and world-acclaimed Chettinad spicy cuisine",
            "Activities": "Palatial mansion architecture walk, Athangudi handmade tile factory visit, Traditional Chettinad banana leaf feast",
            "State": "Tamil Nadu",
            "Country": "India",
            "Category": "Heritage",
            "Travel_Style": "Cultural, Heritage, Culinary, Photography",
            "Best_Season": "October to March",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
        # Rajasthan
        {
            "Name of the Place": "Hawa Mahal",
            "District": "Jaipur",
            "Famous_For": "Palace of Winds constructed in 1799 with 953 honeycombed pink sandstone jharokha windows allowing royal women to observe street festivals",
            "Activities": "Jharokha window photography, Rooftop cafe view of palace, Wind corridor walk, Old Jaipur street shopping",
            "State": "Rajasthan",
            "Country": "India",
            "Category": "Heritage",
            "Travel_Style": "Cultural, Heritage, Photography",
            "Best_Season": "October to March",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Amber Fort",
            "District": "Jaipur",
            "Famous_For": "Majestic hilltop Rajput fortress overlooking Maota Lake, famous for Sheesh Mahal (Mirror Palace) reflecting single candle into thousands of stars",
            "Activities": "Sheesh Mahal mirror viewing, Elephant/jeep ride up ramparts, Evening sound and light show, Maota lake photography",
            "State": "Rajasthan",
            "Country": "India",
            "Category": "Heritage",
            "Travel_Style": "Cultural, Heritage, Photography",
            "Best_Season": "October to March",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Mehrangarh Fort (Jodhpur)",
            "District": "Jodhpur",
            "Famous_For": "Imposing 15th-century fortress rising 400 feet above the Blue City of Jodhpur, containing pearl palaces, armory and canon ramparts",
            "Activities": "Ziplining across fort moats (Flying Fox), Blue City panoramic photography, Royal museum tour, Folk music performances",
            "State": "Rajasthan",
            "Country": "India",
            "Category": "Heritage",
            "Travel_Style": "Cultural, Heritage, Adventure, Photography",
            "Best_Season": "October to March",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Udaipur City Palace",
            "District": "Udaipur",
            "Famous_For": "Magnificent royal palace complex sprawled on the banks of Lake Pichola, featuring peacock courtyards, crystal galleries and marble arches",
            "Activities": "Lake Pichola boat cruise to Jag Mandir, Crystal gallery tour, Sunset photography over palace ghats, Royal dining",
            "State": "Rajasthan",
            "Country": "India",
            "Category": "Heritage",
            "Travel_Style": "Cultural, Heritage, Luxury, Photography",
            "Best_Season": "October to March",
            "Budget_Category": "Luxury",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Jaisalmer Golden Fort",
            "District": "Jaisalmer",
            "Famous_For": "One of the world's very few living forts (Sonar Qila), built in yellow sandstone in the heart of Thar Desert housing a quarter of city's population",
            "Activities": "Living fort exploration, Jain temple carving study, Rooftop desert sunset dining, Havelis walking tour",
            "State": "Rajasthan",
            "Country": "India",
            "Category": "Heritage",
            "Travel_Style": "Cultural, Heritage, Adventure, Photography",
            "Best_Season": "October to March",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Sam Sand Dunes",
            "District": "Jaisalmer",
            "Famous_For": "Vast undulating sand dunes in the Thar Desert offering authentic Rajasthani camel safaris, starlit desert camps and Kalbelia folk dances",
            "Activities": "Desert jeep dune bashing, Sunset camel ride, Campfire Kalbelia dance show, Overnight desert luxury glamping",
            "State": "Rajasthan",
            "Country": "India",
            "Category": "Adventure",
            "Travel_Style": "Adventure, Cultural, Stargazing, Photography",
            "Best_Season": "October to March",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Ranthambore Tiger Reserve",
            "District": "Sawai Madhopur",
            "Famous_For": "Premier tiger sanctuary in Northern India where Royal Bengal tigers roam among 10th-century fort ruins and ancient banyan trees",
            "Activities": "Open-top Canter/Gypsy safari, Tiger spotting, Ranthambore Fort trek, Padam Talao crocodile viewing",
            "State": "Rajasthan",
            "Country": "India",
            "Category": "Wildlife",
            "Travel_Style": "Wildlife, Adventure, Photography",
            "Best_Season": "October to April",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Pushkar Lake",
            "District": "Ajmer",
            "Famous_For": "Sacred Hindu pilgrimage lake with 52 bathing ghats and the world's rare consecrated Jagatpita Brahma Mandir, host of the camel fair",
            "Activities": "Ghat evening Maha Aarti, Brahma temple darshan, Desert camel fair experience, Malpua sweet tasting",
            "State": "Rajasthan",
            "Country": "India",
            "Category": "Lake/Water",
            "Travel_Style": "Spiritual, Cultural, Photography",
            "Best_Season": "October to March",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        # Goa
        {
            "Name of the Place": "Basilica of Bom Jesus",
            "District": "North Goa",
            "Famous_For": "UNESCO World Heritage Baroque church in Old Goa holding the incorrupt mortal remains of Saint Francis Xavier in a silver casket",
            "Activities": "Sacred relic viewing, Baroque art study, Heritage church walk, Se Cathedral exploration nearby",
            "State": "Goa",
            "Country": "India",
            "Category": "Temple/Religious",
            "Travel_Style": "Cultural, Spiritual, Heritage, Photography",
            "Best_Season": "November to March",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Calangute Beach",
            "District": "North Goa",
            "Famous_For": "Queen of Beaches in Goa — lively sweeping sandy coastline teeming with coastal shacks, parasailing, jet-skis and nightlife",
            "Activities": "Parasailing, Jet skiing, Banana boat ride, Shacks dining with Goan fish curry, Beach shopping",
            "State": "Goa",
            "Country": "India",
            "Category": "Beach",
            "Travel_Style": "Beach, Adventure, Leisure, Family",
            "Best_Season": "November to March",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Fort Aguada",
            "District": "North Goa",
            "Famous_For": "17th-century Portuguese coastal fortress and lighthouse perched over Sinquerim Beach overlooking the confluence of Mandovi River and sea",
            "Activities": "Lighthouse photography, Fort rampart walking, Ocean sunset viewing, Portuguese history tour",
            "State": "Goa",
            "Country": "India",
            "Category": "Heritage",
            "Travel_Style": "Heritage, Beach, Cultural, Photography",
            "Best_Season": "November to March",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Palolem Beach",
            "District": "South Goa",
            "Famous_For": "Pristine crescent bay lined with leaning coconut palms, calm turquoise waters, kayak rentals and quiet beach huts",
            "Activities": "Kayaking to Butterfly Beach, Dolphin cruise, Sunset beach yoga, Silent noise headphone party",
            "State": "Goa",
            "Country": "India",
            "Category": "Beach",
            "Travel_Style": "Beach, Relaxation, Adventure, Photography",
            "Best_Season": "November to March",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Dudhsagar Falls",
            "District": "South Goa",
            "Famous_For": "Majestic four-tiered Sea of Milk cascade plunging 1,017 feet through the Western Ghats jungle on the Goa-Karnataka border",
            "Activities": "Jeep jungle safari across streams, Waterfall plunge pool swimming, Railway bridge photography, Trekking",
            "State": "Goa",
            "Country": "India",
            "Category": "Waterfall",
            "Travel_Style": "Adventure, Eco, Nature, Photography",
            "Best_Season": "October to May",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        # Uttarakhand & Himachal
        {
            "Name of the Place": "Rishikesh",
            "District": "Dehradun",
            "Famous_For": "Yoga Capital of the World on the holy Ganges, famous for Ram Jhula, white water river rafting, and evening Triveni Ghat Ganga Aarti",
            "Activities": "Ganga white water rafting, Bungee jumping, Yoga and meditation retreat, Evening Ganga Aarti, Beatles Ashram tour",
            "State": "Uttarakhand",
            "Country": "India",
            "Category": "Adventure",
            "Travel_Style": "Adventure, Spiritual, Cultural, Photography",
            "Best_Season": "September to May",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Haridwar",
            "District": "Haridwar",
            "Famous_For": "Ancient holy pilgrimage city where the Ganges leaves the Himalayas, world-famous for Har Ki Pauri ghat and thousands of floating diyas",
            "Activities": "Har Ki Pauri holy dip, Evening Maha Ganga Aarti, Mansa Devi ropeway cable car, Chandi Devi temple visit",
            "State": "Uttarakhand",
            "Country": "India",
            "Category": "Temple/Religious",
            "Travel_Style": "Spiritual, Cultural, Photography",
            "Best_Season": "October to March",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Valley of Flowers",
            "District": "Chamoli",
            "Famous_For": "UNESCO World Heritage high-altitude Himalayan national park blanketed in over 500 varieties of wild alpine flowers against snow peaks",
            "Activities": "Alpine valley trekking, Botanical photography, Hemkund Sahib pilgrimage trek, Rare Himalayan flora study",
            "State": "Uttarakhand",
            "Country": "India",
            "Category": "Mountain/Hill",
            "Travel_Style": "Adventure, Trekking, Eco, Photography",
            "Best_Season": "July to September",
            "Budget_Category": "Moderate",
            "Duration_Days": 3,
        },
        {
            "Name of the Place": "Jim Corbett",
            "District": "Nainital",
            "Famous_For": "Oldest national park in India established in 1936, world-renowned for Royal Bengal tiger conservation along the Ramganga River",
            "Activities": "Dhikala zone open jeep safari, Elephant interaction, Ramganga river birdwatching, Jungle lodge stay",
            "State": "Uttarakhand",
            "Country": "India",
            "Category": "Wildlife",
            "Travel_Style": "Wildlife, Adventure, Nature, Photography",
            "Best_Season": "November to June",
            "Budget_Category": "Luxury",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Nainital",
            "District": "Nainital",
            "Famous_For": "Scenic lake city nestled around the eye-shaped emerald Naini Lake, overlooked by snow-capped peaks and the Mall Road promenade",
            "Activities": "Yacht and paddle boating on Naini Lake, Naina Devi temple darshan, Snow View ropeway cable car, Mall Road shopping",
            "State": "Uttarakhand",
            "Country": "India",
            "Category": "Mountain/Hill",
            "Travel_Style": "Leisure, Eco, Boating, Family",
            "Best_Season": "March to June",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Mussoorie",
            "District": "Dehradun",
            "Famous_For": "Queen of the Hills in Garhwal Himalayas offering stunning Doon Valley panoramas, Gun Hill viewpoints and cascading Kempty Falls",
            "Activities": "Kempty Falls bathing, Gun Hill cable car ride, Camel's Back road stroll, Mall Road shopping and cafe hopping",
            "State": "Uttarakhand",
            "Country": "India",
            "Category": "Mountain/Hill",
            "Travel_Style": "Leisure, Nature, Photography, Family",
            "Best_Season": "April to June",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Auli Ski Resort",
            "District": "Chamoli",
            "Famous_For": "Premier winter skiing destination in India with powdery snow slopes, 4km cable car ropeway and 360-degree views of Nanda Devi peak",
            "Activities": "Snow skiing lessons, Asia's longest ropeway cable car, Snowboard riding, Nanda Devi mountain photography",
            "State": "Uttarakhand",
            "Country": "India",
            "Category": "Mountain/Hill",
            "Travel_Style": "Adventure, Winter Sports, Nature, Photography",
            "Best_Season": "December to March",
            "Budget_Category": "Luxury",
            "Duration_Days": 3,
        },
        {
            "Name of the Place": "Kedarnath",
            "District": "Rudraprayag",
            "Famous_For": "Highest of the 12 Jyotirlingas of Lord Shiva (3,584m) in the Garhwal Himalayas near the Mandakini River source and Chorabari Glacier",
            "Activities": "Chardham pilgrimage trek, Shiva Jyotirlinga darshan, Himalayan glacier photography, Helicopter darshan service",
            "State": "Uttarakhand",
            "Country": "India",
            "Category": "Temple/Religious",
            "Travel_Style": "Spiritual, Trekking, Adventure, Heritage",
            "Best_Season": "May to October",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Badrinath",
            "District": "Chamoli",
            "Famous_For": "Sacred shrine dedicated to Lord Badri (Vishnu) situated between Nar and Narayana mountain ranges, famous for Tapt Kund hot sulphur springs",
            "Activities": "Badri Vishal darshan, Tapt Kund natural hot spring bath, Mana last Indian village visit, Neelkanth peak photography",
            "State": "Uttarakhand",
            "Country": "India",
            "Category": "Temple/Religious",
            "Travel_Style": "Spiritual, Cultural, Nature, Heritage",
            "Best_Season": "May to October",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Shimla",
            "District": "Shimla",
            "Famous_For": "Former British summer capital of India perched on pine-forested ridges, famous for The Ridge, Christ Church and UNESCO Kalka-Shimla toy train",
            "Activities": "Heritage toy train ride, The Ridge and Mall Road walking, Jakhu Hanuman temple trek, British colonial architecture tour",
            "State": "Himachal Pradesh",
            "Country": "India",
            "Category": "Mountain/Hill",
            "Travel_Style": "Heritage, Leisure, Eco, Photography",
            "Best_Season": "March to June",
            "Budget_Category": "Moderate",
            "Duration_Days": 3,
        },
        {
            "Name of the Place": "Dharamshala/McLeod Ganj",
            "District": "Kangra",
            "Famous_For": "Little Lhasa of India, exile residence of His Holiness the 14th Dalai Lama and headquarters of Central Tibetan Administration beneath Dhauladhar peaks",
            "Activities": "Tsuglagkhang Dalai Lama temple visit, Triund mountain trek, Tibetan handicrafts shopping, Bhagsu waterfall hike",
            "State": "Himachal Pradesh",
            "Country": "India",
            "Category": "Mountain/Hill",
            "Travel_Style": "Spiritual, Cultural, Trekking, Photography",
            "Best_Season": "March to June",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Kasol",
            "District": "Kullu",
            "Famous_For": "Hippie paradise nestled along the Parvati River, renowned for Israeli cafes, coniferous pinewood trails and gateway to Kheerganga trek",
            "Activities": "Parvati riverbank stroll, Kheerganga hot water spring trek, Tosh and Malana village hike, Israeli cuisine tasting",
            "State": "Himachal Pradesh",
            "Country": "India",
            "Category": "Mountain/Hill",
            "Travel_Style": "Adventure, Trekking, Leisure, Bohemian",
            "Best_Season": "April to October",
            "Budget_Category": "Budget",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Spiti Valley",
            "District": "Lahaul and Spiti",
            "Famous_For": "High-altitude cold desert valley featuring 1,000-year-old Key Monastery, Chandratal Lake, fossil villages and moonscapes",
            "Activities": "Key Gompa monastery visit, Chandratal camping under Milky Way, Pin Valley national park safari, Highest post office Hikkim visit",
            "State": "Himachal Pradesh",
            "Country": "India",
            "Category": "Mountain/Hill",
            "Travel_Style": "Adventure, Stargazing, Cultural, Photography",
            "Best_Season": "June to October",
            "Budget_Category": "Moderate",
            "Duration_Days": 4,
        },
        {
            "Name of the Place": "Dalhousie/Khajjiar",
            "District": "Chamba",
            "Famous_For": "Mini Switzerland of India — saucer-shaped lush meadow surrounded by dense deodar pine forests and a floating weed lake",
            "Activities": "Khajjiar meadow zorbing, Horseback riding, Kalatop wildlife sanctuary walk, Panchpula stream photography",
            "State": "Himachal Pradesh",
            "Country": "India",
            "Category": "Mountain/Hill",
            "Travel_Style": "Eco, Leisure, Adventure, Family",
            "Best_Season": "March to June",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
        # J&K & Ladakh
        {
            "Name of the Place": "Dal Lake Shikara",
            "District": "Srinagar",
            "Famous_For": "Jewel in the crown of Kashmir — floating gardens, carved cedarwood houseboats and traditional Shikara boat rides against Zabarwan hills",
            "Activities": "Sunrise floating vegetable market Shikara tour, Luxury houseboat stay, Char Chinar photography, Mughal garden visit",
            "State": "Jammu & Kashmir",
            "Country": "India",
            "Category": "Lake/Water",
            "Travel_Style": "Leisure, Cultural, Boating, Photography",
            "Best_Season": "April to October",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Gulmarg Gondola",
            "District": "Baramulla",
            "Famous_For": "Meadow of Flowers home to the world's second-highest operating cable car (Gulmarg Gondola to 3,980m Apharwat peak) and premier ski resort",
            "Activities": "Phase 2 Gondola ride, Winter snow skiing, Summer golf course playing, Apharwat peak snow photography",
            "State": "Jammu & Kashmir",
            "Country": "India",
            "Category": "Mountain/Hill",
            "Travel_Style": "Adventure, Winter Sports, Nature, Photography",
            "Best_Season": "December to April",
            "Budget_Category": "Luxury",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Pangong Tso",
            "District": "Leh",
            "Famous_For": "World-famous endorheic high-altitude saltwater lake (4,250m) shifting through turquoise, deep blue and emerald shades across India and Tibet",
            "Activities": "Color-changing lake photography, Stargazing over 3 Idiots point, Lakeshore camp stay, Chang La pass crossing",
            "State": "Ladakh",
            "Country": "India",
            "Category": "Lake/Water",
            "Travel_Style": "Adventure, Stargazing, Nature, Photography",
            "Best_Season": "May to September",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Leh Palace & Shanti Stupa",
            "District": "Leh",
            "Famous_For": "17th-century Tibetan royal palace overlooking Leh city and the white-domed Buddhist Shanti Stupa providing 360-degree Karakoram mountain views",
            "Activities": "Sunrise meditation at Shanti Stupa, Royal palace museum tour, Leh market pashmina shopping, Mountain photography",
            "State": "Ladakh",
            "Country": "India",
            "Category": "Heritage",
            "Travel_Style": "Spiritual, Heritage, Cultural, Photography",
            "Best_Season": "May to September",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Nubra Valley",
            "District": "Leh",
            "Famous_For": "Valley of Flowers in Ladakh reached via Khardung La (5,359m), renowned for cold desert white sand dunes and double-humped Bactrian camels",
            "Activities": "Bactrian double-humped camel safari, Diskit monastery Maitreya Buddha viewing, Khardung La pass selfie, Stargazing",
            "State": "Ladakh",
            "Country": "India",
            "Category": "Mountain/Hill",
            "Travel_Style": "Adventure, Nature, Cultural, Photography",
            "Best_Season": "May to September",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
        # Northeast India
        {
            "Name of the Place": "Shillong Peak",
            "District": "East Khasi Hills",
            "Famous_For": "Highest point in Meghalaya (1,965m) offering breathtaking aerial panoramas of the Scotland of the East and Bangladesh plains",
            "Activities": "Telescope panoramic viewing, Khasi traditional dress photography, Ward's Lake boating nearby, Air Force museum tour",
            "State": "Meghalaya",
            "Country": "India",
            "Category": "Mountain/Hill",
            "Travel_Style": "Nature, Leisure, Photography",
            "Best_Season": "October to April",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Cherrapunji",
            "District": "East Khasi Hills",
            "Famous_For": "One of the wettest places on Earth, home to Nohkalikai Falls (tallest plunge waterfall in India at 1,115 ft) and Mawsmai limestone caves",
            "Activities": "Nohkalikai falls viewpoint visit, Mawsmai cave exploration, Seven Sisters waterfall photography, Eco park walk",
            "State": "Meghalaya",
            "Country": "India",
            "Category": "Waterfall",
            "Travel_Style": "Eco, Adventure, Nature, Photography",
            "Best_Season": "October to May",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Nongriat Living Root Bridges",
            "District": "East Khasi Hills",
            "Famous_For": "Ingenious bio-engineered wonders trained over centuries from living Ficus elastica tree roots by Khasi tribes, including the Umshiang Double Decker Bridge",
            "Activities": "3,000-step rainforest trek to Double Decker bridge, Natural turquoise pool swimming, Rainbow falls hike",
            "State": "Meghalaya",
            "Country": "India",
            "Category": "Garden/Nature",
            "Travel_Style": "Adventure, Trekking, Eco, Photography",
            "Best_Season": "October to April",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Tsomgo Lake",
            "District": "East Sikkim",
            "Famous_For": "Glacial high-altitude alpine lake (3,753m) in Sikkim that remains frozen in winter, revered as holy by lamas and gateway to Nathula Pass",
            "Activities": "Yak riding on snow, Nathula Pass China border visit, Baba Harbhajan Singh temple darshan, Alpine snow photography",
            "State": "Sikkim",
            "Country": "India",
            "Category": "Lake/Water",
            "Travel_Style": "Adventure, Nature, Cultural, Photography",
            "Best_Season": "March to May",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Rumtek Monastery",
            "District": "East Sikkim",
            "Famous_For": "Largest monastery in Sikkim and seat of the Karma Kagyu lineage, featuring exquisite Tibetan murals, golden stupa and sacred thangkas",
            "Activities": "Tibetan monastery tour, Golden stupa viewing, Monk prayer chanting attendance, Sacred thangka photography",
            "State": "Sikkim",
            "Country": "India",
            "Category": "Temple/Religious",
            "Travel_Style": "Spiritual, Cultural, Heritage, Photography",
            "Best_Season": "October to May",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Kaziranga Rhino Safari",
            "District": "Golaghat",
            "Famous_For": "UNESCO World Heritage wildlife sanctuary hosting two-thirds of the world's great one-horned rhinoceros population in Brahmaputra floodplains",
            "Activities": "Central Kohora zone jeep safari, Morning elephant grass safari, Rhino sighting photography, Orchid park tour",
            "State": "Assam",
            "Country": "India",
            "Category": "Wildlife",
            "Travel_Style": "Wildlife, Adventure, Nature, Photography",
            "Best_Season": "November to April",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Majuli Island",
            "District": "Majuli",
            "Famous_For": "World's largest river island nestled in the Brahmaputra River, epicenter of Neo-Vaishnavite culture and ancient Satra monastic masks",
            "Activities": "Satra monastic mask making workshop, River ferry cruise, Mishing tribal village visit, Sunset over Brahmaputra",
            "State": "Assam",
            "Country": "India",
            "Category": "Island",
            "Travel_Style": "Cultural, Eco, Island, Photography",
            "Best_Season": "October to March",
            "Budget_Category": "Budget",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Ziro Valley",
            "District": "Lower Subansiri",
            "Famous_For": "UNESCO tentative heritage valley inhabited by the Apatani tribe, celebrated for sustainable wet paddy fish farming and Ziro Music Festival",
            "Activities": "Apatani tribal village cultural tour, Pine grove trek, Ziro music festival attendance, Paddy landscape photography",
            "State": "Arunachal Pradesh",
            "Country": "India",
            "Category": "Mountain/Hill",
            "Travel_Style": "Cultural, Eco, Music, Photography",
            "Best_Season": "September to May",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
        # Other Key Indian States
        {
            "Name of the Place": "Taj Mahal",
            "District": "Agra",
            "Famous_For": "UNESCO World Wonder and ultimate monument of eternal love, built in pure white Makrana marble by Mughal Emperor Shah Jahan for Mumtaz Mahal",
            "Activities": "Sunrise marble monument photography, Guided Mughal history walk, Mehtab Bagh sunset viewing across Yamuna, Agra Petha tasting",
            "State": "Uttar Pradesh",
            "Country": "India",
            "Category": "Heritage",
            "Travel_Style": "Cultural, Heritage, Romance, Photography",
            "Best_Season": "October to March",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Varanasi Ghats",
            "District": "Varanasi",
            "Famous_For": "Oldest continuously inhabited city in the world, renowned for 84 sacred stone ghats, Dashashwamedh evening Ganga Aarti and spiritual rituals",
            "Activities": "Dawn boat ride on the Ganges, Dashashwamedh evening Ganga Aarti, Ghat heritage walk, Banarasi silk saree shopping",
            "State": "Uttar Pradesh",
            "Country": "India",
            "Category": "Temple/Religious",
            "Travel_Style": "Spiritual, Cultural, Heritage, Photography",
            "Best_Season": "October to March",
            "Budget_Category": "Budget",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Kashi Vishwanath",
            "District": "Varanasi",
            "Famous_For": "One of the twelve supreme Jyotirlingas of Lord Shiva standing on the western bank of holy Ganga, newly transformed with the Kashi Vishwanath Corridor",
            "Activities": "Jyotirlinga darshan, Ganga snan holy dip, Temple corridor photography, Banarasi paan tasting",
            "State": "Uttar Pradesh",
            "Country": "India",
            "Category": "Temple/Religious",
            "Travel_Style": "Spiritual, Cultural, Heritage",
            "Best_Season": "October to March",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Ayodhya Ram Mandir",
            "District": "Ayodhya",
            "Famous_For": "Grand Nagara-style pink Bansi Paharpur sandstone temple complex built at Shri Ram Janmabhoomi on the banks of holy Sarayu River",
            "Activities": "Ram Lalla darshan, Sarayu river evening Maha Aarti, Ram Janmabhoomi corridor tour, Cultural spiritual photography",
            "State": "Uttar Pradesh",
            "Country": "India",
            "Category": "Temple/Religious",
            "Travel_Style": "Spiritual, Cultural, Heritage, Photography",
            "Best_Season": "October to March",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Statue of Unity",
            "District": "Narmada",
            "Famous_For": "World's tallest monument (182 meters) dedicated to the Iron Man of India Sardar Vallabhbhai Patel, overlooking Sardar Sarovar Dam",
            "Activities": "153-meter high chest viewing gallery elevator, Light and sound laser show, Valley of Flowers walk, Dam cruise",
            "State": "Gujarat",
            "Country": "India",
            "Category": "Heritage",
            "Travel_Style": "Heritage, Modern, Family, Photography",
            "Best_Season": "October to March",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Rann of Kutch",
            "District": "Kutch",
            "Famous_For": "World's largest salt marsh desert glittering pure white, host of the vibrant Rann Utsav cultural festival under moonlit skies",
            "Activities": "Full moon salt desert photography, Rann Utsav cultural dance viewing, Rogan art craft workshop, Desert paramotoring",
            "State": "Gujarat",
            "Country": "India",
            "Category": "Garden/Nature",
            "Travel_Style": "Cultural, Nature, Festival, Photography",
            "Best_Season": "November to February",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Somnath",
            "District": "Gir Somnath",
            "Famous_For": "First among the twelve holy Jyotirlinga shrines of Lord Shiva, rebuilt on the shores of Arabian Sea where no land lies between it and Antarctica",
            "Activities": "Jyotirlinga morning darshan, Evening sound and light laser show, Sea breeze promenade walk, Spiritual prayers",
            "State": "Gujarat",
            "Country": "India",
            "Category": "Temple/Religious",
            "Travel_Style": "Spiritual, Cultural, Beach, Heritage",
            "Best_Season": "October to March",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Gir Lions",
            "District": "Junagadh",
            "Famous_For": "Only natural habitat in the world for the endangered Asiatic Lion (Panthera leo leo) roaming across dry deciduous teak forests",
            "Activities": "Open jeep lion safari in Devalia zone, Asiatic lion sighting photography, Maldhari tribal hamlet visit",
            "State": "Gujarat",
            "Country": "India",
            "Category": "Wildlife",
            "Travel_Style": "Wildlife, Adventure, Nature, Photography",
            "Best_Season": "December to March",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Ajanta & Ellora Caves",
            "District": "Aurangabad",
            "Famous_For": "UNESCO World Heritage masterworks — Ajanta's ancient Buddhist fresco murals and Ellora's monolithic Kailash Temple carved from single rock",
            "Activities": "Kailash monolithic temple study, Buddhist fresco photography, Ancient cave meditation, Architectural tour",
            "State": "Maharashtra",
            "Country": "India",
            "Category": "Cave/Geological",
            "Travel_Style": "Heritage, Cultural, Educational, Photography",
            "Best_Season": "October to March",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Shirdi Sai Baba",
            "District": "Ahmednagar",
            "Famous_For": "Revered spiritual pilgrimage center housing the Samadhi Temple of 19th-century saint Sai Baba of Shirdi, preaching universal harmony",
            "Activities": "Samadhi Mandir darshan, Kakad Aarti attendance, Dwarkamai and Chavadi pilgrimage walk, Maha Prasad distribution",
            "State": "Maharashtra",
            "Country": "India",
            "Category": "Temple/Religious",
            "Travel_Style": "Spiritual, Cultural, Pilgrimage",
            "Best_Season": "October to March",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Golden Temple (Amritsar)",
            "District": "Amritsar",
            "Famous_For": "Sri Harmandir Sahib — holiest Gurdwara of Sikhism gilded with 500kg of gold leaf, surrounded by the holy Amrit Sarovar lake and mega Langar",
            "Activities": "Golden sanctum darshan, Holy sarovar parikrama, Guru ka Langar volunteer service, Palki Sahib night ceremony",
            "State": "Punjab",
            "Country": "India",
            "Category": "Temple/Religious",
            "Travel_Style": "Spiritual, Cultural, Heritage, Photography",
            "Best_Season": "October to March",
            "Budget_Category": "Budget",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Wagah Border",
            "District": "Amritsar",
            "Famous_For": "Grand international border ceremony between India and Pakistan featuring synchronized goose-stepping military drill and patriotic flag lowering",
            "Activities": "Beating retreat military ceremony viewing, Patriotic song celebrations, Border gate photography, Amritsari kulcha dining",
            "State": "Punjab",
            "Country": "India",
            "Category": "Heritage",
            "Travel_Style": "Cultural, Patriotic, Photography",
            "Best_Season": "October to March",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Puri Jagannath",
            "District": "Puri",
            "Famous_For": "12th-century Char Dham pilgrimage shrine dedicated to Lord Jagannath, Balabhadra and Subhadra, world-renowned for the monumental Ratha Yatra",
            "Activities": "Jagannath temple darshan, Golden beach strolling, Anandabazar Mahaprasad dining, Konark Marine Drive drive",
            "State": "Odisha",
            "Country": "India",
            "Category": "Temple/Religious",
            "Travel_Style": "Spiritual, Cultural, Beach, Heritage",
            "Best_Season": "October to March",
            "Budget_Category": "Budget",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Konark Sun Temple",
            "District": "Puri",
            "Famous_For": "13th-century UNESCO World Heritage stone masterpiece carved as a colossal 24-wheeled chariot of Sun God Surya pulled by seven horses",
            "Activities": "Sundial wheel time-reading study, Kalinga stone carving photography, Konark dance festival viewing, Chandrabhaga beach walk",
            "State": "Odisha",
            "Country": "India",
            "Category": "Heritage",
            "Travel_Style": "Heritage, Cultural, Educational, Photography",
            "Best_Season": "October to March",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Darjeeling",
            "District": "Darjeeling",
            "Famous_For": "Queen of the Himalayas famed for world-renowned Muscatel tea estates, Tiger Hill sunrise over Mount Kanchenjunga and UNESCO Toy Train",
            "Activities": "Tiger Hill sunrise viewing over Kanchenjunga, UNESCO toy train joyride, Happy Valley tea tasting tour, Mall Road walk",
            "State": "West Bengal",
            "Country": "India",
            "Category": "Mountain/Hill",
            "Travel_Style": "Eco, Heritage, Leisure, Photography",
            "Best_Season": "March to May",
            "Budget_Category": "Moderate",
            "Duration_Days": 3,
        },
        {
            "Name of the Place": "Sundarbans",
            "District": "South 24 Parganas",
            "Famous_For": "World's largest contiguous mangrove delta at confluence of Ganga, Brahmaputra and Meghna rivers, home to swimming Royal Bengal tigers",
            "Activities": "Mangrove delta boat cruise, Royal Bengal tiger spotting, Estuarine crocodile viewing, Canopy watchtower climb",
            "State": "West Bengal",
            "Country": "India",
            "Category": "Wildlife",
            "Travel_Style": "Wildlife, Eco, Adventure, Photography",
            "Best_Season": "November to February",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Bodh Gaya",
            "District": "Gaya",
            "Famous_For": "Holiest pilgrimage site of Buddhism where Prince Siddhartha attained supreme enlightenment under the sacred Bodhi Tree around 500 BCE",
            "Activities": "Mahabodhi Temple meditation, Sacred Bodhi Tree circumambulation, 80-foot Great Buddha statue visit, Monastic tours",
            "State": "Bihar",
            "Country": "India",
            "Category": "Temple/Religious",
            "Travel_Style": "Spiritual, Cultural, Heritage, Educational",
            "Best_Season": "October to March",
            "Budget_Category": "Budget",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Tirupati Balaji",
            "District": "Tirupati",
            "Famous_For": "Venkateswara Temple atop the sacred Seven Hills of Tirumala, the world's most visited Hindu pilgrimage shrine renowned for Laddu prasadam",
            "Activities": "Tirumala Balaji darshan, Alipiri footstep trekking, Kalyana Katta hair offering, Sacred Laddu prasadam collection",
            "State": "Andhra Pradesh",
            "Country": "India",
            "Category": "Temple/Religious",
            "Travel_Style": "Spiritual, Cultural, Pilgrimage",
            "Best_Season": "September to February",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Araku Valley",
            "District": "Visakhapatnam",
            "Famous_For": "Picturesque hill station in the Eastern Ghats renowned for indigenous organic tribal coffee, Borra Caves stalactites and Katiki Waterfalls",
            "Activities": "Borra Caves million-year stalactite tour, Araku organic coffee museum and tasting, Katiki waterfall trek, Tribal dance viewing",
            "State": "Andhra Pradesh",
            "Country": "India",
            "Category": "Mountain/Hill",
            "Travel_Style": "Eco, Nature, Adventure, Cultural",
            "Best_Season": "October to March",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
        # 19 International Countries
        # France
        {
            "Name of the Place": "Eiffel Tower",
            "District": "Paris",
            "Famous_For": "Global cultural icon of France and architectural triumph designed by Gustave Eiffel, offering panoramic vistas of Paris from 300m",
            "Activities": "Summit observation deck viewing, Champ de Mars lawn picnic, Night sparkling light show photography, Seine river cruise nearby",
            "State": "Île-de-France",
            "Country": "France",
            "Category": "Heritage",
            "Travel_Style": "Cultural, Heritage, Romance, Photography",
            "Best_Season": "April to October",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Louvre Museum",
            "District": "Paris",
            "Famous_For": "World's most visited museum and historic royal palace housing over 35,000 masterpieces including Leonardo da Vinci's Mona Lisa and Venus de Milo",
            "Activities": "Mona Lisa viewing, Glass Pyramid photography, Greek and Roman antiquity study, Napoleonic state apartment tour",
            "State": "Île-de-France",
            "Country": "France",
            "Category": "Heritage",
            "Travel_Style": "Cultural, Educational, Photography",
            "Best_Season": "April to October",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Palace of Versailles",
            "District": "Versailles",
            "Famous_For": "Opulent principal royal residence of France under King Louis XIV, famous for the Hall of Mirrors, Grand Trianon and 2,000-acre manicured gardens",
            "Activities": "Hall of Mirrors guided tour, Musical fountains show in gardens, Marie Antoinette estate visit, Royal history photography",
            "State": "Île-de-France",
            "Country": "France",
            "Category": "Heritage",
            "Travel_Style": "Cultural, Heritage, Luxury, Photography",
            "Best_Season": "April to October",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Mont Saint-Michel",
            "District": "Normandy",
            "Famous_For": "UNESCO World Heritage tidal island commune crowned by a medieval Gothic Benedictine abbey rising dramatically from vast coastal sand flats",
            "Activities": "Abbey rampart climbing, Tidal bay walking with guide, Medieval cobblestone street exploration, Omelette tasting",
            "State": "Manche",
            "Country": "France",
            "Category": "Heritage",
            "Travel_Style": "Heritage, Cultural, Coastal, Photography",
            "Best_Season": "May to October",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        # Japan
        {
            "Name of the Place": "Senso-ji Temple",
            "District": "Tokyo",
            "Famous_For": "Tokyo's oldest and most sacred Buddhist temple founded in 628 CE, entered through the monumental Kaminarimon Thunder Gate and Nakamise-dori",
            "Activities": "Kaminarimon gate photography, Nakamise-dori street food and souvenir shopping, Incense smoke blessing, Temple courtyard stroll",
            "State": "Kanto",
            "Country": "Japan",
            "Category": "Temple/Religious",
            "Travel_Style": "Spiritual, Cultural, Heritage, Photography",
            "Best_Season": "March to May",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Mount Fuji",
            "District": "Fujinomiya",
            "Famous_For": "Japan's sacred active stratovolcano (3,776m) and UNESCO cultural icon, revered for symmetrical snow-capped cone and reflection in Fuji Five Lakes",
            "Activities": "Summer summit climbing, Lake Kawaguchiko scenic photography, Chureito Pagoda cherry blossom viewpoint, Fuji 5th station visit",
            "State": "Shizuoka",
            "Country": "Japan",
            "Category": "Mountain/Hill",
            "Travel_Style": "Adventure, Nature, Trekking, Photography",
            "Best_Season": "July to September",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Arashiyama Bamboo Grove",
            "District": "Kyoto",
            "Famous_For": "Soaring emerald bamboo forest pathway in Kyoto where the rustling wind through stalks is designated one of Japan's 100 Soundscapes",
            "Activities": "Bamboo forest walking, Tenryu-ji zen temple garden tour, Togetsukyo bridge stroll, Traditional rickshaw ride",
            "State": "Kansai",
            "Country": "Japan",
            "Category": "Garden/Nature",
            "Travel_Style": "Eco, Nature, Cultural, Photography",
            "Best_Season": "April to May",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Fushimi Inari Shrine",
            "District": "Kyoto",
            "Famous_For": "Principal Shinto shrine of Inari with over 10,000 vibrant vermilion Torii gates (Senbon Torii) winding through sacred mountain forest",
            "Activities": "Torii gate corridor hiking, Fox kitsune statue photography, Mountain summit sunset overlook, Souvenir wooden torii buying",
            "State": "Kansai",
            "Country": "Japan",
            "Category": "Temple/Religious",
            "Travel_Style": "Spiritual, Cultural, Hiking, Photography",
            "Best_Season": "March to May",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Hiroshima Peace Memorial",
            "District": "Hiroshima",
            "Famous_For": "Genbaku Dome (A-Bomb Dome) preserved exactly as it survived the world's first atomic bombing in 1945, standing as eternal beacon of global peace",
            "Activities": "Peace memorial park walk, Museum exhibit viewing, Children's peace monument origami cranes, Cenotaph reflection",
            "State": "Chugoku",
            "Country": "Japan",
            "Category": "Heritage",
            "Travel_Style": "Cultural, Educational, Historical, Photography",
            "Best_Season": "March to May",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        # UAE
        {
            "Name of the Place": "Burj Khalifa",
            "District": "Dubai",
            "Famous_For": "World's tallest skyscraper standing at 828 meters (2,717 feet) with 163 floors, featuring high-speed elevators and 360-degree observation decks",
            "Activities": "124th and 148th floor At The Top observation viewing, Dubai fountain show from above, Sunset skyline photography, Atmosphere dining",
            "State": "Dubai",
            "Country": "UAE",
            "Category": "Heritage",
            "Travel_Style": "Modern, Luxury, Sightseeing, Photography",
            "Best_Season": "November to March",
            "Budget_Category": "Luxury",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "The Dubai Mall & Fountain",
            "District": "Dubai",
            "Famous_For": "World's largest shopping and entertainment destination, featuring choreographed Dubai Fountain shows, giant indoor aquarium and ice rink",
            "Activities": "Choreographed musical fountain viewing, Dubai aquarium underwater tunnel walk, Luxury shopping, Souk Al Bahar promenade stroll",
            "State": "Dubai",
            "Country": "UAE",
            "Category": "Shopping",
            "Travel_Style": "Shopping, Entertainment, Family, Modern",
            "Best_Season": "November to March",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Palm Jumeirah",
            "District": "Dubai",
            "Famous_For": "Engineering marvel palm tree-shaped artificial archipelago in the Arabian Gulf, home to luxury resorts like Atlantis The Palm and Aquaventure",
            "Activities": "The View at The Palm observation deck, Aquaventure waterpark rides, Monorail scenic ride, Marina luxury yacht cruise",
            "State": "Dubai",
            "Country": "UAE",
            "Category": "Island",
            "Travel_Style": "Luxury, Island, Beach, Modern",
            "Best_Season": "November to March",
            "Budget_Category": "Luxury",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Burj Al Arab",
            "District": "Dubai",
            "Famous_For": "World's only self-proclaimed 7-star sail-shaped luxury hotel perched on a private island, featuring duplex suites and gold-leaf interiors",
            "Activities": "Inside Burj Al Arab guided tour, High afternoon tea at Skyview Lounge, Jumeirah beach photography, Al Mahara aquarium dining",
            "State": "Dubai",
            "Country": "UAE",
            "Category": "Heritage",
            "Travel_Style": "Luxury, Architecture, Modern, Photography",
            "Best_Season": "November to March",
            "Budget_Category": "Luxury",
            "Duration_Days": 1,
        },
        # Singapore
        {
            "Name of the Place": "Marina Bay Sands",
            "District": "Singapore",
            "Famous_For": "Architectural icon featuring three cascading 55-story hotel towers crowned by a cantilevered SkyPark and 150-meter rooftop infinity pool",
            "Activities": "SkyPark observation deck viewing, Rooftop infinity pool photography, Spectra light and water show, Shoppes luxury retail",
            "State": "Central Region",
            "Country": "Singapore",
            "Category": "Heritage",
            "Travel_Style": "Modern, Luxury, Sightseeing, Photography",
            "Best_Season": "Year-round",
            "Budget_Category": "Luxury",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Gardens by the Bay",
            "District": "Singapore",
            "Famous_For": "Futuristic 250-acre botanical wonderland featuring 50-meter vertical Supertrees, Cloud Forest misty mountain and Flower Dome greenhouse",
            "Activities": "OCBC Skyway canopy walk, Cloud Forest waterfall viewing, Garden Rhapsody evening light and sound show, Flower Dome photography",
            "State": "Central Region",
            "Country": "Singapore",
            "Category": "Garden/Nature",
            "Travel_Style": "Eco, Modern, Nature, Family, Photography",
            "Best_Season": "Year-round",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Universal Studios Singapore",
            "District": "Sentosa",
            "Famous_For": "Southeast Asia's only Universal Studios theme park featuring 24 cutting-edge rides and shows across 7 movie-themed immersive zones",
            "Activities": "Battlestar Galactica roller coaster, Transformers 3D ride, Jurassic Park river rapids, Meet and greet character photo ops",
            "State": "Central Region",
            "Country": "Singapore",
            "Category": "Theme Park",
            "Travel_Style": "Adventure, Theme Park, Family, Entertainment",
            "Best_Season": "Year-round",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Sentosa Island",
            "District": "Sentosa",
            "Famous_For": "Singapore's premier island resort getaway offering Siloso and Palawan tropical beaches, S.E.A. Aquarium and cable car skyline links",
            "Activities": "Siloso beach relaxation, S.E.A. Aquarium marine life walk, Skyline luge ride, Singapore cable car flight",
            "State": "Central Region",
            "Country": "Singapore",
            "Category": "Island",
            "Travel_Style": "Beach, Island, Family, Leisure",
            "Best_Season": "Year-round",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
        # Thailand
        {
            "Name of the Place": "Wat Pho",
            "District": "Bangkok",
            "Famous_For": "Temple of the Reclining Buddha housing a 46-meter gold-leaf covered Buddha and birth center of traditional Thai massage education",
            "Activities": "Reclining Buddha photography, 108 bronze alms bowls coin drop ritual, Traditional authentic Thai massage, Stupa garden walk",
            "State": "Bangkok",
            "Country": "Thailand",
            "Category": "Temple/Religious",
            "Travel_Style": "Spiritual, Cultural, Heritage, Photography",
            "Best_Season": "November to February",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Grand Palace Bangkok",
            "District": "Bangkok",
            "Famous_For": "Dazzling 18th-century official royal residence of the Kings of Siam, housing Wat Phra Kaew and the venerated sacred Emerald Buddha",
            "Activities": "Emerald Buddha veneration, Chakri Maha Prasat throne hall photography, Demon guardian statues tour, Royal museum walk",
            "State": "Bangkok",
            "Country": "Thailand",
            "Category": "Heritage",
            "Travel_Style": "Cultural, Heritage, Spiritual, Photography",
            "Best_Season": "November to February",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "James Bond Island",
            "District": "Phang Nga",
            "Famous_For": "Ko Ta Pu — iconic 20-meter vertical limestone karst pinnacle rising out of emerald Phang Nga Bay, made famous in The Man with the Golden Gun",
            "Activities": "Sea canoe tour through limestone sea caves, Ko Ta Pu rock photography, Floating Muslim fishing village Koh Panyee lunch",
            "State": "Phang Nga",
            "Country": "Thailand",
            "Category": "Island",
            "Travel_Style": "Adventure, Island, Boating, Photography",
            "Best_Season": "November to April",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Phi Phi Islands",
            "District": "Krabi",
            "Famous_For": "Idyllic archipelago in the Andaman Sea featuring towering limestone cliffs, Maya Bay turquoise lagoon and vibrant coral reefs",
            "Activities": "Maya Bay swimming, Snorkeling with blacktip reef sharks, Phi Phi Don viewpoint hike, Longtail boat island tour",
            "State": "Krabi",
            "Country": "Thailand",
            "Category": "Island",
            "Travel_Style": "Beach, Island, Adventure, Snorkeling, Photography",
            "Best_Season": "November to April",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Wat Arun",
            "District": "Bangkok",
            "Famous_For": "Temple of Dawn on the Chao Phraya River, renowned for its 82-meter porcelain and seashell-encrusted central prang reflecting golden sunsets",
            "Activities": "Central prang steep stair climb, Chao Phraya river sunset photography, Traditional Thai costume photo session, River ferry cruise",
            "State": "Bangkok",
            "Country": "Thailand",
            "Category": "Temple/Religious",
            "Travel_Style": "Cultural, Spiritual, Heritage, Photography",
            "Best_Season": "November to February",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Chiang Mai Temples",
            "District": "Chiang Mai",
            "Famous_For": "Northern cultural capital crowned by Wat Phra That Doi Suthep on mountain heights, Wat Chedi Luang ruins and sacred Lanna architecture",
            "Activities": "Doi Suthep 306-step naga staircase climb, Monk blessing ceremony, Sunday walking street night market, Lanna architecture tour",
            "State": "Chiang Mai",
            "Country": "Thailand",
            "Category": "Temple/Religious",
            "Travel_Style": "Cultural, Spiritual, Heritage, Photography",
            "Best_Season": "November to February",
            "Budget_Category": "Budget",
            "Duration_Days": 2,
        },
        # Switzerland
        {
            "Name of the Place": "Jungfraujoch (Top of Europe)",
            "District": "Interlaken",
            "Famous_For": "Highest railway station in Europe at 3,454m nestled between Jungfrau and Monch peaks, overlooking the 22km Great Aletsch Glacier",
            "Activities": "Jungfrau cogwheel railway journey, Sphinx observatory terrace viewing, Ice Palace sculpted caverns walk, Snow fun park skiing",
            "State": "Bern",
            "Country": "Switzerland",
            "Category": "Mountain/Hill",
            "Travel_Style": "Adventure, Alpine, Nature, Photography",
            "Best_Season": "May to October",
            "Budget_Category": "Luxury",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Lake Geneva & Chillon Castle",
            "District": "Montreux",
            "Famous_For": "Romantic medieval island castle on Lake Geneva made legendary by Lord Byron, set against snow-crowned Swiss Alps and terraced vineyards",
            "Activities": "Chillon Castle underground vault tour, Lake Geneva paddle steamer cruise, Lavaux vineyard terrace walk, Montreux promenade stroll",
            "State": "Vaud",
            "Country": "Switzerland",
            "Category": "Heritage",
            "Travel_Style": "Cultural, Heritage, Boating, Photography",
            "Best_Season": "May to October",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Matterhorn Zermatt",
            "District": "Zermatt",
            "Famous_For": "World-famous pyramidal alpine peak (4,478m) towering over car-free ski village of Zermatt, iconic symbol of Swiss chocolates and mountaineering",
            "Activities": "Gornergrat cogwheel train ride, Riffelsee lake Matterhorn reflection photography, Matterhorn Glacier Paradise cable car, Skiing",
            "State": "Valais",
            "Country": "Switzerland",
            "Category": "Mountain/Hill",
            "Travel_Style": "Adventure, Alpine, Nature, Photography",
            "Best_Season": "June to September",
            "Budget_Category": "Luxury",
            "Duration_Days": 2,
        },
        # United Kingdom
        {
            "Name of the Place": "Big Ben & Parliament",
            "District": "London",
            "Famous_For": "Iconic neo-Gothic Elizabeth Tower and Palace of Westminster on River Thames, historic heart of British democracy",
            "Activities": "Westminster Bridge photography, House of Commons tour, River Thames walkway, London Eye observation ride nearby",
            "State": "Greater London",
            "Country": "United Kingdom",
            "Category": "Heritage",
            "Travel_Style": "Cultural, Heritage, Historical, Photography",
            "Best_Season": "May to September",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Buckingham Palace",
            "District": "London",
            "Famous_For": "Official administrative headquarters and principal London residence of the British Monarch, world-famous for the Changing of the Guard",
            "Activities": "Changing of the Guard ceremony, Summer State Rooms tour, St. James's Park stroll, Royal Mews carriage viewing",
            "State": "Greater London",
            "Country": "United Kingdom",
            "Category": "Heritage",
            "Travel_Style": "Cultural, Heritage, Royal, Photography",
            "Best_Season": "May to September",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Stonehenge",
            "District": "Salisbury",
            "Famous_For": "Prehistoric monument erected around 3000 BCE consisting of a ring of standing sarsen megaliths aligned with solstitial sunrise",
            "Activities": "Stone circle audio tour, Prehistoric monument photography, Visitor center archaeological exhibition, Salisbury Cathedral visit",
            "State": "Wiltshire",
            "Country": "United Kingdom",
            "Category": "Heritage",
            "Travel_Style": "Heritage, Archaeological, Mystical, Photography",
            "Best_Season": "May to September",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Edinburgh Castle",
            "District": "Edinburgh",
            "Famous_For": "Historic royal stronghold dominating the skyline of Scotland from Castle Rock, housing Honours of Scotland crown jewels and Stone of Destiny",
            "Activities": "Crown Jewels viewing, One o'Clock Gun firing watch, Royal Mile stroll, Panoramic Edinburgh city overlook",
            "State": "Scotland",
            "Country": "United Kingdom",
            "Category": "Heritage",
            "Travel_Style": "Cultural, Heritage, Historical, Photography",
            "Best_Season": "May to September",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        # Italy
        {
            "Name of the Place": "Colosseum Rome",
            "District": "Rome",
            "Famous_For": "World's largest standing amphitheater built in 80 CE, monumental arena of gladiator combats, sea battle spectacles and Roman Forum center",
            "Activities": "Arena floor walk, Roman Forum and Palatine Hill tour, Gladiator gate photography, Arch of Constantine visit",
            "State": "Lazio",
            "Country": "Italy",
            "Category": "Heritage",
            "Travel_Style": "Cultural, Heritage, Historical, Photography",
            "Best_Season": "April to June",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Vatican Museums & Sistine Chapel",
            "District": "Vatican City",
            "Famous_For": "Papal art galleries containing Michelangelo's breathtaking Sistine Chapel ceiling and The Last Judgment, and St. Peter's Basilica",
            "Activities": "Sistine Chapel ceiling contemplation, St. Peter's Basilica dome climb, Raphael Rooms tour, Bramante spiral staircase walk",
            "State": "Rome",
            "Country": "Italy",
            "Category": "Heritage",
            "Travel_Style": "Cultural, Spiritual, Art, Photography",
            "Best_Season": "April to June",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Venice Grand Canal",
            "District": "Venice",
            "Famous_For": "Major water-traffic corridor winding through Venice flanked by over 170 Byzantine, Gothic and Renaissance palazzi and Rialto Bridge",
            "Activities": "Gondola ride with serenader, Vaporetto water bus cruise, Rialto Bridge photography, St. Mark's Square exploration",
            "State": "Veneto",
            "Country": "Italy",
            "Category": "Lake/Water",
            "Travel_Style": "Cultural, Romance, Boating, Photography",
            "Best_Season": "April to October",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Leaning Tower of Pisa",
            "District": "Pisa",
            "Famous_For": "World-famous freestanding bell tower of Pisa Cathedral in Piazza dei Miracoli, renowned worldwide for its unintended four-degree tilt",
            "Activities": "Leaning Tower spiral stair climb, Classic supporting-the-tower photo op, Pisa Cathedral and Baptistery tour, Campo Santo stroll",
            "State": "Tuscany",
            "Country": "Italy",
            "Category": "Heritage",
            "Travel_Style": "Cultural, Heritage, Architectural, Photography",
            "Best_Season": "April to October",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        # Greece
        {
            "Name of the Place": "Acropolis of Athens",
            "District": "Athens",
            "Famous_For": "Ancient citadel crowning Athens with classical Greek architectural triumphs: the Parthenon, Erechtheion Caryatids and Propylaea",
            "Activities": "Parthenon monument walk, Acropolis Museum artifact study, Odeon of Herodes Atticus overlook, Plaka neighborhood stroll",
            "State": "Attica",
            "Country": "Greece",
            "Category": "Heritage",
            "Travel_Style": "Cultural, Heritage, Historical, Photography",
            "Best_Season": "April to October",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Santorini Oia Caldera Sunset",
            "District": "Santorini",
            "Famous_For": "Iconic cliffside Cycladic village of whitewashed sugar-cube houses and blue-domed churches perched high over volcanic caldera sunsets",
            "Activities": "Blue-domed church photography, Castle of Oia sunset viewing, Ammoudi Bay fresh seafood dining, Caldera sailing cruise",
            "State": "South Aegean",
            "Country": "Greece",
            "Category": "Island",
            "Travel_Style": "Romance, Island, Luxury, Photography",
            "Best_Season": "May to October",
            "Budget_Category": "Luxury",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Meteora Monasteries",
            "District": "Kalabaka",
            "Famous_For": "Surreal complex of Eastern Orthodox monasteries perched atop soaring monolithic sandstone rock pillars up to 400 meters high",
            "Activities": "Monastery staircase hiking, Great Meteoron tour, Sandstone pillar sunset photography, Byzantine fresco appreciation",
            "State": "Thessaly",
            "Country": "Greece",
            "Category": "Temple/Religious",
            "Travel_Style": "Spiritual, Heritage, Nature, Photography",
            "Best_Season": "April to October",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        # Turkey
        {
            "Name of the Place": "Hagia Sophia",
            "District": "Istanbul",
            "Famous_For": "6th-century architectural marvel originally built as Byzantine cathedral, converted to imperial mosque with monumental dome and golden mosaics",
            "Activities": "Upper gallery mosaic viewing, Byzantine dome photography, Blue Mosque visit across Sultanahmet, Historic Turkish bath visit",
            "State": "Marmara",
            "Country": "Turkey",
            "Category": "Heritage",
            "Travel_Style": "Cultural, Heritage, Spiritual, Photography",
            "Best_Season": "April to October",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Cappadocia Hot Air Balloon Valley",
            "District": "Goreme",
            "Famous_For": "Otherworldly landscape of fairy chimneys, troglodyte cave dwellings and hundreds of hot air balloons floating over volcanic valleys at sunrise",
            "Activities": "Sunrise hot air balloon flight, Underground city of Derinkuyu exploration, Cave hotel stay, Goreme Open Air Museum tour",
            "State": "Central Anatolia",
            "Country": "Turkey",
            "Category": "Adventure",
            "Travel_Style": "Adventure, Romance, Nature, Photography",
            "Best_Season": "April to November",
            "Budget_Category": "Luxury",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Pamukkale Terraces",
            "District": "Denizli",
            "Famous_For": "Cotton Castle — natural marvel of snow-white travertine mineral thermal pools cascading down mountainside next to ancient Hierapolis ruins",
            "Activities": "Travertine thermal pool wading, Cleopatra antique pool swimming among submerged Roman columns, Hierapolis theatre tour",
            "State": "Aegean",
            "Country": "Turkey",
            "Category": "Garden/Nature",
            "Travel_Style": "Nature, Wellness, Heritage, Photography",
            "Best_Season": "April to October",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        # Maldives
        {
            "Name of the Place": "Maafushi Island",
            "District": "Kaafu Atoll",
            "Famous_For": "Premier local island in the Maldives offering budget-friendly overwater excursions, bikini beach, manta ray snorkeling and sandbanks",
            "Activities": "Snorkeling with nurse sharks and stingrays, Floating sandbank lunch, Scuba diving with sea turtles, Jet skiing",
            "State": "Kaafu",
            "Country": "Maldives",
            "Category": "Island",
            "Travel_Style": "Beach, Island, Snorkeling, Adventure",
            "Best_Season": "November to April",
            "Budget_Category": "Moderate",
            "Duration_Days": 3,
        },
        {
            "Name of the Place": "Conrad Rangali Undersea Restaurant",
            "District": "Alif Dhaal Atoll",
            "Famous_For": "Ithaa — world's first all-glass undersea restaurant situated five meters beneath the Indian Ocean with 180-degree coral reef panoramas",
            "Activities": "Fine undersea dining among sharks and rays, Coral reef exploration, Overwater bungalow luxury stay, Sunset dhoni cruise",
            "State": "Alif Dhaal",
            "Country": "Maldives",
            "Category": "Island",
            "Travel_Style": "Luxury, Honeymoon, Culinary, Ocean",
            "Best_Season": "November to April",
            "Budget_Category": "Luxury",
            "Duration_Days": 3,
        },
        # Sri Lanka
        {
            "Name of the Place": "Sigiriya Lion Rock",
            "District": "Matale",
            "Famous_For": "Ancient 5th-century palace citadel perched atop a sheer 200-meter granite rock, renowned for Lion Gate, mirror wall and cloud maiden frescoes",
            "Activities": "Lion paw staircase climb, Cloud maiden fresco study, Mirror wall inscription reading, Summit palace garden photography",
            "State": "Central Province",
            "Country": "Sri Lanka",
            "Category": "Heritage",
            "Travel_Style": "Heritage, Archaeological, Adventure, Photography",
            "Best_Season": "December to April",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Temple of the Tooth Kandy",
            "District": "Kandy",
            "Famous_For": "Sri Dalada Maligawa — venerated golden-roofed Buddhist temple housing the sacred left canine tooth relic of Gautama Buddha",
            "Activities": "Thevava drum offering ceremony, Golden tooth relic chamber veneration, Kandy lake promenade stroll, Esala Perahera festival attendance",
            "State": "Central Province",
            "Country": "Sri Lanka",
            "Category": "Temple/Religious",
            "Travel_Style": "Spiritual, Cultural, Heritage, Photography",
            "Best_Season": "December to April",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Mirissa Whale Watching",
            "District": "Matara",
            "Famous_For": "World-premier coastal departure point to encounter blue whales (largest animal on Earth), sperm whales and acrobatic spinner dolphins",
            "Activities": "Ocean whale watching catamaran cruise, Coconut Tree Hill sunset photography, Secret beach swimming, Fresh seafood dining",
            "State": "Southern Province",
            "Country": "Sri Lanka",
            "Category": "Wildlife",
            "Travel_Style": "Wildlife, Adventure, Beach, Boating",
            "Best_Season": "November to April",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Nine Arches Bridge Ella",
            "District": "Badulla",
            "Famous_For": "Bridge in the Sky — spectacular colonial brick and stone viaduct built without steel, curving through lush tropical tea valley forests",
            "Activities": "Blue mountain train crossing photography, Highland tea plantation walk, Ella Rock hike, Little Adam's Peak climb",
            "State": "Uva Province",
            "Country": "Sri Lanka",
            "Category": "Heritage",
            "Travel_Style": "Eco, Heritage, Scenic, Photography",
            "Best_Season": "January to May",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        # Nepal & Bhutan
        {
            "Name of the Place": "Pashupatinath",
            "District": "Kathmandu",
            "Famous_For": "Sacred Hindu temple complex dedicated to Lord Shiva on the banks of Bagmati River, world-famous for pagoda architecture and evening cremation aarti",
            "Activities": "Pagoda temple darshan, Bagmati river evening Sandhya Aarti, Sadhu holy men photo portraits, UNESCO heritage walk",
            "State": "Bagmati",
            "Country": "Nepal",
            "Category": "Temple/Religious",
            "Travel_Style": "Spiritual, Cultural, Heritage, Photography",
            "Best_Season": "October to March",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Everest Base Camp Trek",
            "District": "Solukhumbu",
            "Famous_For": "Legendary Himalayan trekking pilgrimage to the foot of Mount Everest (8,848m) at 5,364 meters through Sherpa villages and Khumbu glacier",
            "Activities": "Kala Patthar sunrise Everest photography, Tengboche monastery blessing, Hillary suspension bridge crossing, Sherpa culture homestay",
            "State": "Koshi",
            "Country": "Nepal",
            "Category": "Mountain/Hill",
            "Travel_Style": "Adventure, Trekking, Mountaineering, Photography",
            "Best_Season": "October to December",
            "Budget_Category": "Luxury",
            "Duration_Days": 5,
        },
        {
            "Name of the Place": "Boudhanath",
            "District": "Kathmandu",
            "Famous_For": "One of the largest spherical Buddhist stupas in the world, surrounded by prayer wheels, fluttering Tibetan lungta flags and rooftop cafes",
            "Activities": "Stupa kora circumambulation, Spinning giant prayer wheels, Rooftop cafe butter tea sipping, Tibetan thangka art study",
            "State": "Bagmati",
            "Country": "Nepal",
            "Category": "Temple/Religious",
            "Travel_Style": "Spiritual, Cultural, Peace, Photography",
            "Best_Season": "October to March",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Pokhara Phewa Lake",
            "District": "Pokhara",
            "Famous_For": "Tranquil freshwater lake reflecting the sacred fishtail peak of Machapuchare, gateway to the Annapurna mountain circuit",
            "Activities": "Colorful doonga wooden boat ride to Tal Barahi island temple, Sarangkot sunrise paragliding, World Peace Pagoda hike",
            "State": "Gandaki",
            "Country": "Nepal",
            "Category": "Lake/Water",
            "Travel_Style": "Eco, Boating, Adventure, Paragliding",
            "Best_Season": "October to April",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Paro Taktsang (Tiger's Nest)",
            "District": "Paro",
            "Famous_For": "Iconic Bhutanese Buddhist sacred monastery clinging dramatically to a sheer granite cliff 900 meters above the Paro Valley floor",
            "Activities": "Mountain cliff pilgrimage trek, Cave of Guru Rinpoche meditation, Waterfall suspension bridge crossing, Paro valley photography",
            "State": "Paro",
            "Country": "Bhutan",
            "Category": "Temple/Religious",
            "Travel_Style": "Spiritual, Trekking, Cultural, Photography",
            "Best_Season": "March to May",
            "Budget_Category": "Luxury",
            "Duration_Days": 1,
        },
        # Australia
        {
            "Name of the Place": "Sydney Opera House",
            "District": "Sydney",
            "Famous_For": "UNESCO World Heritage multi-venue performing arts center designed by Jørn Utzon with iconic expressionist sail shells on Sydney Harbour",
            "Activities": "Concert hall backstage architectural tour, Harbour Bridge walkway photography, Circular Quay ferry ride, Opera performance",
            "State": "New South Wales",
            "Country": "Australia",
            "Category": "Heritage",
            "Travel_Style": "Cultural, Architecture, Modern, Photography",
            "Best_Season": "September to November",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Great Barrier Reef",
            "District": "Cairns",
            "Famous_For": "World's largest coral reef system composed of over 2,900 individual reefs, visible from space, teeming with sea turtles, rays and tropical fish",
            "Activities": "Outer reef scuba diving and snorkeling, Scenic helicopter reef flight, Glass-bottom boat cruise, Green Island eco walk",
            "State": "Queensland",
            "Country": "Australia",
            "Category": "Island",
            "Travel_Style": "Adventure, Ocean, Eco, Snorkeling, Photography",
            "Best_Season": "June to October",
            "Budget_Category": "Luxury",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Uluru (Ayers Rock)",
            "District": "Alice Springs",
            "Famous_For": "Sacred massive red sandstone monolith rising 348m in the Australian Red Centre, deeply revered by Anangu Aboriginal traditional custodians",
            "Activities": "Sunrise and sunset color shift photography, Base walk guided Aboriginal rock art tour, Field of Light art installation walk",
            "State": "Northern Territory",
            "Country": "Australia",
            "Category": "Mountain/Hill",
            "Travel_Style": "Cultural, Indigenous, Mystical, Stargazing",
            "Best_Season": "May to September",
            "Budget_Category": "Luxury",
            "Duration_Days": 2,
        },
        # Vietnam, Cambodia, Malaysia, South Korea
        {
            "Name of the Place": "Ha Long Bay Cruise",
            "District": "Quang Ninh",
            "Famous_For": "UNESCO World Heritage seascape of 1,600 towering limestone karst islets rising from emerald waters in the Gulf of Tonkin",
            "Activities": "Overnight luxury junk boat cruise, Kayaking through Luon cave, Ti Top island summit hike, Sung Sot surprise cave tour",
            "State": "Northeast",
            "Country": "Vietnam",
            "Category": "Island",
            "Travel_Style": "Eco, Boating, Island, Adventure, Photography",
            "Best_Season": "October to December",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Hội An Ancient Town",
            "District": "Quang Nam",
            "Famous_For": "Exceptionally well-preserved 15th-to-19th century Southeast Asian trading port, famous for glowing lantern streets and Japanese Covered Bridge",
            "Activities": "Evening silk lantern boat release on Thu Bon river, Tailor-made custom clothing shopping, Street food Cao Lau tasting, Cycling",
            "State": "South Central Coast",
            "Country": "Vietnam",
            "Category": "Heritage",
            "Travel_Style": "Cultural, Heritage, Romance, Photography",
            "Best_Season": "February to July",
            "Budget_Category": "Budget",
            "Duration_Days": 2,
        },
        {
            "Name of the Place": "Angkor Wat",
            "District": "Siem Reap",
            "Famous_For": "Largest religious monument in the world (402 acres), 12th-century Khmer temple masterpiece symbolizing Mount Meru with central towers and moat",
            "Activities": "Sunrise reflection photography over lotus pond, Bas-relief gallery study, Ta Prohm tomb raider tree root walk, Bayon smiling faces visit",
            "State": "Siem Reap",
            "Country": "Cambodia",
            "Category": "Heritage",
            "Travel_Style": "Heritage, Cultural, Spiritual, Archaeological",
            "Best_Season": "November to March",
            "Budget_Category": "Moderate",
            "Duration_Days": 3,
        },
        {
            "Name of the Place": "Petronas Twin Towers",
            "District": "Kuala Lumpur",
            "Famous_For": "World's tallest twin towers standing at 451.9 meters, connected by a double-decker Skybridge at 41st and 42nd floors with Islamic geometric motifs",
            "Activities": "Skybridge crossing walk, 86th floor observation deck viewing, KLCC park fountain light show, Suria KLCC shopping",
            "State": "Federal Territory",
            "Country": "Malaysia",
            "Category": "Heritage",
            "Travel_Style": "Modern, Architecture, Sightseeing, Photography",
            "Best_Season": "Year-round",
            "Budget_Category": "Moderate",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Batu Caves",
            "District": "Gombak",
            "Famous_For": "Limestone hill riddled with caves and temples guarded by the world's tallest statue of Hindu Lord Murugan (140 feet) and 272 rainbow steps",
            "Activities": "272 rainbow staircase climb, Cathedral cave shrine darshan, Macaque monkey photography, Dark cave conservation tour",
            "State": "Selangor",
            "Country": "Malaysia",
            "Category": "Temple/Religious",
            "Travel_Style": "Spiritual, Cultural, Adventure, Photography",
            "Best_Season": "Year-round",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Gyeongbokgung Palace",
            "District": "Seoul",
            "Famous_For": "Main royal palace of the Joseon dynasty built in 1395, featuring Hyangwonjeong pavilion, throne hall and royal guard changing ceremony",
            "Activities": "Royal guard changing ceremony viewing, Wearing traditional Hanbok dress (free admission), Gyeonghoeru pavilion photography, National folk museum",
            "State": "Seoul Capital Area",
            "Country": "South Korea",
            "Category": "Heritage",
            "Travel_Style": "Cultural, Heritage, Royal, Photography",
            "Best_Season": "March to May",
            "Budget_Category": "Budget",
            "Duration_Days": 1,
        },
        {
            "Name of the Place": "Jeju Island Hallasan",
            "District": "Jeju",
            "Famous_For": "South Korea's highest shield volcano (1,947m) crowned by Baengnokdam crater lake, Manjanggul lava tube and Seongsan Ilchulbong sunrise peak",
            "Activities": "Hallasan summit crater trek, Seongsan sunrise peak hike, Manjanggul lava tube walk, Haenyeo female diver demonstration",
            "State": "Jeju Province",
            "Country": "South Korea",
            "Category": "Mountain/Hill",
            "Travel_Style": "Adventure, Nature, Volcanic, Photography",
            "Best_Season": "April to June",
            "Budget_Category": "Moderate",
            "Duration_Days": 2,
        },
    ]

    added_curated = 0
    updated_curated = 0

    for spot in PROMPT_CURATED_SPOTS:
        key = normalize_place_key(spot["Name of the Place"])
        if key in existing_map:
            # Overwrite with our high-fidelity, verified prompt-specific data
            existing_map[key].update(spot)
            updated_curated += 1
        else:
            existing_map[key] = spot
            added_curated += 1

    print(f"Curated spots: {added_curated} newly added, {updated_curated} updated with rich metadata.")

    # 3. Create DataFrame from existing_map
    combined_rows = list(existing_map.values())
    df_combined = pd.DataFrame(combined_rows)

    # Ensure all target columns exist and are ordered correctly
    for col in TARGET_COLUMNS:
        if col not in df_combined.columns:
            df_combined[col] = ""
    
    df_combined = df_combined[TARGET_COLUMNS]

    # Clean formatting
    for col in TARGET_COLUMNS:
        if col == "Duration_Days":
            df_combined[col] = pd.to_numeric(df_combined[col], errors="coerce").fillna(1).astype(int)
        else:
            df_combined[col] = df_combined[col].fillna("").astype(str).str.strip()

    # Drop any true duplicate rows
    df_combined = df_combined.drop_duplicates(subset=["Name of the Place"])

    # Sort nicely by Country, State, District, Name
    df_combined = df_combined.sort_values(by=["Country", "State", "District", "Name of the Place"]).reset_index(drop=True)

    print(f"\nFinal combined dataset has {len(df_combined)} records across {df_combined['Country'].nunique()} countries!")
    print(f"Country breakdown:")
    for country, count in df_combined['Country'].value_counts().head(20).items():
        print(f"  {country}: {count}")

    # Save to both target locations
    print(f"\nSaving to {TOURISM_CSV_PATH}...")
    df_combined.to_csv(TOURISM_CSV_PATH, index=False, encoding="utf-8")

    print(f"Saving to {BACKEND_TOURISM_CSV_PATH}...")
    df_combined.to_csv(BACKEND_TOURISM_CSV_PATH, index=False, encoding="utf-8")

    print("Success! Both tourism.csv files updated.")


if __name__ == "__main__":
    main()
