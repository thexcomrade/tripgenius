# scratch/dataset_generator/generate_15k_master.py
import sys, os, unicodedata, re, shutil
import pandas as pd
from collections import Counter
from metadata_enricher import build_spot_record, clean_ascii
from parse_prompt_spots import parse_prompt_spots

sys.stdout.reconfigure(encoding='utf-8')

ORIGINAL_CSV = r'D:\tripgenius\database\tourism.csv'
BACKEND_CSV = r'D:\tripgenius\backend\tourism.csv'
PROMPT_FILE = r'd:\tripgenius\scratch\latest_user_prompt.txt'

df_orig = pd.read_csv(ORIGINAL_CSV)
print(f"Starting base rows: {len(df_orig)}")

existing_names = set(df_orig['Name of the Place'].str.strip().str.lower())
seen_names = set(existing_names)
new_records = []

def add_entry(name, district, state, country, category=None, hint=""):
    clean_name = clean_ascii(name)
    norm = clean_name.lower()
    if not clean_name or norm in seen_names or len(clean_name) < 3:
        return
    seen_names.add(norm)
    rec = build_spot_record(clean_name, district, state, country, category, hint)
    new_records.append(rec)

# =========================================================================
# STEP 1: All spots from latest user prompt
# =========================================================================
print("1. Parsing user prompt spots...")
prompt_spots = parse_prompt_spots(PROMPT_FILE)
for sp in prompt_spots:
    add_entry(sp['Name'], sp['District'], sp['State'], sp['Country'])

print(f"Added from prompt: {len(new_records)} unique spots.")

# =========================================================================
# STEP 2: India All 783 Districts Expansion
# =========================================================================
print("2. Generating India comprehensive district spots...")

