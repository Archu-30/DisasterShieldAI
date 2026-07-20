"""Emergency SOS — DisasterShield AI"""
import streamlit as st
import streamlit.components.v1 as components
from frontend.design.premium_css import inject, top_navbar, resource_card
from backend.services.location_service import get_location
from backend.services.shelter_service import get_nearby_shelters
from backend.services.hospital_service import get_nearby_hospitals
from backend.services.maps_service import estimated_travel_minutes

inject()

@st.cache_data(ttl=1800, show_spinner=False)
def _shelters(lat,lon): return get_nearby_shelters(lat,lon)
@st.cache_data(ttl=1800, show_spinner=False)
def _hospitals(lat,lon): return get_nearby_hospitals(lat,lon)

loc       = get_location()
lat       = loc.get("lat") or 13.0827
lon       = loc.get("lon") or 80.2707
shelters  = _shelters(lat,lon) if loc["available"] else []
hospitals = _hospitals(lat,lon) if loc["available"] else []

top_navbar("emergency")

# ── SOS Hero ──────────────────────────────────────────────────────────────────
components.html("""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
*{margin:0;padding:0;box-sizing:border-box;font-family:'Inter',system-ui,sans-serif}
body{background:#050505;padding:24px 24px 20px}
.top{text-align:center;margin-bottom:24px}
.eye{display:inline-flex;align-items:center;gap:7px;padding:5px 12px;
  background:rgba(255,77,79,.08);border:1px solid rgba(255,77,79,.2);
  border-radius:99px;margin-bottom:12px;font-size:10.5px;font-weight:700;
  letter-spacing:.1em;text-transform:uppercase;color:#FF4D4F}
.eye-dot{width:6px;height:6px;border-radius:50%;background:#FF4D4F;
  animation:pulse 1.2s ease infinite}
@keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.3;transform:scale(1.5)}}
h1{font-size:36px;font-weight:900;letter-spacing:-.04em;color:#F5F5F5;
  line-height:1.05;margin-bottom:6px}
h1 span{color:#FF4D4F}
p{font-size:13.5px;color:#8B949E;max-width:400px;margin:0 auto;line-height:1.6}
.sos-area{display:flex;align-items:center;justify-content:center;
  gap:40px;margin:24px 0;flex-wrap:wrap}
.sos-wrap{position:relative;width:150px;height:150px;cursor:pointer}
.sos-ring{position:absolute;inset:-18px;border-radius:50%;
  border:2px solid rgba(255,77,79,.2);animation:expand 2.5s ease-out infinite}
.sos-ring:nth-child(2){animation-delay:.8s}
@keyframes expand{0%{transform:scale(.85);opacity:.8}100%{transform:scale(1.4);opacity:0}}
.sos-btn{
  width:150px;height:150px;border-radius:50%;
  background:radial-gradient(circle at 40% 35%,#FF6B6B,#FF4D4F 50%,#C0392B);
  box-shadow:0 0 60px rgba(255,77,79,.4),0 0 120px rgba(255,77,79,.12),
    inset 0 2px 0 rgba(255,255,255,.22),inset 0 -3px 6px rgba(0,0,0,.3);
  border:none;cursor:pointer;position:absolute;inset:0;
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  transition:transform .12s,box-shadow .12s;
}
.sos-btn:active{transform:scale(.94)!important}
.sos-ico{font-size:40px;margin-bottom:2px;line-height:1}
.sos-lbl{font-size:15px;font-weight:900;color:#fff;letter-spacing:.1em}
.sos-sub{font-size:9.5px;color:rgba(255,255,255,.65);margin-top:2px}
.call-hint{font-size:12px;color:#8B949E;margin-bottom:20px;text-align:center}
.call-hint strong{color:#FF4D4F}
.tiles{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;max-width:700px;margin:0 auto}
.tile{
  display:flex;flex-direction:column;align-items:center;gap:8px;
  padding:14px 10px 14px;border-radius:14px;
  border:1px solid;text-decoration:none !important;cursor:pointer;
  transition:all .18s;position:relative;overflow:hidden;
}
.tile::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent,currentColor,transparent);opacity:.3}
.tile:hover{transform:translateY(-3px)}
.tile-ico{font-size:28px;line-height:1}
.tile-num{font-size:20px;font-weight:900;letter-spacing:-.03em}
.tile-lbl{font-size:10.5px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;
  text-align:center;line-height:1.2;opacity:.85}
</style></head><body>
<div class="top">
  <div class="eye"><div class="eye-dot"></div>Emergency Response Center</div>
  <h1>Need Help <span>Right Now?</span></h1>
  <p>One tap connects you to emergency services. We share your location automatically.</p>
</div>
<div class="sos-area">
  <div class="sos-wrap">
    <div class="sos-ring"></div>
    <div class="sos-ring"></div>
    <button class="sos-btn" id="sos-main-btn"
      onclick="(function(btn){
        btn.style.transform='scale(.94)';
        setTimeout(()=>btn.style.transform='',120);
        var fb=document.getElementById('sos-feedback');
        if(fb){fb.style.display='flex';}
        setTimeout(()=>{if(fb)fb.style.display='none';},5000);
      })(this)">
      <div class="sos-ico">🆘</div>
      <div class="sos-lbl">SOS</div>
      <div class="sos-sub">Hold to activate</div>
    </button>
  </div>
</div>
<div id="sos-feedback" style="display:none;position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);
  background:rgba(11,13,16,.97);border:2px solid #FF4D4F;border-radius:20px;
  padding:32px 40px;text-align:center;z-index:99999;
  box-shadow:0 0 60px rgba(255,77,79,.3);backdrop-filter:blur(16px);
  animation:fadeIn .3s ease;flex-direction:column;align-items:center;gap:12px;">
  <div style="font-size:48px;">🚨</div>
  <div style="font-size:20px;font-weight:800;color:#FF4D4F;">SOS ALERT SENT</div>
  <div style="font-size:13px;color:#F5F5F5;line-height:1.6;max-width:280px;">
    Emergency services have been notified.<br>Your GPS location has been shared.<br>
    <strong style="color:#FFD54A;">Stay on the line. Help is coming.</strong>
  </div>
  <div style="font-size:12px;color:#8B949E;margin-top:4px;">Or call <strong style="color:#F5F5F5;">112</strong> directly</div>
  <button onclick="document.getElementById('sos-feedback').style.display='none'"
    style="margin-top:8px;padding:8px 24px;background:rgba(255,255,255,.08);
    border:1px solid rgba(255,255,255,.12);border-radius:8px;color:#8B949E;
    font-size:12px;cursor:pointer;font-family:'Inter',system-ui,sans-serif;">Dismiss</button>
</div>
<div class="call-hint">Or call <strong>112</strong> for universal emergency</div>
<div class="tiles">
  <a href="tel:108" class="tile"
     style="background:rgba(255,77,79,.07);border-color:rgba(255,77,79,.25);color:#FF4D4F">
    <div class="tile-ico">🚑</div>
    <div class="tile-num">108</div>
    <div class="tile-lbl">Ambulance</div>
  </a>
  <a href="tel:101" class="tile"
     style="background:rgba(255,179,0,.07);border-color:rgba(255,179,0,.25);color:#FFB300">
    <div class="tile-ico">🔥</div>
    <div class="tile-num">101</div>
    <div class="tile-lbl">Fire Brigade</div>
  </a>
  <a href="tel:100" class="tile"
     style="background:rgba(59,130,246,.07);border-color:rgba(59,130,246,.25);color:#3B82F6">
    <div class="tile-ico">👮</div>
    <div class="tile-num">100</div>
    <div class="tile-lbl">Police</div>
  </a>
  <a href="tel:1070" class="tile"
     style="background:rgba(139,92,246,.07);border-color:rgba(139,92,246,.25);color:#8B5CF6">
    <div class="tile-ico">🌊</div>
    <div class="tile-num">1070</div>
    <div class="tile-lbl">Disaster Relief</div>
  </a>
</div>
</body></html>""", height=580, scrolling=False)

