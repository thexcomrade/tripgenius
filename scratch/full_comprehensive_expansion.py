# scratch/full_comprehensive_expansion.py
import sys, os, re, unicodedata, shutil
import pandas as pd
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

ORIGINAL_CSV = r'D:\tripgenius\database\tourism.csv'
BACKEND_CSV = r'D:\tripgenius\backend\tourism.csv'
PROMPT_FILE = r'd:\tripgenius\scratch\expansion_user_prompt.txt'

df_orig = pd.read_csv(ORIGINAL_CSV)
print(f"Base dataset rows: {len(df_orig)}")

existing_names = set(df_orig['Name of the Place'].str.strip().str.lower())
seen_names = set(existing_names)
new_records = []

def clean_ascii(text):
    if not isinstance(text, str):
        return str(text) if text is not None else ""
    t = text.replace('\u2019', "'").replace('\u2018', "'")
    t = t.replace('\u201c', '"').replace('\u201d', '"')
    t = t.replace('\u2014', ' - ').replace('\u2013', ' - ')
    t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode('ascii')
    return ' '.join(t.split()).strip()

def infer_category(name, hint=""):
    norm = (name + " " + hint).lower()
    if any(k in norm for k in ['waterfall', 'waterfalls', 'falls', 'cascade', 'cataract']):
        return 'Waterfall'
    if any(k in norm for k in ['beach', 'coast', 'cove', 'shore', 'cliff', 'promenade', 'atoll', 'lagoon', 'bay', 'playa']):
        return 'Beach'
    if any(k in norm for k in ['lake', 'dam', 'reservoir', 'backwaters', 'backwater', 'river', 'canal', 'barrage', 'sarovar', 'kund', 'tal', 'lac ', 'loch', 'gulf']):
        return 'Lake/Water'
    if any(k in norm for k in ['island', 'dweep', 'isle', 'thuruthu', 'atoll', 'cay', 'ilha', 'archipelago']):
        return 'Island'
    if any(k in norm for k in ['cave', 'caves', 'cavern', 'grotto', 'rock cut', 'stepwell', 'baoli', 'sinkhole', 'cenote', 'crater', 'caldera']):
        return 'Cave/Geological'
    if any(k in norm for k in ['temple', 'mandir', 'ashram', 'mutt', 'church', 'cathedral', 'basilica', 'mosque', 'masjid', 'gurudwara', 'monastery', 'gompa', 'stupa', 'shrine', 'dham', 'pagoda', 'synagogue', 'pilgrimage', 'jyotirlinga', 'sabarimala', 'darshan', 'kovil', 'abbey', 'sanctuary of truth']):
        return 'Temple/Religious'
    if any(k in norm for k in ['fort', 'palace', 'castle', 'museum', 'monument', 'ruins', 'heritage', 'tomb', 'gateway', 'minar', 'mahal', 'qila', 'chateau', 'citadel', 'pyramid', 'colosseum', 'acropolis', 'jail', 'memorial', 'bridge', 'fortress', 'pyramids', 'alcazar', 'belfry', 'hall of mirrors']):
        return 'Heritage'
    if any(k in norm for k in ['wildlife', 'sanctuary', 'national park', 'safari', 'tiger', 'lion', 'elephant', 'bird', 'zoo', 'reserve', 'biosphere', 'game reserve', 'delta', 'penguin', 'whale', 'koala', 'kangaroo', 'quokka', 'orangutan', 'panda']):
        return 'Wildlife'
    if any(k in norm for k in ['trek', 'trail', 'trails', 'pass', 'climb', 'expedition', 'base camp', 'summit', 'skiing', 'paragliding', 'scuba', 'rafting', 'gondola']):
        return 'Adventure'
    if any(k in norm for k in ['peak', 'hill', 'hills', 'viewpoint', 'view point', 'mountain', 'mount', 'ridge', 'plateau', 'bugyal', 'valley', 'gorge', 'canyon', 'mala', 'medu', 'shola', 'top', 'volcano', 'gap']):
        return 'Mountain/Hill'
    if any(k in norm for k in ['garden', 'park', 'botanical', 'forest', 'plantation', 'estate', 'tea', 'flowers', 'tulip', 'vineyard', 'oasis']):
        return 'Garden/Nature'
    return 'Sightseeing'

def build_spot_record(name, district, state, country, category=None, hint=""):
    name_clean = clean_ascii(name)
    district_clean = clean_ascii(district)
    state_clean = clean_ascii(state)
    country_clean = clean_ascii(country)

    if not category:
        category = infer_category(name_clean, hint)

    loc_desc = f"{district_clean}, {state_clean}" if district_clean != state_clean else f"{state_clean}, {country_clean}"

    if category == 'Waterfall':
        famous = f"Scenic natural waterfall cascading amidst verdant forest landscapes in {loc_desc}, popular for nature photography and stream walks"
        activities = "Waterfall viewing, Nature photography, Forest trekking, Stream dip, Scenic walking"
        travel_style = "Eco, Nature, Leisure, Photography"
        duration = 1
        budget = "Budget"
    elif category == 'Beach':
        famous = f"Picturesque coastal stretch in {loc_desc} known for golden sands, sunset vistas, gentle waves and waterside relaxation"
        activities = "Beach strolls, Sunset viewing, Coastal photography, Swimming, Seafood dining"
        travel_style = "Beach, Leisure, Relaxation, Photography"
        duration = 1
        budget = "Budget" if country_clean == 'India' else "Moderate"
    elif category == 'Lake/Water':
        famous = f"Serene freshwater lake and scenic waterfront haven in {loc_desc} offering tranquil boating, waterside promenades and birdwatching"
        activities = "Boating, Houseboat cruise, Waterside walking, Scenic photography, Birdwatching"
        travel_style = "Eco, Leisure, Photography"
        duration = 1
        budget = "Moderate"
    elif category == 'Island':
        famous = f"Enchanting island destination in {loc_desc} surrounded by pristine waters, coastal biodiversity and tropical panoramas"
        activities = "Island hopping, Snorkeling, Beach relaxation, Marine photography, Boat rides"
        travel_style = "Island, Leisure, Adventure, Photography"
        duration = 2
        budget = "Moderate" if country_clean == 'India' else "Luxury"
    elif category == 'Cave/Geological':
        famous = f"Remarkable ancient geological formation and cavern system in {loc_desc} showcasing natural stalactites, archaeology and rock carvings"
        activities = "Cave exploration, Geological photography, Guided cavern walk, Archaeological study"
        travel_style = "Adventure, Educational, Photography"
        duration = 1
        budget = "Budget"
    elif category == 'Temple/Religious':
        famous = f"Sacred pilgrimage shrine and spiritual sanctum in {loc_desc} renowned for traditional devotional rituals and classical temple architecture"
        activities = "Temple darshan, Spiritual meditation, Heritage architecture walk, Devotional rituals, Photography"
        travel_style = "Spiritual, Cultural, Photography"
        duration = 1
        budget = "Budget"
    elif category == 'Heritage':
        famous = f"Historic architectural monument in {loc_desc} reflecting regional royalty, classical masonry and rich cultural heritage"
        activities = "Historical exploration, Heritage photography, Guided monument tour, Architecture appreciation"
        travel_style = "Cultural, Heritage, Photography"
        duration = 1
        budget = "Budget" if country_clean == 'India' else "Moderate"
    elif category == 'Wildlife':
        famous = f"Protected biodiversity sanctuary in {loc_desc} harboring diverse wildlife species, lush jungle canopies and guided safari trails"
        activities = "Jungle safari, Wildlife spotting, Birdwatching, Nature photography, Forest trails"
        travel_style = "Eco, Wildlife, Adventure, Photography"
        duration = 2
        budget = "Moderate"
    elif category == 'Adventure':
        famous = f"Renowned adventure and trekking route in {loc_desc} offering rugged trails, panoramic alpine views and wilderness camping"
        activities = "High-altitude trekking, Wilderness camping, Alpine photography, Expedition hiking, Sunrise summit viewing"
        travel_style = "Adventure, Trekking, Expedition, Photography"
        duration = 2
        budget = "Moderate"
    elif category == 'Mountain/Hill':
        famous = f"Scenic hill haven in {loc_desc} offering cool mountain breezes, misty valleys, tea-clad slopes and panoramic viewpoints"
        activities = "Mountain trekking, Panoramic photography, Sunrise viewing, Nature walks, Cloud gazing"
        travel_style = "Eco, Adventure, Mountain, Photography"
        duration = 1
        budget = "Moderate"
    elif category == 'Garden/Nature':
        famous = f"Lush natural park and botanical haven in {loc_desc} featuring scenic greenery, floral diversity and peaceful walking paths"
        activities = "Nature walks, Botanical exploration, Flora photography, Picnicking, Leisure strolls"
        travel_style = "Eco, Nature, Leisure, Photography"
        duration = 1
        budget = "Budget"
    else:  # Sightseeing
        famous = f"Popular travel destination in {loc_desc} celebrated for local charm, cultural atmosphere and vibrant visitor experiences"
        activities = "City sightseeing, Street exploration, Cultural photography, Local dining, Shopping"
        travel_style = "Cultural, Leisure, Photography"
        duration = 1
        budget = "Moderate"

    # Best Season logic
    if country_clean == 'India':
        if state_clean == 'Kerala':
            season = "June to December" if category == 'Waterfall' else "September to March"
        elif state_clean in ['Himachal Pradesh', 'Uttarakhand', 'Jammu and Kashmir', 'Ladakh', 'Sikkim', 'Arunachal Pradesh', 'Himalayas']:
            if category in ['Adventure', 'Mountain/Hill']:
                season = "May to October"
            else:
                season = "March to June, September to November"
        elif state_clean in ['Goa', 'Maharashtra', 'Karnataka', 'Tamil Nadu', 'Andhra Pradesh', 'Telangana']:
            season = "October to March"
        elif state_clean in ['Rajasthan', 'Gujarat', 'Madhya Pradesh', 'Delhi', 'Punjab', 'Haryana', 'Uttar Pradesh', 'Bihar', 'Jharkhand', 'Chhattisgarh', 'Odisha', 'West Bengal']:
            season = "October to March"
        elif state_clean in ['Assam', 'Meghalaya', 'Nagaland', 'Manipur', 'Mizoram', 'Tripura']:
            season = "October to April"
        elif state_clean in ['Andaman and Nicobar Islands', 'Lakshadweep']:
            season = "October to May"
        else:
            season = "October to March"
    else:
        if country_clean in ['United Kingdom', 'France', 'Italy', 'Switzerland', 'Germany', 'Austria', 'Netherlands', 'Norway', 'Sweden', 'Finland', 'Iceland', 'Ireland', 'Bulgaria', 'Bosnia and Herzegovina', 'Croatia', 'Czech Republic', 'Hungary', 'Poland', 'Slovakia', 'Slovenia', 'Estonia', 'Lithuania', 'Luxembourg', 'Liechtenstein', 'Malta', 'Montenegro', 'North Macedonia', 'Romania', 'Serbia', 'Ukraine', 'Belgium', 'Denmark', 'Portugal', 'Spain', 'Greece']:
            season = "May to October"
        elif country_clean in ['USA', 'Canada']:
            season = "May to October"
        elif country_clean in ['Thailand', 'Vietnam', 'Malaysia', 'Singapore', 'Indonesia', 'Sri Lanka', 'Philippines', 'Brunei', 'Cambodia', 'Laos', 'Myanmar']:
            season = "November to April"
        elif country_clean in ['UAE', 'Qatar', 'Oman', 'Saudi Arabia', 'Egypt', 'Jordan', 'Bahrain', 'Kuwait', 'Lebanon', 'Iran', 'Iraq', 'Algeria', 'Tunisia', 'Libya', 'Morocco']:
            season = "November to March"
        elif country_clean in ['Japan', 'South Korea', 'China', 'Taiwan', 'Mongolia']:
            season = "March to May, September to November"
        elif country_clean in ['Australia', 'New Zealand', 'South Africa', 'Argentina', 'Chile', 'Brazil', 'Uruguay', 'Paraguay', 'Botswana', 'Namibia', 'Zimbabwe', 'Zambia', 'Lesotho', 'Eswatini']:
            season = "October to April"
        elif country_clean in ['Nepal', 'Bhutan']:
            season = "March to May, September to November"
        elif country_clean in ['Kenya', 'Tanzania', 'Uganda', 'Rwanda', 'Madagascar']:
            season = "July to October, January to February"
        else:
            season = "Year-round"

    return {
        'Name of the Place': name_clean,
        'District': district_clean,
        'Famous_For': famous,
        'Activities': activities,
        'State': state_clean,
        'Country': country_clean,
        'Category': category,
        'Travel_Style': travel_style,
        'Best_Season': season,
        'Budget_Category': budget,
        'Duration_Days': duration
    }

def add_spot(name, district, state, country, category=None, hint=""):
    name_clean = clean_ascii(name).strip()
    norm = name_clean.lower()
    if not name_clean or norm in seen_names or len(name_clean) < 3:
        return
    seen_names.add(norm)
    rec = build_spot_record(name_clean, district, state, country, category, hint)
    new_records.append(rec)

# =========================================================================
# STEP 1: Parse 103 Missing Sovereign Countries from Prompt
# =========================================================================
print("1. Parsing Missing Sovereign Countries from prompt...")
with open(PROMPT_FILE, 'r', encoding='utf-8') as f:
    text = f.read()

country_sections = re.findall(r'^###\s+[^\w\s]*\s*([A-Za-z\s,\'\-]+)\s*\n+(.*?)(?=\n###|\n---|\Z)', text, re.MULTILINE | re.DOTALL)
print(f"Found {len(country_sections)} sections.")

for c_raw, content in country_sections:
    country = clean_ascii(c_raw).strip()
    # Skip Kerala here as it is processed as Kerala state districts in Step 2
    if country.lower() == 'kerala':
        continue
    items = re.split(r'[,;\n]\s*', content)
    for it in items:
        it_clean = clean_ascii(it).strip()
        it_clean = re.sub(r'^(?:and\s+)?(?:additional\s+|numerous\s+|other\s+).*$', '', it_clean, flags=re.IGNORECASE)
        it_clean = re.sub(r'\s+and\s+other\s+.*$', '', it_clean, flags=re.IGNORECASE)
        it_clean = re.sub(r'\s+and\s+additional\s+.*$', '', it_clean, flags=re.IGNORECASE)
        it_clean = re.sub(r'\s+and\s+numerous\s+.*$', '', it_clean, flags=re.IGNORECASE)
        it_clean = re.sub(r'^\s*-\s*', '', it_clean)
        if it_clean and len(it_clean) > 2 and not it_clean.lower().startswith('and '):
            add_spot(it_clean, country, country, country)

print(f"New spots after country sections: {len(new_records)}")

# =========================================================================
# STEP 2: Parse All 14 Kerala Districts from Prompt
# =========================================================================
print("2. Parsing Kerala Districts from prompt...")
kerala_districts = [
    'Thiruvananthapuram', 'Kollam', 'Pathanamthitta', 'Alappuzha', 
    'Kottayam', 'Idukki', 'Ernakulam', 'Thrissur', 'Palakkad', 
    'Malappuram', 'Kozhikode', 'Wayanad', 'Kannur', 'Kasaragod'
]

# Find Kerala block
m_kerala = re.search(r'###\s+Kerala\s*\n+(.*?)(?=\n---|\Z)', text, re.DOTALL)
if m_kerala:
    ktext = m_kerala.group(1)
    for kd in kerala_districts:
        m_dist = re.search(r'\*\*' + kd + r':\*\*\s*([^\n\r]+)', ktext)
        if m_dist:
            items = re.split(r'[,;]\s*', m_dist.group(1))
            for it in items:
                it_clean = clean_ascii(it).strip()
                it_clean = re.sub(r'^(?:and\s+)?(?:additional\s+|numerous\s+|other\s+).*$', '', it_clean, flags=re.IGNORECASE)
                it_clean = re.sub(r'\s+and\s+(?:additional|numerous|other)\s+.*$', '', it_clean, flags=re.IGNORECASE)
                it_clean = re.sub(r'^\s*-\s*', '', it_clean)
                if it_clean and len(it_clean) > 2 and not it_clean.lower().startswith('and '):
                    # To avoid generic collisions with single-word place names, make meaningful label if short
                    spot_label = it_clean
                    if len(spot_label.split()) == 1 and not spot_label.lower().endswith(('beach', 'falls', 'dam', 'fort', 'temple', 'palace', 'lake', 'cave', 'caves', 'hill', 'hills', 'peak', 'sanctuary', 'island')):
                        # Disambiguate if needed
                        spot_label = f"{it_clean} {kd}"
                    add_spot(spot_label, kd, 'Kerala', 'India')

