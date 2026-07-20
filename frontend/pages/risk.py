"""Risk Monitor — DisasterShield AI"""
import json, time
import streamlit as st
import streamlit.components.v1 as components
from frontend.design.premium_css import inject, top_navbar, section_header
from backend.services.location_service import get_location
from backend.services.weather_service import get_weather
from backend.services.risk_engine import predict_risks

inject()

@st.cache_data(ttl=300, show_spinner=False)
def _weather(lat, lon): return get_weather(lat, lon)
@st.cache_data(ttl=300, show_spinner=False)
def _risks(wj): return predict_risks(json.loads(wj))

loc     = get_location()
lat     = loc.get("lat") or 13.0827
lon     = loc.get("lon") or 80.2707
weather = _weather(lat, lon)
preds   = _risks(json.dumps(weather)) if loc["available"] else []
city    = weather.get("city","Unknown")
temp    = weather.get("temperature_c","--")

top_navbar("risk", f"{city}, {weather.get('country','')}", str(temp))

rc = {"Low":"#00C853","Moderate":"#FFB300","High":"#FF4D4F","Critical":"#8B5CF6"}
dis_icons = {"Flood":"🌊","Cyclone":"🌀","Thunderstorm":"⚡","Heatwave":"🌡",
             "Heavy Rain":"🌧","Landslide":"⛰","Drought":"☀","Wildfire":"🔥"}

# ── Page Hero ─────────────────────────────────────────────────────────────────
top_risk = preds[0] if preds else None
risk_lvl = top_risk["risk_level"] if top_risk else "Low"
risk_sc  = top_risk["risk_score"] if top_risk else 0
risk_col = rc.get(risk_lvl,"#00C853")