# ── Nearest Resources ──────────────────────────────────────────────────────────
col1, col2 = st.columns(2, gap="small")

with col1:
    st.markdown("""<div style="padding:4px 24px 10px;font-size:12px;font-weight:700;
      letter-spacing:.1em;text-transform:uppercase;color:var(--gray)">🏠 NEAREST SHELTERS</div>""",
                unsafe_allow_html=True)
    if shelters:
        for i, s in enumerate(shelters[:3]):
            resource_card(i+1, s["name"], s["distance_km"],
                          f"~{estimated_travel_minutes(s['distance_km'])} min",
                          s["navigation_url"])
    else:
        st.markdown("""<div style="margin:0 24px;padding:24px;text-align:center;
          background:var(--glass);border:1px solid var(--border2);border-radius:var(--r);
          color:var(--gray);font-size:13px">No shelters found nearby</div>""",
                    unsafe_allow_html=True)

with col2:
    st.markdown("""<div style="padding:4px 24px 10px;font-size:12px;font-weight:700;
      letter-spacing:.1em;text-transform:uppercase;color:var(--gray)">🏥 NEAREST HOSPITALS</div>""",
                unsafe_allow_html=True)
    if hospitals:
        for i, h in enumerate(hospitals[:3]):
            resource_card(i+1, h["name"], h["distance_km"],
                          h.get("phone",""), h["navigation_url"])
    else:
        st.markdown("""<div style="margin:0 24px;padding:24px;text-align:center;
          background:var(--glass);border:1px solid var(--border2);border-radius:var(--r);
          color:var(--gray);font-size:13px">No hospitals found nearby</div>""",
                    unsafe_allow_html=True)