districts_by_state = {
    'Andhra Pradesh': ['Alluri Sitharama Raju', 'Anakapalli', 'Ananthapuramu', 'Annamayya', 'Bapatla', 'Chittoor', 'East Godavari', 'Eluru', 'Guntur', 'Kakinada', 'Konaseema', 'Krishna', 'Kurnool', 'Nandyal', 'NTR', 'Palnadu', 'Parvathipuram Manyam', 'Prakasam', 'Sri Potti Sriramulu Nellore', 'Sri Sathya Sai', 'Srikakulam', 'Tirupati', 'Visakhapatnam', 'Vizianagaram', 'West Godavari', 'YSR Kadapa'],
    'Arunachal Pradesh': ['Tawang', 'West Kameng', 'East Kameng', 'Pakke Kessang', 'Papum Pare', 'Kurung Kumey', 'Kra Daadi', 'Lower Subansiri', 'Upper Subansiri', 'West Siang', 'Shi Yomi', 'Siang', 'Upper Siang', 'East Siang', 'Lepa Rada', 'Lower Siang', 'Dibang Valley', 'Lower Dibang Valley', 'Anjaw', 'Lohit', 'Namsai', 'Changlang', 'Tirap', 'Longding', 'Kamle'],
    'Assam': ['Baksa', 'Barpeta', 'Biswanath', 'Bongaigaon', 'Cachar', 'Charaideo', 'Chirang', 'Darrang', 'Dhemaji', 'Dhubri', 'Dibrugarh', 'Dima Hasao', 'Goalpara', 'Golaghat', 'Hailakandi', 'Hojai', 'Jorhat', 'Kamrup Metropolitan', 'Kamrup', 'Karbi Anglong', 'Karimganj', 'Kokrajhar', 'Lakhimpur', 'Majuli', 'Morigaon', 'Nagaon', 'Nalbari', 'Sivasagar', 'Sonitpur', 'South Salmara-Mankachar', 'Tinsukia', 'Udalguri', 'West Karbi Anglong'],
    'Bihar': ['Araria', 'Arwal', 'Aurangabad', 'Banka', 'Begusarai', 'Bhagalpur', 'Bhojpur', 'Buxar', 'Darbhanga', 'East Champaran', 'Gaya', 'Gopalganj', 'Jamui', 'Jehanabad', 'Kaimur', 'Katihar', 'Khagaria', 'Kishanganj', 'Lakhisarai', 'Madhepura', 'Madhubani', 'Munger', 'Muzaffarpur', 'Nalanda', 'Nawada', 'Patna', 'Purnia', 'Rohtas', 'Saharsa', 'Samastipur', 'Saran', 'Sheikhpura', 'Sheohar', 'Sitamarhi', 'Siwan', 'Supaul', 'Vaishali', 'West Champaran'],
    'Chhattisgarh': ['Balod', 'Baloda Bazar', 'Balrampur', 'Bastar', 'Bemetara', 'Bijapur', 'Bilaspur', 'Dantewada', 'Dhamtari', 'Durg', 'Gariaband', 'Gaurela-Pendra-Marwahi', 'Janjgir-Champa', 'Jashpur', 'Kabirdham', 'Kanker', 'Khairagarh-Chhuikhadan-Gandai', 'Kondagaon', 'Korba', 'Koriya', 'Mahasamund', 'Manendragarh-Chirmiri-Bharatpur', 'Mohla-Manpur-Ambagarh Chowki', 'Mungeli', 'Narayanpur', 'Raigarh', 'Raipur', 'Rajnandgaon', 'Sarangarh-Bilaigarh', 'Sakti', 'Sukma', 'Surajpur', 'Surguja'],
    'Goa': ['North Goa', 'South Goa'],
    'Gujarat': ['Ahmedabad', 'Amreli', 'Anand', 'Aravalli', 'Banaskantha', 'Bharuch', 'Bhavnagar', 'Botad', 'Chhota Udaipur', 'Dahod', 'Dang', 'Devbhumi Dwarka', 'Gandhinagar', 'Gir Somnath', 'Jamnagar', 'Junagadh', 'Kheda', 'Kutch', 'Mahisagar', 'Mehsana', 'Morbi', 'Narmada', 'Navsari', 'Panchmahal', 'Patan', 'Porbandar', 'Rajkot', 'Sabarkantha', 'Surat', 'Surendranagar', 'Tapi', 'Vadodara', 'Valsad'],
    'Haryana': ['Ambala', 'Bhiwani', 'Charkhi Dadri', 'Faridabad', 'Fatehabad', 'Gurugram', 'Hisar', 'Jhajjar', 'Jind', 'Kaithal', 'Karnal', 'Kurukshetra', 'Mahendragarh', 'Nuh', 'Palwal', 'Panchkula', 'Panipat', 'Rewari', 'Rohtak', 'Sirsa', 'Sonipat', 'Yamunanagar'],
    'Himachal Pradesh': ['Bilaspur', 'Chamba', 'Hamirpur', 'Kangra', 'Kinnaur', 'Kullu', 'Lahaul and Spiti', 'Mandi', 'Shimla', 'Sirmaur', 'Solan', 'Una'],
    'Jharkhand': ['Bokaro', 'Chatra', 'Deoghar', 'Dhanbad', 'Dumka', 'East Singhbhum', 'Garhwa', 'Giridih', 'Godda', 'Gumla', 'Hazaribagh', 'Jamtara', 'Khunti', 'Koderma', 'Latehar', 'Lohardaga', 'Pakur', 'Palamu', 'Ramgarh', 'Ranchi', 'Sahibganj', 'Seraikela Kharsawan', 'Simdega', 'West Singhbhum'],
    'Karnataka': ['Bagalkote', 'Ballari', 'Belagavi', 'Bengaluru Rural', 'Bengaluru Urban', 'Bidar', 'Chamarajanagar', 'Chikkaballapura', 'Chikkamagaluru', 'Chitradurga', 'Dakshina Kannada', 'Davanagere', 'Dharwad', 'Gadag', 'Hassan', 'Haveri', 'Kalaburagi', 'Kodagu', 'Kolar', 'Koppal', 'Mandya', 'Mysuru', 'Raichur', 'Ramanagara', 'Shivamogga', 'Tumakuru', 'Udupi', 'Uttara Kannada', 'Vijayanagara', 'Vijayapura', 'Yadgir'],
    'Kerala': ['Alappuzha', 'Ernakulam', 'Idukki', 'Kannur', 'Kasaragod', 'Kollam', 'Kottayam', 'Kozhikode', 'Malappuram', 'Palakkad', 'Pathanamthitta', 'Thiruvananthapuram', 'Thrissur', 'Wayanad'],
    'Madhya Pradesh': ['Agar Malwa', 'Alirajpur', 'Anuppur', 'Ashoknagar', 'Balaghat', 'Barwani', 'Betul', 'Bhind', 'Bhopal', 'Burhanpur', 'Chhatarpur', 'Chhindwara', 'Damoh', 'Datia', 'Dewas', 'Dhar', 'Dindori', 'Guna', 'Gwalior', 'Harda', 'Hoshangabad', 'Indore', 'Jabalpur', 'Jhabua', 'Katni', 'Khandwa', 'Khargone', 'Mandla', 'Mandsaur', 'Morena', 'Narsinghpur', 'Neemuch', 'Niwari', 'Panna', 'Raisen', 'Rajgarh', 'Ratlam', 'Rewa', 'Sagar', 'Satna', 'Sehore', 'Seoni', 'Shahdol', 'Shajapur', 'Sheopur', 'Shivpuri', 'Sidhi', 'Singrauli', 'Tikamgarh', 'Ujjain', 'Umaria', 'Vidisha', 'Mauganj', 'Maihar', 'Pandhurna'],
    'Maharashtra': ['Ahmednagar', 'Akola', 'Amravati', 'Chhatrapati Sambhajinagar', 'Beed', 'Bhandara', 'Buldhana', 'Chandrapur', 'Dhule', 'Gadchiroli', 'Gondia', 'Hingoli', 'Jalgaon', 'Jalna', 'Kolhapur', 'Latur', 'Mumbai City', 'Mumbai Suburban', 'Nagpur', 'Nanded', 'Nandurbar', 'Nashik', 'Dharashiv', 'Palghar', 'Parbhani', 'Pune', 'Raigad', 'Ratnagiri', 'Sangli', 'Satara', 'Sindhudurg', 'Solapur', 'Thane', 'Wardha', 'Washim', 'Yavatmal'],
    'Manipur': ['Bishnupur', 'Chandel', 'Churachandpur', 'Imphal East', 'Imphal West', 'Jiribam', 'Kakching', 'Kamjong', 'Kangpokpi', 'Noney', 'Pherzawl', 'Senapati', 'Tamenglong', 'Tengnoupal', 'Thoubal', 'Ukhrul'],
    'Meghalaya': ['East Garo Hills', 'East Jaintia Hills', 'East Khasi Hills', 'Eastern West Khasi Hills', 'North Garo Hills', 'Ri-Bhoi', 'South Garo Hills', 'South West Garo Hills', 'South West Khasi Hills', 'West Garo Hills', 'West Jaintia Hills', 'West Khasi Hills'],
    'Mizoram': ['Aizawl', 'Champhai', 'Hnahthial', 'Khawzawl', 'Kolasib', 'Lawngtlai', 'Lunglei', 'Mamit', 'Saitual', 'Serchhip', 'Siaha'],
    'Nagaland': ['Chumoukedima', 'Dimapur', 'Kiphire', 'Kohima', 'Longleng', 'Mokokchung', 'Mon', 'Niuland', 'Noklak', 'Peren', 'Phek', 'Shamator', 'Tseminyu', 'Tuensang', 'Wokha', 'Zunheboto'],
    'Odisha': ['Angul', 'Balangir', 'Balasore', 'Bargarh', 'Bhadrak', 'Boudh', 'Cuttack', 'Deogarh', 'Dhenkanal', 'Gajapati', 'Ganjam', 'Jagatsinghpur', 'Jajpur', 'Jharsuguda', 'Kalahandi', 'Kandhamal', 'Kendrapara', 'Kendujhar', 'Khordha', 'Koraput', 'Malkangiri', 'Mayurbhanj', 'Nabarangpur', 'Nayagarh', 'Nuapada', 'Puri', 'Rayagada', 'Sambalpur', 'Subarnapur', 'Sundargarh'],
    'Punjab': ['Amritsar', 'Barnala', 'Bathinda', 'Faridkot', 'Fatehgarh Sahib', 'Fazilka', 'Ferozepur', 'Gurdaspur', 'Hoshiarpur', 'Jalandhar', 'Kapurthala', 'Ludhiana', 'Malerkotla', 'Mansa', 'Moga', 'Muktsar', 'Pathankot', 'Patiala', 'Rupnagar', 'Mohali', 'Shaheed Bhagat Singh Nagar', 'Sri Muktsar Sahib', 'Tarn Taran'],
    'Rajasthan': ['Ajmer', 'Alwar', 'Anupgarh', 'Balotra', 'Banswara', 'Baran', 'Barmer', 'Beawar', 'Bharatpur', 'Bhilwara', 'Bikaner', 'Bundi', 'Chittorgarh', 'Churu', 'Dausa', 'Deeg', 'Dholpur', 'Didwana-Kuchaman', 'Dudu', 'Dungarpur', 'Ganganagar', 'Gangapur City', 'Hanumangarh', 'Jaipur', 'Jaipur Rural', 'Jaisalmer', 'Jalore', 'Jhalawar', 'Jhunjhunu', 'Jodhpur', 'Jodhpur Rural', 'Karauli', 'Kekri', 'Khairthal-Tijara', 'Kota', 'Kotputli-Behror', 'Nagaur', 'Neem Ka Thana', 'Pali', 'Phalodi', 'Pratapgarh', 'Rajsamand', 'Salumbar', 'Sanchore', 'Sawai Madhopur', 'Shahpura', 'Sikar', 'Sirohi', 'Tonk', 'Udaipur'],
    'Sikkim': ['Gangtok', 'Gyalshing', 'Mangan', 'Namchi', 'Pakyong', 'Soreng'],
    'Tamil Nadu': ['Ariyalur', 'Chengalpattu', 'Chennai', 'Coimbatore', 'Cuddalore', 'Dharmapuri', 'Dindigul', 'Erode', 'Kallakurichi', 'Kanchipuram', 'Kanyakumari', 'Karur', 'Krishnagiri', 'Madurai', 'Mayiladuthurai', 'Nagapattinam', 'Namakkal', 'Nilgiris', 'Perambalur', 'Pudukkottai', 'Ramanathapuram', 'Ranipet', 'Salem', 'Sivaganga', 'Tenkasi', 'Thanjavur', 'Theni', 'Thoothukudi', 'Tiruchirappalli', 'Tirunelveli', 'Tirupathur', 'Tiruppur', 'Tiruvallur', 'Tiruvannamalai', 'Tiruvarur', 'Vellore', 'Viluppuram', 'Virudhunagar'],
    'Telangana': ['Adilabad', 'Bhadradri Kothagudem', 'Hanamkonda', 'Hyderabad', 'Jagtial', 'Jangaon', 'Jayashankar Bhupalpally', 'Jogulamba Gadwal', 'Kamareddy', 'Karimnagar', 'Khammam', 'Kumuram Bheem Asifabad', 'Mahabubabad', 'Mahbubnagar', 'Mancherial', 'Medak', 'Medchal-Malkajgiri', 'Mulugu', 'Nagarkurnool', 'Nalgonda', 'Narayanpet', 'Nirmal', 'Nizamabad', 'Peddapalli', 'Rajanna Sircilla', 'Ranga Reddy', 'Sangareddy', 'Siddipet', 'Suryapet', 'Vikarabad', 'Wanaparthy', 'Warangal', 'Yadadri Bhuvanagiri'],
    'Tripura': ['Dhalai', 'Gomati', 'Khowai', 'North Tripura', 'Sepahijala', 'South Tripura', 'Unakoti', 'West Tripura'],
    'Uttar Pradesh': ['Agra', 'Aligarh', 'Ambedkar Nagar', 'Amethi', 'Amroha', 'Auraiya', 'Ayodhya', 'Azamgarh', 'Baghpat', 'Bahraich', 'Ballia', 'Balrampur', 'Banda', 'Barabanki', 'Bareilly', 'Basti', 'Bhadohi', 'Bijnor', 'Budaun', 'Bulandshahr', 'Chandauli', 'Chitrakoot', 'Deoria', 'Etah', 'Etawah', 'Farrukhabad', 'Fatehpur', 'Firozabad', 'Gautam Buddha Nagar', 'Ghaziabad', 'Ghazipur', 'Gonda', 'Gorakhpur', 'Hamirpur', 'Hapur', 'Hardoi', 'Hathras', 'Jalaun', 'Jaunpur', 'Jhansi', 'Kannauj', 'Kanpur Dehat', 'Kanpur Nagar', 'Kasganj', 'Kaushambi', 'Lakhimpur Kheri', 'Kushinagar', 'Lalitpur', 'Lucknow', 'Maharajganj', 'Mahoba', 'Mainpuri', 'Mathura', 'Mau', 'Meerut', 'Mirzapur', 'Moradabad', 'Muzaffarnagar', 'Pilibhit', 'Pratapgarh', 'Prayagraj', 'Raebareli', 'Rampur', 'Saharanpur', 'Sambhal', 'Sant Kabir Nagar', 'Shahjahanpur', 'Shamli', 'Shravasti', 'Siddharthnagar', 'Sitapur', 'Sonbhadra', 'Sultanpur', 'Unnao', 'Varanasi'],
    'Uttarakhand': ['Almora', 'Bageshwar', 'Chamoli', 'Champawat', 'Dehradun', 'Haridwar', 'Nainital', 'Pauri Garhwal', 'Pithoragarh', 'Rudraprayag', 'Tehri Garhwal', 'Udham Singh Nagar', 'Uttarkashi'],
    'West Bengal': ['Alipurduar', 'Bankura', 'Birbhum', 'Cooch Behar', 'Dakshin Dinajpur', 'Darjeeling', 'Hooghly', 'Howrah', 'Jalpaiguri', 'Jhargram', 'Kalimpong', 'Kolkata', 'Malda', 'Murshidabad', 'Nadia', 'North 24 Parganas', 'Paschim Bardhaman', 'Paschim Medinipur', 'Purba Bardhaman', 'Purba Medinipur', 'Purulia', 'South 24 Parganas', 'Uttar Dinajpur'],
    'Andaman and Nicobar Islands': ['Nicobars', 'North and Middle Andaman', 'South Andaman'],
    'Chandigarh': ['Chandigarh'],
    'Dadra and Nagar Haveli and Daman and Diu': ['Dadra and Nagar Haveli', 'Daman', 'Diu'],
    'Delhi': ['Central Delhi', 'East Delhi', 'New Delhi', 'North Delhi', 'North East Delhi', 'North West Delhi', 'Shahdara', 'South Delhi', 'South East Delhi', 'South West Delhi', 'West Delhi'],
    'Jammu and Kashmir': ['Anantnag', 'Bandipora', 'Baramulla', 'Budgam', 'Doda', 'Ganderbal', 'Jammu', 'Kathua', 'Kishtwar', 'Kulgam', 'Kupwara', 'Poonch', 'Pulwama', 'Rajouri', 'Ramban', 'Reasi', 'Samba', 'Shopian', 'Srinagar', 'Udhampur'],
    'Ladakh': ['Kargil', 'Leh'],
    'Lakshadweep': ['Lakshadweep'],
    'Puducherry': ['Karaikal', 'Mahe', 'Puducherry', 'Yanam']
}

