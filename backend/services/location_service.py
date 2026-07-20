import math
import logging

logger = logging.getLogger(__name__)


def _unavailable(reason: str) -> dict:
    return {
        "available": False,
        "reason": reason,
        "lat": None,
        "lon": None,
        "accuracy_m": None,
    }


def get_location() -> dict:
    """
    Request browser GPS via streamlit-js-eval, memoized in session_state.

    The GPS component costs a full extra Streamlit rerun every time it runs,
    so once coordinates are acquired they are reused for the whole session.
    Coordinates are rounded to 3 decimals (~110 m) so they form stable
    st.cache_data keys — raw GPS jitter would otherwise bust every cache
    on each navigation.
    """
    import streamlit as st

    cached = st.session_state.get("_ds_location")
    if cached and cached.get("available"):
        return cached

    try:
        from streamlit_js_eval import get_geolocation
        loc = get_geolocation()

        if not loc:
            return _unavailable("Location permission denied or GPS unavailable")

        coords = loc.get("coords", {})
        lat = coords.get("latitude")
        lon = coords.get("longitude")

        if lat is None or lon is None:
            return _unavailable("GPS returned empty coordinates")

        logger.info("Location acquired: lat=%.4f lon=%.4f", lat, lon)
        result = {
            "available": True,
            "reason": "",
            "lat": round(lat, 3),
            "lon": round(lon, 3),
            "accuracy_m": coords.get("accuracy"),
        }
        st.session_state["_ds_location"] = result
        return result

    except ImportError:
        return _unavailable("streamlit-js-eval not installed — run: pip install streamlit-js-eval")

    except Exception as e:
        logger.error("Location fetch failed: %s", e)
        return _unavailable(f"Location error: {e}")


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in kilometres between two coordinates."""
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
