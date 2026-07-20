import requests
import logging
import streamlit as st
from backend.services.config import OVERPASS_URL, SEARCH_RADIUS_M
from backend.services.location_service import haversine_km

logger = logging.getLogger(__name__)

_SHELTER_TAGS = [
    '["amenity"="shelter"]',
    '["amenity"="community_centre"]',
    '["building"="school"]["operator:type"="government"]',
    '["emergency"="assembly_point"]',
    '["social_facility"="shelter"]',
]


def get_nearby_shelters(lat: float, lon: float, radius_m: int = SEARCH_RADIUS_M) -> list[dict]:
    """
    Query OpenStreetMap Overpass for shelters within radius_m of lat/lon.
    Globally cached for 30 min (shared across all pages); failures are
    not cached so the next rerun retries. Returns [] on failure.
    """
    try:
        return _fetch_shelters(round(lat, 3), round(lon, 3), radius_m)
    except Exception as e:
        logger.error("Shelter search failed: %s", e)
        return []


@st.cache_data(ttl=1800, show_spinner=False)
def _fetch_shelters(lat: float, lon: float, radius_m: int) -> list[dict]:
    if True:
        tag_queries = "\n".join(
            f'  node{tag}(around:{radius_m},{lat},{lon});'
            for tag in _SHELTER_TAGS
        )
        query = f"""
[out:json][timeout:15];
(
{tag_queries}
);
out body;
"""
        headers = {"User-Agent": "DisasterShieldAI/1.0 (ibm-internship-project)"}
        resp = requests.post(OVERPASS_URL, data={"data": query}, headers=headers, timeout=20)
        resp.raise_for_status()
        elements = resp.json().get("elements", [])

        shelters = []
        seen = set()

        for el in elements:
            s_lat = el.get("lat")
            s_lon = el.get("lon")
            tags = el.get("tags", {})
            name = tags.get("name") or tags.get("amenity") or "Emergency Shelter"

            if (s_lat, s_lon) in seen:
                continue
            seen.add((s_lat, s_lon))

            dist = haversine_km(lat, lon, s_lat, s_lon)
            nav_url = f"https://www.google.com/maps/dir/{lat},{lon}/{s_lat},{s_lon}"

            shelters.append({
                "name": name,
                "distance_km": round(dist, 2),
                "lat": s_lat,
                "lon": s_lon,
                "navigation_url": nav_url,
            })

        shelters.sort(key=lambda x: x["distance_km"])
        logger.info("Found %d shelters within %d m", len(shelters), radius_m)
        return shelters
