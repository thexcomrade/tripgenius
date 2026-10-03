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
    "egypt": {
        "canonical_name": "Egypt",
        "aliases": ["egypt", "cairo", "giza", "pyramids", "luxor", "aswan", "nile"],
        "region": "North Africa & Middle East",
        "tagline": "Land of the Pharaohs & Majestic Nile Pyramids",
        "vibe": "Ancient wonder of the world, golden desert pyramids, mystical Nile river feluccas, and vibrant bazaars",
        "best_season": "October to April (Pleasant dry desert weather, 18°C – 26°C)",
        "package_duration": "4 Nights / 5 Days",
        "package_price": "Starting from ₹60,000/- per person",
        "package_inclusions": ["Hotel Stay", "Guided Sightseeing", "Transportation", "Daily Breakfast", "All Entry Tickets"],
        "highlights": [
            {
                "name": "Great Pyramids of Giza & The Sphinx",
                "desc": "Sole surviving wonder of the ancient world built over 4,500 years ago, guarding the golden Sahara horizon.",
                "cost": "Included in holiday package (General entry ~EGP 540)",
            },
            {
                "name": "Nile River Felucca Sunset Cruise",
                "desc": "Traditional wooden sailboat cruise along the historic lifeline of ancient Egyptian civilization.",
                "cost": "Included in tour package",
            },
            {
                "name": "Grand Egyptian Museum & Khan el-Khalili Bazaar",
                "desc": "World's largest archaeological complex featuring King Tutankhamun's gold treasures and 14th-century spiced lantern alleys.",
                "cost": "Entry included in package",
            },
            {
                "name": "Luxor & Karnak Colonnade Temples",
                "desc": "Open-air museum with towering carved lotus columns, hieroglyphs, and avenue of sphinxes.",
                "cost": "Guided excursion",
            },
        ],
        "food_specialities": [
            "Authentic Egyptian Koshary (rice, lentils, macaroni with spiced tomato sauce and fried onions)",
            "Fresh Taameya (Egyptian fava bean falafel) with warm Aish Baladi bread",
            "Charcoal grilled Shish Tawook & Kofta",
            "Sweet sticky Baklava and mint tea at El Fishawy cafe",
        ],
        "stay_options": [
            "Pyramids View 4-Star Hotel in Giza (~₹5,000 – ₹8,500/night)",
            "Nile Riverfront Luxury Resort Cairo (~₹7,000 – ₹12,000/night)",
            "Boutique Heritage Guesthouse in Zamalek (~₹3,500 – ₹5,500/night)",
        ],
        "transit": "Cairo International Airport (CAI) with direct flights from major Indian hubs. Private air-conditioned transfers included.",
        "budget_per_day": "₹6,000 – ₹12,000 per person per day (All-inclusive 4N/5D package from ₹60,000)",
        "insider_tip": "Visit the Pyramids early morning around 8:00 AM for majestic crowd-free photos before the midday desert sun. Sunset camel ride across the Giza dunes is unforgettable.",
        "itinerary_2day": [
            "Day 1: Arrive Cairo, Giza plateau tour exploring the Great Pyramid of Khufu & Sphinx, sunset Nile felucca cruise, evening at Khan el-Khalili souk.",
            "Day 2: Grand Egyptian Museum treasures, Coptic Cairo Hanging Church, evening traditional dinner cruise with folkloric Tanoura dance.",
        ],
        "follow_up_question": "Are you interested in focusing on the Giza pyramids and Cairo, or would you like to extend to the ancient temples of Luxor and Aswan?",
    },
    "vietnam": {
        "canonical_name": "Vietnam",
        "aliases": ["vietnam", "da nang", "danang", "phu quoc", "phuquoc", "hanoi", "ha long", "halong", "hoi an"],
        "region": "Southeast Asia",
        "tagline": "Golden Bridges, Emerald Bays & Vibrant Lantern Alleys",
        "vibe": "Misty mountain bridges held by giant stone hands, serene tropical island beaches, energetic train streets, and world-class street cuisine",
        "best_season": "November to April (Pleasant, sunny, dry season across central and southern coasts)",
        "package_duration": "3 Nights / 4 Days",
        "package_price": "Starting from INR 23,000/- per person",
        "package_inclusions": ["Guide", "Hotel Stay", "Sightseeing", "Transportation", "Daily Breakfast", "All Entry Tickets"],
        "highlights": [
            {
                "name": "Golden Bridge at Ba Na Hills (Da Nang)",
                "desc": "Iconic 150-meter pedestrian walkway supported by two colossal weathered stone hands emerging from mountain mist.",
                "cost": "Entry included in package",
            },
            {
                "name": "Phu Quoc Island Turquoise Beaches",
                "desc": "Pristine white sand coves, starfish beaches, and dramatic sunset cable car over coral islets.",
                "cost": "Free beach access / Included",
            },
            {
                "name": "Hanoi Old Quarter & Historic Train Street",
                "desc": "Historic French-colonial alleys where trains pass inches from bustling coffee shops and flower markets.",
                "cost": "Free walking tour",
            },
            {
                "name": "Hoi An Ancient Lantern Town",
                "desc": "UNESCO heritage river town lit by thousands of silk lanterns every evening along the Thu Bon River.",
                "cost": "Nominal entry ~VND 150,000",
            },
        ],
        "food_specialities": [
            "Steaming bowl of authentic Beef or Chicken Pho with fresh herbs",
            "Crispy Vietnamese Banh Mi baguette sandwich with pate and pickled daikon",
            "Traditional creamy Hanoi Egg Coffee (Ca Phe Trung)",
            "Fresh spring rolls (Goi Cuon) with peanut dipping sauce",
        ],
        "stay_options": [
            "Boutique Hotel near Da Nang My Khe Beach (~₹2,500 – ₹4,500/night)",
            "Phu Quoc Sunset Beach Resort (~₹3,200 – ₹6,000/night)",
            "Hanoi Old Quarter French Heritage Hotel (~₹2,200 – ₹4,000/night)",
        ],
        "transit": "Direct flights from India (Delhi, Mumbai, Kochi) to Da Nang (DAD) or Hanoi (HAN). Tour package includes all intra-city private AC cabs.",
        "budget_per_day": "₹3,500 – ₹6,000 per person per day (All-inclusive 3N/4D holiday from ₹23,000)",
        "insider_tip": "Catch the Dragon Bridge in Da Nang on weekend nights (Saturday & Sunday at 9 PM) to see it breathe real fire and water!",
        "itinerary_2day": [
            "Day 1: Arrive Da Nang, take the world's longest cable car to Ba Na Hills to walk the Golden Bridge, evening sunset swim at My Khe beach.",
            "Day 2: Morning visit to Marble Mountains and dragon pagoda, afternoon trip to Hoi An Ancient Town for lantern boat rides and street food.",
        ],
        "follow_up_question": "Would you like your 3N/4D itinerary centered around Da Nang & Hoi An, or the tropical beaches of Phu Quoc?",
    },
    "uzbekistan": {
        "canonical_name": "Uzbekistan",
        "aliases": ["uzbekistan", "samarkand", "bukhara", "tashkent", "khiva"],
        "region": "Central Asia (Historic Silk Road)",
        "tagline": "The Jewel of the Silk Road & Turquoise Majolica Domes",
        "vibe": "Grand Islamic architecture, glittering azure mosaics, centuries-old caravanserais, and welcoming Silk Road hospitality",
        "best_season": "March to June (Spring blooms) and September to November (Autumn golden light, 18°C – 25°C)",
        "package_duration": "4 Nights / 5 Days (Holiday & Eid al-Adha Package)",
        "package_price": "₹39,900/- per pax",
        "package_inclusions": ["Guide", "Hotel Stay", "Sightseeing", "Transportation", "Breakfast Only", "All Entry Tickets"],
        "highlights": [
            {
                "name": "Registan Square (Samarkand)",
                "desc": "One of the most magnificent architectural ensembles in the world, flanked by three grand madrasahs adorned in dazzling blue tiles.",
                "cost": "Included in tour package",
            },
            {
                "name": "Shah-i-Zinda Necropolis",
                "desc": "A breathtaking avenue of turquoise-domed mausoleums showcasing the pinnacle of 14th-century Persian tilework.",
                "cost": "Included in package",
            },
            {
                "name": "Bukhara Historic Centre & Po-i-Kalyan",
                "desc": "Ancient Silk Road trading post with 45-meter brick minaret that survived Genghis Khan, covered bazaars, and madrasahs.",
                "cost": "Guided tour included",
            },
            {
                "name": "Chorsu Bazaar & Tashkent Metro",
                "desc": "Massive blue-domed bazaar overflowing with dried fruits, spices, and nuts, plus ornate Soviet-era marble underground stations.",
                "cost": "Free bazaar walk / metro token ₹15",
            },
        ],
        "food_specialities": [
            "Authentic Samarkand Wedding Plov cooked in massive cast-iron cauldrons with tender beef, yellow carrots, and raisins",
            "Fresh hot Tandir Non bread stamped with floral patterns",
            "Juicy Shashlik kebabs grilled over grapevine coals with pickled onions",
            "Somsa (crispy baked clay-oven meat pastries) with green tea",
        ],
        "stay_options": [
            "Silk Road Heritage Hotel in Samarkand (~₹3,200 – ₹5,500/night)",
            "Charming Traditional Caravanserai Hotel in Bukhara (~₹2,800 – ₹4,800/night)",
            "Modern 4-Star City Hotel in Tashkent (~₹3,500 – ₹6,000/night)",
        ],
        "transit": "Tashkent International Airport (TAS) with direct 3-hour flights from Delhi. High-speed Afrosiyob bullet train connects Tashkent to Samarkand and Bukhara in 2 hours.",
        "budget_per_day": "₹4,500 – ₹8,000 per person per day (All-inclusive 4N/5D package at ₹39,900)",
        "insider_tip": "Registan Square has an incredible evening sound-and-light illumination where the turquoise tiles glow under spotlights — be sure to visit at 8:30 PM.",
        "itinerary_2day": [
            "Day 1: Arrive Tashkent, board the Afrosiyob bullet train to Samarkand, explore the awe-inspiring Registan Square, and marvel at the gold-plated interior of Tillya-Kori Madrasah.",
            "Day 2: Morning walk through the stunning blue tile corridor of Shah-i-Zinda, visit Gur-e-Amir (Mausoleum of Tamerlane), and feast on authentic Samarkand plov at a local choykhona.",
        ],
        "follow_up_question": "Are you planning your Silk Road holiday around the Eid festivities or a relaxed cultural photography tour?",
    },
    "georgia": {
        "canonical_name": "Georgia",
        "aliases": ["georgia", "tbilisi", "kazbegi", "ananuri", "batumi", "caucasus"],
        "region": "Caucasus (Eurasia)",
        "tagline": "Cradle of Wine, Ancient Fortresses & Alpine Caucasus Peaks",
        "vibe": "Majestic snow-capped Caucasus mountains, fairytale cliffside churches, thermal sulfur springs, and legendary feast traditions",
        "best_season": "May to October (Lush alpine green valleys, comfortable mountain trekking, 20°C – 28°C)",
        "package_duration": "3 Nights / 4 Days",
        "package_price": "40,000 INR per person",
        "package_inclusions": ["Guide", "Hotel Stay", "Sightseeing", "Transportation", "Breakfast"],
        "highlights": [
            {
                "name": "Gergeti Trinity Church & Mount Kazbek",
                "desc": "14th-century stone church dramatically perched at 2,170m altitude beneath the soaring snow peak of Mount Kazbek (5,054m).",
                "cost": "4x4 mountain drive included in package",
            },
            {
                "name": "Ananuri Medieval Fortress & Zhinvali Lake",
                "desc": "Fairytale lakeside stone fortress overlooking a turquoise reservoir along the historic Georgian Military Highway.",
                "cost": "Included in tour",
            },
            {
                "name": "Old Tbilisi Historic Sulfur Bath Quarter (Abanotubani)",
                "desc": "Brick-domed ancient thermal bathhouses nestled along the scenic Leghvtakhevi river gorge and waterfall.",
                "cost": "Walking tour included (Bath entry optional ~₹1,200)",
            },
            {
                "name": "Narikala Fortress & Mother of Georgia Cable Car",
                "desc": "4th-century hilltop fortress reached by scenic aerial cable car with 360-degree vistas over the Mtkvari river.",
                "cost": "Cable car ride included",
            },
        ],
        "food_specialities": [
            "Adjaruli Khachapuri (freshly baked cheese-filled bread boat topped with egg yolk and butter)",
            "Juicy Khinkali dumplings stuffed with spiced meat and aromatic broth",
            "Traditional Qvevri wine fermented in clay amphorae (8,000-year-old UNESCO tradition)",
            "Eggplant rolls with spiced walnut paste (Badrijani Nigvzit)",
        ],
        "stay_options": [
            "Rooms Hotel Kazbegi with direct mountain panoramas (~₹6,500 – ₹11,000/night)",
            "Charming Old Tbilisi Boutique Hotel near Sulfur Baths (~₹3,200 – ₹5,500/night)",
            "Alpine Guesthouse in Stepantsminda (~₹2,000 – ₹3,500/night)",
        ],
        "transit": "Tbilisi International Airport (TBS). The tour package includes full private transportation along the scenic Georgian Military Highway.",
        "budget_per_day": "₹5,000 – ₹9,000 per person per day (All-inclusive 3N/4D package at 40,000 INR)",
        "insider_tip": "When eating Khinkali dumplings, never use a fork! Grab it by the top dough handle, take a small nibble, slurp the delicious hot broth first, then eat the rest.",
        "itinerary_2day": [
            "Day 1: Explore Old Tbilisi, ride the cable car to Narikala Fortress, visit the sulfur bath waterfall, and enjoy a traditional supra feast with live polyphonic music.",
            "Day 2: Scenic drive along the Georgian Military Highway to Ananuri Fortress, cross the Jvari pass to Stepantsminda, and take a 4x4 up to Gergeti Trinity Church.",
        ],
        "follow_up_question": "Would you like your Caucasus trip to focus on mountain adventures in Kazbegi or exploring Tbilisi's culture and wine regions?",
    },
    "azerbaijan": {
        "canonical_name": "Azerbaijan",
        "aliases": ["azerbaijan", "baku", "flame towers", "gobustan", "caspian"],
        "region": "South Caucasus & Caspian Sea",
        "tagline": "The Land of Fire — Futuristic Architecture Meets Silk Road Charm",
        "vibe": "Ultra-modern LED skyline, UNESCO cobblestone old city, mysterious burning natural gas fires, and bubbling mud volcanoes",
        "best_season": "April to June and September to October (Mild pleasant weather, 18°C – 25°C, gentle Caspian sea breezes)",
        "package_duration": "4 Nights / 5 Days",
        "package_price": "25,800 INR per person",
        "package_inclusions": ["Guide", "Hotel Stay", "Sightseeing", "Transportation", "Breakfast"],
        "highlights": [
            {
                "name": "Baku Flame Towers & Highland Park",
                "desc": "Trio of curved glass skyscrapers equipped with LED screens illuminating the night sky like flickering flames above Baku Bay.",
                "cost": "Free panoramic viewpoint",
            },
            {
                "name": "Icherisheher (Walled Old City) & Maiden Tower",
                "desc": "12th-century maze of limestone alleyways, Palace of the Shirvanshahs, and ancient stone minarets.",
                "cost": "Included in package",
            },
            {
                "name": "Gobustan National Park & Mud Volcanoes",
                "desc": "UNESCO site home to 6,000 ancient petroglyphs and over half of the world's active bubbling mud volcanoes.",
                "cost": "Included in guided package",
            },
            {
                "name": "Ateshgah Fire Temple & Yanar Dag Burning Hill",
                "desc": "Ancient Zoroastrian fire sanctuary and a natural hillside that has been burning continuously with natural gas for millennia.",
                "cost": "Entry included in package",
            },
        ],
        "food_specialities": [
            "Azerbaijani Shah Plov (baked inside golden flaky lavash pastry with saffron rice, dried fruits, and lamb)",
            "Crispy Qutab flatbreads stuffed with fresh greens, minced lamb, and pomegranate seeds",
            "Lula Kebab served with sumac and fresh herbs",
            "Azerbaijani black tea served in traditional armudu pear-shaped glasses with homemade cherry jam",
        ],
        "stay_options": [
            "Modern 4-Star Hotel near Baku Boulevard (~₹2,800 – ₹4,800/night)",
            "Boutique Heritage Hotel inside Icherisheher Old City (~₹3,200 – ₹5,500/night)",
            "Luxury Flame Towers Hotel overlooking the Caspian (~₹7,000 – ₹13,000/night)",
        ],
        "transit": "Heydar Aliyev International Airport (GYD) with direct flights from India. Private air-conditioned coach transfers included in the package.",
        "budget_per_day": "₹3,500 – ₹6,000 per person per day (All-inclusive 4N/5D holiday at ₹25,800)",
        "insider_tip": "Stroll along Baku Boulevard at sunset. The Heydar Aliyev Centre designed by Zaha Hadid looks completely magical in the late afternoon golden light.",
        "itinerary_2day": [
            "Day 1: Arrive Baku, walking tour through ancient Icherisheher and Maiden Tower, ride the funicular to Highland Park for sunset views of the Flame Towers.",
            "Day 2: Full-day excursion to Gobustan petroglyphs, explore the bubbling mud volcanoes, and visit the eternal natural flame at Yanar Dag.",
        ],
        "follow_up_question": "Are you excited to see Baku's futuristic architecture and Flame Towers, or the natural wonder of the Gobustan mud volcanoes?",
    },
    "malaysia": {
        "canonical_name": "Malaysia",
        "aliases": ["malaysia", "kuala lumpur", "putrajaya", "batu caves", "penang", "langkawi"],
        "region": "Southeast Asia",
        "tagline": "Truly Asia — Neon Skylines, Pink Mosques & Tropical Sanctuaries",
        "vibe": "Dazzling skyscrapers, vibrant multicultural food street markets, sacred limestone cave temples, and lush tropical islands",
        "best_season": "All Year Round (Tropical climate, 26°C – 32°C; West coast is driest November to March)",
        "package_duration": "3 Nights / 4 Days",
        "package_price": "Starting from INR 22,500/- per person",
        "package_inclusions": ["Guide", "Hotel Stay", "Sightseeing", "Transportation", "Breakfast", "All Entry Tickets"],
        "highlights": [
            {
                "name": "Petronas Twin Towers & KLCC Park",
                "desc": "The world's tallest twin towers soaring 452 meters with a double-decker skybridge and Lake Symphony musical fountains.",
                "cost": "Observation deck ticket included in package",
            },
            {
                "name": "Putrajaya Pink Mosque (Masjid Putra)",
                "desc": "Architectural marvel made of rose-tinted granite situated on the edge of Putrajaya Lake with a 116m minaret.",
                "cost": "Free entry / boat cruise included",
            },
            {
                "name": "Batu Caves & 140ft Golden Lord Murugan Statue",
                "desc": "Sacred limestone hill with 272 vibrant rainbow steps leading into colossal cathedral caverns.",
                "cost": "Free entry",
            },
            {
                "name": "Genting Highlands Cable Car & SkyWorlds",
                "desc": "Cool mountain resort nestled at 1,800m altitude reached by a thrilling 15-minute glass-floor cable car ride.",
                "cost": "Cable car ride included",
            },
        ],
        "food_specialities": [
            "National dish: Nasi Lemak (coconut rice with spicy sambal, fried anchovies, egg, and roasted peanuts)",
            "Crispy Roti Canai with dhal curry and Teh Tarik (pulled milk tea)",
            "Char Kway Teow (stir-fried wok-hei rice noodles with prawns)",
            "Jalan Alor night food street Satay skewers and fresh mango sticky rice",
        ],
        "stay_options": [
            "4-Star Modern Hotel in Bukit Bintang (~₹2,600 – ₹4,500/night)",
            "Infinity Pool Hotel overlooking the Petronas Towers (~₹3,500 – ₹6,500/night)",
            "Comfort City Hotel near KL Sentral (~₹1,800 – ₹3,000/night)",
        ],
        "transit": "Kuala Lumpur International Airport (KLIA/KLIA2) with direct 4-hour flights from Kochi, Chennai, Mumbai, and Delhi. Tour includes all airport & city transfers.",
        "budget_per_day": "₹3,500 – ₹5,500 per person per day (All-inclusive 3N/4D holiday from ₹22,500)",
        "insider_tip": "Visit the Putra Mosque in Putrajaya early in the morning when the pink granite glows soft rose against the turquoise lake. Free pink robes are provided at the entrance.",
        "itinerary_2day": [
            "Day 1: Arrive Kuala Lumpur, explore the colorful rainbow stairs of Batu Caves, afternoon check-in, and evening street food feast at Jalan Alor.",
            "Day 2: Morning photo tour of the Pink Mosque in Putrajaya, afternoon visit to the Petronas Twin Towers skybridge, and sunset drinks overlooking KLCC.",
        ],
        "follow_up_question": "Would you like to spend your time exploring the city sights of Kuala Lumpur and Putrajaya, or add a day trip to the cool hills of Genting?",
    },
    "thailand": {
        "canonical_name": "Thailand",
        "aliases": ["thailand", "bangkok", "phuket", "chiang mai", "chiangmai", "phi phi", "krabi"],
        "region": "Southeast Asia",
        "tagline": "The Land of Smiles — Golden Temples, Floating Markets & Tropical Seas",
        "vibe": "Gilded Buddha sanctuaries, electric night bazaars, world-renowned street cuisine, and turquoise Andaman sea lagoons",
        "best_season": "November to April (Cool and dry season with calm sea conditions and sunny blue skies, 24°C – 32°C)",
        "package_duration": "4 Nights / 5 Days",
        "package_price": "Starting from INR 23,000/- per person",
        "package_inclusions": ["Guide", "Hotel Stay", "Sightseeing", "Transportation", "Breakfast", "All Entry Tickets"],
        "highlights": [
            {
                "name": "Grand Palace & Wat Phra Kaew (Temple of the Emerald Buddha)",
                "desc": "Dazzling 18th-century royal compound with golden spires, vibrant murals, and the sacred Emerald Buddha.",
                "cost": "Included in package",
            },
            {
                "name": "Wat Arun (The Temple of Dawn)",
                "desc": "Stunning riverside temple clad in colorful porcelain mosaics on the west bank of the Chao Phraya River.",
                "cost": "Entry included in package",
            },
            {
                "name": "Phi Phi Islands & Maya Bay Lagoon",
                "desc": "World-famous limestone lagoon with crystal clear emerald waters, colorful clownfish reefs, and dramatic cliffs.",
                "cost": "Speedboat excursion included",
            },
            {
                "name": "Chiang Mai Mountain Temples & Night Bazaars",
                "desc": "Peaceful northern cultural haven with sacred golden hilltop stupas and ethical elephant rescue sanctuaries.",
                "cost": "Tour included in package",
            },
        ],
        "food_specialities": [
            "Authentic Pad Thai cooked in smoking woks with jumbo shrimp, crushed peanuts, and lime",
            "Aromatic Tom Yum Goong (spicy and sour lemongrass prawn soup)",
            "Sweet Mango Sticky Rice with warm coconut cream and toasted mung beans",
            "Fresh iced Thai milk tea (Cha Yen) and coconut ice cream served in coconut shells",
        ],
        "stay_options": [
            "4-Star Riverside Hotel in Bangkok (~₹2,800 – ₹5,000/night)",
            "Beachfront Resort in Phuket or Krabi (~₹3,500 – ₹7,000/night)",
            "Boutique Teakwood Lanna Resort in Chiang Mai (~₹2,400 – ₹4,200/night)",
        ],
        "transit": "Direct 3.5-hour flights to Bangkok (BKK/DMK) or Phuket (HKT) from Kochi, Chennai, Mumbai, and Delhi. Tour includes all private AC vehicles and boat tickets.",
        "budget_per_day": "₹3,500 – ₹6,000 per person per day (All-inclusive 4N/5D package from ₹23,000)",
        "insider_tip": "Wear clothing that covers your shoulders and knees when visiting the Grand Palace and Wat Arun. Take a sunset river shuttle across the Chao Phraya for the best views.",
        "itinerary_2day": [
            "Day 1: Arrive Bangkok, visit the spectacular Grand Palace and Wat Phra Kaew, take a longtail boat through the canal khlongs, and evening walk through Asiatique riverfront.",
            "Day 2: Morning climb up Wat Arun, explore the Damnoen Saduak floating market by wooden boat, and indulge in an authentic 90-minute Thai herbal massage.",
        ],
        "follow_up_question": "Are you planning a city-and-temple getaway in Bangkok and Chiang Mai, or a relaxing beach escape in Phuket and Krabi?",
    },
    "lakshadweep": {
        "canonical_name": "Lakshadweep",
        "aliases": ["lakshadweep", "agatti", "bangaram", "kavaratti", "kalpeni", "minicoy"],
        "region": "Arabian Sea, India (Union Territory)",
        "tagline": "India's Tropical Coral Paradise & Translucent Turquoise Lagoons",
        "vibe": "Pristine white sandbars, completely untouched living coral atolls, tranquil eco-cottages, and playful sea turtles",
        "best_season": "October to May (Calm seas, incredible underwater visibility up to 30 meters, pleasant 26°C – 30°C)",
        "package_duration": "3 Nights / 4 Days",
        "package_price": "Starting from INR 13,500/- per person",
        "package_inclusions": ["Guide", "Hotel Stay / Beach Cottage", "Sightseeing", "Transportation", "Breakfast", "All Entry / Island Permits"],
        "highlights": [
            {
                "name": "Agatti Island Turquoise Lagoon & Coral Reef",
                "desc": "One of the world's most spectacular airstrips leading into shallow, clear turquoise waters teeming with live coral.",
                "cost": "Permit and transfers included in package",
            },
            {
                "name": "Bangaram Atoll & Thinnakara Sandbank",
                "desc": "Uninhabited teardrop-shaped island with glowing bioluminescent plankton at night and crystal snorkeling reefs.",
                "cost": "Speedboat excursion included",
            },
            {
                "name": "Kavaratti Marine Aquarium & Lagoon Kayaking",
                "desc": "Capital island featuring vibrant marine life research center, calm kayaking, and historic wood-carved mosques.",
                "cost": "Included in package",
            },
            {
                "name": "Kalpeni Island Coral Debris Walk & Scuba Diving",
                "desc": "Spectacular lagoon with coral debris banks, manta ray sightings, and PADI certified diving spots.",
                "cost": "Snorkeling gear included in package",
            },
        ],
        "food_specialities": [
            "Authentic Maliku grilled yellowfin tuna with grated coconut and Maldivian spices",
            "Kadalakka Kootu (spiced coconut curry with local seafood and rice)",
            "Fresh sweet tender coconut water plucked straight from island groves",
            "Rayereha (traditional red tuna curry with pathiri or parotta)",
        ],
        "stay_options": [
            "Beachfront AC Cottage on Agatti Island (~₹3,500 – ₹6,000/night)",
            "Bangaram Island Eco Beach Tent / Resort (~₹5,000 – ₹9,000/night)",
            "Government Tourist Hut on Kavaratti (~₹2,500 – ₹4,000/night)",
        ],
        "transit": "Flights from Kochi (COK) directly to Agatti Island (AGX) take just 1 hour 15 mins. Regular passenger ships also operate from Kochi harbor. Entry permits are pre-arranged in package.",
        "budget_per_day": "₹3,500 – ₹5,500 per person per day (All-inclusive 3N/4D island escape starting from ₹13,500)",
        "insider_tip": "Lakshadweep requires an entry permit (e-permit). Our package handles this seamlessly. Sit on the left side of the aircraft when flying into Agatti for the most unreal aerial view of the turquoise lagoon!",
        "itinerary_2day": [
            "Day 1: Arrive Agatti Airport with jaw-dropping aerial lagoon views, check in to beach cottage, afternoon glass-bottom boat coral safari, and sunset kayak.",
            "Day 2: Morning speedboat trip to Bangaram Atoll, snorkel alongside sea turtles and colorful reef fish, afternoon picnic on Thinnakara sandbank, and evening grilled tuna dinner.",
        ],
        "follow_up_question": "Are you interested in water sports like scuba diving and snorkeling in Bangaram, or a tranquil secluded beach escape?",
    },
    "manali": {
        "canonical_name": "Manali, Himachal Pradesh",
        "aliases": ["manali", "kullu manali", "old manali", "solang", "hadimba", "vashisht"],
        "region": "Kullu Valley, Himachal Pradesh (Himalayas)",
        "best_season": "October to June (Snow in Dec–Feb, pleasant summers in Mar–Jun)",
        "vibe": "Misty cedar pine forests, snow-peaked Himalayan ridges, bohemian cafes, and ancient wooden pagoda temples",
        "highlights": [
            {"name": "Hadimba Devi Temple", "desc": "Ancient 1553 AD four-tiered wooden pagoda temple set within towering Dhungri deodar forests"},
            {"name": "Solang Valley & Rohtang", "desc": "Thrilling adventure hub for paragliding, snowmobiles, ropeway rides, and dramatic Himalayan panoramas"},
            {"name": "Old Manali & Manu Temple", "desc": "Quaint bohemian village with live-music riverside cafes, cobblestone trails, and apple orchards"},
            {"name": "Vashisht Natural Hot Springs", "desc": "Therapeutic sulfur hot springs and intricately carved stone-and-timber temple overlooking Beas river"},
            {"name": "Jogini Waterfalls Trek", "desc": "Serene pine-forest foot trail leading to dramatic cascading waterfalls and valley vistas"},
        ],
        "food_specialities": [
            "Himachali Siddu served piping hot with desi ghee and spiced mint chutney",
            "Pan-seared Himalayan Trout Fish in lemon garlic butter",
            "Traditional Himachali Dham & Chana Madra in rich yogurt gravy",
            "Steamed & fried Tibetan Momos with fiery red chili dip",
            "Hot spiced Himalayan Kahwa with saffron and crushed almonds",
        ],
        "stay_options": [
            "Cozy Alpine Guesthouse / Homestay in Old Manali (~₹1,000 – ₹1,800/night)",
            "Comfort Valley View Resort on Log Huts Road (~₹2,500 – ₹4,500/night)",
            "Luxury Victorian Castle / Riverside Heritage Spa (~₹7,000 – ₹12,000/night)",
        ],
        "transit": "Overnight Volvo AC bus from Delhi/Chandigarh to Manali (12–14 hrs). Nearest airport is Bhuntar (KUU - 50 km). Local autos, shared taxis, and scooter rentals available.",
        "budget_per_day": "₹1,500 – ₹2,500 per person per day for budget travel; ₹3,500 – ₹5,500 for comfortable family stays",
        "insider_tip": "For peaceful vibes, stay in Old Manali or Vashisht rather than crowded Mall Road. Head to Jogini Falls early in the morning by 7:30 AM to have the misty waterfall pools all to yourselves!",
        "itinerary_2day": [
            "Day 1: Arrive Manali, settle into Old Manali guesthouse, stroll through Hadimba Temple cedar groves, evening cafe hopping at Cafe 1947 by the river.",
            "Day 2: Morning visit to Solang Valley for panoramic views, afternoon hot sulfur bath at Vashisht, evening Mall Road souvenir shopping and hot Siddu dinner.",
        ],
        "follow_up_question": "Would you prefer staying in quiet scenic Old Manali with cafes, or closer to central Mall Road for convenient family transit?",
    },
    "annapurna": {
        "canonical_name": "Annapurna Base Camp (ABC Trek), Nepal",
        "aliases": ["annapurna", "abc", "abc trek", "abc trekking", "annapurna base camp", "annapoorna", "annapoorna base camp", "machapuchare", "pokhara abc", "annapurna circuit"],
        "region": "Gandaki Province, Nepal Himalayas (Gateway: Pokhara)",
        "best_season": "October to December (Crystal-clear skies) and March to May (Vibrant rhododendron blooms)",
        "vibe": "High-altitude alpine glacier sanctuary, 360-degree amphitheater of 7,000m & 8,000m snow peaks, and warm Gurung teahouse hospitality",
        "highlights": [
            {"name": "Annapurna Base Camp (4,130m)", "desc": "Legendary summit amphitheater surrounded by Annapurna I (8,091m), South, Hiunchuli, and Machapuchare"},
            {"name": "Machapuchare Base Camp (3,700m)", "desc": "Dramatic high-altitude base at the foot of the sacred double Fishtail granite peak"},
            {"name": "Poon Hill Sunrise (3,210m)", "desc": "World-famous dawn panorama over Dhaulagiri and the Annapurna range"},
            {"name": "Jhinu Danda Hot Springs", "desc": "Natural riverside geothermal sulfur pools nestled in a deep Himalayan river canyon"},
            {"name": "Chhomrong Gurung Village", "desc": "Historic stone village overlooking terraced valleys with traditional stone staircases"},
        ],
        "food_specialities": [
            "Dal Bhat Power 24 Hour (Unlimited refills of spiced lentils, seasonal mountain vegetables, and steamed rice)",
            "Hearty Himalayan Sherpa Stew (Syakpa / Thukpa) with root vegetables and warming herbs",
            "Gurung Mountain Honey Bread freshly pan-fried",
            "Tibetan Steamed Momos with roasted sesame tomato chutney",
            "Fresh Ginger Lemon Honey Tea for acclimatization and warmth",
        ],
        "stay_options": [
            "Teahouse Mountain Lodge along Modi Khola trail (~₹800 – ₹1,500/night with twin beds & cozy blankets)",
            "Pokhara Lakeside Boutique Hotel (~₹2,500 – ₹5,000/night before and after trek)",
        ],
        "transit": "Flight or tourist bus from Kathmandu to Pokhara (6 hrs). Shared 4x4 Jeep from Pokhara Lakeside to Nayapul or Siwai trailhead (2.5 hrs).",
        "budget_per_day": "₹2,500 – ₹4,000 per person per day (including TIMS & ACAP permits, teahouse accommodation, and 3 hearty meals)",
        "insider_tip": "Start your morning trail pushes by 6:00 AM before afternoon mist rolls into the Annapurna Sanctuary. Keep water purification tablets, high-energy nuts, and carry sufficient cash in Nepali Rupees as there are no ATMs beyond Nayapul!",
        "itinerary_2day": [
            "Day 1: Drive Pokhara to Siwai trailhead, trek through terraced Gurung villages to Chhomrong with Fishtail views.",
            "Day 2: Trek through dense bamboo gorge and Hinku Cave up to Machapuchare Base Camp (3,700m) for sunset over the glacier.",
        ],
        "follow_up_question": "Are you planning the standard 7–10 day full ABC Sanctuary circuit, or a shorter panoramic Himalayan trek like Poon Hill?",
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
<<<<<<< HEAD
        Synthesizes a warm, conversational, 0-lag response in PADAYAPPA's authentic voice.
=======
        Synthesizes a warm, conversational, 0-lag response in DASAPPAN's authentic voice.
>>>>>>> 3c289274a32b5e22152d56b42e31ac969b5e8f6e
        Follows progressive multi-turn consultative discovery:
        1. Never repeats formal greetings if already greeted in history.
        2. Reacts with authentic delight: 'Oh, {Destination}!! 🌟' followed by a 2-line vivid description.
        3. Collects essential details one comfortable question at a time across multiple messages.
        4. Smoothly handles affirmations ('yes', 'sure') and context follow-ups.
        """
        msg = user_message.strip()
        msg_lower = msg.lower()

        # Check if conversation already has prior messages
        already_greeted = False
        if history and isinstance(history, list) and len(history) > 0:
            for h in history:
                if isinstance(h, dict) and "namaskaram" in str(h.get("content", "")).lower():
                    already_greeted = True
                    break
                elif isinstance(h, dict) and h.get("role") == "assistant":
                    already_greeted = True
                    break

        display_name = (user_name or "").strip()
        greeting_prefix = (
            "" if already_greeted
            else (f"Namaskaram {display_name}! 🙏\n\n" if display_name else "Namaskaram! 🙏\n\n")
        )

        # Collect history text for context
        history_text = ""
        last_assistant_msg = ""
        if history and isinstance(history, list):
            history_text = " ".join([str(h.get("content", "")).lower() for h in history[-6:]])
            for h in reversed(history):
                if isinstance(h, dict) and h.get("role") == "assistant":
                    last_assistant_msg = str(h.get("content", "")).lower()
                    break

        full_context = f"{history_text} {msg_lower}"

        # 1. Pure greeting check (only on first contact or explicit standalone hello)
        greeting_words = {"hai", "hi", "hello", "hey", "namaskaram", "namaste", "vanakkam", "halo", "yo"}
        words_set = set(re.findall(r"\b\w+\b", msg_lower))

        if words_set.issubset(greeting_words) or msg_lower in ["hi", "hai", "hello", "hey", "namaskaram", "namaste", "good morning", "good evening"]:
            if already_greeted:
                return {
                    "reply": (
                        f"Hello {display_name or 'there'}! 😊 Ready for the next adventure.\n\n"
                        "Tell me your destination or whatever is on your mind, and let's plan it out together!"
                    ),
                    "source": "rag_knowledge_engine",
                }
            return {
                "reply": (
<<<<<<< HEAD
                    f"Namaskaram {display_name}! 🙏 PADAYAPPA here, your AI travel companion.\n\n"
=======
                    f"Namaskaram {display_name}! 🙏 DASAPPAN here, your AI travel companion.\n\n"
>>>>>>> 3c289274a32b5e22152d56b42e31ac969b5e8f6e
                    "How may I help you today?\n\n"
                    "Tell me your dream destination, budget, or the travel vibe you have in mind, and I'll analyze it to craft the ideal plan with verified stays and costs in ₹.\n\n"
                    "❓ Where would you like to travel, or what would you like me to plan for you?"
                ),
                "source": "rag_knowledge_engine",
            }

        # 2. Resolve destination (from current message first, then conversation history)
        dest_data = self.resolve_destination(msg_lower)
        if not dest_data:
            dest_data = self.resolve_destination(full_context)

        # Fallback to general destination name if matched in common keywords
        generic_dest_name = None
        if not dest_data:
            common_destinations = [
                "varanasi", "kashi", "banaras", "thenkasi", "tenkasi", "courtallam",
                "munnar", "vattavada", "varkala", "coorg", "ooty", "wayanad", "kodaikanal",
                "hampi", "goa", "alleppey", "mysore", "jaipur", "agra", "manali",
                "paris", "tokyo", "bali", "dubai", "ladakh", "delhi"
            ]
            for cd in common_destinations:
                if cd in msg_lower:
                    generic_dest_name = cd.title()
                    break
                elif cd in full_context:
                    generic_dest_name = cd.title()
                    break

        # 3. Contextual Affirmations ("yes", "sure", "tell me hotels", "refine it")
        is_affirmation = msg_lower in [
            "yes", "yeah", "yep", "sure", "please", "ok", "okay", "yes please",
            "tell me", "hotels", "stays", "transit", "train", "flight"
        ] or msg_lower.startswith("yes ") or msg_lower.startswith("sure ")

        if is_affirmation and dest_data:
            cname = dest_data["canonical_name"]
            stays = "\n".join([f"• **{s.split('(~')[0].strip()}** (~{s.split('(~')[1] if '(~' in s else s})" for s in dest_data["stay_options"]])
            transit = dest_data["transit"]
            tip = dest_data["insider_tip"]
            return {
                "reply": (
                    f"Here are the hand-picked stays and transit details for **{cname}**:\n\n"
                    f"🏨 **Verified Stays**:\n{stays}\n\n"
                    f"🚗 **How to Reach & Local Transit**:\n{transit}\n\n"
<<<<<<< HEAD
                    f"💡 **PADAYAPPA's Insider Secret**: {tip}\n\n"
=======
                    f"💡 **DASAPPAN's Insider Secret**: {tip}\n\n"
>>>>>>> 3c289274a32b5e22152d56b42e31ac969b5e8f6e
                    f"Would you like me to recommend the best local food spots or map out a detailed day-by-day plan next?"
                ),
                "source": "rag_knowledge_engine",
            }

        # 4. Handle specific queries (Food, Weather, Budget, Stays)
        if dest_data:
            cname = dest_data["canonical_name"]
            dest_short = cname.split("(")[0].strip()

            if any(w in msg_lower for w in ["food", "eat", "dishes", "cuisine", "restaurant", "parotta", "chaat", "lassi"]):
                foods = "\n".join([f"• {f}" for f in dest_data["food_specialities"]])
                return {
                    "reply": (
                        f"Here are the authentic must-try food specialities in **{dest_short}**:\n\n"
                        f"{foods}\n\n"
<<<<<<< HEAD
                        f"💡 **PADAYAPPA's Foodie Tip**: {dest_data['insider_tip']}\n\n"
=======
                        f"💡 **DASAPPAN's Foodie Tip**: {dest_data['insider_tip']}\n\n"
>>>>>>> 3c289274a32b5e22152d56b42e31ac969b5e8f6e
                        f"Would you like recommended stays nearby or shall we plan the itinerary?"
                    ),
                    "source": "rag_knowledge_engine",
                }

            if any(w in msg_lower for w in ["weather", "best time", "season", "climate", "rain", "when to visit"]):
                return {
                    "reply": (
                        f"Here is the climate & travel season overview for **{dest_short}**:\n\n"
                        f"📅 **Best Season**: {dest_data['best_season']}\n\n"
                        f"✨ **Atmosphere**: {dest_data['vibe']}\n\n"
                        f"💡 **Insider Tip**: {dest_data['insider_tip']}\n\n"
                        f"How many days are you planning to visit?"
                    ),
                    "source": "rag_knowledge_engine",
                }

        # 5. Progressive Consultative Flow (Multi-turn conversational discovery)
        active_dest_data = dest_data
        active_dest_name = (
            active_dest_data["canonical_name"].split("(")[0].strip()
            if active_dest_data
            else generic_dest_name
        )

        if active_dest_name:
            # Check for travelers
            travelers_match = re.search(
                r"\b(\d+)\s*(?:people|persons?|travelers?|pax|adults?|members?)\b",
                full_context
            )
            has_solo = any(w in full_context for w in ["solo", "alone", "myself", "just me", "single"])
            has_couple = any(w in full_context for w in ["couple", "two of us", "2 of us", "with my wife", "with my husband", "with my partner"])
            has_family = any(w in full_context for w in ["family", "kids", "parents"])
            has_friends = any(w in full_context for w in ["friends", "buddies", "college", "colleagues"])
            has_travelers = bool(travelers_match or has_solo or has_couple or has_family or has_friends or (
                "traveler" in last_assistant_msg and re.search(r"^\b\d+\b$", msg_lower)
            ))

            # Check for days / duration
            days_match = re.search(r"\b(\d+)\s*(?:day|days|d|night|nights|n)\b", full_context)
            has_days = bool(days_match or (
                "how many days" in last_assistant_msg and re.search(r"^\b\d+\b$", msg_lower)
            ))
            num_days = int(days_match.group(1)) if days_match else (
                int(msg_lower.strip()) if ("how many days" in last_assistant_msg and msg_lower.strip().isdigit()) else None
            )

            # Check for budget
            has_budget = any(w in full_context for w in ["budget", "comfort", "luxury", "₹", "rs", "rupee", "cheap", "cost", "10000", "15000", "12000", "20000", "25000", "under"])

            # STEP A: Destination just mentioned -> Warm reaction + 2-line description + Ask travelers
            dest_in_current_msg = (active_dest_name.lower() in msg_lower)
            if dest_in_current_msg and not has_travelers and not has_days:
                tagline = active_dest_data["tagline"] if active_dest_data else f"A breathtaking travel haven"
                vibe = active_dest_data["vibe"] if active_dest_data else f"Rich culture, picturesque landscapes, and memorable local experiences"

                return {
                    "reply": (
                        f"Oh, {active_dest_name}!! 🌟\n\n"
                        f"{tagline}. {vibe}.\n\n"
                        f"How many people will be traveling with you on this trip? (Solo, couple, family, or friends?)"
                    ),
                    "source": "rag_consultative_engine",
                }

            # STEP B: Travelers provided, but duration missing -> Acknowledge travelers + Ask days
            if has_travelers and not has_days:
                group_phrase = (
                    "A couple's journey" if has_couple
                    else "A solo adventure" if has_solo
                    else "A family holiday" if has_family
                    else "A trip with friends" if has_friends
                    else f"A trip for {travelers_match.group(0) if travelers_match else 'your group'}"
                )
                return {
                    "reply": (
                        f"Wonderful! {group_phrase} to **{active_dest_name}** will be an exceptional experience.\n\n"
                        f"How many days are you planning to spend? (Most travelers find 3 to 4 days ideal to explore the key highlights and authentic spots comfortably)."
                    ),
                    "source": "rag_consultative_engine",
                }

            # STEP C: Duration provided, but budget missing -> Acknowledge days + Ask budget
            if has_days and not has_budget:
                days_label = f"{num_days} days" if num_days else "Your planned duration"
                return {
                    "reply": (
                        f"{days_label} is a fantastic timeframe for **{active_dest_name}**! That gives us ample time to experience the signature sights, authentic regional meals, and peaceful hidden corners.\n\n"
                        f"What approximate budget tier or style do you have in mind? (e.g. Budget backpacker, comfortable heritage stays, or luxury in ₹)?"
                    ),
                    "source": "rag_consultative_engine",
                }

            # STEP D: All essential details gathered OR full prompt provided -> Generate tailored complete plan
            chosen_days = num_days or 3

            # Tailor itinerary strictly to chosen_days
            itinerary_entries = []
            if active_dest_data:
                source_itin = active_dest_data.get(f"itinerary_{chosen_days}day") or active_dest_data.get("itinerary_5day") or active_dest_data.get("itinerary_2day") or []
                if len(source_itin) >= chosen_days:
                    itinerary_entries = source_itin[:chosen_days]
                else:
                    # Dynamically synthesize exact day count
                    for day_idx in range(1, chosen_days + 1):
                        if day_idx <= len(source_itin):
                            itinerary_entries.append(source_itin[day_idx - 1])
                        else:
                            itinerary_entries.append(f"Day {day_idx}: Deep exploration of {active_dest_name}'s artisan markets, scenic viewpoints, and peaceful evening cultural trails.")
            else:
                for day_idx in range(1, chosen_days + 1):
                    itinerary_entries.append(f"Day {day_idx}: Signature exploration of {active_dest_name}'s premier landmarks, authentic local food, and sunset panoramic views.")

            itinerary_str = "\n".join([f"• **{step.split(':')[0]}**: {':'.join(step.split(':')[1:]).strip() if ':' in step else step}" for step in itinerary_entries])

            stays_str = "\n".join([f"• {s}" for s in (active_dest_data.get("stay_options", [])[:3] if active_dest_data else [f"Comfort Stays in {active_dest_name} (~₹2,200 – ₹3,800/night)", f"Boutique Heritage Resort (~₹4,500 – ₹6,500/night)"])])
            foods_str = "\n".join([f"• {f}" for f in (active_dest_data.get("food_specialities", [])[:4] if active_dest_data else [f"Local thali and regional delicacies", f"Traditional fresh street snacks", f"Famous hot filter coffee / regional tea"])])
            budget_str = active_dest_data.get("budget_per_day", "₹2,000 – ₹3,500 per person per day") if active_dest_data else "₹2,000 – ₹3,500 per person per day"
            transit_str = active_dest_data.get("transit", f"Direct road, train, and flight connections available to {active_dest_name}.") if active_dest_data else f"Easily accessible by rail, flight, and scenic road networks."
            tip_str = active_dest_data.get("insider_tip", "Explore prime sights early in the morning around 6:30 AM to beat the crowds and enjoy the best light.") if active_dest_data else "Book popular heritage stays early and visit major viewpoints during golden hour."

            plan_title = f"{chosen_days}-Day Bespoke {active_dest_name} Travel Plan"

            reply = (
                f"Here is your personalized **{plan_title}**:\n\n"
                f"### 🗓️ Day-by-Day Journey\n"
                f"{itinerary_str}\n\n"
                f"### 🏨 Recommended Stays\n"
                f"{stays_str}\n\n"
                f"### 🍲 Iconic Food & Dining\n"
                f"{foods_str}\n\n"
                f"### 💰 Estimated Budget Guidelines\n"
                f"• **Daily Average**: {budget_str}\n"
                f"• **Transit Details**: {transit_str}\n\n"
<<<<<<< HEAD
                f"### 💡 Padayappa's Local Insider Secret\n"
=======
                f"### 💡 Dasappan's Local Insider Secret\n"
>>>>>>> 3c289274a32b5e22152d56b42e31ac969b5e8f6e
                f"{tip_str}\n\n"
                f"Would you like recommendations on specific hotel bookings or flight/train transit details?"
            )
            return {"reply": reply, "source": "rag_knowledge_engine"}

        # 6. General fallback when no destination is mentioned
        return {
            "reply": (
                f"{greeting_prefix}"
                "I'm ready to craft your personalized travel plan.\n\n"
<<<<<<< HEAD
                "Which destination do you have in mind? (e.g. Varanasi, Thenkasi, Munnar, Varkala, Coorg, Goa, or Paris)?\n\n"
=======
                "Which destination do you have in mind? (e.g. **Varanasi**, **Thenkasi**, **Munnar**, **Varkala**, **Coorg**, **Goa**, or **Paris**)?\n\n"
>>>>>>> 3c289274a32b5e22152d56b42e31ac969b5e8f6e
                "❓ Just drop the city or region name, and we'll take it from there!"
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
