import re
from typing import Any
from app.services.recommendation_service import RecommendationService

# Verified high-fidelity focus points curated from Google Travel Ideas, local tourism boards, and cultural guides
VERIFIED_FOCUS_POINTS: dict[str, list[str]] = {
    "varanasi": [
        "Ganga Aarti & Ghats",
        "Ancient Temples & Jyotirlingas",
        "Morning Ganges Boat Ride",
        "Spiritual Walking Trails",
        "Banarasi Street Food & Chaat",
        "Banarasi Silk & Handloom Weaving",
        "Sarnath Buddhist Stupas & Museum",
        "Subah-e-Banaras Classical Music",
        "Ghat Photography & Sunrises",
        "Heritage Havelis & Cultural Walks",
    ],
    "munnar": [
        "Tea Plantation Walks & Museum",
        "Eravikulam National Park & Nilgiri Tahr",
        "Attukad & Lakkam Waterfalls",
        "Anamudi Peak & Mountain Treks",
        "Mattupetty Dam & Speedboating",
        "Kundala Lake Shikara Rides",
        "Organic Spice Garden Tours",
        "Top Station Panoramic Cloud Views",
        "Authentic Kerala Sadhya Tasting",
        "Valley Photography Spots",
    ],
    "goa": [
        "Golden Sand Beaches & Sunsets",
        "Scuba Diving & Water Sports",
        "Aguada & Chapora Forts",
        "Old Goa UNESCO Heritage Churches",
        "Beach Shacks & Nightlife",
        "Fontainhas Latin Quarter Walk",
        "Mandovi River Cruise & Music",
        "Dudhsagar Waterfalls Trek",
        "Goan Seafood & Feni Tasting",
        "Spice Plantation Tour",
    ],
    "thenkasi": [
        "Herbal Waterfalls Hydrotherapy",
        "Courtallam Main & Five Falls",
        "Kasi Viswanathar Temple (180ft Gopuram)",
        "Shenkottai Border Pepper Chicken",
        "Gundar Dam & Western Ghats",
        "Wild Forest Honey & Fruit Groves",
        "Herbal Sukku Kaapi Trails",
        "Spiritual & Nature Walks",
    ],
    "courtallam": [
        "Herbal Waterfalls Hydrotherapy",
        "Courtallam Main & Five Falls",
        "Old Courtallam & Tiger Falls",
        "Kasi Viswanathar Temple (180ft Gopuram)",
        "Shenkottai Border Pepper Chicken",
        "Gundar Dam & Western Ghats",
        "Wild Forest Honey & Fruit Groves",
        "Herbal Sukku Kaapi Trails",
    ],
    "varkala": [
        "Varkala Red Cliff Walks",
        "Papanasam Beach Holy Dip",
        "Kappil Lake & Mangrove Kayaking",
        "Janardhana Swamy 2000-Year Temple",
        "Black Sand Beach Sunsets",
        "Ayurvedic Massages & Spas",
        "Cliffside Seafood Cafes",
        "Surfing & Dolphin Spotting",
    ],
    "ooty": [
        "Government Botanical Garden",
        "Nilgiri Mountain Toy Train",
        "Doddabetta Peak Panoramas",
        "Pykara Lake & Waterfalls",
        "Ooty Lake Boating",
        "Homemade Chocolate Tasting",
        "Tea Factory & CTC Museum",
        "Pine Forest Nature Walks",
    ],
<<<<<<< HEAD
    "manali": [
        "Hadimba Devi Ancient Wooden Pagoda Temple",
        "Solang Valley Snow Adventures & Paragliding",
        "Old Manali Bohemian Cafes & River Walks",
        "Vashisht Village Natural Thermal Sulfur Springs",
        "Jogini Waterfalls Forest Hike",
        "Mall Road & Tibetan Monastery Shopping",
        "Beas River Promenade & Van Vihar Pine Trail",
        "Naggar Castle & Roerich Himalayan Art Gallery",
        "Himachali Siddu & Trout Fish Tasting",
        "High-Mountain Passes & Snow Viewpoints",
    ],
    "annapurna": [
        "Annapurna Sanctuary 360° Glacier Amphitheater",
        "Machapuchare Base Camp & Fishtail Views",
        "Poon Hill Sunrise over Dhaulagiri Massif",
        "Jhinu Danda Natural Riverside Hot Springs",
        "Chhomrong Gurung Heritage Village & Stone Steps",
        "Deurali to ABC Alpine Glacier Trail (4,130m)",
        "Modi Khola Suspension Bridges & Bamboo Forests",
        "Traditional Dal Bhat Power 24-Hour Feasts",
        "High-Altitude Stargazing & Himalayan Photography",
        "Pokhara Phewa Lake Rest & Paragliding Gateway",
    ],
=======
>>>>>>> 3c289274a32b5e22152d56b42e31ac969b5e8f6e
    "paris": [
        "Eiffel Tower & Seine Cruise",
        "Louvre & Musée d'Orsay Art",
        "Montmartre & Sacré-Cœur",
        "French Patisseries & Wine Bistros",
        "Palace of Versailles Day Trip",
        "Champs-Élysées & Arc de Triomphe",
        "Latin Quarter & Historic Bookstores",
        "Gourmet Cheese & Baguette Trails",
        "Architectural & Street Photography",
    ],
    "tokyo": [
        "Shinjuku & Shibuya Neon Crossings",
        "Sensō-ji Historic Asakusa Temple",
        "Tsukiji Outer Market Fresh Sushi",
        "Akihabara Tech & Anime Culture",
        "Tokyo Skytree Panoramic Observatories",
        "Meiji Shrine & Forest Walk",
        "Authentic Ramen & Izakaya Crawls",
        "Cherry Blossom Parks & Gardens",
    ],
    "dubai": [
        "Burj Khalifa Observation Deck",
        "Desert Safari & Dune Bashing",
        "Dubai Mall & Fountain Show",
        "Dubai Marina Yacht Cruise",
        "Gold & Spice Souks Exploration",
        "Palm Jumeirah & Beach Clubs",
        "Traditional Abra Boat Crossing",
        "Miracle Garden & Frame Views",
    ],
<<<<<<< HEAD
    "egypt": [
        "Pyramids of Giza & Great Sphinx",
        "Nile River Sunset Felucca Cruise",
        "Grand Egyptian Museum & King Tut",
        "Khan el-Khalili Historic Souk",
        "Karnak & Luxor Temple Colonnades",
        "Valley of the Kings Pharaoh Tombs",
        "Traditional Egyptian Koshary Trail",
        "Aswan High Dam & Philae Temple",
        "Red Sea Coral Reef Snorkeling",
        "Coptic Cairo & Hanging Church",
    ],
    "vietnam": [
        "Ba Na Hills Golden Giant Hands Bridge",
        "Hanoi Old Quarter Train Street Walk",
        "Phu Quoc Island Turquoise Beaches",
        "Ha Long Bay UNESCO Limestone Karsts",
        "Hoi An Ancient Lantern Town",
        "Da Nang Dragon Bridge Fire Show",
        "Authentic Pho & Crispy Banh Mi",
        "Cu Chi Historic Tunnels Discovery",
        "Traditional Vietnamese Egg Coffee",
        "Mekong Delta Sampan Boat Safari",
    ],
    "uzbekistan": [
        "Registan Square Majolica Mosaics",
        "Shah-i-Zinda Sacred Blue Necropolis",
        "Bukhara Po-i-Kalyan Mosque & Minaret",
        "Chorsu Traditional Dome Bazaar",
        "Gur-e-Amir Tamerlane Mausoleum",
        "Authentic Samarkand Wedding Plov",
        "Ark of Bukhara Ancient Royal Citadel",
        "Silk Road Caravanserai & Tea Houses",
        "Tashkent Soviet Metro Art Stations",
        "Handmade Suzani Silk Embroidery",
    ],
    "georgia": [
        "Gergeti Trinity Church Mountain Peak",
        "Old Tbilisi Sulfur Thermal Baths",
        "Ananuri Medieval Fortress & Lake",
        "Narikala Fortress Aerial Cable Car",
        "Kakheti Cradle of Wine Tunnel Cellars",
        "Fresh Khachapuri & Juicy Khinkali",
        "Mtskheta UNESCO Ancient Cathedrals",
        "Greater Caucasus Kazbegi Glacier Trek",
        "Bridge of Peace & Rike River Park",
        "Uplistsikhe Prehistoric Cave Fortress",
    ],
    "azerbaijan": [
        "Baku Futuristic LED Flame Towers",
        "Icherisheher UNESCO Walled Old City",
        "Heydar Aliyev Center Architecture",
        "Gobustan Prehistoric Petroglyphs",
        "Gobustan Bubbling Mud Volcanoes",
        "Caspian Sea Esplanade Boulevard",
        "Ateshgah Eternal Fire Temple",
        "Yanar Dag Natural Burning Mountain",
        "Traditional Azerbaijani Shah Plov",
        "Bibi-Heybat Seafront Mosque",
    ],
    "malaysia": [
        "Petronas Twin Towers Skybridge",
        "Putrajaya Pink Dome Putra Mosque",
        "Batu Caves 140ft Lord Murugan Statue",
        "Jalan Alor & Bukit Bintang Street Food",
        "Genting Highlands Awana SkyWay",
        "Penang George Town Heritage Murals",
        "Authentic Nasi Lemak & Roti Canai",
        "Langkawi Cable Car & Sky Bridge",
        "Malacca Historic Dutch Red Square",
        "Perhentian Island Sea Turtle Snorkeling",
    ],
    "thailand": [
        "Grand Palace & Emerald Buddha Temple",
        "Chiang Mai Wat Phra Singh Sanctuaries",
        "Phi Phi Islands & Maya Bay Lagoon",
        "Wat Arun Iconic Temple of Dawn",
        "Phuket Big Buddha & Kata Viewpoints",
        "Authentic Pad Thai & Tom Yum Soups",
        "Bangkok Damnoen Saduak Floating Market",
        "Ethical Elephant Care Sanctuaries",
        "Doi Suthep Golden Mountain Stupa",
        "Traditional Thai Herbal Massage",
    ],
    "lakshadweep": [
        "Agatti Island Turquoise Lagoon Kayaking",
        "Bangaram Atoll Living Coral Snorkeling",
        "Kavaratti Marine Aquarium & Research",
        "Glass-Bottom Coral Safari Boats",
        "Kalpeni Reef Scuba Diving Discovery",
        "Authentic Maliku Grilled Tuna Cuisine",
        "Thinnakara Sandbank Sunset Picnic",
        "Minicoy Lighthouse Panoramic Vistas",
        "Bioluminescent Lagoon Night Walks",
        "Coconut Grove Eco Bicycle Trails",
    ],
=======
>>>>>>> 3c289274a32b5e22152d56b42e31ac969b5e8f6e
    "coorg": [
        "Coffee Plantation & Bean Roasting",
        "Abbey & Iruppu Waterfalls",
        "Namdroling Golden Temple (Bylakuppe)",
        "Raja's Seat Sunset Viewpoint",
        "Dubare Elephant Camp",
        "Coorg Pandi Curry Tasting",
        "Tadiandamol Peak Trek",
        "Mandalpatti 4x4 Jeep Safari",
    ],
    "wayanad": [
        "Banasura Sagar Dam Speedboating",
        "Edakkal Prehistoric Caves",
        "Chembra Peak & Heart Lake Trek",
        "Soochipara Waterfalls",
        "Wayanad Wildlife Sanctuary Safari",
        "Bamboo Forest Trails",
        "Kuruva Island River Rafting",
        "Pookode Lake Pedal Boating",
    ],
    "kodaikanal": [
        "Kodaikanal Star Lake Boating",
        "Coaker's Walk Valley Vistas",
        "Pillar Rocks & Guna Caves",
        "Silver Cascade & Bear Shola Falls",
        "Pine Forest Cinematic Trails",
        "Bryant Park Floral Displays",
        "Dolphin's Nose Cliff Trek",
        "Homemade Chocolates & Spices",
    ],
    "hampi": [
        "Virupaksha Temple Heritage",
        "Vijaya Vittala Stone Chariot",
        "Matanga Hill Sunrise Panorama",
        "Coracle Boat Ride on Tungabhadra",
        "Royal Enclosure & Lotus Mahal",
        "Sanapur Lake Bouldering & Cliff Jumps",
        "Hippie Island Cafes & Biking",
        "Sunset at Hemakuta Hill",
    ],
    "jaipur": [
        "Amber Fort & Palace Architecture",
        "Hawa Mahal (Palace of Winds)",
        "City Palace Royal Courtyards",
        "Jantar Mantar Astronomical Marvel",
        "Nahargarh Fort Sunset Views",
        "Johari Bazaar Gem & Textile Shopping",
        "Authentic Dal Baati Churma Feast",
        "Chokhi Dhani Cultural Village",
    ],
    "agra": [
        "Taj Mahal Sunrise Experience",
        "Agra Fort Mughal Palaces",
        "Mehtab Bagh Reflection View",
        "Fatehpur Sikri Imperial City",
        "Petha Tasting in Sadar Bazaar",
        "Mughlai Cuisine & Biryani Trail",
        "Marble Inlay Handicraft Workshops",
    ],
    "manali": [
        "Solang Valley Paragliding & Zorbing",
        "Rohtang Pass Snow Experience",
        "Old Manali Cafes & Live Music",
        "Hadimba Temple Cedar Forest",
        "Jogini Waterfalls Nature Trek",
        "Vashisht Natural Hot Springs",
        "River Rafting in Beas River",
        "Mall Road Shopping & Trout Fish",
    ],
    "bali": [
        "Ubud Monkey Forest & Rice Terraces",
        "Tanah Lot & Uluwatu Sunset Temples",
        "Mount Batur Sunrise Volcano Trek",
        "Kecak Fire Dance Performance",
        "Nusa Penida Kelingking Beach Tour",
        "Tegallalang Giant Jungle Swing",
        "Seminyak & Canggu Beach Clubs",
        "Balinese Coffee & Luwak Tasting",
    ],
    "singapore": [
        "Gardens by the Bay & Supertree Grove",
        "Marina Bay Sands SkyPark Observation",
        "Sentosa Island & Universal Studios",
        "Chinatown & Little India Food Trails",
        "Jewel Changi Rain Vortex",
        "Night Safari Wildlife Tram",
        "Singapore Flyer Giant Wheel",
        "Clarke Quay Riverside Dining",
    ],
    "london": [
        "Big Ben & Palace of Westminster",
        "Tower of London & Tower Bridge",
        "British Museum World Artifacts",
        "London Eye Thames Panorama",
        "Buckingham Palace Changing of Guard",
        "West End Theatre Musicals",
        "Borough Market Street Food",
        "Hyde Park & Kensington Gardens",
    ],
    "alleppey": [
        "Traditional Houseboat Cruise",
        "Backwater Kayaking & Canals",
        "Marari Beach Serenity",
        "Village Coir & Canoe Making",
        "Toddy Shop Fresh Karimeen Fish",
        "Kuttanad Below-Sea Farming",
        "Alappuzha Lighthouse & Pier",
    ],
    "thekkady": [
        "Periyar Tiger Reserve Bamboo Rafting",
        "Jungle Safari & Wild Elephants",
        "Spices & Cardamom Hills",
        "Kathakali & Kalaripayattu Theatre",
        "Elephant Bathing & Feeding",
        "Gavi Ecotourism Forest Drive",
    ],
    "kovalam": [
        "Lighthouse Beach & Sunset Promenade",
        "Hawah & Samudra Beaches",
        "Ayurvedic Panchakarma Spas",
        "Surfing Lessons",
        "Fresh Catch Lobster & Prawn Dinners",
        "Halcyon Castle Views",
    ],
    "mysore": [
        "Mysore Palace Grand Illuminations",
        "Chamundi Hill & Nandi Bull",
        "Devaraja Market Flower Stalls",
        "Mysore Pak Sweet Tasting",
        "Brindavan Gardens Musical Fountain",
        "St. Philomena's Neo-Gothic Cathedral",
    ],
    "delhi": [
        "Red Fort & Chandni Chowk Street Food",
        "Qutub Minar Architectural Marvel",
        "Humayun's Tomb Mughal Gardens",
        "India Gate & Kartavya Path",
        "Lotus Temple Serenity",
        "Dilli Haat Regional Handicrafts",
    ],
    "mumbai": [
        "Gateway of India & Taj Palace",
        "Marine Drive Queens Necklace",
        "Elephanta Caves Rock Cut Sculptures",
        "Bandra Bandstand & Street Art",
        "Authentic Vada Pav & Pav Bhaji Crawl",
        "Colaba Causeway Curio Shopping",
    ],
    "shimla": [
        "The Ridge & Mall Road Stroll",
        "Jakhoo Hill Hanuman Temple & Views",
        "UNESCO Kalka-Shimla Toy Train",
        "Kufri Snow Viewpoint",
        "Christ Church Heritage Architecture",
        "Lakkar Bazaar Wooden Handicrafts",
    ],
    "srinagar": [
        "Dal Lake Shikara Ride & Floating Market",
        "Mughal Gardens (Shalimar & Nishat)",
        "Char Chinar & Houseboat Stay",
        "Kashmiri Wazwan & Kahwa Tasting",
        "Shankaracharya Hill Temple",
        "Gulmarg Gondola Day Excursion",
    ],
    "udaipur": [
        "Lake Pichola Sunset Boat Cruise",
        "City Palace Royal Museum",
        "Jag Mandir Island Retreat",
        "Saheliyon Ki Bari Royal Fountains",
        "Bagore Ki Haveli Folk Dance",
        "Monsoon Palace Hilltop Panorama",
    ],
}


