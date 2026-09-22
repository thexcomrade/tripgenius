INTEREST_CATEGORIES = [
    "Nature",
    "Adventure",
    "Food",
    "Photography",
    "Culture",
    "History",
    "Wildlife",
    "Shopping",
    "Relaxation",
    "Spiritual",
    "Nightlife",
    "Family",
]

TRAVEL_STYLES = [
    "Budget",
    "Standard",
    "Luxury",
    "Backpacking",
    "Solo",
    "Family",
    "Business",
]

SUPPORTED_STATES = [
    "Kerala",
    "Karnataka",
]

SUPPORTED_CURRENCIES = [
    "INR",
]

DEFAULT_CURRENCY = "INR"

DEFAULT_TRAVELERS = 1

MIN_DURATION_DAYS = 1
MAX_DURATION_DAYS = 30

MIN_BUDGET = 1000
MAX_BUDGET = 1000000

DEFAULT_WEATHER_UNIT = "metric"

DEFAULT_LANGUAGE = "en"

AI_MODEL_NAME = "gemini-2.5-flash"

MAX_DESTINATION_RESULTS = 10

MAX_RECOMMENDATIONS = 15

MAX_ITINERARY_DAYS = 15

TRIP_STATUS_DRAFT = "draft"
TRIP_STATUS_COMPLETED = "completed"

TRIP_STATUSES = [
    TRIP_STATUS_DRAFT,
    TRIP_STATUS_COMPLETED,
]

WEATHER_API_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

WEATHER_FORECAST_API_BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"

HOTEL_PRICE_BUDGET = "Budget"
HOTEL_PRICE_STANDARD = "Standard"
HOTEL_PRICE_LUXURY = "Luxury"

HOTEL_PRICE_CATEGORIES = [
    HOTEL_PRICE_BUDGET,
    HOTEL_PRICE_STANDARD,
    HOTEL_PRICE_LUXURY,
]

PACKING_CATEGORIES = [
    "Clothing",
    "Documents",
    "Electronics",
    "Health",
    "Accessories",
]

PROMPT_FILES = {
    "itinerary": "itinerary_prompt.txt",
    "cuisine": "cuisine_prompt.txt",
    "packing": "packing_prompt.txt",
}

SUCCESS_RESPONSE = "success"

ERROR_RESPONSE = "error"

DEFAULT_PAGE_SIZE = 10

MAX_PAGE_SIZE = 100

JWT_TOKEN_TYPE = "Bearer"

APPLICATION_NAME = "TripGenius"

APPLICATION_VERSION = "1.0.0"
