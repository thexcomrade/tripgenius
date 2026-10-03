/**
 * Transit Pricing & Route Intelligence Engine
 * Computes realistic travel distance, minimum ticket charges, and approximate fares
 * for trains (Sleeper, 3AC, 2AC), flights, express buses, and cabs across India & worldwide.
 */

export interface TransitPricingDetails {
  origin: string;
  destination: string;
  distanceKm: number;
  isSameCity: boolean;
  isInternational: boolean;
  train: {
    available: boolean;
    sleeperMinFare: number;
    sleeperMaxFare: number;
    threeTierAcMin: number;
    threeTierAcMax: number;
    twoTierAcMin: number;
    twoTierAcMax: number;
    approxDurationHours: number;
    note: string;
  };
  flight: {
    available: boolean;
    economyMinFare: number;
    economyMaxFare: number;
    approxDurationHours: number;
    note: string;
  };
  bus: {
    available: boolean;
    nonAcMinFare: number;
    acSleeperMinFare: number;
    approxDurationHours: number;
  };
  car: {
    fuelAndTollsApprox: number;
    recommendedVehicle: string;
    drivingHours: number;
  };
}

// Major travel hubs and tourism destinations with geographical coordinates
const CITY_COORDINATES: Record<string, { lat: number; lng: number }> = {
  // Kerala
  trivandrum: { lat: 8.5241, lng: 76.9366 },
  thiruvananthapuram: { lat: 8.5241, lng: 76.9366 },
  tvm: { lat: 8.5241, lng: 76.9366 },
  ernakulam: { lat: 9.9816, lng: 76.2999 },
  kochi: { lat: 9.9816, lng: 76.2999 },
  cochin: { lat: 9.9816, lng: 76.2999 },
  calicut: { lat: 11.2588, lng: 75.7804 },
  kozhikode: { lat: 11.2588, lng: 75.7804 },
  kollam: { lat: 8.8932, lng: 76.6141 },
  thrissur: { lat: 10.5276, lng: 76.2144 },
  kannur: { lat: 11.8745, lng: 75.3704 },
  munnar: { lat: 10.0889, lng: 77.0595 },
  varkala: { lat: 8.7379, lng: 76.7163 },
  wayanad: { lat: 11.6854, lng: 76.132 },
  alleppey: { lat: 9.4981, lng: 76.3388 },
  alappuzha: { lat: 9.4981, lng: 76.3388 },
  thekkady: { lat: 9.6031, lng: 77.1615 },
  vattappara: { lat: 8.601, lng: 76.981 },
  kovalam: { lat: 8.4021, lng: 76.9787 },

  // South India
  bangalore: { lat: 12.9716, lng: 77.5946 },
  bengaluru: { lat: 12.9716, lng: 77.5946 },
  chennai: { lat: 13.0827, lng: 80.2707 },
  hyderabad: { lat: 17.385, lng: 78.4867 },
  mysore: { lat: 12.2958, lng: 76.6394 },
  ooty: { lat: 11.4102, lng: 76.695 },
  coorg: { lat: 12.3375, lng: 75.8069 },
  kodaikanal: { lat: 10.2381, lng: 77.4892 },
  thenkasi: { lat: 8.9594, lng: 77.3152 },
  courtallam: { lat: 8.9317, lng: 77.275 },
  hampi: { lat: 15.335, lng: 76.46 },
  gokarna: { lat: 14.5479, lng: 74.3188 },
  madurai: { lat: 9.9252, lng: 78.1198 },
  coimbatore: { lat: 11.0168, lng: 76.9558 },

  // North & Central India
  varanasi: { lat: 25.3176, lng: 82.9739 },
  kashi: { lat: 25.3176, lng: 82.9739 },
  delhi: { lat: 28.6139, lng: 77.209 },
  newdelhi: { lat: 28.6139, lng: 77.209 },
  mumbai: { lat: 19.076, lng: 72.8777 },
  pune: { lat: 18.5204, lng: 73.8567 },
  goa: { lat: 15.2993, lng: 74.124 },
  jaipur: { lat: 26.9124, lng: 75.7873 },
  manali: { lat: 32.2432, lng: 77.1892 },
  shimla: { lat: 31.1048, lng: 77.1734 },
  rishikesh: { lat: 30.0869, lng: 78.2676 },
  agra: { lat: 27.1767, lng: 78.0081 },
  amritsar: { lat: 31.634, lng: 74.8723 },
  kolkata: { lat: 22.5726, lng: 88.3639 },
  darjeeling: { lat: 27.041, lng: 88.2663 },
  gangtok: { lat: 27.3389, lng: 88.6065 },
  ladakh: { lat: 34.1526, lng: 77.5771 },
  leh: { lat: 34.1526, lng: 77.5771 },
  srinagar: { lat: 34.0837, lng: 74.7973 },

  // International
  dubai: { lat: 25.2048, lng: 55.2708 },
  paris: { lat: 48.8566, lng: 2.3522 },
  tokyo: { lat: 35.6762, lng: 139.6503 },
  bali: { lat: -8.4095, lng: 115.1889 },
  bangkok: { lat: 13.7563, lng: 100.5018 },
  singapore: { lat: 1.3521, lng: 103.8198 },
};

