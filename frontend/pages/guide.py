"""Offline Guide — DisasterShield AI"""
import streamlit as st
from frontend.design.premium_css import inject, top_navbar

inject("""
.guide-wrap { max-width: 760px; margin: 0 auto; padding: 16px 24px 60px; }
.step { display: flex; gap: 13px; align-items: flex-start; padding: 11px 0; border-bottom: 1px solid rgba(255,255,255,.04); }
.step:last-child { border-bottom: none; }
.step-num { width: 26px; height: 26px; border-radius: 50%; flex-shrink: 0; background: linear-gradient(135deg,#FFD54A,#D4AF37); color: #050505; font-size: 11.5px; font-weight: 800; display: flex; align-items: center; justify-content: center; margin-top: 1px; }
.step-body { font-size: 12.5px; color: #8B949E; line-height: 1.6; }
.step-body strong { color: #F5F5F5; font-weight: 600; }
.kit-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(110px, 1fr)); gap: 8px; padding-top: 4px; }
.kit-item { background: rgba(255,255,255,.03); border: 1px solid rgba(255,255,255,.06); border-radius: 11px; padding: 14px 10px; text-align: center; transition: all .15s; }
.kit-item:hover { border-color: rgba(255,213,74,.2); background: rgba(255,213,74,.04); }
.kit-ico { font-size: 26px; margin-bottom: 6px; }
.kit-lbl { font-size: 11px; color: #8B949E; font-weight: 500; line-height: 1.3; }
.warning { padding: 10px 14px; background: rgba(255,77,79,.06); border: 1px solid rgba(255,77,79,.18); border-radius: 9px; font-size: 12px; color: #FCA5A5; line-height: 1.5; margin-bottom: 12px; }

/* Style Streamlit expanders as premium accordions */
div[data-testid="stExpander"] {
  background: var(--glass) !important;
  border: 1px solid var(--border2) !important;
  border-radius: var(--r) !important;
  margin-bottom: 8px !important;
  overflow: hidden !important;
  box-shadow: var(--shadow) !important;
}
div[data-testid="stExpander"] details {
  border: none !important;
}
div[data-testid="stExpander"] summary {
  background: rgba(18, 20, 26, 0.78) !important;
  color: var(--white) !important;
  padding: 16px 18px !important;
  font-weight: 700 !important;
  font-size: 13.5px !important;
}
div[data-testid="stExpander"] summary:hover {
  background: rgba(255, 213, 74, 0.04) !important;
  color: var(--white) !important;
}
div[data-testid="stExpander"] [data-testid="stVerticalBlock"] {
  padding: 18px !important;
}

/* Segmented control style overrides */
div[data-testid="stSegmentedControl"] button {
  background: rgba(18, 20, 26, 0.78) !important;
  border: 1px solid rgba(255, 255, 255, 0.07) !important;
  color: #8B949E !important;
  font-weight: 600 !important;
}
div[data-testid="stSegmentedControl"] button[aria-checked="true"] {
  background: rgba(255, 213, 74, 0.08) !important;
  border-color: rgba(255, 213, 74, 0.25) !important;
  color: #FFD54A !important;
}
""")

top_navbar("resources")