print(f"New spots after Kerala districts: {len(new_records)}")

# =========================================================================
# STEP 3: Second-level India Expansion for all 27 States
# =========================================================================
print("3. Generating second-level India expansion for 27 States...")

india_second_level = {
    'Rajasthan': [
        ('Gagron Fort Jhalawar', 'Jhalawar', 'Heritage', 'UNESCO Hill Fort surrounded by rivers'),
        ('Jhalrapatan City of Bells', 'Jhalawar', 'Heritage', 'Historic temple town with 100 bells'),
        ('Kolvi Buddhist Caves', 'Jhalawar', 'Cave/Geological', 'Ancient rock-cut Buddhist stupas and caves'),
        ('Garh Palace Jhalawar', 'Jhalawar', 'Heritage', 'Palace with Sheesh Mahal and miniature paintings'),
        ('Shergarh Wildlife Sanctuary', 'Baran', 'Wildlife', 'Sanctuary on Parban River with leopards'),
        ('Shahabad Fort Baran', 'Baran', 'Heritage', '16th-century fortress on high cliff'),
        ('Bhand Devara Sun Temple Ramgarh', 'Baran', 'Temple/Religious', '10th-century mini Khajuraho temple'),
        ('Ramgarh Crater', 'Baran', 'Cave/Geological', 'Meteorite impact crater with ancient temples'),
        ('Nahargarh Biological Park', 'Jaipur', 'Wildlife', 'Ecosystem reserve at base of Aravalli hills'),
        ('Chand Baori Stepwell Abhaneri', 'Dausa', 'Heritage', 'World deepest stepwell with 3500 stone steps'),
        ('Harshat Mata Temple Abhaneri', 'Dausa', 'Temple/Religious', '8th-century temple with ancient carvings'),
        ('Mehandipur Balaji Temple', 'Dausa', 'Temple/Religious', 'Famous spiritual healing temple'),
        ('Khatushyamji Temple', 'Sikar', 'Temple/Religious', 'Sacred pilgrimage temple of Barbarika'),
        ('Jeen Mata Temple Sikar', 'Sikar', 'Temple/Religious', 'Ancient Shakti shrine in Aravalli valley'),
        ('Harshnath Temple Sikar', 'Sikar', 'Heritage', '10th-century Shiva temple atop Mount Harsh'),
        ('Laxmangarh Fort Sikar', 'Sikar', 'Heritage', 'Unique fort built on scattered granite rocks'),
        ('Mandawa Painted Havelis', 'Jhunjhunu', 'Heritage', 'Open-air art gallery with frescoed havelis'),
        ('Nawalgarh Shekhawati Havelis', 'Jhunjhunu', 'Heritage', 'Golden city of Shekhawati with grand mansions'),
        ('Rani Sati Temple Jhunjhunu', 'Jhunjhunu', 'Temple/Religious', 'Centuries-old marble temple complex'),
        ('Khetri Copper Fort', 'Jhunjhunu', 'Heritage', 'Historic hill fort and palace of Raja Ajit Singh'),
        ('Tal Chhapar Blackbuck Sanctuary', 'Churu', 'Wildlife', 'Open grassland sanctuary for endangered blackbucks'),
        ('Salasar Balaji Temple', 'Churu', 'Temple/Religious', 'Revered Hanuman temple with round face idol'),
        ('Karni Mata Temple Deshnoke', 'Bikaner', 'Temple/Religious', 'Famous Rat Temple sheltering thousands of sacred rats'),
        ('Gajner Palace & Wildlife Sanctuary', 'Bikaner', 'Heritage', 'Lakeside hunting resort of Maharajas'),
        ('Laxmi Niwas Palace Bikaner', 'Bikaner', 'Heritage', 'Indo-Saracenic palace in red sandstone'),
        ('Bhangarh Ghost Fort', 'Alwar', 'Heritage', 'Famous 16th-century atmospheric ruined fortress'),
        ('Neemrana Fort Palace', 'Kotputli-Behror', 'Heritage', '15th-century heritage tier palace hotel'),
        ('Tijara Jain Temple', 'Khairthal-Tijara', 'Temple/Religious', 'Prominent Jain pilgrimage tirth'),
        ('Keoladeo National Park Bharatpur', 'Bharatpur', 'Wildlife', 'UNESCO water-bird sanctuary sheltering siberian cranes'),
        ('Deeg Water Palace & Fountains', 'Deeg', 'Heritage', 'Magnificent summer retreat with 2000 fountains'),
        ('Kumbhalgarh Wildlife Sanctuary', 'Rajsamand', 'Wildlife', 'Sanctuary surrounding the Great Wall of India'),
        ('Haldighati Battlefield & Museum', 'Rajsamand', 'Heritage', 'Historic mountain pass of Maharana Pratap'),
        ('Shrinathji Temple Nathdwara', 'Rajsamand', 'Temple/Religious', '7th-century Vaishnavite shrine of Krishna'),
        ('Ranakpur Jain Temple', 'Pali', 'Heritage', 'Marble marvel with 1444 distinct carved pillars'),
        ('Jawaibandh Leopard Safari', 'Pali', 'Wildlife', 'Granite hill country where leopards roam freely'),
        ('Muchhal Mahavir Temple', 'Pali', 'Temple/Religious', 'Ancient Jain temple in Kumbhalgarh forest'),
        ('Menal Waterfall & Ancient Temples', 'Chittorgarh', 'Waterfall', '150-foot gorge waterfall and Shiva shrines'),
        ('Bassi Wildlife Sanctuary', 'Chittorgarh', 'Wildlife', 'Wooded sanctuary with panthers and antelopes'),
        ('Mukundra Hills Tiger Reserve', 'Kota', 'Wildlife', 'Canyon and forest sanctuary on Chambal River'),
        ('Garadia Mahadev Canyon', 'Kota', 'Mountain/Hill', 'Grand Canyon of India on horseshoe Chambal bend'),
        ('Taragarh Fort Bundi', 'Bundi', 'Heritage', 'Massive star-shaped hill fortress'),
        ('Raniji Ki Baoli Bundi', 'Bundi', 'Heritage', 'Ornate 17th-century stepwell with elephant arches'),
        ('Jaisalmer Desert National Park', 'Jaisalmer', 'Wildlife', 'Thar desert habitat of Great Indian Bustard'),
        ('Kuldhara Abandoned Village', 'Jaisalmer', 'Heritage', 'Eerie 13th-century abandoned Paliwal village'),
        ('Tanot Mata Temple Indo-Pak Border', 'Jaisalmer', 'Temple/Religious', 'Miraculous border shrine preserved in 1965 war'),
        ('Longewala War Memorial', 'Jaisalmer', 'Heritage', 'Historic 1971 battle site with captured tanks'),
        ('Machiya Safari Park Jodhpur', 'Jodhpur', 'Wildlife', 'Biological park near Kaylana Lake'),
        ('Toorji Ka Jhalra Stepwell', 'Jodhpur', 'Heritage', '18th-century restored red-sandstone stepwell'),
        ('Mandore Gardens & Royal Cenotaphs', 'Jodhpur', 'Garden/Nature', 'Ancient capital with high rock terraces and shrines'),
        ('Brahma Temple Pushkar', 'Ajmer', 'Temple/Religious', 'One of the very few dedicated Brahma temples in the world'),
        ('Ajmer Sharif Dargah Khwaja Moinuddin', 'Ajmer', 'Temple/Religious', 'Revered Sufi shrine attracting millions'),
        ('Taragarh Fort Ajmer', 'Ajmer', 'Heritage', 'Ancient hill fort built in 8th century by Ajaypal Chauhan')
    ],
    'Uttar Pradesh': [
        ('Dhamek Stupa Sarnath', 'Varanasi', 'Heritage', 'Massive cylindrical Buddhist stupa from 500 CE'),
        ('Chaukhandi Stupa Sarnath', 'Varanasi', 'Heritage', 'Ancient Buddhist monument marking Buddha first disciples'),
        ('Ramnagar Fort & Museum', 'Varanasi', 'Heritage', '18th-century riverside palace of Kashi Naresh'),
        ('Assi Ghat Morning Aarti', 'Varanasi', 'Sightseeing', 'Southernmost ghat famous for morning yoga and music'),
        ('Manikarnika Sacred Cremation Ghat', 'Varanasi', 'Sightseeing', 'Most auspicious burning ghat of Kashi'),
        ('Tulsi Manas Temple', 'Varanasi', 'Temple/Religious', 'Marble temple inscribed with verses of Ramcharitmanas'),
        ('Sankat Mochan Hanuman Temple', 'Varanasi', 'Temple/Religious', 'Famous Hanuman shrine founded by Goswami Tulsidas'),
        ('Itmad-ud-Daulah Baby Taj', 'Agra', 'Heritage', 'Exquisite marble mausoleum precursor to Taj Mahal'),
        ('Mehtab Bagh Moonlit Garden', 'Agra', 'Garden/Nature', 'Charbagh garden complex opposite Taj across Yamuna'),
        ('Akbar Tomb Sikandra', 'Agra', 'Heritage', 'Grand red sandstone and marble tomb of Emperor Akbar'),
        ('Fatehpur Sikri Buland Darwaza', 'Agra', 'Heritage', 'World highest gateway built by Akbar in 1601'),
        ('Tomb of Sheikh Salim Chishti', 'Agra', 'Temple/Religious', 'White marble Sufi saint mausoleum inside Fatehpur Sikri'),
        ('Bara Imambara & Bhulbhulaiya', 'Lucknow', 'Heritage', 'Monumental hall without beams and labyrinth maze'),
        ('Chota Imambara Palace of Lights', 'Lucknow', 'Heritage', 'Ornate monument with Belgian chandeliers and calligraphy'),
        ('Rumi Darwaza Turkish Gate', 'Lucknow', 'Heritage', 'Imposing 60-foot gateway built by Nawab Asaf-ud-Daula'),
        ('British Residency Lucknow', 'Lucknow', 'Heritage', 'Ruins of 1857 siege preserved as national monument'),
        ('Ambedkar Memorial Park Gomti Nagar', 'Lucknow', 'Heritage', 'Grand monument in red sandstone spanning 107 acres'),
        ('Prem Mandir Vrindavan', 'Mathura', 'Temple/Religious', 'Monumental white Italian marble temple with light show'),
        ('Banke Bihari Temple Vrindavan', 'Mathura', 'Temple/Religious', 'Most popular Krishna shrine with swaying curtains'),
        ('ISKCON Krishna Balaram Temple', 'Mathura', 'Temple/Religious', 'International spiritual headquarters in Vrindavan'),
        ('Radha Raman Temple Vrindavan', 'Mathura', 'Temple/Religious', 'Self-manifested Shaligram deity of Lord Krishna'),
        ('Nidhivan Sacred Forest Vrindavan', 'Mathura', 'Garden/Nature', 'Mystical grove where Radha Krishna perform Raslila'),
        ('Govardhan Hill Parikrama', 'Mathura', 'Mountain/Hill', 'Sacred 21-km circumambulation around Govardhan hill'),
        ('Radha Kund & Shyam Kund', 'Mathura', 'Lake/Water', 'Sacred bathing tanks of Radha and Krishna'),
        ('Barsana Shri Radha Rani Temple', 'Mathura', 'Temple/Religious', 'Hilltop palace temple of Radha, home of Lathmar Holi'),
        ('Kanak Bhavan Ayodhya', 'Ayodhya', 'Temple/Religious', 'Golden palace temple gifted to Sita by Kaikeyi'),
        ('Hanuman Garhi Ayodhya', 'Ayodhya', 'Temple/Religious', '10th-century fort-temple guardian of Ayodhya'),
        ('Ram Ki Paidi Saryu River', 'Ayodhya', 'Lake/Water', 'Series of riverside bathing ghats illuminated with lamps'),
        ('Guptar Ghat Ayodhya', 'Ayodhya', 'Sightseeing', 'Sacred Saryu river bank where Lord Rama took Jal Samadhi'),
        ('Triveni Sangam Prayagraj', 'Prayagraj', 'Lake/Water', 'Holy confluence of Ganga, Yamuna and invisible Saraswati'),
        ('Allahabad Fort & Akshayavat', 'Prayagraj', 'Heritage', 'Mighty fort built by Akbar housing sacred indestructible banyan tree'),
        ('Anand Bhavan Nehru Museum', 'Prayagraj', 'Heritage', 'Historic ancestral home of the Nehru-Gandhi family'),
        ('Khusro Bagh Mughal Tombs', 'Prayagraj', 'Heritage', 'Large walled garden housing tombs of Prince Khusro'),
        ('Jhansi Fort Rani Laxmibai', 'Jhansi', 'Heritage', '17th-century hilltop fortress site of 1857 freedom struggle'),
        ('Rani Mahal Jhansi', 'Jhansi', 'Heritage', 'Palace residence of Rani of Jhansi with murals and sculptures'),
        ('Kushinagar Mahaparinirvana Temple', 'Kushinagar', 'Temple/Religious', 'Reclining Buddha statue marking site of Buddha parinirvana'),
        ('Ramabhar Stupa Kushinagar', 'Kushinagar', 'Heritage', 'Cremation mound stupa of Gautama Buddha'),
        ('Sravasti Jetavana Monastery', 'Shravasti', 'Heritage', 'Ancient monastery where Buddha spent 24 rainy seasons'),
        ('Anathapindika Stupa Sravasti', 'Shravasti', 'Heritage', 'Ancient brick stupa of Buddha chief lay disciple'),
        ('Chitrakoot Ramghat on Mandakini', 'Chitrakoot', 'Sightseeing', 'Ghats where Lord Rama stayed during exile with Tulsidas'),
        ('Gupt Godavari Caves Chitrakoot', 'Chitrakoot', 'Cave/Geological', 'Twin natural stream caves with knee-deep water flow'),
        ('Kamadgiri Hill Chitrakoot', 'Chitrakoot', 'Mountain/Hill', 'Sacred forested hill circumambulated by pilgrims'),
        ('Hanuman Dhara Waterfall Chitrakoot', 'Chitrakoot', 'Waterfall', 'Perennial spring cascading over Lord Hanuman idol atop cliff'),
        ('Dudhwa National Park', 'Lakhimpur Kheri', 'Wildlife', 'Terai ecosystem sheltering tigers, rhinos and swamp deer'),
        ('Kishanpur Wildlife Sanctuary', 'Lakhimpur Kheri', 'Wildlife', 'Dense sal forest and wetland sanctuary for barasingha'),
        ('Katarniaghat Wildlife Sanctuary', 'Bahraich', 'Wildlife', 'Girwa river sanctuary for gharials and Gangetic dolphins'),
        ('Hastinapur Wildlife Sanctuary', 'Meerut', 'Wildlife', 'Ganga wetland sanctuary with rich Mahabharata history'),
        ('Chunar Fort Mirzapur', 'Mirzapur', 'Heritage', 'Ancient cliff fort overlooking Ganga with legends of King Vikramaditya'),
        ('Vindhyachal Temple Mirzapur', 'Mirzapur', 'Temple/Religious', 'One of the prominent Shaktipeeths of Goddess Vindhyavasini'),
        ('Lakhaniya Dari Waterfall Mirzapur', 'Mirzapur', 'Waterfall', 'Forest cascade with deep canyon pool and prehistoric rock art')
    ],
    'Uttarakhand': [
        ('Chopta Mini Switzerland', 'Rudraprayag', 'Mountain/Hill', 'Alpine meadow base camp for Tungnath and Chandrashila'),
        ('Tungnath Highest Shiva Temple', 'Rudraprayag', 'Temple/Religious', 'Highest Hindu temple in world dedicated to Lord Shiva at 3680m'),
        ('Chandrashila Summit Peak', 'Rudraprayag', 'Adventure', 'Summit at 4000m offering 360-degree views of Himalayan giants'),
        ('Deoria Tal Emerald Lake', 'Rudraprayag', 'Lake/Water', 'High-altitude lake with reflection of Chaukhamba peaks'),
        ('Madhyamaheshwar Panch Kedar', 'Rudraprayag', 'Temple/Religious', 'Sacred alpine Shiva temple surrounded by snow peaks'),
        ('Vasuki Tal Glacial Lake', 'Rudraprayag', 'Lake/Water', 'Pristine glacial lake at 14200 ft near Kedarnath'),
        ('Triyuginarayan Temple', 'Rudraprayag', 'Temple/Religious', 'Site of divine wedding of Shiva and Parvati with eternal flame'),
        ('Mana First Indian Village', 'Chamoli', 'Heritage', 'Last and first Indian village on Indo-Tibetan border'),
        ('Vasudhara Falls Mana', 'Chamoli', 'Waterfall', 'Spectacular 400-foot glacial cascade near Badrinath'),
        ('Bhim Pul Saraswati River', 'Chamoli', 'Heritage', 'Massive monolithic stone bridge placed by Pandava Bhima'),
        ('Vyas Gufa Cave Mana', 'Chamoli', 'Cave/Geological', 'Ancient cave where Sage Vyasa composed Mahabharata'),
        ('Joshimath Shankaracharya Math', 'Chamoli', 'Temple/Religious', 'Northern monastic seat established by Adi Shankaracharya'),
        ('Auli Skiing Slopes & Ropeway', 'Chamoli', 'Adventure', 'Premier ski resort with longest cable car in Asia'),
        ('Gurso Bugyal Meadow Auli', 'Chamoli', 'Mountain/Hill', 'Sprawling alpine meadow offering views of Nanda Devi'),
        ('Kwani Bugyal Meadow', 'Chamoli', 'Mountain/Hill', 'Alpine meadow camping spot for high-altitude treks'),
        ('Rudranath Panch Kedar Temple', 'Chamoli', 'Temple/Religious', 'Face of Shiva worshipped inside a natural rock cave'),
        ('Kalpeshwar Panch Kedar Temple', 'Chamoli', 'Temple/Religious', 'Only Kedar temple accessible throughout the year'),
        ('Hemkund Sahib Sacred Gurudwara', 'Chamoli', 'Temple/Religious', 'High-altitude Sikh pilgrimage site at 15200 ft by glacial lake'),
        ('Gaumukh Glacier Cow Mouth', 'Uttarkashi', 'Adventure', 'Source of the holy Bhagirathi river emerging from ice cave'),
        ('Tapovan High Altitude Meadow', 'Uttarkashi', 'Adventure', 'Spiritual meadow directly beneath Mount Shivling at 14600 ft'),
        ('Dayara Bugyal Alpine Meadow', 'Uttarkashi', 'Mountain/Hill', 'Expansive 28-sq-km undulating green meadow at 12000 ft'),
        ('Dodital Emerald Trout Lake', 'Uttarkashi', 'Lake/Water', 'Birthplace of Lord Ganesha surrounded by pine and deodar forests'),
        ('Harsil Apple Valley', 'Uttarkashi', 'Mountain/Hill', 'Hidden valley with wooden bridges, apple orchards and deodars'),
        ('Gartang Gali Cliff Walk', 'Uttarkashi', 'Adventure', '150-year-old historic wooden hanging bridge built on sheer cliff'),
        ('Kasar Devi Temple Cranks Ridge', 'Almora', 'Temple/Religious', 'Sacred temple in Van Allen radiation belt visited by Swami Vivekananda'),
        ('Jageshwar Dham 124 Stone Temples', 'Almora', 'Heritage', 'Cluster of 124 9th-century Nagara style temples in deodar forest'),
        ('Katarmal Sun Temple Almora', 'Almora', 'Heritage', 'Rare 9th-century Sun temple with intricate wood carvings'),
        ('Chitai Golu Devta Temple of Bells', 'Almora', 'Temple/Religious', 'Temple of God of Justice hung with thousands of brass bells'),
        ('Binsar Wildlife Sanctuary Zero Point', 'Almora', 'Wildlife', 'Oak forest sanctuary with panoramic Himalayan view of Kedarnath to Nanda Devi'),
        ('Munsiyari Panchachuli Peaks', 'Pithoragarh', 'Mountain/Hill', 'Himalayan hill town facing five sacred snow-capped peaks'),
        ('Birthi Falls Munsiyari', 'Pithoragarh', 'Waterfall', '400-foot cascading waterfall framed by lush green mountains'),
        ('Patal Bhuvaneshwar Underground Cave', 'Pithoragarh', 'Cave/Geological', 'Limestone cave temple with stalactites representing 33 crore deities'),
        ('Askot Musk Deer Sanctuary', 'Pithoragarh', 'Wildlife', 'High-altitude biodiversity reserve on Indo-Nepal border'),
        ('Kausani Anasakti Ashram', 'Bageshwar', 'Heritage', 'Mahatma Gandhi ashram offering sunrise views of Trishul and Nanda Devi'),
        ('Baijnath Temple Complex Bageshwar', 'Bageshwar', 'Heritage', '12th-century stone temples on Gomti river bank'),
        ('Lansdowne Bhulla Lake & Tip N Top', 'Pauri Garhwal', 'Mountain/Hill', 'Quiet British cantonment town with pine forests and lake'),
        ('Tarkeshwar Mahadev Temple Lansdowne', 'Pauri Garhwal', 'Temple/Religious', 'Ancient Shiva temple surrounded by thousands of cedar trees'),
        ('George Everest Peak Mussoorie', 'Dehradun', 'Mountain/Hill', 'Estate and peak of Sir George Everest with 360-degree views'),
        ('Clouds End Heritage Estate', 'Dehradun', 'Heritage', 'Western end of Mussoorie surrounded by dense deodar forests'),
        ('Benog Wildlife Sanctuary Mussoorie', 'Dehradun', 'Wildlife', 'Sanctuary for extinct mountain quail and colorful pheasants'),
        ('Forest Research Institute FRI', 'Dehradun', 'Heritage', 'Colossal Greco-Roman colonial architectural landmark'),
        ('Mindrolling Monastery Clement Town', 'Dehradun', 'Temple/Religious', 'One of the largest Tibetan Buddhist centers in India with 185-ft stupa'),
        ('Robbers Cave Guchhupani', 'Dehradun', 'Cave/Geological', 'Narrow limestone gorge with freezing underground stream'),
        ('Beatles Ashram Chaurasi Kutia', 'Dehradun', 'Heritage', 'Transcendental meditation ashram where The Beatles composed the White Album'),
        ('Kainchi Dham Neem Karoli Baba', 'Nainital', 'Temple/Religious', 'World-famous ashram visited by Steve Jobs and Mark Zuckerberg'),
        ('Mukteshwar Temple & Chauli Ki Jali', 'Nainital', 'Mountain/Hill', '350-year-old Shiva shrine atop cliffs with rock-climbing crags'),
        ('Pangot Bird Watching Village', 'Nainital', 'Wildlife', 'Birding paradise home to over 580 Himalayan avian species'),
        ('Naukuchiatal Nine Cornered Lake', 'Nainital', 'Lake/Water', 'Deepest lake in Nainital region surrounded by oak forests and paragliding')
    ],
    'Himachal Pradesh': [
        ('Old Manali Bohemian Lanes', 'Kullu', 'Sightseeing', 'Charming village lanes with wooden houses, cafes and live music'),
        ('Jogini Waterfalls Vashisht', 'Kullu', 'Waterfall', 'Scenic cascading waterfall reached by apple orchard trek'),
        ('Nicholas Roerich Art Gallery Naggar', 'Kullu', 'Heritage', 'Estate and museum of famous Russian mystic painter'),
        ('Naggar Castle Medieval Timber Wood', 'Kullu', 'Heritage', '15th-century wood and stone castle overlooking Kullu valley'),
        ('Kasol Parvati River Valley', 'Kullu', 'Mountain/Hill', 'Scenic bohemian hub for mountain backpackers and cafes'),
        ('Manikaran Sahib Gurudwara & Hot Springs', 'Kullu', 'Temple/Religious', 'Famous pilgrimage hot springs where food is cooked in boiling water'),
        ('Tosh Village Parvati Valley', 'Kullu', 'Mountain/Hill', 'Picturesque wooden village perched at 7800 ft overlooking peaks'),
        ('Kheerganga Natural Sulphur Springs', 'Kullu', 'Adventure', 'Alpine meadow hot spring bath after 12-km trek'),
        ('Malana Ancient Democracy Village', 'Kullu', 'Heritage', 'Isolated village with unique self-contained democratic system'),
        ('Jibhi Waterfall & Wooden Bridges', 'Kullu', 'Waterfall', 'Enchanting pine forest village with crystal cascades'),
        ('Serolsar Lake Jalori Pass', 'Kullu', 'Lake/Water', 'Sacred lake in dense oak forest associated with Goddess Budhi Nagin'),
        ('Chehni Kothi 1500 Year Old Tower', 'Kullu', 'Heritage', 'Tallest indigenous timber tower fort structure in Western Himalayas'),
        ('Atal Tunnel Rohtang Highway', 'Kullu', 'Sightseeing', 'World longest highway tunnel above 10000 ft linking Manali to Lahaul'),
        ('Chail Palace & World Highest Cricket Ground', 'Solan', 'Heritage', 'Summer retreat of Maharaja of Patiala surrounded by deodars'),
        ('Kalka Shimla Toy Train UNESCO', 'Shimla', 'Heritage', 'Historic 1903 narrow-gauge mountain railway with 102 tunnels'),
        ('Viceregal Lodge Indian Institute of Advanced Study', 'Shimla', 'Heritage', 'Jacobethan style British presidential estate on Observatory Hill'),
        ('Hatu Peak Narkanda', 'Shimla', 'Mountain/Hill', 'Summit at 11150 ft with ancient Hatu Mata temple and apple views'),
        ('Tattapani Hot Sulphur Springs', 'Mandi', 'Sightseeing', 'Natural thermal springs along the banks of Sutlej River'),
        ('Rewalsar Sacred Lotus Lake', 'Mandi', 'Lake/Water', 'Sacred lake revered by Buddhists, Hindus and Sikhs alike'),
        ('Prashar Lake & Three Tiered Pagoda', 'Mandi', 'Lake/Water', 'High-altitude lake with floating island and 14th-century temple'),
        ('Barot Valley Uhl River Trout Fishing', 'Mandi', 'Eco Tourism', 'Hidden valley known for trout fish farms and reservoir funicular'),
        ('Key Monastery Spiti Valley', 'Lahaul and Spiti', 'Temple/Religious', '1000-year-old cliffside Tibetan Buddhist monastery at 13668 ft'),
        ('Chandratal Moon Lake', 'Lahaul and Spiti', 'Lake/Water', 'Crescent-shaped high-altitude lake changing color from turquoise to navy'),
        ('Kibber Highest Inhabited Village', 'Lahaul and Spiti', 'Mountain/Hill', 'Cold desert village at 14200 ft with snow leopard sanctuary'),
        ('Hikkim Highest Post Office in World', 'Lahaul and Spiti', 'Sightseeing', 'Remote post office at 14567 ft where tourists send postcards'),
        ('Komic Highest Motorable Village', 'Lahaul and Spiti', 'Mountain/Hill', 'Highest village connected by motorable road at 15027 ft'),
        ('Langza Giant Buddha Statue', 'Lahaul and Spiti', 'Heritage', '1000-year-old golden Buddha watching over snow mountains and marine fossils'),
        ('Pin Valley National Park', 'Lahaul and Spiti', 'Wildlife', 'Cold desert park sheltering endangered snow leopards and ibex'),
        ('Tabo Monastery UNESCO World Heritage', 'Lahaul and Spiti', 'Heritage', 'Ajanta of the Himalayas founded in 996 CE with ancient murals'),
        ('Dhankar Monastery Cliff Castle', 'Lahaul and Spiti', 'Heritage', 'Dramatic monastery perched precariously on 1000-foot rocky spur'),
        ('Chitkul Last Indian Village', 'Kinnaur', 'Mountain/Hill', 'Last inhabited village on Indo-Tibetan trade border on Baspa river'),
        ('Kalpa Kinner Kailash Sacred Peak View', 'Kinnaur', 'Mountain/Hill', 'Apple growing hamlet facing the 79-foot Shiva Lingam rock pillar'),
        ('Sangla Valley Kamru Fort', 'Kinnaur', 'Heritage', 'Fertile green valley with ancient wooden fort of Baspa rajas'),
        ('Nako Lake & 11th Century Monastery', 'Kinnaur', 'Lake/Water', 'High-altitude lake framed by willows and Tibetan prayer stones'),
        ('Khajjiar Mini Switzerland of India', 'Chamba', 'Garden/Nature', 'Rolling green saucer-shaped meadow surrounded by dense cedar woods'),
        ('Dainkund Peak Singing Hill Dalhousie', 'Chamba', 'Mountain/Hill', 'Highest peak in Dalhousie offering views of Ravi, Beas and Chenab'),
        ('Sach Pass High Mountain Road', 'Chamba', 'Adventure', 'Rugged 14500-foot pass connecting Chamba with Pangi tribal valley'),
        ('Bir Billing Paragliding World Cup Site', 'Kangra', 'Adventure', 'World-renowned takeoff site for paragliding over Kangra valley'),
        ('Masrur Monolithic Rock Cut Temples', 'Kangra', 'Heritage', '8th-century monolithic rock-cut shrines carved out of single sandstone cliff'),
        ('Kangra Fort Ancient Trigarta Empire', 'Kangra', 'Heritage', 'Oldest dated fort in India and largest in Himalayas dating to Mahabharata'),
        ('Triund Ridge Dhauladhar Trek', 'Kangra', 'Adventure', 'Popular mountain ridge overlooking Kangra valley and snow-clad peaks'),
        ('Dalai Lama Namgyal Monastery McLeod Ganj', 'Kangra', 'Temple/Religious', 'Spiritual seat of the 14th Dalai Lama with Tsuglagkhang complex')
    ],
    'Maharashtra': [
        ('Lonar Meteorite Crater Lake', 'Buldhana', 'Cave/Geological', 'Hyper-velocity meteorite impact crater lake in basalt rock'),
        ('Kaas Plateau Valley of Flowers UNESCO', 'Satara', 'Garden/Nature', 'Biodiversity hotspot with carpets of wild blooming orchids'),
        ('Arthur Seat Point Mahabaleshwar', 'Satara', 'Mountain/Hill', 'Queen of all viewpoints overlooking Savitri river canyon'),
        ('Panchgani Table Land Volcanic Plateau', 'Satara', 'Mountain/Hill', 'Asia second longest mountain plateau with sunset horse rides'),
        ('Matheran Toy Train & Charlotte Lake', 'Raigad', 'Mountain/Hill', 'Asia only automobile-free hill station surrounded by red soil paths'),
        ('Karla & Bhaja Rock Cut Caves', 'Pune', 'Cave/Geological', 'Ancient 2nd-century BCE Buddhist rock-cut chaitya halls'),
        ('Raigad Fort Capital of Shivaji Maharaj', 'Raigad', 'Heritage', 'Hill fortress capital perched at 2700 ft with ropeway'),
        ('Sinhagad Fort Pune Battles', 'Pune', 'Heritage', 'Historic Maratha hill fort famous for Tanaji Malusare battle'),
        ('Pratapgad Fort Mahabaleshwar', 'Satara', 'Heritage', 'High mountain fort site of historic battle with Afzal Khan'),
        ('Murud Janjira Unconquered Sea Fort', 'Raigad', 'Heritage', 'Impregnable island sea fortress with 19 bastions and deep cannons'),
        ('Sindhudurg Sea Fort Malvan', 'Sindhudurg', 'Heritage', 'Fortress built by Shivaji Maharaj amidst Arabian sea waves'),
        ('Tarkarli Coral Beach & Scuba Haven', 'Sindhudurg', 'Beach', 'Crystal-clear waters famous for coral scuba diving and dolphins'),
        ('Alibaug Kolaba Fort in Sea', 'Raigad', 'Heritage', 'Coastal fort accessible by foot during low tide across sands'),
        ('Tadoba Andhari Tiger Reserve', 'Chandrapur', 'Wildlife', 'Oldest and largest tiger reserve in Maharashtra with teak forests'),
        ('Chikhaldara Hill Station Melghat', 'Amravati', 'Mountain/Hill', 'Coffee-growing hill station in Vidarbha near tiger reserve'),
        ('Trimbakeshwar Jyotirlinga Temple', 'Nashik', 'Temple/Religious', 'Sacred Jyotirlinga shrine origin source of holy Godavari river'),
        ('Grishneshwar Jyotirlinga Temple', 'Chhatrapati Sambhajinagar', 'Temple/Religious', '12th Jyotirlinga temple built in red rock by Ahilyabai Holkar'),
        ('Bhimashankar Jyotirlinga & Giant Squirrel', 'Pune', 'Temple/Religious', 'Ancient Jyotirlinga temple in dense Western Ghats sanctuary'),
        ('Harishchandragad Konkan Kada Cliff', 'Ahmednagar', 'Adventure', 'Colossal concave cliff face with circular rainbows and Kedareshwar cave'),
        ('Bhandardara Arthur Lake & Wilson Dam', 'Ahmednagar', 'Lake/Water', 'Tranquil reservoir village beneath Mount Kalsubai highest peak')
    ],
    'Karnataka': [
        ('Hampi Virupaksha Temple & Stone Chariot', 'Vijayanagara', 'Heritage', 'UNESCO ruins of medieval Vijayanagara Empire on Tungabhadra'),
        ('Badami Cave Temples Sandstone Cliffs', 'Bagalkot', 'Heritage', '6th-century Chalukyan rock-cut shrines overlooking Agastya lake'),
        ('Pattadakal UNESCO Group of Monuments', 'Bagalkot', 'Heritage', 'Harmonious blend of northern and southern temple architectures'),
        ('Aihole Cradle of Indian Architecture', 'Bagalkot', 'Heritage', 'Over 120 stone temples experimenting with early Hindu temple styles'),
        ('Gokarna Om Beach & Kudle Beach', 'Uttara Kannada', 'Beach', 'Sacred coastal town with Om-shaped beaches and bohemian shacks'),
        ('Murudeshwar Giant Shiva Statue & Beach', 'Uttara Kannada', 'Temple/Religious', 'World second tallest Shiva statue rising 123 ft above sea'),
        ('Jog Falls Sharavathi River Cascades', 'Shivamogga', 'Waterfall', 'Second-highest plunge waterfall in India dropping 830 feet'),
        ('Abbey Falls & Raja Seat Coorg', 'Kodagu', 'Waterfall', 'Coffee estate waterfall and seasonal sunset viewing pavilion'),
        ('Mullayanagiri Highest Peak Chikmagalur', 'Chikkamagaluru', 'Mountain/Hill', 'Highest summit in Karnataka at 6330 ft offering cloud walks'),
        ('Baba Budangiri Sacred Dattatreya Peetha', 'Chikkamagaluru', 'Mountain/Hill', 'Spiritual mountain range where coffee was first cultivated in India'),
        ('Kudremukh National Park & Horse Face Peak', 'Chikkamagaluru', 'Wildlife', 'Rolling shola grassland mountains sheltering lion-tailed macaques'),
        ('Bandipur Tiger Reserve & National Park', 'Chamarajanagar', 'Wildlife', 'Premier Project Tiger reserve along Mysuru-Ooty highway'),
        ('Nagarhole National Park Kabini River Safari', 'Mysuru', 'Wildlife', 'Famous wildlife sanctuary for leopards, black panthers and elephants'),
        ('Dandeli Kali River White Water Rafting', 'Uttara Kannada', 'Adventure', 'Dense hornbill forest sanctuary with class-3 river rapids'),
        ('Belur Chennakeshava Hoysala Temple', 'Hassan', 'Heritage', '12th-century star-shaped soapstone temple with intricate sculptures'),
        ('Halebidu Hoysaleswara Twin Temples', 'Hassan', 'Heritage', 'Masterpiece of Hoysala architecture with friezes of Mahabharata'),
        ('Shravanabelagola Gommateshwara Statue', 'Hassan', 'Heritage', '57-foot monolithic granite statue of Bahubali carved in 981 CE'),
        ('Agumbe Sunset Point & King Cobra Rainforest', 'Shivamogga', 'Garden/Nature', 'Cherrapunji of South India renowned for waterfalls and herpetology'),
        ('St. Mary Island Basaltic Rock Columns Malpe', 'Udupi', 'Island', 'Sub-aerial volcanic columnar basalt hexagonal formations in sea')
    ],
    'Tamil Nadu': [
        ('Meenakshi Amman Temple 14 Gopurams', 'Madurai', 'Temple/Religious', 'Monumental historic Dravidian temple with 33000 sculptures'),
        ('Brihadisvara Temple Big Temple Thanjavur', 'Thanjavur', 'Heritage', 'Great Living Chola Temple with 80-tonne monolithic cupola dome'),
        ('Gangaikonda Cholapuram Chola Capital', 'Ariyalur', 'Heritage', 'Monumental temple built by Rajendra Chola celebrating Ganges conquest'),
        ('Shore Temple & Pancha Rathas Mahabalipuram', 'Chengalpattu', 'Heritage', '7th-century Pallava monolithic rock relief overlooking Bay of Bengal'),
        ('Nilgiri Mountain Railway Toy Train UNESCO', 'Nilgiris', 'Heritage', 'Historic rack-and-pinion steam railway climbing through mist'),
        ('Doddabetta Peak & Ooty Botanical Gardens', 'Nilgiris', 'Mountain/Hill', 'Highest vantage peak in Nilgiris at 8650 ft with Italian gardens'),
        ('Kodaikanal Pillar Rocks & Kodai Lake', 'Dindigul', 'Mountain/Hill', 'Three giant 400-foot vertical granite pillars and star-shaped lake'),
        ('Dhanushkodi Ghost Town & Rama Setu Point', 'Ramanathapuram', 'Beach', 'Atmospheric ruined coastal town destroyed in 1964 cyclone'),
        ('Ramanathaswamy Temple 1000 Pillar Corridor', 'Ramanathapuram', 'Temple/Religious', 'Longest temple corridor in India with 22 holy teerthams'),
        ('Vivekananda Rock Memorial & Thiruvalluvar', 'Kanyakumari', 'Heritage', 'Sacred rock island memorial at confluence of three oceans'),
        ('Padmanabhapuram Wooden Palace', 'Kanyakumari', 'Heritage', '16th-century Travancore wooden architecture masterwork'),
        ('Chettinad Heritage Mansions Kanadukathan', 'Sivaganga', 'Heritage', 'Opulent palatial merchant homes with Burma teak and Italian tiles'),
        ('Pichavaram Mangrove Forest Boating', 'Cuddalore', 'Eco Tourism', 'Second largest mangrove forest in world with 400 water channels'),
        ('Hogenakkal Falls Niagara of India', 'Dharmapuri', 'Waterfall', 'Carbonatite rock waterfall on Kaveri with circular coracle rides'),
        ('Yercaud Emerald Lake & Shevaroy Hills', 'Salem', 'Mountain/Hill', 'Jewel of the South hill station with orange groves and coffee estates'),
        ('Valparai Tea Plantations & Anamalai Reserve', 'Coimbatore', 'Mountain/Hill', 'Untouched high-altitude plateau with 40 hairpin bends and leopards')
    ],
    'Gujarat': [
        ('Statue of Unity Kevadia Sardar Sarovar', 'Narmada', 'Heritage', 'World tallest monument standing 182 meters on Narmada River'),
        ('Great Rann of Kutch White Salt Desert', 'Kutch', 'Sightseeing', 'Vast white salt marsh shining under full moon with Rann Utsav'),
        ('Somnath Temple First of Twelve Jyotirlingas', 'Gir Somnath', 'Temple/Religious', 'Sacred eternal shrine on the shore of Arabian Sea'),
        ('Dwarkadhish Temple Jagat Mandir', 'Devbhumi Dwarka', 'Temple/Religious', 'Ancient Char Dham coastal temple of Lord Krishna'),
        ('Gir National Park Asiatic Lions Sanctuary', 'Junagadh', 'Wildlife', 'Only natural wilderness habitat of Asiatic lions on Earth'),
        ('Rani ki Vav Patan UNESCO Stepwell', 'Patan', 'Heritage', 'Subterranean 7-level stepwell with 500 major sculptures'),
        ('Sun Temple Modhera Stepwell & Sabha Mandap', 'Mehsana', 'Heritage', 'Solanki architecture sun temple aligned with equinox sunbeams'),
        ('Lothal Ancient Harappan Tidal Dockyard', 'Ahmedabad', 'Heritage', '4500-year-old Indus Valley port city and archaeological ruins'),
        ('Champaner Pavagadh Archaeological Park', 'Panchmahal', 'Heritage', 'UNESCO historic city blending Hindu-Muslim pre-Mughal architecture'),
        ('Palitana Shatrunjaya Hill 863 Jain Temples', 'Bhavnagar', 'Temple/Religious', 'World largest sacred temple complex clustered on marble mountain'),
        ('Saputara Hill Station & Sunset Point', 'Dang', 'Mountain/Hill', 'Picturesque hill retreat in Western Ghats with tribal culture'),
        ('Dholavira UNESCO Harappan Metropolis', 'Kutch', 'Heritage', 'Ancient water reservoirs and stone architecture of Indus civilization'),
        ('Polo Ancient Forest & Temple Ruins', 'Sabarkantha', 'Heritage', '15th-century forgotten Jain and Hindu shrines in lush forest')
    ],
    'Madhya Pradesh': [
        ('Khajuraho Western Group of Temples UNESCO', 'Chhatarpur', 'Heritage', 'Magnificent Chandela temples renowned for nagara architectural finesse'),
        ('Sanchi Great Stupa Ashoka Buddhist Complex', 'Raisen', 'Heritage', 'Oldest stone structure in India commissioned by Emperor Ashoka'),
        ('Gwalior Fort & Man Mandir Palace', 'Gwalior', 'Heritage', 'Pearl amongst fortresses of India atop sandstone precipice'),
        ('Orchha Jahangir Mahal & Ram Raja Temple', 'Niwari', 'Heritage', 'Palace fortress town on Betwa river where Rama is revered as King'),
        ('Bhedaghat Marble Rocks & Dhuandhar Falls', 'Jabalpur', 'Lake/Water', '100-foot white marble gorge on Narmada with smoke cascade falls'),
        ('Bhimbetka Prehistoric Rock Shelters', 'Raisen', 'Heritage', 'UNESCO cave shelters with 30000-year-old Paleolithic rock paintings'),
        ('Kanha Tiger Reserve Sal Forests & Meadow', 'Mandla', 'Wildlife', 'Inspiration for Kipling Jungle Book with hard-ground barasingha'),
        ('Bandhavgarh Tiger Reserve Tala Zone', 'Umaria', 'Wildlife', 'Highest density of Bengal tigers in India around ancient fort ruins'),
        ('Pench Tiger Reserve Mowgli Sanctuary', 'Seoni', 'Wildlife', 'Rich teak forest sanctuary straddling Madhya Pradesh and Maharashtra'),
        ('Panna National Park Ken River Canyon', 'Panna', 'Wildlife', 'Tiger haven with deep gorges, vultures and Pandav waterfalls'),
        ('Mandu Jahaz Mahal Floating Palace', 'Dhar', 'Heritage', 'City of Joy with medieval Afghan palace shaped like a floating ship'),
        ('Ujjain Mahakaleshwar Jyotirlinga & Bhasma Aarti', 'Ujjain', 'Temple/Religious', 'Only south-facing Jyotirlinga famous for sacred dawn ash ritual'),
        ('Omkareshwar Jyotirlinga Narmada Island', 'Khandwa', 'Temple/Religious', 'Sacred island temple shaped naturally in the sacred symbol Om'),
        ('Pachmarhi Queen of Satpuras & Bee Falls', 'Narmadapuram', 'Mountain/Hill', 'Hill station with pine forests, waterfalls and natural cave pools')
    ],
    'Odisha': [
        ('Konark Sun Temple Black Pagoda Chariot', 'Puri', 'Heritage', 'UNESCO 13th-century chariot temple with 24 intricately carved wheels'),
        ('Jagannath Temple Puri Grand Bada Danda', 'Puri', 'Temple/Religious', 'Ancient Char Dham shrine famous for annual Ratha Yatra chariot procession'),
        ('Chilika Lake Kalijai Island & Irrawaddy Dolphins', 'Puri', 'Lake/Water', 'Asia largest brackish water lagoon wintering millions of migratory birds'),
        ('Lingaraj Temple 11th Century Kalinga Marvel', 'Khordha', 'Temple/Religious', 'Towering 180-foot stone sanctum dedicated to Harihara in Bhubaneswar'),
        ('Udayagiri & Khandagiri Rock Cut Caves', 'Khordha', 'Cave/Geological', 'Ancient Jain rock-cut hermit cells with Hathigumpha inscription'),
        ('Dhauli Shanti Stupa Ashokan Edicts', 'Khordha', 'Heritage', 'White peace pagoda marking the historic site of Kalinga War'),
        ('Simlipal Tiger Reserve & Barehipani Falls', 'Mayurbhanj', 'Wildlife', 'Vast biosphere reserve with 1300-foot tiered Barehipani waterfall'),
        ('Bhitarkanika National Park Saltwater Crocodiles', 'Kendrapara', 'Wildlife', 'Mangrove wetland sanctuary harboring giant saltwater crocodiles'),
        ('Daringbadi Kashmir of Odisha Pine Hills', 'Kandhamal', 'Mountain/Hill', 'Cool plateau hill town with coffee plantations and pine forests'),
        ('Chandipur Beach Receding Sea Phenomenon', 'Balasore', 'Beach', 'Unique beach where the sea recedes up to 5 kilometers during low tide')
    ],
    'West Bengal': [
        ('Tiger Hill Sunrise & Mount Kanchenjunga', 'Darjeeling', 'Mountain/Hill', 'Famous vantage point offering panoramic sunrise over Everest and Kanchenjunga'),
        ('Darjeeling Himalayan Toy Train UNESCO', 'Darjeeling', 'Heritage', 'Historic 1881 narrow-gauge zigzag steam train climbing 7000 feet'),
        ('Batasia Loop Gorkha War Memorial', 'Darjeeling', 'Heritage', 'Spiral railway loop with panoramic garden view of snow peaks'),
        ('Mirik Sumendu Lake & Pine Forest Walk', 'Darjeeling', 'Lake/Water', 'Tranquil hill resort featuring arch footbridge over natural lake'),
        ('Kalimpong Deolo Hill & Durpin Monastery', 'Kalimpong', 'Mountain/Hill', 'Highest hill peak in Kalimpong with panoramic Teesta river views'),
        ('Sandakphu Highest Peak of West Bengal', 'Darjeeling', 'Adventure', '11930-foot summit offering views of the Sleeping Buddha mountain massif'),
        ('Sundarbans Royal Bengal Tiger Mangrove Safari', 'South 24 Parganas', 'Wildlife', 'World largest halophytic mangrove forest and tiger delta reserve'),
        ('Jaldapara National Park One Horned Rhinos', 'Alipurduar', 'Wildlife', 'Elephant-grass sanctuary on Torsa river sheltering Indian rhinos'),
        ('Shantiniketan Visva Bharati University', 'Birbhum', 'Heritage', 'UNESCO open-air university town founded by Nobel laureate Rabindranath Tagore'),
        ('Bishnupur Terracotta Temples Rasmancha', 'Bankura', 'Heritage', '17th-century terracotta temples built from local alluvial burnt clay')
    ],
    'Assam': [
        ('Kaziranga National Park Rhino Safari Kohora', 'Golaghat', 'Wildlife', 'UNESCO home to two-thirds of the world great one-horned rhinoceroses'),
        ('Manas National Park Tiger Reserve Safari', 'Baksa', 'Wildlife', 'Pristine Himalayan foothills sanctuary on the border of Bhutan'),
        ('Majuli Island World Largest River Island', 'Majuli', 'Island', 'Vibrant cultural river island on Brahmaputra with Neo-Vaishnavite sattras'),
        ('Kamakhya Temple Nilachal Hill Shaktipeeth', 'Kamrup Metropolitan', 'Temple/Religious', 'Ancient tantric shrine celebrated for the annual Ambubachi Mela'),
        ('Umananda Island Smallest Inhabited River Island', 'Kamrup Metropolitan', 'Island', 'Peacock Island on Brahmaputra housing 17th-century Shiva temple'),
        ('Sivasagar Rang Ghar & Talatal Ghar', 'Sivasagar', 'Heritage', 'Two-storied royal amphitheater and palace of the historic Ahom dynasty'),
        ('Pobitora Wildlife Sanctuary Dense Rhino Haven', 'Morigaon', 'Wildlife', 'Sanctuary with the highest ecological density of one-horned rhinos in India'),
        ('Haflong Lake & Only Hill Station in Assam', 'Dima Hasao', 'Mountain/Hill', 'Scenic hill town with suspension footbridge, mist and orange groves')
    ],
    'Meghalaya': [
        ('Nohkalikai Falls Cherrapunji Plunge', 'East Khasi Hills', 'Waterfall', 'Tallest plunge waterfall in India dropping 1115 ft into turquoise pool'),
        ('Nongriat Double Decker Living Root Bridge', 'East Khasi Hills', 'Heritage', 'Bio-engineered Ficus elastica living root bridge created by Khasi tribe'),
        ('Dawki Umngot River Crystal Clear Boating', 'West Jaintia Hills', 'Lake/Water', 'Transparent emerald river where boats appear to float on thin air'),
        ('Mawlynnong Cleanest Village in Asia', 'East Khasi Hills', 'Eco Tourism', 'Immaculate flower-lined tribal village with treehouse skywalks'),
        ('Krang Suri Waterfalls Amlarem', 'West Jaintia Hills', 'Waterfall', 'Fairytale blue-lagoon waterfall surrounded by sandstone caves'),
        ('Wei Sawdong Three Tiered Waterfall', 'East Khasi Hills', 'Waterfall', 'Dramatic stepped waterfall hidden in dense subtropical jungle'),
        ('Laitlum Canyons Edge of the World', 'East Khasi Hills', 'Mountain/Hill', 'Vast emerald canyons dropping sheer thousands of feet into valleys'),
        ('Umiam Lake Barapani Water Sports', 'Ri Bhoi', 'Lake/Water', 'Expansive reservoir lake framed by pine-covered hills')
    ],
    'Sikkim': [
        ('Gurudongmar Sacred High Altitude Lake', 'North Sikkim', 'Lake/Water', 'Holy lake at 17800 ft blessed by Guru Padmasambhava with crystal water'),
        ('Yumthang Valley of Rhododendron Flowers', 'North Sikkim', 'Garden/Nature', 'River valley blanketed in 24 species of wild blooming rhododendrons'),
        ('Zero Point Yumesamdong Snow Plateau', 'North Sikkim', 'Mountain/Hill', 'Last outpost of civilization at 15300 ft where road terminates in snow'),
        ('Nathu La Pass Indo China Border Trade Post', 'East Sikkim', 'Mountain/Hill', 'Historic Silk Route mountain pass at 14140 ft on China border'),
        ('Tsomgo Sacred Glacial Changu Lake', 'East Sikkim', 'Lake/Water', 'High-altitude lake at 12310 ft with yak rides and reflection of peaks'),
        ('Ravangla Buddha Park Tathagata Tsal', 'South Sikkim', 'Heritage', '130-foot copper statue of Gautama Buddha consecrated by Dalai Lama'),
        ('Pelling Skywalk & Chenrezig Colossus', 'West Sikkim', 'Heritage', 'First glass skywalk in India facing 137-foot statue of Avalokiteshvara')
    ],
    'Arunachal Pradesh': [
        ('Tawang Monastery Largest in India', 'Tawang', 'Temple/Religious', '400-year-old fortress monastery of Gelug school founded by Merak Lama'),
        ('Sela Pass & Sela Frozen Lake at 13700 ft', 'Tawang', 'Mountain/Hill', 'High-altitude mountain pass with twin sacred alpine lakes'),
        ('Madhuri Lake Sangetsar Tso', 'Tawang', 'Lake/Water', 'Glacial lake formed by earthquake with dead tree trunks emerging from water'),
        ('Nuranang Jang Falls 100-Meter Cascade', 'Tawang', 'Waterfall', 'Spectacular thunderous waterfall dropping into the Tawang River'),
        ('Ziro Valley Apatani Paddy Fish Cultivation', 'Lower Subansiri', 'Eco Tourism', 'Picturesque UNESCO landscape of gentle pine-clad hills and tribal culture'),
        ('Namdapha National Park Rainforest Biosphere', 'Changlang', 'Wildlife', 'Biodiversity hotspot sheltering tigers, leopards, snow leopards and cloudeds')
    ],
    'Nagaland': [
        ('Kisama Heritage Village Hornbill Festival', 'Kohima', 'Heritage', 'Cultural village showcasing authentic tribal morungs and festival dances'),
        ('Dzukou Valley Lily Carpet Trek', 'Kohima', 'Adventure', 'Enchanting undulating high valley famous for endemic Dzukou lilies'),
        ('Khonoma First Green Village of India', 'Kohima', 'Eco Tourism', 'Angami Naga village renowned for forest conservation and terraced paddies'),
        ('Longwa Village Indo-Myanmar Border Chieftain', 'Mon', 'Heritage', 'Konyak Naga village where chief house spans both India and Myanmar borders')
    ],
    'Manipur': [
        ('Loktak Lake Phumdis & Floating Islands', 'Bishnupur', 'Lake/Water', 'Largest freshwater lake in Northeast India with circular floating vegetation'),
        ('Keibul Lamjao Only Floating National Park', 'Bishnupur', 'Wildlife', 'World only floating national park last natural home of Sangai brow-antlered deer'),
        ('Kangla Fort Ancient Meitei Royal Citadel', 'Imphal West', 'Heritage', 'Ancient royal palace seat of the Kingdom of Manipur on Imphal river'),
        ('Ima Keithel Mothers Market Imphal', 'Imphal West', 'Sightseeing', '500-year-old bustling market operated entirely by over 5000 women merchants')
    ],
    'Mizoram': [
        ('Reiek Heritage Tlang Peak & Khasi Village', 'Mamit', 'Mountain/Hill', 'Mountain peak at 5000 ft with panoramic views over Bangladesh plains'),
        ('Vantawng Falls Highest Waterfall in Mizoram', 'Serchhip', 'Waterfall', '750-foot two-tiered cascade plunging amidst dense bamboo forests'),
        ('Phawngpui Blue Mountain Peak', 'Lawngtlai', 'Mountain/Hill', 'Highest peak in Mizoram at 7100 ft sacred to tribal spirits with dwarf orchids'),
        ('Tamdil Natural Serene Lake', 'Saitual', 'Lake/Water', 'Tranquil natural lake surrounded by evergreen forests and holiday cottages')
    ],
    'Tripura': [
        ('Ujjayanta Palace White Marble Museum', 'West Tripura', 'Heritage', 'Neoclassical palace of Tripura Maharajas set amidst Mughal gardens'),
        ('Neermahal Water Palace Rudrasagar Lake', 'Sipahijala', 'Heritage', 'Largest water palace in India blending Hindu and Mughal architecture in lake'),
        ('Unakoti Colossal Rock Cut Shiva Carvings', 'Unakoti', 'Heritage', 'Ancient Shaivite pilgrimage site with 30-foot head of Shiva carved in rock'),
        ('Tripura Sundari Temple Matabari Udaipur', 'Gomati', 'Temple/Religious', '500-year-old sacred Shaktipeeth temple shaped like a tortoise hill')
    ],
    'Jharkhand': [
        ('Hundru Falls Subarnarekha River Plunge', 'Ranchi', 'Waterfall', '320-foot waterfall dropping over metamorphic rocks into scenic pool'),
        ('Dassam Falls Kanchi River Cascade', 'Ranchi', 'Waterfall', 'Spectacular cascade where Kanchi river plunges 144 feet over craggy ledge'),
        ('Betla National Park Palamau Tiger Reserve', 'Latehar', 'Wildlife', 'Pioneering Project Tiger reserve with elephant herds and 16th-century forts'),
        ('Netarhat Queen of Chotanagpur Magnolia Sunset', 'Latehar', 'Mountain/Hill', 'Scenic hill plateau famous for sunset views, pine forests and sunrise point'),
        ('Parasnath Shikharji Sacred Jain Mountain', 'Giridih', 'Temple/Religious', 'Highest peak in Jharkhand where 20 of 24 Jain Tirthankaras attained moksha'),
        ('Baidyanath Dham Jyotirlinga Deoghar', 'Deoghar', 'Temple/Religious', 'Revered Kamna Linga temple attracting millions during Shravan Kanwar Yatra'),
        ('Patratu Valley Scenic Ghat Road & Dam', 'Ramgarh', 'Mountain/Hill', 'Winding hairpin curves through green hills overlooking reservoir lake')
    ],
    'Chhattisgarh': [
        ('Chitrakote Falls Niagara of India Horseshoe', 'Bastar', 'Waterfall', 'Broadest waterfall in India spanning 980 feet across Indravati river'),
        ('Tirathgarh Cascading Falls Kanger Valley', 'Bastar', 'Waterfall', '300-foot stepped waterfall tumbling down jagged limestone cliffs'),
        ('Kutumsar Underground Stalactite Caves', 'Bastar', 'Cave/Geological', 'Deep pitch-black limestone cave system with subterranean blind fish'),
        ('Kanger Valley National Park Moist Deciduous', 'Bastar', 'Wildlife', 'Biodiversity-rich valley park sheltering the Bastar hill myna'),
        ('Sirpur Buddhist Brick Monasteries & Lakshman Temple', 'Mahasamund', 'Heritage', 'Ancient archaeological capital with 7th-century ornate red brick temple'),
        ('Mainpat Little Tibet of Chhattisgarh', 'Surguja', 'Mountain/Hill', 'High plateau with Tibetan refugee settlements, potato farms and bouncy soil'),
        ('Bhoramdeo Temple Khajuraho of Chhattisgarh', 'Kabirdham', 'Heritage', '11th-century Nagara temple nestled in Maikal mountain ranges')
    ],
    'Bihar': [
        ('Mahabodhi Temple Complex Bodh Gaya UNESCO', 'Gaya', 'Heritage', 'Sacred spot where Siddhartha Gautama attained enlightenment beneath Bodhi Tree'),
        ('Great Buddha 80-Foot Statue Bodh Gaya', 'Gaya', 'Heritage', 'Monumental seated stone Buddha statue unveiled by 14th Dalai Lama'),
        ('Nalanda Mahavihara Ancient University UNESCO', 'Nalanda', 'Heritage', 'Ruins of 5th-century residential university that taught 10000 scholars'),
        ('Vishwa Shanti Stupa World Peace Pagoda Rajgir', 'Nalanda', 'Heritage', 'Colossal white stupa atop Ratnagiri hill accessible by scenic chairlift'),
        ('Griddhakuta Vulture Peak Rajgir', 'Nalanda', 'Heritage', 'Sacred mountain hermitage where Lord Buddha preached the Lotus Sutra'),
        ('Barabar Caves Oldest Rock Cut Caves in India', 'Jehanabad', 'Cave/Geological', 'Maurya Empire 3rd-century BCE granite caves with high mirror polish'),
        ('Valmiki National Park & Tiger Reserve', 'West Champaran', 'Wildlife', 'Only national park in Bihar located in Terai forest along Gandak river'),
        ('Kesariya Stupa World Tallest Buddhist Stupa', 'East Champaran', 'Heritage', 'Ancient 104-foot circular brick stupa larger than Borobudur')
    ],
    'Punjab': [
        ('Golden Temple Harmandir Sahib Amritsar', 'Amritsar', 'Temple/Religious', 'Spiritual center of Sikhism surrounded by the holy Amrit Sarovar lake'),
        ('Wagah Border Beating Retreat Ceremony', 'Amritsar', 'Sightseeing', 'Electrifying daily military parade and flag-lowering at Indo-Pak border'),
        ('Jallianwala Bagh Historic Memorial Park', 'Amritsar', 'Heritage', 'National memorial preserving the bullet marks of the 1919 massacre'),
        ('Gobindgarh Fort Military Heritage Complex', 'Amritsar', 'Heritage', '18th-century royal brick fortress of Maharaja Ranjit Singh'),
        ('Virasat-e-Khalsa Museum Anandpur Sahib', 'Rupnagar', 'Heritage', 'Monumental architecture celebrating 500 years of Sikh history and culture'),
        ('Qila Mubarak Bathinda Ancient Brick Fort', 'Bathinda', 'Heritage', '1400-year-old fort where Razia Sultana, first woman ruler of Delhi, was held')
    ],
    'Haryana': [
        ('Brahma Sarovar Sacred Water Tank Kurukshetra', 'Kurukshetra', 'Lake/Water', 'Vast sacred water reservoir associated with Lord Brahma and solar eclipses'),
        ('Jyotisar Birthplace of Bhagavad Gita', 'Kurukshetra', 'Heritage', 'Sacred banyan tree where Lord Krishna delivered Gita sermon to Arjuna'),
        ('Sultanpur National Park Bird Sanctuary', 'Gurugram', 'Wildlife', 'Wetland haven wintering over 250 species of resident and migratory birds'),
        ('Yadavindra Gardens Pinjore Mughal Terraces', 'Panchkula', 'Garden/Nature', '17th-century seven-tiered Mughal terraced pleasure gardens with fountains'),
        ('Morni Hills & Tikkar Taal Lake', 'Panchkula', 'Mountain/Hill', 'Only hill station in Haryana with pine forests and interconnected lakes'),
        ('Rakhigarhi Indus Valley Archaeological Site', 'Hisar', 'Heritage', 'Largest settlement of the ancient Harappan civilization spanning 350 hectares')
    ],
    'Andhra Pradesh': [
        ('Tirumala Venkateswara Temple Seven Hills', 'Tirupati', 'Temple/Religious', 'World most visited pilgrimage shrine perched atop sacred Venkatadri hill'),
        ('Sri Kalahasteeswara Temple Vayu Lingam', 'Tirupati', 'Temple/Religious', 'Ancient Pancha Bhoota shrine where Lord Shiva is worshipped as Wind'),
        ('Lepakshi Veerabhadra Hanging Pillar Temple', 'Sri Sathya Sai', 'Heritage', '16th-century Vijayanagara temple famous for miraculous hanging pillar and Nandi'),
        ('Gandikota Grand Canyon of India Pennar River', 'YSR Kadapa', 'Mountain/Hill', 'Dramatic gorge of red granite cliffs flanking historic 13th-century fort'),
        ('Belum Caves Longest Underground Caverns', 'Nandyal', 'Cave/Geological', 'Second largest cave system in Indian subcontinent with stalactite formations'),
        ('Borra Caves Stalactite Caverns Araku', 'Alluri Sitharama Raju', 'Cave/Geological', 'Deep 80-meter million-year-old limestone karst caves with natural lingam'),
        ('Katiki Waterfalls Ghostalani River Araku', 'Alluri Sitharama Raju', 'Waterfall', '50-foot natural mountain cascade deep in eastern ghats bamboo forests'),
        ('Rishikonda Beach Water Sports Visakhapatnam', 'Visakhapatnam', 'Beach', 'Golden sand crescent beach famous for sea kayaking and speed boating'),
        ('Submarine Museum INS Kursura Vizag Beach', 'Visakhapatnam', 'Heritage', 'Decommissioned Soviet-built submarine preserved on beach for public walk-in'),
        ('Amaravati Dhyana Buddha & Ancient Mahachaitya', 'Guntur', 'Heritage', '125-foot giant Buddha statue and 2000-year-old Buddhist stupa heritage site'),
        ('Srisailam Mallikarjuna Swamy Jyotirlinga', 'Nandyal', 'Temple/Religious', 'Ancient temple on Nallamala hills revered as both Jyotirlinga and Shaktipeeth')
    ],
    'Telangana': [
        ('Golconda Fort & Acoustic Echo Clapping Portico', 'Hyderabad', 'Heritage', 'Medieval fortress of Qutb Shahi kings where Koh-i-Noor diamond was stored'),
        ('Charminar & Laad Bazaar Pearl Market', 'Hyderabad', 'Heritage', '1591 iconic four-minaret monument and historic lacquer bangle market'),
        ('Ramappa Temple UNESCO Kakatiya Sandbox Architecture', 'Mulugu', 'Heritage', '13th-century temple built with floating bricks and earthquake-resistant sandboxes'),
        ('Thousand Pillar Temple Hanamkonda', 'Hanamkonda', 'Heritage', 'Kakatiya star-shaped temple dedicated to Shiva, Vishnu and Surya with carved Nandi'),
        ('Nagarjuna Sagar Dam & Island Museum', 'Nalgonda', 'Lake/Water', 'World largest masonry dam with Nagarjunakonda Buddhist archaeological island'),
        ('Kuntala Falls Highest Waterfall in Telangana', 'Adilabad', 'Waterfall', '150-foot cascading waterfall tumbling down rock precipice in Kadam river'),
        ('Laknavaram Lake 160-Meter Hanging Ropeway Bridge', 'Mulugu', 'Lake/Water', 'Sprawling lake with 13 lush green islands connected by suspension bridges'),
        ('Ananthagiri Hills Coffee Woods & Musi Source', 'Vikarabad', 'Mountain/Hill', 'Lush forested hill retreat source of Musi river with ancient Anantha temple')
    ],
    'Goa': [
        ('Basilica of Bom Jesus UNESCO Old Goa', 'North Goa', 'Heritage', '16th-century baroque basilica enshrining sacred relics of St. Francis Xavier'),
        ('Se Cathedral Largest Church in Asia Old Goa', 'North Goa', 'Heritage', 'Monumental Portuguese-Manueline cathedral housing the famous Golden Bell'),
        ('Dudhsagar Waterfalls Four Tiered Sea of Milk', 'South Goa', 'Waterfall', 'Majestic 1017-foot four-tiered white torrent cascading through railway bridge'),
        ('Aguada Fort & 17th Century Portuguese Lighthouse', 'North Goa', 'Heritage', 'Massive coastal fortress overlooking Mandovi river with freshwater cistern'),
        ('Chapora Fort Red Sandstone Ramparts', 'North Goa', 'Heritage', 'Atmospheric cliff fortress overlooking Vagator beach and Arabian sunset'),
        ('Cabo de Rama Fort Sea Cliff Cape', 'South Goa', 'Heritage', 'Wild cliffside headland fortress with panoramic views over southern coastline'),
        ('Palolem Beach Crescent Bay South Goa', 'South Goa', 'Beach', 'Picturesque palm-fringed sheltered cove with calm turquoise waters'),
        ('Agonda Beach Olive Ridley Turtle Haven', 'South Goa', 'Beach', 'Quiet pristine stretch of golden sand designated as sea turtle nesting site'),
        ('Fontainhas Latin Quarter Colorful Panaji', 'North Goa', 'Heritage', 'Preserved Portuguese heritage district with terracotta-roofed pastel villas'),
        ('Netravali Bubbling Lake & Wildlife Sanctuary', 'South Goa', 'Lake/Water', 'Mysterious temple pond where methane gas bubbles continuously from floor')
    ]
}

