# scratch/generate_spots_india.py
import sys

def get_india_spots():
    spots = []
    
    # helper
    def s(name, district, state, cat, famous, act, style, season, budget, days):
        spots.append((name, district, state, "India", cat, famous, act, style, season, budget, days))

    # ==========================================
    # 1. TAMIL NADU (38 Districts)
    # ==========================================
    # Chennai
    s("Kapaleeshwarar Temple Mylapore", "Chennai", "Tamil Nadu", "Temple/Religious",
      "Ancient 7th-century Dravidian temple dedicated to Lord Shiva with an iconic 37-meter rainbow gopuram",
      "Temple darshan, Dravidian architecture photography, Mylapore cultural walk, Evening prayer chanting",
      "Spiritual, Cultural, Photography", "November to February", "Budget", 1)
    s("Fort St. George Museum", "Chennai", "Tamil Nadu", "Heritage",
      "First English fortress in India established in 1644 housing colonial relics, weapons, coins and St. Mary's Church",
      "Historical museum tour, Colonial architecture study, St. Mary's Church walk, Photography",
      "Cultural, Educational, Photography", "October to March", "Budget", 1)
    s("Santhome Cathedral Basilica", "Chennai", "Tamil Nadu", "Heritage",
      "Neo-Gothic Roman Catholic minor basilica built over the tomb of St. Thomas the Apostle",
      "Church prayer, Architecture appreciation, Underground tomb museum visit, Beachside stroll",
      "Spiritual, Cultural, Architecture", "October to March", "Budget", 1)
    s("Government Museum & National Art Gallery Egmore", "Chennai", "Tamil Nadu", "Heritage",
      "Second-oldest museum in India renowned for magnificent Chola bronze sculptures including Nataraja",
      "Bronze gallery tour, Amaravati Buddhist sculptures, Numismatics study, Art appreciation",
      "Cultural, Educational, Photography", "Year-round", "Budget", 1)
    s("Guindy National Park", "Chennai", "Tamil Nadu", "Wildlife",
      "Unique protected national park situated completely within Chennai metropolis home to blackbucks and spotted deer",
      "Nature trails, Deer spotting, Birdwatching, Children's park visit, Photography",
      "Eco, Wildlife, Leisure", "October to March", "Budget", 1)
    s("Arignar Anna Zoological Park Vandalur", "Chennai", "Tamil Nadu", "Wildlife",
      "One of the largest zoological parks in Southeast Asia sprawling over 1,490 acres with safari and lion reserves",
      "Battery car safari, Lion safari, White tiger viewing, Butterfly house tour, Wildlife photography",
      "Eco, Wildlife, Family", "October to March", "Budget", 1)
    s("DakshinaChitra Heritage Museum", "Chengalpattu", "Tamil Nadu", "Heritage",
      "Living history museum showcasing traditional architecture, crafts, performing arts and folk lifestyles of South India",
      "Crafts workshops, Heritage home exploration, Folk dance viewing, Traditional pottery",
      "Cultural, Educational, Photography", "Year-round", "Moderate", 1)
    s("Muttukadu Boat House", "Chengalpattu", "Tamil Nadu", "Lake/Water",
      "Backwater estuary along the East Coast Road offering rowing, speed boating and water skiing",
      "Speedboat cruise, Water skiing, Kayaking, Sunset backwater photography",
      "Leisure, Adventure, Water Sports", "October to March", "Moderate", 1)
    s("Covelong Beach & Surfing School", "Chengalpattu", "Tamil Nadu", "Beach",
      "Historic fishing village and crescent beach famous for premier surfing schools and windsurfing",
      "Surfing lessons, Catamaran ride, Beach volleyball, Coastal seafood dining",
      "Beach, Adventure, Water Sports", "October to March", "Moderate", 1)
    s("Alamparai Fort Ruins", "Chengalpattu", "Tamil Nadu", "Heritage",
      "Historic 18th-century sea-facing brick and limestone fortress ruins overlooking the Bay of Bengal backwaters",
      "Fort photography, Backwater boat ride, Sunset viewing, Coastal walking",
      "Heritage, Photography, Leisure", "November to February", "Budget", 1)
    s("Pancha Rathas Mahabalipuram", "Chengalpattu", "Tamil Nadu", "Heritage",
      "Monolithic rock-cut shrines carved from single granite boulders in the 7th century during Pallava rule",
      "Monolithic sculpture study, Architectural photography, UNESCO heritage walk",
      "Heritage, Cultural, Photography", "October to March", "Budget", 1)
    s("Arjuna's Penance & Krishna's Butterball", "Chengalpattu", "Tamil Nadu", "Heritage",
      "World's largest open-air rock relief carving alongside a gigantic 250-ton precariously balanced granite boulder",
      "Rock bas-relief exploration, Butterball physics photography, Pallava history study",
      "Heritage, Photography, Educational", "October to March", "Budget", 1)
    s("Tiger Cave Mahabalipuram", "Chengalpattu", "Tamil Nadu", "Heritage",
      "Coastal rock-cut temple pavilion featuring a carved ring of fierce tiger and yali heads overlooking beach lawns",
      "Rock-cut cave study, Picnic on lawns, Beach stroll, Coastal photography",
      "Heritage, Leisure, Photography", "October to March", "Budget", 1)
    s("Vedanthangal Bird Sanctuary", "Chengalpattu", "Tamil Nadu", "Wildlife",
      "Oldest water bird sanctuary in India attracting over 40,000 migratory birds from around the globe",
      "Birdwatching, Photography from watchtowers, Nature walking, Pelican and heron spotting",
      "Eco, Wildlife, Birdwatching", "November to February", "Budget", 1)

    # Kanchipuram
    s("Ekambareswarar Temple", "Kanchipuram", "Tamil Nadu", "Temple/Religious",
      "Monumental Shiva temple representing the Earth element (Prithvi) with a sacred 3,500-year-old mango tree",
      "Temple darshan, 1000-pillar hall walk, Sacred mango tree viewing, Photography",
      "Spiritual, Cultural, Architecture", "October to March", "Budget", 1)
    s("Kailasanathar Temple", "Kanchipuram", "Tamil Nadu", "Temple/Religious",
      "Oldest structural sandstone temple in Kanchipuram built by Pallava King Rajasimha with exquisite friezes",
      "Sandstone sculpture appreciation, Circumbulatory tunnel walk, Historical photography",
      "Heritage, Spiritual, Architecture", "October to March", "Budget", 1)
    s("Varadharaja Perumal Temple", "Kanchipuram", "Tamil Nadu", "Temple/Religious",
      "Grand Vishnu temple famous for its stone chain rings, 100-pillar hall and the subterranean Athi Varadar wooden idol",
      "Temple darshan, Stone chain ring viewing, Dravidian architecture photography",
      "Spiritual, Cultural, Architecture", "October to March", "Budget", 1)
    s("Kanchi Kudil Heritage House", "Kanchipuram", "Tamil Nadu", "Heritage",
      "Century-old ancestral house restored into a living museum depicting traditional joint-family agricultural living",
      "Traditional home tour, Antique utensil study, Silk weaving demonstration, Photography",
      "Cultural, Educational, Leisure", "Year-round", "Budget", 1)

    # Vellore & Tirupathur & Ranipet
    s("Vellore Fort & Jalakanteswarar Temple", "Vellore", "Tamil Nadu", "Heritage",
      "Formidable 16th-century granite fort surrounded by a deep moat housing a richly sculpted Vijayanagara temple",
      "Moat rampart walk, Stone carving photography, Tipu Mahal visit, State museum tour",
      "Heritage, Architecture, Photography", "October to March", "Budget", 1)
    s("Golden Temple Sripuram", "Vellore", "Tamil Nadu", "Temple/Religious",
      "Spiritual park and Lakshmi Narayani temple gilded with over 1,500 kg of pure gold foliage in a star-shaped path",
      "Star path walking, Golden temple darshan, Spiritual meditation, Eco-park stroll",
      "Spiritual, Leisure, Cultural", "October to March", "Moderate", 1)
    s("Amirthi Zoological Park", "Vellore", "Tamil Nadu", "Wildlife",
      "Scenic nature reserve nestled in the Javadi Hills with seasonal waterfalls, trekking paths and deer enclosures",
      "Forest trekking, Waterfall picnic, Deer spotting, Nature photography",
      "Eco, Nature, Trekking", "October to February", "Budget", 1)
    s("Yelagiri Hills Swamimalai Trek", "Tirupathur", "Tamil Nadu", "Mountain/Hill",
      "Pleasant hill station cluster offering scenic hiking to the highest peak Swamimalai overlooking the plains",
      "Swamimalai summit trek, Punganoor lake boating, Nature park walks, Paragliding",
      "Eco, Adventure, Trekking", "September to March", "Moderate", 1)
    s("Jalagamparai Waterfalls", "Tirupathur", "Tamil Nadu", "Waterfall",
      "Picturesque waterfall created by the Attaru River cascading down rocky tiers in the Yelagiri foothills",
      "Waterfall dip, Forest trek, Picnic by the stream, Nature photography",
      "Nature, Waterfall, Trekking", "November to January", "Budget", 1)

    # Tiruvannamalai
    s("Annamalaiyar Temple", "Tiruvannamalai", "Tamil Nadu", "Temple/Religious",
      "Colossal temple at the base of sacred Annamalai Hill representing the Fire element (Agni Lingam)",
      "Temple darshan, 1000-pillar hall walk, Gopuram photography, Karthigai Deepam festival viewing",
      "Spiritual, Cultural, Architecture", "October to March", "Budget", 1)
    s("Girivalam Path Annamalai Hill", "Tiruvannamalai", "Tamil Nadu", "Temple/Religious",
      "Sacred 14-kilometer barefoot circumambulation path around Mount Arunachala dotted with eight Ashtalingams",
      "Spiritual barefoot walk, Ashtalingam darshan, Meditation, Sunset hill photography",
      "Spiritual, Wellness, Walking", "October to March", "Budget", 1)
    s("Sri Ramana Maharshi Ashram", "Tiruvannamalai", "Tamil Nadu", "Temple/Religious",
      "Serene spiritual sanctuary at the foot of Arunachala where sage Ramana Maharshi lived and taught self-inquiry",
      "Silent meditation, Samadhi shrine visit, Ashram bookstall, Virupaksha cave hike",
      "Spiritual, Meditation, Peace", "Year-round", "Budget", 1)
    s("Sathanur Dam & Crocodile Farm", "Tiruvannamalai", "Tamil Nadu", "Lake/Water",
      "Major gravity dam across Thenpennai River featuring landscaped gardens, crocodile park and swimming pool",
      "Dam garden walk, Crocodile viewing, Water views, Family picnic",
      "Leisure, Nature, Family", "October to February", "Budget", 1)
    s("Jawadhu Hills & Beeman Falls", "Tiruvannamalai", "Tamil Nadu", "Mountain/Hill",
      "Undisturbed blue hill range known for sandalwood groves, Vainu Bappu astronomical observatory and waterfalls",
      "Hill drive, Observatory visit, Waterfall trekking, Fruit plantation tour",
      "Eco, Adventure, Mountain", "October to March", "Budget", 1)

    # Dharmapuri & Krishnagiri
    s("Hogenakkal Falls", "Dharmapuri", "Tamil Nadu", "Waterfall",
      "Majestic series of roaring cascades on the Kaveri River celebrated as the Niagara of India with coracle rides",
      "Coracle boat ride, Fresh Kaveri fish fry tasting, Herbal oil massage, Mist photography",
      "Waterfall, Adventure, Boating", "July to February", "Budget", 1)
    s("Theerthamalai Sacred Hill Temple", "Dharmapuri", "Tamil Nadu", "Temple/Religious",
      "Ancient hill temple where Lord Rama is believed to have worshipped, famous for perennial holy springs",
      "Hill steps climb, Spring water bath, Temple worship, Valley viewpoint photography",
      "Spiritual, Trekking, Nature", "October to March", "Budget", 1)
    s("Krishnagiri Reservoir Dam", "Krishnagiri", "Tamil Nadu", "Lake/Water",
      "Picturesque dam built across Thenpennai River nestled between ancient rocky hills with landscaped parks",
      "Dam viewpoint walk, Boating, Hill photography, Children's park recreation",
      "Leisure, Picnic, Photography", "October to February", "Budget", 1)
    s("Sayeed Basha Hill Fort", "Krishnagiri", "Tamil Nadu", "Heritage",
      "Historic hilltop fortress constructed by King Krishnadevaraya and later occupied by Tipu Sultan",
      "Fort trekking, Granite ramparts exploration, Panoramic city view, Sunset photography",
      "Heritage, Adventure, Trekking", "October to March", "Budget", 1)

    # Salem & Namakkal
    s("Yercaud Emerald Lake & Deer Park", "Salem", "Tamil Nadu", "Lake/Water",
      "Charming lake situated in the heart of Shevaroy Hills offering pedal boating surrounded by lush gardens",
      "Pedal boating, Lake promenade walk, Deer feeding, Lakeside dining",
      "Leisure, Romantic, Nature", "October to June", "Moderate", 1)
    s("Lady's Seat & Pagoda Point Yercaud", "Salem", "Tamil Nadu", "Mountain/Hill",
      "Spectacular cliff viewpoint with a historic telescope house overlooking the ghat road hairpin bends and Salem town",
      "Telescope viewing, Ghat road night view photography, Cliff walk, Sunset watching",
      "Mountain, Scenic, Photography", "September to May", "Budget", 1)
    s("Killiyur Falls Yercaud", "Salem", "Tamil Nadu", "Waterfall",
      "Exhilarating 300-foot cascade formed by the overflow of Yercaud Lake plunging into the valley beneath",
      "Valley forest hike, Waterfall base dip, Nature photography, Bird watching",
      "Nature, Adventure, Waterfall", "July to January", "Budget", 1)
    s("Mettur Dam & Ellis Park", "Salem", "Tamil Nadu", "Lake/Water",
      "One of the largest and oldest dams in India built in 1934 across Kaveri River creating the Stanley Reservoir",
      "Dam viewpoint walking, Park visit, Hydroelectric plant viewing, Fresh river fish tasting",
      "Heritage, Engineering, Leisure", "October to February", "Budget", 1)
    s("Namakkal Anjaneyar Temple & Rock Fort", "Namakkal", "Tamil Nadu", "Heritage",
      "Colossal 18-foot single-stone Hanuman statue facing an 8th-century monolithic rock-cut fort built on a single granite hill",
      "Hanuman darshan, Rock-cut Narasimha cave study, Fort hilltop climb, City view photography",
      "Spiritual, Heritage, Architecture", "October to March", "Budget", 1)
    s("Kolli Hills Agaya Gangai Falls", "Namakkal", "Tamil Nadu", "Waterfall",
      "Dramatic 300-foot jungle waterfall reached via a challenging descent of 1,025 stone steps in the Kolli Hills",
      "1025-steps descent hike, Waterfall pool bath, Medicinal herbs tour, 70-hairpin curve drive",
      "Adventure, Trekking, Waterfall", "September to February", "Budget", 2)
    s("Arapaleeswarar Temple Kolli Hills", "Namakkal", "Tamil Nadu", "Temple/Religious",
      "Ancient Shiva temple situated amidst dense cloud forests of Kolli Hills mentioned in Sangam literature",
      "Temple prayer, Sacred fish feeding in river, Forest walk, Viewpoint photography",
      "Spiritual, Cultural, Nature", "September to March", "Budget", 1)

    # Erode & Tiruppur & Coimbatore
    s("Bhavanisagar Dam", "Erode", "Tamil Nadu", "Lake/Water",
      "One of the world's largest earthen dams built at the confluence of Bhavani and Moyar Rivers",
      "Dam garden walk, Boating, Engineering structure study, Sunset picnic",
      "Leisure, Nature, Family", "October to February", "Budget", 1)
    s("Kodiveri Dam Waterfalls", "Erode", "Tamil Nadu", "Waterfall",
      "Popular barrage waterfall constructed across the Bhavani River where visitors enjoy bathing in gentle cascades",
      "Cascade bathing, Coracle boating, Fresh fish fry tasting, Family picnic",
      "Leisure, Family, Fun", "Year-round", "Budget", 1)
    s("Tiruppur Kumaran Memorial & Noyyal Park", "Tiruppur", "Tamil Nadu", "Heritage",
      "Memorial commemorating Indian freedom fighter Kumaran who died holding the national flag against British forces",
      "Historical exhibition visit, Flag memorial walk, Textile shopping, Cultural reflection",
      "Cultural, Historical, Educational", "Year-round", "Budget", 1)
    s("Marudhamalai Murugan Temple", "Coimbatore", "Tamil Nadu", "Temple/Religious",
      "Beloved 12th-century hilltop temple of Lord Murugan surrounded by Western Ghats medicinal herbal flora",
      "Hill temple darshan, Herbal breeze walk, Hill steps climb, Valley photography",
      "Spiritual, Nature, Mountain", "Year-round", "Budget", 1)
    s("Perur Pateeswarar Temple", "Coimbatore", "Tamil Nadu", "Temple/Religious",
      "Ancient temple on the Noyyal River renowned for the Kanaka Sabha hall adorned with intricate stone filigree carvings",
      "Kanaka Sabha sculpture study, Sacred temple bath, Dravidian art photography",
      "Spiritual, Heritage, Architecture", "Year-round", "Budget", 1)
    s("Adiyogi Shiva Statue Isha", "Coimbatore", "Tamil Nadu", "Sightseeing",
      "Guinness World Record 112-foot steel bust of Adiyogi Shiva set against the backdrop of the Velliangiri Mountains",
      "Adiyogi viewing, Divyachamundeshwari darshan, 3D laser light & sound show, Dhyanalinga meditation",
      "Spiritual, Cultural, Photography", "Year-round", "Budget", 1)
    s("Siruvani Waterfalls and Dam", "Coimbatore", "Tamil Nadu", "Waterfall",
      "Picturesque cascade located in dense Western Ghats reserve forests celebrated for having the world's sweetest water",
      "Forest department van safari, Waterfall dip, Sweet water tasting, Jungle photography",
      "Eco, Nature, Waterfall", "September to January", "Budget", 1)
    s("Topslip Anamalai Tiger Reserve", "Coimbatore", "Tamil Nadu", "Wildlife",
      "Pristine wildlife sanctuary in the Anamalai Hills offering elephant camps, teak forests and wilderness safaris",
      "Jungle jeep safari, Elephant camp visit, Medicinal plant garden walk, Birdwatching",
      "Wildlife, Eco, Safari", "October to April", "Moderate", 2)
    s("Valparai Tea Plantations & Sholayar Dam", "Coimbatore", "Tamil Nadu", "Mountain/Hill",
      "Unspoiled hill station perched at 3,500 ft reachable via 40 hairpin bends, featuring Asia's second-deepest dam",
      "Hairpin bend drive, Sholayar reservoir visit, Tea factory tour, Lion-tailed macaque spotting",
      "Mountain, Scenic, Eco", "September to May", "Moderate", 2)

    # Nilgiris (Ooty, Coonoor, Kotagiri)
    s("Doddabetta Peak", "Nilgiris", "Tamil Nadu", "Mountain/Hill",
      "Highest mountain in the Nilgiri Hills at 2,637 meters offering 360-degree panoramic views of Bandipur and Ooty",
      "Telescope house viewing, Misty ridge walk, Valley photography, Tea stall snacking",
      "Mountain, Scenic, Photography", "October to May", "Budget", 1)
    s("Pykara Lake and Waterfalls", "Nilgiris", "Tamil Nadu", "Lake/Water",
      "Sacred river of the Toda tribe flowing into majestic twin waterfalls and a tranquil boat-house lake",
      "Speedboat cruise, Waterfall hike, Pine forest stroll, Photography",
      "Lake, Waterfall, Romantic", "September to May", "Moderate", 1)
    s("Avalanche Lake Nilgiris", "Nilgiris", "Tamil Nadu", "Lake/Water",
      "Enchanting lake formed naturally by an 1823 landslide, surrounded by rolling shola meadows and trout streams",
      "Forest department safari, Trout fishing, Wildflower photography, Peaceful lakeside walk",
      "Eco, Nature, Wilderness", "September to April", "Moderate", 1)
    s("Emerald Lake Ooty", "Nilgiris", "Tamil Nadu", "Lake/Water",
      "Serene, lesser-crowded turquoise lake nestled amidst lush tea plantations and eucalyptus forests",
      "Lakeside picnic, Tea plantation walks, Sunrise photography, Birdwatching",
      "Nature, Romantic, Leisure", "Year-round", "Budget", 1)
    s("Sim's Park Coonoor", "Nilgiris", "Tamil Nadu", "Garden/Nature",
      "Uniquely terraced botanical garden established in 1874 featuring over 1,000 species of rare exotic trees and flowers",
      "Botanical tree walk, Rose garden photography, Annual fruit show viewing, Leisure stroll",
      "Garden, Leisure, Photography", "Year-round", "Budget", 1)
    s("Dolphin's Nose & Catherine Falls Viewpoint", "Nilgiris", "Tamil Nadu", "Mountain/Hill",
      "Prominent rock promontory in Coonoor offering breathtaking vistas of Catherine Falls plummeting 250 ft across the gorge",
      "Gorge viewpoint photography, Catherine Falls observation, Tea garden walking, St. Catherine tea tasting",
      "Scenic, Mountain, Photography", "September to May", "Budget", 1)
    s("Kodanad Viewpoint Kotagiri", "Nilgiris", "Tamil Nadu", "Mountain/Hill",
      "Spectacular edge-of-the-world viewpoint overlooking the Moyar River gorge, Bhavanisagar dam and Mysore plateau",
      "Valley canyon viewing, Tea estate trails, Sunset watching, Nature photography",
      "Mountain, Scenic, Eco", "October to May", "Budget", 1)
    s("Mukurthi National Park", "Nilgiris", "Tamil Nadu", "Wildlife",
      "High-altitude UNESCO protected montane grassland and shola forest designated specifically to protect the Nilgiri Tahr",
      "Trekking trails, Nilgiri tahr spotting, Endemic birdwatching, Alpine grassland photography",
      "Eco, Wildlife, Trekking", "November to April", "Moderate", 2)

    # Dindigul (Kodaikanal)
    s("Coaker's Walk & Bryant Park", "Dindigul", "Tamil Nadu", "Garden/Nature",
      "One-kilometer mountain promenade built along the edge of steep slopes offering views of Pambar Valley and dolphin's nose",
      "Cliff edge walking, Telescope observation, Flower show viewing in Bryant Park, Cycling",
      "Leisure, Scenic, Walking", "September to May", "Budget", 1)
    s("Pillar Rocks & Guna Caves", "Dindigul", "Tamil Nadu", "Mountain/Hill",
      "Three giant granite rock boulders standing 400 ft tall alongside mysterious deep cavern chasms (Devil's Kitchen)",
      "Pillar rocks viewing, Cloud watching, Cave overlook walking, Photography",
      "Mountain, Scenic, Adventure", "September to May", "Budget", 1)
    s("Berijam Lake & Pine Forest", "Dindigul", "Tamil Nadu", "Lake/Water",
      "Pristine reservoir nestled inside protected forest reserve surrounded by towering fragrant pine groves",
      "Forest permit safari, Pine grove photography, Bird watching, Quiet contemplation",
      "Eco, Nature, Photography", "September to May", "Moderate", 1)
    s("Mannavanur Lake & Sheep Farm", "Dindigul", "Tamil Nadu", "Lake/Water",
      "Picturesque high-altitude grassland valley with an emerald lake and central sheep breeding research station",
      "Coracle boating, Rolling meadows walk, Sheep petting, Scenic photography",
      "Eco, Leisure, Rural", "September to May", "Moderate", 1)
    s("Silver Cascade & Vattakanal Falls", "Dindigul", "Tamil Nadu", "Waterfall",
      "Twin waterfalls tumbling over steep rocks, with Vattakanal renowned as the Little Israel bohemian hub",
      "Waterfall photography, Cafe hopping in Vattakanal, Dolphin nose trekking, Cliff sunset",
      "Waterfall, Youth, Adventure", "July to February", "Budget", 1)
    s("Dindigul Rock Fort", "Dindigul", "Tamil Nadu", "Heritage",
      "Imposing 17th-century rock-cut fortress built atop a 280-meter monolithic rock by Nayak kings, later fortified by Hyder Ali",
      "Rock fort stairs climb, Cannon battery study, Panoramic city view, Sunset photography",
      "Heritage, History, Architecture", "October to March", "Budget", 1)

    # Madurai & Theni & Virudhunagar
    s("Thirumalai Nayakkar Mahal", "Madurai", "Tamil Nadu", "Heritage",
      "Palatial 1636 CE Indo-Saracenic royal residence famous for its massive whitewashed pillars and grand celestial pavilion",
      "Palace pillar walk, Sound and light show viewing, Royal courtyard photography, History study",
      "Heritage, Architecture, Photography", "October to March", "Budget", 1)
    s("Alagar Koyil & Pazhamudircholai", "Madurai", "Tamil Nadu", "Temple/Religious",
      "Hilltop Vishnu temple and one of the six sacred abodes (Arupadai Veedu) of Lord Murugan amidst Alagar Hills",
      "Temple worship, Hill monkey feeding, Natural spring bath at Rakkayi temple, Heritage walk",
      "Spiritual, Nature, Mountain", "Year-round", "Budget", 1)
    s("Samanar Hills Rock Cut Jain Caves", "Madurai", "Tamil Nadu", "Heritage",
      "Ancient hill complex with 2,000-year-old rock-cut Jain carvings, stone beds, natural springs and Brahmi inscriptions",
      "Hillock climb, Jain rock carving study, Ancient inscription reading, Sunset viewing",
      "Heritage, Archaeological, Trekking", "October to March", "Budget", 1)
    s("Vandiyur Mariamman Teppakulam", "Madurai", "Tamil Nadu", "Lake/Water",
      "Enormous temple water tank with a central mandapam built in 1645 connected to the Vaigai River via underground channels",
      "Tank perimeter walk, Float festival viewing, Maiya Mandapam photography, Evening leisure",
      "Cultural, Leisure, Photography", "October to March", "Budget", 1)
    s("Meghamalai Highwavys Cloud Mountain", "Theni", "Tamil Nadu", "Mountain/Hill",
      "Mist-clad Western Ghats hill range celebrated for cardamom estates, wild elephants and Highwavys Dam lake",
      "Tea estate safari, Highwavys dam boating, Elephant spotting, Misty viewpoint photography",
      "Eco, Offbeat, Mountain", "September to May", "Moderate", 2)
    s("Suruli Falls Theni", "Theni", "Tamil Nadu", "Waterfall",
      "Two-tiered waterfall cascading down from Meghamalai hills mentioned in the ancient epic Silappadikaram",
      "Waterfall bath, Forest walk, Cave shrine visit, Photography",
      "Waterfall, Nature, Spiritual", "June to December", "Budget", 1)
    s("Kumbakkarai Falls", "Theni", "Tamil Nadu", "Waterfall",
      "Scenic waterfall on the foothills of Kodaikanal hills flowing through natural rock cavities before falling into pools",
      "Rock pool swimming, Cascade shower, Picnic under forest canopy, Photography",
      "Nature, Leisure, Waterfall", "July to January", "Budget", 1)
    s("Kurangani Hills & Top Station Trek", "Theni", "Tamil Nadu", "Adventure",
      "Challenging mountain trek through coffee plantations and pine forests connecting Bodinayakanur to Top Station",
      "Mountain trekking, Campfire camping, Cloud valley sunrise, 4x4 jeep safari",
      "Adventure, Trekking, Camping", "September to April", "Moderate", 2)
    s("Ayyanar Falls Rajapalayam", "Virudhunagar", "Tamil Nadu", "Waterfall",
      "Picturesque forest cascade nestled in the Eastern slopes of Western Ghats worshipped alongside forest deity Ayyanar",
      "Forest stream trek, Temple prayer, Natural waterfall shower, Wildlife spotting",
      "Eco, Nature, Spiritual", "September to January", "Budget", 1)

    # Thanjavur & Tiruvarur & Mayiladuthurai & Nagapattinam
    s("Thanjavur Maratha Palace & Saraswathi Mahal Library", "Thanjavur", "Tamil Nadu", "Heritage",
      "Official residence of Thanjavur Nayak and Maratha rulers housing medieval manuscripts, royal regalia and art",
      "Rare palm-leaf manuscript viewing, Royal court walk, Bell tower ascent, Chola bronze study",
      "Heritage, Educational, Art", "October to March", "Budget", 1)
    s("Punnai Nallur Mariamman Temple", "Thanjavur", "Tamil Nadu", "Temple/Religious",
      "Sacred 17th-century temple built by Maratha ruler Venkoji where the idol is made of natural ant-hill mud (puttu)",
      "Temple darshan, Traditional puja, Ghee lamp lighting, Cultural exploration",
      "Spiritual, Cultural, Heritage", "Year-round", "Budget", 1)
    s("Thyagaraja Temple Tiruvarur", "Tiruvarur", "Tamil Nadu", "Temple/Religious",
      "Massive ancient Shiva temple complex famous for Kamalalayam, one of the largest temple tanks in India, and giant chariot",
      "Kamalalayam tank walk, Chariot (Aazhi Ther) study, Carnatic music pilgrimage, Darshan",
      "Spiritual, Cultural, Architecture", "October to March", "Budget", 1)
    s("Muthupet Mangrove Forest", "Tiruvarur", "Tamil Nadu", "Wildlife",
      "Sprawling lagoon and mangrove ecosystem along the Palk Strait featuring wooden walkways and migratory birds",
      "Mangrove boat cruise, Wooden walkway exploration, Flamingo birdwatching, Photography",
      "Eco, Nature, Boating", "November to February", "Moderate", 1)
    s("Mayuranathaswamy Temple", "Mayiladuthurai", "Tamil Nadu", "Temple/Religious",
      "Ancient temple where Goddess Parvati worshipped Lord Shiva in the form of a peahen (Mayura)",
      "Temple worship, Cauvery river thula snanam bath, Gopuram photography",
      "Spiritual, Heritage, Culture", "Year-round", "Budget", 1)
    s("Tharangambadi Danish Fort Tranquebar", "Mayiladuthurai", "Tamil Nadu", "Heritage",
      "Charming coastal Danish colony established in 1620 featuring Fort Dansborg, ozone-rich breeze and colonial bungalows",
      "Danish fort exploration, Sea breeze walk, Zion Church visit, Colonial museum study",
      "Heritage, Beach, Relaxing", "October to March", "Moderate", 1)
    s("Poompuhar Ancient Port & Beach", "Mayiladuthurai", "Tamil Nadu", "Heritage",
      "Legendary submerged Chola capital and maritime port city featured in Silappadikaram with a modern monument gallery",
      "Silappadikaram art gallery walk, Beach walk, Cauvery confluence viewing, Archaeology study",
      "Heritage, Beach, Cultural", "October to March", "Budget", 1)
    s("Velankanni Basilica of Our Lady of Good Health", "Nagapattinam", "Nagapattinam", "Temple/Religious",
      "Lourdes of the East - world-famous Catholic pilgrimage shrine situated directly on the Coromandel coast",
      "Basilica prayer, Offerings of miniature silver replicas, Seaside walk, Museum visit",
      "Spiritual, Cultural, Seaside", "Year-round", "Budget", 1)
    s("Nagore Dargah Shrine", "Nagapattinam", "Tamil Nadu", "Temple/Religious",
      "500-year-old Sufi saint shrine with five ornate minarets visited by people of all faiths",
      "Dargah visit, Evening qawwali listening, Holy pond prayer, Cultural harmony walk",
      "Spiritual, Cultural, Music", "Year-round", "Budget", 1)
    s("Point Calimere Wildlife & Bird Sanctuary", "Nagapattinam", "Tamil Nadu", "Wildlife",
      "Historic coastal headland and wetland sanctuary sheltering greater flamingos, blackbucks and sea turtles",
      "Flamingo birdwatching, Blackbuck safari, Lighthouse walk, Chola heritage ruins",
      "Wildlife, Eco, Birding", "November to March", "Budget", 1)

    # Tiruchirappalli & Pudukkottai & Ariyalur & Perambalur
    s("Rockfort Ucchi Pillayar Temple", "Tiruchirappalli", "Tamil Nadu", "Heritage",
      "Dramatic 7th-century temple carved atop a 273-foot ancient rock older than the Greenland ice cap, accessible by 437 steps",
      "437-step rock climb, Panoramic city views of Trichy and Kaveri River, Sunset watching",
      "Heritage, Spiritual, Panoramic", "October to March", "Budget", 1)
    s("Ranganathaswamy Temple Srirangam", "Tiruchirappalli", "Tamil Nadu", "Temple/Religious",
      "Largest functioning Hindu temple complex in the world spanning 156 acres with 21 magnificent gopurams",
      "Rajagopuram viewing, Vaikunta Ekadasi path walk, Ancient inscriptions study, Temple darshan",
      "Spiritual, Architecture, Heritage", "October to March", "Budget", 1)
    s("Jambukeshwarar Temple Thiruvanaikaval", "Tiruchirappalli", "Tamil Nadu", "Temple/Religious",
      "Pancha Bhoota Stalam representing the Water element (Appu Lingam) with an underground spring bubbling under the idol",
      "Underground spring viewing, Elephant blessings, Temple darshan, Stone carving study",
      "Spiritual, Cultural, Ancient", "Year-round", "Budget", 1)
    s("Kallanai Grand Anicut Dam", "Tiruchirappalli", "Tamil Nadu", "Heritage",
      "One of the world's oldest active water-diversion dams built by Chola King Karikalan in the 2nd century CE",
      "Ancient dam architecture study, Kaveri river breeze, Garden walk, History photography",
      "Heritage, Engineering, Leisure", "October to February", "Budget", 1)
    s("Sittannavasal Cave Rock Cut Jain Monuments", "Pudukkottai", "Tamil Nadu", "Heritage",
      "2nd-century Jain rock-cut monastery renowned for ancient fresco murals painted with vegetable dyes and musical pillars",
      "Ancient fresco painting study, Jain rock-bed exploration, Echo cavern demonstration, Hill climb",
      "Archaeology, Heritage, Art", "October to March", "Budget", 1)
    s("Thirumayam Fort & Rock Cut Temples", "Pudukkottai", "Tamil Nadu", "Heritage",
      "17th-century ring fort built by the Raja of Ramnad housing rock-cut Vaishnavite and Saivite shrines",
      "Ring wall fortress walk, Rock-cut cave darshan, Cannon viewing, Sunset photography",
      "Heritage, Architecture, History", "October to March", "Budget", 1)
    s("Gangaikonda Cholapuram Brihadisvara Temple", "Ariyalur", "Tamil Nadu", "Heritage",
      "UNESCO World Heritage masterpiece built by Rajendra Chola I featuring a graceful feminine curved vimana tower",
      "Chola sculpture photography, Stone lion well study, Temple lawn walk, Inscription reading",
      "Heritage, UNESCO, Architecture", "October to March", "Budget", 1)
    s("Ranjankudi Fort", "Perambalur", "Tamil Nadu", "Heritage",
      "17th-century granite fort constructed by the Nawab of the Carnatic, site of the historic Battle of Valikondapuram",
      "Granite rampart exploration, Bastion photography, Battlefield history study",
      "Heritage, History, Architecture", "October to March", "Budget", 1)

    # Tirunelveli & Tenkasi & Thoothukudi & Kanyakumari
    s("Nellaiappar Temple & Musical Pillars", "Tirunelveli", "Tamil Nadu", "Temple/Religious",
      "Massive ancient Shiva temple complex spanning 14 acres famous for musical stone pillars and the Tamra Sabha copper hall",
      "Tapping musical pillars, Tamra Sabha inspection, Golden chariot darshan, Halwa tasting in car street",
      "Spiritual, Cultural, Music", "October to March", "Budget", 1)
    s("Manimuthar Waterfalls and Dam", "Tirunelveli", "Tamil Nadu", "Waterfall",
      "Spectacular natural cascade tumbling into a 90-foot deep natural pool nestled inside dense reserve forest",
      "Waterfall pool bathing, Dam garden walk, Forest drive, Scenic photography",
      "Nature, Waterfall, Leisure", "October to February", "Budget", 1)
    s("Papanasam Agasthiyar Falls", "Tirunelveli", "Tamil Nadu", "Waterfall",
      "Sacred perennial waterfall on the Thamirabarani River where sage Agastya was blessed with the divine wedding vision",
      "Sacred river bath, Agastya temple darshan, Forest monkey watching, Photography",
      "Spiritual, Waterfall, Nature", "Year-round", "Budget", 1)
    s("Manjolai Tea Estate & Kakkachi", "Tirunelveli", "Tamil Nadu", "Mountain/Hill",
      "Misty hilltop tea paradise situated at 4,000 ft inside Kalakkad Mundanthurai Tiger Reserve overlooking reservoirs",
      "Tea garden walks, Viewpoint photography, Mountain drive, Jungle climate experience",
      "Eco, Mountain, Offbeat", "October to March", "Moderate", 1)
    s("Courtallam Main & Five Falls", "Tenkasi", "Tamil Nadu", "Waterfall",
      "Famous Spa of South India where mountain streams flow through dense herbal forests providing natural therapeutic showers",
      "Herbal waterfall bath, Oil massage, Local fruit market shopping, Tenkasi Kasi Viswanathar temple visit",
      "Wellness, Nature, Waterfall", "June to October", "Budget", 1)
    s("Kulasekaranpattinam Mutharamman Temple", "Thoothukudi", "Tamil Nadu", "Temple/Religious",
      "Famous coastal shrine celebrated for the 10-day grand Dussehra festival where devotees dress as deities and spirits",
      "Coastal temple worship, Dussehra trance festival viewing, Beach sunset, Local culture",
      "Spiritual, Culture, Photography", "October to March", "Budget", 1)
    s("Hare Island & V.O.C. Port Beach", "Thoothukudi", "Tamil Nadu", "Beach",
      "Scenic island spit and harbor beach offering views of giant merchant vessels, pearl fisheries and sunset walks",
      "Harbor walk, Macroon sweet tasting, Sea view photography, Fishing harbor visit",
      "Beach, Maritime, Food", "October to March", "Budget", 1)
    s("Padmanabhapuram Palace", "Kanyakumari", "Tamil Nadu", "Heritage",
      "Magnificent 16th-century wooden palace of the Travancore Maharajas featuring intricate rosewood ceilings and Belgian mirrors",
      "Wooden architecture tour, King's council chamber, Secret underground passage, Floral wood ceilings",
      "Heritage, Architecture, Art", "Year-round", "Moderate", 1)
    s("Mathur Hanging Aqueduct", "Kanyakumari", "Tamil Nadu", "Heritage",
      "One of the longest and highest trough aqueducts in Asia spanning 1,240 ft across the Pahrali River on 28 concrete pillars",
      "Aqueduct catwalk crossing, Forest canopy viewing, River photography, Rural landscape soak",
      "Engineering, Scenic, Photography", "Year-round", "Budget", 1)
    s("Thirparappu Waterfalls", "Kanyakumari", "Tamil Nadu", "Waterfall",
      "Broad 300-foot waterfall cascading over rocky beds into Kodayar River adjacent to an ancient Shiva shrine",
      "Waterfall shower, Children's water park, Pedalo boating, Temple prayer",
      "Waterfall, Leisure, Family", "June to January", "Budget", 1)
    s("Vattakottai Fort Seaside Ramparts", "Kanyakumari", "Tamil Nadu", "Heritage",
      "Historic 18th-century seaside granite fort built by Captain De Lannoy offering sweeping views of the Arabian Sea and Ghats",
      "Coastal rampart walking, Black sand beach stroll, Sea horizon photography, Wind farm viewing",
      "Heritage, Beach, Photography", "October to March", "Budget", 1)
    s("Chitharal Jain Rock Cut Monuments", "Kanyakumari", "Tamil Nadu", "Heritage",
      "9th-century Digambara Jain rock-cut cave and sculpted bas-relief figures carved atop a scenic granite hillock",
      "Granite hill trek, Jain bas-relief study, Panoramic view of coconut groves, Sunset watching",
      "Heritage, Archaeology, Trekking", "October to March", "Budget", 1)
    s("Muttom Lighthouse & Beach", "Kanyakumari", "Tamil Nadu", "Beach",
      "Picturesque fishing village with a 100-year-old British lighthouse, rocky cliff shores and surging surf",
      "Lighthouse climb, Rocky cliff photography, Sunset viewing, Seaside sea-spray soak",
      "Beach, Photography, Scenic", "October to March", "Budget", 1)

    return spots

print(f"Loaded India module.")