/**
 * Calculates Haversine distance between two coordinates in kilometers
 */
function calculateHaversineDistance(
  lat1: number,
  lon1: number,
  lat2: number,
  lon2: number
): number {
  const R = 6371; // Earth's radius in km
  const dLat = ((lat2 - lat1) * Math.PI) / 180;
  const dLon = ((lon2 - lon1) * Math.PI) / 180;
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos((lat1 * Math.PI) / 180) *
      Math.cos((lat2 * Math.PI) / 180) *
      Math.sin(dLon / 2) *
      Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return Math.round(R * c);
}

/**
 * Finds coordinate matching query string
 */
function findCoordinates(query: string): { lat: number; lng: number } | null {
  if (!query) return null;
  const clean = query.toLowerCase().replace(/[^a-z0-9]/g, "");
  for (const [key, coords] of Object.entries(CITY_COORDINATES)) {
    if (clean.includes(key) || key.includes(clean)) {
      return coords;
    }
  }
  return null;
}

/**
 * Computes realistic transit pricing intelligence between origin and destination
 */
export function calculateTransitPricing(
  origin: string,
  destination: string
): TransitPricingDetails {
  const origClean = (origin || "Kochi").trim();
  const destClean = (destination || "Munnar").trim();

  const origCoords = findCoordinates(origClean);
  const destCoords = findCoordinates(destClean);

  let rawDistance = 250; // default regional fallback
  if (origCoords && destCoords) {
    rawDistance = calculateHaversineDistance(
      origCoords.lat,
      origCoords.lng,
      destCoords.lat,
      destCoords.lng
    );
  } else {
    // Keyword heuristics if coordinates are not in the primary map
    const origLower = origClean.toLowerCase();
    const destLower = destClean.toLowerCase();
    const isSouthOrigin = /kerala|ernakulam|kochi|tvm|trivandrum|bangalore|chennai|calicut|kollam|kannur/i.test(origLower);
    const isNorthDest = /varanasi|delhi|manali|kashi|jaipur|agra|shimla|amritsar/i.test(destLower);
    
    if (isSouthOrigin && isNorthDest) {
      rawDistance = 2400; // ~2400 km
    } else if (isSouthOrigin && /goa|mumbai|pune/i.test(destLower)) {
      rawDistance = 850;
    } else if (isSouthOrigin && /munnar|ooty|wayanad|kodaikanal|coorg/i.test(destLower)) {
      rawDistance = 140;
    }
  }

  const origLower = origClean.toLowerCase();
  const destLower = destClean.toLowerCase();

  const INTERNATIONAL_KEYWORDS = [
    "paris", "france", "london", "uk", "england", "dubai", "uae", "tokyo", "japan",
    "bali", "indonesia", "bangkok", "phuket", "thailand", "singapore",
    "new york", "nyc", "usa", "san francisco", "switzerland", "zurich",
    "rome", "italy", "barcelona", "spain", "amsterdam", "netherlands",
    "sydney", "melbourne", "australia", "kuala lumpur", "malaysia",
    "maldives", "male", "colombo", "sri lanka", "kathmandu", "nepal",
    "berlin", "germany", "cairo", "egypt", "doha", "qatar", "toronto", "canada"
  ];

  const isDestInternational = INTERNATIONAL_KEYWORDS.some(
    (kw) => destLower.includes(kw) || kw.includes(destLower)
  );
  const isOrigInternational = INTERNATIONAL_KEYWORDS.some(
    (kw) => origLower.includes(kw) || kw.includes(origLower)
  );

  const isInternational = isDestInternational || isOrigInternational || rawDistance > 3200;

  // Multiply by road/rail winding factor (1.20)
  const distanceKm = Math.max(25, Math.round(rawDistance * 1.2));
  const isSameCity = distanceKm < 40 && !isInternational;

  // 1. Train Calculations (modeled on IRCTC fare slabs)
  const isTrainFeasible = !isInternational && distanceKm >= 45 && distanceKm <= 3500;
  const sleeperMinFare = isSameCity || isInternational
    ? 0
    : Math.max(160, Math.round(distanceKm * 0.42));
  const sleeperMaxFare = Math.round(sleeperMinFare * 1.15);
  const threeTierAcMin = isSameCity || isInternational
    ? 0
    : Math.max(540, Math.round(distanceKm * 1.05));
  const threeTierAcMax = Math.round(threeTierAcMin * 1.15);
  const twoTierAcMin = isSameCity || isInternational
    ? 0
    : Math.max(820, Math.round(distanceKm * 1.55));
  const twoTierAcMax = Math.round(twoTierAcMin * 1.15);
  const approxTrainDuration = isInternational ? 0 : Math.max(1, Math.round(distanceKm / 55));

  // 2. Flight Calculations
  const isFlightFeasible = isInternational || distanceKm >= 350;
  let flightMin = 2800;
  let flightMax = 4500;
  let flightHours = Math.max(1, Math.round(distanceKm / 550) + 1);

  if (isInternational) {
    if (/paris|france|london|uk|europe|rome|zurich|amsterdam|berlin/i.test(destLower)) {
      flightMin = 38000;
      flightMax = 58000;
      flightHours = 11;
    } else if (/dubai|uae|doha|qatar/i.test(destLower)) {
      flightMin = 16000;
      flightMax = 24000;
      flightHours = 4;
    } else if (/singapore|bangkok|thailand|bali|indonesia|malaysia/i.test(destLower)) {
      flightMin = 17000;
      flightMax = 28000;
      flightHours = 6;
    } else if (/usa|new york|nyc|canada|toronto|tokyo|japan|australia/i.test(destLower)) {
      flightMin = 65000;
      flightMax = 95000;
      flightHours = 17;
    } else {
      flightMin = Math.max(22000, Math.round(distanceKm * 4.2));
      flightMax = Math.round(flightMin * 1.4);
      flightHours = Math.max(4, Math.round(distanceKm / 700) + 2);
    }
  } else if (distanceKm > 1500) {
    flightMin = 6500;
    flightMax = 9500;
  } else if (distanceKm > 800) {
    flightMin = 4200;
    flightMax = 6800;
  }

  // 3. Express Bus Calculations
  const isBusFeasible = !isInternational && distanceKm <= 1200;
  const busMin = isSameCity || isInternational ? 50 : Math.max(140, Math.round(distanceKm * 1.15));
  const busSleeper = isSameCity || isInternational
    ? 100
    : Math.max(260, Math.round(distanceKm * 1.65));
  const busDuration = isInternational ? 0 : Math.max(1, Math.round(distanceKm / 42));

  // 4. Car / Taxi Calculations
  const fuelAndTolls = isSameCity || isInternational
    ? 500
    : Math.round(distanceKm * 9.5 + (distanceKm > 100 ? (distanceKm / 80) * 120 : 0));
  const drivingHours = isInternational ? 0 : Math.max(1, Math.round(distanceKm / 48));

  return {
    origin: origClean,
    destination: destClean,
    distanceKm,
    isSameCity,
    isInternational,
    train: {
      available: isTrainFeasible,
      sleeperMinFare,
      sleeperMaxFare,
      threeTierAcMin,
      threeTierAcMax,
      twoTierAcMin,
      twoTierAcMax,
      approxDurationHours: approxTrainDuration,
      note: isInternational
        ? "No rail service across continents / oceans (Intercontinental route)"
        : isTrainFeasible
          ? `Direct / Express rail connecting ${origClean} to ${destClean}`
          : "Local road transit recommended",
    },
    flight: {
      available: isFlightFeasible,
      economyMinFare: flightMin,
      economyMaxFare: flightMax,
      approxDurationHours: flightHours,
      note: isInternational
        ? `International flight connecting nearest global airport hubs (e.g. COK ➔ CDG)`
        : isFlightFeasible
          ? `Connecting major airport hubs nearest to ${origClean} and ${destClean}`
          : "Short regional distance — rail or road preferred",
    },
    bus: {
      available: isBusFeasible,
      nonAcMinFare: busMin,
      acSleeperMinFare: busSleeper,
      approxDurationHours: busDuration,
    },
    car: {
      fuelAndTollsApprox: fuelAndTolls,
      recommendedVehicle: isInternational
        ? "Not applicable for overseas journey"
        : distanceKm > 400 ? "Sedan / SUV with Highway Fastag" : "Hatchback / Sedan",
      drivingHours,
    },
  };
}
