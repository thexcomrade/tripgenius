# d:\tripgenius\scratch\upgrade_tourism_database.py
import sys, re, os, shutil
import pandas as pd
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

ORIGINAL_CSV = r'D:\tripgenius\database\tourism.csv'
BACKEND_CSV = r'D:\tripgenius\backend\tourism.csv'
CHECKLIST_FILE = r'C:\Users\deva5\.gemini\antigravity\brain\7bd95c8b-4710-4b50-88cf-0db3af9b3d75\scratch\user_raw_checklist.txt'

# 1. Load existing dataset
df_orig = pd.read_csv(ORIGINAL_CSV)
print(f'Original dataset rows: {len(df_orig)}')
existing_names = set(df_orig['Name of the Place'].str.strip().str.lower())

# Curated lookup for well-known destinations
CURATED_DETAILS = {
    'sree padmanabhaswamy temple': {
        'Famous_For': 'World-renowned ancient Vishnu temple in Dravidian architecture with gold-plated Gopuram and sacred royal vaults',
        'Activities': 'Temple darshan, Spiritual prayer, Architecture photography, Traditional attire temple walk',
        'Category': 'Temple/Religious',
        'Travel_Style': 'Spiritual, Cultural, Photography',
        'Best_Season': 'October to March',
        'Budget_Category': 'Budget',
        'Duration_Days': 1
    },
    'jatayu earth’s center': {
        'Famous_For': 'World\'s largest bird sculpture and ecotourism park atop Jatayu Rock featuring cable car, adventure zone and 6D theater',
        'Activities': 'Cable car ride, Sculpture viewing, Rock climbing, Adventure games, Sunset photography',
        'Category': 'Sightseeing',
        'Travel_Style': 'Eco, Adventure, Photography',
        'Best_Season': 'September to March',
        'Budget_Category': 'Moderate',
        'Duration_Days': 1
    },
    'jatayu rock': {
        'Famous_For': 'Mythological giant rocky hillock in Chadayamangalam where bird demi-god Jatayu fell, crowned by the giant bird sculpture',
        'Activities': 'Hill trekking, Sculpture visit, Cable car journey, Panoramic photography',
        'Category': 'Sightseeing',
        'Travel_Style': 'Eco, Adventure, Photography',
        'Best_Season': 'September to March',
        'Budget_Category': 'Moderate',
        'Duration_Days': 1
    },
    'gavi': {
        'Famous_For': 'Pristine eco-tourism haven inside Periyar Tiger Reserve featuring evergreen forests, gaurs and reservoir boating',
        'Activities': 'Jungle safari, Reservoir boating, Forest trekking, Wildlife photography, Treehouse stay',
        'Category': 'Eco Tourism',
        'Travel_Style': 'Eco, Wildlife, Adventure, Photography',
        'Best_Season': 'September to March',
        'Budget_Category': 'Moderate',
        'Duration_Days': 2
    },
    'ponmudi': {
        'Famous_For': 'Scenic hill station with 22 hairpin turns, misty tea gardens, Golden Valley streams and winding mountain ridges',
        'Activities': 'Hairpin drive, Mountain trekking, Tea estate walks, Golden Valley dip, Sunset photography',
        'Category': 'Mountain/Hill',
        'Travel_Style': 'Eco, Adventure, Mountain, Photography',
        'Best_Season': 'September to March',
        'Budget_Category': 'Budget',
        'Duration_Days': 1
    },
    'kovalam beach': {
        'Famous_For': 'Iconic crescent coastline famous for the red-and-white Lighthouse Beach, calm waters and seaside seafood cafes',
        'Activities': 'Beach strolls, Sunset viewing, Lighthouse climb, Catamaran boating, Seafood dining',
        'Category': 'Beach',
        'Travel_Style': 'Beach, Leisure, Relaxation, Photography',
        'Best_Season': 'October to March',
        'Budget_Category': 'Moderate',
        'Duration_Days': 1
    },
    'lighthouse beach': {
        'Famous_For': 'Southernmost beach of Kovalam crowned by the iconic 35-meter Vizhinjam Lighthouse with panoramic Arabian Sea views',
        'Activities': 'Lighthouse spiral climb, Coastal photography, Sunset watching, Surfing, Beachside cafes',
        'Category': 'Beach',
        'Travel_Style': 'Beach, Leisure, Relaxation, Photography',
        'Best_Season': 'October to March',
        'Budget_Category': 'Budget',
        'Duration_Days': 1
    },
    'varkala cliff': {
        'Famous_For': 'Dramatic red laterite cliffs bordering the Arabian Sea with rooftop cafes, sunset viewpoints and mineral beach springs',
        'Activities': 'Cliff walking, Sunset watching, Tibetan souvenir shopping, Cafe dining, Surfing',
        'Category': 'Beach',
        'Travel_Style': 'Beach, Leisure, Relaxation, Photography',
        'Best_Season': 'October to March',
        'Budget_Category': 'Moderate',
        'Duration_Days': 1
    },
    'annapurna base camp': {
        'Famous_For': 'Iconic Himalayan amphitheatre trek in Nepal reaching 4,130m, surrounded by Annapurna I, Machapuchare and Hiunchuli',
        'Activities': 'High-altitude trekking, Teahouse stays, Machapuchare sunrise view, Hot spring bath at Jhinu, Alpine photography',
        'Category': 'Adventure',
        'Travel_Style': 'Adventure, Trekking, Expedition, Photography',
        'Best_Season': 'April to June, September to November',
        'Budget_Category': 'Moderate',
        'Duration_Days': 3
    },
    'everest base camp': {
        'Famous_For': 'World-famous high-altitude expedition in the Khumbu region reaching 5,364m at the foot of Mount Everest and Khumbu Icefall',
        'Activities': 'Alpine expedition, Kala Patthar summit view, Tengboche Monastery visit, Sherpa culture immersion, Glacial photography',
        'Category': 'Adventure',
        'Travel_Style': 'Adventure, Trekking, Expedition, Photography',
        'Best_Season': 'April to May, September to November',
        'Budget_Category': 'Luxury',
        'Duration_Days': 3
    },
    'chadar trek': {
        'Famous_For': 'Thrilling winter ice expedition walking directly on the frozen Zanskar River beneath towering Himalayan canyons',
        'Activities': 'Frozen river walking, Sub-zero ice camping, Tibb cave exploration, Nerak frozen waterfall visit, Ice photography',
        'Category': 'Adventure',
        'Travel_Style': 'Adventure, Trekking, Expedition, Photography',
        'Best_Season': 'January to February',
        'Budget_Category': 'Luxury',
        'Duration_Days': 3
    },
    'valley of flowers': {
        'Famous_For': 'UNESCO World Heritage alpine valley in Garhwal Himalayas blanketed with rare endemic blossoms and misty peaks',
        'Activities': 'Alpine botanical trekking, Floral photography, Hemkund Sahib pilgrimage, Nature walk',
        'Category': 'Garden/Nature',
        'Travel_Style': 'Eco, Nature, Trekking, Photography',
        'Best_Season': 'July to September',
        'Budget_Category': 'Moderate',
        'Duration_Days': 2
    },
    'har ki dun': {
        'Famous_For': 'Cradle-shaped hanging valley in Garhwal Himalayas surrounded by snow peaks, alpine meadows and ancient villages',
        'Activities': 'Valley trekking, Traditional village visits, Swargarohini peak view, Riverside camping',
        'Category': 'Adventure',
        'Travel_Style': 'Adventure, Trekking, Expedition, Photography',
        'Best_Season': 'April to June, September to November',
        'Budget_Category': 'Moderate',
        'Duration_Days': 3
    },
    'kedarkantha': {
        'Famous_For': 'Classic winter summit trek renowned for pristine pine forests, snowy campsites and 360-degree Himalayan views',
        'Activities': 'Snow summit trek, Pine forest trail walk, Juda Ka Talab camping, Sunrise summit photography',
        'Category': 'Adventure',
        'Travel_Style': 'Adventure, Trekking, Expedition, Photography',
        'Best_Season': 'December to April',
        'Budget_Category': 'Moderate',
        'Duration_Days': 2
    },
    'kashmir great lakes': {
        'Famous_For': 'Breathtaking wilderness trek crossing seven pristine alpine lakes surrounded by snow-capped Kashmiri peaks',
        'Activities': 'High-altitude lake circuit, Meadow trekking, Trout fishing, Wilderness camping, Alpine photography',
        'Category': 'Adventure',
        'Travel_Style': 'Adventure, Trekking, Expedition, Photography',
        'Best_Season': 'July to September',
        'Budget_Category': 'Moderate',
        'Duration_Days': 3
    },
    'pangong lake': {
        'Famous_For': 'High-altitude endorheic lake at 14,270 ft extending into Tibet, renowned for shifting blue and turquoise shades',
        'Activities': 'Lakeside camping, Stargazing, Color-change photography, Chang La pass crossing',
        'Category': 'Lake/Water',
        'Travel_Style': 'Eco, Adventure, Photography',
        'Best_Season': 'May to September',
        'Budget_Category': 'Moderate',
        'Duration_Days': 1
    },
    'khardung la': {
        'Famous_For': 'One of the world\'s highest motorable mountain passes at 17,982 ft offering views of the Karakoram range',
        'Activities': 'High-altitude mountain drive, Photography at summit sign, Mountain biking, Snow viewing',
        'Category': 'Mountain/Hill',
        'Travel_Style': 'Adventure, Eco, Photography',
        'Best_Season': 'May to September',
        'Budget_Category': 'Budget',
        'Duration_Days': 1
    },
    'eiffel tower': {
        'Famous_For': 'Iconic 330-meter wrought-iron lattice tower on the Champ de Mars offering panoramic views of Paris',
        'Activities': 'Summit elevator ascent, Champagne bar, Night illumination viewing, Trocadéro photography',
        'Category': 'Sightseeing',
        'Travel_Style': 'Cultural, Leisure, Photography',
        'Best_Season': 'May to October',
        'Budget_Category': 'Moderate',
        'Duration_Days': 1
    },
    'louvre': {
        'Famous_For': 'World\'s largest art museum and historic royal palace housing masterworks like the Mona Lisa and Venus de Milo',
        'Activities': 'Art gallery tours, Glass Pyramid photography, Historic wing exploration, Curated audio guides',
        'Category': 'Heritage',
        'Travel_Style': 'Cultural, Educational, Photography',
        'Best_Season': 'Year-round',
        'Budget_Category': 'Moderate',
        'Duration_Days': 1
    },
    'mount fuji': {
        'Famous_For': 'Japan\'s sacred 3,776-meter volcanic peak with iconic snow-capped symmetry, shrines and surrounding five lakes',
        'Activities': 'Sunrise summit climb, Lake Kawaguchiko photography, Chureito Pagoda views, Onsen bath',
        'Category': 'Mountain/Hill',
        'Travel_Style': 'Adventure, Eco, Photography',
        'Best_Season': 'July to September',
        'Budget_Category': 'Moderate',
        'Duration_Days': 2
    },
    'matterhorn': {
        'Famous_For': 'Iconic pyramid-shaped Alpine peak towering over Zermatt, one of the most photographed mountains in the world',
        'Activities': 'Gornergrat railway ride, Alpine hiking, Skiing, Matterhorn Glacier Paradise visit, Cable car',
        'Category': 'Mountain/Hill',
        'Travel_Style': 'Adventure, Eco, Mountain, Photography',
        'Best_Season': 'June to September, December to March',
        'Budget_Category': 'Luxury',
        'Duration_Days': 2
    }
}