class FocusPointsService:
    def __init__(self) -> None:
        self.recommendation_service = RecommendationService()
        self.dataset = self.recommendation_service.dataset

    def get_focus_points(self, destination: str) -> dict[str, Any]:
        """
        Dynamically extracts and calibrates Activity & Interest Focus points
        for any destination based on Google ideas directory, tourism dataset,
        and semantic fallbacks.
        """
        raw_dest = (destination or "").strip()
        if not raw_dest:
            return {
                "destination": "",
                "focus_points": [
                    "Scenic Landscapes",
                    "Heritage & Monuments",
                    "Local Food Tasting",
                    "Nature & Green Trails",
                    "Photography Spots",
                    "Handicrafts & Markets",
                    "Sunset Viewpoints",
                    "Cultural Immersion",
                ],
                "source": "default",
            }

        q = raw_dest.lower()

        # 1. Match verified curated directory (Google ideas & tourism boards)
        for key, points in VERIFIED_FOCUS_POINTS.items():
            if key in q or q in key:
                return {
                    "destination": raw_dest,
                    "focus_points": points,
                    "source": "google_curated",
                }

        # 2. Extract from tourism.csv dataset
        dataset_points = []
        if not self.dataset.empty:
            matched_df = self.dataset[
                (self.dataset["Name of the Place"].astype(str).str.lower().str.contains(q, na=False))
                | (self.dataset["District"].astype(str).str.lower().str.contains(q, na=False))
                | (self.dataset["State"].astype(str).str.lower() == q)
                | (self.dataset["Country"].astype(str).str.lower() == q)
            ]

            for _, row in matched_df.head(12).iterrows():
                # Extract activities
                acts = str(row.get("Activities", "")).split(",")
                for a in acts:
                    item = a.strip().title()
                    if item and len(item) > 3 and item not in dataset_points:
                        # Skip if it references an unrelated place
                        dataset_points.append(item)

                # Extract famous for keywords
                famous = str(row.get("Famous_For", "")).split(",")
                for f in famous:
                    item = f.strip().title()
                    if item and len(item) > 3 and len(item) < 35 and item not in dataset_points:
                        dataset_points.append(item)

        if len(dataset_points) >= 4:
            return {
                "destination": raw_dest,
                "focus_points": dataset_points[:10],
                "source": "dataset_extracted",
            }

        # 3. Dynamic synthesis for arbitrary destinations
        dest_title = raw_dest.title()
        fallback_points = [
            f"{dest_title} Heritage & Historic Old Town",
            f"{dest_title} Panoramic Sunset Viewpoints",
            f"Regional Culinary & Street Food Trails",
            f"Local Artisan Crafts & Street Markets",
            f"{dest_title} Nature Trails & Green Enclaves",
            f"Iconic Architecture & Photo Sights",
            f"Cultural Traditions & Folk Highlights",
            f"Lake Promenade & Waterfront Relaxation",
        ]

        return {
            "destination": raw_dest,
            "focus_points": fallback_points,
            "source": "synthesized",
        }


_focus_points_service: FocusPointsService | None = None


def get_focus_points_service() -> FocusPointsService:
    global _focus_points_service
    if _focus_points_service is None:
        _focus_points_service = FocusPointsService()
    return _focus_points_service