for state, spots in india_second_level.items():
    for name, dist, cat, hint in spots:
        add_spot(name, dist, state, "India", cat, hint)

print(f"New spots after second-level India expansion: {len(new_records)}")

# =========================================================================
# STEP 4: Deep World Expansion (USA, Canada, Australia, Japan, China, Indonesia, Thailand)
# =========================================================================
print("4. Generating deep world expansion...")

world_deep_expansion = {
    'USA': [
        ('Denali National Park & Mount McKinley', 'Alaska', 'USA', 'Wildlife', 'Highest peak in North America with wilderness tundra and grizzly bears'),
        ('Kenai Fjords National Park', 'Alaska', 'USA', 'Wildlife', 'Glacial fjords with calving glaciers, whales and puffins'),
        ('Glacier Bay National Park', 'Alaska', 'USA', 'Garden/Nature', 'Massive tidewater glaciers and marine wilderness'),
        ('Waikiki Beach & Diamond Head', 'Hawaii', 'USA', 'Beach', 'World-famous crescent beach with volcanic crater backdrop'),
        ('Hawaii Volcanoes National Park', 'Hawaii', 'USA', 'Mountain/Hill', 'Active volcanoes Kilauea and Mauna Loa with lava tubes'),
        ('Haleakala National Park Maui', 'Hawaii', 'USA', 'Mountain/Hill', 'Massive dormant shield volcano crater for sunrise viewing'),
        ('Zion National Park Angels Landing', 'Utah', 'USA', 'Adventure', 'Dramatic red Navajo sandstone canyon with sheer cliff trail'),
        ('Bryce Canyon National Park Hoodoos', 'Utah', 'USA', 'Mountain/Hill', 'Largest collection of natural amphitheater rock hoodoos on Earth'),
        ('Arches National Park Delicate Arch', 'Utah', 'USA', 'Cave/Geological', 'Over 2000 natural sandstone arches in desert landscape'),
        ('Monument Valley Navajo Tribal Park', 'Arizona', 'USA', 'Mountain/Hill', 'Iconic sandstone buttes rising 1000 ft above desert floor'),
        ('Antelope Canyon Upper and Lower', 'Arizona', 'USA', 'Cave/Geological', 'World-famous slot canyon with wave-like sandstone beams of light'),
        ('Sedona Red Rock Country & Vortexes', 'Arizona', 'USA', 'Mountain/Hill', 'Dramatic red sandstone formations and spiritual energy vortexes'),
        ('Rocky Mountain National Park', 'Colorado', 'USA', 'Mountain/Hill', 'Trail Ridge Road alpine tundra and Trail peak vistas'),
        ('Garden of the Gods Colorado Springs', 'Colorado', 'USA', 'Cave/Geological', 'Dramatic red rock formations against Pikes Peak backdrop'),
        ('Glacier National Park Going-to-the-Sun Road', 'Montana', 'USA', 'Mountain/Hill', '50-mile alpine scenic highway crossing the Continental Divide'),
        ('Grand Teton National Park Jenny Lake', 'Wyoming', 'USA', 'Mountain/Hill', 'Jagged mountain range rising abruptly over alpine lakes'),
        ('Olympic National Park Hoh Rainforest', 'Washington', 'USA', 'Garden/Nature', 'Temperate rainforest with moss-draped spruce and Pacific coastline'),
        ('Mount Rainier National Park Paradise', 'Washington', 'USA', 'Mountain/Hill', 'Active stratovolcano with 25 glaciers and wildflower meadows'),
        ('Crater Lake National Park', 'Oregon', 'USA', 'Lake/Water', 'Deepest lake in USA formed inside collapsed caldera with intense blue water'),
        ('Columbia River Gorge & Multnomah Falls', 'Oregon', 'USA', 'Waterfall', '620-foot two-tiered waterfall with historic bridge view'),
        ('Big Sur Bixby Creek Bridge & Coast', 'California', 'USA', 'Beach', 'Dramatic rugged coastline along Highway 1 overlooking Pacific surf'),
        ('Death Valley National Park Badwater Basin', 'California', 'USA', 'Mountain/Hill', 'Lowest point in North America at 282 ft below sea level'),
        ('Joshua Tree National Park', 'California', 'USA', 'Garden/Nature', 'Bizarre twisted Joshua trees and giant boulder piles in Mojave desert'),
        ('Everglades National Park Airboat Tour', 'Florida', 'USA', 'Wildlife', 'Vast subtropical wetland wilderness sheltering alligators and manatees'),
        ('Key West Duval Street & Sunset Celebration', 'Florida', 'USA', 'Beach', 'Southernmost point of continental US with conch architecture'),
        ('Acadia National Park Cadillac Mountain', 'Maine', 'USA', 'Mountain/Hill', 'First place in US to view sunrise from rocky granite coastline'),
        ('Great Smoky Mountains Cades Cove', 'Tennessee', 'USA', 'Mountain/Hill', 'Most visited national park in US with mist-covered ridges and black bears'),
        ('French Quarter Bourbon Street & Jackson Square', 'Louisiana', 'USA', 'Heritage', 'Historic colonial heart of New Orleans with jazz and Creole dining')
    ],
    'Canada': [
        ('Banff Lake Louise & Fairmont Chateau', 'Alberta', 'Canada', 'Lake/Water', 'Iconic turquoise glacial lake framed by Victoria Glacier'),
        ('Moraine Lake Valley of the Ten Peaks', 'Alberta', 'Canada', 'Lake/Water', 'Glacier-fed azure lake featured on Canadian currency'),
        ('Columbia Icefield Skywalk Athabasca Glacier', 'Alberta', 'Canada', 'Adventure', 'Glass-floored observation walkway over Sunwapta Canyon'),
        ('Jasper Maligne Lake & Spirit Island', 'Alberta', 'Canada', 'Lake/Water', 'World-famous remote island in glacial lake reached by boat'),
        ('Capilano Suspension Bridge Park', 'British Columbia', 'Canada', 'Garden/Nature', '450-foot simple suspension bridge crossing canyon rainforest'),
        ('Whistler Blackcomb Ski Resort & Peak 2 Peak', 'British Columbia', 'Canada', 'Adventure', 'World-class ski resort with record-breaking gondola'),
        ('Stanley Park Seawall & Totem Poles', 'British Columbia', 'Canada', 'Garden/Nature', '1000-acre coastal rainforest park in Vancouver'),
        ('Old Quebec City Chateau Frontenac', 'Quebec', 'Canada', 'Heritage', 'UNESCO walled historic city with most photographed hotel in world'),
        ('Mont Tremblant Pedestrian Resort', 'Quebec', 'Canada', 'Mountain/Hill', 'European-style mountain resort with colorful chalets and skiing'),
        ('Gros Morne National Park Western Brook Pond', 'Newfoundland', 'Canada', 'Mountain/Hill', 'UNESCO fjord carved by glaciers with dramatic sheer cliffs'),
        ('Bay of Fundy Hopewell Rocks', 'New Brunswick', 'Canada', 'Cave/Geological', 'Highest tides in the world sculpting flowerpot sea stacks'),
        ('Peggy\'s Cove Lighthouse & Granite Rocks', 'Nova Scotia', 'Canada', 'Heritage', 'Picturesque red-and-white lighthouse on wave-washed granite shores'),
        ('Cabot Trail Cape Breton Island', 'Nova Scotia', 'Canada', 'Sightseeing', 'Spectacular 185-mile coastal highway with ocean cliff views'),
        ('Kluane National Park Mount Logan', 'Yukon', 'Canada', 'Mountain/Hill', 'Highest peak in Canada and largest non-polar icefield on Earth'),
        ('Nahanni National Park Virginia Falls', 'Northwest Territories', 'Canada', 'Waterfall', 'UNESCO wilderness park with waterfall twice the height of Niagara')
    ],
    'Australia': [
        ('Uluru Kata Tjuta Sacred Monolith', 'Northern Territory', 'Australia', 'Heritage', 'Ancient 550-million-year-old sandstone monolith sacred to Anangu people'),
        ('Kings Canyon Watarrka National Park', 'Northern Territory', 'Australia', 'Mountain/Hill', 'Red sandstone canyon with 300-meter cliffs and Garden of Eden pool'),
        ('Kakadu Ubirr Ancient Aboriginal Rock Art', 'Northern Territory', 'Australia', 'Heritage', 'World-renowned 20000-year-old Indigenous rock art gallery'),
        ('Litchfield National Park Florence Falls', 'Northern Territory', 'Australia', 'Waterfall', 'Twin waterfalls cascading into deep plunge pool surrounded by monsoon forest'),
        ('Cradle Mountain Lake St Clair', 'Tasmania', 'Australia', 'Mountain/Hill', 'Iconic jagged dolerite peak rising over glacial Dove Lake'),
        ('Freycinet Wineglass Bay Lookout', 'Tasmania', 'Australia', 'Beach', 'Curved white sand beach and sapphire sea flanked by pink granite hazards'),
        ('Port Arthur Historic Convict Site', 'Tasmania', 'Australia', 'Heritage', 'UNESCO World Heritage 19th-century penal settlement ruins'),
        ('Rottnest Island Quokka Haven', 'Western Australia', 'Australia', 'Wildlife', 'Car-free island famous for friendly smiling quokkas and 63 beaches'),
        ('Ningaloo Reef Whale Shark Swim', 'Western Australia', 'Australia', 'Wildlife', 'World-heritage fringing coral reef where visitors swim with whale sharks'),
        ('Pinnacles Desert Nambung National Park', 'Western Australia', 'Australia', 'Cave/Geological', 'Thousands of limestone pillars rising out of yellow sand dunes'),
        ('Barossa Valley Wine Tasting Trail', 'South Australia', 'Australia', 'Garden/Nature', 'Premier Shiraz wine region with historic stone cellars and vineyards'),
        ('Kangaroo Island Remarkable Rocks', 'South Australia', 'Australia', 'Cave/Geological', 'Granite boulders sculpted into surreal shapes by wind and sea'),
        ('Flinders Ranges Wilpena Pound', 'South Australia', 'Australia', 'Mountain/Hill', 'Enormous natural amphitheater of mountains in the outback'),
        ('Whitsunday Whitehaven Beach Hill Inlet', 'Queensland', 'Australia', 'Beach', 'Pure white silica sand beach with swirling turquoise tidal lagoon'),
        ('Fraser Island Kgari Lake McKenzie', 'Queensland', 'Australia', 'Island', 'World largest sand island with pristine perched freshwater dune lakes'),
        ('Daintree Rainforest Mossman Gorge', 'Queensland', 'Australia', 'Wildlife', 'World oldest tropical rainforest where emerald canopy meets river boulders'),
        ('Blue Mountains Three Sisters Rock Echo Point', 'New South Wales', 'Australia', 'Mountain/Hill', 'Famous sandstone rock formation overlooking Jamison Valley eucalyptus haze'),
        ('Byron Bay Cape Byron Lighthouse', 'New South Wales', 'Australia', 'Beach', 'Easternmost point of Australian mainland with dolphin and whale sightings'),
        ('Great Ocean Road Twelve Apostles & Loch Ard', 'Victoria', 'Australia', 'Beach', 'Iconic limestone sea stacks rising majestically from the Southern Ocean'),
        ('Phillip Island Fairy Penguin Parade', 'Victoria', 'Australia', 'Wildlife', 'Nightly parade of hundreds of wild little penguins returning from sea')
    ],
    'Japan': [
        ('Fushimi Inari 10000 Torii Gates Trail', 'Kyoto', 'Japan', 'Temple/Religious', 'Mount Inari mountain path lined with thousands of vermilion shrine gates'),
        ('Kinkaku-ji Temple of the Golden Pavilion', 'Kyoto', 'Japan', 'Heritage', 'Zen Buddhist temple with top two floors completely covered in gold leaf'),
        ('Kiyomizu-dera Wooden Stage Temple', 'Kyoto', 'Japan', 'Temple/Religious', 'Ancient hillside temple built without a single nail overlooking maple trees'),
        ('Arashiyama Sagano Bamboo Forest', 'Kyoto', 'Japan', 'Garden/Nature', 'Towering natural green bamboo grove with wind-whispering walkway'),
        ('Gion Traditional Geisha District', 'Kyoto', 'Japan', 'Heritage', 'Preserved Edo period wooden machiya merchant houses and teahouses'),
        ('Todai-ji Great Bronze Buddha Hall', 'Nara', 'Japan', 'Heritage', 'World largest wooden building housing monumental 15-meter bronze Buddha'),
        ('Nara Deer Park Sacred Sika', 'Nara', 'Japan', 'Wildlife', 'Over 1200 free-roaming sacred sika deer bowing for rice crackers'),
        ('Osaka Castle & Nishinomaru Garden', 'Osaka', 'Japan', 'Heritage', '16th-century fortress of Toyotomi Hideyoshi surrounded by stone moats'),
        ('Dotonbori Glico Running Man Sign', 'Osaka', 'Japan', 'Sightseeing', 'Vibrant neon canal district famous for takoyaki and street food'),
        ('Hiroshima Peace Memorial Genbaku Dome', 'Hiroshima', 'Japan', 'Heritage', 'UNESCO memorial ruin preserved exactly as it survived atomic bomb'),
        ('Miyajima Itsukushima Floating Torii Shrine', 'Hiroshima', 'Japan', 'Heritage', 'Iconic red Torii gate appearing to float on the Seto Inland Sea'),
        ('Lake Kawaguchiko Mount Fuji Reflection', 'Yamanashi', 'Japan', 'Lake/Water', 'Mirror-like lake offering legendary views of snow-capped Mount Fuji'),
        ('Chureito Pagoda Mount Fuji Viewpoint', 'Yamanashi', 'Japan', 'Heritage', 'Five-story red pagoda framed by cherry blossoms and Mount Fuji'),
        ('Hakone Open-Air Museum & Hot Springs', 'Kanagawa', 'Japan', 'Garden/Nature', 'Sculpture park among mountains with footbath onsens'),
        ('Kamakura Kotoku-in Great Buddha', 'Kanagawa', 'Japan', 'Heritage', 'Monumental 13-meter outdoor bronze Buddha statue surviving tsunami'),
        ('Shirakawa-go Gassho Zukuri Farmhouses', 'Gifu', 'Japan', 'Heritage', 'Steep thatched-roof historic mountain village covered in snow'),
        ('Kanazawa Kenroku-en Six Attributes Garden', 'Ishikawa', 'Japan', 'Garden/Nature', 'Ranked as one of Japan three most beautiful classical landscape gardens'),
        ('Sapporo Otaru Canal & Snow Light Festival', 'Hokkaido', 'Japan', 'Sightseeing', 'Historic Victorian gas-lit canal lined with brick warehouses'),
        ('Furano Tomita Lavender Fields', 'Hokkaido', 'Japan', 'Garden/Nature', 'Rolling rainbow flower fields blooming beneath Tokachi mountain range'),
        ('Biei Shirogane Blue Pond', 'Hokkaido', 'Japan', 'Lake/Water', 'Eerie cobalt-blue volcanic pond with submerged dead birch trees'),
        ('Shuri Castle Ryukyu Kingdom Heritage', 'Okinawa', 'Japan', 'Heritage', 'Gusuku castle of Ryukyu Kingdom blending Chinese and Japanese architecture'),
        ('Churaumi Aquarium Kuroshio Sea', 'Okinawa', 'Japan', 'Wildlife', 'Colossal multi-story tank housing giant whale sharks and manta rays')
    ],
    'China': [
        ('Badaling & Mutianyu Great Wall of China', 'Beijing', 'China', 'Heritage', 'Magnificent ancient military masonry fortifications spanning mountain ridges'),
        ('Forbidden City Palace Museum', 'Beijing', 'China', 'Heritage', 'Imperial palace of 24 emperors containing 9999 rooms across 180 acres'),
        ('Temple of Heaven Hall of Prayer for Good Harvests', 'Beijing', 'China', 'Heritage', 'Circular triple-gabled wooden building built without nails in 1420'),
        ('Summer Palace & Kunming Lake', 'Beijing', 'China', 'Garden/Nature', 'Vast imperial garden with Long Corridor and marble boat pavilion'),
        ('The Bund Historic Waterfront & Skyline', 'Shanghai', 'China', 'Sightseeing', 'Colonial European architecture facing futuristic Lujiazui skyscrapers'),
        ('Yu Garden & City God Temple', 'Shanghai', 'China', 'Garden/Nature', 'Classical Ming Dynasty garden with zig-zag bridge and dragon walls'),
        ('Terracotta Army of Emperor Qin Shi Huang', 'Shaanxi', 'China', 'Heritage', 'Thousands of life-sized individualized clay soldiers buried in 210 BCE'),
        ('Ancient City Wall of Xi\'an', 'Shaanxi', 'China', 'Heritage', 'Best-preserved 14-km ancient defensive wall in China for cycling'),
        ('Zhangjiajie Avatar Hallelujah Mountain', 'Hunan', 'China', 'Mountain/Hill', '3000 towering quartz-sandstone pillars inspiring the movie Avatar'),
        ('Tianmen Mountain Glass Skywalk & Heavens Gate', 'Hunan', 'China', 'Adventure', 'Natural karst arch reached by 999 steep stairs and world longest cable car'),
        ('Li River Karst Peaks Cruise Guilin to Yangshuo', 'Guangxi', 'China', 'Lake/Water', 'Scenic 83-km river journey depicted on the 20-yuan banknote'),
        ('Longji Longsheng Dragon Backbone Rice Terraces', 'Guangxi', 'China', 'Mountain/Hill', 'Layered agricultural terraces carved into mountains 650 years ago'),
        ('Chengdu Giant Panda Breeding Research Base', 'Sichuan', 'China', 'Wildlife', 'World premier conservation sanctuary for giant pandas and red pandas'),
        ('Leshan Giant Stone Buddha', 'Sichuan', 'China', 'Heritage', '71-meter tall stone Buddha carved out of cliff face at confluence of three rivers'),
        ('Jiuzhaigou Multi-Colored Lakes Valley', 'Sichuan', 'China', 'Lake/Water', 'UNESCO fairy valley with tiered crystal waterfalls and turquoise lakes'),
        ('Potala Palace Winter Residence of Dalai Lamas', 'Tibet', 'China', 'Heritage', 'Fortress palace with 1000 rooms perched on Marpo Ri red mountain at 12000 ft'),
        ('Jokhang Temple Barkhor Pilgrimage Street', 'Tibet', 'China', 'Temple/Religious', 'Most sacred Buddhist temple in Tibet with devout pilgrims prostrating'),
        ('Yamdrok Sacred Turquoise Lake', 'Tibet', 'China', 'Lake/Water', 'One of the three sacred lakes of Tibet framed by snow-capped mountains'),
        ('Hangzhou West Lake Three Pools Mirroring Moon', 'Zhejiang', 'China', 'Lake/Water', 'Classical freshwater lake celebrated by poets with pagodas and causeways'),
        ('Suzhou Humble Administrator\'s Garden', 'Jiangsu', 'China', 'Garden/Nature', 'Finest classical scholar garden in China featuring lotus ponds and pavilions'),
        ('Huangshan Yellow Mountain Sea of Clouds', 'Anhui', 'China', 'Mountain/Hill', 'Granite peaks with twisted pines rising through shifting mists'),
        ('Mogao Caves Thousand Buddha Grottoes', 'Gansu', 'China', 'Heritage', '492 cave shrines preserving 1000 years of Silk Road Buddhist frescoes'),
        ('Lijiang Ancient Town Waterwheels', 'Yunnan', 'China', 'Heritage', 'UNESCO stone-paved canal town of Naxi minority beneath Jade Dragon Snow Mountain'),
        ('Tiger Leaping Gorge Jinsha River Canyon', 'Yunnan', 'China', 'Adventure', 'One of the deepest river canyons in the world flanked by 5000m peaks')
    ],
    'Indonesia': [
        ('Tanah Lot Offshore Rock Temple', 'Bali', 'Indonesia', 'Temple/Religious', 'Ancient sea temple perched on wave-swept rock offshore with sunset views'),
        ('Uluwatu Cliffside Temple & Kecak Fire Dance', 'Bali', 'Indonesia', 'Temple/Religious', '70-meter sea cliff temple famous for open-air sunset Kecak choir dance'),
        ('Tegallalang Layered Rice Terraces', 'Bali', 'Indonesia', 'Garden/Nature', 'Iconic emerald green valley with subak cooperative irrigation system'),
        ('Tirta Empul Holy Water Spring Temple', 'Bali', 'Indonesia', 'Temple/Religious', 'Sacred Hindu water temple where devotees bathe in 13 purified spouts'),
        ('Besakih Mother Temple of Bali', 'Bali', 'Indonesia', 'Temple/Religious', 'Largest and holiest temple complex of 86 shrines perched on Mount Agung slopes'),
        ('Ulun Danu Beratan Floating Water Temple', 'Bali', 'Indonesia', 'Temple/Religious', 'Iconic 11-roofed pagoda temple floating on mountain crater lake'),
        ('Jatiluwih UNESCO Rice Terraces', 'Bali', 'Indonesia', 'Garden/Nature', 'Sprawling 600 hectares of terraced paddy fields below Mount Batukaru'),
        ('Mount Batur Sunrise Volcano Trek', 'Bali', 'Indonesia', 'Adventure', 'Active volcanic crater climb for sunrise breakfast and crater steam vents'),
        ('Nusa Penida Kelingking T-Rex Beach', 'Bali', 'Indonesia', 'Beach', 'Dramatic coastal rock cliff shaped like a Tyrannosaurus Rex over turquoise cove'),
        ('Nusa Penida Broken Beach & Angel Billabong', 'Bali', 'Indonesia', 'Cave/Geological', 'Natural stone arch circular cove and crystal clear natural rock infinity pool'),
        ('Gili Trawangan Turtle Reef Snorkeling', 'Lombok', 'Indonesia', 'Island', 'Car-free island famous for coral reefs, sea turtles and sunset swings'),
        ('Mount Rinjani Crater Lake Segara Anak', 'Lombok', 'Indonesia', 'Mountain/Hill', 'Second highest volcano in Indonesia with crescent emerald lake in caldera'),
        ('Borobudur Colossal Buddhist Temple', 'Java', 'Indonesia', 'Heritage', 'World largest Buddhist monument built in 9th century with 504 Buddha statues'),
        ('Prambanan Majestic Hindu Temple Compound', 'Java', 'Indonesia', 'Heritage', 'Tallest Hindu temple in Indonesia dedicated to Brahma, Vishnu and Shiva'),
        ('Mount Bromo Active Caldera & Sea of Sand', 'Java', 'Indonesia', 'Mountain/Hill', 'Surreal volcanic moonscape inside Tengger caldera with billowing smoke'),
        ('Kawah Ijen Electric Blue Fire Crater', 'Java', 'Indonesia', 'Cave/Geological', 'Sulfuric crater lake famous for nighttime natural electric blue sulfur flames'),
        ('Komodo National Park Giant Monitor Dragons', 'Komodo', 'Indonesia', 'Wildlife', 'Protected islands home to the world largest living lizards (Komodo dragons)'),
        ('Padar Island Three Colored Beach Viewpoint', 'Komodo', 'Indonesia', 'Island', 'Iconic ridgeline viewpoint overlooking pink, black and white sand bays'),
        ('Pink Beach Pantai Merah Komodo', 'Komodo', 'Indonesia', 'Beach', 'Rare natural pink sand beach colored by microscopic red foraminifera coral'),
        ('Lake Toba Samosir Batak Island', 'Sumatra', 'Indonesia', 'Lake/Water', 'World largest volcanic lake formed inside supervolcano caldera'),
        ('Bukit Lawang Wild Orangutan Jungle Trek', 'Sumatra', 'Indonesia', 'Wildlife', 'Gunung Leuser National Park rainforest home to endangered Sumatran orangutans'),
        ('Raja Ampat Misool & Wayag Coral Karsts', 'Papua', 'Indonesia', 'Island', 'Global epicenter of marine biodiversity with emerald mushroom islands and reefs')
    ],
    'Thailand': [
        ('Grand Palace & Emerald Buddha Wat Phra Kaew', 'Bangkok', 'Thailand', 'Heritage', 'Official ceremonial royal palace complex housing the sacred jasper Buddha'),
        ('Wat Arun Temple of Dawn River Spire', 'Bangkok', 'Thailand', 'Heritage', '70-meter porcelain mosaic prang rising above the Chao Phraya River'),
        ('Wat Pho Reclining Buddha & Traditional Massage', 'Bangkok', 'Thailand', 'Temple/Religious', '46-meter gold-plated reclining Buddha and birth school of Thai massage'),
        ('Chatuchak Weekend Market 15000 Stalls', 'Bangkok', 'Thailand', 'Sightseeing', 'World largest outdoor weekend market selling handicrafts, food and fashion'),
        ('Wat Phra That Doi Suthep Golden Chedi', 'Chiang Mai', 'Thailand', 'Temple/Religious', 'Sacred mountain temple reachable by 306 dragon steps overlooking city'),
        ('Doi Inthanon National Park Roof of Thailand', 'Chiang Mai', 'Thailand', 'Mountain/Hill', 'Highest peak in Thailand at 2565m with twin royal chedis and cloud forest'),
        ('Elephant Nature Park Ethical Sanctuary', 'Chiang Mai', 'Thailand', 'Wildlife', 'Pioneering rescue haven for mistreated Asian elephants in valley forest'),
        ('Wat Rong Khun White Temple', 'Chiang Rai', 'Thailand', 'Heritage', 'Surreal contemporary white Buddhist temple created by artist Chalermchai'),
        ('Wat Rong Suea Ten Blue Temple', 'Chiang Rai', 'Thailand', 'Temple/Religious', 'Vibrant sapphire blue Buddhist temple with modern spiritual murals'),
        ('Golden Triangle Mekong River Viewpoint', 'Chiang Rai', 'Thailand', 'Sightseeing', 'Historic border confluence where Thailand, Laos and Myanmar meet'),
        ('Phra Nang Cave Beach & Princess Shrine', 'Krabi', 'Thailand', 'Beach', 'Stunning white sand cove flanked by limestone cliffs and sacred fertility cave'),
        ('Railay Beach Rock Climbing Crags', 'Krabi', 'Thailand', 'Adventure', 'World-famous peninsula cut off by limestone karsts with 700 climbing routes'),
        ('Maya Bay Phi Phi Leh The Beach', 'Krabi', 'Thailand', 'Beach', 'Iconic enclosed lagoon with 100m cliffs and powdered coral sand'),
        ('Erawan National Park 7-Tiered Emerald Falls', 'Kanchanaburi', 'Thailand', 'Waterfall', 'Seven levels of stepped cascading pools in tropical jungle'),
        ('Bridge on the River Kwai Death Railway', 'Kanchanaburi', 'Thailand', 'Heritage', 'Historic WWII bridge and railway line built by Allied prisoners of war'),
        ('Ayutthaya Wat Mahathat Buddha in Tree Roots', 'Ayutthaya', 'Thailand', 'Heritage', 'Famous stone Buddha head entwined inside the roots of a banyan tree'),
        ('Sanctuary of Truth All-Wood Temple Castle', 'Pattaya', 'Thailand', 'Heritage', '105-meter hand-carved teak temple on the sea celebrating Asian philosophies'),
        ('Khao Sok National Park Cheow Lan Lake', 'Surat Thani', 'Thailand', 'Lake/Water', 'Emerald reservoir flanked by limestone karst spires with floating raft houses'),
        ('Ang Thong National Marine Park 42 Islands', 'Surat Thani', 'Thailand', 'Island', 'Pristine archipelago of limestone peaks, hidden emerald lagoon and sea caves')
    ]
}

