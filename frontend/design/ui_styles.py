"""Shared CSS injected into every page for a consistent native-app look."""

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Reset & Base ─────────────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}
.stApp {
    background: #0d1117 !important;
    color: #c9d1d9 !important;
}

/* ── Hide Streamlit chrome ────────────────────────────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Sidebar ──────────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: #0d1117 !important;
    border-right: 1px solid #21262d !important;
}
[data-testid="stSidebar"] * { color: #c9d1d9 !important; }

/* ── Tabs ─────────────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    gap: 4px;
    border-bottom: 1px solid #21262d !important;
    padding-bottom: 0;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #8b949e !important;
    border-radius: 8px 8px 0 0 !important;
    padding: 8px 16px !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    border: none !important;
    transition: all 0.2s ease !important;
}
.stTabs [aria-selected="true"] {
    background: #161b22 !important;
    color: #58a6ff !important;
    border-bottom: 2px solid #58a6ff !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: transparent !important;
    padding-top: 20px !important;
}

/* ── Metric cards ─────────────────────────────────────────────────────────── */
[data-testid="metric-container"] {
    background: #161b22 !important;
    border: 1px solid #21262d !important;
    border-radius: 12px !important;
    padding: 16px !important;
}
[data-testid="metric-container"] label {
    color: #8b949e !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #c9d1d9 !important;
    font-size: 24px !important;
    font-weight: 700 !important;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    color: #8b949e !important;
    font-size: 12px !important;
}

/* ── Buttons ──────────────────────────────────────────────────────────────── */
.stButton > button {
    background: #1f6feb !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 8px 20px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    transition: all 0.2s ease !important;
    width: 100%;
}
.stButton > button:hover {
    background: #388bfd !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(31,111,235,0.4) !important;
}

/* ── Link buttons ─────────────────────────────────────────────────────────── */
[data-testid="stLinkButton"] a {
    background: #21262d !important;
    color: #58a6ff !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    padding: 8px 16px !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    text-decoration: none !important;
    display: inline-block !important;
    transition: all 0.2s ease !important;
}
[data-testid="stLinkButton"] a:hover {
    background: #30363d !important;
    border-color: #58a6ff !important;
}

/* ── Alerts / Banners ─────────────────────────────────────────────────────── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    border-left: 4px solid !important;
    padding: 12px 16px !important;
}
.stSuccess {
    background: rgba(35, 134, 54, 0.15) !important;
    border-color: #238636 !important;
    color: #3fb950 !important;
}
.stWarning {
    background: rgba(210, 153, 34, 0.15) !important;
    border-color: #d29922 !important;
    color: #e3b341 !important;
}
.stError {
    background: rgba(218, 54, 51, 0.15) !important;
    border-color: #da3633 !important;
    color: #f85149 !important;
}
.stInfo {
    background: rgba(31, 111, 235, 0.1) !important;
    border-color: #1f6feb !important;
    color: #58a6ff !important;
}

/* ── Text inputs ──────────────────────────────────────────────────────────── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #0d1117 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    color: #c9d1d9 !important;
    font-size: 14px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #58a6ff !important;
    box-shadow: 0 0 0 3px rgba(88,166,255,0.15) !important;
}

/* ── File uploader ────────────────────────────────────────────────────────── */
[data-testid="stFileUploader"] {
    background: #161b22 !important;
    border: 2px dashed #30363d !important;
    border-radius: 12px !important;
    padding: 20px !important;
}

/* ── Expander ─────────────────────────────────────────────────────────────── */
[data-testid="stExpander"] {
    background: #161b22 !important;
    border: 1px solid #21262d !important;
    border-radius: 10px !important;
    margin-bottom: 8px !important;
}
[data-testid="stExpander"] summary {
    color: #c9d1d9 !important;
    font-weight: 500 !important;
}

/* ── Divider ──────────────────────────────────────────────────────────────── */
hr {
    border-color: #21262d !important;
    margin: 20px 0 !important;
}

/* ── Spinner ──────────────────────────────────────────────────────────────── */
.stSpinner > div {
    border-top-color: #58a6ff !important;
}

/* ── Page links (sidebar nav) ─────────────────────────────────────────────── */
[data-testid="stPageLink"] a {
    color: #8b949e !important;
    font-size: 14px !important;
    padding: 6px 10px !important;
    border-radius: 6px !important;
    transition: all 0.15s ease !important;
    display: block !important;
}
[data-testid="stPageLink"] a:hover {
    background: #161b22 !important;
    color: #c9d1d9 !important;
}

