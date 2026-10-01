export interface DayPlan {
  day: number;
  title?: string;
  theme?: string;
  morning?: string;
  afternoon?: string;
  evening?: string;
  activities?: string[];
  estimated_daily_cost?: number;
}

interface DestinationSchedule {
  themes: string[];
  days: Array<{
    theme: string;
    morning: string;
    afternoon: string;
    evening: string;
    activities: string[];
  }>;
}

const CURATED_DESTINATIONS: Record<string, DestinationSchedule> = {
  ooty: {
    themes: [
      "Botanical Wonders & Lake Horizons",
      "Tea Gardens, Pine Forests & Waterfalls",
      "UNESCO Toy Train & Nilgiri Peaks",
      "Avalanche Valley & Silent Lake Safari",
      "Tribal Heritage & Mudumalai Wildlife",
    ],
    days: [
      {
        theme: "Botanical Wonders & Lake Horizons",
        morning:
          "9:00 AM • Stroll through the historic Government Botanical Gardens (fossil tree trunk & 1,000+ exotic floral species). Head up to Doddabetta Peak (2,637m) for panoramic vistas of the Nilgiri hills.",
        afternoon:
          "1:30 PM • Authentic South Indian lunch or tea-estate bistro meal in Charing Cross. Visit the Ooty Thread Garden showcasing hand-crafted artificial flora.",
        evening:
          "5:00 PM • Peaceful pedal or motor boating on Ooty Lake as the mist rolls in, followed by homemade chocolate tasting and eucalyptus oil shopping along Commercial Road.",
        activities: ["Government Botanical Garden", "Doddabetta Peak", "Ooty Lake & Boathouse", "Homemade Chocolate Trail"],
      },
      {
        theme: "Tea Gardens, Pine Forests & Waterfalls",
        morning:
          "8:30 AM • Scenic drive to the 9th Mile Shooting Point and Wenlock Downs pine forest. Enjoy the crisp mountain breeze and photography amidst rolling meadows.",
        afternoon:
          "1:00 PM • Visit Pykara Lake & Waterfalls. Enjoy speedboating on the pristine reservoir, followed by lunch at the TTDC lakeside restaurant.",
        evening:
          "4:30 PM • Guided tour of the Ooty Tea Factory & The Tea Museum. Watch CTC tea processing live and sample piping-hot freshly brewed cardamom tea.",
        activities: ["Pykara Lake & Waterfalls", "9th Mile Pine Forest", "Wenlock Downs", "Ooty Tea Factory & Museum"],
      },
      {
        theme: "UNESCO Toy Train & Nilgiri Peaks",
        morning:
          "8:00 AM • Board the iconic Nilgiri Mountain Railway (Toy Train) from Ooty to Coonoor. Marvel at dramatic tunnels, viaducts, and valley views.",
        afternoon:
          "12:30 PM • Explore Sim's Park in Coonoor with its curated botanical species, followed by lunch featuring local Nilgiri badaga delicacies.",
        evening:
          "4:00 PM • Drive to Dolphin's Nose viewpoint overlooking Catherine Falls, then return to Ooty for a cozy café dinner with Nilgiri spiced coffee.",
        activities: ["Nilgiri Mountain Railway (Toy Train)", "Sim's Park Coonoor", "Dolphin's Nose Viewpoint", "Catherine Falls View"],
      },
      {
        theme: "Avalanche Valley & Silent Lake Safari",
        morning:
          "8:00 AM • Forest department safari through the protected Avalanche Forest Reserve. Spot wild deer and trout hatcheries nestled by pristine streams.",
        afternoon:
          "1:30 PM • Picnic lunch by the crystal-clear waters of Emerald Lake surrounded by rolling tea slopes and quiet silence.",
        evening:
          "5:30 PM • Sunset vista at Upper Bhavani approach, returning to Ooty town for hot dinner and bonfire relaxation.",
        activities: ["Avalanche Lake", "Emerald Lake", "Trout Hatchery", "Upper Bhavani Approach"],
      },
    ],
  },
  munnar: {
    themes: [
      "Endless Tea Hills & Nilgiri Tahr",
      "Lakes, Echoes & Cloud-Covered Peaks",
      "Cascading Waterfalls & Spice Trails",
      "Kolukkumalai Sunrise & Village Life",
    ],
    days: [
      {
        theme: "Endless Tea Hills & Nilgiri Tahr",
        morning:
          "7:30 AM • Early visit to Eravikulam National Park (Rajamalai) to spot the rare endangered Nilgiri Tahr against rolling shola-grassland hills.",
        afternoon:
          "1:00 PM • Explore the KDHP Tea Museum in Munnar town. Learn orthodox tea processing history and taste single-origin black and green teas.",
        evening:
          "4:30 PM • Stroll through Munnar flower garden and Pothamedu Viewpoint for an awe-inspiring sunset over endless tea-carpeted slopes.",
        activities: ["Eravikulam National Park", "KDHP Tea Museum", "Pothamedu Viewpoint", "Munnar Spice Market"],
      },
      {
        theme: "Lakes, Echoes & Cloud-Covered Peaks",
        morning:
          "9:00 AM • Drive along the scenic Mattupetty direction. Visit Mattupetty Dam for speedboating and peaceful water reflections.",
        afternoon:
          "1:00 PM • Shout across the scenic Echo Point surrounded by eucalyptus groves, followed by shikara pedal boating at Kundala Lake.",
        evening:
          "4:30 PM • Ascend towards Top Station (historic transshipment point for tea) to witness the clouds floating beneath your feet into Tamil Nadu valleys.",
        activities: ["Mattupetty Dam", "Echo Point", "Kundala Lake", "Top Station Viewpoint"],
      },
      {
        theme: "Cascading Waterfalls & Spice Trails",
        morning:
          "8:30 AM • Guided trek down to Attukad Waterfalls through mist-veiled mountain paths and blooming wild orchids.",
        afternoon:
          "1:00 PM • Traditional Kerala banana leaf sadhya lunch with authentic red matta rice, avial, and spicy rasam.",
        evening:
          "3:30 PM • Visit a certified organic spice plantation to learn cardamom, black pepper, clove, and vanilla cultivation, followed by Kathakali/Kalaripayattu cultural performance.",
        activities: ["Attukad Waterfalls", "Spice Plantation Walk", "Punadaran Kathakali Centre", "Local Tea Tasting"],
      },
    ],
  },
  varkala: {
    themes: [
      "Cliffside Vistas & Holy Springs",
      "Backwaters Kayaking & Ancient Heritage",
      "Coastal Forts, Lighthouses & Sunset Shacks",
    ],
    days: [
      {
        theme: "Cliffside Vistas & Holy Springs",
        morning:
          "8:00 AM • Morning cliff walk along the red laterite geological formation overlooking the turquoise Arabian Sea. Sacred dip at Papanasam Beach.",
        afternoon:
          "1:00 PM • Fresh smoothie bowls and wood-fired pizza at cliffside cafes (Darjeeling Cafe / Cafe del Mar).",
        evening:
          "5:00 PM • Unwind on Black Sand Beach (Odayam) watching the golden sun dip into the horizon, followed by candlelit seafood dinner on North Cliff.",
        activities: ["North Cliff Walk", "Papanasam Beach", "Odayam Black Sand Beach", "Cliffside Cafe Dining"],
      },
      {
        theme: "Backwaters Kayaking & Ancient Heritage",
        morning:
          "8:30 AM • Peaceful kayaking or canoe ride through the mangrove corridors of Kappil Beach & Edava backwaters where the lake meets the sea.",
        afternoon:
          "1:30 PM • Traditional Malabar seafood curry meal with appams, followed by coconut water by the estuary.",
        evening:
          "4:30 PM • Darshan at the 2,000-year-old Janardhana Swamy Temple with its sacred temple pond, followed by golden hour meditation.",
        activities: ["Kappil Lake & Beach", "Edava Mangrove Kayaking", "Janardhana Swamy Temple", "South Cliff Serenity"],
      },
      {
        theme: "Coastal Forts, Lighthouses & Sunset Shacks",
        morning:
          "9:00 AM • Historical exploration of 17th-century Anjengo (Anchuthengu) Fort and climb the historic Anjengo Lighthouse for a 360° coastal view.",
        afternoon:
          "1:30 PM • Traditional coastal meals at a local fishermens wharf eatery, followed by an Ayurvedic massage or yoga rejuvenation session.",
        evening:
          "5:30 PM • Golden hour cliff acoustic music session, watching dolphins offshore and souvenir shopping for Tibetan crafts.",
        activities: ["Anjengo Fort & Lighthouse", "Ayurvedic Spa Session", "Cliff Acoustic Sundowner", "Beachside Yoga"],
      },
    ],
  },
  thenkasi: {
    themes: [
      "Herbal Waterfalls & Pandyan Heritage",
      "Five Falls & Western Ghats Reservoirs",
      "Spice Orchards & Border Culinary Trail",
    ],
    days: [
      {
        theme: "Herbal Waterfalls & Pandyan Heritage",
        morning:
          "7:00 AM • Invigorating natural herbal hydrotherapy bath at Courtallam Main Falls (Peraruvi). Rejuvenating mountain waters flowing over medicinal plants.",
        afternoon:
          "1:00 PM • Authentic hot parotta with spicy salna lunch, followed by darshan at the 13th-century Kasi Viswanathar Temple with its 180-ft Rajagopuram.",
        evening:
          "5:00 PM • Leisurely walk through Old Courtallam (Pazhaya Courtallam) and Tiger Falls, savoring fresh jackfruit, rambutan, and wild forest honey.",
        activities: ["Courtallam Main Falls", "Kasi Viswanathar Temple", "Old Courtallam Falls", "Ayikudi Guava Groves"],
      },
      {
        theme: "Five Falls & Western Ghats Reservoirs",
        morning:
          "6:30 AM • Early morning bath at the five cascading streams of Five Falls (Aintharuvi) before the Saaral season crowds arrive.",
        afternoon:
          "12:30 PM • Scenic drive through Sengottai into the rubber estates of Gundar Dam reservoir. Enjoy the cool breeze and peaceful mountain backdrop.",
        evening:
          "5:30 PM • Legendary pepper chicken and country chicken fry dinner at Border Rahmath Hotel in Shenkottai, accompanied by Tirunelveli halwa.",
        activities: ["Five Falls (Aintharuvi)", "Gundar Dam & Reservoir", "Shenkottai Border Food Trail", "Herbal Sukku Kaapi"],
      },
    ],
  },
  paris: {
    themes: [
      "Iconic Monuments & Seine River Cruise",
      "Louvre Treasures & Montmartre Artists",
      "Palace of Versailles & Latin Quarter Bistro",
    ],
    days: [
      {
        theme: "Iconic Monuments & Seine River Cruise",
        morning:
          "9:00 AM • Ascend the Eiffel Tower summit or 2nd floor for spectacular panoramas of Paris. Walk along Champ de Mars gardens.",
        afternoon:
          "1:00 PM • Stroll down Avenue des Champs-Élysées towards the Arc de Triomphe. Café lunch with fresh croissants and café au lait.",
        evening:
          "6:00 PM • One-hour scenic Bateaux Parisiens boat cruise along the Seine River, viewing illuminated bridges and Notre-Dame Cathedral.",
        activities: ["Eiffel Tower", "Champ de Mars", "Arc de Triomphe", "Seine River Cruise"],
      },
      {
        theme: "Louvre Treasures & Montmartre Artists",
        morning:
          "9:00 AM • Explore the world's greatest art museum, the Louvre (Mona Lisa, Winged Victory, Venus de Milo, Tuileries Garden).",
        afternoon:
          "1:30 PM • Lunch in the historic Le Marais neighborhood, followed by a visit to Île de la Cité and Sainte-Chapelle's stained glass windows.",
        evening:
          "5:00 PM • Climb Montmartre hill to the Basilica of Sacré-Cœur for golden hour sunsets overlooking Paris, followed by dinner in Place du Tertre.",
        activities: ["Louvre Museum", "Tuileries Garden", "Sacré-Cœur Basilica", "Montmartre Art Walk"],
      },
      {
        theme: "Palace of Versailles & Latin Quarter Bistro",
        morning:
          "8:30 AM • Day excursion to the magnificent Palace of Versailles. Explore the Hall of Mirrors, the King's Grand Apartments, and fountains.",
        afternoon:
          "1:30 PM • Rent a rowboat on the Grand Canal of Versailles, then stroll through the Queen's Hamlet (Le Hameau de la Reine).",
        evening:
          "6:30 PM • Return to Paris for evening exploration of the Latin Quarter and Shakespeare and Company bookstore, ending with a fondue dinner.",
        activities: ["Palace of Versailles", "Hall of Mirrors", "Versailles Grand Canal", "Latin Quarter Bistro"],
      },
    ],
  },
  goa: {
    themes: [
      "Historic Forts & Lively Coastal Vibes",
      "UNESCO Heritage Churches & Portuguese Alleys",
      "South Goa Serenity & Scenic Shacks",
    ],
    days: [
      {
        theme: "Historic Forts & Lively Coastal Vibes",
        morning:
          "9:00 AM • Visit 17th-century Aguada Fort and lighthouse overlooking the Arabian Sea, followed by Sinquerim beach walk.",
        afternoon:
          "1:00 PM • Beach shack lunch with fresh catch Goan fish curry and prawn balchao in Candolim or Calangute.",
        evening:
          "5:00 PM • Vibrant sunset vibe at Anjuna or Vagator beach cliffs, followed by evening curio shopping at flea markets.",
        activities: ["Aguada Fort & Lighthouse", "Candolim Beach", "Vagator Clifftop", "Goan Fish Curry Lunch"],
      },
      {
        theme: "UNESCO Heritage Churches & Portuguese Alleys",
        morning:
          "9:00 AM • Discover Old Goa's UNESCO heritage: Basilica of Bom Jesus (relics of St. Francis Xavier) and Se Cathedral.",
        afternoon:
          "1:00 PM • Guided heritage stroll through Fontainhas (Latin Quarter in Panaji) with colorful Portuguese villas and bakeries.",
        evening:
          "5:30 PM • Sunset river cruise on the Mandovi River with traditional Goan folk performances and live music.",
        activities: ["Basilica of Bom Jesus", "Se Cathedral", "Fontainhas Latin Quarter", "Mandovi River Cruise"],
      },
      {
        theme: "South Goa Serenity & Scenic Shacks",
        morning:
          "8:30 AM • Drive south to the crescent-shaped paradise of Palolem Beach for dolphin spotting and serene swimming.",
        afternoon:
          "1:30 PM • Scenic lunch at Cabo de Rama cliff restaurant overlooking the turquoise bay.",
        evening:
          "5:00 PM • Sunset drinks at Colva beach shack and peaceful evening walk on white sands.",
        activities: ["Palolem Beach", "Cabo de Rama Fort", "Dolphin Spotting", "Sunset Shack Relax"],
      },
    ],
  },
};