for country_key, spots in world_deep_expansion.items():
    for item in spots:
        if len(item) == 4:
            name, dist, cat, hint = item
            ctry = country_key
        elif len(item) == 5:
            name, dist, ctry, cat, hint = item
        else:
            continue
        add_spot(name, dist, dist, ctry, cat, hint)

print(f"Total new records after deep world expansion: {len(new_records)}")

# =========================================================================
# STEP 5: Deep Europe Expansion (21 Countries Requested)
# =========================================================================
print("5. Generating deep European expansion...")

europe_deep_expansion = {
    'France': [
        ('Mont Saint-Michel Tidal Island Abbey', 'Normandy', 'Heritage', 'Iconic medieval abbey perched on a rocky tidal island in the English Channel'),
        ('Palace of Versailles Hall of Mirrors', 'Versailles', 'Heritage', 'Opulent royal chateau with 357 mirrors and sprawling classical fountains'),
        ('Cote d\'Azur Promenade des Anglais Nice', 'Nice', 'Beach', 'Iconic palm-fringed Mediterranean coastal promenade along Baie des Anges'),
        ('Chamonix Mont-Blanc Aiguille du Midi', 'Chamonix', 'Mountain/Hill', '3842-meter alpine peak cable car offering views of highest European Alps'),
        ('Chateau de Chambord French Renaissance', 'Loire Valley', 'Heritage', 'Grandest chateau in Loire valley with double-helix staircase attributed to Da Vinci'),
        ('Gorges du Verdon Grand Canyon of Europe', 'Provence', 'Lake/Water', 'Deep turquoise river canyon flanked by 700-meter sheer limestone cliffs')
    ],
    'Italy': [
        ('Colosseum & Roman Forum Imperial Ruins', 'Rome', 'Heritage', 'World largest ancient amphitheater where gladiators fought in 80 CE'),
        ('Venice Grand Canal Gondola & St Marks Basilica', 'Venice', 'Sightseeing', 'Historic Venetian lagoon waterway lined with Renaissance palaces and bridges'),
        ('Florence Duomo Cathedral & Uffizi Gallery', 'Florence', 'Heritage', 'Brunelleschi Renaissance terracotta dome and world premier Renaissance art'),
        ('Amalfi Coast Positano Cliffside Village', 'Amalfi', 'Beach', 'Pastel houses stacked vertically on sheer cliffs above the Mediterranean sea'),
        ('Cinque Terre Riomaggiore to Monterosso', 'Liguria', 'Sightseeing', 'Five colorful centuries-old fishing villages clinging to rugged coastal cliffs'),
        ('Pompeii Preserved Roman Ruins & Mount Vesuvius', 'Campania', 'Heritage', 'Ancient Roman city frozen in time under volcanic ash from 79 CE eruption'),
        ('Lake Como Bellagio & Villa del Balbianello', 'Lombardy', 'Lake/Water', 'Y-shaped glacial alpine lake framed by elegant terraced villas and gardens'),
        ('Dolomites Tre Cime di Lavaredo Alpine Peaks', 'Trentino', 'Mountain/Hill', 'Three distinctive battlement-like limestone peaks in the Italian Alps')
    ],
    'Spain': [
        ('Sagrada Familia Gaudi Basilicata', 'Barcelona', 'Heritage', 'Antoni Gaudi awe-inspiring unfinished modernist basilica with towering spires'),
        ('Alhambra Palace & Generalife Gardens', 'Granada', 'Heritage', 'Moorish citadel palace complex featuring intricate Islamic arabesque stuccowork'),
        ('Park Guell Mosaic Dragon & Serpentine Bench', 'Barcelona', 'Garden/Nature', 'Whimsical public park system featuring multicolored mosaic salamander sculptures'),
        ('Mezquita Cathedral of Cordoba', 'Cordoba', 'Heritage', 'Monumental 8th-century forest of 856 red-and-white jasper stone columns'),
        ('Seville Plaza de Espana & Real Alcazar', 'Seville', 'Heritage', 'Grand semi-circular regional pavilion with tiled alcoves and Mudéjar royal palace'),
        ('Toledo Imperial Walled Medieval City', 'Toledo', 'Heritage', 'Historic hill fortress city where Christian, Muslim and Jewish cultures coexisted')
    ],
    'Germany': [
        ('Neuschwanstein Fairy Tale Castle Bavaria', 'Bavaria', 'Heritage', '19th-century Romanesque Revival palace inspiring the Disney sleeping beauty castle'),
        ('Brandenburg Gate & Reichstag Glass Dome', 'Berlin', 'Heritage', '18th-century neoclassical monument symbol of German unity and freedom'),
        ('Cologne Cathedral Gothic Twin Spires', 'Cologne', 'Heritage', 'Monumental twin-towered Gothic cathedral housing the Shrine of the Three Kings'),
        ('Black Forest Triberg Waterfalls & Cuckoo Clock', 'Baden-Wurttemberg', 'Garden/Nature', 'Germany highest stepped waterfalls nestled amidst dense dark pine forests'),
        ('Rothenburg ob der Tauber Medieval Town', 'Bavaria', 'Heritage', 'Pristine walled medieval town with timber-framed houses and cobblestone alleys')
    ],
    'Switzerland': [
        ('Matterhorn Zermatt Gornergrat Railway', 'Valais', 'Mountain/Hill', 'Iconic 4478m pyramid peak viewed from historic mountain rack railway'),
        ('Jungfraujoch Top of Europe Sphinx Observatory', 'Bernese Oberland', 'Mountain/Hill', 'Highest railway station in Europe at 3454m facing Aletsch Glacier'),
        ('Lucerne Chapel Bridge & Lion Monument', 'Lucerne', 'Heritage', '14th-century covered wooden footbridge with interior triangular ceiling paintings'),
        ('Lauterbrunnen Valley of 72 Waterfalls', 'Bernese Oberland', 'Waterfall', 'Alpine glacial trough valley framed by towering vertical rock cliffs and falls'),
        ('Rhine Falls Europe Largest Plain Waterfall', 'Schaffhausen', 'Waterfall', 'Massive 150-meter wide thundering waterfall with boat excursions to middle rock')
    ],
    'Austria': [
        ('Schonbrunn Palace Imperial Habsburg Gardens', 'Vienna', 'Heritage', '1441-room Baroque summer residence of Empress Maria Theresa and Franz Joseph'),
        ('Hallstatt Alpine Village on Hallstatter See', 'Salzkammergut', 'Mountain/Hill', 'Fairy tale 16th-century pastel village mirrored in placid mountain lake'),
        ('Salzburg Hohensalzburg Fortress & Mirabell', 'Salzburg', 'Heritage', 'Massive 11th-century cliff castle overlooking Mozart birthplace and baroque gardens'),
        ('Grossglockner High Alpine Road', 'Carinthia', 'Mountain/Hill', 'Spectacular panoramic 48-km road leading to Austria highest mountain at 3798m')
    ],
    'Greece': [
        ('Acropolis & Parthenon Classical Citadel', 'Athens', 'Heritage', '5th-century BCE monumental limestone citadel dedicated to goddess Athena'),
        ('Santorini Oia Blue Domes Sunset Caldera', 'Santorini', 'Sightseeing', 'Iconic whitewashed cliffside village with cobalt blue church domes and Aegean views'),
        ('Mykonos Windmills & Little Venice', 'Mykonos', 'Beach', 'Cycladic 16th-century thatched windmills perched above crystal blue waters'),
        ('Meteora Monasteries on Monolithic Rock Pillars', 'Thessaly', 'Heritage', 'Six Eastern Orthodox monasteries built atop colossal natural sandstone pillars'),
        ('Navagio Beach Shipwreck Cove Zakynthos', 'Zakynthos', 'Beach', 'Secluded limestone cove with stranded freightliner on bright white pebbles')
    ],
    'Portugal': [
        ('Pena Palace Romanticism Sintra', 'Sintra', 'Heritage', 'Vibrant yellow-and-red Romanticist castle perched atop Sintra mountain forest'),
        ('Belem Tower & Jeronimos Monastery Lisbon', 'Lisbon', 'Heritage', '16th-century Manueline architecture celebrating Age of Discoveries navigators'),
        ('Porto Dom Luis I Bridge & Douro River', 'Porto', 'Sightseeing', 'Double-deck metal arch bridge connecting historic riverside port wine lodges'),
        ('Algarve Benagil Sea Cave & Ponta da Piedade', 'Algarve', 'Cave/Geological', 'Stunning natural sea dome cave illuminated by sunlight through circular roof skylight')
    ],
    'Netherlands': [
        ('Keukenhof Tulip Gardens Lisse', 'Lisse', 'Garden/Nature', 'Garden of Europe blooming with over 7 million colorful tulips and hyacinths'),
        ('Amsterdam Canals & Anne Frank House', 'Amsterdam', 'Sightseeing', 'Concentric UNESCO canal rings, merchant canal houses and historic wartime museum'),
        ('Zaanse Schans Historic Working Windmills', 'Zaandam', 'Heritage', 'Open-air conservation village with preserved 18th-century green wooden windmills'),
        ('Giethoorn Venice of the North Car-Free Village', 'Overijssel', 'Lake/Water', 'Peaceful village with thatched-roof farmhouses connected solely by canals and wooden bridges')
    ],
    'Norway': [
        ('Geirangerfjord UNESCO Glacial Fjord Cruise', 'More og Romsdal', 'Lake/Water', 'Deep sapphire fjord framed by majestic snow peaks and Seven Sisters waterfalls'),
        ('Preikestolen Pulpit Rock Lysefjord', 'Rogaland', 'Mountain/Hill', 'Massive 604-meter flat-topped cliff plateau hanging directly over Lysefjord'),
        ('Lofoten Islands Reinebringen & Rorbu Cabins', 'Nordland', 'Island', 'Dramatic Arctic archipelago of razor-sharp peaks, sandy beaches and red fisher huts'),
        ('Tromso Arctic Cathedral & Northern Lights Aurora', 'Troms', 'Adventure', 'Gateway to the Arctic for winter dog-sledding and viewing the Aurora Borealis')
    ],
    'Sweden': [
        ('Stockholm Gamla Stan Old Town & Royal Palace', 'Stockholm', 'Heritage', 'Cobblestone medieval island city center with ochre-colored buildings'),
        ('Abisko National Park Aurora Sky Station', 'Lapland', 'Adventure', 'Arctic mountain valley wilderness renowned for the clearest northern lights viewing'),
        ('Icehotel Jukkasjarvi Sculpted Ice Suites', 'Lapland', 'Sightseeing', 'World first hotel sculpted entirely from natural river ice and snow in Arctic circle')
    ],
    'Finland': [
        ('Rovaniemi Santa Claus Village Arctic Circle', 'Lapland', 'Sightseeing', 'Official hometown of Santa Claus crossed by the Arctic Circle boundary line'),
        ('Suomenlinna Sea Fortress Helsinki', 'Helsinki', 'Heritage', 'UNESCO 18th-century maritime fortress built across six interconnected islands'),
        ('Lake Saimaa Labyrinth & Ringed Seal Waters', 'Saimaa', 'Lake/Water', 'Vast blue lake network of 14000 islands home to rare freshwater ringed seals')
    ],
    'Iceland': [
        ('Gullfoss Golden Falls Two-Tiered Cascade', 'Golden Circle', 'Waterfall', 'Massive glacial cataract on Hvita river plunging 32 meters into rugged canyon'),
        ('Geiranger Geysir Strokkur Erupting Spout', 'Golden Circle', 'Cave/Geological', 'Active natural geothermal geyser blasting steaming water 30 meters high every 8 minutes'),
        ('Thingvellir National Park Continental Rift', 'Golden Circle', 'Cave/Geological', 'Tectonic boundary where North American and Eurasian tectonic plates drift apart'),
        ('Reynisfjara Black Sand Beach & Basalt Columns', 'Vik', 'Beach', 'Dramatic volcanic black sand shore with Reynisdrangar sea stacks and crashing waves'),
        ('Jokulsarlon Glacier Lagoon & Diamond Beach', 'Vatnajokull', 'Lake/Water', 'Luminous blue icebergs floating out to sea and glittering like diamonds on black sand')
    ],
    'Ireland': [
        ('Cliffs of Moher Atlantic Ocean Precipice', 'Clare', 'Mountain/Hill', 'Sheer 700-foot sea cliffs stretching 14 kilometers along wild Atlantic coast'),
        ('Ring of Kerry Iveragh Peninsula Scenic Circuit', 'Kerry', 'Sightseeing', '179-km circular scenic route through rugged coastal mountains and colorful villages'),
        ('Giant Causeway Basalt Columns Antrim Coast', 'Antrim', 'Cave/Geological', '40000 interlocking hexagonal basalt columns formed by ancient volcanic activity'),
        ('Blarney Castle & Stone of Eloquence', 'Cork', 'Heritage', 'Medieval stronghold where visitors kiss the legendary stone to receive the gift of gab')
    ],
    'United Kingdom': [
        ('Stonehenge Megalithic Stone Circle', 'Wiltshire', 'Heritage', 'Prehistoric 5000-year-old monument aligned with summer solstice sunrise'),
        ('Tower of London & Crown Jewels', 'London', 'Heritage', 'Historic royal fortress and prison beside Thames guarding the Royal Regalia'),
        ('Scottish Highlands Loch Ness & Eilean Donan', 'Highlands', 'Lake/Water', 'Deep mysterious freshwater loch and romantic 13th-century island castle'),
        ('Isle of Skye Fairy Pools & Old Man of Storr', 'Skye', 'Mountain/Hill', 'Surreal volcanic rock pinnacles and crystal clear mountain stream pools'),
        ('Lake District Windermere & Scafell Pike', 'Cumbria', 'Lake/Water', 'UNESCO picturesque national park with England largest natural lake and fells')
    ],
    'Poland': [
        ('Wieliczka Salt Mine Underground Chapels', 'Krakow', 'Heritage', 'UNESCO 13th-century underground mine with subterranean cathedral carved of rock salt'),
        ('Wawel Royal Castle & Dragon Den Krakow', 'Krakow', 'Heritage', 'Gothic and Renaissance royal castle seat of Polish kings on the Vistula River'),
        ('Zakopane Tatra Mountains & Kasprowy Wierch', 'Tatra', 'Mountain/Hill', 'Winter capital of Poland with traditional wooden chalets and rugged alpine trails')
    ],
    'Czech Republic': [
        ('Prague Charles Bridge & Astronomical Clock', 'Prague', 'Heritage', '14th-century Gothic stone bridge flanked by 30 statues over Vltava river'),
        ('Prague Castle & St Vitus Cathedral', 'Prague', 'Heritage', 'Vast 9th-century royal castle complex dominating the Prague skyline'),
        ('Cesky Krumlov Fairy Tale Castle River Bend', 'South Bohemia', 'Heritage', 'UNESCO medieval walled town nestled in a horseshoe loop of the Vltava')
    ],
    'Hungary': [
        ('Hungarian Parliament Building Danube River', 'Budapest', 'Heritage', 'Magnificent neo-Gothic riverside palace with 691 rooms illuminated at dusk'),
        ('Buda Castle & Fisherman Bastion Lookout', 'Budapest', 'Heritage', 'Historic castle quarter offering sweeping panoramic views across Danube bridges'),
        ('Szechenyi Thermal Baths Neo-Baroque Palace', 'Budapest', 'Sightseeing', 'Europe largest medicinal thermal bath complex with outdoor steaming pools')
    ],
    'Croatia': [
        ('Plitvice Lakes 16 Cascading Lakes UNESCO', 'Lika-Senj', 'Lake/Water', 'Terraced crystal turquoise lakes interconnected by thundering cascades and wooden boardwalks'),
        ('Dubrovnik Old Town Walled Citadel Walls', 'Dubrovnik', 'Heritage', '16th-century white stone defensive walls encasing historic Adriatic city'),
        ('Split Diocletian Roman Palace Peristyle', 'Split', 'Heritage', 'Colossal 4th-century Roman emperor palace integrated into living city center')
    ],
    'Belgium': [
        ('Grand Place Guildhalls & Town Hall Brussels', 'Brussels', 'Heritage', 'Opulent central square surrounded by gilded 17th-century baroque guild houses'),
        ('Bruges Medieval Canals & Belfry Tower', 'Bruges', 'Heritage', 'Fairy tale canal city known as Venice of the North with 83-meter belfry')
    ],
    'Denmark': [
        ('Nyhavn 17th Century Colorful Waterfront Canal', 'Copenhagen', 'Sightseeing', 'Vibrant canal street lined with 17th-century townhouses and historic wooden ships'),
        ('Tivoli Gardens Historic Theme Park Copenhagen', 'Copenhagen', 'Sightseeing', '1843 historic pleasure garden and amusement park that inspired Walt Disney'),
        ('Kronborg Castle Hamlet Elsinore Fortress', 'Helsingor', 'Heritage', 'Renaissance fortress on Oresund sound immortalized as Elsinore in Shakespeare Hamlet')
    ]
}

