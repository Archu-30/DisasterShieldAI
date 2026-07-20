import streamlit as st


def _js_notify(title: str, body: str) -> str:
    """Return JavaScript that requests permission then fires a browser notification."""
    # Escape single quotes in content
    safe_title = title.replace("'", "\\'")
    safe_body = body.replace("'", "\\'")
    return f"""
Notification.requestPermission().then(function(permission) {{
    if (permission === 'granted') {{
        new Notification('{safe_title}', {{
            body: '{safe_body}',
            icon: 'https://cdn-icons-png.flaticon.com/512/2972/2972531.png'
        }});
    }}
}});
"""


def trigger_browser_alert(risk: dict, nearest_shelter: dict | None, nearest_hospital: dict | None) -> None:
    """
    Fire a browser notification when risk level is High or Critical.
    Also displays a Streamlit warning banner.
    risk: dict from risk_engine.predict_risks()
    """
    level = risk.get("risk_level", "")
    if level not in ("High", "Critical"):
        return

    disaster = risk.get("disaster", "Disaster")
    action = risk.get("recommended_action", "Follow official guidance.")

    shelter_line = ""
    if nearest_shelter:
        km = nearest_shelter["distance_km"]
        from backend.services.maps_service import estimated_travel_minutes
        mins = estimated_travel_minutes(km, "walking")
        shelter_line = f"Nearest Shelter: {km} km (~{mins} min walk). "

    hospital_line = ""
    if nearest_hospital:
        hospital_line = f"Nearest Hospital: {nearest_hospital['distance_km']} km."

    notif_title = f"⚠ {disaster.upper()} ALERT — Risk Level: {level}"
    notif_body = (
        f"{action} "
        f"{shelter_line}"
        f"{hospital_line} "
        f"Emergency: 112 | Ambulance: 108"
    )

    # Streamlit on-page banner
    st.error(f"""
**⚠ {disaster} ALERT — {level} Risk**

{action}

{shelter_line}{hospital_line}

**Emergency: 112 | Ambulance: 108 | Fire: 101 | Police: 100**
""")

    # Browser notification via JS
    try:
        from streamlit_js_eval import streamlit_js_eval
        streamlit_js_eval(js_expressions=_js_notify(notif_title, notif_body), key=f"notif_{disaster}_{level}")
    except Exception:
        pass  # JS notification is best-effort; banner above already shown