/**
 * Synthesizes a structured DayPlan array for any destination and duration.
 */
export function generateRichDayPlans(
  destination: string,
  duration_days: number = 3,
  interests: string[] = ["Sightseeing"],
  travel_style: string = "Balanced",
  attractions: string[] = [],
  budget: number = 25000
): DayPlan[] {
  const destClean = (destination || "").trim();
  const destLower = destClean.toLowerCase();
  const daysCount = Math.max(1, duration_days);

  // Look up curated destination presets
  const curatedKey = Object.keys(CURATED_DESTINATIONS).find(
    (k) => destLower.includes(k) || k.includes(destLower)
  );

  const curated = curatedKey ? CURATED_DESTINATIONS[curatedKey] : null;

  const result: DayPlan[] = [];
  const dailyCost = Math.round(budget / daysCount);

  for (let i = 1; i <= daysCount; i++) {
    if (curated && curated.days[i - 1]) {
      const cDay = curated.days[i - 1];
      result.push({
        day: i,
        title: cDay.theme,
        theme: cDay.theme,
        morning: cDay.morning,
        afternoon: cDay.afternoon,
        evening: cDay.evening,
        activities: cDay.activities,
        estimated_daily_cost: dailyCost,
      });
    } else {
      // Dynamic synthesis using destination name and available attractions/interests
      const attrPool =
        attractions && attractions.length > 0
          ? attractions
          : [
              `${destClean} Heritage Landmark`,
              `${destClean} Scenic Viewpoint`,
              `${destClean} Nature & Botanical Trail`,
              `${destClean} Artisan Market & Craft Center`,
              `${destClean} Cultural Museum`,
              `${destClean} Lake & Sunset Promenade`,
            ];

      const a1 = attrPool[(i * 3 - 3) % attrPool.length];
      const a2 = attrPool[(i * 3 - 2) % attrPool.length];
      const a3 = attrPool[(i * 3 - 1) % attrPool.length];

      let theme = `Signature Highlights & Scenic Landmarks`;
      if (i === 1) theme = `Arrival & Signature ${destClean} Landmarks`;
      else if (i === 2) theme = `Nature Trails, Culture & Local Flavors`;
      else if (i === 3) theme = `Panoramic Viewpoints & Sunset Trails`;
      else if (i === 4) theme = `Hidden Gems & Artisan Heritage`;
      else theme = `Leisure Discovery & Memorable Farewell`;

      result.push({
        day: i,
        title: theme,
        theme: theme,
        morning: `8:30 AM • Morning exploration at ${a1}. Enjoy the fresh morning atmosphere, photography, and guided walking tour through key historical landmarks.`,
        afternoon: `1:00 PM • Traditional regional lunch at a popular local eatery, followed by an afternoon visit to ${a2} with cultural immersion.`,
        evening: `5:00 PM • Sunset viewing and promenade stroll around ${a3}, followed by local souvenir shopping and dinner featuring authentic ${destClean} dishes.`,
        activities: [a1, a2, a3],
        estimated_daily_cost: dailyCost,
      });
    }
  }

  return result;
}

