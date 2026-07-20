def get_navigation_url(from_lat: float, from_lon: float, to_lat: float, to_lon: float) -> str:
    """Generate a Google Maps navigation URL between two coordinates."""
    return f"https://www.google.com/maps/dir/{from_lat},{from_lon}/{to_lat},{to_lon}"


def estimated_travel_minutes(distance_km: float, mode: str = "walking") -> int:
    """
    Rough travel time estimate.
    Walking ~5 km/h, Driving ~30 km/h (urban emergency).
    """
    speed = 5.0 if mode == "walking" else 30.0
    return max(1, round((distance_km / speed) * 60))
