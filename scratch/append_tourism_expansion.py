import csv
import sys
from pathlib import Path

# The 402 expansion records provided directly by the user:
expansion_csv_text = """Name of the Place,District,Famous_For,Activities,State,Country,Category,Travel_Style,Best_Season,Budget_Category,Duration_Days
Buenos Aires Historic Center,Buenos Aires,"grand avenues, plazas and historic architecture","Walking tours, architecture, cultural experiences",Buenos Aires,Argentina,Heritage,"Cultural, Photography","March to May, September to November",Moderate,2
Bariloche,Río Negro,"Andean lakes, forests and mountain scenery","Hiking, boating, photography, winter sports",Río Negro,Argentina,Mountain/Hill,"Adventure, Eco, Photography",December to March,Premium,3
Lake Sevan,Gegharkunik,high-altitude lake and lakeside monasteries,"Lake sightseeing, boating, photography",Gegharkunik,Armenia,Lake/Water,"Leisure, Eco, Photography",June to September,Budget,1
Cascade Complex,Yerevan,monumental stairway and contemporary art complex,"City views, art viewing, photography",Yerevan,Armenia,Heritage,"Cultural, Photography",May to October,Budget,1
Uluru-Kata Tjuta National Park,Northern Territory,iconic sandstone monolith and desert cultural landscape,"Guided walks, sunrise viewing, photography",Northern Territory,Australia,Mountain/Hill,"Cultural, Eco, Photography",May to September,Premium,2
Salzburg Old Town,Salzburg,baroque historic centre and Mozart heritage,"Walking tour, museums, architecture photography",Salzburg,Austria,Heritage,"Cultural, Photography",April to October,Premium,2
Hallstatt,Upper Austria,lakeside Alpine village and historic salt-mining region,"Village walk, lake views, photography",Upper Austria,Austria,Mountain/Hill,"Leisure, Photography",April to October,Premium,1
Schönbrunn Palace,Vienna,former imperial summer palace and gardens,"Palace tour, garden walk, photography",Vienna,Austria,Heritage,"Cultural, Photography",April to October,Premium,1
Atomium,Brussels,iconic modernist landmark shaped like an iron crystal,"Observation decks, architecture photography, city sightseeing",Brussels,Belgium,Heritage,"Family, Photography",April to October,Moderate,1
"Grand Place, Brussels",Brussels,historic central square with ornate guildhall architecture,"City walk, architecture photography, food tourism",Brussels,Belgium,Heritage,"Cultural, Photography",April to October,Moderate,1
Bruges Historic Centre,West Flanders,medieval canals and preserved old-town architecture,"Canal cruise, walking tour, photography",West Flanders,Belgium,Heritage,"Cultural, Leisure, Photography",April to October,Premium,2
Tiger’s Nest Monastery,Paro,clifftop Buddhist monastery and national symbol,"Hiking, monastery visit, photography",Paro,Bhutan,Temple/Religious,"Spiritual, Adventure, Photography","March to May, September to November",Premium,1
Dochula Pass,Thimphu District,mountain pass with Himalayan panoramas and chortens,"Viewpoint stop, photography, scenic drive",Thimphu District,Bhutan,Mountain/Hill,"Eco, Photography",October to April,Premium,1
"Iguazu Falls, Brazil",Parana,massive waterfall system on the Iguazu River,"Boardwalks, boat safari, photography",Parana,Brazil,Waterfall,"Adventure, Eco, Photography","March to May, August to October",Premium,2
Christ the Redeemer,Rio de Janeiro,Art Deco statue overlooking Rio de Janeiro,"Viewpoint visit, city sightseeing, photography",Rio de Janeiro,Brazil,Heritage,"Cultural, Photography",April to September,Premium,1
Sugarloaf Mountain,Rio de Janeiro,granite peak with cable-car city and harbor views,"Cable-car ride, viewpoints, photography",Rio de Janeiro,Brazil,Mountain/Hill,"Adventure, Leisure, Photography",April to September,Premium,1
Bayon Temple,Siem Reap,temple known for monumental carved faces,"Temple tour, archaeology, photography",Siem Reap,Cambodia,Heritage,"Cultural, Photography",November to February,Moderate,1
Ta Prohm,Siem Reap,ruined temple entwined with mature trees,"Archaeology, photography, heritage walk",Siem Reap,Cambodia,Heritage,"Cultural, Photography",November to February,Moderate,1
CN Tower,Ontario,iconic observation tower overlooking Toronto,"Observation deck, city sightseeing, photography",Ontario,Canada,Heritage,"Leisure, Photography",Year-round,Premium,1
Niagara Falls,Ontario,major waterfall system on the Canada-US border,"Boat cruise, viewpoints, photography",Ontario,Canada,Waterfall,"Family, Adventure, Photography",May to October,Premium,2
Rapa Nui National Park,Easter Island,Polynesian archaeological landscape with moai,"Archaeology, hiking, cultural tourism, photography",Easter Island,Chile,Heritage,"Cultural, Adventure, Photography",Year-round,Premium,3
Forbidden City,Beijing,imperial palace complex and museum,"Museum visit, architecture photography, history tour",Beijing,China,Heritage,"Cultural, Photography","April to May, September to October",Moderate,1
Great Wall of China,Beijing / Hebei,historic fortification crossing northern China,"Hiking, heritage sightseeing, photography",Beijing / Hebei,China,Heritage,"Adventure, Cultural, Photography","April to May, September to October",Premium,2
Terracotta Army,Shaanxi,archaeological army of life-sized Qin sculptures,"Museum visit, archaeology, photography",Shaanxi,China,Heritage,"Cultural, Photography","March to May, September to November",Moderate,1
Cartagena Old Town,Bolivar,walled colonial city on the Caribbean coast,"Walking tour, architecture photography, food tourism",Bolivar,Colombia,Heritage,"Cultural, Leisure, Photography",December to March,Premium,2
Cocora Valley,Quindío,Andean valley famous for giant wax palms,"Hiking, horseback riding, photography",Quindío,Colombia,Mountain/Hill,"Adventure, Eco, Photography",December to February,Moderate,1
Dubrovnik Old Town,Dubrovnik-Neretva,walled Adriatic city with medieval streets,"City walls, walking tour, photography",Dubrovnik-Neretva,Croatia,Heritage,"Cultural, Photography",April to October,Premium,2
Diocletian’s Palace,Split-Dalmatia,Roman imperial palace embedded in Split’s old town,"Heritage walk, architecture photography, food tourism",Split-Dalmatia,Croatia,Heritage,"Cultural, Photography",April to October,Moderate,1
Charles Bridge,Prague,iconic historic bridge lined with statues,"Walking tour, sunrise photography, city sightseeing",Prague,Czech Republic,Heritage,"Cultural, Photography",April to October,Budget,1
Prague Castle,Prague,large historic castle complex overlooking the Vltava,"Castle tour, architecture photography, city views",Prague,Czech Republic,Heritage,"Cultural, Photography",April to October,Moderate,1
Český Krumlov,South Bohemia,preserved medieval town around a winding river,"Old-town walk, castle visit, photography",South Bohemia,Czech Republic,Heritage,"Cultural, Photography",April to October,Moderate,1
Nyhavn,Copenhagen,colorful historic waterfront district,"Canal walk, dining, photography",Copenhagen,Denmark,Heritage,"Cultural, Leisure, Photography",May to September,Premium,1
Tivoli Gardens,Copenhagen,historic amusement park in central Copenhagen,"Rides, gardens, family recreation",Copenhagen,Denmark,Theme Park,"Family, Leisure, Photography",April to September,Premium,1
Kronborg Castle,Helsingør,Renaissance castle linked to Hamlet tradition,"Castle tour, history walk, photography",Helsingør,Denmark,Heritage,"Cultural, Photography",April to October,Moderate,1
Karnak Temple,Luxor,vast ancient Egyptian temple complex,"Archaeology, guided tour, photography",Luxor,Egypt,Heritage,"Cultural, Photography",October to April,Moderate,1
Danakil Depression,Afar,extreme volcanic desert landscape,"Desert expedition, geothermal sightseeing, photography",Afar,Ethiopia,Mountain/Hill,"Adventure, Photography",November to February,Luxury,2
Rock-Hewn Churches of Lalibela,Amhara,monolithic medieval churches carved from rock,"Heritage walk, pilgrimage, photography",Amhara,Ethiopia,Heritage,"Spiritual, Cultural, Photography",October to March,Moderate,2
Taveuni,Northern Division,lush volcanic island known for forests and waterfalls,"Trekking, diving, waterfall visits, photography",Northern Division,Fiji,Island,"Eco, Adventure, Photography",May to October,Premium,3
Mamanuca Islands,Western Division,tropical island group with reefs and beaches,"Snorkeling, diving, boat trips, beach leisure",Western Division,Fiji,Island,"Beach, Island, Photography",May to October,Premium,3
Nadi,Western Division,"gateway city with markets, temples and resort access","City sightseeing, market visits, photography",Western Division,Fiji,Sightseeing,"Cultural, Leisure, Photography",May to October,Moderate,1
Suomenlinna,Helsinki,maritime fortress spread across islands,"Ferry ride, fort walk, museums, photography",Helsinki,Finland,Heritage,"Cultural, Photography",May to September,Moderate,1
Rovaniemi,Lapland,Arctic gateway and Santa Claus destination,"Northern-lights tours, reindeer experiences, photography",Lapland,Finland,Sightseeing,"Family, Adventure, Photography",December to March,Premium,2
Nuuksio National Park,Uusimaa,forest and lake landscape near Helsinki,"Hiking, canoeing, nature photography",Uusimaa,Finland,Eco Tourism,"Eco, Adventure, Photography",May to September,Moderate,1
Louvre Museum,Paris,one of the world’s major art museums,"Museum visit, art appreciation, architecture photography",Paris,France,Heritage,"Cultural, Photography",Year-round,Premium,1
Gergeti Trinity Church,Mtskheta-Mtianeti,mountaintop church below Mount Kazbek,"Scenic drive, hiking, photography",Mtskheta-Mtianeti,Georgia,Temple/Religious,"Spiritual, Adventure, Photography",May to October,Moderate,1
Uplistsikhe,Shida Kartli,ancient rock-hewn town carved into cliffs,"Archaeology, cave exploration, photography",Shida Kartli,Georgia,Cave/Geological,"Cultural, Adventure, Photography",May to October,Moderate,1
Brandenburg Gate,Berlin,neoclassical landmark in central Berlin,"City sightseeing, photography, history tour",Berlin,Germany,Heritage,"Cultural, Photography",April to October,Moderate,1
Santorini,South Aegean,volcanic island famous for caldera villages and sunsets,"Boat trips, village walks, photography",South Aegean,Greece,Island,"Leisure, Beach, Photography",April to October,Luxury,3
Meteora,Thessaly,Orthodox monasteries built on dramatic rock pillars,"Monastery visits, hiking, photography",Thessaly,Greece,Heritage,"Spiritual, Cultural, Photography",April to October,Moderate,2
Buda Castle,Budapest,historic castle district above the Danube,"Castle district walk, museums, photography",Budapest,Hungary,Heritage,"Cultural, Photography",April to October,Moderate,1
Hungarian Parliament Building,Budapest,iconic riverside Neo-Gothic parliament,"Guided tour, riverfront photography, architecture",Budapest,Hungary,Heritage,"Cultural, Photography",April to October,Moderate,1
Lake Balaton,Transdanubia,Central Europe’s large freshwater leisure lake,"Swimming, cycling, boating, photography",Transdanubia,Hungary,Lake/Water,"Leisure, Family, Photography",May to September,Moderate,2
Blue Lagoon,Reykjanes,geothermal spa in a lava-field setting,"Geothermal bathing, wellness, photography",Reykjanes,Iceland,Eco Tourism,"Wellness, Leisure, Photography",Year-round,Premium,1
Golden Circle,South Iceland,route linking major geothermal and waterfall landscapes,"Road trip, nature viewing, photography",South Iceland,Iceland,Sightseeing,"Adventure, Eco, Photography",June to September,Premium,1
Jökulsárlón Glacier Lagoon,South Iceland,glacial lagoon with floating icebergs,"Boat tour, photography, wildlife viewing",South Iceland,Iceland,Lake/Water,"Adventure, Eco, Photography",May to September,Premium,1
"Bharatpur Beach, Neil Island",Neil Island,clear-water beach known for reef scenery,"Snorkeling, beach walks, photography",Andaman and Nicobar Islands,India,Beach,"Beach, Leisure, Photography",October to May,Budget,1
Baratang Island,Regional destination,"mangroves, limestone caves and unique island ecology","Boat safari, cave exploration, photography",Andaman and Nicobar Islands,India,Cave/Geological,"Eco, Adventure, Photography",October to May,Budget,2
North Bay Island,Regional destination,popular island for coral and marine experiences,"Snorkeling, glass-bottom boat, photography",Andaman and Nicobar Islands,India,Island,"Island, Leisure, Photography",October to May,Budget,2
Radhanagar-style Neil coastal circuit,Regional destination,white-sand island shoreline and tropical scenery,"Beach relaxation, sunset photography, swimming",Andaman and Nicobar Islands,India,Beach,"Beach, Leisure, Photography",October to May,Budget,1
Ross Island,Regional destination,former colonial administrative settlement with historic ruins,"Heritage walk, boat trip, photography",Andaman and Nicobar Islands,India,Heritage,"Cultural, Photography",October to May,Moderate,1
Srisailam,Nandyal,major pilgrimage destination surrounded by Nallamala hills,"Pilgrimage, temple visit, nature sightseeing",Andhra Pradesh,India,Temple/Religious,"Spiritual, Cultural, Photography",October to March,Moderate,1
Amaravati Stupa,Palnadu,ancient Buddhist archaeological site on the Krishna River,"Heritage tour, archaeology, photography",Andhra Pradesh,India,Heritage,"Cultural, Photography",October to March,Moderate,1
Lepakshi Temple,Sri Sathya Sai,historic temple complex renowned for Vijayanagara architecture,"Temple visit, architecture photography, heritage walk",Andhra Pradesh,India,Temple/Religious,"Spiritual, Cultural, Photography",October to March,Moderate,1
Namdapha National Park,Changlang,large Eastern Himalayan protected forest and wildlife area,"Wildlife trekking, birdwatching, nature photography",Arunachal Pradesh,India,Wildlife,"Eco, Adventure, Photography","March to June, October to November",Moderate,2
Ziro Valley,Lower Subansiri,green valley known for landscapes and Apatani culture,"Village tourism, hiking, cultural experiences, photography",Arunachal Pradesh,India,Mountain/Hill,"Eco, Adventure, Photography","March to June, October to November",Moderate,2
Bum La Pass,Tawang,high-altitude Himalayan border pass near Tawang,"Mountain sightseeing, photography, snow viewing",Arunachal Pradesh,India,Mountain/Hill,"Eco, Adventure, Photography","March to June, October to November",Moderate,2
Sela Pass,Tawang,high-altitude mountain pass and alpine lake landscape,"Scenic drive, photography, snow viewing",Arunachal Pradesh,India,Mountain/Hill,"Eco, Adventure, Photography","March to June, October to November",Moderate,2
Kamakhya Temple,Guwahati,major Shakti pilgrimage shrine on Nilachal Hill,"Temple visit, pilgrimage, cultural photography",Assam,India,Temple/Religious,"Spiritual, Cultural, Photography",October to April,Moderate,1
Umananda Island,Guwahati,small Brahmaputra river island with temple heritage,"Boat trip, temple visit, photography",Assam,India,Island,"Island, Leisure, Photography",October to April,Budget,2
Majuli Island,Majuli,river island known for Vaishnavite culture and satras,"Village tourism, satra visits, cycling, photography",Assam,India,Island,"Island, Leisure, Photography",October to April,Budget,2
Pobitora Wildlife Sanctuary,Morigaon,wildlife reserve noted for Indian rhinoceros,"Jeep safari, birdwatching, wildlife photography",Assam,India,Wildlife,"Eco, Adventure, Photography",October to April,Moderate,2
Sivasagar Sivadol,Sivasagar,historic Ahom-era temple complex,"Heritage visit, temple sightseeing, photography",Assam,India,Temple/Religious,"Spiritual, Cultural, Photography",October to April,Moderate,1
Mahabodhi Temple Complex,Regional destination,major Buddhist pilgrimage site at Bodh Gaya,"Pilgrimage, meditation, heritage photography",Bihar,India,Temple/Religious,"Spiritual, Cultural, Photography",October to March,Moderate,1
Nalanda Mahavihara,Regional destination,archaeological remains of the ancient Buddhist university,"Archaeology, museum visit, photography",Bihar,India,Heritage,"Cultural, Photography",October to March,Moderate,1
Rajgir,Regional destination,historic hill town associated with Buddhist and Jain traditions,"Heritage sightseeing, ropeway ride, photography",Bihar,India,Heritage,"Cultural, Photography",October to March,Moderate,1
Valmiki National Park,Regional destination,Bihar’s major forest and wildlife destination,"Wildlife safari, birdwatching, nature photography",Bihar,India,Wildlife,"Eco, Adventure, Photography",October to March,Moderate,2
Vikramshila Archaeological Site,Regional destination,ruins of a major medieval Buddhist learning centre,"Archaeology, history tour, photography",Bihar,India,Heritage,"Cultural, Photography",October to March,Moderate,1
Capitol Complex,Regional destination,modernist civic architecture complex by Le Corbusier,"Architecture tour, photography, city sightseeing",Chandigarh,India,Heritage,"Cultural, Photography",October to March,Moderate,1
Leisure Valley,Regional destination,green urban park corridor through Chandigarh,"Walking, cycling, photography, recreation",Chandigarh,India,Garden/Nature,"Leisure, Photography",October to March,Budget,1
Rock Garden of Chandigarh,Regional destination,sculpture garden built from recycled materials,"Garden walk, sculpture viewing, photography",Chandigarh,India,Garden/Nature,"Leisure, Photography",October to March,Budget,1
Sukhna Lake,Regional destination,major urban lake and recreation zone,"Boating, walking, cycling, photography",Chandigarh,India,Lake/Water,"Leisure, Photography",October to March,Budget,1
Zakir Hussain Rose Garden,Regional destination,large landscaped rose garden in the city,"Garden walk, photography, family outing",Chandigarh,India,Garden/Nature,"Leisure, Photography",October to March,Budget,1
Barnawapara Wildlife Sanctuary,Regional destination,forest sanctuary known for wildlife and birdlife,"Safari, birdwatching, nature photography",Chhattisgarh,India,Wildlife,"Eco, Adventure, Photography",October to February,Moderate,2
Kanger Valley National Park,Regional destination,biodiversity-rich forest with caves and waterfalls,"Wildlife trekking, cave exploration, photography",Chhattisgarh,India,Wildlife,"Eco, Adventure, Photography",October to February,Moderate,2
Sirpur,Regional destination,archaeological and cultural heritage town with ancient temples,"Archaeology, temple visits, photography",Chhattisgarh,India,Heritage,"Cultural, Photography",October to February,Moderate,1
Tirathgarh Falls,Regional destination,multi-tier waterfall in Kanger Valley landscape,"Nature walk, waterfall viewing, photography",Chhattisgarh,India,Waterfall,"Eco, Adventure, Photography",October to February,Budget,2
Daman Ganga Riverfront,Regional destination,waterfront recreation area in Silvassa,"Riverfront walks, boating, photography",Dadra and Nagar Haveli and Daman and Diu,India,Lake/Water,"Leisure, Photography",October to March,Budget,1
Devka Beach,Regional destination,popular coastal recreation area in Daman,"Beach walks, sunset viewing, leisure",Dadra and Nagar Haveli and Daman and Diu,India,Beach,"Beach, Leisure, Photography",October to March,Budget,1
Dudhni Lake,Regional destination,reservoir surrounded by forested hills,"Boating, kayaking, nature photography",Dadra and Nagar Haveli and Daman and Diu,India,Lake/Water,"Leisure, Photography",October to March,Budget,1
St. Jerome Fort,Regional destination,historic Portuguese-era fort overlooking the Daman Ganga,"Heritage walk, photography, river views",Dadra and Nagar Haveli and Daman and Diu,India,Heritage,"Cultural, Photography",October to March,Moderate,1
"Tribal Museum, Silvassa",Silvassa,museum documenting tribal culture of the region,"Museum visit, cultural study, photography",Dadra and Nagar Haveli and Daman and Diu,India,Heritage,"Cultural, Photography",October to March,Moderate,1
"Akshardham Temple, Delhi",Delhi,large Hindu temple complex with intricate architecture,"Temple visit, cultural sightseeing, architecture photography",Delhi,India,Temple/Religious,"Spiritual, Cultural, Photography",October to March,Moderate,1
Humayun’s Tomb,New Delhi,Mughal garden-tomb and major architectural landmark,"Heritage walk, garden visit, photography",Delhi,India,Heritage,"Cultural, Photography",October to March,Moderate,1
"National Museum, New Delhi",New Delhi,"major museum of Indian art, history and archaeology","Museum visit, cultural education, photography",Delhi,India,Heritage,"Cultural, Photography",October to March,Moderate,1
Basilica of Bom Jesus,Regional destination,historic church containing the tomb of St. Francis Xavier,"Church visit, heritage walk, architecture photography",Goa,India,Temple/Religious,"Spiritual, Cultural, Photography",November to March,Moderate,1
Se Cathedral,Regional destination,historic church in Old Goa,"Heritage visit, architecture photography, cultural tourism",Goa,India,Temple/Religious,"Spiritual, Cultural, Photography",November to March,Moderate,1
Dwarkadhish Temple,Devbhumi Dwarka,major Krishna temple in the sacred city of Dwarka,"Temple visit, pilgrimage, heritage walk",Gujarat,India,Temple/Religious,"Spiritual, Cultural, Photography",October to March,Moderate,1
White Rann of Kutch,Kutch,vast salt desert landscape famous for seasonal white scenery,"Sunset photography, cultural tourism, desert sightseeing",Gujarat,India,Sightseeing,"Leisure, Photography",October to March,Budget,1
Rani ki Vav,Patan,ornate stepwell and UNESCO World Heritage site,"Heritage walk, architecture photography, archaeology",Gujarat,India,Heritage,"Cultural, Photography",October to March,Moderate,1
"Brahma Sarovar, Kurukshetra",Kurukshetra,large sacred water body and pilgrimage landscape,"Pilgrimage, lakeside walk, photography",Haryana,India,Lake/Water,"Leisure, Photography",October to March,Budget,1
Morni Hills,Regional destination,Haryana’s hill destination with wooded ridges and lakes,"Trekking, boating, photography",Haryana,India,Mountain/Hill,"Eco, Adventure, Photography",October to March,Moderate,2
Pinjore Gardens,Regional destination,historic Mughal-style terraced garden,"Garden walk, photography, family outing",Haryana,India,Garden/Nature,"Leisure, Photography",October to March,Budget,1
Sheikh Chilli’s Tomb,Regional destination,Mughal-period architectural complex in Thanesar,"Heritage walk, architecture photography, history study",Haryana,India,Heritage,"Cultural, Photography",October to March,Moderate,1
Sultanpur National Park,Regional destination,wetland bird sanctuary near Gurugram,"Birdwatching, nature walks, photography",Haryana,India,Wildlife,"Eco, Adventure, Photography",October to March,Moderate,2
"Dal Lake, McLeod Ganj",Kangra,small mountain lake surrounded by deodar forest,"Walks, photography, nearby monastery visits",Himachal Pradesh,India,Lake/Water,"Leisure, Photography","March to June, September to November",Budget,1
Great Himalayan National Park,Kullu,UNESCO-listed alpine wildlife conservation area,"Trekking, birdwatching, wildlife photography",Himachal Pradesh,India,Wildlife,"Eco, Adventure, Photography","March to June, September to November",Moderate,2
Hadimba Devi Temple,Kullu,historic wooden temple set within cedar forest,"Temple visit, heritage photography, forest walk",Himachal Pradesh,India,Temple/Religious,"Spiritual, Cultural, Photography","March to June, September to November",Moderate,1
Rohtang Pass,Kullu,high Himalayan pass near Manali with seasonal snow,"Snow viewing, scenic drives, photography",Himachal Pradesh,India,Mountain/Hill,"Eco, Adventure, Photography","March to June, September to November",Moderate,2
Betaab Valley,Anantnag,scenic valley in Pahalgam surrounded by mountains,"Nature walks, horse riding, photography",Jammu and Kashmir,India,Mountain/Hill,"Eco, Adventure, Photography",April to October,Moderate,2
Gulmarg,Baramulla,famous Himalayan meadow and ski destination,"Skiing, gondola ride, hiking, photography",Jammu and Kashmir,India,Mountain/Hill,"Eco, Adventure, Photography",April to October,Moderate,2
Vaishno Devi Shrine,Reasi,major pilgrimage destination in the Trikuta hills,"Pilgrimage, trekking, mountain sightseeing",Jammu and Kashmir,India,Temple/Religious,"Spiritual, Cultural, Photography",April to October,Moderate,1
Dal Lake,Srinagar,iconic lake with houseboats and shikaras in Srinagar,"Shikara ride, photography, houseboat experience",Jammu and Kashmir,India,Lake/Water,"Leisure, Photography",April to October,Budget,1
Shankaracharya Temple,Srinagar,hilltop temple overlooking Srinagar,"Temple visit, city viewpoints, photography",Jammu and Kashmir,India,Temple/Religious,"Spiritual, Cultural, Photography",April to October,Moderate,1
"Baidyanath Temple, Deoghar",Deoghar,major Jyotirlinga pilgrimage temple,"Pilgrimage, temple visit, cultural sightseeing",Jharkhand,India,Temple/Religious,"Spiritual, Cultural, Photography",October to February,Moderate,1
Betla National Park,Regional destination,forest reserve with wildlife and historic fort remains,"Safari, wildlife photography, nature walks",Jharkhand,India,Wildlife,"Eco, Adventure, Photography",October to February,Moderate,2
Dassam Falls,Regional destination,waterfall on the Kanchi River near Ranchi,"Waterfall sightseeing, photography, nature walks",Jharkhand,India,Waterfall,"Eco, Adventure, Photography",October to February,Budget,2
Hundru Falls,Regional destination,dramatic waterfall on the Subarnarekha River,"Waterfall viewing, hiking, photography",Jharkhand,India,Waterfall,"Eco, Adventure, Photography",October to February,Budget,2
Netarhat,Regional destination,hill station known for forests and viewpoints,"Sunrise viewing, hiking, photography",Jharkhand,India,Mountain/Hill,"Eco, Adventure, Photography",October to February,Moderate,2
Jog Falls,Shivamogga,major waterfall on the Sharavathi River,"Waterfall viewing, trekking, photography",Karnataka,India,Waterfall,"Eco, Adventure, Photography",October to March,Budget,2
Alappuzha Canal Cruise,Alappuzha,urban and rural canal network experience,"Canal cruise, photography, local-life sightseeing",Kerala,India,Lake/Water,"Eco, Leisure, Photography",October to March,Budget,2
Alappuzha–Kochi Backwater Cruise,Alappuzha,long-distance cruise through interconnected canals and lakes,"Backwater cruise, photography, village sightseeing",Kerala,India,Lake/Water,"Eco, Leisure, Photography",October to March,Budget,2
Chakkulathukavu Bhagavathy Temple,Alappuzha,popular Bhagavathy pilgrimage centre on the backwater belt,"Temple visit, festival experience, photography",Kerala,India,Temple/Religious,"Spiritual, Cultural",October to March,Budget,1
Champakulam St. Mary’s Basilica Heritage Circuit,Alappuzha,historic church and cultural landscape on the Pampa backwaters,"Church visit, heritage walk, photography",Kerala,India,Heritage,"Spiritual, Cultural, Photography",October to March,Moderate,1
Chavara Bhavan,Alappuzha,birthplace and heritage centre associated with Kuriakose Elias Chavara,"Heritage visit, spiritual tourism, photography",Kerala,India,Heritage,"Spiritual, Cultural",October to March,Moderate,1
Chengannur Mahadeva Temple,Alappuzha,historic Shiva temple and major pilgrimage centre,"Temple visit, architecture photography, pilgrimage",Kerala,India,Temple/Religious,"Spiritual, Cultural, Photography",October to March,Budget,1
Chettikulangara Bhagavathy Temple,Alappuzha,famous temple and Kettukazhcha festival tradition,"Temple visit, festival culture, photography",Kerala,India,Temple/Religious,"Spiritual, Cultural, Photography",October to March,Budget,1
"Coir Museum, Alappuzha",Alappuzha,museum documenting Kerala coir-making traditions,"Museum visit, craft demonstration, shopping",Kerala,India,Heritage,"Cultural, Leisure",October to March,Moderate,1
Kuttanad Aqua Tourism,Alappuzha,water-based tourism across paddy fields and canals,"Boat rides, village exploration, photography",Kerala,India,Lake/Water,"Eco, Leisure, Photography",October to March,Budget,2
Mannar Bell Metal Industry Village,Alappuzha,traditional Kerala bell-metal craft centre,"Craft tour, shopping, cultural photography",Kerala,India,Heritage,"Cultural, Shopping, Photography",October to March,Moderate,1
Bastion Bungalow,Ernakulam,historic Dutch-era building in Fort Kochi,"Museum visit, heritage walk, architecture photography",Kerala,India,Heritage,"Cultural, Heritage, Photography",October to March,Moderate,1
"Bishop’s House, Fort Kochi",Ernakulam,historic bishop’s residence overlooking the harbour,"Heritage walk, architecture photography",Kerala,India,Heritage,"Cultural, Photography",October to March,Moderate,1
"David Hall, Fort Kochi",Ernakulam,historic colonial building now used for art and cultural activities,"Art events, heritage walk, photography",Kerala,India,Heritage,"Cultural, Heritage, Photography",October to March,Moderate,1
"Haritha Bio-park, Ernakulam",Ernakulam,urban nature and recreation space,"Nature walk, family outing, photography",Kerala,India,Garden/Nature,"Eco, Family, Leisure",October to March,Budget,1
Koder House,Ernakulam,historic Indo-European heritage mansion in Fort Kochi,"Heritage walk, architecture photography",Kerala,India,Heritage,"Cultural, Heritage, Photography",October to March,Moderate,1
Kumbalangi Responsible Tourism Village,Ernakulam,fishing village known for backwater life and community tourism,"Village walk, canoeing, fishing experiences, photography",Kerala,India,Eco Tourism,"Eco, Cultural, Photography",October to March,Budget,1
"Maritime Museum, Kochi",Ernakulam,museum focused on Kerala and naval maritime heritage,"Museum visit, history tour, photography",Kerala,India,Heritage,"Cultural, Heritage, Photography",October to March,Moderate,1
Museum of Kerala History,Ernakulam,museum presenting Kerala history through art and exhibits,"Museum visit, cultural education, photography",Kerala,India,Heritage,"Cultural, Photography",October to March,Moderate,1
Old Harbour House,Ernakulam,historic trading-era building in Fort Kochi,"Heritage walk, architecture photography",Kerala,India,Heritage,"Cultural, Heritage, Photography",October to March,Moderate,1
Pierce Leslie Bungalow,Ernakulam,historic waterfront colonial-era residence,"Heritage walk, architecture photography",Kerala,India,Heritage,"Cultural, Heritage, Photography",October to March,Moderate,1
Chellarkovil,Idukki,waterfall and valley viewpoint near Kumily,"Viewpoint visit, hiking, photography",Kerala,India,Waterfall,"Adventure, Eco, Photography",October to March,Budget,2
Keezharkuthu Waterfalls,Idukki,multi-tier waterfall in forested eastern Idukki,"Trekking, waterfall sightseeing, photography",Kerala,India,Waterfall,"Adventure, Eco, Photography",October to March,Budget,2
Kuttikanam,Idukki,misty plantation hill station in Peerumade region,"Trekking, plantation walks, photography",Kerala,India,Mountain/Hill,"Adventure, Eco, Photography",October to March,Moderate,2
Murikkady,Idukki,spice plantation landscape near Thekkady,"Spice tour, plantation walk, photography",Kerala,India,Garden/Nature,"Eco, Cultural, Photography",October to March,Budget,1
Pandikuzhi,Idukki,green valley with streams near Thekkady,"Trekking, picnic, photography",Kerala,India,Mountain/Hill,"Adventure, Eco, Photography",October to March,Moderate,2
Peeru Hills,Idukki,wooded hillscape and trekking viewpoint,"Trekking, nature walks, photography",Kerala,India,Mountain/Hill,"Adventure, Eco, Photography",October to March,Moderate,2
Pullumedu,Idukki,forest hill destination on the Sabarimala route,"Hiking, forest sightseeing, photography",Kerala,India,Mountain/Hill,"Adventure, Spiritual, Photography",October to March,Moderate,2
Thrissanku Hills,Idukki,panoramic Western Ghats viewpoint near Peermade,"Sunset viewing, hiking, photography",Kerala,India,Mountain/Hill,"Adventure, Eco, Photography",October to March,Moderate,2
Vandanmedu,Idukki,major cardamom-growing region in Idukki,"Spice plantation visits, photography, local experiences",Kerala,India,Garden/Nature,"Eco, Cultural, Photography",October to March,Budget,1
Vattavada,Idukki,high-altitude farming valley known for seasonal crops,"Village visits, farm tourism, photography",Kerala,India,Mountain/Hill,"Eco, Cultural, Photography",October to March,Moderate,2
"Cinnamon Valley, Kannur",Kannur,spice plantation landscape associated with cinnamon cultivation,"Plantation tour, spice experience, photography",Kerala,India,Garden/Nature,"Eco, Cultural, Photography",October to March,Budget,1
Kanhirode Weavers Cooperative,Kannur,traditional handloom weaving centre,"Handloom visit, shopping, craft photography",Kerala,India,Heritage,"Cultural, Shopping, Photography",October to March,Moderate,1
Kunhimangalam Heritage Village,Kannur,traditional metal craft and village heritage landscape,"Craft tourism, village walk, photography",Kerala,India,Heritage,"Cultural, Eco, Photography",October to March,Moderate,1
Malayala Kalagramam,Kannur,cultural centre devoted to arts and regional traditions,"Art workshops, cultural events, photography",Kerala,India,Heritage,"Cultural, Leisure, Photography",October to March,Moderate,1
Odathil Palli,Kannur,historic mosque with distinctive Kerala architectural elements,"Architecture study, heritage walk, photography",Kerala,India,Temple/Religious,"Spiritual, Cultural, Photography",October to March,Budget,1
Overbury’s Folly,Kannur,hilltop colonial-era structure with sea and town views,"Heritage walk, viewpoint photography",Kerala,India,Heritage,"Cultural, Photography",October to March,Moderate,1
Palukachimala,Kannur,wooded hill and trekking landscape in eastern Kannur,"Trekking, nature walks, photography",Kerala,India,Mountain/Hill,"Adventure, Eco, Photography",October to March,Moderate,2
"St. Mary’s Forane Church, Kannur region",Kannur,historic Christian pilgrimage and architecture destination,"Church visit, architecture photography, cultural tourism",Kerala,India,Temple/Religious,"Spiritual, Cultural, Photography",October to March,Budget,1
Trichambaram Temple,Kannur,historic Krishna temple with strong ritual and festival traditions,"Temple visit, festival culture, photography",Kerala,India,Temple/Religious,"Spiritual, Cultural, Photography",October to March,Budget,1
Achamthuruthi,Kasaragod,backwater village and rural riverside landscape,"Canoeing, village tourism, photography",Kerala,India,Lake/Water,"Eco, Leisure, Photography",October to March,Budget,2
Anandashram,Kasaragod,peaceful spiritual retreat with wooded surroundings,"Meditation, heritage visit, nature walks",Kerala,India,Heritage,"Spiritual, Eco",October to March,Moderate,1
Central Plantation Crops Research Institute,Kasaragod,major coconut and plantation research campus and visitor destination,"Garden visit, agricultural education, photography",Kerala,India,Garden/Nature,"Eco, Cultural, Photography",October to March,Budget,1
Chithari,Kasaragod,"coastal village with beaches, backwaters and traditional life","Beach walks, village sightseeing, photography",Kerala,India,Beach,"Eco, Beach, Photography",October to March,Budget,2
Edneer Mutt,Kasaragod,historic monastery and cultural centre,"Heritage visit, cultural study, photography",Kerala,India,Heritage,"Spiritual, Cultural, Photography",October to March,Moderate,1
Padanna Backwaters,Kasaragod,quiet backwater village and coir/fishing landscape,"Boat rides, village walk, photography",Kerala,India,Lake/Water,"Eco, Cultural, Photography",October to March,Budget,2
Pandiyan Kallu,Kasaragod,rocky coastal landmark and scenic sea viewpoint,"Coastal sightseeing, photography, sunset viewing",Kerala,India,Beach,"Beach, Adventure, Photography",October to March,Budget,2
Sree Mahalingeswara Temple,Kasaragod,historic temple set amid the northern Kerala countryside,"Temple visit, architecture photography, pilgrimage",Kerala,India,Temple/Religious,"Spiritual, Cultural, Photography",October to March,Budget,1
Thalankara Heritage Area,Kasaragod,historic port-side neighbourhood with Islamic and maritime heritage,"Heritage walk, architecture photography, food tourism",Kerala,India,Heritage,"Cultural, Photography",October to March,Moderate,1
Tulur Vanam,Kasaragod,sacred forest and biodiversity-rich cultural landscape,"Nature walk, cultural study, photography",Kerala,India,Eco Tourism,"Eco, Spiritual, Photography",October to March,Budget,1
Achankovil Sastha Temple,Kollam,forest pilgrimage centre in the eastern hills,"Pilgrimage, forest drive, cultural sightseeing",Kerala,India,Temple/Religious,"Spiritual, Cultural",October to March,Budget,1
Ashtamudi Wetland,Kollam,extensive backwater ecosystem and mangrove landscape,"Backwater cruise, birdwatching, photography",Kerala,India,Eco Tourism,"Eco, Leisure, Photography",October to March,Budget,1
Chinnakada Clock Tower,Kollam,historic urban landmark in central Kollam,"City walk, architecture photography, local shopping",Kerala,India,Heritage,"Cultural, Photography",October to March,Moderate,1
Kallada River,Kollam,scenic river landscape through eastern Kollam,"River views, photography, village sightseeing",Kerala,India,Lake/Water,"Eco, Leisure, Photography",October to March,Budget,2
Kollam Adventure Park,Kollam,waterfront recreation area beside Ashtamudi Lake,"Boating, family recreation, lakeside walks",Kerala,India,Theme Park,"Family, Leisure, Photography",October to March,Budget,1
Kottarakkara Kathakali Centre,Kollam,cultural centre linked with Kerala classical performance,"Kathakali viewing, cultural experience, photography",Kerala,India,Heritage,"Cultural, Leisure, Photography",October to March,Moderate,1
Kottukal Rock-cut Cave Temple,Kollam,ancient rock-cut shrine carved into natural rock,"Temple visit, heritage exploration, photography",Kerala,India,Cave/Geological,"Spiritual, Cultural, Photography",October to March,Budget,1
Pattazhy Devi Temple,Kollam,historic Bhagavathy temple and local pilgrimage centre,"Temple visit, cultural photography, festival experience",Kerala,India,Temple/Religious,"Spiritual, Cultural, Photography",October to March,Budget,1
Thangassery Dutch Cemetery,Kollam,colonial-era cemetery reflecting Kollam trading history,"Heritage walk, history study, photography",Kerala,India,Heritage,"Heritage, Cultural, Photography",October to March,Moderate,1
Thevally Palace,Kollam,historic palace on the banks of Ashtamudi Lake,"Heritage sightseeing, lake views, photography",Kerala,India,Heritage,"Cultural, Heritage, Photography",October to March,Moderate,1
"Anchuvilakku, Kottayam",Kottayam,historic stone-lamp landmark in Kottayam town,"Heritage walk, photography, city sightseeing",Kerala,India,Heritage,"Cultural, Photography",October to March,Moderate,1
Bay Island Driftwood Museum,Kottayam,unusual driftwood art and natural-material collections,"Museum visit, photography, family outing",Kerala,India,Heritage,"Cultural, Photography",October to March,Moderate,1
Kottathavalam,Kottayam,rock formations and hilltop picnic landscape,"Trekking, nature walks, photography",Kerala,India,Mountain/Hill,"Adventure, Eco, Photography",October to March,Moderate,2
Nadukani Hills,Kottayam,panoramic hill landscape overlooking the plains,"Trekking, viewpoint visits, photography",Kerala,India,Mountain/Hill,"Adventure, Eco, Photography",October to March,Moderate,2
"St. George Orthodox Church, Puthuppally",Kottayam,historic church and annual pilgrimage centre,"Church visit, architecture photography, cultural tourism",Kerala,India,Temple/Religious,"Spiritual, Cultural, Photography",October to March,Budget,1
Thangalppara,Kottayam,rocky hilltop viewpoint in the highlands,"Trekking, sunrise viewing, photography",Kerala,India,Mountain/Hill,"Adventure, Eco, Photography",October to March,Moderate,2
"The Old Seminary, Kottayam",Kottayam,historic theological and colonial-era educational landmark,"Heritage tour, architecture photography, museum-style visit",Kerala,India,Heritage,"Cultural, Heritage, Photography",October to March,Moderate,1
"Vavarambalam, Erumeli",Kottayam,cultural and pilgrimage landmark in the foothills,"Pilgrimage, cultural sightseeing, photography",Kerala,India,Temple/Religious,"Spiritual, Cultural",October to March,Budget,1
"Vazhikkadavu, Kottayam",Kottayam,riverside and hill landscape around eastern Kottayam,"Nature walks, riverside views, photography",Kerala,India,Lake/Water,"Eco, Leisure, Photography",October to March,Budget,2
"Vembanad Lake, Kottayam",Kottayam,major backwater lake and village landscape,"Boating, birdwatching, photography",Kerala,India,Lake/Water,"Eco, Leisure, Photography",October to March,Budget,2
Arippara Waterfalls,Kozhikode,multi-stage waterfall amid forest and rocky terrain,"Trekking, waterfall sightseeing, photography",Kerala,India,Waterfall,"Adventure, Eco, Photography",October to March,Budget,2
KIRTADS Museum,Kozhikode,museum documenting tribal cultures and traditions of Kerala,"Museum visit, cultural education, photography",Kerala,India,Heritage,"Cultural, Photography",October to March,Moderate,1
Kolavi Palam Beach,Kozhikode,nesting area and scenic shoreline on the Malabar coast,"Beach walks, birdwatching, photography",Kerala,India,Beach,"Eco, Beach, Photography",October to March,Budget,2
Krishna Menon Museum,Kozhikode,museum devoted to art and regional cultural history,"Museum visit, art appreciation, photography",Kerala,India,Heritage,"Cultural, Photography",October to March,Moderate,1
Payyoli Beach,Kozhikode,broad Malabar coast beach with village surroundings,"Beach walks, swimming, sunset photography",Kerala,India,Beach,"Beach, Leisure, Photography",October to March,Budget,2
Thikkoti Lighthouse,Kozhikode,historic coastal lighthouse at Thikkodi,"Lighthouse sightseeing, coastal photography",Kerala,India,Heritage,"Cultural, Photography",October to March,Moderate,1
Vadakara Sand Banks,Kozhikode,river-mouth beach landscape where river meets the sea,"Beach walks, photography, sunset viewing",Kerala,India,Beach,"Beach, Leisure, Photography",October to March,Budget,2
Varakkal Devi Temple,Kozhikode,traditional temple associated with Kerala temple architecture,"Temple visit, architecture photography, pilgrimage",Kerala,India,Temple/Religious,"Spiritual, Cultural, Photography",October to March,Budget,1
Vayalada Viewpoint,Kozhikode,hilltop view across Kozhikode and nearby valleys,"Trekking, sunrise viewing, photography",Kerala,India,Mountain/Hill,"Adventure, Eco, Photography",October to March,Moderate,2
"Water Museum and Bio Park, Kozhikode",Kozhikode,water-conservation interpretation and nature recreation centre,"Educational visit, nature walk, family recreation",Kerala,India,Garden/Nature,"Eco, Family, Photography",October to March,Budget,1
"Jama-at Mosque, Malappuram",Malappuram,historic mosque and regional Islamic architectural heritage,"Heritage visit, architecture study, photography",Kerala,India,Temple/Religious,"Spiritual, Cultural, Photography",October to March,Budget,1
Karuvarakundu,Malappuram,green highland area with streams and waterfalls,"Trekking, waterfall visits, photography",Kerala,India,Mountain/Hill,"Adventure, Eco, Photography",October to March,Moderate,2
Poonkudil Mana,Malappuram,traditional Kerala heritage mansion,"Heritage visit, architecture photography",Kerala,India,Heritage,"Cultural, Heritage, Photography",October to March,Moderate,1
Shanthi Theeram Riverside Park,Malappuram,riverfront recreation and family leisure destination,"River walks, family outing, photography",Kerala,India,Lake/Water,"Family, Leisure, Photography",October to March,Budget,2
Tanur,Malappuram,historic coastal town and Arabian Sea shoreline,"Beach walks, fishing-village sightseeing, photography",Kerala,India,Beach,"Beach, Cultural, Photography",October to March,Budget,2
Thirurangadi,Malappuram,historic Malabar town with strong cultural and Islamic heritage,"Heritage walk, architecture photography, food tourism",Kerala,India,Heritage,"Cultural, Photography",October to March,Moderate,1
Trikandiyur Shiva Temple,Malappuram,historic Shiva temple in Tirur region,"Temple visit, architecture photography, pilgrimage",Kerala,India,Temple/Religious,"Spiritual, Cultural, Photography",October to March,Budget,1
Vakkad Beach,Malappuram,coastal landscape near Tirur and the Bharathapuzha estuary zone,"Beach walks, birdwatching, photography",Kerala,India,Beach,"Beach, Eco, Photography",October to March,Budget,2
Vallikkunnu Beach,Malappuram,quiet coastal beach and village landscape,"Beach walks, sunset photography, swimming",Kerala,India,Beach,"Beach, Leisure, Photography",October to March,Budget,2
Vettakkorumakan Temple,Malappuram,traditional Kerala temple dedicated to Vettakkorumakan,"Temple visit, cultural photography, pilgrimage",Kerala,India,Temple/Religious,"Spiritual, Cultural",October to March,Budget,1
Gandhi Seva Sadan,Palakkad,cultural and arts institution linked to classical traditions,"Cultural programs, heritage visit, photography",Kerala,India,Heritage,"Cultural, Photography",October to March,Moderate,1
"Kambalathara, Palakkad",Palakkad,rural landscape and lesser-known nature viewpoint,"Nature walks, village sightseeing, photography",Kerala,India,Garden/Nature,"Eco, Leisure, Photography",October to March,Budget,1
Krishnankutty Pulavar Memorial,Palakkad,cultural memorial linked to Kerala puppetry traditions,"Cultural visit, performance arts, photography",Kerala,India,Heritage,"Cultural, Photography",October to March,Moderate,1
Kunchan Smarakam,Palakkad,memorial and cultural centre for poet Kunchan Nambiar,"Museum visit, literary tourism, photography",Kerala,India,Heritage,"Cultural, Photography",October to March,Moderate,1
Navara Eco Farm,Palakkad,agricultural landscape promoting traditional farming and eco experiences,"Farm visit, local-food experience, photography",Kerala,India,Eco Tourism,"Eco, Cultural, Family",October to March,Budget,1
Olappamanna Mana,Palakkad,traditional Kerala manor and cultural heritage site,"Heritage walk, architecture photography",Kerala,India,Heritage,"Cultural, Heritage, Photography",October to March,Moderate,1
Poomully Mana,Palakkad,heritage mansion associated with Kerala cultural traditions,"Heritage tour, architecture photography",Kerala,India,Heritage,"Cultural, Heritage, Photography",October to March,Moderate,1
Ramassery Village,Palakkad,village known for Ramassery idli and traditional food culture,"Food tourism, village walk, local cuisine",Kerala,India,Heritage,"Food, Cultural, Photography",October to March,Moderate,1
Thenari,Palakkad,natural spring and rural pilgrimage landscape,"Nature walk, local sightseeing, photography",Kerala,India,Lake/Water,"Eco, Spiritual, Photography",October to March,Budget,2
Thiruvegappura Sankaranarayan Temple,Palakkad,historic temple known for Kerala architecture and rituals,"Temple visit, architecture photography, pilgrimage",Kerala,India,Temple/Religious,"Spiritual, Cultural, Photography",October to March,Budget,1
Aranmula Thiruvonathoni,Pathanamthitta,traditional ceremonial boat linked to Aranmula heritage,"Boat-race culture, heritage viewing, photography",Kerala,India,Heritage,"Cultural, Photography",October to March,Moderate,1
Aranmula Vallasadya,Pathanamthitta,traditional feast and cultural heritage experience at Aranmula,"Cultural experience, local cuisine, photography",Kerala,India,Heritage,"Cultural, Food, Photography",October to March,Moderate,1
Kadmanitta Padayani Village,Pathanamthitta,traditional ritual-art heritage associated with Padayani,"Cultural performance, folk-art experience, photography",Kerala,India,Heritage,"Cultural, Photography",October to March,Moderate,1
Maramon,Pathanamthitta,historic riverbank village known for Christian pilgrimage and convention,"Cultural visit, riverside walk, photography",Kerala,India,Heritage,"Spiritual, Cultural, Photography",October to March,Moderate,1
Nilackal,Pathanamthitta,forest gateway associated with Sabarimala pilgrimage routes,"Pilgrimage, forest sightseeing, photography",Kerala,India,Temple/Religious,"Spiritual, Eco",October to March,Budget,1
Pamba River,Pathanamthitta,major river and pilgrimage landscape of central Kerala,"River sightseeing, photography, cultural exploration",Kerala,India,Lake/Water,"Spiritual, Eco, Photography",October to March,Budget,2
Pandalam Valiyakoickal Temple,Pathanamthitta,important royal and pilgrimage landmark associated with Ayyappa tradition,"Temple visit, heritage study, photography",Kerala,India,Temple/Religious,"Spiritual, Cultural",October to March,Budget,1
"Sree Vallabha Temple Riverfront, Thiruvalla",Pathanamthitta,major Vaishnavite temple and cultural landmark by the Manimala basin,"Temple visit, architecture photography, cultural sightseeing",Kerala,India,Temple/Religious,"Spiritual, Cultural, Photography",October to March,Budget,1
Thekkekudi Cave Temple,Pathanamthitta,rock-cut shrine with historic architecture,"Heritage exploration, temple visit, photography",Kerala,India,Cave/Geological,"Spiritual, Cultural, Photography",October to March,Budget,1
"Vavar Mosque, Erumeli",Pathanamthitta,historic Islamic pilgrimage landmark associated with Sabarimala route,"Pilgrimage, cultural study, architecture photography",Kerala,India,Temple/Religious,"Spiritual, Cultural, Photography",October to March,Budget,1
Aruvikkara Dam,Thiruvananthapuram,scenic reservoir and riverside landscape near the capital,"Boating, picnicking, photography",Kerala,India,Lake/Water,"Family, Leisure, Photography",October to March,Budget,2
"CVN Kalari Sangham, Thiruvananthapuram",Thiruvananthapuram,traditional Kalaripayattu training and demonstrations,"Kalari demonstration, cultural experience, photography",Kerala,India,Heritage,"Cultural, Adventure, Photography",October to March,Moderate,1
Koyikkal Palace,Thiruvananthapuram,historic palace complex and folk traditions,"Heritage tour, museum visit, photography",Kerala,India,Heritage,"Cultural, Heritage, Photography",October to March,Moderate,1
Neyyar Wildlife Sanctuary,Thiruvananthapuram,forest and wildlife landscape around Neyyar catchment,"Wildlife watching, nature walks, photography",Kerala,India,Wildlife,"Eco, Adventure, Photography",October to March,Budget,2
Samudra Beach,Thiruvananthapuram,quieter Kovalam-area shoreline and sunset views,"Beach walks, swimming, sunset photography",Kerala,India,Beach,"Beach, Leisure, Photography",October to March,Budget,2
Sree Chitra Art Gallery,Thiruvananthapuram,major collection of Indian and Asian art,"Art appreciation, museum visit, photography",Kerala,India,Heritage,"Cultural, Photography",October to March,Moderate,1
Sree Chitra Enclave,Thiruvananthapuram,heritage collection connected with Kerala royal history,"Museum visit, history tour, photography",Kerala,India,Heritage,"Cultural, Heritage, Photography",October to March,Moderate,1
Thiruvananthapuram Zoo,Thiruvananthapuram,historic zoological garden with diverse animal collections,"Wildlife viewing, family outing, photography",Kerala,India,Wildlife,"Family, Leisure, Photography",October to March,Budget,2
Valiathura Beach,Thiruvananthapuram,historic coastal pier and Arabian Sea sunsets,"Sunset walks, photography, coastal sightseeing",Kerala,India,Beach,"Beach, Leisure, Photography",October to March,Budget,2
Vyloppilli Samskrithi Bhavan,Thiruvananthapuram,Kerala arts and cultural performance centre,"Cultural programs, literature, photography",Kerala,India,Heritage,"Cultural, Leisure, Photography",October to March,Moderate,1
"Archaeological Museum, Thrissur",Thrissur,museum displaying archaeological and historical collections,"Museum visit, history tour, photography",Kerala,India,Heritage,"Cultural, Photography",October to March,Moderate,1
Ariyannur Umbrellas / Kudakkallu,Thrissur,megalithic archaeological landscape and laterite monuments,"Archaeology, heritage walk, photography",Kerala,India,Heritage,"Cultural, Photography",October to March,Moderate,1
Dream World Water Park,Thrissur,large recreation and water-theme attraction near Athirappilly route,"Water rides, family recreation, leisure",Kerala,India,Theme Park,"Family, Leisure",October to March,Budget,1
Gothuruthu,Thrissur,island village known for waterways and local culture,"Village walk, canoeing, photography",Kerala,India,Island,"Eco, Cultural, Photography",October to March,Budget,1
Ilanjippara Waterfalls,Thrissur,forest waterfall in the Athirappilly region,"Trekking, waterfall viewing, photography",Kerala,India,Waterfall,"Adventure, Eco, Photography",October to March,Budget,2
Kuthampully Handloom Village,Thrissur,traditional handloom weaving centre,"Handloom demonstrations, shopping, cultural photography",Kerala,India,Heritage,"Cultural, Shopping, Photography",October to March,Moderate,1
Malakkappara,Thrissur,highland tea and forest landscape on the Chalakudy route,"Scenic drive, plantation visits, photography",Kerala,India,Mountain/Hill,"Eco, Leisure, Photography",October to March,Moderate,2
Nattika Beach,Thrissur,long sandy shoreline on Thrissur coast,"Beach walks, swimming, sunset photography",Kerala,India,Beach,"Beach, Leisure, Photography",October to March,Budget,2
Sampaloor Church,Thrissur,historic church in the Chalakudy region,"Heritage visit, architecture photography",Kerala,India,Heritage,"Spiritual, Cultural, Photography",October to March,Moderate,1
Silver Storm Water Theme Park,Thrissur,family-oriented amusement and water park,"Water rides, family recreation, leisure",Kerala,India,Theme Park,"Family, Leisure",October to March,Budget,1
Begur Wildlife Sanctuary,Wayanad,forest and wildlife habitat in the northern Wayanad landscape,"Wildlife watching, nature walks, photography",Kerala,India,Wildlife,"Eco, Adventure, Photography",October to March,Budget,2
Boys Town Herbal Garden,Wayanad,botanical and herbal demonstration centre,"Garden walk, nature study, photography",Kerala,India,Garden/Nature,"Eco, Family, Photography",October to March,Budget,1
En Ooru Tribal Heritage Village,Wayanad,tribal heritage and experiential tourism village,"Tribal-culture experience, craft viewing, photography",Kerala,India,Heritage,"Cultural, Eco, Photography",October to March,Moderate,1
Kanthanpara Waterfalls,Wayanad,scenic cascade surrounded by coffee and forest country,"Nature walks, waterfall sightseeing, photography",Kerala,India,Waterfall,"Eco, Adventure, Photography",October to March,Budget,2
Kurumbalakkotta,Wayanad,hilltop viewpoint overlooking Wayanad valleys,"Trekking, sunrise viewing, photography",Kerala,India,Mountain/Hill,"Adventure, Eco, Photography",October to March,Moderate,2
"Pazhassi Raja Museum and Memorial, Mananthavady",Wayanad,heritage destination associated with Kerala resistance history,"Museum visit, history tour, photography",Kerala,India,Heritage,"Cultural, Heritage, Photography",October to March,Moderate,1
Sentinel Rock Waterfall,Wayanad,dramatic waterfall and forest landscape,"Trekking, waterfall viewing, photography",Kerala,India,Waterfall,"Adventure, Eco, Photography",October to March,Budget,2
Thollayiram,Wayanad,remote highland landscape and trekking area,"Trekking, scenic views, photography",Kerala,India,Mountain/Hill,"Adventure, Eco, Photography",October to March,Moderate,2
Vythiri Hill Station,Wayanad,misty highland destination with plantations and forest,"Trekking, plantation visits, photography",Kerala,India,Mountain/Hill,"Eco, Leisure, Photography",October to March,Moderate,2
Wayanad Wildlife Sanctuary,Wayanad,protected forest landscape encompassing rich Western Ghats biodiversity,"Safari, wildlife watching, photography",Kerala,India,Wildlife,"Eco, Adventure, Photography",October to March,Budget,2
Khardung La,Regional destination,high mountain pass north of Leh,"Scenic drive, mountain photography, adventure touring",Ladakh,India,Mountain/Hill,"Eco, Adventure, Photography",May to September,Moderate,2
Magnetic Hill,Regional destination,popular roadside landmark west of Leh,"Scenic drive, photography, local sightseeing",Ladakh,India,Mountain/Hill,"Eco, Adventure, Photography",May to September,Moderate,2
Pangong Lake,Regional destination,high-altitude endorheic lake known for changing blue hues,"Scenic drive, photography, camping",Ladakh,India,Lake/Water,"Leisure, Photography",May to September,Budget,1
Tso Moriri,Regional destination,remote high-altitude lake in eastern Ladakh,"Camping, photography, birdwatching",Ladakh,India,Lake/Water,"Leisure, Photography",May to September,Budget,1
Agatti Island,Regional destination,reef-fringed island with turquoise lagoons,"Snorkeling, scuba diving, beach walks, photography",Lakshadweep,India,Island,"Island, Leisure, Photography",October to May,Budget,2
Bangaram Island,Regional destination,tropical lagoon island known for coral and clear water,"Snorkeling, diving, beach relaxation, photography",Lakshadweep,India,Island,"Island, Leisure, Photography",October to May,Budget,2
Kadmat Island,Regional destination,long sandy island popular for water sports,"Diving, snorkeling, kayaking, photography",Lakshadweep,India,Island,"Island, Leisure, Photography",October to May,Budget,2
Kalpeni Island,Regional destination,lagoon destination known for coral and white-sand beaches,"Snorkeling, kayaking, beach relaxation",Lakshadweep,India,Island,"Island, Leisure, Photography",October to May,Budget,2
Kavaratti Island,Regional destination,administrative capital with lagoons and marine life,"Kayaking, snorkeling, island sightseeing, photography",Lakshadweep,India,Island,"Island, Leisure, Photography",October to May,Budget,2
Mandu,Dhar,historic hilltop city of medieval Afghan architecture,"Fort sightseeing, architecture photography, heritage walk",Madhya Pradesh,India,Heritage,"Cultural, Photography",October to March,Moderate,1
Kanha National Park,Mandla,large tiger-reserve landscape of sal forests and meadows,"Jeep safari, wildlife photography, nature viewing",Madhya Pradesh,India,Wildlife,"Eco, Adventure, Photography",October to March,Moderate,2
Andro Heritage Village,Regional destination,traditional village displaying local cultural traditions,"Village tourism, museum visit, cultural photography",Manipur,India,Heritage,"Cultural, Photography",October to April,Moderate,1
Kangla Fort,Regional destination,historic seat of Manipur’s royal administration,"Fort walk, cultural sightseeing, photography",Manipur,India,Heritage,"Cultural, Photography",October to April,Moderate,1
Loktak Lake,Regional destination,largest freshwater lake in Northeast India with floating phumdis,"Boating, birdwatching, photography",Manipur,India,Lake/Water,"Leisure, Photography",October to April,Budget,1
Shree Govindajee Temple,Regional destination,major Vaishnavite temple in Imphal,"Temple visit, cultural photography, pilgrimage",Manipur,India,Temple/Religious,"Spiritual, Cultural, Photography",October to April,Moderate,1
Dawki River,Regional destination,clear-water river along the India-Bangladesh border,"Boating, kayaking, photography",Meghalaya,India,Lake/Water,"Leisure, Photography",October to April,Budget,1
Living Root Bridges,Regional destination,unique bio-engineered bridges grown from living roots,"Trekking, village tourism, photography",Meghalaya,India,Eco Tourism,"Eco, Adventure, Photography",October to April,Budget,1
Mawlynnong,Regional destination,village known for community-managed cleanliness and greenery,"Village walk, nature tourism, photography",Meghalaya,India,Eco Tourism,"Eco, Adventure, Photography",October to April,Budget,1
Mawsynram,Regional destination,high-rainfall hill landscape with caves and waterfalls,"Scenic drives, cave visits, photography",Meghalaya,India,Mountain/Hill,"Eco, Adventure, Photography",October to April,Moderate,2
Aizawl,Regional destination,hill capital with panoramic ridges and cultural attractions,"City sightseeing, viewpoints, cultural tourism",Mizoram,India,Mountain/Hill,"Eco, Adventure, Photography",October to March,Moderate,2
Durtlang Hills,Regional destination,ridge-top views over Aizawl and surrounding valleys,"Hiking, city views, photography",Mizoram,India,Mountain/Hill,"Eco, Adventure, Photography",October to March,Moderate,2
Phawngpui National Park,Regional destination,blue mountain national park in southeastern Mizoram,"Trekking, wildlife viewing, photography",Mizoram,India,Wildlife,"Eco, Adventure, Photography",October to March,Moderate,2
Reiek,Regional destination,mountain viewpoint overlooking rolling Mizo hills,"Trekking, viewpoint photography, sunrise viewing",Mizoram,India,Mountain/Hill,"Eco, Adventure, Photography",October to March,Moderate,2
Vantawng Falls,Regional destination,highest waterfall in Mizoram,"Waterfall sightseeing, hiking, photography",Mizoram,India,Waterfall,"Eco, Adventure, Photography",October to March,Budget,2
Dzukou Valley,Regional destination,high-altitude valley famous for seasonal flowers and trekking,"Trekking, camping, photography",Nagaland,India,Mountain/Hill,"Eco, Adventure, Photography",October to May,Moderate,2
Japfu Peak,Regional destination,high peak and trekking destination near Kohima,"Trekking, sunrise viewing, photography",Nagaland,India,Mountain/Hill,"Eco, Adventure, Photography",October to May,Moderate,2
Khonoma Village,Regional destination,historic Angami village known for conservation and culture,"Village walk, cultural tourism, photography",Nagaland,India,Heritage,"Cultural, Photography",October to May,Moderate,1
Kisama Heritage Village,Regional destination,cultural village associated with Hornbill Festival,"Cultural performances, craft viewing, photography",Nagaland,India,Heritage,"Cultural, Photography",October to May,Moderate,1
Naga Heritage Village,Regional destination,showcase of traditional Naga architectural styles and culture,"Cultural walk, photography, local craft experience",Nagaland,India,Heritage,"Cultural, Photography",October to May,Moderate,1
"Jagannath Temple, Puri",Puri,major pilgrimage temple and iconic Puri landmark,"Pilgrimage, heritage walk, cultural sightseeing",Odisha,India,Temple/Religious,"Spiritual, Cultural, Photography",October to March,Moderate,1
Arikamedu,Ariyankuppam,ancient archaeological site linked to Indo-Roman maritime trade,"Archaeology, heritage walk, photography",Puducherry,India,Heritage,"Cultural, Heritage, Photography",October to March,Budget,1
Matrimandir,Auroville,golden spherical meditation centre and architectural landmark,"Guided visit, meditation, architecture photography",Puducherry,India,Heritage,"Spiritual, Photography",October to March,Moderate,1
Promenade Beach,Puducherry,seafront promenade and iconic coastal landscape in the French Quarter,"Beach walks, sunrise viewing, photography, city sightseeing",Puducherry,India,Beach,"Beach, Leisure, Photography",October to March,Budget,1
Sri Aurobindo Ashram,Puducherry,spiritual retreat and cultural landmark associated with Sri Aurobindo and The Mother,"Meditation, heritage visit, peaceful walks, photography",Puducherry,India,Heritage,"Spiritual, Cultural, Photography",October to March,Moderate,1
"Qila Mubarak, Patiala",Patiala,historic fort-palace complex of Patiala royalty,"Heritage walk, palace tour, photography",Punjab,India,Heritage,"Cultural, Photography",October to March,Moderate,1
Anandpur Sahib,Regional destination,important Sikh pilgrimage town and heritage centre,"Pilgrimage, museum visit, cultural sightseeing",Punjab,India,Temple/Religious,"Spiritual, Cultural, Photography",October to March,Moderate,1
Golden Temple,Regional destination,major Sikh pilgrimage complex in Amritsar,"Pilgrimage, architecture photography, cultural tourism",Punjab,India,Temple/Religious,"Spiritual, Cultural, Photography",October to March,Moderate,1
Jallianwala Bagh,Regional destination,historic memorial site in Amritsar,"History visit, memorial tour, photography",Punjab,India,Heritage,"Cultural, Photography",October to March,Moderate,1
Wagah-Attari Border,Regional destination,international border ceremony and visitor attraction,"Ceremony viewing, photography, cultural experience",Punjab,India,Heritage,"Cultural, Photography",October to March,Moderate,1
Gurudongmar Lake,Regional destination,high-altitude sacred lake in North Sikkim,"Scenic drive, photography, nature viewing",Sikkim,India,Lake/Water,"Leisure, Photography","March to June, September to November",Budget,1
Nathula Pass,Regional destination,high Himalayan pass linking Sikkim with Tibet region,"Scenic drive, snow viewing, photography",Sikkim,India,Mountain/Hill,"Eco, Adventure, Photography","March to June, September to November",Moderate,2
Rumtek Monastery,Regional destination,important Buddhist monastery near Gangtok,"Monastery visit, cultural study, photography",Sikkim,India,Temple/Religious,"Spiritual, Cultural, Photography","March to June, September to November",Moderate,1
Tsomgo Lake,Regional destination,high-altitude glacial lake near Gangtok,"Lake sightseeing, snow viewing, photography",Sikkim,India,Lake/Water,"Leisure, Photography","March to June, September to November",Budget,1
Yumthang Valley,Regional destination,high Himalayan valley known for seasonal flowers,"Nature walks, scenic drives, photography",Sikkim,India,Mountain/Hill,"Eco, Adventure, Photography","March to June, September to November",Moderate,2
Ooty,Nilgiris,hill station known for tea estates and the Nilgiri landscape,"Toy-train ride, plantation visits, photography",Tamil Nadu,India,Mountain/Hill,"Eco, Adventure, Photography",October to March,Moderate,2
"Ramanathaswamy Temple, Rameswaram",Ramanathapuram,major pilgrimage temple with long corridors,"Pilgrimage, temple architecture, photography",Tamil Nadu,India,Temple/Religious,"Spiritual, Cultural, Photography",October to March,Moderate,1
Brihadeeswarar Temple,Thanjavur,Chola-era temple at Thanjavur and UNESCO component,"Temple visit, heritage walk, photography",Tamil Nadu,India,Temple/Religious,"Spiritual, Cultural, Photography",October to March,Moderate,1
Charminar,Regional destination,iconic four-minaret monument in Hyderabad,"Heritage walk, architecture photography, shopping",Telangana,India,Heritage,"Cultural, Photography",October to February,Moderate,1
Golconda Fort,Regional destination,historic fort and acoustic architectural complex,"Fort tour, sound-and-light experience, photography",Telangana,India,Heritage,"Cultural, Photography",October to February,Moderate,1
Hussain Sagar Lake,Regional destination,large urban lake with Buddha statue viewpoint,"Boating, lakeside walk, city photography",Telangana,India,Lake/Water,"Leisure, Photography",October to February,Budget,1
Ramappa Temple,Regional destination,UNESCO-listed Kakatiya temple complex,"Heritage walk, architecture photography, cultural tourism",Telangana,India,Temple/Religious,"Spiritual, Cultural, Photography",October to February,Moderate,1
Salar Jung Museum,Regional destination,major art and antiquities museum in Hyderabad,"Museum visit, art appreciation, photography",Telangana,India,Heritage,"Cultural, Photography",October to February,Moderate,1
Neermahal Palace,Regional destination,lake palace set in Rudrasagar Lake,"Boat ride, palace visit, photography",Tripura,India,Heritage,"Cultural, Photography",October to March,Moderate,1
Sepahijala Wildlife Sanctuary,Regional destination,forest and wetland wildlife area near Agartala,"Wildlife viewing, birdwatching, nature walks",Tripura,India,Wildlife,"Eco, Adventure, Photography",October to March,Moderate,2
Tripura Sundari Temple,Regional destination,major Shakti pilgrimage shrine at Udaipur,"Pilgrimage, temple visit, cultural photography",Tripura,India,Temple/Religious,"Spiritual, Cultural, Photography",October to March,Moderate,1
Ujjayanta Palace,Regional destination,historic royal palace in Agartala,"Palace museum visit, architecture photography",Tripura,India,Heritage,"Cultural, Photography",October to March,Moderate,1
Unakoti,Regional destination,rock-cut Shaivite sculptures set amid forest hills,"Rock-art sightseeing, trekking, photography",Tripura,India,Heritage,"Cultural, Photography",October to March,Moderate,1
Bara Imambara,Lucknow,large 18th-century monument and labyrinth complex,"Heritage walk, architecture photography, history tour",Uttar Pradesh,India,Heritage,"Cultural, Photography",October to March,Moderate,1
Rishikesh,Dehradun,riverfront spiritual and adventure destination on the Ganges,"River rafting, yoga, temple visits, photography",Uttarakhand,India,Lake/Water,"Leisure, Photography","March to June, September to November",Budget,1
Bishnupur Terracotta Temples,Bankura,historic Bengal temple town famous for terracotta art,"Temple sightseeing, craft viewing, photography",West Bengal,India,Heritage,"Cultural, Photography",October to March,Moderate,1
Darjeeling Himalayan Railway,Darjeeling,historic mountain railway and UNESCO property,"Toy-train ride, scenic sightseeing, photography",West Bengal,India,Heritage,"Cultural, Photography",October to March,Moderate,1
Victoria Memorial,Kolkata,grand colonial-era museum and Kolkata landmark,"Museum visit, garden walk, photography",West Bengal,India,Heritage,"Cultural, Photography",October to March,Moderate,1
Ubud,Bali,"arts, temples, rice terraces and wellness culture","Temple visits, rice-terrace walks, wellness, photography",Bali,Indonesia,Heritage,"Cultural, Wellness, Photography",April to October,Moderate,2
Guinness Storehouse,Dublin,visitor attraction dedicated to the history of Guinness,"Museum experience, city views, food and beverage tourism",Dublin,Ireland,Heritage,"Cultural, Leisure, Photography",Year-round,Premium,1
Old City of Jerusalem,Jerusalem,historic walled city sacred to multiple faiths,"Heritage walk, pilgrimage, architecture photography",Jerusalem,Israel,Heritage,"Spiritual, Cultural, Photography","March to May, September to November",Premium,2
"Dead Sea, Israel",Southern District,hypersaline lake and wellness destination,"Floating, wellness, resort leisure, photography",Southern District,Israel,Lake/Water,"Wellness, Leisure, Photography",October to April,Premium,1
Masada,Southern District,desert fortress and archaeological site above the Dead Sea,"Archaeology, hiking, sunrise viewing, photography",Southern District,Israel,Heritage,"Cultural, Adventure, Photography",October to April,Moderate,1
Colosseum,Rome,iconic ancient Roman amphitheatre,"Archaeology, guided tour, photography",Rome,Italy,Heritage,"Cultural, Photography","March to June, September to October",Premium,1
Fushimi Inari Taisha,Kyoto,Shinto shrine famous for thousands of torii gates,"Shrine visit, hiking, photography",Kyoto,Japan,Temple/Religious,"Spiritual, Cultural, Photography","March to May, October to November",Moderate,1
Nara Park,Nara,historic park with temples and free-roaming deer,"Temple visits, walking, photography",Nara,Japan,Garden/Nature,"Cultural, Family, Photography","March to May, October to November",Moderate,1
Nikko Toshogu Shrine,Tochigi,ornate shrine complex in cedar forests,"Shrine visit, heritage walk, photography",Tochigi,Japan,Temple/Religious,"Spiritual, Cultural, Photography",April to November,Moderate,1
Wadi Rum,Aqaba,dramatic desert of sandstone mountains and valleys,"Jeep safari, camel ride, camping, stargazing",Aqaba,Jordan,Mountain/Hill,"Adventure, Eco, Photography","March to May, September to November",Premium,2
Dead Sea,Madaba / Karak,hypersaline lake and wellness destination,"Floating, wellness, resort leisure, photography",Madaba / Karak,Jordan,Lake/Water,"Wellness, Leisure, Photography","March to May, September to November",Premium,1
Petra,Ma’an,Nabataean rock-cut archaeological city,"Archaeology, hiking, photography",Ma’an,Jordan,Heritage,"Cultural, Adventure, Photography","March to May, September to November",Premium,2
Diani Beach,Kwale,tropical beach on Kenya’s Indian Ocean coast,"Swimming, snorkeling, beach leisure, photography",Kwale,Kenya,Beach,"Beach, Leisure, Photography",June to October,Premium,2
Maasai Mara National Reserve,Narok,iconic savanna wildlife reserve and migration landscape,"Game drives, wildlife photography, cultural experiences",Narok,Kenya,Wildlife,"Eco, Adventure, Photography",July to October,Luxury,3
Andasibe-Mantadia National Park,Alaotra-Mangoro,rainforest known for lemurs and endemic species,"Trekking, wildlife watching, photography",Alaotra-Mangoro,Madagascar,Wildlife,"Eco, Adventure, Photography",April to October,Premium,2
Nosy Be,Diana,tropical island destination with beaches and marine life,"Snorkeling, diving, boat trips, beach leisure",Diana,Madagascar,Island,"Beach, Island, Photography",April to October,Premium,3
Avenue of the Baobabs,Menabe,iconic road lined by giant baobab trees,"Scenic drive, sunset photography, nature sightseeing",Menabe,Madagascar,Garden/Nature,"Eco, Photography",April to October,Premium,1
Langkawi Sky Bridge,Kedah,curved pedestrian bridge over rainforest and mountains,"Cable-car ride, viewpoints, photography",Kedah,Malaysia,Mountain/Hill,"Adventure, Photography",December to March,Premium,1
George Town,Penang,historic multicultural city with shophouses and street art,"Walking tour, food tourism, photography",Penang,Malaysia,Heritage,"Cultural, Food, Photography",December to March,Moderate,2
Baa Atoll,Baa Atoll,UNESCO biosphere reserve with rich marine life,"Snorkeling, diving, marine wildlife viewing",Baa Atoll,Maldives,Island,"Eco, Beach, Photography",November to April,Luxury,3
Hulhumalé,Kaafu Atoll,planned island city with beaches near Malé,"Beach walks, swimming, photography",Kaafu Atoll,Maldives,Island,"Beach, Leisure, Photography",November to April,Premium,1
Vaadhoo Island,Raa Atoll,island destination associated with bioluminescent waters,"Night beach viewing, snorkeling, photography",Raa Atoll,Maldives,Island,"Beach, Photography",November to April,Premium,2
Black River Gorges National Park,Black River,largest protected native forest area in Mauritius,"Hiking, birdwatching, nature photography",Black River,Mauritius,Wildlife,"Eco, Adventure, Photography",May to October,Moderate,2
Chamarel Seven Coloured Earth,Black River,geological landscape of multicolored dunes,"Nature sightseeing, photography, nearby waterfall visit",Black River,Mauritius,Garden/Nature,"Eco, Photography",May to October,Moderate,1
Le Morne Brabant,Black River,mountain and UNESCO cultural landscape overlooking a lagoon,"Hiking, viewpoint photography, beach leisure",Black River,Mauritius,Mountain/Hill,"Adventure, Beach, Photography",May to October,Premium,2
Mexico City Historic Center,Mexico City,dense historic district with Aztec and colonial heritage,"Walking tour, museums, architecture photography",Mexico City,Mexico,Heritage,"Cultural, Photography","March to May, October to November",Moderate,2
Tulum Archaeological Zone,Quintana Roo,Maya coastal ruins overlooking the Caribbean,"Archaeology, beach visit, photography",Quintana Roo,Mexico,Heritage,"Cultural, Beach, Photography",November to April,Moderate,1
Merzouga Dunes,Drâa-Tafilalet,Sahara sand-dune landscape near Erg Chebbi,"Camel safari, desert camping, stargazing",Drâa-Tafilalet,Morocco,Mountain/Hill,"Adventure, Eco, Photography",October to April,Premium,2
Marrakech Medina,Marrakesh-Safi,"historic medina with souks, riads and monuments","Souk shopping, walking tour, food exploration, photography",Marrakesh-Safi,Morocco,Heritage,"Cultural, Shopping, Food, Photography",October to April,Moderate,2
Chefchaouen,Tangier-Tetouan-Al Hoceima,blue-painted mountain town,"Town walk, shopping, photography",Tangier-Tetouan-Al Hoceima,Morocco,Heritage,"Cultural, Photography","March to May, September to November",Moderate,1
Annapurna Circuit,Gandaki Province,classic Himalayan trekking route,"Trekking, mountain photography, village tourism",Gandaki Province,Nepal,Mountain/Hill,"Adventure, Eco, Photography","October to November, March to April",Premium,8
Rijksmuseum,Amsterdam,major museum of Dutch art and history,"Museum visit, art appreciation, photography",Amsterdam,Netherlands,Heritage,"Cultural, Photography",Year-round,Premium,1
Keukenhof,Lisse,famous seasonal flower garden,"Garden walk, flower photography",Lisse,Netherlands,Garden/Nature,"Leisure, Photography",March to May,Moderate,1
Kinderdijk Windmills,South Holland,historic windmill landscape and water-management heritage,"Cycling, heritage walk, photography",South Holland,Netherlands,Heritage,"Eco, Cultural, Photography",April to October,Moderate,1
Tongariro National Park,Manawatū-Whanganui,volcanic mountains and alpine trekking,"Hiking, trekking, photography",Manawatū-Whanganui,New Zealand,Mountain/Hill,"Adventure, Eco, Photography",November to April,Moderate,2
Milford Sound,Southland,fjord with waterfalls and rainforest,"Cruise, kayaking, scenic flights, photography",Southland,New Zealand,Lake/Water,"Eco, Adventure, Photography",December to March,Premium,1
Geirangerfjord,Møre og Romsdal,dramatic fjord with waterfalls and mountain scenery,"Cruise, hiking, photography",Møre og Romsdal,Norway,Lake/Water,"Adventure, Eco, Photography",May to September,Premium,2
Trolltunga,Vestland,famous rock ledge above a lake,"Trekking, viewpoint photography",Vestland,Norway,Mountain/Hill,"Adventure, Photography",June to September,Premium,1
Wadi Shab,Al Sharqiyah,dramatic canyon and pools along the coast,"Hiking, swimming, canyon exploration, photography",Al Sharqiyah,Oman,Mountain/Hill,"Adventure, Eco, Photography",October to April,Moderate,1
Wahiba Sands,Al Wusta / North Ash Sharqiyah,vast golden desert dunes,"Dune safari, camel riding, camping, stargazing",Al Wusta / North Ash Sharqiyah,Oman,Mountain/Hill,"Adventure, Eco, Photography",October to March,Premium,2
Sultan Qaboos Grand Mosque,Muscat,major modern Islamic architectural landmark,"Mosque visit, architecture photography, cultural tourism",Muscat,Oman,Temple/Religious,"Spiritual, Cultural, Photography",October to April,Moderate,1
Nazca Lines,Ica,large geoglyphs etched across desert plains,"Scenic flight, archaeology, photography",Ica,Peru,Heritage,"Adventure, Cultural, Photography",April to November,Premium,1
Banaue Rice Terraces,Ifugao,mountain terraces cultivated for centuries,"Trekking, village tourism, photography",Ifugao,Philippines,Eco Tourism,"Eco, Cultural, Photography","March to May, November to April",Moderate,2
Tubbataha Reefs Natural Park,Palawan,marine protected area with exceptional coral reefs,"Scuba diving, marine wildlife viewing, photography",Palawan,Philippines,Wildlife,"Eco, Adventure, Photography",March to June,Luxury,3
Boracay,Western Visayas,famous white-sand beach island,"Swimming, water sports, sunset photography",Western Visayas,Philippines,Beach,"Beach, Leisure, Photography",November to May,Premium,3
Belém Tower,Lisbon,fortified waterfront tower from the Age of Discoveries,"Heritage walk, architecture photography, river views",Lisbon,Portugal,Heritage,"Cultural, Photography",March to October,Moderate,1
"Ribeira District, Porto",Porto,historic riverside quarter of colorful buildings,"Walking tour, food tourism, photography",Porto,Portugal,Heritage,"Cultural, Leisure, Photography",April to October,Moderate,2
Pena Palace,Sintra,romantic 19th-century palace set in wooded hills,"Palace tour, garden walk, photography",Sintra,Portugal,Heritage,"Cultural, Photography",March to October,Premium,1
Museum of Islamic Art,Doha,major museum of Islamic art on Doha’s waterfront,"Museum visit, art appreciation, photography",Doha,Qatar,Heritage,"Cultural, Photography",November to March,Premium,1
Souq Waqif,Doha,traditional market district with shops and restaurants,"Shopping, food exploration, cultural walk",Doha,Qatar,Shopping,"Cultural, Shopping, Food",November to March,Moderate,1
The Pearl-Qatar,Doha,luxury island development with marinas and promenades,"Waterfront walks, dining, shopping, photography",Doha,Qatar,Island,"Luxury, Leisure, Photography",November to March,Premium,1
AlUla Old Town,Al Madinah Region,historic mud-brick settlement surrounded by desert scenery,"Old-town walk, heritage tour, photography",Al Madinah Region,Saudi Arabia,Heritage,"Cultural, Photography",October to March,Premium,1
Hegra,Al Madinah Region,Nabataean rock-cut tombs in the AlUla landscape,"Archaeology, desert sightseeing, photography",Al Madinah Region,Saudi Arabia,Heritage,"Cultural, Adventure, Photography",October to March,Premium,1
Diriyah,Riyadh Region,historic birthplace of the first Saudi state,"Heritage walk, museums, cultural tourism",Riyadh Region,Saudi Arabia,Heritage,"Cultural, Photography",October to March,Premium,1
Anse Source d’Argent,La Digue,granite-framed beach with shallow turquoise water,"Swimming, cycling, beach photography",La Digue,Seychelles,Beach,"Beach, Leisure, Photography",May to October,Premium,1
Victoria,Mahé,small capital with colonial and Creole landmarks,"City walk, markets, photography, cultural tourism",Mahé,Seychelles,Heritage,"Cultural, Shopping, Photography",May to October,Premium,1
Vallée de Mai,Praslin,UNESCO-listed palm forest and endemic biodiversity,"Nature walk, birdwatching, photography",Praslin,Seychelles,Eco Tourism,"Eco, Photography",April to October,Premium,1
Merlion Park,Singapore,waterfront landmark featuring the Merlion statue,"Waterfront walk, city sightseeing, photography",Singapore,Singapore,Heritage,"Leisure, Photography",Year-round,Budget,1
Table Mountain,Western Cape,iconic flat-topped mountain overlooking Cape Town,"Cableway, hiking, viewpoints, photography",Western Cape,South Africa,Mountain/Hill,"Adventure, Photography",October to April,Premium,1
Garden Route,Western Cape / Eastern Cape,scenic coastal drive with forests and beaches,"Road trip, hiking, wildlife, photography",Western Cape / Eastern Cape,South Africa,Sightseeing,"Eco, Leisure, Photography",October to April,Premium,3
Jeju Island,Jeju,"volcanic island with beaches, lava tubes and scenic peaks","Hiking, coastal drives, photography, beach leisure",Jeju,South Korea,Island,"Eco, Adventure, Beach, Photography","April to June, September to November",Premium,3
Bukchon Hanok Village,Seoul,historic neighborhood of traditional Korean houses,"Walking tour, architecture photography, cultural tourism",Seoul,South Korea,Heritage,"Cultural, Photography","April to June, September to November",Budget,1
Gyeongbokgung Palace,Seoul,largest Joseon-era palace complex,"Palace tour, cultural dress experience, photography",Seoul,South Korea,Heritage,"Cultural, Photography","April to June, September to November",Moderate,1
Alhambra,Andalusia,Nasrid palace and fortress complex in Granada,"Palace tour, gardens, photography",Andalusia,Spain,Heritage,"Cultural, Photography","March to May, September to November",Premium,1
Park Güell,Catalonia,Gaudí park with mosaic architecture and city views,"Park walk, architecture photography, viewpoints",Catalonia,Spain,Garden/Nature,"Cultural, Photography","March to June, September to November",Moderate,1
Sagrada Família,Catalonia,Gaudí’s monumental basilica in Barcelona,"Architecture tour, photography, city sightseeing",Catalonia,Spain,Heritage,"Cultural, Photography","March to June, September to November",Premium,1
Abisko National Park,Norrbotten,Arctic mountain landscape and northern-lights destination,"Hiking, aurora watching, photography",Norrbotten,Sweden,Mountain/Hill,"Adventure, Eco, Photography",June to September,Premium,2
"Icehotel, Jukkasjärvi",Norrbotten,seasonal hotel built from snow and ice,"Ice-art viewing, winter experiences, photography",Norrbotten,Sweden,Heritage,"Adventure, Photography",December to March,Luxury,1
Gamla Stan,Stockholm,historic old town with medieval lanes,"Walking tour, museums, photography",Stockholm,Sweden,Heritage,"Cultural, Photography",May to September,Premium,1
Jungfraujoch,Bernese Alps,high-altitude Alpine viewpoint reached by mountain railway,"Mountain railway, snow viewing, photography",Bernese Alps,Switzerland,Mountain/Hill,"Adventure, Photography",May to October,Luxury,1
Matterhorn,Valais,iconic pyramid-shaped Alpine peak,"Mountain excursions, skiing, photography",Valais,Switzerland,Mountain/Hill,"Adventure, Photography",June to September,Premium,2
Lake Geneva,Vaud/Geneva,large Alpine lake surrounded by cities and mountains,"Boat cruise, lakeside walks, photography",Vaud/Geneva,Switzerland,Lake/Water,"Leisure, Photography",May to September,Premium,2
Ngorongoro Crater,Arusha,volcanic caldera with exceptional wildlife density,"Safari, wildlife viewing, photography",Arusha,Tanzania,Wildlife,"Eco, Adventure, Photography",June to October,Luxury,2
"Stone Town, Zanzibar",Zanzibar City,historic Swahili trading quarter,"Walking tour, spice/food experiences, photography",Zanzibar City,Tanzania,Heritage,"Cultural, Food, Photography",June to October,Premium,2
"Grand Palace, Bangkok",Bangkok,royal palace complex and major Bangkok landmark,"Palace tour, temple visit, photography",Bangkok,Thailand,Heritage,"Cultural, Photography",November to February,Moderate,1
Ayutthaya Historical Park,Phra Nakhon Si Ayutthaya,ruins of the historic Siamese capital,"Temple ruins, cycling, photography",Phra Nakhon Si Ayutthaya,Thailand,Heritage,"Cultural, Adventure, Photography",November to February,Budget,1
Hagia Sophia,Istanbul,landmark monument with Byzantine and Ottoman history,"Architecture tour, heritage photography, city sightseeing",Istanbul,Turkey,Heritage,"Cultural, Photography","April to May, September to October",Moderate,1
Ephesus,Izmir,major ancient Greco-Roman archaeological city,"Archaeology, guided tour, photography",Izmir,Turkey,Heritage,"Cultural, Photography","April to June, September to October",Moderate,1
Sheikh Zayed Grand Mosque,Abu Dhabi,grand white-marble mosque and architectural landmark,"Mosque visit, architecture photography, cultural tourism",Abu Dhabi,UAE,Temple/Religious,"Spiritual, Cultural, Photography",November to March,Premium,1
Burj Khalifa,Dubai,world-famous skyscraper and observation landmark,"Observation deck, city sightseeing, photography",Dubai,UAE,Heritage,"Luxury, Photography",November to March,Luxury,1
Statue of Liberty,New York,iconic harbor monument and symbol of New York,"Ferry ride, museum visit, city photography",New York,USA,Heritage,"Cultural, Photography",April to October,Premium,1
Cu Chi Tunnels,Ho Chi Minh City,wartime underground tunnel network,"History tour, museum visit, photography",Ho Chi Minh City,Vietnam,Heritage,"Cultural, Photography",December to April,Moderate,1"""