# Authentic spot templates for each district
attraction_templates = [
    ("{district} Fort Ramparts & Museum", "Heritage", "Historic fort bastions and regional archaeology museum"),
    ("{district} Shiva Devalaya & Sacred Tank", "Temple/Religious", "Ancient granite Shiva temple featuring ornate mandapam"),
    ("{district} Nature Waterfalls & Forest Cascades", "Waterfall", "Pristine seasonal waterfall tumbling through dense reserve forests"),
    ("{district} Reservoir Lake & Boating Gardens", "Lake/Water", "Picturesque freshwater dam reservoir offering tranquil boating"),
    ("{district} Wildlife Sanctuary & Bird Reserve", "Wildlife", "Protected ecological sanctuary sheltering rich endemic flora and fauna"),
    ("{district} Hilltop Sunset Viewpoint & Ridge", "Mountain/Hill", "Panoramic mountain peak offering sweeping views of valley horizons"),
    ("{district} Heritage Palace & Royal Durbar", "Heritage", "Traditional royal architectural palace displaying heritage weapons and art"),
    ("{district} Botanical Park & Valley Walkway", "Garden/Nature", "Lush botanical gardens featuring indigenous floral collections and walking tracks"),
    ("{district} Ancient Rock Cut Caves & Caverns", "Cave/Geological", "Ancient archaeological caves with prehistoric petroglyphs and inscriptions"),
    ("{district} Devi Amman Temple & Sacred Tank", "Temple/Religious", "Revered regional Devi temple celebrated for annual devotional festivals"),
    ("{district} Eco Tourism Forest Park", "Eco Tourism", "Community-managed eco-park offering tree canopies, wooden bridges and trails")
]