/* ── Custom card component ────────────────────────────────────────────────── */
.ds-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 12px;
}
.ds-card-title {
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #8b949e;
    margin-bottom: 8px;
}
.ds-card-value {
    font-size: 28px;
    font-weight: 700;
    color: #e6edf3;
    line-height: 1.2;
}
.ds-card-sub {
    font-size: 12px;
    color: #8b949e;
    margin-top: 4px;
}

/* ── Risk badge ───────────────────────────────────────────────────────────── */
.badge-low      { background:#0d4a1e; color:#3fb950; border:1px solid #238636; border-radius:20px; padding:3px 12px; font-size:12px; font-weight:600; display:inline-block; }
.badge-moderate { background:#3b2900; color:#e3b341; border:1px solid #d29922; border-radius:20px; padding:3px 12px; font-size:12px; font-weight:600; display:inline-block; }
.badge-high     { background:#3d0000; color:#f85149; border:1px solid #da3633; border-radius:20px; padding:3px 12px; font-size:12px; font-weight:600; display:inline-block; }
.badge-critical { background:#2d0a3e; color:#d2a8ff; border:1px solid #8957e5; border-radius:20px; padding:3px 12px; font-size:12px; font-weight:600; display:inline-block; }

/* ── Emergency contact card ───────────────────────────────────────────────── */
.ec-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.ec-service { font-size: 14px; font-weight: 500; color: #c9d1d9; }
.ec-number  { font-size: 20px; font-weight: 700; color: #58a6ff; font-variant-numeric: tabular-nums; }

/* ── Resource row ─────────────────────────────────────────────────────────── */
.res-row {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 8px;
}
.res-name { font-size: 15px; font-weight: 600; color: #e6edf3; }
.res-dist { font-size: 13px; color: #8b949e; margin-top: 2px; }

/* ── Weather strip ────────────────────────────────────────────────────────── */
.weather-strip {
    background: linear-gradient(135deg, #161b22 0%, #0d1f3c 100%);
    border: 1px solid #1f6feb44;
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 20px;
}
.weather-city {
    font-size: 22px;
    font-weight: 700;
    color: #e6edf3;
}
.weather-desc {
    font-size: 14px;
    color: #8b949e;
    margin-top: 2px;
}

/* ── Hero header ──────────────────────────────────────────────────────────── */
.hero {
    background: linear-gradient(135deg, #0d1f3c 0%, #161b22 60%, #1a0a0a 100%);
    border: 1px solid #21262d;
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 24px;
}
.hero h1 {
    font-size: 28px !important;
    font-weight: 700 !important;
    color: #e6edf3 !important;
    margin: 0 0 6px 0 !important;
}
.hero p {
    font-size: 14px;
    color: #8b949e;
    margin: 0;
}

/* ── Status dot ───────────────────────────────────────────────────────────── */
.dot-live { width:8px; height:8px; background:#3fb950; border-radius:50%; display:inline-block; margin-right:6px; animation: pulse 2s infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.4} }

/* ── Checkboxes ───────────────────────────────────────────────────────────── */
[data-testid="stCheckbox"] label {
    color: #c9d1d9 !important;
    font-size: 14px !important;
}

/* ── Audio player ─────────────────────────────────────────────────────────── */
audio { border-radius: 8px; width: 100%; }

/* ── Scrollbar ────────────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0d1117; }
::-webkit-scrollbar-thumb { background: #30363d; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #484f58; }
</style>
"""


def inject_css():
    import streamlit as st
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def card(title: str, value: str, sub: str = "") -> str:
    sub_html = f'<div class="ds-card-sub">{sub}</div>' if sub else ""
    return f"""
<div class="ds-card">
  <div class="ds-card-title">{title}</div>
  <div class="ds-card-value">{value}</div>
  {sub_html}
</div>"""


def risk_badge(level: str) -> str:
    cls = {"Low": "badge-low", "Moderate": "badge-moderate",
           "High": "badge-high", "Critical": "badge-critical"}.get(level, "badge-low")
    return f'<span class="{cls}">{level}</span>'


def weather_strip(weather: dict) -> str:
    return f"""
<div class="weather-strip">
  <div class="weather-city">📍 {weather['city']}, {weather['country']}</div>
  <div class="weather-desc"><span class="dot-live"></span>Live · {weather['description']}</div>
</div>"""


def ec_card(service: str, number: str) -> str:
    return f"""
<div class="ec-card">
  <span class="ec-service">{service}</span>
  <span class="ec-number">{number}</span>
</div>"""


def res_row(name: str, dist_km: float, extra: str = "") -> str:
    extra_html = f"<span style='color:#8b949e;font-size:12px;margin-left:12px;'>{extra}</span>" if extra else ""
    return f"""
<div class="res-row">
  <div class="res-name">{name}</div>
  <div class="res-dist">📍 {dist_km} km away {extra_html}</div>
</div>"""
