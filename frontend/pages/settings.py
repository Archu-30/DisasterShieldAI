"""Settings — DisasterShield AI"""
import json
import streamlit as st
from frontend.design.premium_css import inject, top_navbar
from backend.services import push_service
from backend.services.location_service import get_location

inject("""
.settings-wrap { max-width: 760px; margin: 0 auto; padding: 16px 24px 60px; }
.s-head { font-size: 14px; font-weight: 700; color: var(--white); margin-bottom: 18px; display: flex; align-items: center; gap: 8px; border-bottom: 1px solid var(--border2); padding-bottom: 8px; }
.s-label { font-size: 13.5px; font-weight: 600; color: var(--white); }
.s-sub { font-size: 11.5px; color: var(--gray); margin-top: 2px; }
.s-row { margin-bottom: 4px; }

/* Style Streamlit containers as settings sections */
div[data-testid="stVerticalBlockBorderWrapper"] {
  background: var(--glass) !important;
  border: 1px solid var(--border2) !important;
  border-radius: var(--r) !important;
  padding: 24px !important;
  margin-bottom: 16px !important;
  box-shadow: var(--shadow) !important;
}

/* Style the native toggle buttons */
div[data-testid="stCheckbox"] label, div[data-testid="stToggle"] label {
  color: var(--white) !important;
}

/* Style primary buttons for save settings */
.stButton > button[kind="primary"] {
  background: linear-gradient(135deg, #FFD54A, #D4AF37) !important;
  color: #050505 !important;
  font-weight: 700 !important;
  border: none !important;
  border-radius: var(--r) !important;
  padding: 12px !important;
  font-size: 14px !important;
}
.stButton > button[kind="primary"]:hover {
  opacity: 0.9 !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 15px rgba(255, 213, 74, 0.3) !important;
}
""")

top_navbar("settings")

# ── Closed-browser push: sync the browser's push subscription to the server ──
# The navbar's Enable flow stores the Web Push subscription in localStorage;
# here we read it back into Python (one component round-trip, only until
# synced) and persist it so the background daemon can push alerts even when
# the browser is fully closed.
if not st.session_state.get("_push_synced"):
    try:
        from streamlit_js_eval import streamlit_js_eval
        _sub_raw = streamlit_js_eval(
            js_expressions="localStorage.getItem('ds_push_sub')",
            key="ds_push_sub_sync",
        )
        if _sub_raw:
            _loc = get_location()
            _lat = _loc.get("lat") or 13.0827
            _lon = _loc.get("lon") or 80.2707
            if push_service.save_subscription(json.loads(_sub_raw), _lat, _lon):
                st.session_state["_push_synced"] = True
    except Exception:
        pass