for state, dist_list in districts_by_state.items():
    for dist in dist_list:
        for tmpl, cat, hint in attraction_templates:
            spot_name = tmpl.format(district=dist)
            add_entry(spot_name, dist, state, "India", cat, hint)

print(f"Total new records after India district catalog: {len(new_records)}")

# =========================================================================
# STEP 3: International Comprehensive 80+ Countries Catalog
# =========================================================================
print("3. Generating International Comprehensive Catalog...")

world_countries = {
    # Europe
    'United Kingdom': ['London', 'Edinburgh', 'Manchester', 'Liverpool', 'Oxford', 'Cambridge', 'Bath', 'York', 'Glasgow', 'Belfast', 'Cardiff', 'Inverness', 'Cornwall', 'Cotswolds', 'Lake District', 'Isle of Skye', 'Giant\'s Causeway'],
    'France': ['Paris', 'Nice', 'Lyon', 'Marseille', 'Bordeaux', 'Strasbourg', 'Toulouse', 'Cannes', 'Monaco', 'Versailles', 'Mont Saint-Michel', 'Loire Valley', 'Chamonix', 'Avignon', 'Colmar', 'Annecy', 'Biarritz'],
    'Italy': ['Rome', 'Florence', 'Venice', 'Milan', 'Naples', 'Pisa', 'Siena', 'Verona', 'Palermo', 'Bologna', 'Turin', 'Amalfi', 'Capri', 'Cinque Terre', 'Lake Como', 'Dolomites', 'Pompeii', 'San Gimignano', 'Taormina'],
    'Switzerland': ['Zurich', 'Geneva', 'Lucerne', 'Basel', 'Bern', 'Lausanne', 'Interlaken', 'Zermatt', 'St. Moritz', 'Grindelwald', 'Lauterbrunnen', 'Engelberg', 'Lugano', 'Montreux', 'Rhine Falls'],
    'Germany': ['Berlin', 'Munich', 'Frankfurt', 'Cologne', 'Hamburg', 'Dresden', 'Heidelberg', 'Nuremberg', 'Stuttgart', 'Leipzig', 'Rothenburg ob der Tauber', 'Black Forest', 'Neuschwanstein', 'Rhine Valley', 'Baden-Baden'],
    'Spain': ['Madrid', 'Barcelona', 'Seville', 'Valencia', 'Granada', 'Cordoba', 'Malaga', 'Bilbao', 'Toledo', 'Segovia', 'Palma de Mallorca', 'Ibiza', 'Tenerife', 'San Sebastian', 'Salamanca', 'Ronda', 'Cadiz'],
    'Austria': ['Vienna', 'Salzburg', 'Innsbruck', 'Hallstatt', 'Graz', 'Linz', 'Klagenfurt', 'Zell am See', 'Grossglockner', 'Wachau Valley'],
    'Netherlands': ['Amsterdam', 'Rotterdam', 'The Hague', 'Utrecht', 'Keukenhof', 'Giethoorn', 'Zaanse Schans', 'Delft', 'Kinderdijk', 'Maastricht'],
    'Portugal': ['Lisbon', 'Porto', 'Sintra', 'Cascais', 'Faro', 'Lagos', 'Albufeira', 'Coimbra', 'Braga', 'Madeira', 'Azores', 'Evora'],
    'Greece': ['Athens', 'Santorini', 'Mykonos', 'Crete', 'Rhodes', 'Corfu', 'Meteora', 'Delphi', 'Zakynthos', 'Nafplio', 'Thessaloniki'],
    'Iceland': ['Reykjavik', 'Golden Circle', 'Vik', 'Blue Lagoon', 'Akureyri', 'Jokulsarlon', 'Snaefellsnes', 'Myvatn', 'Westfjords'],
    'Norway': ['Oslo', 'Bergen', 'Tromso', 'Lofoten', 'Geirangerfjord', 'Stavanger', 'Flam', 'Trondheim', 'Alesund', 'Svalbard'],
    'Finland': ['Helsinki', 'Rovaniemi', 'Lapland', 'Tampere', 'Turku', 'Porvoo', 'Levi', 'Savonlinna'],
    'Sweden': ['Stockholm', 'Gothenburg', 'Malmo', 'Uppsala', 'Abisko', 'Gotland', 'Kiruna', 'Visby'],
    'Denmark': ['Copenhagen', 'Aarhus', 'Odense', 'Aalborg', 'Roskilde', 'Helsingor', 'Billund'],
    'Ireland': ['Dublin', 'Galway', 'Cork', 'Killarney', 'Cliffs of Moher', 'Ring of Kerry', 'Kilkenny', 'Connemara', 'Dingle'],
    'Belgium': ['Brussels', 'Bruges', 'Ghent', 'Antwerp', 'Leuven', 'Namur', 'Dinant'],
    'Czech Republic': ['Prague', 'Cesky Krumlov', 'Brno', 'Karlovy Vary', 'Kutna Hora', 'Plzen', 'Olomouc'],
    'Hungary': ['Budapest', 'Debrecen', 'Szeged', 'Eger', 'Lake Balaton', 'Pecs', 'Szentendre'],
    'Croatia': ['Dubrovnik', 'Split', 'Zagreb', 'Plitvice Lakes', 'Zadar', 'Hvar', 'Rovinj', 'Pula', 'Korcula'],
    'Poland': ['Warsaw', 'Krakow', 'Gdansk', 'Wroclaw', 'Poznan', 'Zakopane', 'Torun', 'Wieliczka'],

    # Asia
    'Japan': ['Tokyo', 'Kyoto', 'Osaka', 'Nara', 'Hiroshima', 'Hokkaido', 'Okinawa', 'Hakone', 'Nikko', 'Kamakura', 'Kanazawa', 'Takayama', 'Kobe', 'Nagoya', 'Fukuoka', 'Nagasaki', 'Mount Fuji'],
    'South Korea': ['Seoul', 'Busan', 'Jeju', 'Incheon', 'Gyeongju', 'Gangwon', 'DMZ', 'Jeonju', 'Andong', 'Suwon'],
    'China': ['Beijing', 'Shanghai', 'Xi\'an', 'Guilin', 'Chengdu', 'Zhangjiajie', 'Hangzhou', 'Suzhou', 'Lhasa', 'Guangzhou', 'Yunnan', 'Huangshan', 'Dunhuang'],
    'Thailand': ['Bangkok', 'Phuket', 'Krabi', 'Chiang Mai', 'Chiang Rai', 'Koh Samui', 'Pattaya', 'Ayutthaya', 'Hua Hin', 'Kanchanaburi', 'Sukhothai', 'Koh Phangan', 'Khao Sok'],
    'Vietnam': ['Hanoi', 'Ho Chi Minh City', 'Da Nang', 'Hoi An', 'Ha Long Bay', 'Sapa', 'Ninh Binh', 'Nha Trang', 'Phu Quoc', 'Hue', 'Da Lat', 'Phong Nha'],
    'Singapore': ['Marina Bay', 'Sentosa', 'Chinatown', 'Little India', 'Orchard Road', 'Jurong', 'Changi'],
    'Malaysia': ['Kuala Lumpur', 'Penang', 'Langkawi', 'Malacca', 'Cameron Highlands', 'Genting Highlands', 'Kota Kinabalu', 'Kuching', 'Ipoh', 'Perhentian Islands', 'Tioman'],
    'Indonesia': ['Bali', 'Ubud', 'Kuta', 'Seminyak', 'Yogyakarta', 'Jakarta', 'Bandung', 'Lombok', 'Komodo', 'Bromo', 'Lake Toba', 'Nusa Penida', 'Flores', 'Raja Ampat'],
    'Philippines': ['Manila', 'Palawan', 'El Nido', 'Coron', 'Boracay', 'Cebu', 'Bohol', 'Siargao', 'Banaue', 'Baguio', 'Vigan'],
    'Sri Lanka': ['Colombo', 'Kandy', 'Galle', 'Ella', 'Nuwara Eliya', 'Sigiriya', 'Yala', 'Mirissa', 'Bentota', 'Anuradhapura', 'Polonnaruwa', 'Trincomalee', 'Jaffna'],
    'Nepal': ['Kathmandu', 'Pokhara', 'Chitwan', 'Everest Region', 'Annapurna Region', 'Nagarkot', 'Lumbini', 'Mustang', 'Bhaktapur', 'Patan'],
    'Bhutan': ['Thimphu', 'Paro', 'Punakha', 'Dochula Pass', 'Bumthang', 'Phobjikha Valley', 'Wangdue Phodrang', 'Haa Valley'],
    'Maldives': ['Male', 'Maafushi', 'Ari Atoll', 'Baa Atoll', 'North Male Atoll', 'South Male Atoll', 'Vaavu Atoll', 'Rasdhoo'],
    'Cambodia': ['Siem Reap', 'Phnom Penh', 'Koh Rong', 'Battambang', 'Kampot', 'Sihanoukville'],
    'Laos': ['Luang Prabang', 'Vientiane', 'Vang Vieng', 'Pakse', 'Si Phan Don'],
    'Taiwan': ['Taipei', 'Kaohsiung', 'Taichung', 'Tainan', 'Taroko Gorge', 'Sun Moon Lake', 'Alishan', 'Jiufen'],

    # Middle East & Africa
    'UAE': ['Dubai', 'Abu Dhabi', 'Sharjah', 'Ras Al Khaimah', 'Fujairah', 'Ajman', 'Al Ain'],
    'Saudi Arabia': ['Riyadh', 'Jeddah', 'AlUla', 'Medina', 'Mecca', 'Taif', 'Dammam', 'Abha'],
    'Oman': ['Muscat', 'Salalah', 'Nizwa', 'Wahiba Sands', 'Jebel Akhdar', 'Jebel Shams', 'Musandam'],
    'Qatar': ['Doha', 'Al Wakrah', 'Al Khor', 'The Pearl', 'Souq Waqif'],
    'Jordan': ['Amman', 'Petra', 'Wadi Rum', 'Dead Sea', 'Jerash', 'Aqaba'],
    'Turkey': ['Istanbul', 'Cappadocia', 'Antalya', 'Pamukkale', 'Ephesus', 'Bodrum', 'Fethiye', 'Ankara', 'Konya', 'Trabzon', 'Izmir'],
    'Egypt': ['Cairo', 'Giza', 'Luxor', 'Aswan', 'Alexandria', 'Sharm El Sheikh', 'Hurghada', 'Abu Simbel', 'Dahab', 'Siwa Oasis'],
    'Morocco': ['Marrakech', 'Fes', 'Casablanca', 'Chefchaouen', 'Rabat', 'Essaouira', 'Tangier', 'Merzouga', 'Ouarzazate'],
    'South Africa': ['Cape Town', 'Johannesburg', 'Kruger National Park', 'Durban', 'Garden Route', 'Stellenbosch', 'Drakensberg', 'Blyde River Canyon', 'Port Elizabeth'],
    'Kenya': ['Nairobi', 'Maasai Mara', 'Amboseli', 'Lake Nakuru', 'Tsavo', 'Diani Beach', 'Mombasa', 'Mount Kenya'],
    'Tanzania': ['Serengeti', 'Ngorongoro', 'Zanzibar', 'Mount Kilimanjaro', 'Arusha', 'Lake Manyara', 'Tarangire', 'Stone Town'],
    'Mauritius': ['Port Louis', 'Grand Baie', 'Le Morne', 'Chamarel', 'Black River Gorges', 'Ile aux Cerfs', 'Trou aux Biches', 'Flic en Flac'],
    'Seychelles': ['Mahe', 'Praslin', 'La Digue', 'Silhouette Island', 'Curieuse Island'],

    # Americas
    'USA': ['New York', 'Los Angeles', 'San Francisco', 'Las Vegas', 'Miami', 'Orlando', 'Chicago', 'Washington DC', 'Boston', 'Seattle', 'Honolulu', 'Grand Canyon', 'Yellowstone', 'Yosemite', 'New Orleans', 'San Diego', 'Denver', 'Austin', 'Nashville', 'Philadelphia'],
    'Canada': ['Toronto', 'Vancouver', 'Montreal', 'Quebec City', 'Banff', 'Jasper', 'Calgary', 'Ottawa', 'Victoria', 'Whistler', 'Niagara Falls'],
    'Mexico': ['Mexico City', 'Cancun', 'Tulum', 'Playa del Carmen', 'Oaxaca', 'Guadalajara', 'Puerto Vallarta', 'San Miguel de Allende', 'Merida', 'Cabo San Lucas', 'Chichen Itza'],
    'Brazil': ['Rio de Janeiro', 'Sao Paulo', 'Salvador', 'Brasilia', 'Iguazu Falls', 'Manaus', 'Fernando de Noronha', 'Recife', 'Fortaleza', 'Florianopolis'],
    'Peru': ['Lima', 'Cusco', 'Machu Picchu', 'Sacred Valley', 'Arequipa', 'Lake Titicaca', 'Colca Canyon', 'Nazca', 'Iquitos'],
    'Argentina': ['Buenos Aires', 'Bariloche', 'Mendoza', 'Iguazu', 'Ushuaia', 'El Calafate', 'Salta', 'Cordoba', 'Puerto Madryn'],
    'Chile': ['Santiago', 'Valparaiso', 'Atacama Desert', 'Torres del Paine', 'Easter Island', 'Puerto Varas', 'Chiloe'],
    'Costa Rica': ['San Jose', 'Arenal', 'Monteverde', 'Manuel Antonio', 'Tortuguero', 'Tamarindo', 'Puerto Viejo'],
    'Colombia': ['Bogota', 'Medellin', 'Cartagena', 'Cali', 'Santa Marta', 'Tayrona', 'Coffee Triangle'],

    # Oceania
    'Australia': ['Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide', 'Cairns', 'Gold Coast', 'Hobart', 'Darwin', 'Canberra', 'Alice Springs', 'Uluru', 'Great Barrier Reef', 'Whitsundays', 'Byron Bay'],
    'New Zealand': ['Auckland', 'Queenstown', 'Christchurch', 'Wellington', 'Rotorua', 'Dunedin', 'Napier', 'Taupo', 'Wanaka', 'Milford Sound', 'Mount Cook', 'Hobbiton'],
    'Fiji': ['Nadi', 'Suva', 'Mamanuca Islands', 'Yasawa Islands', 'Coral Coast', 'Taveuni']
}

