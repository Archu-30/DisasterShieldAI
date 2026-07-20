"""Resources — DisasterShield AI"""
import streamlit as st
from frontend.design.premium_css import inject, top_navbar, resource_card, section_header
from backend.services.location_service import get_location
from backend.services.shelter_service import get_nearby_shelters
from backend.services.hospital_service import get_nearby_hospitals
from backend.services.maps_service import estimated_travel_minutes

inject()
top_navbar("resources")

@st.cache_data(ttl=1800, show_spinner=False)
def _shelters(lat, lon): return get_nearby_shelters(lat, lon)
@st.cache_data(ttl=1800, show_spinner=False)
def _hospitals(lat, lon): return get_nearby_hospitals(lat, lon)

loc       = get_location()
lat       = loc.get("lat") or 13.0827
lon       = loc.get("lon") or 80.2707
shelters  = _shelters(lat, lon) if loc["available"] else []
hospitals = _hospitals(lat, lon) if loc["available"] else []

st.markdown("""
<div style="padding:36px 24px 20px">
  <div style="font-size:10px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
    color:var(--gold);margin-bottom:10px">📍 NEARBY RESOURCES</div>
  <div style="font-size:30px;font-weight:900;letter-spacing:-.04em;color:var(--white);
    margin-bottom:6px">Emergency Resources</div>
  <div style="font-size:13px;color:var(--gray)">
    Hospitals, shelters, and emergency services near your location
  </div>
</div>""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "🏥 Hospitals", "🏠 Shelters", "👮 Police", "🔥 Fire Stations"
])

with tab1:
    section_header("Nearby Hospitals", "Sorted by distance · Live availability")
    if hospitals:
        for i, h in enumerate(hospitals[:10]):
            resource_card(i + 1, h["name"], h["distance_km"],
                          h.get("phone", ""), h["navigation_url"])
    else:
        st.markdown("""
<div style="margin:0 24px;padding:40px;text-align:center;background:var(--glass);
  border:1px solid var(--border2);border-radius:var(--r);color:var(--gray)">
  No hospitals found via OpenStreetMap for your location.
</div>""", unsafe_allow_html=True)

with tab2:
    section_header("Emergency Shelters", "Verified safe zones · Open 24/7 during emergencies")
    if shelters:
        for i, s in enumerate(shelters[:10]):
            resource_card(i + 1, s["name"], s["distance_km"],
                          f"~{estimated_travel_minutes(s['distance_km'])} min drive",
                          s["navigation_url"])
    else:
        st.markdown("""
<div style="margin:0 24px;padding:40px;text-align:center;background:var(--glass);
  border:1px solid var(--border2);border-radius:var(--r);color:var(--gray)">
  No shelters found for your location.
</div>""", unsafe_allow_html=True)

with tab3:
    section_header("Police Stations", "Law enforcement & security")
    for i, (name, dist) in enumerate([
        ("Central Police Station", 0.8),
        ("Adyar Police Station", 1.4),
        ("Anna Nagar Police Station", 2.1),
        ("Nungambakkam Police Station", 2.7),
        ("Kodambakkam Police Station", 3.1),
    ]):
        resource_card(i + 1, name, dist, "24/7",
                      f"https://maps.google.com/?q={name.replace(' ', '+')}")

with tab4:
    section_header("Fire Stations", "Emergency fire response")
    for i, (name, dist) in enumerate([
        ("Chennai Central Fire Station", 1.1),
        ("Adyar Fire Station", 1.9),
        ("T. Nagar Fire Station", 2.5),
        ("Tambaram Fire Station", 3.2),
        ("Anna Nagar Fire Station", 2.8),
    ]):
        resource_card(i + 1, name, dist, "24/7",
                      f"https://maps.google.com/?q={name.replace(' ', '+')}")

st.markdown('<div style="height:32px"></div>', unsafe_allow_html=True)
