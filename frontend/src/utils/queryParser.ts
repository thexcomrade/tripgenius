/**
 * TripGenius Intelligent Travel Prompt & Query Parser
 * Automatically parses natural language prompts like:
 * - "3 days goa" -> { destination: "Goa", duration: 3 }
 * - "3 day goa" -> { destination: "Goa", duration: 3 }
 * - "goa 3 days" -> { destination: "Goa", duration: 3 }
 * - "plan a 4-day trip to Munnar" -> { destination: "Munnar", duration: 4 }
 * - "Varkala" -> { destination: "Varkala", duration: 3 }
 */

export interface ParsedTravelQuery {
  destination: string;
  duration: number;
  rawInput: string;
  isCustomDuration: boolean;
}

export function parseDestinationQuery(input: string): ParsedTravelQuery {
  const rawInput = (input || "").trim();
  if (!rawInput) {
    return {
      destination: "",
      duration: 3,
      rawInput: "",
      isCustomDuration: false,
    };
  }

  let clean = rawInput;
  let duration = 3;
  let isCustomDuration = false;

  // 1. Prefix: "3 days goa", "3 day goa", "5d munnar"
  const prefixMatch = clean.match(/^(\d+)\s*(?:days?|d)\s+(?:in\s+|to\s+)?(.+)$/i);
  if (prefixMatch) {
    duration = Math.max(1, Math.min(30, parseInt(prefixMatch[1])));
    clean = prefixMatch[2];
    isCustomDuration = true;
  } else {
    // 2. Suffix: "goa 3 days", "goa for 3 days", "munnar 4d"
    const suffixMatch = clean.match(/^(.+?)\s+(?:for\s+)?(\d+)\s*(?:days?|d)$/i);
    if (suffixMatch) {
      clean = suffixMatch[1];
      duration = Math.max(1, Math.min(30, parseInt(suffixMatch[2])));
      isCustomDuration = true;
    } else {
      // 3. Middle: "trip to goa for 3 days", "plan 5 days in munnar under 20k"
      const midMatch = clean.match(/(\d+)\s*(?:days?|d)/i);
      if (midMatch) {
        duration = Math.max(1, Math.min(30, parseInt(midMatch[1])));
        clean = clean.replace(/(\d+)\s*(?:days?|d)/i, "").trim();
        isCustomDuration = true;
      }
    }
  }

  // Strip conversational prefixes
  clean = clean.replace(
    /^(?:plan|plan\s+a|trip\s+to|visit|explore|travel\s+to|vacation\s+in|go\s+to)\s+/i,
    "",
  );
  // Strip trailing budget / style phrases
  clean = clean.replace(/\s+(?:under|budget|below|with|for)\s+.*$/i, "").trim();
  // Strip leading prepositions
  clean = clean.replace(/^(?:in|to|at)\s+/i, "").trim();

  // Clean trailing punctuation
  clean = clean.replace(/[.,!?]+$/, "").trim();

  // Capitalize nicely
  const formattedDest = clean
    ? clean
        .split(" ")
        .map((w) => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase())
        .join(" ")
    : "";

  return {
    destination: formattedDest,
    duration,
    rawInput,
    isCustomDuration,
  };
}