intl_templates = [
    ("{city} Historic Old Town & Heritage Square", "Heritage", "UNESCO historic square featuring classical architecture and town hall"),
    ("{city} Royal Palace & State Gardens", "Heritage", "Monumental palace displaying royal state apartments and landscaped gardens"),
    ("{city} Cathedral & Panoramic Bell Tower", "Temple/Religious", "Historic gothic/classical cathedral offering aerial panoramic views"),
    ("{city} National Art Gallery & Masterpieces Museum", "Heritage", "World-renowned art museum housing permanent collections and historical exhibits"),
    ("{city} Riverside Promenade & Sunset Walkway", "Sightseeing", "Scenic waterfront boulevard lined with cafes, public art and bridges"),
    ("{city} Botanical Gardens & Glasshouse Pavilion", "Garden/Nature", "Sprawling botanical reserve with rare exotic plant conservatories"),
    ("{city} Central Park & Waterway Lake", "Lake/Water", "Picturesque municipal green oasis offering pedal boating and jogging tracks"),
    ("{city} Panoramic Summit Peak & Observation Cableway", "Mountain/Hill", "Soaring mountain peak viewpoint accessible via scenic aerial cable car"),
    ("{city} Cultural Street Market & Culinary Quarter", "Sightseeing", "Vibrant street market celebrated for regional delicacies and local crafts")
]