st.markdown("""
<div class="settings-wrap">
  <div style="margin-bottom:28px">
    <div style="font-size:10px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
      color:var(--gold);margin-bottom:10px">⚙️ SETTINGS</div>
    <div style="font-size:28px;font-weight:900;letter-spacing:-.04em;color:var(--white);
      margin-bottom:4px">Platform Settings</div>
    <div style="font-size:13px;color:var(--gray)">Manage notifications, alerts, and preferences</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Wrap settings inside a wrapper div to match padding
st.markdown('<div class="settings-wrap" style="padding-top:0; padding-bottom:0">', unsafe_allow_html=True)

# 1. Notifications
with st.container(border=True):
    st.markdown('<div class="s-head">🔔 Notification Settings</div>', unsafe_allow_html=True)
    
    # Row 1
    c1, c2 = st.columns([5, 1])
    with c1:
        st.markdown('<div class="s-row"><div class="s-label">Push Notifications</div><div class="s-sub">Receive alerts on this device</div></div>', unsafe_allow_html=True)
    with c2:
        st.toggle("Push Notifications", value=True, key="push_notif", label_visibility="collapsed")
        
    # Row 2
    c1, c2 = st.columns([5, 1])
    with c1:
        st.markdown('<div class="s-row"><div class="s-label">Critical Alerts</div><div class="s-sub">Full-screen warnings for critical disasters</div></div>', unsafe_allow_html=True)
    with c2:
        st.toggle("Critical Alerts", value=True, key="crit_alerts", label_visibility="collapsed")
        
    # Row 3
    c1, c2 = st.columns([5, 1])
    with c1:
        st.markdown('<div class="s-row"><div class="s-label">Sound Alerts</div><div class="s-sub">Play sound for emergency notifications</div></div>', unsafe_allow_html=True)
    with c2:
        st.toggle("Sound Alerts", value=True, key="sound_alerts", label_visibility="collapsed")
        
    # Row 4
    c1, c2 = st.columns([5, 1])
    with c1:
        st.markdown('<div class="s-row"><div class="s-label">Weather Updates</div><div class="s-sub">Hourly weather condition changes</div></div>', unsafe_allow_html=True)
    with c2:
        st.toggle("Weather Updates", value=False, key="weather_updates", label_visibility="collapsed")
        
    # Row 5
    c1, c2 = st.columns([5, 1])
    with c1:
        st.markdown('<div class="s-row"><div class="s-label">AI Recommendations</div><div class="s-sub">Daily safety tips from AI analysis</div></div>', unsafe_allow_html=True)
    with c2:
        st.toggle("AI Recommendations", value=True, key="ai_rec", label_visibility="collapsed")

# 2. Alert Thresholds
with st.container(border=True):
    st.markdown('<div class="s-head">⚡ Alert Thresholds</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="s-label">Minimum Alert Level</div><div class="s-sub">Only notify for this severity and above</div>', unsafe_allow_html=True)
    threshold = st.select_slider(
        "Minimum Alert Level", options=["🟢 Low", "🟡 Moderate", "🟠 High", "🔴 Critical"],
        value="🟡 Moderate", key="threshold_slider", label_visibility="collapsed"
    )
    
    st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
    st.markdown('<div class="s-label">Geofence Radius</div><div class="s-sub">Alert radius around your location</div>', unsafe_allow_html=True)
    radius = st.select_slider(
        "Geofence Radius", options=["5 km","10 km","25 km","50 km","100 km"],
        value="25 km", key="radius_slider", label_visibility="collapsed"
    )

# 3. Data & Privacy
with st.container(border=True):
    st.markdown('<div class="s-head">🔒 Data &amp; Privacy</div>', unsafe_allow_html=True)
    
    # Row 1
    c1, c2 = st.columns([5, 1])
    with c1:
        st.markdown('<div class="s-row"><div class="s-label">Location Sharing</div><div class="s-sub">Share GPS for personalized alerts</div></div>', unsafe_allow_html=True)
    with c2:
        st.toggle("Location Sharing", value=True, key="loc_sharing", label_visibility="collapsed")
        
    # Row 2
    c1, c2 = st.columns([5, 1])
    with c1:
        st.markdown('<div class="s-row"><div class="s-label">Anonymous Analytics</div><div class="s-sub">Help improve AI models (no personal data)</div></div>', unsafe_allow_html=True)
    with c2:
        st.toggle("Anonymous Analytics", value=True, key="anon_analytics", label_visibility="collapsed")
        
    # Row 3
    c1, c2 = st.columns([5, 1])
    with c1:
        st.markdown('<div class="s-row"><div class="s-label">Offline Mode</div><div class="s-sub">Cache guides and maps for offline access</div></div>', unsafe_allow_html=True)
    with c2:
        st.toggle("Offline Mode", value=True, key="offline_mode", label_visibility="collapsed")

# 4. Appearance
with st.container(border=True):
    st.markdown('<div class="s-head">🎨 Appearance</div>', unsafe_allow_html=True)
    
    # Row 1
    c1, c2 = st.columns([5, 2])
    with c1:
        st.markdown('<div class="s-row"><div class="s-label">Theme</div><div class="s-sub">Luxury Black &amp; Gold (only theme)</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div style="text-align:right;font-size:12px;padding:5px 12px;background:rgba(255,213,74,.08);border:1px solid rgba(255,213,74,.2);border-radius:7px;color:var(--gold);font-weight:600;display:inline-block">Dark · Gold ✓</div>', unsafe_allow_html=True)
        
    # Row 2
    c1, c2 = st.columns([5, 1])
    with c1:
        st.markdown('<div class="s-row"><div class="s-label">Reduced Motion</div><div class="s-sub">Disable animations for accessibility</div></div>', unsafe_allow_html=True)
    with c2:
        st.toggle("Reduced Motion", value=False, key="red_motion", label_visibility="collapsed")
        
    # Row 3
    c1, c2 = st.columns([5, 1])
    with c1:
        st.markdown('<div class="s-row"><div class="s-label">Compact Mode</div><div class="s-sub">Denser information layout</div></div>', unsafe_allow_html=True)
    with c2:
        st.toggle("Compact Mode", value=False, key="compact_mode", label_visibility="collapsed")

# 5. Closed-browser push alerts
with st.container(border=True):
    st.markdown('<div class="s-head">📲 Closed-Browser Push Alerts</div>', unsafe_allow_html=True)
    _n_subs = push_service.subscription_count()
    if st.session_state.get("_push_synced") or _n_subs:
        st.markdown(
            f'<div class="s-row"><div class="s-label" style="color:#00C853">✅ '
            f'{_n_subs} device(s) registered for closed-browser alerts</div>'
            '<div class="s-sub">The server re-checks disaster risk every 5 minutes and pushes '
            'High/Critical alerts to your OS notification drawer — even when the browser is closed.</div></div>',
            unsafe_allow_html=True)
        if st.button("📤 Send Test Push Notification", use_container_width=True):
            sent = push_service.send_to_all(
                "🛡 DisasterShield Test Alert",
                "Push delivery works! You will receive disaster alerts even when the browser is closed.",
                critical=False,
            )
            if sent:
                st.toast(f"Test push sent to {sent} device(s) — check your notification drawer!", icon="📲")
            else:
                st.toast("No push delivered — re-enable from the 🔔 bell panel.", icon="⚠️")
    else:
        st.markdown(
            '<div class="s-row"><div class="s-label">Not enabled yet</div>'
            '<div class="s-sub">Open the 🔔 bell panel in the navbar, click <b>Enable</b>, accept the '
            'browser prompt, then revisit this page to register this device.</div></div>',
            unsafe_allow_html=True)

if st.button("Save Settings", type="primary", use_container_width=True):
    st.toast("Settings saved successfully!", icon="✅")

st.markdown('</div>', unsafe_allow_html=True)