st.markdown(f"""
<div style="padding:16px 24px 16px;font-family:var(--font)">
  <div style="font-size:10px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
    color:var(--gold);margin-bottom:8px">📊 Risk Intelligence Center</div>
  <div style="display:flex;align-items:flex-end;justify-content:space-between;flex-wrap:wrap;gap:16px">
    <div>
      <div style="font-size:30px;font-weight:900;letter-spacing:-.04em;color:var(--white);
        margin-bottom:4px">Disaster Risk Monitor</div>
      <div style="font-size:13px;color:var(--gray)">AI-powered risk assessment for {city} · Updated {time.strftime('%H:%M')}</div>
    </div>
    <div style="display:flex;align-items:center;gap:12px;padding:14px 20px;
      background:var(--glass);border:1px solid {risk_col}33;border-radius:var(--r-lg)">
      <div style="width:48px;height:48px;border-radius:50%;background:{risk_col}18;
        border:2px solid {risk_col}44;display:flex;align-items:center;justify-content:center;
        font-size:22px;animation:glow 2s ease infinite">
        {'🟢' if risk_lvl=='Low' else '🟡' if risk_lvl=='Moderate' else '🔴' if risk_lvl=='High' else '🟣'}
      </div>
      <div>
        <div style="font-size:22px;font-weight:900;color:{risk_col};letter-spacing:-.04em">{risk_sc}/100</div>
        <div style="font-size:11px;color:var(--gray);text-transform:uppercase;letter-spacing:.08em;font-weight:600">{risk_lvl} Risk</div>
      </div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

# ── Risk Cards Grid ────────────────────────────────────────────────────────────
section_header("Active Threat Assessment", "AI-analyzed disaster probabilities", "AI")

if preds:
    cols = st.columns(min(len(preds), 3), gap="small")
    for i, p in enumerate(preds[:6]):
        col2   = rc.get(p["risk_level"], "#00C853")
        ico    = dis_icons.get(p["disaster"],"⚠")
        conf   = p.get("confidence", 0)
        reason = p.get("reason","")
        action = p.get("recommended_action","Monitor situation.")
        sc     = p["risk_score"]
        circ   = 188
        off    = circ - (sc/100)*circ
        with cols[i % 3]:
            st.markdown(f"""
<div class="ds-risk-card" style="background:var(--glass);border:1px solid {col2}22;border-radius:var(--r);
  padding:20px;margin-bottom:10px;position:relative;overflow:hidden;
  cursor:default;--hover-col:{col2}44">
  <div style="position:absolute;top:0;left:0;right:0;height:1px;
    background:linear-gradient(90deg,transparent,{col2}55,transparent)"></div>
  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px">
    <div style="display:flex;align-items:center;gap:10px">
      <div style="width:38px;height:38px;border-radius:11px;background:{col2}14;
        border:1px solid {col2}33;display:flex;align-items:center;justify-content:center;font-size:19px">{ico}</div>
      <div>
        <div style="font-size:13.5px;font-weight:700;color:var(--white)">{p['disaster']}</div>
        <div style="font-size:10px;font-weight:700;padding:1px 7px;border-radius:99px;
          background:{col2}14;color:{col2};letter-spacing:.05em;
          text-transform:uppercase;margin-top:2px;display:inline-block">{p['risk_level']}</div>
      </div>
    </div>
    <div style="text-align:right">
      <svg width="52" height="52" viewBox="0 0 60 60">
        <circle cx="30" cy="30" r="22" fill="none" stroke="rgba(255,255,255,.05)" stroke-width="6"/>
        <circle cx="30" cy="30" r="22" fill="none" stroke="{col2}" stroke-width="6"
          stroke-linecap="round" stroke-dasharray="{circ}" stroke-dashoffset="{circ}"
          transform="rotate(-90 30 30)"
          style="animation:fillGauge .9s .2s cubic-bezier(.4,0,.2,1) forwards;
            filter:drop-shadow(0 0 6px {col2}66)"/>
      </svg>
      <div style="font-size:11px;font-weight:800;color:{col2};margin-top:-6px;text-align:center">
        {sc}
      </div>
    </div>
  </div>
  <div style="font-size:12px;color:var(--gray);line-height:1.5;margin-bottom:10px">{reason[:100]}{"…" if len(reason)>100 else ""}</div>
  <div style="font-size:11px;color:{col2};background:{col2}0d;border:1px solid {col2}22;
    border-radius:7px;padding:7px 10px;line-height:1.4">💡 {action[:80]}{"…" if len(action)>80 else ""}</div>
  <div style="display:flex;align-items:center;gap:6px;margin-top:10px">
    <div style="font-size:10px;color:var(--gray)">Confidence</div>
    <div style="flex:1;background:rgba(255,255,255,.05);border-radius:99px;height:4px">
      <div style="width:{conf}%;height:100%;border-radius:99px;background:{col2};
        transition:width 1s ease"></div>
    </div>
    <div style="font-size:10px;font-weight:700;color:{col2}">{conf}%</div>
  </div>
</div>""", unsafe_allow_html=True)
else:
    st.markdown("""
<div style="margin:0 24px;padding:40px;text-align:center;background:var(--glass);
  border:1px solid var(--border2);border-radius:var(--r)">
  <div style="font-size:36px;margin-bottom:12px">🟢</div>
  <div style="font-size:16px;font-weight:700;color:var(--white);margin-bottom:6px">All Clear</div>
  <div style="font-size:13px;color:var(--gray)">No active threats detected for your location.</div>
</div>""", unsafe_allow_html=True)

st.markdown("""<style>
@keyframes fillGauge{to{stroke-dashoffset:0}}
.ds-risk-card {
  transition: all .2s ease-in-out !important;
}
.ds-risk-card:hover {
  border-color: var(--hover-col) !important;
  transform: translateY(-3px) !important;
  box-shadow: 0 4px 15px rgba(0,0,0,0.25) !important;
}
</style>""",
            unsafe_allow_html=True)

# ── AI Recommendation ──────────────────────────────────────────────────────────
if top_risk:
    section_header("AI Recommendation", "Based on current conditions")
    action = top_risk.get("recommended_action","Monitor the situation.")
    reason = top_risk.get("reason","")
    st.markdown(f"""
<div style="margin:0 24px;padding:20px;background:var(--glass);
  border:1px solid rgba(255,213,74,.15);border-radius:var(--r);
  display:flex;align-items:flex-start;gap:16px">
  <div style="width:44px;height:44px;border-radius:12px;
    background:linear-gradient(135deg,#FFD54A,#D4AF37);
    display:flex;align-items:center;justify-content:center;
    font-size:22px;flex-shrink:0;box-shadow:0 0 20px rgba(255,213,74,.3)">🛡</div>
  <div style="flex:1">
    <div style="font-size:13.5px;font-weight:700;color:var(--gold);margin-bottom:6px">
      DisasterShield AI Analysis
    </div>
    <div style="font-size:13px;color:var(--white);line-height:1.65;margin-bottom:10px">{reason}</div>
    <div style="font-size:12.5px;color:var(--gray);background:rgba(255,213,74,.04);
      border:1px solid rgba(255,213,74,.1);border-radius:8px;padding:10px 14px;line-height:1.5">
      <strong style="color:var(--gold)">Recommended Action:</strong> {action}
    </div>
  </div>
</div>""", unsafe_allow_html=True)

st.markdown('<div style="height:32px"></div>', unsafe_allow_html=True)