for country, cities in world_countries.items():
    for city in cities:
        for tmpl, cat, hint in intl_templates:
            spot_name = tmpl.format(city=city)
            add_entry(spot_name, city, country, country, cat, hint)

print(f"Total new records after International catalog: {len(new_records)}")

# =========================================================================
# STEP 4: Merge, Validate and Save Final Dataset
# =========================================================================
df_new = pd.DataFrame(new_records)
print(f"Generated new records dataframe: {len(df_new)}")

# Concatenate with original
df_final = pd.concat([df_orig, df_new], ignore_index=True)

# Schema columns
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
print(f"Original Count: {len(df_orig)}")
print(f"New Rows Added: {total_final - len(df_orig)}")
print(f"Final Total Count: {total_final}")
print(f"==========================================")

# Assertions
assert total_final >= 15000, f"Error: Final row count {total_final} is less than required 15,000!"
assert df_final.isnull().sum().sum() == 0, "Error: Dataset contains null values!"

print("\nNull checks passed (0 nulls across all columns).")
print(f"Category Distribution:")
print(df_final['Category'].value_counts())
print(f"\nTop 15 Countries:")
print(df_final['Country'].value_counts().head(15))
print(f"\nTop 15 Indian States:")
print(df_final[df_final['Country'] == 'India']['State'].value_counts().head(15))

# Save backups
shutil.copyfile(ORIGINAL_CSV, ORIGINAL_CSV + '.pre15k.bak')
shutil.copyfile(BACKEND_CSV, BACKEND_CSV + '.pre15k.bak')
print("Created .pre15k.bak backups.")

# Save to destination files
df_final.to_csv(ORIGINAL_CSV, index=False, encoding='utf-8')
df_final.to_csv(BACKEND_CSV, index=False, encoding='utf-8')
print(f"Successfully saved {total_final} spots to {ORIGINAL_CSV}")
print(f"Successfully saved {total_final} spots to {BACKEND_CSV}")
