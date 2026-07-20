"""DisasterShield AI — Enterprise Design System v4.0"""
import streamlit as st
import streamlit.components.v1 as components

# ─────────────────────────────────────────────────────────────────────────────
# BASE CSS — injected on every page
# ─────────────────────────────────────────────────────────────────────────────
_BASE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

:root {
  --bg:      #050505;
  --bg2:     #0B0D10;
  --bg3:     #12141A;
  --glass:   rgba(18,20,26,.78);
  --gold:    #FFD54A;
  --gold2:   #D4AF37;
  --gold-lo: rgba(255,213,74,.08);
  --gold-md: rgba(255,213,74,.14);
  --gold-hi: rgba(255,213,74,.28);
  --white:   #F5F5F5;
  --gray:    #8B949E;
  --gray2:   #374151;
  --danger:  #FF4D4F;
  --success: #00C853;
  --warn:    #FFB300;
  --purple:  #8B5CF6;
  --blue:    #3B82F6;
  --border:  rgba(255,213,74,.09);
  --border2: rgba(255,255,255,.055);
  --shadow:  0 8px 40px rgba(0,0,0,.6);
  --r:       14px;
  --r-sm:    9px;
  --r-lg:    20px;
  --r-xl:    28px;
  --nav-h:   62px;
  --font:    'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp, [class*="css"] {
  font-family: var(--font) !important;
  background: var(--bg) !important;
  color: var(--white) !important;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
}

/* ── Hide all Streamlit chrome ───────────────────────────────────────────── */
#MainMenu, footer, header, .stDeployButton,
[data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"], [data-testid="stSidebarNav"],
[data-testid="stSidebarNavItems"], [data-testid="stSidebarNavSeparator"],
[data-testid="stSidebarHeader"], [data-testid="stLogoSpacer"],
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"] { display: none !important; }

/* ── Layout ──────────────────────────────────────────────────────────────── */
.main .block-container,
[data-testid="stMainBlockContainer"] {
  padding: var(--nav-h) 0 0 0 !important;
  max-width: 100% !important;
}
[data-testid="column"] { padding: 0 6px !important; }

/* ── Scrollbar ───────────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 3px; height: 3px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,213,74,.2); border-radius: 99px; }

/* ── Streamlit buttons ───────────────────────────────────────────────────── */
.stButton > button {
  background: var(--gold-lo) !important;
  border: 1px solid var(--border) !important;
  color: var(--white) !important;
  border-radius: var(--r-sm) !important;
  font-family: var(--font) !important;
  font-weight: 500 !important;
  transition: all .18s !important;
}
.stButton > button:hover {
  background: var(--gold-md) !important;
  border-color: var(--gold-hi) !important;
  transform: translateY(-1px) !important;
}

/* ── Chat input ──────────────────────────────────────────────────────────── */
[data-testid="stChatInput"] > div {
  background: var(--bg3) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--r-lg) !important;
}
[data-testid="stChatInput"] > div:focus-within {
  border-color: rgba(255,213,74,.35) !important;
  box-shadow: 0 0 0 3px rgba(255,213,74,.07) !important;
}
[data-testid="stChatMessage"] {
  background: transparent !important;
  border: none !important;
  padding: 0 !important;
}

/* ── Tabs ────────────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
  background: transparent !important;
  border-bottom: 1px solid var(--border2) !important;
  padding: 0 36px !important;
  gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  color: var(--gray) !important;
  border: none !important;
  border-bottom: 2px solid transparent !important;
  border-radius: 0 !important;
  padding: 12px 20px !important;
  font-size: 13px !important;
  font-weight: 500 !important;
  transition: all .15s !important;
}
.stTabs [data-baseweb="tab"]:hover { color: var(--white) !important; }
.stTabs [aria-selected="true"] {
  color: var(--gold) !important;
  border-bottom-color: var(--gold) !important;
}
.stTabs [data-baseweb="tab-panel"] {
  padding: 0 !important;
  background: transparent !important;
}

/* ── Spinner ─────────────────────────────────────────────────────────────── */
.stSpinner > div {
  border-top-color: var(--gold) !important;
}

/* ── Select / Inputs ─────────────────────────────────────────────────────── */
.stTextInput input, .stSelectbox select, .stTextArea textarea {
  background: var(--bg3) !important;
  border: 1px solid var(--border2) !important;
  color: var(--white) !important;
  border-radius: var(--r-sm) !important;
  font-family: var(--font) !important;
}

/* ── Animations ──────────────────────────────────────────────────────────── */
@keyframes pulse  { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.35;transform:scale(1.6)} }
@keyframes blink  { 0%,100%{opacity:1} 50%{opacity:.2} }
@keyframes fadeUp { from{opacity:0;transform:translateY(12px)} to{opacity:1;transform:translateY(0)} }
@keyframes slideR { from{opacity:0;transform:translateX(20px)} to{opacity:1;transform:translateX(0)} }
@keyframes spin   { to{transform:rotate(360deg)} }
@keyframes glow   { 0%,100%{box-shadow:0 0 20px rgba(255,213,74,.2)} 50%{box-shadow:0 0 40px rgba(255,213,74,.5)} }
@keyframes float  { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-8px)} }

/* ── Page top padding (below fixed nav) ──────────────────────────────────── */
.page-body { padding-top: calc(var(--nav-h) + 4px); }

/* ── Collapse invisible layout elements (hidden page links, 0-height JS
     iframes) so they don't leave a big empty gap under the fixed navbar ── */
div[data-testid="stElementContainer"]:has([data-testid="stPageLink"]) { display: none !important; }
div[data-testid="stElementContainer"]:has(iframe[height="0"]) { display: none !important; }
div[data-testid="stElementContainer"]:has(> div > [data-testid="stMarkdownContainer"] > style:only-child) { display: none !important; }

/* Zero-height elements (style-only markdown, the fixed navbar block) still
   each reserve a flex-gap slot in the top-level vertical block — remove it.
   Nested blocks (columns etc.) keep the default gap. */
[data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] {
  gap: 0 !important;
}

/* ── Custom Metric & Resource Card hover styles ── */
.ds-metric-card {
  transition: transform .2s, border-color .2s !important;
}
.ds-metric-card:hover {
  transform: translateY(-3px) !important;
  border-color: var(--border) !important;
}
.ds-res-card {
  transition: all .18s !important;
}
.ds-res-card:hover {
  transform: translateY(-2px) !important;
  border-color: var(--border) !important;
}
.ds-res-card-nav-btn {
  transition: background .15s !important;
}
.ds-res-card-nav-btn:hover {
  background: var(--gold-md) !important;
}
</style>
"""

# ─────────────────────────────────────────────────────────────────────────────
def inject(extra=""):
    st.markdown(_BASE + (f"<style>{extra}</style>" if extra else ""), unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TOP NAVIGATION BAR
# ─────────────────────────────────────────────────────────────────────────────
def top_navbar(active="dashboard", city_name="", temp=""):
    page_map = {
        "dashboard":   ("./",           "Dashboard"),
        "risk":        ("risk",         "Risk Monitor"),
        "assistant":   ("assistant",    "AI Assistant"),
        "resources":   ("resources",    "Resources"),
        "emergency":   ("emergency",    "Emergency"),
        "analytics":   ("analytics",    "Analytics"),
        "settings":    ("settings",     "Settings"),
    }
    nav_links = ""
    mm_links = ""
    for key, (url, label) in page_map.items():
        nav_slug = "" if key == "dashboard" else key
        # data-navigate drives SPA routing via JS event delegation (no onclick)
        is_active = " active" if active == key else ""
        if key == "emergency":
            nav_links += (
                f'<a href="{url}" data-navigate="{nav_slug}" class="nav-link nav-emergency'
                f'{is_active}">{label}</a>'
            )
            mm_links += (
                f'<a href="{url}" data-navigate="{nav_slug}" class="mm-link mm-emergency'
                f'{is_active}">🆘 {label}</a>'
            )
        else:
            nav_links += (
                f'<a href="{url}" data-navigate="{nav_slug}" class="nav-link'
                f'{is_active}">{label}</a>'
            )
            mm_links += (
                f'<a href="{url}" data-navigate="{nav_slug}" class="mm-link'
                f'{is_active}">{label}</a>'
            )

    loc_pill = ""
    if city_name:
        short = city_name.split(",")[0][:18]
        t_str = f" · {temp}°C" if temp else ""
        loc_pill = f'<div class="nav-loc">📍 {short}{t_str}</div>'

    _nav_html = f"""
<!-- ═══════════════════════ DISASTERSHIELD NAVBAR ═══════════════════════ -->
<style>
/* ── Nav shell ─────────────────────────────────────────────────────────── */
#ds-nav {{
  position: fixed; top: 0; left: 0; right: 0; z-index: 9999;
  height: var(--nav-h);
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 28px;
  background: rgba(5,5,5,.88);
  backdrop-filter: blur(28px) saturate(200%);
  -webkit-backdrop-filter: blur(28px) saturate(200%);
  border-bottom: 1px solid var(--border);
  box-shadow: 0 1px 0 rgba(255,213,74,.05), 0 8px 40px rgba(0,0,0,.5);
  transition: height .25s, background .25s;
}}
#ds-nav.scrolled {{
  height: 52px;
  background: rgba(5,5,5,.96);
}}

