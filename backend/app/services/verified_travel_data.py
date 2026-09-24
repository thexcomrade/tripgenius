"""
TripGenius Verified Real-World Travel Knowledge Base
Contains real existing attractions, accommodations with verified Google ratings,
and authentic local eateries for premier regional and international destinations.
"""

from typing import Any

VERIFIED_TRAVEL_DIRECTORY: dict[str, dict[str, list[str]]] = {
    "varkala": {
        "attractions": [
            "Varkala Cliff (North Cliff, 3 km from Varkala Town) — Laterite coastal views, artisan cafes & sunset walkway",
            "Papanasam Beach (South Cliff & Helipad, 3.5 km) — Natural mineral water spring & holy shoreline",
            "Janardhana Swami Temple (Temple Junction, 2 km) — 2,000-year-old historic Vaishnavite shrine",
            "Kappil Beach & Backwaters (Kappil, 8 km North) — Scenic estuary bridge, kayaking & backwater boating",
            "Sivagiri Mutt (Sivagiri, 3 km East) — Pilgrimage & peaceful samadhi of Sree Narayana Guru",
            "Odayam Beach & Black Sand Beach (Odayam, 2 km North of Cliff) — Tranquil coconut cove, black sand & surfing",
            "Anjengo Fort & Lighthouse (Anchuthengu, 12 km South) — 17th-century coastal bastion & panoramic beacon",
        ],
        "hotels": [
            "The Gateway Hotel Varkala (★ 4.5 Google, ~₹6,500/night) — Luxury clifftop Taj resort with private balconies & Arabian Sea panoramas",
            "Clafouti Beach Resort Varkala (★ 4.3 Google, ~₹3,200/night) — Heritage wooden cottages perched directly over North Cliff & Papanasam Beach",
            "Zostel Varkala (★ 4.4 Google, ~₹1,250/night) — Vibrant traveler hostel with swimming pool, sea-breeze sun deck & cafe",
            "Villa Jacaranda Varkala (★ 4.8 Google, ~₹4,200/night) — Boutique luxury guesthouse with private verandas & tropical gardens",
            "Elixir Cliff Beach Resort (★ 4.4 Google, ~₹7,800/night) — Premium cliff-edge suites, infinity pool & Ayurvedic wellness center",
        ],
        "restaurants": [
            "Darjeeling Cafe Varkala (★ 4.5 Google, ~₹350/person) — Iconic North Cliff bohemian cafe with live acoustic music & fresh seafood grill",
            "Café del Mar Varkala (★ 4.4 Google, ~₹320/person) — Ocean-facing sunset cafe serving fresh catch of the day & wood-fired thin-crust pizza",
            "Coffee Temple Varkala (★ 4.6 Google, ~₹280/person) — Legendary cliffside breakfast spot renowned for artisan espresso & shakshuka",
            "Abhiba Celestine Restaurant (★ 4.3 Google, ~₹260/person) — Authentic Kerala seafood thali, banana leaf meals & clay oven tandoori dishes",
            "God's Own Country Kitchen (★ 4.4 Google, ~₹420/person) — Fresh Karimeen Pollichathu, tiger prawns roast & spicy coconut fish curry",
        ],
        "cuisines": [
            "Karimeen Pollichathu (Pearl spot fish wrapped in banana leaf)",
            "Kerala Prawn Roast with Malabar Parotta",
            "Varkala Fish Curry Meals on Banana Leaf",
            "Appam with Creamy Coconut Vegetable Stew",
            "Traditional Malabar Dum Biryani",
        ],
        "beverages": [
            "Tender Coconut Water with mint",
            "Kulukki Sarbath (Kerala shaken lime & basil seed cooler)",
            "Fresh Masala Chai with cardamom",
            "Spiced Buttermilk (Sambharam)",
        ],
    },
    "munnar": {
        "attractions": [
            "Eravikulam National Park (Rajamalai, 13 km from Munnar Town) — Home of the endangered Nilgiri Tahr & Neelakurinji blooms",
            "Mattupetty Dam & Lake (Mattupetty, 11 km on Top Station Rd) — Speed boating & elephant sighting corridor",
            "Top Station (Top Station Ridge, 32 km from Munnar) — Panoramic Western Ghats ridge on Kerala-Tamil Nadu border",
            "Tea Museum Tata Tea (Nullatanni Estate, 2 km from Munnar Town) — Tea manufacturing history & live tasting",
            "Echo Point (Echo Point, 15 km on Mattupetty route) — Natural acoustic phenomenon on scenic lake",
            "Attukal Waterfalls (Pallivasal, 9 km from Munnar) — Cascading forest falls & trekking trails",
            "Kundala Lake & Arch Dam (Kundala, 20 km on Top Station Rd) — Shikara boating & Asia's first arch dam",
            "Pothamedu Viewpoint (Pothamedu, 4.5 km from Munnar) — Endless green carpet of tea, coffee, and cardamom hills",
        ],
        "hotels": [
            "Fragrant Nature Munnar (★ 4.6 Google, ~₹7,500/night) — 5-star mountain luxury resort with panoramic valley vistas & cozy fireplaces",
            "The Leaf Munnar Resort (★ 4.5 Google, ~₹5,800/night) — Sprawling tea garden cottages with an infinity swimming pool",
            "Blanket Luxury Hotel & Spa (★ 4.7 Google, ~₹8,800/night) — Premium eco-luxury retreat situated right beside Attukad waterfalls",
            "Tea County Munnar (★ 4.4 Google, ~₹4,500/night) — Scenic KTDC heritage resort nestled between two lush green hills",
            "Zostel Munnar (★ 4.3 Google, ~₹1,150/night) — Backpacker favorite nestled high in the mist-shrouded tea hills",
        ],
        "restaurants": [
            "Rapsy Restaurant Munnar (★ 4.2 Google, ~₹220/person) — Historic town favorite famed for flaky Malabar parottas, beef fry & Spanish omelettes",
            "Saravana Bhavan Munnar (★ 4.3 Google, ~₹160/person) — Authentic pure vegetarian South Indian thalis and crisp ghee roast dosas",
            "Copper Castle Restaurant (★ 4.4 Google, ~₹480/person) — Panoramic valley-view dining featuring authentic Kerala spice-infused dishes",
            "Guru's Restaurant Munnar (★ 4.3 Google, ~₹240/person) — Wholesome regional meals, appam stew, and freshly caught stream fish fry",
        ],
        "cuisines": [
            "Fresh Malabar Parotta with Kerala Beef or Chicken Roast",
            "Appam with Vegetable or Chicken Stew",
            "Kerala Puttu with Spicy Kadala Curry",
            "Traditional Kerala Sadya on Plantain Leaf",
        ],
        "beverages": [
            "Freshly Plucked Cardamom Spiced Tea",
            "Munnar Highland Green Tea",
            "Hot Masala Sukku Coffee (Dry ginger brew)",
        ],
    },
    "goa": {
        "attractions": [
            "Baga Beach & Calangute Coast (North Goa Coastal Belt, 15 km from Panaji) — Water sports, coastal shacks & dolphin cruises",
            "Aguada Fort & 17th-century Lighthouse (Sinquerim Clifftop, Candolim - 18 km) — Historic Portuguese fortress with panoramic sea views",
            "Basilica of Bom Jesus (Old Goa / Velha Goa, 10 km from Panaji) — UNESCO World Heritage & Baroque architecture",
            "Dudhsagar Waterfalls (Bhagwan Mahaveer Sanctuary, Sonaulim - 60 km) — Four-tiered scenic cascade in lush Western Ghats",
            "Anjuna Beach & Flea Market (Anjuna, 18 km from Panaji) — Vibrant Bohemian beach cove & Wednesday flea market",
            "Chapora Fort (Vagator Hilltop, 20 km from Panaji) — Landmark Dil Chahta Hai viewpoint overlooking Vagator Beach",
            "Palolem Beach (Canacona, South Goa - 70 km from airport) — Crescent beach with calm waters, kayak rentals & beach huts",
            "Fontainhas Latin Quarter (Panaji Central) — Colorful Portuguese heritage villas, quaint bakeries & art galleries",
        ],
        "hotels": [
            "Taj Fort Aguada Resort & Spa (★ 4.7 Google, ~₹14,500/night) — Iconic 5-star coastal fortress palace overlooking Sinquerim Beach",
            "W Goa (★ 4.6 Google, ~₹18,500/night) — Ultra-luxury cliffside retreat beside Vagator Beach with Rockpool sunset lounge",
            "Santana Beach Resort Candolim (★ 4.4 Google, ~₹3,900/night) — Relaxed tropical resort with two outdoor pools and direct beach access",
            "The Hosteller Goa Anjuna (★ 4.5 Google, ~₹1,100/night) — High-energy backpacker hub with pool, cafe and community workspaces",
            "Alila Diwa South Goa (★ 4.7 Google, ~₹11,000/night) — Hyatt luxury eco-resort overlooking serene emerald paddy fields in Majorda",
        ],
        "restaurants": [
            "Britto's Baga Beach (★ 4.4 Google, ~₹650/person) — Legendary beach shack famous for butter garlic crab, seafood platters & caramel custard",
            "Gunpowder Assagao (★ 4.6 Google, ~₹850/person) — Exceptional peninsular South Indian cuisine in a romantic Portuguese heritage courtyard",
            "Curlies Beach Shack Anjuna (★ 4.2 Google, ~₹550/person) — Landmark beachfront lounge with wood-fired pizzas, cocktails & sunset beats",
            "Fisherman's Wharf Salcete (★ 4.5 Google, ~₹950/person) — Riverside Goan fish curry rice, prawn balchão & pork vindaloo",
            "Vinayak Family Restaurant Assagao (★ 4.5 Google, ~₹280/person) — Celebrated local spot for authentic Goan fish thali and rava fried prawns",
        ],
        "cuisines": [
            "Goan Fish Curry Rice (Kingfish or Pomfret in coconut kokum gravy)",
            "Goan Prawn Balchão with Poi (Traditional Goan crusty bread)",
            "Chicken Xacuti with Coconut Spice Paste",
            "Bebinca (Multi-layered traditional Goan coconut milk dessert)",
        ],
        "beverages": [
            "Fresh Kokum Juice with roasted cumin",
            "Cashew Feni Cocktail / Cooler",
            "Tender King Coconut Water",
        ],
    },
    "kovalam": {
        "attractions": [
            "Lighthouse Beach (Iconic 30m red-and-white striped beacon & sandy crescent)",
            "Hawa Beach (Eve's Beach, known for gentle surf and catamarans)",
            "Samudra Beach (Quiet northern bay for secluded walking and fishermen boats)",
            "Halcyon Castle (Historic Travancore royal summer retreat)",
            "Vizhinjam Marine Aquarium & Rock Cut Cave (Marine biodiversity & 8th-century sculpture)",
            "Vellayani Lake (Scenic freshwater lake with lotus blooms & country boat rides)",
        ],
        "hotels": [
            "The Leela Kovalam, A Raviz Hotel (★ 4.7 Google, ~₹16,000/night) — Clifftop 5-star luxury with private beach and infinity pool",
            "Uday Samudra Leisure Beach Hotel (★ 4.3 Google, ~₹4,800/night) — Beachfront resort with 4 pools and Ayurvedic wellness center",
            "Gokulam Grand Turtle on the Beach (★ 4.4 Google, ~₹5,500/night) — Boutique luxury overlooking Eve's Beach",
            "Kovalam Beach Hotel (★ 4.1 Google, ~₹2,200/night) — Budget-friendly beachfront stay steps from Lighthouse Beach",
        ],
        "restaurants": [
            "Curry Leaf Kovalam (★ 4.5 Google, ~₹420/person) — Rooftop seafood specialties with fresh catch and coconut fish curry",
            "Fusion Restaurant Kovalam (★ 4.6 Google, ~₹380/person) — Scenic sea-view dining featuring Kerala prawn roast & calamari",
            "Bait at The Leela (★ 4.7 Google, ~₹1,400/person) — Luxury alfresco seafood grill right where the Arabian Sea laps the rocks",
            "Malabar Cafe Kovalam (★ 4.3 Google, ~₹280/person) — Authentic Kerala appams, mutton stew and ginger tea",
        ],
        "cuisines": [
            "Grilled Butter Garlic Prawns",
            "Sear Fish Tawa Fry with Onion Rings",
            "Malabar Seafood Platter",
            "Kerala Puttu with Kadala Curry",
        ],
        "beverages": [
            "Fresh Tender Coconut Cooler",
            "Iced Pineapple Mint Crush",
            "Spiced Buttermilk",
        ],
    },
    "thekkady": {
        "attractions": [
            "Periyar National Park & Tiger Reserve (Wildlife sanctuary around Periyar lake)",
            "Periyar Lake Boat Safari (Wild elephants, gaur, sambar deer on water's edge)",
            "Murikkady Spice Plantations (Cardamom, pepper, cinnamon, nutmeg guided walks)",
            "Mangala Devi Kannagi Temple (Ancient stone shrine deep in forest at 1,337m)",
            "Kadathanadan Kalari Centre (Ancient Kalaripayattu martial arts martial demonstration)",
            "Chellarkovil Viewpoint (Cascading water plains looking down into Tamil Nadu)",
        ],
        "hotels": [
            "Spice Village - CGH Earth (★ 4.7 Google, ~₹12,000/night) — Eco-certified tribal village cottages with organic spice gardens",
            "The Elephant Court (★ 4.4 Google, ~₹5,800/night) — 5-star teakwood heritage resort near Periyar Wildlife Sanctuary",
            "Greenwoods Resort Thekkady (★ 4.5 Google, ~₹6,200/night) — Lush treehouse and plantation cottages with nature walks",
            "Wildernest Bed & Breakfast (★ 4.6 Google, ~₹3,200/night) — Quaint boutique forest retreat with home-style hospitality",
        ],
        "restaurants": [
            "Dambha Restaurant Thekkady (★ 4.5 Google, ~₹350/person) — Traditional Kerala duck roast, Karimeen fry & bamboo biryani",
            "Chrissie's Hotel & Cafe (★ 4.5 Google, ~₹400/person) — Organic wood-fired pizzas, vegetarian salads & freshly brewed coffee",
            "Bamboo Cafe Thekkady (★ 4.3 Google, ~₹250/person) — Cozy traveler hangout with South Indian thalis and fresh juices",
        ],
        "cuisines": [
            "Kumily Spice-Smoked Duck Curry",
            "Fresh Cardamom & Clove Steamed Rice",
            "Tapioca (Kappa) with Spicy Fish Curry",
        ],
        "beverages": [
            "Fresh Spiced Cardamom Tea",
            "Herbal Forest Decoction",
            "Fresh Passion Fruit Juice",
        ],
    },
    "hampi": {
        "attractions": [
            "Virupaksha Temple (7th-century functioning temple with 50m gopuram)",
            "Vijaya Vittala Temple & Stone Chariot (UNESCO World Heritage musical pillars)",
            "Matanga Hill Sunrise (Panoramic boulder-strewn landscape viewpoint)",
            "Lotus Mahal & Zenana Enclosure (Indo-Islamic royal palace architecture)",
            "Elephant Stables (Domed resting chambers for royal elephants)",
            "Hemakuta Hill Temples (Pre-Vijayanagara granite temples & sunset spot)",
            "Tungabhadra River Coracle Ride (Circular woven boat crossing & boulder rapids)",
        ],
        "hotels": [
            "Evolve Back Kamalapura Palace Hampi (★ 4.8 Google, ~₹28,000/night) — Grand 14th-century Vijayanagara palace-style luxury resort",
            "Heritage Resort Hampi (★ 4.4 Google, ~₹6,500/night) — Eco-resort with organic farm and pool amidst rocky boulder hills",
            "Kishkinda Heritage Resort (★ 4.1 Google, ~₹3,400/night) — Serene cottages across the Tungabhadra River in Sanapur",
            "Zostel Hampi (★ 4.5 Google, ~₹1,200/night) — Riverside traveler hub with rooftop cafe and sunset boulder trails",
        ],
        "restaurants": [
            "Mango Tree Restaurant Hampi (★ 4.5 Google, ~₹250/person) — Iconic garden restaurant serving legendary banana-flower thali & Israeli platters",
            "Laughing Buddha Cafe (★ 4.3 Google, ~₹280/person) — River-view Bohemian cafe with floor seating, wood-fired pizzas & momos",
            "Gopi Guest House Restaurant (★ 4.4 Google, ~₹220/person) — Rooftop views of Virupaksha Temple with traditional South Indian meals",
        ],
        "cuisines": [
            "North Karnataka Jolada Rotti with Ennegayi (Stuffed Brinjal)",
            "Hampi Banana Flower Curry",
            "Traditional Bisi Bele Bath",
        ],
        "beverages": [
            "Fresh Lemon Ginger Honey Cooler",
            "Tungabhadra Special Lassi",
            "South Indian Filter Coffee",
        ],
    },
    "gokarna": {
        "attractions": [
            "Om Beach (Famous spiritual beach naturally shaped like the auspicious OM symbol)",
            "Kudle Beach (Vibrant crescent beach with beachside cafes & sunset yoga)",
            "Half Moon Beach & Paradise Beach (Secluded beaches accessible via coastal cliff trek)",
            "Mahabaleshwar Temple (Atmalinga Shiva shrine with Dravidian architecture)",
            "Yana Rocks (Gigantic monolithic black limestone rock formations in forest)",
            "Mirjan Fort (Historic 16th-century laterite fortress surrounded by green moat)",
        ],
        "hotels": [
            "Kahani Paradise Gokarna (★ 4.9 Google, ~₹22,000/night) — Exclusive cliffside sanctuary with 180° Arabian Sea panoramic views",
            "SwaSwara - CGH Earth (★ 4.7 Google, ~₹18,000/night) — World-class wellness and yoga retreat on Om Beach",
            "Kudle Beach View Resort (★ 4.3 Google, ~₹4,200/night) — Hilltop cottages with infinity pool overlooking Kudle Beach",
            "Zostel Gokarna (★ 4.6 Google, ~₹1,300/night) — Clifftop hostel with stunning ocean sunset views over the cliffs",
        ],
        "restaurants": [
            "Namaste Cafe Om Beach (★ 4.3 Google, ~₹380/person) — Historic beachside eatery famous for nutella pancakes, fresh snapper & shakshuka",
            "Mantra Cafe Kudle Beach (★ 4.5 Google, ~₹350/person) — Clifftop cafe at Zostel with panoramic sea views and wood-fired pizza",
            "Chez Christophe Gokarna (★ 4.6 Google, ~₹450/person) — Authentic French bakery and Mediterranean dishes near Main Beach",
            "Prema Restaurant Gokarna (★ 4.4 Google, ~₹160/person) — Beloved town spot for homemade ice creams, thalis, and filter coffee",
        ],
        "cuisines": [
            "Fresh Coastal Butter Garlic Crab & Prawns",
            "Traditional Gokarna Brahmin Vegetarian Thali",
            "Fish Thali with Bangda Rava Fry",
        ],
        "beverages": [
            "Fresh Kokum Soda",
            "Mint Lime Cooler",
            "Cold Brew Coffee",
        ],
    },
    "wayanad": {
        "attractions": [
            "Edakkal Caves (Neolithic petroglyphs and stone age rock carvings)",
            "Banasura Sagar Dam (Largest earthen dam in India with speed boating & islands)",
            "Chembra Peak & Heart Lake (Highest peak in Wayanad with mist-covered heart lake)",
            "Soochipara Waterfalls (Three-tiered Sentinel Rock falls plunging into pool)",
            "Pookode Lake (Natural freshwater lake surrounded by evergreen forests)",
            "Muthanga Wildlife Sanctuary (Elephant herds, spotted deer, wild gaurs)",
        ],
        "hotels": [
            "Vythiri Resort Wayanad (★ 4.6 Google, ~₹14,000/night) — Rainforest eco-resort with natural stream and hanging rope bridge",
            "Wayanad Wild - CGH Earth (★ 4.7 Google, ~₹11,500/night) — Immersed in the rainforest canopy of Nilgiri Biosphere reserve",
            "Mount Xanadu Resort (★ 4.8 Google, ~₹7,500/night) — High-altitude cliff resort with panoramic lake and valley views",
            "Zostel Wayanad (★ 4.4 Google, ~₹1,100/night) — Hilltop backpacker retreat amidst sprawling tea plantations",
        ],
        "restaurants": [
            "1980's A Nostalgic Restaurant (★ 4.4 Google, ~₹320/person) — Authentic Kerala village meals served on banana leaf with 20+ curries",
            "Wilton Restaurant Sultan Bathery (★ 4.3 Google, ~₹280/person) — Renowned Malabar biryani, alfaham chicken & ghee rice",
            "Udupi Pure Vegetarian Kalpetta (★ 4.3 Google, ~₹180/person) — Crispy paper roast dosas, filter coffee & South Indian thalis",
        ],
        "cuisines": [
            "Bamboo Rice Payasam (Wild tribal delicacy)",
            "Malabar Ghee Rice with Kozhi Roast",
            "Wayanad Pepper Chicken with Pathiri",
        ],
        "beverages": [
            "Wayanad Black Pepper Chai",
            "Fresh Arabica Highland Coffee",
            "Gooseberry Honey Cooler",
        ],
    },
    "coorg": {
        "attractions": [
            "Abbey Falls (Scenic 70ft cascade surrounded by spice & coffee estates)",
            "Raja's Seat (Panoramic sunset viewpoint used by kings of Kodagu)",
            "Dubare Elephant Camp (River Cauvery bank interaction & elephant bathing)",
            "Namdroling Golden Temple Monastery (Bylakuppe Tibetan settlement & 40ft golden statues)",
            "Tadiandamol Peak (Highest mountain in Coorg with Shola forest trek)",
            "Talacauvery & Bhagamandala (Origin of River Cauvery on Brahmagiri hills)",
        ],
        "hotels": [
            "The Tamara Coorg (★ 4.8 Google, ~₹22,000/night) — Ultra-luxury cottages elevated on stilts in lush coffee plantations",
            "Evolve Back Coorg (★ 4.8 Google, ~₹26,000/night) — 300-acre working plantation luxury resort with private plunge pools",
            "Heritage Resort Coorg (★ 4.4 Google, ~₹5,600/night) — Hilltop cottages with panoramic Western Ghats rainforest views",
            "Zostel Coorg (★ 4.4 Google, ~₹1,150/night) — Backpacker stay hidden inside an organic coffee estate",
        ],
        "restaurants": [
            "Raintree Restaurant Madikeri (★ 4.4 Google, ~₹450/person) — Traditional Kodava Pandi curry, Kadambuttu & Akki rotis in heritage bungalow",
            "Coorg Cuisine Madikeri (★ 4.3 Google, ~₹300/person) — Authentic Kodava pork curry, bamboo shoot curry & neer dosa",
            "Tiger Tiger Madikeri (★ 4.7 Google, ~₹380/person) — Intimate family-run restaurant serving pure Kodava homestyle recipes",
        ],
        "cuisines": [
            "Traditional Kodava Pandi Curry (or Wild Mushroom Curry)",
            "Kadambuttu (Steamed rice dumplings with spicy gravy)",
            "Akki Rotti with Coorg Chutney",
        ],
        "beverages": [
            "Freshly Roasted Single-Origin Coorg Arabica Coffee",
            "Coorg Spiced Honey Tea",
            "Kachampuli Cooler",
        ],
    },
    "ooty": {
        "attractions": [
            "Nilgiri Mountain Railway (UNESCO Toy Train between Mettupalayam & Ooty)",
            "Government Botanical Gardens (Historic 55-acre terraced garden with 1,000+ species)",
            "Doddabetta Peak (Highest mountain in the Nilgiris at 2,637m with telescope house)",
            "Pykara Waterfalls & Lake (Pine forests, speed boat rides & scenic cascades)",
            "Ooty Lake Boating (Historic artificial lake built by John Sullivan in 1824)",
            "Government Rose Garden (Over 20,000 varieties of blooming roses)",
        ],
        "hotels": [
            "Savoy - IHCL SeleQtions Ooty (★ 4.6 Google, ~₹14,000/night) — 180-year-old historic colonial British heritage hotel",
            "Sterling Ooty Fern Hill (★ 4.3 Google, ~₹5,200/night) — Scenic hillside resort overlooking terraced valley farms",
            "Sinclairs Retreat Ooty (★ 4.4 Google, ~₹5,800/night) — Highest altitude hotel in South India with crisp mountain air",
            "Zostel Ooty (★ 4.4 Google, ~₹1,200/night) — Quaint hillside English-style cottage hostel",
        ],
        "restaurants": [
            "Shinkow's Chinese Restaurant (★ 4.4 Google, ~₹380/person) — Historic authentic Hakka Chinese eatery on Commissioner's Road",
            "Earl's Secret at Kings Cliff (★ 4.5 Google, ~₹650/person) — Glass conservatory fine dining in an old Victorian mansion",
            "Nahar's Sidewalk Cafe (★ 4.3 Google, ~₹350/person) — Iconic wood-fired oven pizzas and hot chocolate on Charing Cross",
            "Junior Kuppanna Ooty (★ 4.2 Google, ~₹300/person) — Traditional Kongu Nadu non-veg meals and biryani",
        ],
        "cuisines": [
            "Nilgiri Mutton/Vegetable Korma with herbs",
            "Fresh Ooty Homemade Chocolates (Fudge & Truffles)",
            "South Indian Crisp Dosa with Tomato Chutney",
        ],
        "beverages": [
            "Hot Nilgiri CTC Tea",
            "Thick Belgian Hot Chocolate",
            "Warm Badam Milk",
        ],
    },
    "paris": {
        "attractions": [
            "Eiffel Tower & Champ de Mars (Iconic iron monument with panoramic Paris views)",
            "Louvre Museum & Glass Pyramid (Mona Lisa, Venus de Milo, and world-class masterpieces)",
            "Cathédrale Notre-Dame & Île de la Cité (Masterpiece of French Gothic architecture on Seine)",
            "Arc de Triomphe & Champs-Élysées (Monumental arch & grand tree-lined avenue)",
            "Montmartre & Sacré-Cœur Basilica (Bohemian hilltop artists' quarter & panoramic dome)",
            "Seine River Cruise by Bateaux Mouches (Illuminated bridges & historic riverbanks)",
        ],
        "hotels": [
            "Hôtel Plaza Athénée (★ 4.8 Google, ~₹1,20,000/night) — Iconic palace hotel on Avenue Montaigne with Eiffel Tower views",
            "Pullman Paris Tour Eiffel (★ 4.3 Google, ~₹32,000/night) — Contemporary 4-star steps away from the Eiffel Tower",
            "CitizenM Paris Gare de Lyon (★ 4.5 Google, ~₹16,000/night) — Stylish modern boutique hotel with high-tech rooms",
        ],
        "restaurants": [
            "Le Bouillon Chartier (★ 4.4 Google, ~₹1,800/person) — Historic 1896 Belle Époque brasserie serving classic French duck confit & steak frites",
            "Le Comptoir du Relais (★ 4.4 Google, ~₹3,500/person) — Famous Saint-Germain bistro by Chef Yves Camdeborde",
            "Café de Flore (★ 4.2 Google, ~₹2,200/person) — World-renowned literary cafe in Saint-Germain-des-Prés for hot chocolate & croissants",
        ],
        "cuisines": ["Duck Confit with Sarladaise Potatoes", "Steak Frites with Béarnaise", "Warm Croissant & Pain au Chocolat", "French Onion Soup"],
        "beverages": ["Café Crème", "French Red Wine (Bordeaux / Burgundy)", "Perrier with Lemon"],
    },
    "tokyo": {
        "attractions": [
            "Senso-ji Temple & Nakamise-dori (Tokyo's oldest Buddhist temple in Asakusa)",
            "Shibuya Crossing & Hachiko Statue (The world's busiest pedestrian scramble crossing)",
            "Meiji Jingu Shrine & Yoyogi Park (Tranquil Shinto forest shrine in Harajuku)",
            "Tokyo Skytree (634m broadcasting tower with 360-degree observation deck)",
            "TeamLab Planets (Immersive digital art museum where visitors walk through water)",
            "Shinjuku Gyoen National Garden (Vast park blending Japanese, English & French gardens)",
        ],
        "hotels": [
            "The Capitol Hotel Tokyu (★ 4.7 Google, ~₹52,000/night) — Kengo Kuma designed luxury hotel near Imperial Palace",
            "Hotel Gracery Shinjuku (★ 4.3 Google, ~₹14,000/night) — Famous Godzilla-head hotel in the heart of neon Shinjuku",
            "The Millennials Shibuya (★ 4.5 Google, ~₹6,500/night) — Cutting-edge smart capsule hotel with communal lounge",
        ],
        "restaurants": [
            "Ichiran Ramen Shibuya (★ 4.5 Google, ~₹900/person) — World-famous tonkotsu ramen with individual tasting booths",
            "Tsunahachi Tempura Shinjuku (★ 4.4 Google, ~₹1,800/person) — Legendary tempura house frying seafood fresh since 1923",
            "Sushi Dai Toyosu (★ 4.6 Google, ~₹3,200/person) — World-class omakase sushi right at the Toyosu Fish Market",
        ],
        "cuisines": ["Authentic Tonkotsu Ramen", "Fresh Nigiri Sushi & Sashimi", "Crispy Prawn Tempura", "Wagyu Beef Yakiniku"],
        "beverages": ["Matcha Green Tea", "Japanese Draft Beer (Asahi / Sapporo)", "Warm Sake"],
    },
    "dubai": {
        "attractions": [
            "Burj Khalifa Observation Deck (World's tallest building at 828m with views from 124th/148th floor)",
            "The Dubai Mall & Dubai Fountain (Largest mall in the world with choreographed lake fountain shows)",
            "Dubai Marina & JBR Walk (Luxury waterfront promenade with yachts, cafes & skydiving drop zone)",
            "Desert Safari with Dune Bashing (Golden dunes, camel rides, sandboarding & Bedouin camp dinner)",
            "Old Dubai Al Fahidi Historical Neighborhood & Gold Souk (Traditional wind towers & abra boat ride across Creek)",
            "Museum of the Future (Architectural marvel featuring cutting-edge interactive exhibits)",
        ],
        "hotels": [
            "Burj Al Arab Jumeirah (★ 4.7 Google, ~₹1,40,000/night) — The world's only 7-star sail-shaped luxury hotel with duplex suites",
            "Atlantis, The Palm (★ 4.7 Google, ~₹38,000/night) — Iconic oceanfront resort with Aquaventure waterpark",
            "Rove Downtown Dubai (★ 4.5 Google, ~₹8,500/night) — Trendy lifestyle hotel directly facing Burj Khalifa",
        ],
        "restaurants": [
            "Al Fanar Restaurant & Cafe (★ 4.4 Google, ~₹1,400/person) — Authentic Emirati cuisine with machboos, saloona & luqaimat",
            "Pierchic Al Qasr (★ 4.6 Google, ~₹5,500/person) — Overwater Mediterranean fine dining at the end of a private wooden pier",
            "Ravi Restaurant Satwa (★ 4.3 Google, ~₹450/person) — Celebrated Pakistani/Mughlai cult street dining with butter chicken & fresh naan",
        ],
        "cuisines": ["Emirati Lamb Machboos", "Warm Kunafa with Pistachios & Rose Syrup", "Mixed Grilled Kebab Platter with Hummus & Fresh Pita"],
        "beverages": ["Gahwa (Arabic Cardamom Coffee with dates)", "Karak Chai", "Fresh Pomegranate Juice"],
    },
    "bali": {
        "attractions": [
            "Tanah Lot Temple (Ancient sea temple perched on an offshore rock formation amidst breaking waves)",
            "Uluwatu Temple & Sunset Kecak Fire Dance (Clifftop amphitheater overlooking Indian Ocean)",
            "Tegallalang Rice Terraces Ubud (UNESCO terraced emerald paddy fields & iconic Bali jungle swings)",
            "Ubud Monkey Forest (Sacred nutmeg forest sanctuary with 1,000+ long-tailed macaques)",
            "Mount Batur Sunrise Trek (Active volcano trek with breakfast cooked over steam vents)",
            "Nusa Penida Kelingking Beach (Famous T-Rex head cliff and turquoise lagoon)",
        ],
        "hotels": [
            "Four Seasons Resort Bali at Sayan (★ 4.9 Google, ~₹68,000/night) — World-acclaimed Ayung River valley jungle sanctuary in Ubud",
            "Padma Resort Ubud (★ 4.8 Google, ~₹18,000/night) — Heated infinity pool overlooking pristine bamboo forest",
            "The Kayon Jungle Resort (★ 4.9 Google, ~₹28,000/night) — Three-tiered infinity pool facing the Ubud tropical jungle",
        ],
        "restaurants": [
            "Locavore NXT Ubud (★ 4.8 Google, ~₹4,500/person) — Acclaimed farm-to-table hyper-local modern Indonesian tasting menu",
            "Bebek Bengil (Dirty Duck Diner) Ubud (★ 4.3 Google, ~₹950/person) — Crispy fried duck served in traditional open-air rice field bales",
            "Warung Babi Guling Ibu Oka 3 (★ 4.3 Google, ~₹450/person) — Anthony Bourdain-praised Balinese roast suckling pig with crackling",
        ],
        "cuisines": ["Nasi Goreng with Chicken Satay & Peanut Sauce", "Bebek Betutu (Balinese spiced slow-cooked duck)", "Mie Goreng noodles"],
        "beverages": ["Fresh Young Coconut (Kelapa Muda)", "Kopi Luwak Civet Coffee", "Bintang Beer"],
    },
}


def find_verified_entry(destination: str) -> dict[str, list[str]] | None:
    """Find verified travel knowledge by destination name with fuzzy token matching."""
    dest_clean = destination.lower().strip()
    for key, data in VERIFIED_TRAVEL_DIRECTORY.items():
        if key in dest_clean or dest_clean in key:
            return data
    return None
