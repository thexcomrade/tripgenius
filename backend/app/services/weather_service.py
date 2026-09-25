from typing import Any

import requests

from app.core.config import settings


class WeatherService:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self) -> None:
        self.api_key = settings.OPENWEATHER_API_KEY

    CITY_ALIASES = {
        "chickmanglore": "Chikkamagaluru",
        "chikmagalur": "Chikkamagaluru",
        "chickmagalur": "Chikkamagaluru",
        "trivandrum": "Thiruvananthapuram",
        "cochin": "Kochi",
        "ooty": "Udhagamandalam",
        "calicut": "Kozhikode",
        "alleppey": "Alappuzha",
        "quilon": "Kollam",
        "palghat": "Palakkad",
        "cannanoor": "Kannur",
        "cannanore": "Kannur",
        "trichur": "Thrissur",
        "mysore": "Mysuru",
        "bangalore": "Bengaluru",
        "bombay": "Mumbai",
        "madras": "Chennai",
        "calcutta": "Kolkata",
        "pondi": "Puducherry",
        "pondicherry": "Puducherry",
    }

    def get_current_weather(self, city: str) -> dict[str, Any]:
        city_query = self.CITY_ALIASES.get(city.strip().lower(), city.strip())
        params = {"q": city_query, "appid": self.api_key, "units": "metric"}

        response = requests.get(self.BASE_URL, params=params, timeout=15)

        response.raise_for_status()

        data = response.json()

        return self._format_weather_data(data)

    def _format_weather_data(self, data: dict) -> dict[str, Any]:

        weather = data.get("weather", [{}])[0]

        main = data.get("main", {})

        wind = data.get("wind", {})

        visibility = data.get("visibility", 0)

        return {
            "city": data.get("name"),
            "country": data.get("sys", {}).get("country"),
            "temperature": main.get("temp"),
            "feels_like": main.get("feels_like"),
            "humidity": main.get("humidity"),
            "pressure": main.get("pressure"),
            "condition": weather.get("main"),
            "description": weather.get("description"),
            "wind_speed": wind.get("speed"),
            "visibility": visibility,
            "travel_recommendation": self._generate_recommendation(
                weather.get("main", "")
            ),
            "packing_suggestions": self._generate_packing_suggestions(
                main.get("temp", 0), weather.get("main", "")
            ),
        }

    def _generate_recommendation(self, weather_condition: str) -> str:

        condition = weather_condition.lower()

        if "rain" in condition:
            return "Carry an umbrella and plan indoor activities."

        if "storm" in condition:
            return "Avoid outdoor adventures and monitor alerts."

        if "snow" in condition:
            return "Wear thermal clothing and travel carefully."

        if "clear" in condition:
            return "Excellent weather for sightseeing and exploration."

        if "cloud" in condition:
            return "Comfortable weather for general travel activities."

        return "Check local conditions before planning outdoor activities."

    def _generate_packing_suggestions(
        self, temperature: float, weather_condition: str
    ) -> list[str]:

        items: list[str] = []

        if temperature >= 30:
            items.extend(
                ["Light cotton clothes", "Sunscreen", "Water bottle", "Sunglasses"]
            )

        elif temperature >= 20:
            items.extend(["Comfortable clothing", "Walking shoes"])

        elif temperature >= 10:
            items.extend(["Light jacket", "Comfortable shoes"])

        else:
            items.extend(["Winter jacket", "Thermal wear", "Gloves"])

        condition = weather_condition.lower()

        if "rain" in condition:
            items.extend(["Umbrella", "Raincoat"])

        if "snow" in condition:
            items.extend(["Snow boots", "Woolen cap"])

        return items

    def get_weather_summary(self, city: str) -> dict[str, Any]:

        weather = self.get_current_weather(city)

        return {
            "destination": city,
            "temperature": weather["temperature"],
            "condition": weather["condition"],
            "humidity": weather["humidity"],
            "travel_recommendation": weather["travel_recommendation"],
        }
