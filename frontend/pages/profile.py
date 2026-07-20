"""My Profile — DisasterShield AI"""
import streamlit as st
from frontend.design.premium_css import inject, top_navbar
from backend.services.location_service import get_location
from backend.services.weather_service import get_weather

inject("""
.profile-wrap{max-width:820px;margin:0 auto;padding:16px 24px 60px}
.p-hero{display:flex;align-items:center;gap:22px;padding:28px;margin-bottom:16px;
  background:var(--glass);border:1px solid var(--border2);border-radius:var(--r-lg);
  position:relative;overflow:hidden}
.p-hero::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent,var(--gold),transparent);opacity:.4}
.p-avatar{width:84px;height:84px;border-radius:50%;flex-shrink:0;
  background:linear-gradient(135deg,#FFD54A,#D4AF37);
  display:flex;align-items:center;justify-content:center;font-size:40px;
  border:3px solid rgba(255,213,74,.3);box-shadow:0 0 30px rgba(255,213,74,.2)}
.p-name{font-size:22px;font-weight:900;letter-spacing:-.03em;color:var(--white)}
.p-mail{font-size:13px;color:var(--gray);margin-top:3px}
.p-badges{display:flex;gap:8px;margin-top:10px;flex-wrap:wrap}
.p-badge{font-size:10.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;
  padding:4px 11px;border-radius:99px}
.p-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:16px}
.p-stat{background:var(--glass);border:1px solid var(--border2);border-radius:var(--r);
  padding:16px;text-align:center}
.p-stat-num{font-size:22px;font-weight:900;letter-spacing:-.03em}
.p-stat-lbl{font-size:10.5px;color:var(--gray);text-transform:uppercase;
  letter-spacing:.08em;margin-top:4px;font-weight:600}
.p-section{background:var(--glass);border:1px solid var(--border2);border-radius:var(--r);
  padding:20px;margin-bottom:14px}
.p-head{font-size:12.5px;font-weight:700;color:var(--white);margin-bottom:14px;
  display:flex;align-items:center;gap:8px}
.p-row{display:flex;align-items:center;justify-content:space-between;
  padding:10px 0;border-bottom:1px solid var(--border2)}
.p-row:last-child{border-bottom:none;padding-bottom:0}
.p-label{font-size:13px;color:var(--gray)}
.p-value{font-size:13px;color:var(--white);font-weight:600;text-align:right}
""")

loc = get_location()
lat = loc.get("lat") or 13.0827
lon = loc.get("lon") or 80.2707

@st.cache_data(ttl=300, show_spinner=False)
def _weather(la, lo):
    return get_weather(la, lo)

weather = _weather(lat, lon)
city = weather.get("city", "Unknown")
temp = weather.get("temperature_c", "--")

top_navbar("profile", f"{city}", str(temp))

st.markdown(f'<div class="profile-wrap"><div style="margin-bottom:24px"><div style="font-size:10px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);margin-bottom:10px">👤 MY PROFILE</div><div style="font-size:28px;font-weight:900;letter-spacing:-.04em;color:var(--white);margin-bottom:4px">Account Overview</div><div style="font-size:13px;color:var(--gray)">Your identity, monitored location, and safety readiness</div></div><div class="p-hero"><div class="p-avatar">🧑</div><div><div class="p-name">DisasterShield User</div><div class="p-mail">abc@gmail.com</div><div class="p-badges"><span class="p-badge" style="background:rgba(0,200,83,.1);color:#00C853;border:1px solid rgba(0,200,83,.25)">● Active</span><span class="p-badge" style="background:rgba(255,213,74,.08);color:var(--gold);border:1px solid rgba(255,213,74,.22)">Free Plan</span><span class="p-badge" style="background:rgba(59,130,246,.08);color:#3B82F6;border:1px solid rgba(59,130,246,.25)">📍 {city}</span></div></div></div><div class="p-grid"><div class="p-stat"><div class="p-stat-num" style="color:var(--gold)">24/7</div><div class="p-stat-lbl">AI Monitoring</div></div><div class="p-stat"><div class="p-stat-num" style="color:#00C853">25 km</div><div class="p-stat-lbl">Alert Radius</div></div><div class="p-stat"><div class="p-stat-num" style="color:#3B82F6">5</div><div class="p-stat-lbl">Active Alerts Feed</div></div></div><div class="p-section"><div class="p-head">🪪 Account Details</div><div class="p-row"><div class="p-label">Full Name</div><div class="p-value">DisasterShield User</div></div><div class="p-row"><div class="p-label">Email</div><div class="p-value">abc@gmail.com</div></div><div class="p-row"><div class="p-label">Member Since</div><div class="p-value">July 2026</div></div><div class="p-row"><div class="p-label">Account Type</div><div class="p-value">Personal · Free</div></div></div><div class="p-section"><div class="p-head">📍 Monitored Location</div><div class="p-row"><div class="p-label">Current City</div><div class="p-value">{city}</div></div><div class="p-row"><div class="p-label">Coordinates</div><div class="p-value">{lat:.4f}, {lon:.4f}</div></div><div class="p-row"><div class="p-label">Live Temperature</div><div class="p-value">{temp}°C</div></div><div class="p-row"><div class="p-label">Geofence Radius</div><div class="p-value">25 km</div></div></div><div class="p-section"><div class="p-head">🛡 Safety Readiness</div><div class="p-row"><div class="p-label">Emergency Contacts</div><div class="p-value" style="color:#00C853">Configured · 112 / 108 / 100</div></div><div class="p-row"><div class="p-label">Critical Alerts</div><div class="p-value" style="color:#00C853">Enabled</div></div><div class="p-row"><div class="p-label">Offline Guide</div><div class="p-value" style="color:#00C853">Cached</div></div><div class="p-row"><div class="p-label">Preferred Language</div><div class="p-value">English</div></div></div><div style="display:flex;gap:10px"><a href="settings" data-navigate="settings" style="flex:1;text-align:center;padding:12px;background:linear-gradient(135deg,#FFD54A,#D4AF37);color:#050505;font-size:13px;font-weight:700;border-radius:var(--r);text-decoration:none">⚙️ Manage Settings</a><a href="emergency" data-navigate="emergency" style="flex:1;text-align:center;padding:12px;background:rgba(255,77,79,.08);border:1px solid rgba(255,77,79,.25);color:#FF4D4F;font-size:13px;font-weight:700;border-radius:var(--r);text-decoration:none">🆘 Emergency Center</a></div></div>', unsafe_allow_html=True)
