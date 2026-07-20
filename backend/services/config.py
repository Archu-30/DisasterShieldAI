import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def _get_secret(key: str, default: str = "") -> str:
    val = os.getenv(key)
    if not val:
        try:
            val = st.secrets.get(key, default)
        except Exception:
            val = default
    return val or default


# ── API Keys ──────────────────────────────────────────────────────────────────
GROQ_API_KEY = _get_secret("GROQ_API_KEY", "")
OPENWEATHER_API_KEY = _get_secret("OPENWEATHER_API_KEY", "")

# ── Weather ───────────────────────────────────────────────────────────────────
WEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
WEATHER_REFRESH_SECONDS = 300       # refresh every 5 minutes

# ── Location ──────────────────────────────────────────────────────────────────
LOCATION_REFRESH_SECONDS = 180      # re-check GPS every 3 minutes
LOCATION_MOVE_THRESHOLD_KM = 0.5   # re-fetch resources if moved > 500 m

# ── Overpass (OpenStreetMap) ──────────────────────────────────────────────────
OVERPASS_URL = "https://overpass-api.de/api/interpreter"
SEARCH_RADIUS_M = 10000             # 10 km radius

# ── Risk Engine thresholds ────────────────────────────────────────────────────
RISK_THRESHOLDS = {
    "flood": {
        "high":     {"rainfall_mm": 80},
        "moderate": {"rainfall_mm": 50},
        "low":      {"rainfall_mm": 20},
    },
    "cyclone": {
        "high":     {"wind_kmh": 70},
        "moderate": {"wind_kmh": 50},
        "low":      {"wind_kmh": 30},
    },
    "heatwave": {
        "critical": {"temp_c": 42},
        "high":     {"temp_c": 38},
        "moderate": {"temp_c": 35},
    },
    "thunderstorm": {
        "high":     {"wind_kmh": 40, "rainfall_mm": 30},
    },
    "heavy_rain": {
        "moderate": {"rainfall_mm": 50},
    },
    "landslide": {
        "moderate": {"rainfall_mm": 100, "humidity_pct": 90},
    },
}

# ── Emergency contacts (official India) ───────────────────────────────────────
EMERGENCY_CONTACTS = [
    {"service": "National Emergency",         "number": "112"},
    {"service": "Ambulance",                  "number": "108"},
    {"service": "Fire",                       "number": "101"},
    {"service": "Police",                     "number": "100"},
    {"service": "State Disaster Control Room","number": "1070"},
    {"service": "District Disaster Control",  "number": "1077"},
]