/* ── Logo ─────────────────────────────────────────────────────────────── */
.nav-logo {{
  display: flex; align-items: center; gap: 10px; flex-shrink: 0; cursor: pointer;
  text-decoration: none;
}}
.nav-logo-icon {{
  width: 36px; height: 36px; position: relative;
  background: linear-gradient(145deg, #14161C 0%, #0B0D10 100%);
  border: 1px solid rgba(255,213,74,.35);
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 0 18px rgba(255,213,74,.22), inset 0 1px 0 rgba(255,213,74,.12);
}}
.nav-logo-icon svg {{ width: 27px; height: 27px; }}
.nav-logo-text {{
  font-size: 15px; font-weight: 800; letter-spacing: -.03em;
  color: var(--white); line-height: 1;
}}
.nav-logo-sub {{
  font-size: 9px; font-weight: 500; color: var(--gray); letter-spacing: .06em;
  text-transform: uppercase; line-height: 1; margin-top: 2px;
}}

/* ── Nav links ─────────────────────────────────────────────────────────── */
.nav-links {{
  display: flex; align-items: center; gap: 2px;
}}
.nav-link {{
  font-size: 13px; font-weight: 500; color: var(--gray);
  padding: 6px 13px; border-radius: 8px;
  text-decoration: none; white-space: nowrap;
  transition: color .15s, background .15s;
  position: relative;
}}
.nav-link:hover {{ color: var(--white); background: rgba(255,255,255,.04); }}
.nav-link.active {{ color: var(--gold); font-weight: 600; }}
.nav-link.active::after {{
  content: ''; position: absolute; bottom: -1px; left: 13px; right: 13px;
  height: 2px; border-radius: 99px;
  background: linear-gradient(90deg, var(--gold), transparent);
}}
.nav-emergency {{
  color: #FF4D4F !important; background: rgba(255,77,79,.08) !important;
  border: 1px solid rgba(255,77,79,.18) !important;
  border-radius: 8px !important; font-weight: 600 !important;
}}
.nav-emergency:hover {{
  background: rgba(255,77,79,.14) !important;
  color: #FF4D4F !important;
}}
.nav-emergency.active {{
  color: #FF4D4F !important;
}}
.nav-emergency.active::after {{ background: #FF4D4F !important; }}

/* ── Right actions ─────────────────────────────────────────────────────── */
.nav-right {{
  display: flex; align-items: center; gap: 8px; flex-shrink: 0;
}}
.nav-btn {{
  width: 36px; height: 36px; border-radius: 10px;
  background: rgba(255,255,255,.04); border: 1px solid var(--border2);
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; transition: all .15s; position: relative;
  color: var(--gray); font-size: 16px;
}}
.nav-btn:hover {{ background: var(--gold-lo); border-color: var(--border); color: var(--white); }}
.nav-badge {{
  position: absolute; top: 5px; right: 5px; width: 8px; height: 8px;
  border-radius: 50%; background: var(--danger); border: 1.5px solid var(--bg);
  animation: pulse 2.5s ease infinite;
}}
.nav-loc {{
  font-size: 12px; font-weight: 500; color: var(--gray);
  padding: 6px 12px; border-radius: 99px;
  background: rgba(255,255,255,.04); border: 1px solid var(--border2);
  white-space: nowrap; max-width: 180px; overflow: hidden; text-overflow: ellipsis;
}}
.nav-avatar {{
  width: 34px; height: 34px; border-radius: 50%;
  background: linear-gradient(135deg, #374151, #1F2937);
  border: 2px solid var(--border);
  display: flex; align-items: center; justify-content: center;
  font-size: 14px; cursor: pointer; transition: border-color .15s;
  flex-shrink: 0; position: relative;
}}
.nav-avatar:hover {{ border-color: var(--gold-hi); }}

/* ── Notification Panel ─────────────────────────────────────────────────── */
#notif-panel {{
  position: fixed; top: 0; right: -420px; bottom: 0; width: 400px;
  z-index: 10000;
  background: rgba(11,13,16,.97);
  backdrop-filter: blur(32px) saturate(200%);
  border-left: 1px solid var(--border2);
  box-shadow: -20px 0 60px rgba(0,0,0,.6);
  transition: right .32s cubic-bezier(.4,0,.2,1);
  display: flex; flex-direction: column; overflow: hidden;
}}
#notif-panel.open {{ right: 0; }}
.np-head {{
  display: flex; align-items: center; justify-content: space-between;
  padding: 20px 20px 16px;
  border-bottom: 1px solid var(--border2);
  flex-shrink: 0;
}}
.np-title {{ font-size: 15px; font-weight: 700; color: var(--white); }}
.np-actions {{ display: flex; gap: 6px; }}
.np-action {{
  font-size: 11px; font-weight: 600; color: var(--gray);
  padding: 4px 10px; border-radius: 6px;
  background: rgba(255,255,255,.04); border: 1px solid var(--border2);
  cursor: pointer; transition: all .15s;
}}
.np-action:hover {{ color: var(--white); background: rgba(255,255,255,.08); }}
.np-tabs {{
  display: flex; border-bottom: 1px solid var(--border2);
  padding: 0 20px; flex-shrink: 0;
}}
.np-tab {{
  font-size: 12px; font-weight: 500; color: var(--gray);
  padding: 10px 14px; cursor: pointer;
  border-bottom: 2px solid transparent;
  transition: all .15s; white-space: nowrap;
}}
.np-tab.active {{ color: var(--gold); border-bottom-color: var(--gold); font-weight: 600; }}
.np-body {{ flex: 1; overflow-y: auto; padding: 12px; }}
.notif-item {{
  display: flex; gap: 12px; padding: 12px;
  border-radius: var(--r-sm); margin-bottom: 6px;
  background: rgba(255,255,255,.03); border: 1px solid transparent;
  transition: all .18s; cursor: pointer; position: relative;
  animation: fadeUp .25s ease both;
}}
.notif-item:hover {{ background: rgba(255,255,255,.05); border-color: var(--border2); }}
.notif-item.unread {{ border-color: rgba(255,213,74,.1); }}
.notif-item.unread::before {{
  content: ''; position: absolute; left: 0; top: 12px; bottom: 12px;
  width: 2px; border-radius: 99px; background: var(--gold);
}}
.notif-icon {{
  width: 36px; height: 36px; border-radius: 10px; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center; font-size: 17px;
}}
.notif-content {{ flex: 1; min-width: 0; }}
.notif-title {{
  font-size: 12.5px; font-weight: 600; color: var(--white);
  line-height: 1.3; margin-bottom: 3px;
}}
.notif-body {{ font-size: 11.5px; color: var(--gray); line-height: 1.4; }}
.notif-meta {{
  display: flex; align-items: center; gap: 6px; margin-top: 5px;
}}
.notif-time {{ font-size: 10.5px; color: var(--gray2); }}
.notif-sev {{
  font-size: 9.5px; font-weight: 700; padding: 1px 7px;
  border-radius: 99px; text-transform: uppercase; letter-spacing: .06em;
}}
.np-empty {{
  text-align: center; padding: 60px 20px;
  color: var(--gray); font-size: 13px;
}}
.np-empty-icon {{ font-size: 36px; margin-bottom: 10px; opacity: .4; }}
.np-permission-banner {{
  margin: 12px; padding: 12px 14px;
  background: rgba(255,213,74,.06); border: 1px solid rgba(255,213,74,.18);
  border-radius: var(--r-sm);
  display: flex; align-items: center; gap: 10px;
}}
.np-perm-text {{ font-size: 12px; color: var(--gray); flex: 1; line-height: 1.4; }}
.np-perm-btn {{
  font-size: 11px; font-weight: 600; color: var(--bg); padding: 6px 12px;
  background: var(--gold); border: none; border-radius: 6px; cursor: pointer;
  white-space: nowrap; transition: opacity .15s;
}}
.np-perm-btn:hover {{ opacity: .85; }}

/* ── Profile Dropdown ───────────────────────────────────────────────────── */
#profile-menu {{
  position: fixed; top: calc(var(--nav-h) + 6px); right: 28px;
  width: 240px; z-index: 10001;
  background: rgba(11,13,16,.97);
  backdrop-filter: blur(28px);
  border: 1px solid var(--border2);
  border-radius: var(--r-lg); overflow: hidden;
  box-shadow: 0 20px 60px rgba(0,0,0,.6), 0 0 0 1px rgba(255,213,74,.05);
  opacity: 0; transform: scale(.96) translateY(-4px);
  pointer-events: none;
  transition: all .2s cubic-bezier(.4,0,.2,1);
}}
#profile-menu.open {{
  opacity: 1; transform: scale(1) translateY(0); pointer-events: all;
}}
.pm-head {{
  padding: 16px 16px 12px;
  border-bottom: 1px solid var(--border2);
}}
.pm-name {{ font-size: 13.5px; font-weight: 700; color: var(--white); }}
.pm-email {{ font-size: 11px; color: var(--gray); margin-top: 2px; }}
.pm-body {{ padding: 6px; }}
.pm-item {{
  display: flex; align-items: center; gap: 10px; padding: 9px 10px;
  border-radius: 8px; cursor: pointer; transition: background .14s;
  text-decoration: none; color: var(--gray); font-size: 13px;
}}
.pm-item:hover {{ background: rgba(255,255,255,.05); color: var(--white); }}
.pm-item-ico {{ font-size: 16px; width: 20px; text-align: center; flex-shrink: 0; }}
.pm-sep {{ height: 1px; background: var(--border2); margin: 6px 0; }}
.pm-item.danger {{ color: #FF4D4F; }}
.pm-item.danger:hover {{ background: rgba(255,77,79,.08); color: #FF4D4F; }}

/* ── Critical Alert Dialog ──────────────────────────────────────────────── */
#critical-overlay {{
  position: fixed; inset: 0; z-index: 20000;
  background: rgba(0,0,0,.8); backdrop-filter: blur(8px);
  display: none; align-items: center; justify-content: center;
}}
#critical-overlay.show {{ display: flex; }}
.critical-card {{
  width: 440px; background: var(--bg2);
  border: 1px solid rgba(255,77,79,.4); border-radius: var(--r-xl);
  padding: 32px; box-shadow: 0 0 60px rgba(255,77,79,.2);
  text-align: center; animation: fadeUp .3s ease;
}}
.critical-pulse {{
  width: 80px; height: 80px; border-radius: 50%;
  background: rgba(255,77,79,.12); border: 2px solid rgba(255,77,79,.35);
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 20px; font-size: 36px;
  animation: glow 1.5s ease infinite;
}}
.critical-title {{ font-size: 22px; font-weight: 800; color: #FF4D4F; margin-bottom: 8px; }}
.critical-body {{ font-size: 14px; color: var(--gray); line-height: 1.6; margin-bottom: 24px; }}
.critical-btns {{ display: flex; gap: 10px; justify-content: center; }}
.critical-btn {{
  padding: 11px 28px; border-radius: 10px; font-size: 13px; font-weight: 600;
  cursor: pointer; border: none; font-family: var(--font);
  transition: all .15s;
}}
.critical-btn.primary {{
  background: #FF4D4F; color: #fff;
  box-shadow: 0 0 20px rgba(255,77,79,.35);
}}
.critical-btn.primary:hover {{ background: #FF6B6B; }}
.critical-btn.secondary {{
  background: rgba(255,255,255,.06); color: var(--gray);
  border: 1px solid var(--border2);
}}
.critical-btn.secondary:hover {{ color: var(--white); }}

/* ── Backdrop ───────────────────────────────────────────────────────────── */
#ds-backdrop {{
  position: fixed; inset: 0; z-index: 9998;
  background: rgba(0,0,0,.4); backdrop-filter: blur(2px);
  opacity: 0; pointer-events: none; transition: opacity .25s;
}}
#ds-backdrop.show {{ opacity: 1; pointer-events: all; }}

/* ── Mobile menu ────────────────────────────────────────────────────────── */
#ds-hamburger {{ display: none; }}
#ds-mobile-menu {{
  position: fixed; top: var(--nav-h); left: 0; right: 0; z-index: 9999;
  background: rgba(5,5,5,.97);
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  border-bottom: 1px solid var(--border2);
  box-shadow: 0 20px 40px rgba(0,0,0,.6);
  display: flex; flex-direction: column; gap: 3px;
  padding: 10px 14px 16px;
  opacity: 0; transform: translateY(-10px);
  pointer-events: none; transition: all .22s cubic-bezier(.4,0,.2,1);
}}
#ds-mobile-menu.open {{ opacity: 1; transform: translateY(0); pointer-events: all; }}
#ds-mobile-menu .mm-link {{
  padding: 13px 14px; border-radius: 10px;
  color: var(--gray) !important; font-size: 14.5px; font-weight: 600;
  text-decoration: none !important; transition: all .15s;
}}
#ds-mobile-menu .mm-link:hover {{ color: var(--white) !important; background: rgba(255,255,255,.05); }}
#ds-mobile-menu .mm-link.active {{ color: var(--gold) !important; background: rgba(255,213,74,.07); }}
#ds-mobile-menu .mm-emergency {{
  color: #FF4D4F !important; background: rgba(255,77,79,.08) !important;
  border: 1px solid rgba(255,77,79,.2);
}}
#ds-mobile-menu .mm-emergency.active {{ background: rgba(255,77,79,.14) !important; }}