# 2. Parse checklist file
with open(CHECKLIST_FILE, 'r', encoding='utf-8') as f:
    text = f.read()

lines = [l.strip() for l in text.splitlines()]

candidates = {}

def add_candidate(name, country, state, district, source):
    name_clean = name.strip()
    name_clean = re.sub(r'^\d+[\.\)]\s*', '', name_clean)
    name_clean = re.sub(r'^[•\-\*]\s*', '', name_clean)
    name_clean = re.sub(r'\[.*?\]\(.*?\)', '', name_clean)
    name_clean = name_clean.strip()
    if not name_clean or len(name_clean) < 2:
        return
    # Skip meta lines
    if any(name_clean.lower().startswith(x) for x in [
        'kerala has', 'the government', 'for what you', 'recent 2026', 'tiger /',
        'kerala wildlife', 'char dham', 'chota char dham', 'jyotirlingas', 'major buddhist',
        'sikh', 'if you\'re making', 'other 28 states', 'union territories', 'india\'s major',
        'best beach', 'major pilgrimage', 'international destinations', 'the big international',
        'for a serious'
    ]):
        return
    # Skip category headings
    if name_clean.lower() in [
        'himalayas', 'western ghats', 'desert safari', 'jungle safari', 'tiger safari',
        'whale watching', 'scuba diving', 'snorkelling', 'skydiving', 'paragliding',
        'bungee jumping', 'rafting', 'camping', 'trekking', 'snow trekking', 'northern lights',
        'glacier visit', 'volcano', 'cave exploration', 'island hopping', 'houseboat',
        'train journey', 'luxury train', 'motorcycle road trip', 'himalayan road trip',
        'coastal road trip', 'desert road trip', 'temple pilgrimage', 'unesco heritage site',
        'fort exploration', 'palace stay', 'beach sunrise', 'beach sunset', 'mountain sunrise',
        'mountain sunset', 'wildlife photography', 'star gazing', 'village tourism', 'tribal tourism',
        'food tourism', 'cultural festival', 'music festival', 'carnival', 'christmas market',
        'cherry blossom', 'autumn foliage', 'tulip fields', 'tea plantation', 'coffee plantation',
        'wine region', 'safari', 'cruise', 'desert camping', 'igloo/glass-dome stay', 'treehouse stay',
        'luxury resort', 'backpacking', 'solo trip', 'road trip with friends', 'international trip',
        'multi-country trip', 'waterfall', 'waterfalls', 'glaciers', 'tea gardens', 'marine diving',
        'luxury resort islands', 'glass igloos'
    ]:
        return

    norm = name_clean.lower()
    if norm not in candidates:
        candidates[norm] = {
            'Name': name_clean,
            'Country': country.strip(),
            'State': state.strip(),
            'District': district.strip(),
            'Source': source
        }