def append_to_csv(target_path: Path):
    if not target_path.exists():
        print(f"File not found: {target_path}")
        return

    # Read existing places
    existing_places = set()
    with open(target_path, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            place = row.get("Name of the Place", "").strip().lower()
            if place:
                existing_places.add(place)

    print(f"Target: {target_path} - Existing records: {len(existing_places)}")

    # Parse expansion CSV
    import io
    expansion_reader = csv.DictReader(io.StringIO(expansion_csv_text.strip()))
    
    added_count = 0
    new_rows = []
    for row in expansion_reader:
        place_clean = row["Name of the Place"].strip().lower()
        if place_clean not in existing_places:
            # Map fields to match target header
            formatted_row = {fn: row.get(fn, "") for fn in fieldnames}
            new_rows.append(formatted_row)
            existing_places.add(place_clean)
            added_count += 1

    print(f"Found {added_count} new unique records to append.")

    # Append to file
    with open(target_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        for r in new_rows:
            writer.writerow(r)

    print(f"Successfully appended {added_count} rows to {target_path}!")

def main():
    paths = [
        Path(r"d:\tripgenius\backend\tourism.csv"),
        Path(r"d:\tripgenius\database\tourism.csv")
    ]
    for p in paths:
        append_to_csv(p)

if __name__ == "__main__":
    main()
