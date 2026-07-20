"""AI Assistant — DisasterShield AI · ChatGPT-style"""
import streamlit as st
import streamlit.components.v1 as components
from backend.graph.workflow import get_response
from frontend.design.premium_css import inject, top_navbar, chat_bubble
from backend.services.location_service import get_location
from backend.services.weather_service import get_weather


inject("""
/* ── Chat Page Container ──────────────────────────────────────────────── */
.chat-container {
  max-width: 780px;
  margin: 0 auto;
  padding-bottom: 120px;
}

/* ── Centered Floating Chat Input ───────────────────────────────────────── */
[data-testid="stChatInput"] {
  max-width: 780px !important;
  width: calc(100% - 48px) !important;
  margin: 0 auto !important;
  position: fixed !important;
  bottom: 24px !important;
  left: 50% !important;
  transform: translateX(-50%) !important;
  z-index: 9990 !important;
}
[data-testid="stChatInput"] > div {
  background: rgba(18, 20, 26, 0.95) !important;
  border: 1px solid rgba(255, 213, 74, 0.22) !important;
  border-radius: 16px !important;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.7), 0 0 0 1px rgba(255, 213, 74, 0.08) !important;
  backdrop-filter: blur(20px) !important;
}
[data-testid="stChatInput"] textarea {
  color: #F5F5F5 !important;
  font-family: 'Inter', system-ui, sans-serif !important;
  font-size: 14px !important;
}
[data-testid="stChatInput"] textarea::placeholder {
  color: #8B949E !important;
}
[data-testid="stChatInput"] button {
  color: #FFD54A !important;
}

/* ── Suggestions Grid ─────────────────────────────────────────────────── */
.suggestions-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin: 24px 0 36px;
}
""")

loc     = get_location()
lat     = loc.get("lat") or 13.0827
lon     = loc.get("lon") or 80.2707

@st.cache_data(ttl=300, show_spinner=False)
def _weather(lat, lon): return get_weather(lat, lon)
weather = _weather(lat, lon)
city    = weather.get("city", "Your Location")
temp    = weather.get("temperature_c", "--")

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

# ── Top Action Header (Clear Chat) ─────────────────────────────────────────────
if st.session_state.messages:
    col_t1, col_t2 = st.columns([6, 1])
    with col_t2:
        if st.button("🗑 Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

# ── Main Chat Area ────────────────────────────────────────────────────────────
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# ── Hero (only when no messages) ──────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
<div style="text-align:center;padding:36px 16px 20px">
  <div style="width:64px;height:64px;border-radius:20px;
    background:linear-gradient(135deg,#FFD54A,#D4AF37);
    display:flex;align-items:center;justify-content:center;
    font-size:32px;margin:0 auto 18px;
    box-shadow:0 0 40px rgba(255,213,74,.35)">🛡</div>
  <div style="font-size:28px;font-weight:900;letter-spacing:-.04em;color:#F5F5F5;margin-bottom:8px">
    DisasterShield AI
  </div>
  <div style="font-size:14px;color:#8B949E;max-width:420px;margin:0 auto;line-height:1.6">
    Your intelligent emergency companion. Ask about disaster risks,
    preparedness, evacuation routes, or first aid.
  </div>
</div>
""", unsafe_allow_html=True)

    # Suggestions
    c1, c2 = st.columns(2)
    for i, (ico, title, prompt_text, sub) in enumerate(SUGGESTIONS):
        with (c1 if i % 2 == 0 else c2):
            if st.button(f"**{ico} {title}**\n\n{sub}", key=f"sug_{i}", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": prompt_text})
                with st.spinner(""):
                    response = get_response(prompt_text)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()

# ── Render Message History ────────────────────────────────────────────────────
for msg in st.session_state.messages:
    content = msg["content"]
    if isinstance(content, dict):
        content = content.get("response", content.get("text", str(content)))
    elif not isinstance(content, str):
        content = str(content)
    chat_bubble(msg["role"], content)

st.markdown('</div>', unsafe_allow_html=True)

# ── Chat Input ────────────────────────────────────────────────────────────────
prompt = st.chat_input("Ask about disasters, emergency procedures, evacuation routes…")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    chat_bubble("user", prompt)
    chat_bubble("assistant", "", is_typing=True)
    with st.spinner(""):
        response = get_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
