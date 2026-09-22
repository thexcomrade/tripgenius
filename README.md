<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&height=220&color=0:00C2FF,100:00FF99&text=TripGenius%20AI&fontSize=65&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=Your%20Personal%20AI%20Travel%20Companion&descAlignY=60"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/AI-Gemini-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/FastAPI-Python-green?style=for-the-badge">
  <img src="https://img.shields.io/badge/Next.js-TypeScript-black?style=for-the-badge">
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge">
</p>

<p align="center">
  🌍 Discover &nbsp;•&nbsp; ✈️ Plan &nbsp;•&nbsp; 🏨 Stay &nbsp;•&nbsp; 🍲 Explore &nbsp;•&nbsp; 🎒 Travel
</p>

<p align="center">
  <b>Plan Smarter. Travel Better.</b>
</p>


TripGenius AI is an intelligent travel planning platform that transforms a few simple user inputs into a complete, personalized travel experience. By combining Generative AI, real-time weather insights, and destination intelligence, TripGenius creates end-to-end travel itineraries tailored to each traveler's budget, interests, duration, and destination preferences.

Whether you're planning a weekend getaway, a family vacation, a solo adventure, or a budget-friendly exploration, TripGenius acts as your personal AI travel companion—helping you discover attractions, accommodations, local cuisines, travel tips, and optimized day-wise schedules in seconds.

---

## 🚀 Problem Statement

Travel planning often involves switching between multiple websites for destination research, hotel searches, weather forecasts, local attractions, and itinerary creation.

TripGenius AI solves this problem by bringing everything together into a single intelligent platform that automatically generates personalized travel plans using AI.

---

## ✨ Key Features

### 🤖 AI-Powered Travel Planning

* Personalized itinerary generation
* Day-wise travel schedules
* Budget-aware recommendations
* Interest-based activity suggestions

### 🗺️ Smart Destination Discovery

* Tourist attraction recommendations
* Hidden gems and local experiences
* Activity-based destination matching
* Region-specific travel insights

### 🏨 Accommodation Recommendations

* Budget stays
* Mid-range hotels
* Premium accommodations

### 🍲 Local Cuisine Explorer

* Popular local dishes
* Regional beverages
* Food recommendations based on destination

### 🌤️ Real-Time Weather Insights

* Current weather conditions
* Temperature forecasts
* Travel-friendly weather recommendations

### 🎒 Smart Packing Assistant

* Weather-based packing suggestions
* Destination-specific essentials
* Travel preparation checklist

### 👤 User Management

* Secure authentication
* User profiles
* Trip history management
* Saved travel plans

---

## 🧠 How It Works

```text
User Input
    │
    ▼
Destination + Budget + Duration + Interests
    │
    ▼
Tourism Dataset Analysis
    │
    ▼
Gemini AI Processing
    │
    ▼
Weather API Integration
    │
    ▼
Personalized Travel Plan
    │
    ▼
Hotels + Attractions + Food + Tips
```

---

## 🏗️ Technology Stack

### Frontend

* Next.js
* TypeScript
* Tailwind CSS
* Framer Motion

### Backend

* FastAPI
* Python

### Database

* SQLite

### Artificial Intelligence

* Google Gemini API

### External APIs

* OpenWeather API

### Dataset

* Kerala & Karnataka Tourism Places Dataset

---

## 📂 Project Structure

```text
tripgenius/

├── frontend/
│
├── backend/
│
├── database/
│   └── tourism.csv
│
├── docs/
│
└── assets/
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/thexcomrade/TripGenius.git
cd TripGenius
```

### Backend Setup

```bash
cd backend

python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

---

## 🔐 Environment Variables

Create:

```text
backend/.env
```

```env
SECRET_KEY=your_secret_key

GEMINI_API_KEY=your_gemini_api_key

OPENWEATHER_API_KEY=your_openweather_api_key

DATABASE_URL=sqlite:///./tripgenius.db
```

---

## 🎯 User Workflow

### Step 1

Enter travel details:

* Destination
* Duration
* Budget
* Travel Style
* Interests

### Step 2

AI analyzes:

* Destination information
* Tourist activities
* Weather conditions
* Budget constraints

### Step 3

TripGenius generates:

* Complete itinerary
* Recommended attractions
* Hotel suggestions
* Local food recommendations
* Packing checklist
* Travel tips

---

## 🌟 Why TripGenius?

✅ AI-Driven Personalization

✅ Real-Time Weather Integration

✅ Tourism Dataset Intelligence

✅ Fast and User-Friendly Experience

✅ Budget-Conscious Recommendations

✅ End-to-End Travel Planning

---

## 🔮 Future Enhancements

* Interactive Maps
* Multi-City Planning
* Flight Recommendations
* PDF Export
* AI Travel Chatbot
* Travel Cost Optimization
* Collaborative Group Trips
* Voice-Based Trip Planning

---

## 👨‍💻 Developed For

### ClaySys AI/ML Hackathon 2026

TripGenius AI demonstrates how Generative AI can simplify travel planning by delivering intelligent, personalized, and data-driven travel experiences through a single unified platform.

---

### 🌎 Travel Less Stressfully. Explore More Intelligently.