for country_key, spots in europe_deep_expansion.items():
    for name, dist, cat, hint in spots:
        add_spot(name, dist, dist, country_key, cat, hint)

print(f"Total new records after European expansion: {len(new_records)}")

# =========================================================================
# STEP 6: Merge with Original 19,974, Validate, and Save
# =========================================================================
df_new = pd.DataFrame(new_records)
print(f"Total brand new unique spots prepared: {len(df_new)}")

df_final = pd.concat([df_orig, df_new], ignore_index=True)

# Ensure schema columns
cols = ['Name of the Place', 'District', 'Famous_For', 'Activities', 'State', 'Country', 'Category', 'Travel_Style', 'Best_Season', 'Budget_Category', 'Duration_Days']
df_final = df_final[cols]

# Clean all columns to ASCII
for col in df_final.columns:
    if df_final[col].dtype == object:
        df_final[col] = df_final[col].apply(clean_ascii)

# Deduplicate by lowercase Name of the Place
df_final['norm_key'] = df_final['Name of the Place'].str.strip().str.lower()
df_final = df_final.drop_duplicates(subset=['norm_key'], keep='first').drop(columns=['norm_key'])

total_final = len(df_final)
print(f"\n==========================================")
print(f"Base Count: {len(df_orig)}")
print(f"New Rows Added: {total_final - len(df_orig)}")
print(f"Final Total Count: {total_final}")
print(f"==========================================")