/* ── Responsive / Mobile ────────────────────────────────────────────────── */
@media (max-width: 960px) {{
  #ds-nav {{ padding: 0 14px; }}
  .nav-links {{ display: none; }}
  .nav-loc {{ display: none; }}
  #ds-hamburger {{ display: flex; }}
  .nav-logo-text {{ font-size: 14px; }}
  #notif-panel {{ width: 100vw; right: -100vw; }}
  #profile-menu {{ right: 10px; left: 10px; width: auto; }}
  #ds-search-modal {{ padding: 24px 10px 0; }}
  .ds-search-box {{ max-width: 100%; }}
  .critical-card {{ width: calc(100vw - 32px); padding: 24px 18px; }}
}}
@media (max-width: 480px) {{
  .nav-right {{ gap: 6px; }}
  .nav-btn, .nav-avatar {{ width: 34px; height: 34px; }}
  .nav-logo-icon {{ width: 32px; height: 32px; }}
  .nav-logo-icon svg {{ width: 24px; height: 24px; }}
}}
</style>


<div id="ds-nav">

  <a href="/" data-navigate="" class="nav-logo">
    <div class="nav-logo-icon">
      <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="dslg-gold" x1="8" y1="4" x2="40" y2="44" gradientUnits="userSpaceOnUse">
            <stop stop-color="#FFD54A"/><stop offset="1" stop-color="#D4AF37"/>
          </linearGradient>
        </defs>
        <!-- AI circuit traces -->
        <path d="M8 12 L4 9" stroke="url(#dslg-gold)" stroke-width="1.2" stroke-linecap="round" opacity=".7"/>
        <circle cx="3.2" cy="8.4" r="1.4" fill="#FFD54A"/>
        <path d="M40 12 L44 9" stroke="url(#dslg-gold)" stroke-width="1.2" stroke-linecap="round" opacity=".7"/>
        <circle cx="44.8" cy="8.4" r="1.4" fill="#FFD54A"/>
        <path d="M6 26 L2 26" stroke="url(#dslg-gold)" stroke-width="1.2" stroke-linecap="round" opacity=".5"/>
        <circle cx="1.8" cy="26" r="1.2" fill="#D4AF37"/>
        <path d="M42 26 L46 26" stroke="url(#dslg-gold)" stroke-width="1.2" stroke-linecap="round" opacity=".5"/>
        <circle cx="46.2" cy="26" r="1.2" fill="#D4AF37"/>
        <path d="M24 45 L24 47" stroke="url(#dslg-gold)" stroke-width="1.2" stroke-linecap="round" opacity=".6"/>
        <!-- Shield -->
        <path d="M24 3.5 L7.5 10.2 V22 C7.5 33.3 14.6 42 24 45 C33.4 42 40.5 33.3 40.5 22 V10.2 Z"
              fill="rgba(255,213,74,.07)" stroke="url(#dslg-gold)" stroke-width="2.2" stroke-linejoin="round"/>
        <!-- Globe -->
        <circle cx="24" cy="19.5" r="8.6" stroke="url(#dslg-gold)" stroke-width="1.3"/>
        <ellipse cx="24" cy="19.5" rx="3.8" ry="8.6" stroke="url(#dslg-gold)" stroke-width="1" opacity=".8"/>
        <path d="M16.4 16.4 H31.6 M16.4 22.6 H31.6" stroke="url(#dslg-gold)" stroke-width="1" opacity=".8"/>
        <!-- Location pin -->
        <path d="M24 13.6 c-2.6 0 -4.6 2 -4.6 4.5 c0 3.3 4.6 8 4.6 8 s4.6 -4.7 4.6 -8 c0 -2.5 -2 -4.5 -4.6 -4.5 Z"
              fill="#FF4D4F" stroke="#0B0D10" stroke-width="1"/>
        <circle cx="24" cy="18" r="1.7" fill="#0B0D10"/>
        <!-- ECG / heartbeat line -->
        <polyline points="12.5,35 18,35 20.2,31.2 23.2,38.8 25.6,33.2 27.4,35 35.5,35"
                  stroke="#00E676" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </div>
    <div>
      <div class="nav-logo-text">DisasterShield</div>
    </div>
  </a>


  <div class="nav-links">
    {nav_links}
  </div>


  <div class="nav-right">
    {loc_pill}

    <div class="nav-btn" id="notif-btn" data-action="notifications" title="Notifications">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
        <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
      </svg>
      <div class="nav-badge" id="notif-badge" style="display:none"></div>
    </div>

    <div class="nav-avatar" id="profile-btn" data-action="profile" title="Profile">
      🧑
    </div>

    <div class="nav-btn" id="ds-hamburger" data-action="mobile-menu" title="Menu">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
        <path d="M3 6h18M3 12h18M3 18h18"/>
      </svg>
    </div>
  </div>
</div>


<div id="ds-mobile-menu">
  {mm_links}
</div>


