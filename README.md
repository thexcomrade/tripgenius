# TripGenius AI

An AI-powered travel planning assistant that generates personalized end-to-end travel itineraries based on destination, travel duration, budget, travel preferences, and interests. The platform helps travelers plan trips efficiently by providing day-wise itineraries, accommodation recommendations, transportation suggestions, tourist attractions, local cuisines, weather insights, and travel tips in a single intelligent dashboard.

## Features

* User Registration and Authentication
* Personalized Travel Planning
* AI-Generated Day-Wise Itineraries
* Destination-Based Recommendations
* Hotel and Accommodation Suggestions
* Tourist Attraction Recommendations
* Local Cuisine and Beverage Suggestions
* Weather Forecast Integration
* Packing Recommendations
* Trip History Management
* Responsive User Interface

## Technology Stack

### Frontend

* Next.js
* TypeScript
* Tailwind CSS

### Backend

* FastAPI
* Python

### Database

* SQLite

### AI Services

* Gemini API

### External APIs

* OpenWeather API

## Project Structure

```text
tripgenius-ai/
├── frontend/
├── backend/
├── database/
├── docs/
└── assets/
```

## Installation

### Clone Repository

```bash
git clone https://github.com/thexcomrade/TripGenius
cd tripgenius-ai
```

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

Create a `.env` file inside the backend directory.

```env
GEMINI_API_KEY=
OPENWEATHER_API_KEY=
SECRET_KEY=
DATABASE_URL=
```

## Usage

1. Register a new account.
2. Login to the platform.
3. Enter travel details such as destination, duration, budget, and interests.
4. Generate an AI-powered itinerary.
5. Explore accommodations, attractions, cuisines, and weather information.
6. Save and review previous travel plans.

## Solution Approach

TripGenius AI combines Generative AI with travel-related APIs to provide intelligent travel planning. User preferences are processed by the AI engine to generate customized itineraries, while external APIs provide weather and destination-related insights. The generated recommendations are stored for future access and trip management.

## Future Enhancements

* Interactive Maps
* Multi-City Trip Planning
* Flight Recommendations
* PDF Itinerary Export
* Real-Time Travel Alerts
* Social Sharing Features

## License

This project is developed for the ClaySys AI/ML Hackathon.