# Section 12 (892 arrow items)
for l in lines[2050:]:
    m = re.match(r'^\d+\.\s*([^→]+)→([^→]+)→([^→]+)→(.+)$', l)
    if m:
        c, s, d, p = m.group(1).strip(), m.group(2).strip(), m.group(3).strip(), m.group(4).strip()
        add_candidate(p, c, s, d, 'sec12')

# Section 1 (Kerala 14 districts)
kerala_lines = lines[17:560]
current_district = None
for l in kerala_lines:
    if not l or l.startswith('[') or l.startswith('1. 🌴'):
        continue
    m_dist = re.match(r'^\d+\.\s*(.+)$', l)
    if m_dist:
        current_district = m_dist.group(1).strip()
    elif current_district and l:
        add_candidate(l, 'India', 'Kerala', current_district, 'sec1_kerala')

# Section 10 (International destinations)
intl_lines = lines[1582:1907]
current_country = None
for l in intl_lines:
    if not l or l.startswith('✈️') or l.startswith('Recent') or l.startswith('['):
        continue
    if re.match(r'^[^\w\s]*[\U0001F1E6-\U0001F1FF]{2}', l) or any(l.endswith(c) for c in [
        'Thailand', 'UAE', 'Singapore', 'Malaysia', 'Indonesia', 'Sri Lanka', 'Nepal', 'Vietnam',
        'Maldives', 'Mauritius', 'Australia', 'United Kingdom', 'France', 'Italy', 'Switzerland',
        'Japan', 'South Korea', 'USA', 'Canada', 'New Zealand', 'Egypt', 'Turkey', 'Greece', 'Spain',
        'Austria', 'Germany', 'Netherlands', 'Norway', 'Finland', 'Iceland', 'South Africa', 'Kenya',
        'Tanzania', 'Bhutan'
    ]):
        current_country = re.sub(r'^[^\w\s]+', '', l).strip()
    elif current_country and l:
        add_candidate(l, current_country, current_country, current_country, 'sec10_intl')

