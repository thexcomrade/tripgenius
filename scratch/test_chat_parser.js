const text = `Here is your tailored **3-Day Vattappara Travel Blueprint**:

### 🗓️ Curated 3-Day Itinerary
• **Day 1: Arrival & Local Immersion** — Check in, explore central heritage streets, enjoy local sunset viewpoints and authentic regional dinner.
• **Day 2: Iconic Landmarks & Scenic Exploration** — Guided exploration of prime natural and architectural wonders, panoramic photo stops, and signature cultural visits.
• **Day 3: Offbeat Trails & Cuisine** — Discover hidden nature trails, local artisan markets, and heritage dining.

### 🏨 Stays & Dining
• Boutique stays & eco-resorts: ~₹2,200 – ₹4,500/night
• Authentic regional delicacies, fresh thalis, and local street treats

### 💰 Estimated Budget
• ~₹2,000 – ₹4,000 per person per day (covering stay, meals, and local transit in ₹)

Would you like me to refine this with specific hotel options or flight/train transit details?`;

// 1. Title & Destination Extraction:
let title = "";
let dest = "";

// A. Check for bold title in first 3 lines (e.g. **3-Day Vattappara Travel Blueprint**)
const boldTitleMatch = text.match(/\*\*(?:(\d+)[-–\s]*Day\s+)?([A-Za-z0-9\s\-]+?)\s*(?:Travel Blueprint|Itinerary|Trip|Tour)\*\*/i);
if (boldTitleMatch) {
  dest = boldTitleMatch[2].trim();
  title = `${dest}: ${boldTitleMatch[1] || '3'}-Day Travel Blueprint`;
}

// B. Check ### header if not found
if (!dest) {
  const h3Match = text.match(/###\s*[^\w\s]*\s*([A-Za-z0-9\s\-]+?)(?:[:–\-(]|$)/);
  if (h3Match && h3Match[1] && !/^(?:curated|itinerary|day|stays|estimated)/i.test(h3Match[1].trim())) {
    dest = h3Match[1].trim();
  }
}

// C. Fallback: search known destinations
if (!dest) {
  const keywords = ["Vattappara", "Vattavada", "Manali", "Varanasi", "Munnar", "Thenkasi", "Goa", "Ooty", "Coorg", "Wayanad", "Kodaikanal"];
  dest = keywords.find(k => text.toLowerCase().includes(k.toLowerCase())) || "Travel";
}

console.log('Extracted Dest:', dest);
console.log('Extracted Title:', title);

// 2. Stays & Dining from ### Stays & Dining:
const hotels = [];
const restaurants = [];
const cuisines = [];

const staysBlock = text.match(/###[^\n]*Stays\s*&\s*Dining[\s\S]*?(?=\n\s*###|\n\s*Would you|$)/i);
if (staysBlock) {
  const lines = staysBlock[0].split('\n');
  for (const l of lines) {
    const clean = l.replace(/^[•*\-\s]+/, '').replace(/[*_#`~]/g, '').trim();
    if (/stays|resort|hotel|cottage|homestay/i.test(clean)) {
      hotels.push(clean);
    } else if (/delicac|thali|cuisine|food|dish|treat/i.test(clean)) {
      cuisines.push(clean);
    }
  }
}
console.log('Hotels from block:', hotels);
console.log('Cuisines from block:', cuisines);

// 3. Days parsing:
const daySections = [];
const lines = text.split('\n');
let currentDay = null;
let currentSlot = null;
let parsingDays = true;

for (const rawLine of lines) {
  const line = rawLine.trim();

  // Stop markers
  if (/^(?:###|\*\*|---\s*$)?\s*(?:Recommended Stays|Stays\s*&|Authentic Regional|Must-Try|Local Eateries|Estimated Budget|Budget|PADAYAPPA'S|Cost Breakdown|Weather)/i.test(line)) {
    if (currentDay) {
      daySections.push(currentDay);
      currentDay = null;
    }
    parsingDays = false;
    continue;
  }

  const dMatch = line.match(/^[•*\-\s]*(?:###\s*)?(?:\*{1,2})?Day\s*(\d+)\s*[:–-]?\s*([^*\n—]+)?(?:\*{1,2})?(?:\s*[—–-]\s*(.*))?/i);
  if (dMatch) {
    parsingDays = true;
    if (currentDay) daySections.push(currentDay);
    const dNum = parseInt(dMatch[1], 10);
    const dTitle = (dMatch[2] || `Day ${dNum} Exploration`).replace(/[*_#`~]/g, '').trim();
    const dDesc = dMatch[3] ? dMatch[3].replace(/[*_#`~]/g, '').trim() : '';

    currentDay = {
      day: dNum,
      theme: dTitle,
      morning: dDesc || "",
      afternoon: "",
      evening: "",
      activities: dDesc ? [dDesc] : []
    };
    currentSlot = null;
    continue;
  }

  if (!parsingDays || !currentDay) continue;

  const morningMatch = line.match(/^(?:\*{1,2}|•|-)?\s*(?:Morning|Dawn)(?:\s*\((.*?)\))?[:–-]?\s*(.*)/i);
  const afternoonMatch = line.match(/^(?:\*{1,2}|•|-)?\s*(?:Afternoon|Midday|Noon)(?:\s*\((.*?)\))?[:–-]?\s*(.*)/i);
  const eveningMatch = line.match(/^(?:\*{1,2}|•|-)?\s*(?:Evening|Night|Dusk)(?:\s*\((.*?)\))?[:–-]?\s*(.*)/i);

  if (morningMatch) {
    currentSlot = "morning";
    const sub = (morningMatch[1] || "").replace(/[*_]/g, "").trim();
    const detail = (morningMatch[2] || "").replace(/[*_]/g, "").trim();
    currentDay.morning = [sub, detail].filter(Boolean).join(" — ");
  } else if (afternoonMatch) {
    currentSlot = "afternoon";
    const sub = (afternoonMatch[1] || "").replace(/[*_]/g, "").trim();
    const detail = (afternoonMatch[2] || "").replace(/[*_]/g, "").trim();
    currentDay.afternoon = [sub, detail].filter(Boolean).join(" — ");
  } else if (eveningMatch) {
    currentSlot = "evening";
    const sub = (eveningMatch[1] || "").replace(/[*_]/g, "").trim();
    const detail = (eveningMatch[2] || "").replace(/[*_]/g, "").trim();
    currentDay.evening = [sub, detail].filter(Boolean).join(" — ");
  } else if (line.startsWith("*") || line.startsWith("•") || line.startsWith("-")) {
    const bullet = line.replace(/^[*•\-]\s*/, "").replace(/[*_]/g, "").trim();
    if (bullet && !bullet.toLowerCase().startsWith("cost saver")) {
      if (currentSlot && currentDay[currentSlot]) {
        currentDay[currentSlot] += ` • ${bullet}`;
      } else if (currentSlot) {
        currentDay[currentSlot] = bullet;
      } else {
        currentDay.activities.push(bullet);
      }
    }
  }
}
if (currentDay) daySections.push(currentDay);

console.log('Parsed Days count:', daySections.length);
daySections.forEach(d => {
  console.log(`Day ${d.day}: ${d.theme} => ${d.morning}`);
});