# Assertions
assert total_final >= len(df_orig), "Error: Row count decreased!"
assert df_final.isnull().sum().sum() == 0, "Error: Dataset contains null values!"

print("\nNull checks passed (0 nulls across all columns).")
print(f"Category Distribution:")
print(df_final['Category'].value_counts())
print(f"\nTotal Countries represented: {df_final['Country'].nunique()}")
print(f"Top 20 Countries:")
print(df_final['Country'].value_counts().head(20))

# Verify no country called "Kerala"
kerala_as_country = len(df_final[df_final['Country'].str.lower() == 'kerala'])
assert kerala_as_country == 0, f"Error: Found {kerala_as_country} rows where Country is Kerala!"
print(f"Verified: 0 rows have Country='Kerala'. Kerala spots properly mapped to State='Kerala', Country='India'!")
print(f"Total Kerala Spots in Database: {len(df_final[df_final['State'] == 'Kerala'])}")

# Save backups
shutil.copyfile(ORIGINAL_CSV, ORIGINAL_CSV + '.pre_deep_expand.bak')
shutil.copyfile(BACKEND_CSV, BACKEND_CSV + '.pre_deep_expand.bak')
print("Created .pre_deep_expand.bak backups.")

# Save to destination files
df_final.to_csv(ORIGINAL_CSV, index=False, encoding='utf-8')
df_final.to_csv(BACKEND_CSV, index=False, encoding='utf-8')
print(f"Successfully saved {total_final} spots to {ORIGINAL_CSV}")
print(f"Successfully saved {total_final} spots to {BACKEND_CSV}")