# Section 4 (Treks)
in_trek = False
for l in lines:
    if '🏔️ 4. INDIA\'S MAJOR TREKKING LIST' in l:
        in_trek = True
        continue
    if in_trek and ('🐅 5. MAJOR WILDLIFE' in l or '5. MAJOR WILDLIFE' in l):
        in_trek = False
        break
    if in_trek and l and len(l) > 1 and not (len(l) == 1 and l.isalpha()):
        c = 'Nepal' if 'nepal' in l.lower() or 'everest' in l.lower() or 'annapurna' in l.lower() else 'India'
        s = 'Gandaki' if 'annapurna' in l.lower() else ('Solukhumbu' if 'everest' in l.lower() else 'Himalayas')
        add_candidate(l, c, s, 'Trekking Route', 'sec4_treks')

# Section 3 (UTs)
s3_lines = lines[1116:1236]
uts = ['Delhi', 'Jammu & Kashmir', 'Ladakh', 'Andaman & Nicobar', 'Lakshadweep', 'Puducherry', 'Chandigarh', 'Dadra & Nagar Haveli and Daman & Diu']
current_ut = None
for l in s3_lines:
    if any(l == u or l.startswith(u) for u in uts):
        current_ut = l.split('/')[0].strip()
    elif current_ut and l and not l.startswith('🇮🇳'):
        add_candidate(l, 'India', current_ut, current_ut, 'sec3_uts')

