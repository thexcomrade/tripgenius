from pathlib import Path
from typing import Any

import pandas as pd


def _find_tourism_csv() -> Path:
    """Search for tourism.csv in multiple candidate locations."""
    candidates = [
        # Relative to this file: backend/app/services/recommendation_service.py
        # go up 4 levels to tripgenius root, then database/
        Path(__file__).resolve().parents[3] / "database" / "tourism.csv",
        # go up 3 levels to backend root, then database/
        Path(__file__).resolve().parents[2] / "database" / "tourism.csv",
        # Same directory as script (backend/)
        Path(__file__).resolve().parent.parent.parent / "database" / "tourism.csv",
        # tourism.csv placed directly in backend/
        Path(__file__).resolve().parents[2] / "tourism.csv",
        # cwd-based fallback
        Path.cwd() / "database" / "tourism.csv",
        Path.cwd().parent / "database" / "tourism.csv",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        f"tourism.csv not found. Searched: {[str(c) for c in candidates]}"
    )


class RecommendationService:
    def __init__(self) -> None:
        self.dataset = self._load_dataset()

        self.kerala_districts = {
            "thiruvananthapuram",
            "kollam",
            "pathanamthitta",
            "alappuzha",
            "kottayam",
            "idukki",
            "ernakulam",
            "thrissur",
            "palakkad",
            "malappuram",
            "kozhikode",
            "wayanad",
            "kannur",
            "kasaragod",
            "kochi",
            "munnar",
        }

        self.karnataka_districts = {
            "mysuru",
            "kodagu",
            "chikkamagaluru",
            "shivamogga",
            "udupi",
            "dakshina kannada",
            "hassan",
            "bengaluru",
            "belagavi",
            "ballari",
            "hampi",
            "coorg",
            "mangaluru",
            "chikkaballapur",
            "mandya",
            "kalaburagi",
            "uttar_kannada",
        }

    def _load_dataset(self) -> pd.DataFrame:
        try:
            dataset_path = _find_tourism_csv()
        except FileNotFoundError:
            import logging

            logging.getLogger(__name__).warning(
                "tourism.csv not found — RecommendationService will return empty results."
            )
            return pd.DataFrame(
                columns=[
                    "Name of the Place",
                    "District",
                    "Famous_For",
                    "Activities",
                    "State",
                    "Country",
                    "Category",
                    "Travel_Style",
                    "Best_Season",
                    "Budget_Category",
                    "Duration_Days",
                ]
            )

        dataframe = pd.read_csv(dataset_path)
        dataframe.columns = [column.strip() for column in dataframe.columns]
        dataframe = dataframe.fillna("")
        return dataframe

    def _row_to_dict(self, row: Any) -> dict[str, Any]:
        """
        Convert a DataFrame row into a standardized destination record.
        Maintains 100% backward compatibility with legacy keys ('place_name',
        'district', 'description', 'activities') while exposing enriched metadata.
        """
        duration_raw = str(row.get("Duration_Days", "1")).strip()
        duration_days = int(duration_raw) if duration_raw.isdigit() else 1

        return {
            "place_name": str(row.get("Name of the Place", "")).strip(),
            "district": str(row.get("District", "")).strip(),
            "description": str(row.get("Famous_For", "")).strip(),
            "activities": str(row.get("Activities", "")).strip(),
            "state": str(row.get("State", "")).strip(),
            "country": str(row.get("Country", "India")).strip() or "India",
            "category": str(row.get("Category", "Sightseeing")).strip(),
            "travel_style": str(row.get("Travel_Style", "Leisure")).strip(),
            "best_season": str(row.get("Best_Season", "Year-round")).strip(),
            "budget_category": str(row.get("Budget_Category", "Moderate")).strip(),
            "duration_days": duration_days,
        }

    def get_all_destinations(self) -> list[dict[str, Any]]:
        results = []
        for _, row in self.dataset.iterrows():
            results.append(self._row_to_dict(row))
        return results

    def search_destination(self, query: str) -> list[dict[str, Any]]:
        """
        Relevance-scored destination search across place names, cities/districts,
        states, countries, and activity descriptions.
        """
        q = str(query or "").strip().lower()
        if not q:
            return []

        scored_results: list[dict[str, Any]] = []

        for _, row in self.dataset.iterrows():
            place_name = str(row.get("Name of the Place", "")).lower().strip()
            district = str(row.get("District", "")).lower().strip()
            state = str(row.get("State", "")).lower().strip()
            country = str(row.get("Country", "")).lower().strip()
            description = str(row.get("Famous_For", "")).lower()
            activities = str(row.get("Activities", "")).lower()

            score = 0

            # 1. Exact & prefix matching on Place Name (highest relevance)
            if place_name == q:
                score += 100
            elif place_name.startswith(q):
                score += 60
            elif q in place_name:
                score += 40

            # 2. Match on District / City / Region
            if district == q:
                score += 55
            elif district.startswith(q):
                score += 40
            elif q in district:
                score += 25

            # 3. Match on State
            if state == q:
                score += 45
            elif q in state:
                score += 20

            # 4. Match on Country
            if country == q:
                score += 35
            elif q in country:
                score += 15

            # 5. Semantic description and activities
            if q in description:
                score += 12
            if q in activities:
                score += 8

            if score > 0:
                item = self._row_to_dict(row)
                item["relevance_score"] = score
                scored_results.append(item)

        scored_results.sort(key=lambda item: item["relevance_score"], reverse=True)
        return scored_results

    def recommend_by_interest(self, interests: list[str]) -> list[dict[str, Any]]:
        recommendations = []
        keywords = [interest.lower().strip() for interest in interests if interest.strip()]

        for _, row in self.dataset.iterrows():
            description = str(row.get("Famous_For", "")).lower()
            activities = str(row.get("Activities", "")).lower()
            travel_style = str(row.get("Travel_Style", "")).lower()
            category = str(row.get("Category", "")).lower()

            score = 0

            for keyword in keywords:
                if keyword in travel_style:
                    score += 4
                if keyword in category:
                    score += 3
                if keyword in activities:
                    score += 3
                if keyword in description:
                    score += 2

            if score > 0:
                item = self._row_to_dict(row)
                item["match_score"] = score
                recommendations.append(item)

        recommendations.sort(key=lambda item: item["match_score"], reverse=True)
        return recommendations[:12]

    def recommend_eco_destinations(self) -> list[dict[str, Any]]:
        eco_keywords = [
            "nature",
            "wildlife",
            "forest",
            "trekking",
            "hill",
            "waterfall",
            "lake",
            "eco",
            "green",
            "mountain",
            "sanctuary",
            "biosphere",
            "national park",
        ]

        recommendations = []

        for _, row in self.dataset.iterrows():
            description = str(row.get("Famous_For", "")).lower()
            activities = str(row.get("Activities", "")).lower()
            category = str(row.get("Category", "")).lower()
            travel_style = str(row.get("Travel_Style", "")).lower()

            score = 0

            if "eco" in category or "wildlife" in category or "mountain" in category or "waterfall" in category:
                score += 4
            if "eco" in travel_style:
                score += 4

            for keyword in eco_keywords:
                if keyword in description:
                    score += 2
                if keyword in activities:
                    score += 3

            if score > 0:
                item = self._row_to_dict(row)
                item["eco_score"] = score
                recommendations.append(item)

        recommendations.sort(key=lambda item: item["eco_score"], reverse=True)
        return recommendations[:12]

    def get_kerala_destinations(self) -> list[dict[str, Any]]:
        results = []
        for _, row in self.dataset.iterrows():
            district = str(row.get("District", "")).lower().strip()
            state = str(row.get("State", "")).lower().strip()

            if state == "kerala" or district in self.kerala_districts:
                results.append(self._row_to_dict(row))

        return results

    def get_karnataka_destinations(self) -> list[dict[str, Any]]:
        results = []
        for _, row in self.dataset.iterrows():
            district = str(row.get("District", "")).lower().strip()
            state = str(row.get("State", "")).lower().strip()

            if state == "karnataka" or district in self.karnataka_districts:
                results.append(self._row_to_dict(row))

        return results

    def get_destinations_by_country(self, country: str) -> list[dict[str, Any]]:
        target = country.strip().lower()
        results = []
        for _, row in self.dataset.iterrows():
            c = str(row.get("Country", "")).strip().lower()
            if c == target or target in c:
                results.append(self._row_to_dict(row))
        return results

    def get_destinations_by_state(self, state: str) -> list[dict[str, Any]]:
        target = state.strip().lower()
        results = []
        for _, row in self.dataset.iterrows():
            s = str(row.get("State", "")).strip().lower()
            if s == target or target in s:
                results.append(self._row_to_dict(row))
        return results

    def get_destinations_by_category(self, category: str) -> list[dict[str, Any]]:
        target = category.strip().lower()
        results = []
        for _, row in self.dataset.iterrows():
            cat = str(row.get("Category", "")).strip().lower()
            if target in cat:
                results.append(self._row_to_dict(row))
        return results

    def get_all_countries(self) -> list[str]:
        if "Country" not in self.dataset.columns:
            return ["India"]
        countries = self.dataset["Country"].replace("", "India").dropna().unique().tolist()
        return sorted([c for c in countries if str(c).strip()])

    def get_all_categories(self) -> list[str]:
        if "Category" not in self.dataset.columns:
            return ["Heritage", "Nature", "Beach", "Mountain"]
        categories = self.dataset["Category"].dropna().unique().tolist()
        return sorted([c for c in categories if str(c).strip()])

    def recommend_by_budget(self, budget: float) -> dict[str, Any]:
        """
        Calibrate budget tier and recommend real destinations matching the budget profile.
        """
        if budget <= 15000:
            category = "Budget"
            range_desc = "₹0 - ₹15,000 (Ideal for backpackers, homestays, public transit & scenic nature)"
        elif budget <= 40000:
            category = "Moderate"
            range_desc = "₹15,000 - ₹40,000 (Comfortable boutique stays, regional dining & curated sightseeing)"
        elif budget <= 80000:
            category = "Premium"
            range_desc = "₹40,000 - ₹80,000 (Luxury resorts, private cab transit, adventure & culinary tours)"
        else:
            category = "Luxury"
            range_desc = "₹80,000+ (5-star private villas, luxury transport & exclusive personalized experiences)"

        matching_places: list[dict[str, Any]] = []
        if "Budget_Category" in self.dataset.columns:
            matches_df = self.dataset[
                self.dataset["Budget_Category"].astype(str).str.lower() == category.lower()
            ]
            for _, row in matches_df.head(10).iterrows():
                matching_places.append(self._row_to_dict(row))

        return {
            "budget": budget,
            "recommended_category": category,
            "budget_range_description": range_desc,
            "matching_destinations": matching_places,
            "suggestions": [
                "Local transportation",
                "Regional cuisine",
                "Popular attractions",
                "Nature experiences",
            ],
        }

    def generate_destination_profile(
        self, destination_name: str
    ) -> dict[str, Any] | None:
        matches = self.search_destination(destination_name)

        if not matches:
            return None

        destination = matches[0]

        duration = destination.get("duration_days", 2)

        return {
            "destination": destination["place_name"],
            "district": destination["district"],
            "state": destination.get("state", ""),
            "country": destination.get("country", "India"),
            "category": destination.get("category", "Sightseeing"),
            "description": destination["description"],
            "activities": destination["activities"],
            "travel_style": destination.get("travel_style", "Leisure"),
            "best_season": destination.get("best_season", "October to March"),
            "budget_category": destination.get("budget_category", "Moderate"),
            "eco_friendly": True,
            "recommended_duration": f"{duration}-{duration + 2} Days",
        }
