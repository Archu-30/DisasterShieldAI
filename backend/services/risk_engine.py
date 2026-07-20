from backend.services.config import RISK_THRESHOLDS


def _prediction(disaster: str, level: str, score: int, confidence: int, reason: str, action: str) -> dict:
    return {
        "disaster": disaster,
        "risk_level": level,
        "risk_score": score,
        "confidence": confidence,
        "reason": reason,
        "recommended_action": action,
    }


def predict_risks(weather: dict) -> list[dict]:
    """
    Given a weather dict (from weather_service.get_weather),
    return a list of active risk predictions sorted by risk_score descending.
    Returns empty list if weather is unavailable.
    """
    if not weather.get("available"):
        return []

    rain = weather.get("rainfall_mm") or 0.0
    wind = weather.get("wind_kmh") or 0.0
    temp = weather.get("temperature_c") or 0.0
    humidity = weather.get("humidity_pct") or 0.0
    desc = (weather.get("description") or "").lower()

    predictions = []
    t = RISK_THRESHOLDS

    # ── Flood ─────────────────────────────────────────────────────────────────
    if rain >= t["flood"]["high"]["rainfall_mm"]:
        predictions.append(_prediction(
            "Flood", "High", 80, 85,
            f"Rainfall {rain} mm/h exceeds flood threshold (80 mm/h)",
            "Move immediately to higher ground. Avoid roads and low-lying areas."
        ))
    elif rain >= t["flood"]["moderate"]["rainfall_mm"]:
        predictions.append(_prediction(
            "Flood", "Moderate", 55, 75,
            f"Rainfall {rain} mm/h is elevated (50–80 mm/h)",
            "Monitor water levels. Avoid low-lying areas. Keep emergency kit ready."
        ))
    elif rain >= t["flood"]["low"]["rainfall_mm"]:
        predictions.append(_prediction(
            "Flood", "Low", 25, 65,
            f"Rainfall {rain} mm/h is light but notable",
            "Stay alert. Avoid areas near rivers or drainage channels."
        ))

    # ── Cyclone ───────────────────────────────────────────────────────────────
    if wind >= t["cyclone"]["high"]["wind_kmh"]:
        predictions.append(_prediction(
            "Cyclone", "High", 82, 88,
            f"Wind speed {wind} km/h exceeds cyclone warning threshold (70 km/h)",
            "Seek strong shelter immediately. Stay indoors away from windows."
        ))
    elif wind >= t["cyclone"]["moderate"]["wind_kmh"]:
        predictions.append(_prediction(
            "Cyclone", "Moderate", 55, 78,
            f"Wind speed {wind} km/h is elevated (50–70 km/h)",
            "Secure loose objects outside. Monitor official weather bulletins."
        ))
    elif wind >= t["cyclone"]["low"]["wind_kmh"]:
        predictions.append(_prediction(
            "Cyclone", "Low", 22, 60,
            f"Wind speed {wind} km/h is notable",
            "Be cautious outdoors. Check weather updates."
        ))

    # ── Heatwave ──────────────────────────────────────────────────────────────
    if temp >= t["heatwave"]["critical"]["temp_c"]:
        predictions.append(_prediction(
            "Heatwave", "Critical", 95, 92,
            f"Temperature {temp}°C — extreme heatwave conditions",
            "Stay indoors. Drink water every 15 minutes. Seek medical help if dizzy."
        ))
    elif temp >= t["heatwave"]["high"]["temp_c"]:
        predictions.append(_prediction(
            "Heatwave", "High", 72, 85,
            f"Temperature {temp}°C — heatwave warning level",
            "Avoid outdoor activity 11am–4pm. Drink plenty of water. Wear light clothing."
        ))
    elif temp >= t["heatwave"]["moderate"]["temp_c"]:
        predictions.append(_prediction(
            "Heatwave", "Moderate", 45, 75,
            f"Temperature {temp}°C — elevated heat",
            "Stay hydrated. Reduce physical exertion outdoors."
        ))

    # ── Thunderstorm ──────────────────────────────────────────────────────────
    ts = t["thunderstorm"]["high"]
    if (wind >= ts["wind_kmh"] and rain >= ts["rainfall_mm"]) or "thunderstorm" in desc:
        predictions.append(_prediction(
            "Thunderstorm", "High", 74, 80,
            f"Thunderstorm conditions detected (wind {wind} km/h, rain {rain} mm/h)",
            "Stay indoors. Unplug electronics. Avoid trees and open fields."
        ))

    # ── Heavy Rain ────────────────────────────────────────────────────────────
    hr = t["heavy_rain"]["moderate"]
    if rain >= hr["rainfall_mm"] and "flood" not in [p["disaster"].lower() for p in predictions]:
        predictions.append(_prediction(
            "Heavy Rain", "Moderate", 50, 80,
            f"Rainfall {rain} mm/h qualifies as heavy rain",
            "Avoid driving. Watch for waterlogging and drainage overflow."
        ))

    # ── Landslide (weather-estimate only) ────────────────────────────────────
    ls = t["landslide"]["moderate"]
    if rain >= ls["rainfall_mm"] and humidity >= ls["humidity_pct"]:
        predictions.append(_prediction(
            "Landslide", "Moderate", 52, 55,
            f"High rainfall ({rain} mm/h) + humidity ({humidity}%) — landslide-prone conditions",
            "Avoid hilly terrain and steep slopes. Do not travel on mountain roads."
        ))

    predictions.sort(key=lambda x: x["risk_score"], reverse=True)
    return predictions


def highest_risk(predictions: list[dict]) -> dict | None:
    """Return the single highest-risk prediction, or None."""
    return predictions[0] if predictions else None