# Section 2 (Other 28 States)
s2_lines = lines[560:1116]
indian_states = ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal']
current_state = None
for l in s2_lines:
    if l in indian_states:
        current_state = l
    elif current_state and l and not l.startswith('🇮🇳'):
        add_candidate(l, 'India', current_state, current_state, 'sec2_states')

# Filter for brand new places
brand_new = [v for k, v in candidates.items() if k not in existing_names]
print(f'Total candidates: {len(candidates)}')
print(f'Brand new places to add: {len(brand_new)}')

# 3. Dynamic metadata generator
def infer_metadata(item):
    name = item['Name']
    norm = name.lower()
    country = item['Country']
    state = item['State']
    district = item['District']

    # 1. Curated exact match
    if norm in CURATED_DETAILS:
        c_data = CURATED_DETAILS[norm]
        return {
            'Name of the Place': name,
            'District': district,
            'Famous_For': c_data['Famous_For'],
            'Activities': c_data['Activities'],
            'State': state,
            'Country': country,
            'Category': c_data['Category'],
            'Travel_Style': c_data['Travel_Style'],
            'Best_Season': c_data['Best_Season'],
            'Budget_Category': c_data['Budget_Category'],
            'Duration_Days': c_data['Duration_Days']
        }

    # 2. Determine Category
    if any(k in norm for k in ['waterfall', 'waterfalls', 'falls', 'cascade', 'cataract']):
        cat = 'Waterfall'
    elif any(k in norm for k in ['beach', 'coast', 'cove', 'shore', 'cliff', 'promenade', 'atoll']):
        cat = 'Beach'
    elif any(k in norm for k in ['lake', 'dam', 'reservoir', 'backwaters', 'backwater', 'river', 'canal', 'barrage', 'sarovar', 'kund', 'lagoon']):
        cat = 'Lake/Water'
    elif any(k in norm for k in ['island', 'dweep', 'isle', 'thuruthu', 'atoll']):
        cat = 'Island'
    elif any(k in norm for k in ['cave', 'caves', 'cavern', 'grotto', 'rock cut', 'stepwell', 'baoli']):
        cat = 'Cave/Geological'
    elif any(k in norm for k in ['temple', 'mandir', 'ashram', 'mutt', 'church', 'cathedral', 'basilica', 'mosque', 'masjid', 'gurudwara', 'monastery', 'gompa', 'stupa', 'shrine', 'dham', 'pagoda', 'synagogue', 'pilgrimage', 'jyotirlinga', 'sabarimala', 'aazhimala', 'sivagiri', 'darshan', 'kovil']):
        cat = 'Temple/Religious'
    elif any(k in norm for k in ['fort', 'palace', 'castle', 'museum', 'monument', 'ruins', 'heritage', 'tomb', 'gateway', 'minar', 'mahal', 'qila', 'chateau', 'citadel', 'pyramid', 'colosseum', 'acropolis', 'jail']):
        cat = 'Heritage'
    elif any(k in norm for k in ['wildlife', 'sanctuary', 'national park', 'safari', 'tiger', 'lion', 'elephant', 'bird', 'zoo', 'reserve', 'biosphere']):
        cat = 'Wildlife'
    elif any(k in norm for k in ['trek', 'trail', 'trails', 'pass', 'climb', 'expedition', 'base camp', 'summit']) or item['Source'] == 'sec4_treks':
        cat = 'Adventure'
    elif any(k in norm for k in ['peak', 'hill', 'hills', 'viewpoint', 'view point', 'mountain', 'mount', 'ridge', 'plateau', 'bugyal', 'valley', 'gorge', 'canyon', 'mala', 'medu', 'shola', 'top']):
        cat = 'Mountain/Hill'
    elif any(k in norm for k in ['garden', 'park', 'botanical', 'forest', 'plantation', 'estate', 'tea', 'valley of flowers']):
        cat = 'Garden/Nature'
    else:
        cat = 'Sightseeing'

    # 3. Dynamic Famous_For
    loc_desc = f"{district}, {state}" if district != state else f"{state}, {country}"
    if cat == 'Waterfall':
        famous = f"Scenic natural waterfall cascading amidst verdant forest landscapes in {loc_desc}, popular for nature photography and stream walks"
        activities = "Waterfall viewing, Nature photography, Forest trekking, Stream dip, Scenic walking"
        travel_style = "Eco, Nature, Leisure, Photography"
        duration = 1
        budget = "Budget"
    elif cat == 'Beach':
        famous = f"Picturesque coastal stretch in {loc_desc} known for golden sands, sunset vistas, gentle waves and waterside relaxation"
        activities = "Beach strolls, Sunset viewing, Coastal photography, Swimming, Seafood dining"
        travel_style = "Beach, Leisure, Relaxation, Photography"
        duration = 1
        budget = "Budget" if country == 'India' else "Moderate"
    elif cat == 'Lake/Water':
        famous = f"Serene freshwater lake and scenic waterfront haven in {loc_desc} offering tranquil boating, waterside promenades and birdwatching"
        activities = "Boating, Houseboat cruise, Waterside walking, Scenic photography, Birdwatching"
        travel_style = "Eco, Leisure, Photography"
        duration = 1
        budget = "Moderate"
    elif cat == 'Island':
        famous = f"Enchanting island destination in {loc_desc} surrounded by pristine waters, coastal biodiversity and tropical panoramas"
        activities = "Island hopping, Snorkeling, Beach relaxation, Marine photography, Boat rides"
        travel_style = "Island, Leisure, Adventure, Photography"
        duration = 2
        budget = "Moderate" if country == 'India' else "Luxury"
    elif cat == 'Cave/Geological':
        famous = f"Remarkable ancient geological formation and cavern system in {loc_desc} showcasing natural stalactites, archaeology and rock carvings"
        activities = "Cave exploration, Geological photography, Guided cavern walk, Archaeological study"
        travel_style = "Adventure, Educational, Photography"
        duration = 1
        budget = "Budget"
    elif cat == 'Temple/Religious':
        famous = f"Sacred pilgrimage shrine and spiritual sanctum in {loc_desc} renowned for traditional devotional rituals and classical temple architecture"
        activities = "Temple darshan, Spiritual meditation, Heritage architecture walk, Devotional rituals, Photography"
        travel_style = "Spiritual, Cultural, Photography"
        duration = 1
        budget = "Budget"
    elif cat == 'Heritage':
        famous = f"Historic architectural monument in {loc_desc} reflecting regional royalty, classical masonry and rich cultural heritage"
        activities = "Historical exploration, Heritage photography, Guided monument tour, Architecture appreciation"
        travel_style = "Cultural, Heritage, Photography"
        duration = 1
        budget = "Budget" if country == 'India' else "Moderate"
    elif cat == 'Wildlife':
        famous = f"Protected biodiversity sanctuary in {loc_desc} harboring diverse wildlife species, lush jungle canopies and guided safari trails"
        activities = "Jungle safari, Wildlife spotting, Birdwatching, Nature photography, Forest trails"
        travel_style = "Eco, Wildlife, Adventure, Photography"
        duration = 2
        budget = "Moderate"
    elif cat == 'Adventure':
        famous = f"Renowned adventure and trekking route in {loc_desc} offering rugged trails, panoramic alpine views and wilderness camping"
        activities = "High-altitude trekking, Wilderness camping, Alpine photography, Expedition hiking, Sunrise summit viewing"
        travel_style = "Adventure, Trekking, Expedition, Photography"
        duration = 2
        budget = "Moderate"
    elif cat == 'Mountain/Hill':
        famous = f"Scenic hill haven in {loc_desc} offering cool mountain breezes, misty valleys, tea-clad slopes and panoramic viewpoints"
        activities = "Mountain trekking, Panoramic photography, Sunrise viewing, Nature walks, Cloud gazing"
        travel_style = "Eco, Adventure, Mountain, Photography"
        duration = 1
        budget = "Moderate"
    elif cat == 'Garden/Nature':
        famous = f"Lush natural park and botanical haven in {loc_desc} featuring scenic greenery, floral diversity and peaceful walking paths"
        activities = "Nature walks, Botanical exploration, Flora photography, Picnicking, Leisure strolls"
        travel_style = "Eco, Nature, Leisure, Photography"
        duration = 1
        budget = "Budget"
    else: # Sightseeing
        famous = f"Popular travel destination in {loc_desc} celebrated for local charm, cultural atmosphere and vibrant visitor experiences"
        activities = "City sightseeing, Street exploration, Cultural photography, Local dining, Shopping"
        travel_style = "Cultural, Leisure, Photography"
        duration = 1
        budget = "Moderate"

    # 4. Best Season
    if country == 'India':
        if state == 'Kerala':
            season = "June to December" if cat == 'Waterfall' else "September to March"
        elif state in ['Himachal Pradesh', 'Uttarakhand', 'Jammu and Kashmir', 'Ladakh', 'Sikkim', 'Arunachal Pradesh', 'Himalayas']:
            if cat in ['Adventure', 'Mountain/Hill']:
                season = "May to October"
            else:
                season = "March to June, September to November"
        elif state in ['Goa', 'Maharashtra', 'Karnataka', 'Tamil Nadu', 'Andhra Pradesh', 'Telangana']:
            season = "October to March"
        elif state in ['Rajasthan', 'Gujarat', 'Madhya Pradesh', 'Delhi', 'Punjab', 'Haryana', 'Uttar Pradesh', 'Bihar']:
            season = "October to March"
        elif state in ['Andaman and Nicobar Islands', 'Lakshadweep']:
            season = "October to May"
        else:
            season = "October to March"
    else:
        # International
        if country in ['United Kingdom', 'France', 'Italy', 'Switzerland', 'Germany', 'Austria', 'Netherlands', 'Norway', 'Finland', 'Iceland', 'Spain', 'Greece']:
            season = "May to October"
        elif country in ['USA', 'Canada']:
            season = "May to October"
        elif country in ['Thailand', 'Vietnam', 'Malaysia', 'Singapore', 'Indonesia', 'Sri Lanka']:
            season = "November to April"
        elif country in ['UAE', 'Qatar', 'Oman', 'Saudi Arabia', 'Egypt']:
            season = "November to March"
        elif country in ['Japan', 'South Korea']:
            season = "March to May, September to November"
        elif country in ['Australia', 'New Zealand', 'South Africa']:
            season = "October to April"
        elif country in ['Nepal', 'Bhutan']:
            season = "March to May, September to November"
        else:
            season = "Year-round"

    return {
        'Name of the Place': name,
        'District': district,
        'Famous_For': famous,
        'Activities': activities,
        'State': state,
        'Country': country,
        'Category': cat,
        'Travel_Style': travel_style,
        'Best_Season': season,
        'Budget_Category': budget,
        'Duration_Days': duration
    }