/**
 * Validates and repairs any trip object so that `ai_itinerary` has rich DayPlans.
 */
export function ensureTripItinerary(trip: any): any {
  if (!trip) return trip;

  const itin = trip.ai_itinerary;
  const hasValidItinerary =
    Array.isArray(itin) &&
    itin.length > 0 &&
    itin.some((d: any) => d && (d.morning || d.afternoon || d.evening || d.theme));

  if (!hasValidItinerary) {
    const richItin = generateRichDayPlans(
      trip.destination || "Destination",
      trip.duration_days || 3,
      trip.interests || ["Sightseeing"],
      trip.travel_style || "Balanced",
      trip.attractions || [],
      trip.budget || 25000
    );
    trip.ai_itinerary = richItin;
  }

  return trip;
}

/**
 * Accurately maps any destination name (case-insensitive, substring-aware)
 * to its verified photograph, avoiding duplicate/incorrect fallbacks.
 */
export function getDestinationImage(destination?: string): string {
  if (!destination) return "/destinations/travel.jpg";
  const clean = destination.toLowerCase().trim();

  if (
    clean.includes("varanasi") ||
    clean.includes("kashi") ||
    clean.includes("benaras") ||
    clean.includes("benares") ||
    clean.includes("banaras")
  ) {
    return "/destinations/varanasi.jpg";
  }
  if (clean.includes("ooty") || clean.includes("nilgiri")) return "/destinations/ooty.jpg";
  if (clean.includes("varkala")) return "/destinations/varkala.jpg";
  if (clean.includes("delhi")) return "/destinations/delhi.jpg";
  if (clean.includes("munnar")) return "/destinations/munnar.jpg";
  if (clean.includes("goa")) return "/destinations/goa.jpg";
  if (clean.includes("paris") || clean.includes("france")) return "/destinations/paris.jpg";
  if (clean.includes("tokyo") || clean.includes("japan")) return "/destinations/tokyo.jpg";
  if (clean.includes("bali") || clean.includes("indonesia")) return "/destinations/bali.jpg";
  if (clean.includes("dubai") || clean.includes("uae")) return "/destinations/dubai.jpg";
  if (
    clean.includes("thenkasi") ||
    clean.includes("tenkasi") ||
    clean.includes("courtallam") ||
    clean.includes("kutralam")
  ) {
    return "/destinations/thenkasi.jpg";
  }
  if (clean.includes("coorg") || clean.includes("madikeri") || clean.includes("kodagu")) {
    return "/destinations/coorg.jpg";
  }
  if (clean.includes("kodaikanal") || clean.includes("kodai")) return "/destinations/kodaikanal.jpg";
  if (clean.includes("alleppey") || clean.includes("alappuzha")) return "/destinations/alleppey.jpg";
  if (clean.includes("wayanad")) return "/destinations/wayanad.jpg";
  if (clean.includes("mysore") || clean.includes("mysuru")) return "/destinations/mysore.jpg";
  if (clean.includes("hampi")) return "/destinations/hampi.jpg";
  if (clean.includes("gokarna")) return "/destinations/gokarna.jpg";
  if (clean.includes("thekkady")) return "/destinations/thekkady.jpg";
  if (clean.includes("kovalam")) return "/destinations/kovalam.jpg";
  if (clean.includes("manali")) return "/destinations/manali.jpg";

  return "/destinations/travel.jpg";
}
