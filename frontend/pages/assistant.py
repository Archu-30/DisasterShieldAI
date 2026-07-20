"""AI Assistant — DisasterShield AI · ChatGPT-style"""
import streamlit as st
import streamlit.components.v1 as components
from backend.graph.workflow import get_response
from frontend.design.premium_css import inject, top_navbar, chat_bubble
from backend.services.location_service import get_location
from backend.services.weather_service import get_weather


inject("""
.chat-page{max-width:820px;margin:0 auto;padding-bottom:140px}
.chat-hero{text-align:center;padding:16px 24px 20px}
.suggestions{display:grid;grid-template-columns:repeat(2,1fr);gap:9px;
  max-width:640px;margin:0 auto 28px;padding:0 24px}
.sug-card{
  background:var(--glass);border:1px solid var(--border2);
  border-radius:var(--r);padding:14px 16px;
  cursor:pointer;transition:all .18s;text-align:left;
  font-family:var(--font);width:100%;
}
.sug-card:hover{background:rgba(255,213,74,.04);border-color:var(--border);transform:translateY(-2px)}
.sug-ico{font-size:20px;margin-bottom:8px;display:block}
.sug-title{font-size:13px;font-weight:600;color:var(--white);margin-bottom:3px}
.sug-body{font-size:11.5px;color:var(--gray);line-height:1.4}
.fixed-input{
  position:fixed;bottom:0;left:0;right:0;z-index:8000;
  background:rgba(5,5,5,.94);backdrop-filter:blur(24px);
  border-top:1px solid var(--border2);
  padding:14px 24px 20px;
}
.input-inner{max-width:820px;margin:0 auto;display:flex;align-items:center;gap:10px}
""")

loc     = get_location()
lat     = loc.get("lat") or 13.0827
lon     = loc.get("lon") or 80.2707

@st.cache_data(ttl=300, show_spinner=False)
def _weather(lat, lon): return get_weather(lat, lon)
weather = _weather(lat, lon)
city    = weather.get("city","Your Location")
temp    = weather.get("temperature_c","--")
top_navbar("assistant", f"{city}", str(temp))

if "messages" not in st.session_state:
    st.session_state.messages = []

SUGGESTIONS = [
    ("🌊", "Flood Risk Assessment",
     "What is the current flood risk in my area? What precautions should I take right now?",
     "Get personalized flood risk analysis"),
    ("🌀", "Cyclone Preparedness Guide",
     "How do I prepare my family for a cyclone? Give me a complete preparation checklist.",
     "Step-by-step cyclone preparation"),
    ("🩺", "Medical Emergency Protocol",
     "Someone is injured during a disaster. Walk me through first aid and emergency response.",
     "First aid & emergency medical help"),
    ("📡", "Live Disaster Alerts",
     f"Are there any active disaster warnings or alerts near {city} right now? What should I know?",
     "Check real-time alerts for your area"),
]

# ── Chat hero (only when no messages) ─────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
<div class="chat-hero">
  <div style="width:64px;height:64px;border-radius:20px;
    background:linear-gradient(135deg,#FFD54A,#D4AF37);
    display:flex;align-items:center;justify-content:center;
    font-size:30px;margin:0 auto 18px;
    box-shadow:0 0 40px rgba(255,213,74,.3)">🛡</div>
  <div style="font-size:26px;font-weight:900;letter-spacing:-.04em;color:var(--white);
    margin-bottom:8px">DisasterShield AI</div>
  <div style="font-size:14px;color:var(--gray);max-width:380px;margin:0 auto;line-height:1.6">
    Your intelligent emergency companion. Ask about disaster risks,
    preparedness, evacuation routes, or first aid.
  </div>
</div>""", unsafe_allow_html=True)

    st.markdown('<div class="suggestions">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    for i, (ico, title, prompt, sub) in enumerate(SUGGESTIONS):
        with (c1 if i % 2 == 0 else c2):
            if st.button(f"**{ico} {title}**\n\n{sub}",
                         key=f"sug_{i}", use_container_width=True):
                st.session_state.messages.append({"role":"user","content":prompt})
                with st.spinner(""):
                    response = get_response(prompt)
                st.session_state.messages.append({"role":"assistant","content":response})
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ── Render history ─────────────────────────────────────────────────────────────
st.markdown('<div class="chat-page">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    content = msg["content"]
    if isinstance(content, dict):
        content = content.get("response", content.get("text", str(content)))
    elif not isinstance(content, str):
        content = str(content)
    chat_bubble(msg["role"], content)
st.markdown('</div>', unsafe_allow_html=True)

# ── Fixed input bar ────────────────────────────────────────────────────────────
st.markdown("""
<div class="fixed-input">
  <div class="input-inner">
""", unsafe_allow_html=True)

col_in, col_clr = st.columns([10, 1])
with col_in:
    prompt = st.chat_input("Ask about disasters, emergency procedures, evacuation routes…")
with col_clr:
    if st.button("🗑", help="Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.markdown("</div></div>", unsafe_allow_html=True)

if prompt:
    st.session_state.messages.append({"role":"user","content":prompt})
    chat_bubble("user", prompt)
    chat_bubble("assistant","",is_typing=True)
    with st.spinner(""):
        response = get_response(prompt)
    st.session_state.messages.append({"role":"assistant","content":response})
    st.rerun()
