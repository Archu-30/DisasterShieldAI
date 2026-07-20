import requests
import logging
import streamlit as st
from backend.services.config import OVERPASS_URL, SEARCH_RADIUS_M
from backend.services.location_service import haversine_km

logger = logging.getLogger(__name__)


def get_nearby_hospitals(lat: float, lon: float, radius_m: int = SEARCH_RADIUS_M) -> list[dict]:
    """
    Query OpenStreetMap Overpass for hospitals within radius_m of lat/lon.
    Globally cached for 30 min (shared across all pages); failures are
    not cached so the next rerun retries. Returns [] on failure.
    """
    try:
        return _fetch_hospitals(round(lat, 3), round(lon, 3), radius_m)
    except Exception as e:
        logger.error("Hospital search failed: %s", e)
        return []


@st.cache_data(ttl=1800, show_spinner=False)
def _fetch_hospitals(lat: float, lon: float, radius_m: int) -> list[dict]:
    if True:
        query = f"""
[out:json][timeout:15];
(
  node["amenity"="hospital"](around:{radius_m},{lat},{lon});
  node["amenity"="clinic"](around:{radius_m},{lat},{lon});
);
out body;
"""
        headers = {"User-Agent": "DisasterShieldAI/1.0 (ibm-internship-project)"}
        resp = requests.post(OVERPASS_URL, data={"data": query}, headers=headers, timeout=20)
        resp.raise_for_status()
        elements = resp.json().get("elements", [])

        hospitals = []
        seen = set()

        for el in elements:
            h_lat = el.get("lat")
            h_lon = el.get("lon")
            tags = el.get("tags", {})
            name = tags.get("name") or "Hospital"
            phone = tags.get("phone") or tags.get("contact:phone") or "Phone Number Not Available"

            if (h_lat, h_lon) in seen:
                continue
            seen.add((h_lat, h_lon))

            dist = haversine_km(lat, lon, h_lat, h_lon)
            nav_url = f"https://www.google.com/maps/dir/{lat},{lon}/{h_lat},{h_lon}"

            hospitals.append({
                "name": name,
                "distance_km": round(dist, 2),
                "lat": h_lat,
                "lon": h_lon,
                "phone": phone,
                "navigation_url": nav_url,
            })

        hospitals.sort(key=lambda x: x["distance_km"])
        logger.info("Found %d hospitals within %d m", len(hospitals), radius_m)
        return hospitals