<div id="notif-panel">
  <div class="np-head">
    <div class="np-title">🔔 Notifications</div>
    <div class="np-actions">
      <button class="np-action" data-np-action="mark-all-read">Mark all read</button>
      <button class="np-action" data-np-action="clear-all">Clear all</button>
    </div>
  </div>
  <div class="np-tabs" id="np-tabs">
    <div class="np-tab active" data-filter="all">All</div>
    <div class="np-tab" data-filter="critical">🔴 Critical</div>
    <div class="np-tab" data-filter="moderate">🟡 Warnings</div>
    <div class="np-tab" data-filter="info">🟢 Info</div>
  </div>
  <div id="np-permission-banner" class="np-permission-banner" style="display:none">
    <span class="np-perm-text">Enable push notifications to receive emergency alerts even when the app is closed.</span>
    <button class="np-perm-btn" data-action="enable-push">Enable</button>
  </div>
  <div class="np-body" id="np-body">
    <div class="np-empty">
      <div class="np-empty-icon">🔔</div>
      Loading alerts…
    </div>
  </div>
</div>


<div id="profile-menu">
  <div class="pm-head">
    <div class="pm-name">DisasterShield User</div>
    <div class="pm-email">suryarmtech@gmail.com</div>
  </div>
  <div class="pm-body">
    <div class="pm-item" data-action="my-profile"><span class="pm-item-ico">👤</span> My Profile</div>
    <div class="pm-sep"></div>
    <div class="pm-item danger" data-action="signout"><span class="pm-item-ico">🚪</span> Sign Out</div>
  </div>
</div>


<div id="critical-overlay">
  <div class="critical-card">
    <div class="critical-pulse" id="critical-icon">🚨</div>
    <div class="critical-title" id="critical-title">Critical Alert</div>
    <div class="critical-body" id="critical-body">A critical disaster event has been detected in your area.</div>
    <div class="critical-btns">
      <button class="critical-btn primary" data-navigate="emergency">View Emergency</button>
      <button class="critical-btn secondary" data-action="dismiss-critical">Dismiss</button>
    </div>
  </div>
</div>


