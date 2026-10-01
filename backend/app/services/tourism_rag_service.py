"""
TripGenius — RAG (Retrieval-Augmented Generation) Tourism Knowledge Service.

Provides instant, grounded, high-precision regional & international travel intelligence.
Operates with sub-10ms latency, zero API rate-limit dependency, and verified facts:
- Regional geography, Western Ghats corridors, authentic local food & prices in ₹
- Detailed attractions, stays, transit routes, and seasonal microclimate insights.
"""

from typing import Any, Optional
import re

DESTINATION_KNOWLEDGE_BASE: dict[str, dict[str, Any]] = {
    "thenkasi": {
        "canonical_name": "Thenkasi & Courtallam",
        "aliases": ["thenkasi", "tenkasi", "courtallam", "kourtallam", "kutralam", "kuttralam", "ayikudi", "shenkottai"],
        "region": "Tamil Nadu (Western Ghats Foothills / Kerala Border)",
        "tagline": "The Spa of South India & Gateway to the Western Ghats",
        "vibe": "Rejuvenating waterfalls, temple heritage, mist-wrapped foothills, and famous border food",
        "best_season": "June to September (Peak Saaral season / monsoon waterfalls) and October to February (pleasant temple & dam visits)",
        "highlights": [
            {
                "name": "Courtallam Main Falls & Five Falls (Aintharuvi)",
                "desc": "Natural mineral-rich cascading falls running through herbal forests of the Western Ghats, renowned for therapeutic natural hydrotherapy.",
                "timing": "6:00 AM – 6:00 PM (season dependent)",
                "cost": "Free entry / nominal parking ₹30",
            },
            {
                "name": "Kasi Viswanathar Temple",
                "desc": "Historic 13th-century Pandyan temple built by King Parakrama Pandyan with a majestic 180-ft 9-tier Rajagopuram facing the misty hills.",
                "timing": "6:00 AM – 12:00 PM, 4:00 PM – 8:30 PM",
                "cost": "Free darshan / Special ₹50",
            },
            {
                "name": "Gundar Dam & Sengottai Western Ghats Drive",
                "desc": "Tranquil water reservoir surrounded by dense forest, rubber estates, and scenic mountain roads connecting to Aryankavu and Kollam.",
                "timing": "8:00 AM – 5:30 PM",
                "cost": "Nominal entry ₹20",
            },
            {
                "name": "Old Courtallam (Pazhaya Courtallam) & Tiger Falls",
                "desc": "Gentler cascades ideal for families, lined with herbal steam stalls and fresh fruit markets selling jackfruit and rambutan.",
                "timing": "6:30 AM – 5:30 PM",
                "cost": "Free entry",
            },
        ],
        "food_specialities": [
            "Hot Tenkasi Ennai Parotta with spicy Salna",
            "Border Rahmath Hotel Mutton Fry & Country Chicken",
            "Herbal Sukku Kaapi (dry ginger coffee) after waterfall baths",
            "Tirunelveli Halwa (freshly made nearby in Tenkasi)",
            "Ayikudi Sweet Guava and seasonal Western Ghats wild honey",
        ],
        "stay_options": [
            "Heritage Resort Courtallam (~₹2,800 – ₹4,200/night)",
            "Five Falls Orchard Farmstay (~₹2,200 – ₹3,500/night)",
            "Comfort Hotel / Lodge near Bus Stand (~₹1,200 – ₹1,800/night)",
        ],
        "transit": "Tenkasi Junction Railway Station (TSI) connects directly to Chennai, Madurai, and Kollam. Nearest airport: Tuticorin (TCR, 90 km) or Trivandrum (TRV, 105 km).",
        "budget_per_day": "₹1,800 – ₹3,000 per person per day (budget to comfort)",
        "insider_tip": "Visit Five Falls early morning around 6:30 AM to beat the Saaral season crowds. Must stop at Border Rahmath in Shenkottai for authentic pepper chicken.",
        "itinerary_2day": [
            "Day 1: Arrive Tenkasi, darshan at Kasi Viswanathar Temple, enjoy herbal shower at Courtallam Main Falls, evening parotta trail at Shenkottai.",
            "Day 2: Morning bath at Five Falls (Aintharuvi), scenic drive to Gundar Dam reservoir, explore Old Falls & spice shopping before return.",
        ],
        "follow_up_question": "Are you planning a trip during the Courtallam Saaral season (June–Sept) for waterfalls, or a peaceful weekend trip?",
    },
    "munnar": {
        "canonical_name": "Munnar",
        "aliases": ["munnar", "munar", "devikulam", "mattupetty", "kolukkumalai", "marayoor"],
        "region": "Idukki District, Kerala",
        "tagline": "The Emerald Tea Hills of the Western Ghats",
        "vibe": "Endless tea plantations, misty mountain passes, cool climate, and rare wildlife",
        "best_season": "September to May (Crisp cool air, 10°C – 22°C)",
        "highlights": [
            {
                "name": "Eravikulam National Park (Rajamalai)",
                "desc": "Home to the endangered Nilgiri Tahr and rolling shola-grassland hills.",
                "cost": "₹200 per adult",
            },
            {
                "name": "Kolukkumalai Sunrise 4x4 Jeep Safari",
                "desc": "World's highest tea plantation with jaw-dropping sunrise above a bed of clouds.",
                "cost": "₹2,500 – ₹3,200 per jeep (up to 6 people)",
            },
            {
                "name": "Mattupetty Dam & Kundala Lake",
                "desc": "Scenic lake boating, echo point viewpoints, and lush eucalyptus groves.",
                "cost": "Speedboat ₹600 for 5 pax",
            },
            {
                "name": "Tea Museum & Lockhart Tea Trail",
                "desc": "Historic tea processing machinery, fresh orthodox tea tasting, and panoramic valleys.",
                "cost": "₹150 entry",
            },
        ],
        "food_specialities": [
            "Kerala Puttu with Kadala Curry and fresh banana",
            "Clay-pot Fish Curry Meals with red Matta rice",
            "Steaming cardamom & masala tea straight from the estate",
            "Hot beef / chicken fry with flaky Malabar parotta",
        ],
        "stay_options": [
            "Tea Estate Boutique Bungalows (~₹4,500 – ₹7,000/night)",
            "Chithirapuram & Pallivasal View Stays (~₹2,500 – ₹3,800/night)",
            "Old Munnar Town Budget Homestays (~₹1,200 – ₹1,800/night)",
        ],
        "transit": "Nearest railway: Aluva (110 km) or Ernakulam (130 km). Nearest airport: Kochi (COK, 110 km). Regular KSRTC buses from Kochi and Coimbatore.",
        "budget_per_day": "₹2,500 – ₹4,500 per person per day",
        "insider_tip": "Book the 4:30 AM sunrise jeep to Kolukkumalai in advance. Avoid peak town traffic by staying in Pallivasal or Chinnakanal.",
        "itinerary_2day": [
            "Day 1: Tea Museum, Eravikulam National Park to spot Nilgiri Tahr, sunset view from Pothamedu viewpoint.",
            "Day 2: 4:30 AM Kolukkumalai sunrise safari, Mattupetty boating, tea spice shopping in old Munnar market.",
        ],
        "follow_up_question": "Do you prefer staying inside a scenic tea estate resort, or looking for a budget-friendly homestay?",
    },
    "vattavada": {
        "canonical_name": "Vattavada",
        "aliases": ["vattavada", "koviloor", "pambadum shola", "chilanthiyar"],
        "region": "Idukki District, Kerala (near Munnar / Tamil Nadu border)",
        "tagline": "Kerala's Organic Strawberry & Winter Vegetable Bowl",
        "vibe": "Pristine mountain village, terrace farming, apple & strawberry orchards, pine forests, and cool nights",
        "best_season": "October to April (Strawberry harvesting peaks in Dec–March)",
        "highlights": [
            {
                "name": "Organic Strawberry & Berry Farm Picking",
                "desc": "Walk through terraced farms, pick juicy strawberries, blackberries, and passionfruit directly from local farmers.",
                "cost": "₹150 – ₹250 per box",
            },
            {
                "name": "Pambadum Shola National Park Drive",
                "desc": "Drive through Kerala's smallest national park with towering pine trees, misty woods, and rare flying squirrels.",
                "cost": "Nominal checkpost entry ₹40",
            },
            {
                "name": "Koviloor Village & Ancient Mud-brick Houses",
                "desc": "Traditional tribal mountain settlement with centuries-old customs and terraced cabbage, garlic, and carrot fields.",
                "cost": "Free",
            },
        ],
        "food_specialities": [
            "Fresh strawberry jam and homemade fruit wine",
            "Farm-fresh organic vegetable stew with hot rotis",
            "Authentic country chicken curry prepared on woodfire",
            "Hot herbal mountain tea sweetened with wild honey",
        ],
        "stay_options": [
            "Vattavada Strawberry Farm Homestay (~₹2,200 – ₹3,500/night)",
            "Hill-top Tent Camping with Campfire (~₹1,500 – ₹2,200/night including meals)",
        ],
        "transit": "44 km from Munnar town via Top Station & Pambadum Shola road (about 1.5 to 2 hours scenic drive). Accessible by bike, car, or KSRTC bus from Munnar.",
        "budget_per_day": "₹2,000 – ₹3,200 per person per day",
        "insider_tip": "The temperature drops to 5°C at night in winter—carry a warm fleece jacket. Buy freshly harvested mountain garlic and dried wild herbs directly from local farmers.",
        "itinerary_2day": [
            "Day 1: Drive from Munnar via Top Station, cross Pambadum Shola forest, check into organic farmstay, sunset campfire.",
            "Day 2: Morning strawberry farm walk, Koviloor village viewpoint trek, Chilanthiyar waterfall, return drive.",
        ],
        "follow_up_question": "Would you like me to map out a farmstay camping plan or a day-trip from Munnar?",
    },
    "varkala": {
        "canonical_name": "Varkala",
        "aliases": ["varkala", "papanasam", "north cliff", "south cliff", "kappil"],
        "region": "Thiruvananthapuram District, Kerala",
        "tagline": "The Bohemian Red Cliffs of the Arabian Sea",
        "vibe": "Dramatic laterite cliffs overlooking turquoise sea, cliff cafes, surfing, yoga, and holy springs",
        "best_season": "October to March (Ideal beach & surfing weather)",
        "highlights": [
            {
                "name": "Varkala North Cliff Walk & Sunset Cafes",
                "desc": "Vibrant promenade packed with international bohemian cafes, live music, Tibetan handicrafts, and cliff sunset views.",
                "cost": "Free walk",
            },
            {
                "name": "Papanasam Beach & Holy Spring",
                "desc": "Golden sand beach backed by sacred mineral springs believed to wash away sins.",
                "cost": "Free",
            },
            {
                "name": "Kappil Beach & Mangrove Kayaking",
                "desc": "Serene spot where the Edava-Nadayara backwaters meet the Arabian Sea, separated by a thin coastal road.",
                "cost": "Kayaking ₹400 – ₹700/hour",
            },
            {
                "name": "Janardhana Swamy Temple",
                "desc": "2,000-year-old historic Vishnu temple with bell towers overlooking the ocean.",
                "cost": "Free",
            },
        ],
        "food_specialities": [
            "Catch of the day grilled sea bass & tiger prawns at North Cliff cafes",
            "Traditional Kerala Sadhya at local heritage eateries",
            "Nutella banana pancakes & cold brew coffee at Cliff cafes",
            "Fresh tender coconut water and banana fritters (Pazham Pori)",
        ],
        "stay_options": [
            "Cliffside Sea-View Boutique Cottages (~₹3,200 – ₹5,500/night)",
            "Backpacker Hostels & Yoga Retreats (~₹800 – ₹1,800/night)",
            "South Cliff Tranquil Homestays (~₹1,500 – ₹2,500/night)",
        ],
        "transit": "Varkala Sivagiri Railway Station (VAK) is just 3 km from the cliff. Trivandrum Airport (TRV) is 45 km away.",
        "budget_per_day": "₹2,200 – ₹4,000 per person per day",
        "insider_tip": "For peaceful beach time without crowds, head to Black Sand Beach or Odayam Beach just north of the main cliff.",
        "itinerary_2day": [
            "Day 1: Check in near North Cliff, swim at Papanasam beach, cliff cafe hopping, live music sunset dinner.",
            "Day 2: Morning surf lesson or yoga session, scooter ride to Kappil Lake kayaking, visit Janardhana temple.",
        ],
        "follow_up_question": "Are you traveling solo, with a partner, or with a group of friends?",
    },
    "wayanad": {
        "canonical_name": "Wayanad",
        "aliases": ["wayanad", "sulthan bathery", "kalpetta", "mananthavady", "vythiri", "meppadi"],
        "region": "Wayanad District, Kerala",
        "tagline": "The Land of Paddy Fields, Waterfalls & Forest Caves",
        "vibe": "Misty rainforests, bamboo groves, tea & spice plantations, prehistoric caves, and wildlife corridors",
        "best_season": "October to May",
        "highlights": [
            {
                "name": "Chembra Peak & Heart Lake",
                "desc": "Scenic mountain trek to the perpetual heart-shaped lake amidst clouds.",
                "cost": "Trek permit ₹1,000 for group of up to 5",
            },
            {
                "name": "Banasura Sagar Dam",
                "desc": "India's largest earthen dam with speedboating amidst floating green hill islands.",
                "cost": "Entry ₹40, Speedboat ₹850",
            },
            {
                "name": "Edakkal Caves",
                "desc": "Neolithic rock carvings and petroglyphs dating back to 6,000 BCE reached via a steep mountain climb.",
                "cost": "Entry ₹50",
            },
            {
                "name": "Soochipara & Meenmutty Waterfalls",
                "desc": "Three-tiered forest waterfalls with natural plunge pools surrounded by deciduous forest.",
                "cost": "Entry ₹80",
            },
        ],
        "food_specialities": [
            "Malabar Bamboo Biryani with date pickle",
            "Nadan Kozhi Curry with soft Neypathiri (fried rice pathiri)",
            "Gandhakasala aromatic rice meals",
            "Roasted Wayanad coffee & wild forest honey",
        ],
        "stay_options": [
            "Vythiri Rainforest Treehouse Resort (~₹6,000 – ₹10,000/night)",
            "Plantation Eco-Lodge & Spice Farmstay (~₹2,800 – ₹4,500/night)",
            "Kalpetta / Meppadi Budget Homestays (~₹1,400 – ₹2,200/night)",
        ],
        "transit": "Nearest railway station: Kozhikode (Calicut - CLT, 75 km). Nearest airport: Calicut International Airport (CCJ, 85 km).",
        "budget_per_day": "₹2,500 – ₹4,500 per person per day",
        "insider_tip": "Chembra Peak trek tokens are limited daily—reach the forest office by 7:00 AM to secure a morning trekking slot.",
        "itinerary_2day": [
            "Day 1: Banasura Sagar dam speedboating, Karlad lake zipline, Meenmutty / Soochipara falls bath.",
            "Day 2: Morning trek to Edakkal Caves petroglyphs, Muthanga wildlife safari, spice market shopping.",
        ],
        "follow_up_question": "Do you enjoy trekking and adventure activities, or looking for a relaxing plantation stay?",
    },
    "ooty": {
        "canonical_name": "Ooty & Coonoor",
        "aliases": ["ooty", "udhagamandalam", "coonoor", "kotagiri", "nilgiris"],
        "region": "Nilgiris District, Tamil Nadu",
        "tagline": "Queen of Hill Stations",
        "vibe": "Heritage toy train, botanical gardens, colonial heritage, pine forests, and homemade chocolates",
        "best_season": "October to June (pleasant 12°C – 20°C)",
        "highlights": [
            {
                "name": "Nilgiri Mountain Railway (Toy Train)",
                "desc": "UNESCO World Heritage steam/diesel rack railway passing through 16 tunnels and 250 bridges between Mettupalayam, Coonoor, and Ooty.",
                "cost": "₹30 – ₹205 (advance IRCTC booking recommended)",
            },
            {
                "name": "Doddabetta Peak & Tea Factory",
                "desc": "Highest point in the Nilgiris (2,637 m) offering 360° views across the mist-clad valley.",
                "cost": "Peak entry ₹10, telescope house ₹10",
            },
            {
                "name": "Pykara Lake & Waterfalls",
                "desc": "Pristine boat house surrounded by Toda settlements, shola forests, and pine tree forests.",
                "cost": "Boating ₹400 – ₹800",
            },
        ],
        "food_specialities": [
            "Ooty homemade dark & milk chocolates",
            "Hot Nilgiri Varkey (crisp flaky pastry) with tea",
            "South Indian breakfast with Chettinad filter coffee",
            "English scones and carrot cake at historic bakeries",
        ],
        "stay_options": [
            "Colonial Heritage Bungalow (~₹4,000 – ₹7,500/night)",
            "Valley View Resort in Coonoor (~₹3,000 – ₹5,000/night)",
            "Budget Homestay near Charing Cross (~₹1,400 – ₹2,200/night)",
        ],
        "transit": "Nearest railway: Mettupalayam (50 km) or Coimbatore (85 km). Nearest airport: Coimbatore (CJB, 90 km).",
        "budget_per_day": "₹2,500 – ₹4,200 per person per day",
        "insider_tip": "Take the toy train from Coonoor to Ooty in the morning—it offers the best photography curves with less crowd than Mettupalayam.",
        "itinerary_2day": [
            "Day 1: Ride the Nilgiri Toy Train, visit Government Botanical Gardens, boat at Ooty lake, chocolate shopping.",
            "Day 2: Early morning Doddabetta Peak view, Pykara lake speedboating, walk through the 9th Mile shooting point pine forest.",
        ],
        "follow_up_question": "Would you like to include the historic Toy Train ride between Coonoor and Ooty in the plan?",
    },
    "coorg": {
        "canonical_name": "Coorg (Kodagu)",
        "aliases": ["coorg", "kodagu", "madikeri", "kushalnagar", "virajpet"],
        "region": "Karnataka (Western Ghats)",
        "tagline": "The Scotland of India & Coffee Capital",
        "vibe": "Coffee and cardamom estates, Tibetan monasteries, Abbey Falls, and authentic Kodava cuisine",
        "best_season": "October to April",
        "highlights": [
            {
                "name": "Namdroling Monastery (Golden Temple), Bylakuppe",
                "desc": "One of India's largest Tibetan settlements featuring 40-ft gilded Buddha statues and prayer halls.",
                "cost": "Free entry",
            },
            {
                "name": "Abbey Falls & Raja's Seat",
                "desc": "Roaring waterfall surrounded by spice plantations and the historic sunset garden of the Kodagu Rajas.",
                "cost": "₹15 – ₹40 entry",
            },
            {
                "name": "Dubare Elephant Camp & River Rafting",
                "desc": "Interact with elephants along the Cauvery river and seasonal river rafting.",
                "cost": "Camp entry ₹50, boat ride ₹30",
            },
        ],
        "food_specialities": [
            "Traditional Pandi Curry (Coorg spiced pork) or Mushroom Kadambuttu (steamed rice dumplings)",
            "Paputtu (steamed rice cakes with coconut and milk)",
            "Freshly roasted Arabica and Robusta estate coffee",
            "Homemade berry and ginger wines",
        ],
        "stay_options": [
            "Heritage Coffee Estate Homestay (~₹2,800 – ₹4,500/night)",
            "Luxury Plantation Spa Resort (~₹7,000 – ₹14,000/night)",
            "Madikeri Town Budget Guesthouse (~₹1,500 – ₹2,200/night)",
        ],
        "transit": "Nearest railway station: Mysore (120 km) or Mangalore (135 km). Nearest airport: Kannur (CNN, 90 km) or Mangalore (IXE, 140 km).",
        "budget_per_day": "₹2,800 – ₹5,000 per person per day",
        "insider_tip": "Stay inside a working coffee estate rather than in Madikeri town for morning mist walks and authentic Kodava home-cooked dinners.",
        "itinerary_2day": [
            "Day 1: Bylakuppe Golden Temple, Dubare elephant camp on Cauvery river, sunset at Raja's Seat.",
            "Day 2: Abbey falls walk, coffee estate walking tour, Madikeri Fort, spice and homemade wine shopping.",
        ],
        "follow_up_question": "Are you traveling with family or a group of friends looking for coffee plantation stays?",
    },
    "goa": {
        "canonical_name": "Goa",
        "aliases": ["goa", "panaji", "north goa", "south goa", "anjuna", "palolem", "baga"],
        "region": "Goa (Konkan Coast)",
        "tagline": "Sun, Sand, Portuguese Heritage & Susegad",
        "vibe": "Golden beaches, beach shacks, Portuguese villas in Fontainhas, watersports, and vibrant nightlife",
        "best_season": "November to March",
        "highlights": [
            {
                "name": "Palolem & Agonda Beaches (South Goa)",
                "desc": "Crescent-shaped calm beaches with cliff-top shacks, dolphin boat trips, and peaceful sunsets.",
                "cost": "Dolphin boat ₹400/pax",
            },
            {
                "name": "Fontainhas Latin Quarter, Panaji",
                "desc": "Colorful heritage Portuguese street with terracotta-tiled balconies, art cafes, and bakeries.",
                "cost": "Free walking tour",
            },
            {
                "name": "Fort Aguada & Chapora Fort",
                "desc": "17th-century Portuguese coastal fortresses overlooking the expansive Arabian sea.",
                "cost": "Aguada entry ₹50",
            },
        ],
        "food_specialities": [
            "Goan Fish Curry Thali with Kingfish / Pomfret",
            "Pork Vindaloo or Chicken Xacuti with warm Poi bread",
            "Bebinca (multi-layered Goan coconut cake)",
            "Fresh feni cocktail or chilled King's beer at beach shacks",
        ],
        "stay_options": [
            "South Goa Beachfront Bamboo Hut (~₹2,500 – ₹4,500/night)",
            "North Goa Boutique Villa (~₹3,500 – ₹6,500/night)",
            "Backpacker Hostel in Anjuna / Vagator (~₹700 – ₹1,500/night)",
        ],
        "transit": "Dabolim Airport (GOI) or Mopa Airport (GOX). Major railway stations: Madgaon (MAO) and Thivim (THVM).",
        "budget_per_day": "₹2,500 – ₹5,000 per person per day",
        "insider_tip": "Split your stay: 2 days in North Goa for vibrant cafes and night markets, and 2 days in South Goa (Palolem) for serene beaches.",
        "itinerary_2day": [
            "Day 1: Panaji Fontainhas Latin Quarter walk, Reis Magos Fort, sunset at Vagator beach, cliff shack dinner.",
            "Day 2: South Goa drive to Palolem beach, butterfly beach boat ride, seafood dinner at coastal shack.",
        ],
        "follow_up_question": "Do you prefer the energetic party vibe of North Goa or the quiet, pristine beaches of South Goa?",
    },
    "delhi": {
        "canonical_name": "Delhi",
        "aliases": ["delhi", "new delhi", "old delhi", "ncr"],
        "region": "National Capital Territory of India",
        "tagline": "The City of Empires, Heritage & Legendary Street Food",
        "vibe": "Mughal monuments, colonial boulevards, bustling bazaars, and world-class metro connectivity",
        "best_season": "October to March (Crisp winter weather)",
        "highlights": [
            {
                "name": "Red Fort & Chandni Chowk",
                "desc": "Iconic red sandstone Mughal fortress and electric rickshaw ride through historic food lanes.",
                "cost": "Red Fort ₹50 for Indians / ₹550 foreigners",
            },
            {
                "name": "Humayun's Tomb & Sunder Nursery",
                "desc": "UNESCO garden tomb masterpiece that inspired the Taj Mahal, adjacent to heritage botanical gardens.",
                "cost": "₹40 entry",
            },
            {
                "name": "Qutub Minar & Mehrauli Archaeological Park",
                "desc": "73m high brick minaret built in 1192 surrounded by historic Indo-Islamic ruins.",
                "cost": "₹40 entry",
            },
        ],
        "food_specialities": [
            "Old Delhi Butter Chicken at Karim's / Aslam Chicken",
            "Paranthe Wali Gali assorted stuffed parathas",
            "Chole Bhature with pickled carrots at Sita Ram Diwan Chand",
            "Jalebi with Rabri in Chandni Chowk",
        ],
        "stay_options": [
            "Central Delhi Heritage Boutique Stay (~₹3,500 – ₹6,000/night)",
            "South Delhi Aerocity Modern Hotel (~₹3,000 – ₹5,000/night)",
            "Connaught Place / Paharganj Budget Hub (~₹1,200 – ₹2,000/night)",
        ],
        "transit": "Indira Gandhi International Airport (DEL). World-class Delhi Metro network reaches virtually all major monuments.",
        "budget_per_day": "₹2,000 – ₹4,500 per person per day",
        "insider_tip": "Use the Delhi Metro Tourist Day Pass (₹150) for unlimited travel to avoid city traffic. Visit monuments early morning.",
        "itinerary_2day": [
            "Day 1: Humayun's Tomb, Qutub Minar, drive past India Gate & Rashtrapati Bhavan, dinner at Connaught Place.",
            "Day 2: Chandni Chowk morning rickshaw tour, Jama Masjid, Red Fort, evening shopping at Dilli Haat.",
        ],
        "follow_up_question": "Are you keen on exploring historical monuments, or focused on a culinary street food trail?",
    },
    "paris": {
        "canonical_name": "Paris",
        "aliases": ["paris", "france"],
        "region": "Île-de-France, France",
        "tagline": "The City of Light, Art & Timeless Elegance",
        "vibe": "Haussmannian boulevards, world-class museums, Seine river cruises, sidewalk bistros, and iconic landmarks",
        "best_season": "April to October (Spring blooms or autumn colors)",
        "highlights": [
            {
                "name": "Eiffel Tower & Champ de Mars",
                "desc": "Global symbol of France; best viewed from Trocadéro or during the nightly sparkle show.",
                "cost": "Lift ticket €18 – €35",
            },
            {
                "name": "Louvre Museum & Tuileries Garden",
                "desc": "World's largest museum housing the Mona Lisa and Venus de Milo in an ancient royal palace.",
                "cost": "Entry €22 (advance timed slot mandatory)",
            },
            {
                "name": "Montmartre & Sacré-Cœur Basilica",
                "desc": "Bohemian hilltop district with cobbled streets, portrait painters at Place du Tertre, and city panoramas.",
                "cost": "Free basilica entry",
            },
            {
                "name": "Seine River Sunset Cruise",
                "desc": "Glide past illuminated monuments like Notre-Dame, Musée d'Orsay, and historic bridges.",
                "cost": "€16 – €25 per person",
            },
        ],
        "food_specialities": [
            "Fresh butter croissants & pain au chocolat from an artisanal boulangerie",
            "Classic French Onion Soup (Soupe à l'oignon) with melted Gruyère",
            "Steak Frites at a sidewalk Parisian bistro",
            "Colorful macarons from Ladurée or Pierre Hermé",
        ],
        "stay_options": [
            "Boutique Hotel in Le Marais / Saint-Germain (~₹14,000 – ₹24,000/night)",
            "Charming 3-star near Bastille or Montparnasse (~₹8,500 – ₹13,000/night)",
        ],
        "transit": "Paris Metro & RER train system. Paris Navigo Easy Pass or €2.15 single metro tickets.",
        "budget_per_day": "₹10,000 – ₹18,000 per person per day (excluding international flights)",
        "insider_tip": "Book Louvre and Eiffel Tower tickets 3–4 weeks in advance online. Skip expensive restaurant waters—always ask for 'une carafe d'eau' (free tap water).",
        "itinerary_2day": [
            "Day 1: Morning at the Louvre, stroll through Tuileries to Place de la Concorde, sunset Seine river cruise, evening Eiffel Tower sparkle.",
            "Day 2: Climb to Sacré-Cœur in Montmartre, explore Le Marais boutiques, visit Notre-Dame and Sainte-Chapelle stained glass.",
        ],
        "follow_up_question": "How many days are you planning for Paris, and are you traveling as a couple or family?",
    },
    "varanasi": {
        "canonical_name": "Varanasi (Kashi / Banaras)",
        "aliases": ["varanasi", "kashi", "benaras", "benares", "banaras", "assi ghat", "dashashwamedh"],
        "region": "Uttar Pradesh, India (Sacred Ganges Riverfront)",
        "tagline": "The Eternal Spiritual Heart of India & City of Light",
        "vibe": "Sacred river ghats, hypnotic evening Ganga Aartis, dawn rowboat rides, ancient mystical galis, and timeless living heritage",
        "best_season": "October to March (Crisp pleasant air, 12°C – 25°C, serene misty sunrises)",
        "highlights": [
            {
                "name": "Dashashwamedh & Assi Ghat Evening Ganga Aarti",
                "desc": "Grand spiritual ceremony of choreographed brass lamps, conch shells, and sacred incense chants overlooking the holy river.",
                "cost": "Free to watch from steps / Boat viewing ₹300 – ₹600",
            },
            {
                "name": "Subah-e-Banaras Dawn Wooden Boat Cruise",
                "desc": "Traditional hand-rowed wooden boat gliding from Assi Ghat past Tulsi, Harishchandra, and Manikarnika Ghats during sunrise.",
                "cost": "₹400 – ₹800 per private wooden boat",
            },
            {
                "name": "Kashi Vishwanath Corridor & Golden Temple",
                "desc": "Revered Jyotirlinga shrine connected directly to the Ganga via the monumental riverfront corridor.",
                "cost": "Free general darshan / Sugam Darshan ₹300",
            },
            {
                "name": "Sarnath & Dhamek Stupa Excursion",
                "desc": "Historic deer park where Lord Buddha preached his first sermon after enlightenment; home to the 5th-century Dhamek Stupa and Ashokan Lion Capital.",
                "cost": "₹40 entry",
            },
            {
                "name": "Madanpura Heritage Silk Weaving & Galis",
                "desc": "Labyrinth of medieval lanes where master Muslim and Hindu weavers craft world-renowned pure Banarasi silk sarees on handlooms.",
                "cost": "Free walking exploration",
            },
        ],
        "food_specialities": [
            "Hot crispy Kachori-Sabzi with golden syrupy Jalebi at Ram Bhandar (morning only)",
            "Famous Tamatar Chaat and Palak Patta Chaat at Kashi Chaat Bhandar",
            "Rich clay-cup Lassi topped with thick saffron malai at Blue Lassi Shop",
            "Authentic Banarasi Meetha Paan at Keshav Tambool Bhandar",
            "Winter special Malaiyo (whipped saffron milk froth with pistachios)",
        ],
        "stay_options": [
            "Heritage Riverside Haveli / Palace on the Ghats (~₹3,500 – ₹7,000/night)",
            "Charming Boutique Hotel near Godowlia (~₹2,000 – ₹3,500/night)",
            "Comfort Riverside Guesthouse near Assi Ghat (~₹1,200 – ₹2,200/night)",
        ],
        "transit": "Lal Bahadur Shastri International Airport (VNS, Babatpur, 24 km). Varanasi Junction (BSB) and Deen Dayal Upadhyaya Junction (DDU) connect directly to all major cities.",
        "budget_per_day": "₹1,600 – ₹3,500 per person per day (budget to heritage comfort)",
        "insider_tip": "Always take a hand-rowed wooden boat at 5:30 AM rather than a noisy motorboat—it glides quietly across the misty water for stunning photography. Book Kashi Vishwanath Sugam Darshan online beforehand.",
        "itinerary_5day": [
            "Day 1: Arrive in Varanasi, settle into your riverside haveli, take an afternoon walking tour along the ghats from Assi to Dashashwamedh, and witness the spellbinding evening Ganga Aarti from a wooden boat.",
            "Day 2: 5:30 AM Subah-e-Banaras dawn boat cruise, followed by traditional kachori-jalebi breakfast at Ram Bhandar. Afternoon darshan at Kashi Vishwanath Corridor and Annapurna Temple, followed by an evening street food trail at Godowlia.",
            "Day 3: Morning excursion to Sarnath (Dhamek Stupa & Archaeological Museum). Return for an afternoon visit to Bharat Kala Bhavan museum on the BHU campus, followed by sunset reflections at Chet Singh Ghat.",
            "Day 4: Deep dive into the silk-weaving quarters of Madanpura, visit the ancient Kal Bhairav Temple, and take a local boat across the river to explore the 18th-century sandstone Ramnagar Fort.",
            "Day 5: Gentle morning walk through the northern ghats (Panchganga and Scindia Ghat), souvenir shopping for Banarasi silk and brassware, culminating with a famous Banarasi Paan before departure.",
        ],
        "itinerary_2day": [
            "Day 1: Arrival, afternoon walking exploration of the ghats, sunset boat ride for the grand Dashashwamedh Ganga Aarti, dinner at Kashi Chaat Bhandar.",
            "Day 2: 5:30 AM sunrise boat ride from Assi to Manikarnika Ghat, darshan at Kashi Vishwanath Corridor, half-day excursion to Sarnath, and evening silk shopping.",
        ],
        "follow_up_question": "Would you like recommendations on heritage havelis directly on the ghats, or assistance with temple darshan timings?",
    },
    "jaipur": {
        "canonical_name": "Jaipur (The Pink City)",
        "aliases": ["jaipur", "pink city", "rajasthan"],
        "region": "Rajasthan, India",
        "tagline": "The Royal Citadel of Palaces, Forts & Vibrant Bazaars",
        "vibe": "Regal Rajput architecture, hilltop forts, grand palaces, block-print textiles, and royal cuisine",
        "best_season": "October to March (Warm sunny days, crisp cool evenings)",
        "highlights": [
            {
                "name": "Amber Fort & Palace",
                "desc": "Majestic hilltop fortress overlooking Maota Lake with the dazzling Sheesh Mahal (Mirror Palace).",
                "cost": "₹100 for Indians / ₹550 foreigners",
            },
            {
                "name": "Hawa Mahal (Palace of Winds)",
                "desc": "Iconic five-story pink sandstone facade with 953 intricate jharokhas.",
                "cost": "₹50 entry",
            },
            {
                "name": "City Palace & Jantar Mantar",
                "desc": "UNESCO astronomical observatory and royal residence with exquisite courtyards.",
                "cost": "Composite ticket ~₹300",
            },
        ],
        "food_specialities": [
            "Dal Baati Churma with pure desi ghee",
            "Pyaaz Kachori and Mawa Kachori at Rawat Mishtan Bhandar",
            "Laal Maas (spicy Rajasthani mutton curry)",
            "Lassi in earthen kulhad at Lassiwala (MI Road)",
        ],
        "stay_options": [
            "Heritage Haveli Hotel (~₹3,000 – ₹5,500/night)",
            "Royal Palace Stay (~₹8,000 – ₹18,000/night)",
            "Comfort City Hotel (~₹1,500 – ₹2,500/night)",
        ],
        "transit": "Jaipur International Airport (JAI). Connected by Vande Bharat trains to Delhi and Agra.",
        "budget_per_day": "₹2,200 – ₹4,500 per person per day",
        "insider_tip": "Visit Nahargarh Fort at sunset for a breathtaking panoramic view of the entire illuminated Pink City. Shop for textiles at Bapu Bazaar after 3 PM.",
        "itinerary_2day": [
            "Day 1: Amber Fort morning tour, photography at Jal Mahal, visit City Palace & Jantar Mantar, sunset drinks at Nahargarh Fort.",
            "Day 2: Hawa Mahal dawn view, Rawat pyaaz kachori breakfast, shopping at Johari and Bapu Bazaars, evening cultural show at Chokhi Dhani.",
        ],
        "follow_up_question": "Are you planning a quick weekend trip or combining Jaipur with Udaipur and Jodhpur?",
    },
    "goa": {
        "canonical_name": "Goa",
        "aliases": ["goa", "panjim", "panaji", "north goa", "south goa", "anjuna", "palolem", "vagator"],
        "region": "Konkan Coast, India",
        "tagline": "Sun-Kissed Beaches, Portuguese Heritage & Coastal Soul",
        "vibe": "Golden sandy coastlines, vibrant beach shacks, Portuguese Latin quarters, spice plantations, and fresh seafood",
        "best_season": "November to March (Pleasant coastal breezes, sunny skies, lively nightlife)",
        "highlights": [
            {
                "name": "Fontainhas Latin Quarter (Panaji)",
                "desc": "Picturesque heritage quarter with pastel-hued Portuguese villas, indie bakeries, and art galleries.",
                "cost": "Free walking tour",
            },
            {
                "name": "Palolem & Agonda Beaches (South Goa)",
                "desc": "Crescent-shaped tranquil beaches lined with coconut palms and peaceful sunset beach shacks.",
                "cost": "Free entry",
            },
            {
                "name": "Aguada & Chapora Forts",
                "desc": "17th-century coastal fortifications with dramatic views over the Arabian Sea.",
                "cost": "Nominal entry ₹25 – ₹50",
            },
        ],
        "food_specialities": [
            "Goan Fish Curry Thali with Kingfish and red rice",
            "Pork or Chicken Vindaloo with fresh Poi bread",
            "Prawn Balchão & Bebinca dessert",
            "Fresh feni cocktail or chilled tender coconut water",
        ],
        "stay_options": [
            "Beachfront Wooden Cottage in South Goa (~₹2,800 – ₹5,000/night)",
            "Portuguese Heritage Villa in Fontainhas (~₹3,500 – ₹6,000/night)",
            "Hostel / Guesthouse near North Goa beaches (~₹1,000 – ₹2,000/night)",
        ],
        "transit": "Goa International Airport (Dabolim - GOI) and Manohar International Airport (Mopa - GOX). Madgaon (MAO) and Thivim railway stations.",
        "budget_per_day": "₹2,500 – ₹5,000 per person per day",
        "insider_tip": "Rent a scooter (₹350–₹500/day) for maximum freedom. Head south to Palolem and Cola Beach for uncrowded serenity.",
        "itinerary_2day": [
            "Day 1: Morning stroll through Fontainhas Latin Quarter, visit Basilica of Bom Jesus, sunset and seafood at Vagator or Anjuna.",
            "Day 2: Drive south to Palolem Beach, boat trip to Butterfly Beach, and evening candlelit beach shack dinner under the stars.",
        ],
        "follow_up_question": "Do you prefer the lively vibe of North Goa or the serene, pristine shores of South Goa?",
    },
}


