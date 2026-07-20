import requests
import logging
import streamlit as st

logger = logging.getLogger(__name__)

_WMO_CODES = {
    0:"Clear sky", 1:"Mainly clear", 2:"Partly cloudy", 3:"Overcast",
    45:"Foggy", 48:"Icy fog",
    51:"Light drizzle", 53:"Moderate drizzle", 55:"Dense drizzle",
    61:"Slight rain", 63:"Moderate rain", 65:"Heavy rain",
    71:"Slight snow", 73:"Moderate snow", 75:"Heavy snow",
    80:"Rain showers", 81:"Moderate showers", 82:"Violent showers",
    95:"Thunderstorm", 96:"Thunderstorm w/ hail", 99:"Severe thunderstorm",
}


def _unavailable(reason: str) -> dict:
    return {
        "available": False, "reason": reason,
        "temperature_c": None, "feels_like_c": None,
        "humidity_pct": None, "wind_kmh": None,
        "pressure_hpa": None, "visibility_km": None,
        "rainfall_mm": None, "description": "N/A",
        "city": "Unknown", "country": "Unknown",
    }


def _reverse_geocode(lat: float, lon: float) -> tuple[str, str]:
    try:
        r = requests.get(
            "https://nominatim.openstreetmap.org/reverse",
            params={"lat": lat, "lon": lon, "format": "json"},
            headers={"User-Agent": "DisasterShieldAI/1.0 (ibm-internship-project)"},
            timeout=5,
        )
        r.raise_for_status()
        addr = r.json().get("address", {})
        city = addr.get("city") or addr.get("town") or addr.get("village") or addr.get("county") or "Unknown"
        country = addr.get("country_code", "IN").upper()
        return city, country
    except Exception:
        return "Unknown", "IN"


def _fetch_weather_raw(lat: float, lon: float) -> dict:
    """Uncached fetch — raises on failure. Used by cache wrapper and daemon."""
    resp = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": lat, "longitude": lon,
            "current": ",".join([
                "temperature_2m", "relative_humidity_2m",
                "apparent_temperature", "precipitation",
                "weather_code", "surface_pressure",
                "wind_speed_10m", "visibility",
            ]),
            "wind_speed_unit": "kmh",
            "timezone": "auto",
        },
        timeout=10,
    )
    resp.raise_for_status()
    cur = resp.json()["current"]

    city, country = _reverse_geocode(lat, lon)
    wmo = cur.get("weather_code", 0)

    return {
        "available": True,
        "reason": "",
        "temperature_c": round(cur["temperature_2m"], 1),
        "feels_like_c": round(cur["apparent_temperature"], 1),
        "humidity_pct": cur["relative_humidity_2m"],
        "wind_kmh": round(cur["wind_speed_10m"], 1),
        "pressure_hpa": round(cur["surface_pressure"], 0),
        "visibility_km": round(cur.get("visibility", 10000) / 1000, 1),
        "rainfall_mm": round(cur.get("precipitation", 0.0), 1),
        "description": _WMO_CODES.get(wmo, f"Code {wmo}"),
        "city": city,
        "country": country,
    }


@st.cache_data(ttl=300, show_spinner=False)
def _fetch_weather(lat: float, lon: float) -> dict:
    """Cached fetch — raises on failure so errors are never cached."""
    return _fetch_weather_raw(lat, lon)


def get_weather(lat: float, lon: float) -> dict:
    """
    Live weather via Open-Meteo (free, no API key), globally cached for
    5 minutes and shared by every page — navigation never refetches.
    Coordinates are rounded so cache keys stay stable. Failures are NOT
    cached, so the next rerun retries immediately.
    """
    try:
        return _fetch_weather(round(lat, 3), round(lon, 3))
    except requests.exceptions.Timeout:
        return _unavailable("Weather request timed out")
    except Exception as e:
        logger.error("Weather fetch failed: %s", e)
        return _unavailable(f"Weather unavailable: {e}")


def get_weather_uncached(lat: float, lon: float) -> dict:
    """For background threads (push daemon) — no Streamlit cache involved."""
    try:
        return _fetch_weather_raw(round(lat, 3), round(lon, 3))
    except Exception as e:
        logger.error("Weather fetch (daemon) failed: %s", e)
        return _unavailable(str(e))