# 4. Process all brand new places
new_rows = []
for item in brand_new:
    row = infer_metadata(item)
    new_rows.append(row)

df_new = pd.DataFrame(new_rows)
print(f'New rows prepared: {len(df_new)}')
print('\nCategory distribution of new entries:')
print(df_new['Category'].value_counts())
print('\nCountry distribution of new entries (top 10):')
print(df_new['Country'].value_counts().head(10))

# 5. Concatenate and clean
df_final = pd.concat([df_orig, df_new], ignore_index=True)
# Ensure columns match exact schema
schema_cols = ['Name of the Place', 'District', 'Famous_For', 'Activities', 'State', 'Country', 'Category', 'Travel_Style', 'Best_Season', 'Budget_Category', 'Duration_Days']
df_final = df_final[schema_cols]

# Deduplicate by Name of the Place (case insensitive) keeping first
df_final['lower_name'] = df_final['Name of the Place'].str.strip().str.lower()
df_final = df_final.drop_duplicates(subset=['lower_name'], keep='first').drop(columns=['lower_name'])

print(f'\nOriginal count: {len(df_orig)}')
print(f'Appended count: {len(df_new)}')
print(f'Final total rows: {len(df_final)}')
print(f'Net new rows added: {len(df_final) - len(df_orig)}')

# Check for any nulls
nulls = df_final.isnull().sum()
print('\nNull counts:')
print(nulls)

# Create backups
shutil.copyfile(ORIGINAL_CSV, ORIGINAL_CSV + '.bak')
shutil.copyfile(BACKEND_CSV, BACKEND_CSV + '.bak')
print('Backups created successfully.')

# Save to both paths
df_final.to_csv(ORIGINAL_CSV, index=False, encoding='utf-8')
df_final.to_csv(BACKEND_CSV, index=False, encoding='utf-8')
print(f'Saved updated dataset to {ORIGINAL_CSV}')
print(f'Saved updated dataset to {BACKEND_CSV}')