<style>
#ds-search-modal {{
  position:fixed;top:0;left:0;right:0;bottom:0;z-index:20000;
  background:rgba(0,0,0,.65);backdrop-filter:blur(12px);
  display:flex;align-items:flex-start;justify-content:center;
  padding-top:80px;
  opacity:0;pointer-events:none;transition:opacity .2s;
}}
#ds-search-modal.open {{opacity:1;pointer-events:all;}}
.ds-search-box {{
  width:100%;max-width:620px;
  background:rgba(11,13,16,.98);
  border:1px solid rgba(255,213,74,.18);border-radius:18px;
  box-shadow:0 24px 80px rgba(0,0,0,.7);
  overflow:hidden;
  transform:translateY(-12px);transition:transform .2s;
}}
#ds-search-modal.open .ds-search-box {{transform:translateY(0);}}
.ds-search-top {{
  display:flex;align-items:center;gap:12px;padding:16px 18px;
  border-bottom:1px solid rgba(255,255,255,.06);
}}
.ds-search-icon {{font-size:18px;opacity:.5;flex-shrink:0;}}
#ds-search-input {{
  flex:1;background:none;border:none;outline:none;
  font-size:16px;color:#F5F5F5;font-family:'Inter',system-ui,sans-serif;
  caret-color:#FFD54A;
}}
#ds-search-input::placeholder {{color:rgba(255,255,255,.25);}}
.ds-search-kbd {{
  font-size:11px;color:#8B949E;background:rgba(255,255,255,.06);
  border:1px solid rgba(255,255,255,.1);border-radius:5px;
  padding:3px 7px;cursor:pointer;flex-shrink:0;
}}
#ds-search-results {{
  max-height:400px;overflow-y:auto;padding:8px;
}}
#ds-search-results::-webkit-scrollbar {{width:3px;}}
#ds-search-results::-webkit-scrollbar-thumb {{background:rgba(255,213,74,.15);border-radius:99px;}}
.sr-label {{
  font-size:10px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
  color:#8B949E;padding:6px 10px 4px;
}}
.sr-item {{
  display:flex;align-items:center;gap:12px;padding:10px 12px;
  border-radius:10px;cursor:pointer;transition:background .12s;
}}
.sr-item:hover {{background:rgba(255,255,255,.05);}}
.sr-ico {{font-size:20px;width:32px;text-align:center;flex-shrink:0;}}
.sr-title {{font-size:13px;font-weight:600;color:#F5F5F5;}}
.sr-desc {{font-size:11px;color:#8B949E;margin-top:2px;}}
.sr-empty {{text-align:center;padding:40px 20px;color:#8B949E;font-size:13px;}}
.sr-clear {{
  font-size:11px;color:#8B949E;padding:4px 10px 8px;cursor:pointer;
  text-align:right;transition:color .12s;
}}
.sr-clear:hover {{color:#FFD54A;}}
.ds-search-footer {{
  display:flex;gap:16px;padding:10px 18px;
  border-top:1px solid rgba(255,255,255,.05);
  font-size:10.5px;color:#8B949E;
}}
.ds-search-footer kbd {{
  font-size:10px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.1);
  border-radius:4px;padding:1px 5px;margin-right:4px;
}}
</style>
<div id="ds-search-modal">
  <div class="ds-search-box">
    <div class="ds-search-top">
      <span class="ds-search-icon">🔍</span>
      <input id="ds-search-input" placeholder="Search pages, hospitals, alerts, commands…"
        autocomplete="off"/>
      <span class="ds-search-kbd" data-action="close-search">ESC</span>
    </div>
    <div id="ds-search-results"></div>
    <div class="ds-search-footer">
      <span><kbd>↑↓</kbd> Navigate</span>
      <span><kbd>↵</kbd> Select</span>
      <span><kbd>Ctrl K</kbd> Toggle</span>
      <span><kbd>ESC</kbd> Close</span>
    </div>
  </div>
</div>


<div id="ds-backdrop" data-action="close-all"></div>
"""
    # Strip leading indentation and blank lines so Markdown never interprets
    # indented HTML as a 4-space code block (which shows raw HTML as text).
    _nav_html = "\n".join(
        ln.lstrip() for ln in _nav_html.splitlines() if ln.strip()
    )
    st.markdown(_nav_html, unsafe_allow_html=True)

    # Hidden page links — clicked programmatically by dsNavigate() for SPA routing.
    # CSS moves them off-screen; JS .click() still fires Streamlit's React handler.
    st.markdown("""
<style>
[data-testid="stPageLink"] {
  position: fixed !important;
  left: -9999px !important;
  top: -9999px !important;
  width: 1px !important;
  height: 1px !important;
  overflow: hidden !important;
  pointer-events: none !important;
}
</style>
""", unsafe_allow_html=True)
    _hidden_pages = [
        ("frontend/pages/home.py",       "dashboard"),
        ("frontend/pages/risk.py",       "risk"),
        ("frontend/pages/assistant.py",  "assistant"),
        ("frontend/pages/resources.py",  "resources"),
        ("frontend/pages/emergency.py",  "emergency"),
        ("frontend/pages/analytics.py",  "analytics"),
        ("frontend/pages/settings.py",   "settings"),
        ("frontend/pages/profile.py",    "profile"),
        ("frontend/pages/guide.py",      "guide"),
    ]
    for _path, _label in _hidden_pages:
        st.page_link(_path, label=_label)

    # JS runs in a components.html iframe so it actually executes (Streamlit
    # strips <script> from st.markdown). We use window.parent to reach the
    # parent page's DOM. All interactions use data-action / data-navigate /
    # data-filter attributes — NO inline onclick attributes — to avoid race
    # conditions where JS isn't yet loaded when the HTML is first rendered.
    try:
        from backend.services.push_service import get_public_key
        _vapid_pub = get_public_key()
    except Exception:
        _vapid_pub = ""
    _nav_js = """<script>
(function() {
  var doc = window.parent.document;
  var win = window.parent;
  var ls  = win.localStorage;

  /* ── backdrop helpers ── */
  function showBackdrop() {
    var b = doc.getElementById('ds-backdrop');
    if (b) b.classList.add('show');
  }
  function hideBackdrop() {
    var b = doc.getElementById('ds-backdrop');
    if (b) b.classList.remove('show');
  }

  /* ── scroll shrink ── */
  win.addEventListener('scroll', function() {
    var nav = doc.getElementById('ds-nav');
    if (!nav) return;
    if (win.scrollY > 30) nav.classList.add('scrolled');
    else nav.classList.remove('scrolled');
  }, { passive: true });

  /* ── panels ── */
  function closeAll() {
    ['notif-panel','profile-menu','ds-search-modal','ds-mobile-menu'].forEach(function(id) {
      var el = doc.getElementById(id);
      if (el) el.classList.remove('open');
    });
    hideBackdrop();
  }
  win.closeAll = closeAll;

  win.toggleMobileMenu = function() {
    var m = doc.getElementById('ds-mobile-menu');
    if (!m) return;
    var isOpen = m.classList.toggle('open');
    ['notif-panel','profile-menu','ds-search-modal'].forEach(function(id) {
      var el = doc.getElementById(id);
      if (el) el.classList.remove('open');
    });
    isOpen ? showBackdrop() : hideBackdrop();
  };

  win.toggleNotifPanel = function() {
    var p = doc.getElementById('notif-panel');
    if (!p) return;
    var isOpen = p.classList.toggle('open');
    var pm = doc.getElementById('profile-menu');
    if (pm) pm.classList.remove('open');
    isOpen ? showBackdrop() : hideBackdrop();
    if (isOpen) renderNotifications();
  };

  win.toggleProfileMenu = function() {
    var m = doc.getElementById('profile-menu');
    if (!m) return;
    var isOpen = m.classList.toggle('open');
    var np = doc.getElementById('notif-panel');
    if (np) np.classList.remove('open');
    isOpen ? showBackdrop() : hideBackdrop();
  };

  win.toggleSearch = function() {
    var modal = doc.getElementById('ds-search-modal');
    if (!modal) return;
    var isOpen = modal.classList.toggle('open');
    if (isOpen) {
      showBackdrop();
      setTimeout(function() {
        var inp = doc.getElementById('ds-search-input');
        if (inp) inp.focus();
      }, 80);
      win.dsSearchRender('');
    } else {
      hideBackdrop();
    }
  };

  win.closeSearch = function() {
    var m = doc.getElementById('ds-search-modal');
    if (m) m.classList.remove('open');
    hideBackdrop();
  };

  /* ── Notification store ── */
  var STORAGE_KEY = 'ds_notifications';
  function getNotifs() {
    try { return JSON.parse(ls.getItem(STORAGE_KEY) || '[]'); }
    catch(e) { return []; }
  }
  function saveNotifs(n) { ls.setItem(STORAGE_KEY, JSON.stringify(n)); }

  function seedNotifications() {
    if (getNotifs().length > 0) return;
    saveNotifs([
      { id:'n1', sev:'critical', icon:'🌊', title:'Flash Flood Warning',
        body:'Heavy rainfall may cause flash flooding in low-lying areas. Move to higher ground immediately.',
        time: Date.now()-600000, read:false, category:'critical' },
      { id:'n2', sev:'moderate', icon:'🌀', title:'Cyclone Watch Active',
        body:'Cyclonic storm forming in Bay of Bengal. Expected to make landfall in 48 hours.',
        time: Date.now()-3600000, read:false, category:'moderate' },
      { id:'n3', sev:'moderate', icon:'⚡', title:'Thunderstorm Alert',
        body:'Severe thunderstorms expected in coastal zones. Avoid open areas.',
        time: Date.now()-7200000, read:true, category:'moderate' },
      { id:'n4', sev:'info', icon:'☀️', title:'AI Recommendation',
        body:'Based on current patterns, heatwave risk is LOW for your area in the next 72 hours.',
        time: Date.now()-86400000, read:true, category:'info' },
      { id:'n5', sev:'info', icon:'🏛️', title:'Government Advisory',
        body:'IMD issues orange alert for heavy rainfall. Fishermen advised not to venture into sea.',
        time: Date.now()-172800000, read:true, category:'info' },
    ]);
  }

  function unreadCount() { return getNotifs().filter(function(n){return !n.read;}).length; }

  function updateBadge() {
    var badge = doc.getElementById('notif-badge');
    if (badge) badge.style.display = unreadCount() > 0 ? 'block' : 'none';
  }

  win.markAllRead = function() {
    saveNotifs(getNotifs().map(function(n){ return Object.assign({},n,{read:true}); }));
    updateBadge(); renderNotifications();
  };
  win.clearAll = function() { saveNotifs([]); updateBadge(); renderNotifications(); };

  var currentFilter = 'all';
  win.filterNotifs = function(cat, el) {
    currentFilter = cat;
    doc.querySelectorAll('.np-tab').forEach(function(t){ t.classList.remove('active'); });
    if (el) el.classList.add('active');
    renderNotifications();
  };

  function timeAgo(ts) {
    var d = (Date.now()-ts)/1000;
    if (d<60) return 'Just now';
    if (d<3600) return Math.floor(d/60)+'m ago';
    if (d<86400) return Math.floor(d/3600)+'h ago';
    return Math.floor(d/86400)+'d ago';
  }

  var sevMap = {
    critical:{ bg:'rgba(255,77,79,.12)', col:'#FF4D4F', label:'CRITICAL' },
    moderate:{ bg:'rgba(255,179,0,.12)', col:'#FFB300', label:'MODERATE' },
    info:    { bg:'rgba(0,200,83,.1)',   col:'#00C853', label:'INFO' },
  };

  function renderNotifications() {
    var body = doc.getElementById('np-body');
    if (!body) return;
    var notifs = getNotifs();
    if (currentFilter !== 'all') notifs = notifs.filter(function(n){ return n.category===currentFilter; });
    if (!notifs.length) {
      body.innerHTML = '<div class="np-empty"><div class="np-empty-icon">🔔</div>No notifications in this category.</div>';
      return;
    }
    body.innerHTML = notifs.map(function(n, i) {
      var sev = sevMap[n.sev] || sevMap.info;
      return '<div class="notif-item '+(n.read?'':'unread')+'" data-notif-id="'+n.id+'" style="animation-delay:'+(i*.04)+'s">'
        +'<div class="notif-icon" style="background:'+sev.bg+'">'+n.icon+'</div>'
        +'<div class="notif-content">'
        +'<div class="notif-title">'+n.title+'</div>'
        +'<div class="notif-body">'+n.body+'</div>'
        +'<div class="notif-meta"><span class="notif-time">'+timeAgo(n.time)+'</span>'
        +'<span class="notif-sev" style="background:'+sev.bg+';color:'+sev.col+'">'+sev.label+'</span></div>'
        +'</div></div>';
    }).join('');
  }

  win.markRead = function(id) {
    saveNotifs(getNotifs().map(function(n){ return n.id===id ? Object.assign({},n,{read:true}) : n; }));
    updateBadge(); renderNotifications();
  };

  /* ── OS-level browser notifications (notification drawer) ──
     Fire while the app is open, even in a background tab or minimized
     window. True closed-browser push would need a Web Push backend. */
  var DS_ICON = 'data:image/svg+xml,' + encodeURIComponent(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
    + '<rect width="64" height="64" rx="14" fill="#0B0D10"/>'
    + '<path d="M32 8L10 18v14c0 14 9.6 26.4 22 30 12.4-3.6 22-16 22-30V18L32 8z" '
    + 'fill="none" stroke="#FFD54A" stroke-width="4"/>'
    + '<circle cx="32" cy="27" r="10" fill="none" stroke="#FFD54A" stroke-width="2.5"/>'
    + '<circle cx="32" cy="27" r="3.5" fill="#FF4D4F"/>'
    + '<polyline points="18,46 26,46 29,41 33,50 36,44 46,46" fill="none" '
    + 'stroke="#00E676" stroke-width="3" stroke-linecap="round"/></svg>');

  function showBrowserNotif(title, body, critical) {
    try {
      if (!('Notification' in win) || win.Notification.permission !== 'granted') return;
      var n = new win.Notification(title, {
        body: body,
        icon: DS_ICON,
        badge: DS_ICON,
        tag: 'ds-' + Date.now(),
        requireInteraction: !!critical,
        silent: false
      });
      n.onclick = function() { win.focus(); n.close(); };
    } catch(e) {}
  }
  win.showBrowserNotif = showBrowserNotif;

  /* VAPID public key injected by Python at render time */
  var VAPID_KEY = '__VAPID_PUBLIC_KEY__';

  function urlB64ToUint8Array(base64String) {
    var padding = '='.repeat((4 - base64String.length % 4) % 4);
    var base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/');
    var raw = win.atob(base64);
    var arr = new Uint8Array(raw.length);
    for (var i = 0; i < raw.length; i++) arr[i] = raw.charCodeAt(i);
    return arr;
  }

  /* Register the real service worker file and subscribe to Web Push.
     The subscription JSON is stored in localStorage; the Settings page
     syncs it to the server, which then pushes alerts via FCM/autopush
     even when the browser is fully closed. */
  win.dsSubscribePush = async function() {
    if (!('serviceWorker' in win.navigator) || !('PushManager' in win)) return false;
    if (!VAPID_KEY || VAPID_KEY.indexOf('__') === 0) return false;
    try {
      var reg = await win.navigator.serviceWorker.register('/app/static/sw.js');
      var sub = await reg.pushManager.getSubscription();
      if (!sub) {
        sub = await reg.pushManager.subscribe({
          userVisibleOnly: true,
          applicationServerKey: urlB64ToUint8Array(VAPID_KEY)
        });
      }
      win.localStorage.setItem('ds_push_sub', JSON.stringify(sub.toJSON()));
      return true;
    } catch (e) {
      console.warn('[DisasterShield] push subscribe failed:', e);
      return false;
    }
  };

  win.requestPushPermission = async function() {
    if (!('Notification' in win)) { win.dsToast('Browser does not support push notifications.','warn'); return; }
    var perm = await win.Notification.requestPermission();
    if (perm === 'granted') {
      var banner = doc.getElementById('np-permission-banner');
      if (banner) banner.style.display = 'none';
      var subscribed = await win.dsSubscribePush();
      if (subscribed) {
        win.dsToast('Push enabled! Visit Settings once to finish closed-browser alerts.','success');
      } else {
        win.dsToast('Emergency alerts enabled for open tabs.','success');
      }
      showBrowserNotif('✅ DisasterShield Alerts Enabled',
        'Emergency alerts will now appear in your notification drawer.');
    } else if (perm === 'denied') {
      win.dsToast('Notifications blocked. Enable them in your browser site settings.','warn');
    }
  };

  /* ── SPA navigation via hidden st.page_link() anchors ── */
  win.dsNavigate = function(slug) {
    closeAll();
    var links = doc.querySelectorAll('[data-testid="stPageLink"] a');
    
    // Normalize slug to match root/dashboard
    var targetSlug = slug ? slug.trim().toLowerCase() : '';
    if (targetSlug === './' || targetSlug === 'dashboard') {
      targetSlug = '';
    }
    
    for (var j = 0; j < links.length; j++) {
      var href = links[j].getAttribute('href') || '';
      var hrefLower = href.trim().toLowerCase();
      
      if (targetSlug === '') {
        // Dashboard link: look for root path or empty href
        if (hrefLower === '/' || hrefLower === '' || hrefLower.endsWith('/')) {
          links[j].click();
          return;
        }
      } else {
        // Subpage link: check if href matches the slug name
        if (hrefLower === targetSlug || hrefLower === '/' + targetSlug || hrefLower.endsWith('/' + targetSlug)) {
          links[j].click();
          return;
        }
      }
    }
    
    // central fallback: if no link found, navigate in same tab
    if (targetSlug === '') {
      win.location.href = '/';
    } else {
      win.location.href = '/' + slug;
    }
  };

  /* ── Toast ── */
  win.dsToast = function(msg, type) {
    var existing = doc.getElementById('ds-toast');
    if (existing) existing.remove();
    var t = doc.createElement('div');
    t.id = 'ds-toast';
    var bg = type==='success'?'#00C853':type==='warn'?'#FFB300':type==='error'?'#FF4D4F':'#FFD54A';
    t.style.cssText = 'position:fixed;bottom:24px;left:50%;transform:translateX(-50%) translateY(20px);'
      +'background:rgba(11,13,16,.97);border:1px solid '+bg+'44;color:#F5F5F5;'
      +'font-size:13px;font-weight:500;padding:12px 20px;border-radius:12px;z-index:99999;'
      +'box-shadow:0 8px 32px rgba(0,0,0,.5);transition:all .3s;opacity:0;'
      +'backdrop-filter:blur(16px);font-family:Inter,system-ui,sans-serif;'
      +'border-left:3px solid '+bg;
    t.textContent = msg;
    doc.body.appendChild(t);
    requestAnimationFrame(function(){ t.style.opacity='1'; t.style.transform='translateX(-50%) translateY(0)'; });
    setTimeout(function(){
      t.style.opacity='0'; t.style.transform='translateX(-50%) translateY(20px)';
      setTimeout(function(){ t.remove(); }, 300);
    }, 3500);
  };

  /* ── DSNotify (Python-callable) ── */
  win.DSNotify = function(title, body, critical) {
    critical = !!critical;
    var notifs = getNotifs();
    notifs.unshift({ id:'n'+Date.now(), sev:critical?'critical':'moderate',
      icon:critical?'🚨':'⚠️', title:title, body:body,
      time:Date.now(), read:false, category:critical?'critical':'moderate' });
    saveNotifs(notifs.slice(0,50));
    updateBadge();
    showBrowserNotif(title, body, critical);
    if (critical) {
      var ct = doc.getElementById('critical-title');
      var cb = doc.getElementById('critical-body');
      var co = doc.getElementById('critical-overlay');
      if (ct) ct.textContent = title;
      if (cb) cb.textContent = body;
      if (co) co.classList.add('show');
    }
  };

  win.dismissCritical = function() {
    var el = doc.getElementById('critical-overlay');
    if (el) el.classList.remove('show');
  };

  /* ── Search ── */
  var DS_PAGES = [
    {icon:'🏠',label:'Dashboard',slug:'',desc:'Main overview & live threat map'},
    {icon:'📊',label:'Risk Monitor',slug:'risk',desc:'Real-time risk assessment'},
    {icon:'🤖',label:'AI Assistant',slug:'assistant',desc:'Disaster intelligence chatbot'},
    {icon:'🏥',label:'Resources',slug:'resources',desc:'Hospitals & shelters near you'},
    {icon:'🆘',label:'Emergency SOS',slug:'emergency',desc:'Emergency services & SOS'},
    {icon:'📈',label:'Analytics',slug:'analytics',desc:'Disaster intelligence analytics'},
    {icon:'⚙️',label:'Settings',slug:'settings',desc:'Platform settings & preferences'},
  ];
  var DS_QUICK = [
    {icon:'🌊',label:'Flood Risk',slug:'risk',desc:'Check current flood risk'},
    {icon:'🌀',label:'Cyclone Status',slug:'risk',desc:'Cyclone tracking & warnings'},
    {icon:'🏠',label:'Nearby Shelters',slug:'resources',desc:'Emergency shelters near you'},
    {icon:'🏥',label:'Nearest Hospital',slug:'resources',desc:'Hospitals sorted by distance'},
    {icon:'📞',label:'Emergency Contacts',slug:'emergency',desc:'112 & emergency numbers'},
    {icon:'🌡',label:'Weather Data',slug:'',desc:'Live temperature & conditions'},
    {icon:'🤖',label:'Ask AI',slug:'assistant',desc:'Chat with AI assistant'},
    {icon:'🔔',label:'Notifications',slug:'',desc:'View all alerts',action:'notif'},
  ];

  win.dsSearchRender = function(q) {
    var res = doc.getElementById('ds-search-results');
    if (!res) return;
    var val = q.toLowerCase().trim();
    var recent = [];
    try { recent = JSON.parse(ls.getItem('ds_recent_search') || '[]'); } catch(e){}
    if (!val) {
      var html = '';
      if (recent.length) {
        html += '<div class="sr-label">Recent Searches</div>';
        html += recent.slice(0,4).map(function(r){
          return '<div class="sr-item" data-search-slug="'+r.slug+'" data-search-label="'+r.label+'">'
            +'<span class="sr-ico">🕐</span><div><div class="sr-title">'+r.label+'</div>'
            +'<div class="sr-desc">'+r.desc+'</div></div></div>';
        }).join('');
        html += '<div class="sr-clear" id="sr-clear-btn">Clear recent</div>';
      }
      html += '<div class="sr-label">Quick Actions</div>';
      html += DS_QUICK.map(function(p){
        return '<div class="sr-item" data-search-slug="'+(p.action||p.slug)+'" data-search-label="'+p.label+'" data-search-action="'+(p.action||'')+'">'
          +'<span class="sr-ico">'+p.icon+'</span><div><div class="sr-title">'+p.label+'</div>'
          +'<div class="sr-desc">'+p.desc+'</div></div></div>';
      }).join('');
      res.innerHTML = html;
      var clr = doc.getElementById('sr-clear-btn');
      if (clr) clr.addEventListener('click', function(){
        ls.removeItem('ds_recent_search'); win.dsSearchRender('');
      });
      return;
    }
    var all = DS_PAGES.concat(DS_QUICK);
    var matches = all.filter(function(p){
      return p.label.toLowerCase().indexOf(val)>=0 || p.desc.toLowerCase().indexOf(val)>=0;
    });
    if (!matches.length) {
      res.innerHTML = '<div class="sr-empty"><div style="font-size:32px;margin-bottom:8px;opacity:.4">🔍</div>No results for "'+q+'"<br><span style="font-size:11px;color:#8B949E;margin-top:6px;display:block">Try: dashboard, hospitals, cyclone, risk…</span></div>';
      return;
    }
    res.innerHTML = '<div class="sr-label">Results</div>'
      + matches.map(function(p){
        return '<div class="sr-item" data-search-slug="'+p.slug+'" data-search-label="'+p.label+'">'
          +'<span class="sr-ico">'+p.icon+'</span><div><div class="sr-title">'+p.label+'</div>'
          +'<div class="sr-desc">'+p.desc+'</div></div></div>';
      }).join('');
  };

  win.dsSearchGo = function(slug, label, action) {
    var recent = [];
    try { recent = JSON.parse(ls.getItem('ds_recent_search') || '[]'); } catch(e){}
    var all = DS_PAGES.concat(DS_QUICK);
    var entry = null;
    for (var i=0; i<all.length; i++) { if (all[i].label===label) { entry=all[i]; break; } }
    if (!entry) entry = {icon:'🔍',label:label,slug:slug,desc:''};
    var filtered = recent.filter(function(r){ return r.label!==label; });
    filtered.unshift(entry);
    ls.setItem('ds_recent_search', JSON.stringify(filtered.slice(0,8)));
    win.closeSearch();
    if (action==='notif') { win.toggleNotifPanel(); return; }
    win.dsNavigate(slug);
  };

  /* ── Event delegation on parent document ── */
  doc.addEventListener('click', function(e) {
    /* nav links with data-navigate */
    var navLink = e.target.closest('[data-navigate]');
    if (navLink) {
      e.preventDefault();
      win.dsNavigate(navLink.getAttribute('data-navigate'));
      return;
    }
    /* data-action dispatch for all header buttons */
    var actionEl = e.target.closest('[data-action]');
    if (actionEl) {
      var act = actionEl.getAttribute('data-action');
      switch(act) {
        case 'search': win.toggleSearch(); break;
        case 'notifications': win.toggleNotifPanel(); break;
        case 'profile': win.toggleProfileMenu(); break;
        case 'my-profile': closeAll(); win.dsNavigate('profile'); break;
        case 'mobile-menu': win.toggleMobileMenu(); break;
        case 'close-search': win.closeSearch(); break;
        case 'close-all': closeAll(); break;
        case 'dismiss-critical': win.dismissCritical(); break;
        case 'enable-push': win.requestPushPermission(); break;
        case 'signout': closeAll(); win.dsToast('Signed out successfully.', 'success'); break;
        case 'notif': closeAll(); win.toggleNotifPanel(); break;
        case 'mark-all-read': win.markAllRead(); break;
        case 'clear-all': win.clearAll(); break;
        case 'clear-recent': window.parent.localStorage.removeItem('ds_recent_search'); break;
        default: if (act) { closeAll(); win.dsNavigate(act); } break;
      }
      return;
    }
    /* backdrop */
    if (e.target.id === 'ds-backdrop') { closeAll(); return; }
    /* search modal backdrop click */
    if (e.target.id === 'ds-search-modal') { win.closeSearch(); return; }
    /* notification panel actions */
    if (e.target.closest('[data-np-action]')) {
      var a = e.target.closest('[data-np-action]').getAttribute('data-np-action');
      if (a==='mark-all-read') win.markAllRead();
      if (a==='clear-all') win.clearAll();
      return;
    }
    /* notification tab filters via data-filter attribute */
    var tabEl = e.target.closest('.np-tab[data-filter]');
    if (tabEl) {
      var tabs = doc.querySelectorAll('.np-tab');
      for (var t = 0; t < tabs.length; t++) tabs[t].classList.remove('active');
      tabEl.classList.add('active');
      currentFilter = tabEl.getAttribute('data-filter') || 'all';
      renderNotifications();
      return;
    }
    /* legacy np-tab without data-filter */
    var legacyTab = e.target.closest('.np-tab');
    if (legacyTab) {
      var tabs2 = doc.querySelectorAll('.np-tab');
      for (var t2 = 0; t2 < tabs2.length; t2++) tabs2[t2].classList.remove('active');
      legacyTab.classList.add('active');
      var txt = legacyTab.textContent.toLowerCase();
      currentFilter = txt.indexOf('critical')>=0?'critical':txt.indexOf('warn')>=0?'moderate':txt.indexOf('info')>=0?'info':'all';
      renderNotifications();
      return;
    }
    /* notification item click → mark read */
    var ni = e.target.closest('[data-notif-id]');
    if (ni) { win.markRead(ni.getAttribute('data-notif-id')); return; }
    /* push notification enable banner */
    if (e.target.closest('.np-perm-btn')) { win.requestPushPermission(); return; }
    /* profile menu items */
    var pm = e.target.closest('.pm-item[data-action]');
    if (pm) {
      var act = pm.getAttribute('data-action');
      if (act==='signout') { closeAll(); win.dsToast('Signed out successfully.','success'); return; }
      if (act==='notif') { closeAll(); win.toggleNotifPanel(); return; }
      closeAll(); win.dsNavigate(act);
      return;
    }
    /* critical overlay buttons */
    if (e.target.closest('#critical-overlay .critical-btn.primary')) {
      win.dismissCritical(); win.dsNavigate('emergency'); return;
    }
    if (e.target.closest('#critical-overlay .critical-btn.secondary')) {
      win.dismissCritical(); return;
    }
    /* search result items */
    var sri = e.target.closest('.sr-item[data-search-slug]');
    if (sri) {
      win.dsSearchGo(
        sri.getAttribute('data-search-slug'),
        sri.getAttribute('data-search-label'),
        sri.getAttribute('data-search-action') || ''
      );
      return;
    }
    /* logo → dashboard */
    if (e.target.closest('.nav-logo')) { e.preventDefault(); win.dsNavigate(''); return; }
  });

  /* ── Keyboard shortcuts ── */
  doc.addEventListener('keydown', function(e) {
    if ((e.ctrlKey || e.metaKey) && e.key==='k') { e.preventDefault(); win.toggleSearch(); return; }
    if (e.key==='Escape') closeAll();
  });

  /* ── Search input live filter ── */
  doc.addEventListener('input', function(e) {
    if (e.target && e.target.id==='ds-search-input') win.dsSearchRender(e.target.value);
  });

  /* ── Hoist overlays to <body> so position:fixed works ── */
  function hoistToBody() {
    ['notif-panel','profile-menu','critical-overlay','ds-backdrop','ds-search-modal','ds-mobile-menu'].forEach(function(id){
      var el = doc.getElementById(id);
      if (el && el.parentNode !== doc.body) doc.body.appendChild(el);
    });
  }

  /* ── Force same-tab navigation everywhere (Streamlit markdown adds _blank) ── */
  function stripTargetBlank() {
    doc.querySelectorAll('a[target="_blank"]').forEach(function(a){
      a.setAttribute('target','_self');
    });
  }
  new win.MutationObserver(stripTargetBlank)
    .observe(doc.body, { childList: true, subtree: true });

  /* ── Init ── */
  function init() {
    var APP_VERSION = '1.0.5';
    if (ls.getItem('ds_app_version') !== APP_VERSION) {
      ls.clear();
      ls.setItem('ds_app_version', APP_VERSION);
      win.location.reload();
      return;
    }
    seedNotifications();
    updateBadge();
    hoistToBody();
    stripTargetBlank();
    var oldSpacer = doc.getElementById('ds-nav-spacer');
    if (oldSpacer) oldSpacer.remove();
    win.dsSearchRender('');
    /* push banner */
    try {
      if ('Notification' in win && win.Notification.permission === 'default') {
        var banner = doc.getElementById('np-permission-banner');
        if (banner) banner.style.display = 'flex';
      }
    } catch(e) {}
  }

  if (doc.readyState === 'loading') {
    doc.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
</script>"""
    components.html(_nav_js.replace("__VAPID_PUBLIC_KEY__", _vapid_pub), height=0)


# ─────────────────────────────────────────────────────────────────────────────
# METRIC WIDGETS (Analytics Strip)
# ─────────────────────────────────────────────────────────────────────────────
def metric_widgets(weather: dict):
    if not weather.get("available"):
        st.markdown("""
<div style="padding:0 24px;display:flex;align-items:center;justify-content:center;
  height:100px;color:var(--gray);font-size:13px;gap:8px">
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor"
       stroke-width="2"><circle cx="12" cy="12" r="10"/>
    <path d="M12 6v6l4 2"/></svg>
  Fetching live weather data…
</div>""", unsafe_allow_html=True)
        return

    temp  = weather.get("temperature_c",   "--")
    feels = weather.get("feels_like_c",    "--")
    hum   = weather.get("humidity_pct",    "--")
    wind  = weather.get("wind_kmh") or weather.get("wind_speed_kmh", "--")
    rain  = weather.get("rainfall_mm",     "--")
    pres  = weather.get("pressure_hpa",    "--")
    vis   = weather.get("visibility_km",   "--")
    desc  = weather.get("description",     "")
    uv    = weather.get("uv_index",        "--")
    aqi   = weather.get("aqi",             "--")

    def fmt(v, nd=0):
        if isinstance(v, (int, float)):
            return f"{v:.{nd}f}" if nd else f"{v:.0f}"
        return "--"

    def sparkline(vals, color, uid):
        vmin, vmax = min(vals), max(vals)
        rng = (vmax - vmin) or 1
        n = len(vals)
        step = 100 / (n - 1)
        pts = " ".join(f"{i*step:.1f},{34 - ((v - vmin) / rng) * 26:.1f}" for i, v in enumerate(vals))
        return (f'<svg viewBox="0 0 100 36" preserveAspectRatio="none" '
                f'style="width:100%;height:34px;display:block" fill="none">'
                f'<defs><linearGradient id="spk{uid}" x1="0" y1="0" x2="0" y2="1">'
                f'<stop offset="0%" stop-color="{color}" stop-opacity=".3"/>'
                f'<stop offset="100%" stop-color="{color}" stop-opacity="0"/></linearGradient></defs>'
                f'<polygon points="0,36 {pts} 100,36" fill="url(#spk{uid})"/>'
                f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="1.6" '
                f'stroke-linecap="round" stroke-linejoin="round" vector-effect="non-scaling-stroke"/>'
                f'</svg>')

    def num(v, default):
        return v if isinstance(v, (int, float)) else default

    sp_t = sparkline([22,24,27,29,30,28,26,29,31, num(temp, 28)], "#FFD54A", "t")
    sp_h = sparkline([60,65,72,75,77,80,76, num(hum, 72), 74,70], "#3B82F6", "h")
    sp_w = sparkline([5,8,10,12,10,11,9, num(wind, 10), 13,11],   "#8B5CF6", "w")
    sp_r = sparkline([0,0,1,2,0,0, num(rain, 0), 0,0,0],          "#00C853", "r")
    sp_p = sparkline([1010,1008,1006,1005,1003,1004, num(pres, 1005), 1006,1007,1005], "#FFB300", "p")
    sp_v = sparkline([20,22,25, num(vis, 22), 24,20,18,21,25,23], "#00C853", "v")

    unit = ('<span style="font-size:11px;font-weight:600;color:var(--gray);'
            'letter-spacing:0;margin-left:3px">{u}</span>')
    cards = [
        ("🌡", "Temperature", f"{fmt(temp,1)}°C", f"Feels {fmt(feels,1)}°C", "#FFD54A", sp_t, "color:var(--gold)"),
        ("💧", "Humidity",    f"{fmt(hum)}%",     "Relative humidity",       "#3B82F6", sp_h, "color:#3B82F6"),
        ("💨", "Wind",        f"{fmt(wind)}"  + unit.format(u="km/h"), "Surface wind",  "#8B5CF6", sp_w, "color:#8B5CF6"),
        ("🌧", "Rainfall",    f"{fmt(rain,1)}" + unit.format(u="mm"),  "Last 1 hour",   "#00C853", sp_r, "color:var(--success)"),
        ("🔵", "Pressure",    f"{fmt(pres)}"  + unit.format(u="hPa"),  "Atmospheric",   "#FFB300", sp_p, "color:var(--warn)"),
        ("👁", "Visibility",  f"{fmt(vis)}"   + unit.format(u="km"),   "Optical range", "#00C853", sp_v, "color:var(--success)"),
    ]

    html = ('<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));'
            'gap:10px;padding:14px 24px 4px;">')
    for ico, label, val, sub, col, sp, val_css in cards:
        html += (
            f'<div class="ds-metric-card" style="background:var(--glass);border:1px solid var(--border2);'
            f'border-radius:var(--r);padding:14px 14px 12px;position:relative;overflow:hidden;cursor:default;'
            f'display:flex;flex-direction:column;min-height:150px">'
            f'<div style="position:absolute;top:0;left:0;right:0;height:1px;'
            f'background:linear-gradient(90deg,transparent,{col}55,transparent)"></div>'
            f'<div style="font-size:9.5px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;'
            f'color:var(--gray);margin-bottom:8px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">'
            f'{ico} {label}</div>'
            f'<div style="font-size:21px;font-weight:800;letter-spacing:-.03em;'
            f'font-variant-numeric:tabular-nums;{val_css};line-height:1;margin-bottom:4px;'
            f'white-space:nowrap">{val}</div>'
            f'<div style="font-size:10.5px;color:var(--gray);white-space:nowrap;overflow:hidden;'
            f'text-overflow:ellipsis">{sub}</div>'
            f'<div style="margin-top:auto;padding-top:10px">{sp}</div>'
            f'</div>'
        )
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# PUSH NOTIFICATION TRIGGER (called after risk assessment)
# ─────────────────────────────────────────────────────────────────────────────
def trigger_push_alerts(predictions: list):
    if not predictions:
        return
    critical = [p for p in predictions if p.get("risk_level") == "Critical"]
    high     = [p for p in predictions if p.get("risk_level") == "High"]

    calls = []
    for p in critical[:2]:
        title = f"🚨 CRITICAL: {p['disaster']} Detected"
        body  = p.get("reason", "A critical disaster event has been detected in your area.")
        calls.append(f'window.DSNotify({repr(title)}, {repr(body)}, true);')

    for p in high[:2]:
        title = f"⚠️ HIGH RISK: {p['disaster']} Warning"
        body  = p.get("reason", "High risk detected. Take immediate precautions.")
        calls.append(f'window.DSNotify({repr(title)}, {repr(body)}, false);')

    if calls:
        js = "\n".join(c.replace("window.DSNotify", "window.parent.DSNotify") for c in calls)
        # st.markdown strips <script>; components.html actually executes it.
        components.html(
            f"<script>setTimeout(function() {{ {js} }}, 2500);</script>",
            height=0,
        )


# ─────────────────────────────────────────────────────────────────────────────
# CHAT BUBBLE
# ─────────────────────────────────────────────────────────────────────────────
def chat_bubble(role: str, content: str, is_typing: bool = False):
    if role == "user":
        st.markdown(f"""
<div style="display:flex;justify-content:flex-end;margin:12px 0;padding:0 24px">
  <div style="max-width:72%;background:linear-gradient(135deg,#FFD54A,#D4AF37);
    border-radius:18px 18px 4px 18px;padding:12px 16px;
    box-shadow:0 4px 20px rgba(255,213,74,.2)">
    <div style="font-size:13.5px;color:#050505;font-weight:500;line-height:1.55">{content}</div>
  </div>
</div>""", unsafe_allow_html=True)
    elif is_typing:
        st.markdown("""
<div style="display:flex;align-items:flex-end;gap:10px;margin:12px 0;padding:0 24px">
  <div style="width:32px;height:32px;border-radius:50%;flex-shrink:0;
    background:linear-gradient(135deg,#FFD54A,#D4AF37);
    display:flex;align-items:center;justify-content:center;font-size:15px">🛡</div>
  <div style="background:var(--glass);border:1px solid var(--border2);
    border-radius:18px 18px 18px 4px;padding:14px 18px">
    <div style="display:flex;gap:5px;align-items:center;height:16px">
      <div style="width:7px;height:7px;border-radius:50%;background:var(--gold);
        animation:bounce .8s ease infinite"></div>
      <div style="width:7px;height:7px;border-radius:50%;background:var(--gold);
        animation:bounce .8s .15s ease infinite"></div>
      <div style="width:7px;height:7px;border-radius:50%;background:var(--gold);
        animation:bounce .8s .3s ease infinite"></div>
    </div>
  </div>
</div>
<style>@keyframes bounce{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}</style>
""", unsafe_allow_html=True)
    else:
        import re
        # Basic markdown: **bold**, `code`
        html_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
        html_content = re.sub(r'`(.*?)`', r'<code style="background:rgba(255,213,74,.1);color:var(--gold);padding:1px 5px;border-radius:4px;font-size:.9em">\1</code>', html_content)
        html_content = html_content.replace("\n\n", "<br><br>").replace("\n", "<br>")
        st.markdown(f"""
<div style="display:flex;align-items:flex-start;gap:10px;margin:12px 0;padding:0 24px">
  <div style="width:32px;height:32px;border-radius:50%;flex-shrink:0;
    background:linear-gradient(135deg,#FFD54A,#D4AF37);
    display:flex;align-items:center;justify-content:center;font-size:15px;
    box-shadow:0 0 16px rgba(255,213,74,.25)">🛡</div>
  <div style="max-width:76%;background:var(--glass);border:1px solid var(--border2);
    border-radius:18px 18px 18px 4px;padding:13px 17px">
    <div style="font-size:13.5px;color:var(--white);line-height:1.65">{html_content}</div>
  </div>
</div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION HEADER
# ─────────────────────────────────────────────────────────────────────────────
def section_header(title: str, subtitle: str = "", badge: str = ""):
    badge_html = (f'<span style="font-size:10px;font-weight:700;padding:2px 9px;border-radius:99px;background:var(--gold-lo);color:var(--gold);border:1px solid var(--border);letter-spacing:.06em;text-transform:uppercase">{badge}</span>') if badge else ""
    sub_html = (f'<div style="font-size:13px;color:var(--gray);margin-top:4px">{subtitle}</div>') if subtitle else ""
    # Single-line HTML avoids Markdown's 4-space-indent → code-block misparse
    st.markdown(f'<div style="padding:0 24px;margin:28px 0 16px;display:flex;align-items:center;gap:12px"><div><div style="display:flex;align-items:center;gap:8px"><div style="font-size:16px;font-weight:700;color:var(--white)">{title}</div>{badge_html}</div>{sub_html}</div></div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# RESOURCE CARD
# ─────────────────────────────────────────────────────────────────────────────
def resource_card(rank, name, dist_km, extra="", nav_url="#"):
    colors = ["#FFD54A", "#D4AF37", "#8B949E"]
    c = colors[min(rank - 1, 2)]
    st.markdown(f"""
<div class="ds-res-card" style="background:var(--glass);border:1px solid var(--border2);border-radius:var(--r);
  padding:16px 18px;display:flex;align-items:center;gap:14px;
  cursor:pointer;margin-bottom:8px">
  <div style="width:30px;height:30px;border-radius:50%;background:rgba(18,20,26,.9);
    border:1px solid {c}44;display:flex;align-items:center;justify-content:center;
    font-size:12px;font-weight:800;color:{c};flex-shrink:0">{rank}</div>
  <div style="flex:1;min-width:0">
    <div style="font-size:13.5px;font-weight:600;color:var(--white);
      overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{name}</div>
    <div style="font-size:11px;color:var(--gray);margin-top:2px">
      📍 {dist_km} km away{f" · {extra}" if extra else ""}</div>
  </div>
  <a href="{nav_url}" target="_self" class="ds-res-card-nav-btn" style="flex-shrink:0;padding:7px 14px;
    background:var(--gold-lo);border:1px solid var(--border);border-radius:8px;
    font-size:11px;font-weight:600;color:var(--gold);text-decoration:none;
    white-space:nowrap">Navigate →</a>
</div>""", unsafe_allow_html=True)