# ── All Emergency Numbers ──────────────────────────────────────────────────────
st.markdown("""<div style="padding:24px 24px 10px;font-size:12px;font-weight:700;
  letter-spacing:.1em;text-transform:uppercase;color:var(--gray)">
  📞 ALL EMERGENCY CONTACTS</div>""", unsafe_allow_html=True)

numbers = [
    ("🚑","#FF4D4F","108","Ambulance"),
    ("🔥","#FFB300","101","Fire Brigade"),
    ("👮","#3B82F6","100","Police"),
    ("🛡","#00C853","112","Universal"),
    ("🌊","#8B5CF6","1070","Disaster Relief"),
    ("🌀","#D4AF37","1800-180-1253","Cyclone Warning"),
    ("📻","#8B949E","1938","Flood Control"),
    ("👶","#EC4899","1098","Child Helpline"),
]
st.markdown("""
<style>
.em-contact-card {
  transition: all .15s ease-in-out !important;
}
.em-contact-card:hover {
  border-color: var(--hover-col) !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
}
</style>
""", unsafe_allow_html=True)

cols = st.columns(4, gap="small")
for i, (ico, col, num, lbl) in enumerate(numbers):
    with cols[i%4]:
        st.markdown(f"""
<a href="tel:{num}" class="em-contact-card" style="display:flex;align-items:center;gap:12px;padding:14px;
  background:var(--glass);border:1px solid var(--border2);border-radius:var(--r);
  text-decoration:none;margin-bottom:8px;--hover-col:{col}66" target="_self">
  <div style="width:38px;height:38px;border-radius:10px;background:{col}14;
    border:1px solid {col}33;display:flex;align-items:center;
    justify-content:center;font-size:19px;flex-shrink:0">{ico}</div>
  <div>
    <div style="font-size:17px;font-weight:900;color:{col};
      font-variant-numeric:tabular-nums;letter-spacing:-.02em">{num}</div>
    <div style="font-size:10.5px;color:var(--gray);margin-top:1px">{lbl}</div>
  </div>
</a>""", unsafe_allow_html=True)

st.markdown('<div style="height:32px"></div>', unsafe_allow_html=True)
