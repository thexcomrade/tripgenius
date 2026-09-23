-- =============================================================================
-- TripGenius — Database Schema (SQLite / PostgreSQL compatible)
-- =============================================================================
-- PURPOSE:
--   This file documents the exact database schema used by TripGenius.
--   The live schema is managed by SQLAlchemy ORM (app/models/user.py,
--   app/models/trip.py) via Base.metadata.create_all() on startup.
--
--   Use this file for:
--     - Developer reference and onboarding
--     - Manual DB inspection or recreation
--     - Migration planning
--     - DBA review
--     - CI/CD schema validation
--
-- The authoritative Python models are:
--   backend/app/models/user.py  → users table
--   backend/app/models/trip.py  → trips table
--
-- The tourism recommendations dataset is a CSV file, NOT stored in SQLite:
--   database/tourism.csv        → loaded by RecommendationService via Pandas
-- =============================================================================


-- ---------------------------------------------------------------------------
-- TABLE: users
-- ---------------------------------------------------------------------------
-- Stores registered user accounts. Passwords are bcrypt-hashed.
-- Users can have multiple trips (one-to-many: users → trips).
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS users (
    -- Primary key: UUID v4 string (36 chars)
    id                      VARCHAR(36)     PRIMARY KEY,

    -- Core identity
    full_name               VARCHAR(150)    NOT NULL,
    email                   VARCHAR(255)    NOT NULL UNIQUE,
    hashed_password         VARCHAR(255)    NOT NULL,

    -- Profile details
    profile_image           VARCHAR(500)    NULL,       -- URL or base64 data URI
    bio                     TEXT            NULL,
    country                 VARCHAR(100)    NULL,

    -- Travel preferences
    preferred_budget        VARCHAR(50)     NULL,       -- e.g. 'Budget', 'Moderate', 'Premium', 'Luxury'
    preferred_travel_style  VARCHAR(100)    NULL,       -- e.g. 'Adventure', 'Eco', 'Romantic', 'Family'
    favourite_destination   VARCHAR(150)    NULL,

    -- Gamification / eco-tracking
    eco_travel_score        INTEGER         NOT NULL DEFAULT 0,
    total_trips             INTEGER         NOT NULL DEFAULT 0,

    -- Account state
    is_active               BOOLEAN         NOT NULL DEFAULT TRUE,
    is_verified             BOOLEAN         NOT NULL DEFAULT FALSE,

    -- Timestamps (UTC)
    created_at              DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at              DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Indexes used by authentication and lookup queries
CREATE UNIQUE INDEX IF NOT EXISTS ix_users_email ON users (email);
CREATE INDEX        IF NOT EXISTS ix_users_id    ON users (id);


-- ---------------------------------------------------------------------------
-- TABLE: trips
-- ---------------------------------------------------------------------------
-- Stores AI-generated or manually curated trip itineraries.
-- Each trip belongs to one user. Cost, AI output, and weather data are all
-- stored here as JSON blobs or flat columns.
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS trips (
    -- Primary key: UUID v4 string (36 chars)
    id                          VARCHAR(36)     PRIMARY KEY,

    -- Owner reference (cascade delete — if user is deleted, trips are too)
    user_id                     VARCHAR(36)     NOT NULL
                                    REFERENCES users(id) ON DELETE CASCADE,

    -- Trip metadata
    trip_title                  VARCHAR(200)    NOT NULL,
    destination                 VARCHAR(200)    NOT NULL,
    state                       VARCHAR(100)    NULL,   -- e.g. 'Kerala', 'Rajasthan'
    district                    VARCHAR(100)    NULL,   -- e.g. 'Munnar', 'Jaipur'

    -- Trip parameters
    duration_days               INTEGER         NOT NULL,
    travelers_count             INTEGER         NOT NULL DEFAULT 1,
    budget                      REAL            NOT NULL,  -- total budget in INR
    travel_style                VARCHAR(100)    NULL,   -- e.g. 'Romantic', 'Adventure', 'Eco'
    interests                   JSON            NOT NULL DEFAULT '[]',
    transportation_mode         VARCHAR(100)    NULL,   -- e.g. 'Car', 'Train', 'Flight'
    preferred_accommodation     VARCHAR(100)    NULL,   -- e.g. 'Hotel', 'Hostel', 'Resort'

    -- AI-generated itinerary content (all JSON)
    ai_itinerary                JSON            NOT NULL DEFAULT '{}',
        -- Structure: { "day_1": { "morning": {...}, "afternoon": {...}, "evening": {...} }, ... }
    itinerary_summary           TEXT            NULL,
    attractions                 JSON            NOT NULL DEFAULT '[]',
        -- Structure: [{ "name": str, "description": str, "entry_fee": float, ... }]
    recommended_hotels          JSON            NOT NULL DEFAULT '[]',
        -- Structure: [{ "name": str, "location": str, "price_per_night": float, "rating": float, ... }]
    recommended_restaurants     JSON            NOT NULL DEFAULT '[]',
        -- Structure: [{ "name": str, "cuisine": str, "price_range": str, ... }]
    local_cuisines              JSON            NOT NULL DEFAULT '[]',
    beverages_to_try            JSON            NOT NULL DEFAULT '[]',

    -- Weather data (fetched from OpenWeather API)
    weather_summary             JSON            NOT NULL DEFAULT '{}',
        -- Structure: { "temperature": float, "condition": str, "humidity": int, ... }
    weather_alerts              JSON            NOT NULL DEFAULT '[]',

    -- Utility data
    packing_checklist           JSON            NOT NULL DEFAULT '[]',
    travel_tips                 JSON            NOT NULL DEFAULT '[]',

    -- Budget breakdown (in INR, pre-computed by estimate_trip_cost)
    estimated_trip_cost         REAL            NOT NULL DEFAULT 0.0,
    accommodation_cost          REAL            NOT NULL DEFAULT 0.0,
    food_cost                   REAL            NOT NULL DEFAULT 0.0,
    transportation_cost         REAL            NOT NULL DEFAULT 0.0,
    miscellaneous_cost          REAL            NOT NULL DEFAULT 0.0,

    -- Sustainability / eco metrics
    sustainability_score        INTEGER         NOT NULL DEFAULT 0,  -- 0–100 scale
    carbon_footprint_estimate   REAL            NOT NULL DEFAULT 0.0,
    eco_friendly_recommendations JSON           NOT NULL DEFAULT '[]',

    -- AI generation metadata
    ai_confidence_score         REAL            NOT NULL DEFAULT 0.0,
    generated_by_ai             BOOLEAN         NOT NULL DEFAULT TRUE,
    generation_model            VARCHAR(100)    NULL,   -- e.g. 'gemini-2.5-flash'

    -- Trip lifecycle
    is_favorite                 BOOLEAN         NOT NULL DEFAULT FALSE,
    is_public                   BOOLEAN         NOT NULL DEFAULT FALSE,
    status                      VARCHAR(50)     NOT NULL DEFAULT 'draft',
        -- Allowed values: 'draft', 'planned', 'completed', 'cancelled'

    -- Timestamps (UTC)
    created_at                  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at                  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for common query patterns
CREATE INDEX IF NOT EXISTS ix_trips_id          ON trips (id);
CREATE INDEX IF NOT EXISTS ix_trips_user_id     ON trips (user_id);
CREATE INDEX IF NOT EXISTS ix_trips_destination ON trips (destination);


-- =============================================================================
-- NOTE ON TOURISM DATASET
-- =============================================================================
-- The tourism recommendation data (destinations, activities, descriptions) is
-- NOT stored in SQLite. It lives as a CSV file loaded into memory at startup:
--
--   database/tourism.csv
--   Columns: Name of the Place, District, Famous_For, Activities,
--            State, Country, Category, Travel_Style, Best_Season,
--            Budget_Category, Duration_Days
--
-- This is loaded by:
--   backend/app/services/recommendation_service.py → RecommendationService
-- =============================================================================