st.markdown("""
<div class="guide-wrap">
  <div style="margin-bottom:28px">
    <div style="font-size:10px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
      color:var(--gold);margin-bottom:10px">📖 OFFLINE EMERGENCY GUIDE</div>
    <div style="font-size:30px;font-weight:900;letter-spacing:-.04em;color:var(--white);
      margin-bottom:6px">Emergency Preparedness Library</div>
    <div style="font-size:13px;color:var(--gray);max-width:520px;line-height:1.6">
      Complete offline-ready emergency procedures. Save this page — works without internet.
      All guides authored with WHO and NDMA protocols.
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# Wrap settings inside a wrapper div to match padding
st.markdown('<div class="guide-wrap" style="padding-top:0; padding-bottom:0">', unsafe_allow_html=True)

category = st.segmented_control(
    "Guide Category",
    options=["All Guides", "🩺 Medical", "⛈ Disasters", "🎒 Preparation"],
    default="All Guides",
    key="guide_category",
    label_visibility="collapsed"
)

st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)

# 1. CPR
if category in ["All Guides", "🩺 Medical"]:
    with st.expander("❤️ CPR — Cardiopulmonary Resuscitation", expanded=(category == "🩺 Medical")):
        st.markdown("""
        <div class="warning">⚠ <strong>Call emergency services (108) first.</strong> CPR is a bridge — get professional help on the way.</div>
        <div class="step"><div class="step-num">1</div><div class="step-body"><strong>Check responsiveness:</strong> Tap shoulders firmly, shout "Are you OK?" If unresponsive, shout for help and call 108.</div></div>
        <div class="step"><div class="step-num">2</div><div class="step-body"><strong>Open airway:</strong> Tilt head back, lift chin to open the airway. Look, listen and feel for normal breathing (no more than 10 seconds).</div></div>
        <div class="step"><div class="step-num">3</div><div class="step-body"><strong>30 chest compressions:</strong> Place heel of hand on center of chest. Push down 5–6 cm at 100–120 beats/min ("Stayin' Alive" rhythm). Allow full chest recoil.</div></div>
        <div class="step"><div class="step-num">4</div><div class="step-body"><strong>2 rescue breaths:</strong> Pinch nose, seal mouth, give 1-second breath. Watch for chest rise. If untrained — compression-only CPR is still effective.</div></div>
        <div class="step"><div class="step-num">5</div><div class="step-body"><strong>Continue 30:2 cycle</strong> until person breathes normally, AED arrives, or professional help takes over. Don't stop.</div></div>
        """, unsafe_allow_html=True)

# 2. First Aid Essentials
if category in ["All Guides", "🩺 Medical"]:
    with st.expander("🩹 First Aid Essentials", expanded=False):
        st.markdown("""
        <div class="step"><div class="step-num">1</div><div class="step-body"><strong>Bleeding:</strong> Apply firm pressure with clean cloth. Elevate above heart. Don't remove soaked cloth — add more on top. Tourniquet only if life-threatening.</div></div>
        <div class="step"><div class="step-num">2</div><div class="step-body"><strong>Burns:</strong> Cool with running water for 10–20 min. Do NOT use ice, butter, or toothpaste. Cover loosely with sterile bandage. Seek help for large burns.</div></div>
        <div class="step"><div class="step-num">3</div><div class="step-body"><strong>Fractures:</strong> Immobilize with splint. Don't try to realign. Apply ice pack wrapped in cloth. Elevate if possible.</div></div>
        <div class="step"><div class="step-num">4</div><div class="step-body"><strong>Shock:</strong> Lay flat, elevate legs 12 inches (unless head/spine injury suspected). Keep warm. No food or water. Monitor breathing constantly.</div></div>
        <div class="step"><div class="step-num">5</div><div class="step-body"><strong>Choking (adult):</strong> Give 5 back blows between shoulder blades. Then 5 abdominal thrusts (Heimlich). Alternate until object dislodged or person becomes unconscious.</div></div>
        """, unsafe_allow_html=True)

# 3. Flood
if category in ["All Guides", "⛈ Disasters"]:
    with st.expander("🌊 Flood Response Protocol", expanded=(category == "⛈ Disasters")):
        st.markdown("""
        <div class="step"><div class="step-num">1</div><div class="step-body"><strong>Move immediately to higher ground.</strong> Don't wait for official orders if water is rising. Every minute matters.</div></div>
        <div class="step"><div class="step-num">2</div><div class="step-body"><strong>Never walk in floodwater:</strong> 15 cm of fast-moving water can knock you down. 30 cm can carry a car. Stay away.</div></div>
        <div class="step"><div class="step-num">3</div><div class="step-body"><strong>Turn off utilities</strong> at the main switch/valve if instructed and safe. Do not touch electrical equipment if you or it is wet.</div></div>
        <div class="step"><div class="step-num">4</div><div class="step-body"><strong>Fill water containers</strong> before power goes out — clean water will be scarce. Secure important documents in waterproof bags.</div></div>
        <div class="step"><div class="step-num">5</div><div class="step-body"><strong>After flood:</strong> Document damage with photos. Wear gloves and boots during cleanup. Boil or filter all water. Discard any food that touched floodwater.</div></div>
        """, unsafe_allow_html=True)

# 4. Earthquake
if category in ["All Guides", "⛈ Disasters"]:
    with st.expander("🏚 Earthquake Response", expanded=False):
        st.markdown("""
        <div class="step"><div class="step-num">1</div><div class="step-body"><strong>DROP, COVER, HOLD ON:</strong> Get under a sturdy table or desk, or against an interior wall. Cover your neck and head with your arms.</div></div>
        <div class="step"><div class="step-num">2</div><div class="step-body"><strong>Stay inside:</strong> Don't run outside — most injuries happen as people try to leave buildings. Stay until shaking stops completely.</div></div>
        <div class="step"><div class="step-num">3</div><div class="step-body"><strong>Check for hazards:</strong> After shaking stops, check for gas leaks (smell), electrical damage, structural damage. Expect aftershocks.</div></div>
        <div class="step"><div class="step-num">4</div><div class="step-body"><strong>Gas leak:</strong> If you smell gas, open windows and leave immediately without switching lights. Call gas company from outside.</div></div>
        <div class="step"><div class="step-num">5</div><div class="step-body"><strong>Evacuate only if ordered</strong> or if building is clearly damaged. Go to designated assembly point. Stay off roads to allow emergency access.</div></div>
        """, unsafe_allow_html=True)

# 5. Cyclone
if category in ["All Guides", "⛈ Disasters"]:
    with st.expander("🌀 Cyclone & Hurricane Protocol", expanded=False):
        st.markdown("""
        <div class="step"><div class="step-num">1</div><div class="step-body"><strong>Prepare 72 hours before:</strong> Board windows, secure loose objects, fill water, charge devices, stock emergency supplies for 3+ days.</div></div>
        <div class="step"><div class="step-num">2</div><div class="step-body"><strong>During cyclone:</strong> Stay in the strongest interior room, lowest floor. Keep away from all windows and exterior doors.</div></div>
        <div class="step"><div class="step-num">3</div><div class="step-body"><strong>⚠ Eye of storm:</strong> DO NOT go outside during the calm. The other side of the eyewall is equally dangerous and arrives suddenly.</div></div>
        <div class="step"><div class="step-num">4</div><div class="step-body"><strong>After:</strong> Wait for official all-clear. Watch for downed power lines, broken gas lines, structural damage. Report any injuries.</div></div>
        """, unsafe_allow_html=True)

# 6. Emergency Kit
if category in ["All Guides", "🎒 Preparation"]:
    with st.expander("🎒 Emergency Go-Bag Checklist", expanded=(category == "🎒 Preparation")):
        st.markdown("""
        <div class="kit-grid">
          <div class="kit-item"><div class="kit-ico">💧</div><div class="kit-lbl">Water<br>(3+ days)</div></div>
          <div class="kit-item"><div class="kit-ico">🥫</div><div class="kit-lbl">Non-perishable Food</div></div>
          <div class="kit-item"><div class="kit-ico">🔦</div><div class="kit-lbl">Flashlight + Batteries</div></div>
          <div class="kit-item"><div class="kit-ico">🩹</div><div class="kit-lbl">First Aid Kit</div></div>
          <div class="kit-item"><div class="kit-ico">📻</div><div class="kit-lbl">Battery Radio</div></div>
          <div class="kit-item"><div class="kit-ico">🔋</div><div class="kit-lbl">Power Bank</div></div>
          <div class="kit-item"><div class="kit-ico">🗺</div><div class="kit-lbl">Physical Map</div></div>
          <div class="kit-item"><div class="kit-ico">💊</div><div class="kit-lbl">Medications</div></div>
          <div class="kit-item"><div class="kit-ico">📄</div><div class="kit-lbl">Documents (copy)</div></div>
          <div class="kit-item"><div class="kit-ico">💵</div><div class="kit-lbl">Cash (small bills)</div></div>
          <div class="kit-item"><div class="kit-ico">🌡</div><div class="kit-lbl">Blanket / Mylar</div></div>
          <div class="kit-item"><div class="kit-ico">😷</div><div class="kit-lbl">N95 Masks (x10)</div></div>
          <div class="kit-item"><div class="kit-ico">🔧</div><div class="kit-lbl">Multi-tool</div></div>
          <div class="kit-item"><div class="kit-ico">🕯</div><div class="kit-lbl">Candles / Lighter</div></div>
          <div class="kit-item"><div class="kit-ico">📞</div><div class="kit-lbl">Contact List (printed)</div></div>
          <div class="kit-item"><div class="kit-ico">👟</div><div class="kit-lbl">Sturdy Shoes</div></div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
