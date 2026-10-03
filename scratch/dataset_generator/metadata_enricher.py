# scratch/dataset_generator/metadata_enricher.py
import re, unicodedata

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
    if any(k in norm for k in ['beach', 'coast', 'cove', 'shore', 'cliff', 'promenade', 'atoll', 'lagoon']):
        return 'Beach'
    if any(k in norm for k in ['lake', 'dam', 'reservoir', 'backwaters', 'backwater', 'river', 'canal', 'barrage', 'sarovar', 'kund', 'tal', 'beel', 'lake']):
        return 'Lake/Water'
    if any(k in norm for k in ['island', 'dweep', 'isle', 'thuruthu', 'atoll', 'cay']):
        return 'Island'
    if any(k in norm for k in ['cave', 'caves', 'cavern', 'grotto', 'rock cut', 'stepwell', 'baoli']):
        return 'Cave/Geological'
    if any(k in norm for k in ['temple', 'mandir', 'ashram', 'mutt', 'church', 'cathedral', 'basilica', 'mosque', 'masjid', 'gurudwara', 'monastery', 'gompa', 'stupa', 'shrine', 'dham', 'pagoda', 'synagogue', 'pilgrimage', 'jyotirlinga', 'sabarimala', 'darshan', 'kovil', 'devalaya']):
        return 'Temple/Religious'
    if any(k in norm for k in ['fort', 'palace', 'castle', 'museum', 'monument', 'ruins', 'heritage', 'tomb', 'gateway', 'minar', 'mahal', 'qila', 'chateau', 'citadel', 'pyramid', 'colosseum', 'acropolis', 'jail', 'memorial']):
        return 'Heritage'
    if any(k in norm for k in ['wildlife', 'sanctuary', 'national park', 'safari', 'tiger', 'lion', 'elephant', 'bird', 'zoo', 'reserve', 'biosphere']):
        return 'Wildlife'
    if any(k in norm for k in ['trek', 'trail', 'trails', 'pass', 'climb', 'expedition', 'base camp', 'summit', 'la ']):
        return 'Adventure'
    if any(k in norm for k in ['peak', 'hill', 'hills', 'viewpoint', 'view point', 'mountain', 'mount', 'ridge', 'plateau', 'bugyal', 'valley', 'gorge', 'canyon', 'mala', 'medu', 'shola', 'top', 'betta']):
        return 'Mountain/Hill'
    if any(k in norm for k in ['garden', 'park', 'botanical', 'forest', 'plantation', 'estate', 'tea', 'flowers']):
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
        elif state_clean in ['Rajasthan', 'Gujarat', 'Madhya Pradesh', 'Delhi', 'Punjab', 'Haryana', 'Uttar Pradesh', 'Bihar']:
            season = "October to March"
        elif state_clean in ['Andaman and Nicobar Islands', 'Lakshadweep']:
            season = "October to May"
        else:
            season = "October to March"
    else:
        if country_clean in ['United Kingdom', 'France', 'Italy', 'Switzerland', 'Germany', 'Austria', 'Netherlands', 'Norway', 'Finland', 'Iceland', 'Spain', 'Greece']:
            season = "May to October"
        elif country_clean in ['USA', 'Canada']:
            season = "May to October"
        elif country_clean in ['Thailand', 'Vietnam', 'Malaysia', 'Singapore', 'Indonesia', 'Sri Lanka', 'Philippines']:
            season = "November to April"
        elif country_clean in ['UAE', 'Qatar', 'Oman', 'Saudi Arabia', 'Egypt', 'Jordan']:
            season = "November to March"
        elif country_clean in ['Japan', 'South Korea', 'China']:
            season = "March to May, September to November"
        elif country_clean in ['Australia', 'New Zealand', 'South Africa', 'Argentina', 'Chile', 'Brazil']:
            season = "October to April"
        elif country_clean in ['Nepal', 'Bhutan']:
            season = "March to May, September to November"
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