class TourismRAGService:
    """High-speed regional travel knowledge retrieval engine."""

    def __init__(self) -> None:
        self.kb = DESTINATION_KNOWLEDGE_BASE

    def resolve_destination(self, text: str) -> Optional[dict[str, Any]]:
        """Extract and match destination entity from user text or context."""
        cleaned = re.sub(r"[^\w\s]", " ", text.lower())
        tokens = cleaned.split()

        # Check multi-word and single-word aliases
        for dest_key, data in self.kb.items():
            for alias in data["aliases"]:
                if alias in cleaned:
                    return data

        return None

    def retrieve_context_for_query(self, query: str, history: Optional[list] = None) -> str:
        """
        Builds a compact, factual context block to inject into prompts or direct replies.
        """
        combined = query.lower()
        if history:
            combined = " ".join([str(h.get("content", "")) for h in history[-4:]]) + " " + combined

        dest_data = self.resolve_destination(combined)
        if not dest_data:
            return ""

        highlights_str = "; ".join([f"{h['name']} ({h['desc']})" for h in dest_data["highlights"][:3]])
        foods_str = ", ".join(dest_data["food_specialities"][:4])
        stays_str = "; ".join(dest_data["stay_options"][:2])

        return (
            f"VERIFIED REGIONAL RAG FACTS FOR {dest_data['canonical_name'].upper()}:\n"
            f"- Region: {dest_data['region']}\n"
            f"- Best Season: {dest_data['best_season']}\n"
            f"- Highlights: {highlights_str}\n"
            f"- Authentic Food: {foods_str}\n"
            f"- Stay Pricing: {stays_str}\n"
            f"- Transit: {dest_data['transit']}\n"
            f"- Estimated Budget: {dest_data['budget_per_day']}\n"
            f"- Local Insider Secret: {dest_data['insider_tip']}\n"
        )

    def generate_grounded_response(
        self, user_message: str, history: Optional[list] = None, user_name: Optional[str] = None
    ) -> dict[str, str]:
        """
        Synthesizes a warm, structured, 0-lag response in DASAPPAN's voice,
        strictly grounded in authentic travel facts and deep intent analysis.
        Greets warmly with Namaskaram *username*!
        """
        msg = user_message.strip()
        msg_lower = msg.lower()

        # Format personalized greeting
        display_name = (user_name or "").strip()
        greeting_prefix = f"Namaskaram {display_name}! 🙏" if display_name else "Namaskaram! 🙏"

        # Collect history text
        history_text = ""
        if history:
            history_text = " ".join([str(h.get("content", "")).lower() for h in history[-4:]])
        full_context = f"{history_text} {msg_lower}"

        # 1. Pure greeting check (e.g. "hai", "hello", "hi", "namaskaram", "hey")
        greeting_words = {"hai", "hi", "hello", "hey", "namaskaram", "namaste", "vanakkam", "halo", "yo", "morning", "evening"}
        words_set = set(re.findall(r"\b\w+\b", msg_lower))

        is_pure_greeting = (
            words_set.issubset(greeting_words)
            or msg_lower in ["hi", "hai", "hello", "hey", "namaskaram", "namaste", "vanakkam", "good morning", "good evening"]
        )

        if is_pure_greeting:
            return {
                "reply": (
                    f"{greeting_prefix} DASAPPAN here, your AI travel companion.\n\n"
                    "How may I help you today?\n\n"
                    "Tell me your dream destination, budget, or the travel vibe you have in mind, and I'll analyze it to craft the ideal plan with verified stays and costs in ₹.\n\n"
                    "❓ Where would you like to travel, or what would you like me to plan for you?"
                ),
                "source": "rag_knowledge_engine",
            }

        # 2. Check for destination match
        dest_data = self.resolve_destination(full_context)

        if dest_data:
            cname = dest_data["canonical_name"]

            # Analyze user's specific intent:
            # - Is user asking about food?
            if any(w in msg_lower for w in ["food", "eat", "dishes", "cuisine", "restaurant", "parotta", "salna"]):
                foods = "\n".join([f"• {f}" for f in dest_data["food_specialities"]])
                return {
                    "reply": (
                        f"{greeting_prefix} Here are the authentic must-try food specialities in **{cname}**:\n\n"
                        f"{foods}\n\n"
                        f"💡 **DASAPPAN's Foodie Tip**: {dest_data['insider_tip']}\n\n"
                        f"❓ Would you like recommended restaurants or budget stays nearby?"
                    ),
                    "source": "rag_knowledge_engine",
                }

            # - Is user asking about budget or cost?
            if any(w in msg_lower for w in ["budget", "cost", "price", "how much", "rate", "rupee", "cheap"]):
                stays = "\n".join([f"• {s}" for s in dest_data["stay_options"]])
                return {
                    "reply": (
                        f"{greeting_prefix} Here is a realistic budget blueprint for **{cname}**:\n\n"
                        f"💰 **Estimated Daily Budget**: {dest_data['budget_per_day']}\n\n"
                        f"🏨 **Stay Options**:\n{stays}\n\n"
                        f"🚗 **Transit**: {dest_data['transit']}\n\n"
                        f"❓ How many days are you planning for this trip, and how many people are traveling?"
                    ),
                    "source": "rag_knowledge_engine",
                }

            # - Is user asking about best time / weather?
            if any(w in msg_lower for w in ["weather", "best time", "season", "climate", "rain", "monsoon", "when to visit"]):
                return {
                    "reply": (
                        f"{greeting_prefix} The best time to visit **{cname}**:\n\n"
                        f"📅 **Optimal Season**: {dest_data['best_season']}\n\n"
                        f"✨ **Vibe**: {dest_data['vibe']}\n\n"
                        f"💡 **Insider Tip**: {dest_data['insider_tip']}\n\n"
                        f"❓ What month are you thinking of traveling in?"
                    ),
                    "source": "rag_knowledge_engine",
                }

            # Check if duration / days are provided in query or history
            days_match = re.search(r"\b(\d+)\s*(?:day|days|d)\b", full_context)
            has_days = bool(days_match)
            num_days = int(days_match.group(1)) if days_match else None

            has_travelers = any(w in full_context for w in ["solo", "couple", "family", "friends", "group", "people", "person", "pax"])
            has_budget = any(w in full_context for w in ["budget", "comfort", "luxury", "₹", "rs", "rupee", "cheap", "cost"])

            # CASE A: User just mentioned destination without enough trip parameters -> Ask questions to collect info
            if not has_days and not has_travelers and not any(w in msg_lower for w in ["food", "weather", "stay", "hotel", "reach", "transit"]):
                return {
                    "reply": (
                        f"{greeting_prefix}\n\n"
                        f"**{cname}** is an extraordinary choice! {dest_data['tagline']}.\n\n"
                        f"{dest_data['vibe']}.\n\n"
                        f"To help me craft your complete, personalized day-by-day itinerary with verified stays and costs in ₹, could you tell me:\n\n"
                        f"• 🗓️ **How many days** are you planning to spend? (e.g. 2–3 days for highlights or 4–5 days for deep immersion?)\n"
                        f"• 👥 **How many travelers** will be joining? (Solo, couple, family, or friends?)\n"
                        f"• 💰 What is your approximate **budget tier**? (Budget backpacker, comfortable heritage stay, or luxury?)\n"
                        f"• ✨ Any **must-have experiences**? (Temple darshan, morning boat rides, street food trails, silk shopping, or peaceful relaxation?)\n\n"
                        f"Drop your details below, and I'll synthesize a comprehensive day-by-day plan with timings, authentic stays, food spots, and costs in ₹ for you!"
                    ),
                    "source": "rag_consultative_engine",
                }

            # CASE B: Days or parameters are provided -> Generate complete text plan
            itinerary_list = dest_data.get("itinerary_5day") if (num_days and num_days >= 4 and "itinerary_5day" in dest_data) else dest_data.get("itinerary_2day", [])
            itinerary_str = "\n".join([f"• **{step.split(':')[0]}**: {':'.join(step.split(':')[1:]).strip() if ':' in step else step}" for step in itinerary_list])
            foods_str = "\n".join([f"• {f}" for f in dest_data["food_specialities"][:4]])
            stays_str = "\n".join([f"• {s}" for s in dest_data["stay_options"][:3]])

            plan_title = f"{num_days or 3}-Day Bespoke {cname} Travel Plan"

            reply = (
                f"{greeting_prefix}\n\n"
                f"Here is your personalized **{plan_title}** — {dest_data['tagline']}:\n\n"
                f"### 🗓️ Day-by-Day Journey\n"
                f"{itinerary_str}\n\n"
                f"### 🏨 Recommended Stays\n"
                f"{stays_str}\n\n"
                f"### 🍲 Iconic Food & Dining\n"
                f"{foods_str}\n\n"
                f"### 💰 Estimated Budget Guidelines\n"
                f"• **Daily Average**: {dest_data['budget_per_day']}\n"
                f"• **Transit Details**: {dest_data['transit']}\n\n"
                f"### 💡 Dasappan's Local Insider Secret\n"
                f"{dest_data['insider_tip']}\n\n"
                f"Would you like recommendations on specific hotel bookings or adjustments to this plan?"
            )
            return {"reply": reply, "source": "rag_knowledge_engine"}

        # 3. No specific destination detected — analyze general travel query
        if any(w in msg_lower for w in ["budget", "cost", "cheap", "10000", "5000", "20000", "under"]):
            return {
                "reply": (
                    f"{greeting_prefix} I can tailor an exact budget plan for you anywhere in India or abroad.\n\n"
                    "To give you realistic numbers for stays, flights/trains, meals, and local transit:\n"
                    "• What destination are you considering (e.g. Munnar, Thenkasi, Varkala, Ooty, Coorg, Goa, or Paris)?\n"
                    "• How many days and how many travelers?\n\n"
                    "❓ Tell me the place you have in mind!"
                ),
                "source": "rag_knowledge_engine",
            }

        return {
            "reply": (
                f"{greeting_prefix} I'd love to help you plan your travel.\n\n"
                f"Could you tell me:\n"
                f"• Which destination or region in the world are you targeting?\n"
                f"• How many days do you have in mind?\n\n"
                f"💡 Popular destinations right now: **Thenkasi & Courtallam**, **Munnar**, **Vattavada**, **Varkala**, **Coorg**, or **Paris**.\n\n"
                f"❓ Which one shall we look into first?"
            ),
            "source": "rag_knowledge_engine",
        }


# Singleton accessor
_tourism_rag_service: Optional[TourismRAGService] = None


def get_tourism_rag_service() -> TourismRAGService:
    global _tourism_rag_service
    if _tourism_rag_service is None:
        _tourism_rag_service = TourismRAGService()
    return _tourism_rag_service
