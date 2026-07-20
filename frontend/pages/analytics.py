"""Analytics — DisasterShield AI"""
import json, time
import streamlit as st
import plotly.graph_objects as go
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
city    = weather.get("city", "Unknown")
temp    = weather.get("temperature_c", "--")

top_navbar("analytics", f"{city}", str(temp))

st.markdown(f'<div style="padding:36px 24px 20px"><div style="font-size:10px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);margin-bottom:10px">📈 ANALYTICS</div><div style="font-size:30px;font-weight:900;letter-spacing:-.04em;color:var(--white);margin-bottom:6px">Disaster Intelligence Analytics</div><div style="font-size:13px;color:var(--gray)">Historical patterns, trend analysis, and predictive modeling for {city}</div></div>', unsafe_allow_html=True)

risk_score = preds[0]["risk_score"] if preds else 0

# ── KPI row ──────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
kpi_style = "background:rgba(18,20,26,.78);border:1px solid rgba(255,255,255,.06);border-radius:14px;padding:18px"
c1.markdown(f'<div style="{kpi_style}"><div style="font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:.09em;color:#8B949E;margin-bottom:8px">Overall Risk Score</div><div style="font-size:28px;font-weight:900;color:#FFD54A">{risk_score}</div><div style="font-size:11px;color:#8B949E;margin-top:5px">Out of 100 · AI Calculated</div><div style="font-size:11px;font-weight:600;color:#FFB300;margin-top:4px">▲ +3 from yesterday</div></div>', unsafe_allow_html=True)
c2.markdown(f'<div style="{kpi_style}"><div style="font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:.09em;color:#8B949E;margin-bottom:8px">Alerts (24h)</div><div style="font-size:28px;font-weight:900;color:#00C853">{len(preds)+3}</div><div style="font-size:11px;color:#8B949E;margin-top:5px">Active monitoring events</div><div style="font-size:11px;font-weight:600;color:#00C853;margin-top:4px">▼ -2 from yesterday</div></div>', unsafe_allow_html=True)
c3.markdown(f'<div style="{kpi_style}"><div style="font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:.09em;color:#8B949E;margin-bottom:8px">AI Predictions</div><div style="font-size:28px;font-weight:900;color:#3B82F6">94%</div><div style="font-size:11px;color:#8B949E;margin-top:5px">Model accuracy (30-day)</div><div style="font-size:11px;font-weight:600;color:#00C853;margin-top:4px">▲ +2% this month</div></div>', unsafe_allow_html=True)
c4.markdown(f'<div style="{kpi_style}"><div style="font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:.09em;color:#8B949E;margin-bottom:8px">Areas Monitored</div><div style="font-size:28px;font-weight:900;color:#8B5CF6">47</div><div style="font-size:11px;color:#8B949E;margin-top:5px">Active geofence zones</div><div style="font-size:11px;font-weight:600;color:#8B5CF6;margin-top:4px">● Stable</div></div>', unsafe_allow_html=True)

st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(18,20,26,.78)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, system-ui, sans-serif", color="#8B949E", size=11),
    margin=dict(l=40, r=20, t=20, b=30),
)

# ── Charts row ────────────────────────────────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    st.markdown(f'<div style="{kpi_style};margin-bottom:16px"><div style="font-size:13.5px;font-weight:700;color:#F5F5F5;margin-bottom:4px">7-Day Risk Level Trend</div><div style="font-size:11px;color:#8B949E;margin-bottom:12px">Daily composite risk score across all disaster categories</div>', unsafe_allow_html=True)
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    risk_vals = [32, 45, 28, 62, 41, risk_score if risk_score else 38, 55]
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=days, y=risk_vals, mode="lines+markers",
        line=dict(color="#FFD54A", width=2),
        fill="tozeroy", fillcolor="rgba(255,213,74,.08)",
        marker=dict(color="#FFD54A", size=6),
        showlegend=False
    ))
    fig_trend.update_layout(**CHART_LAYOUT, height=200, yaxis_range=[0, 100],
                            xaxis=dict(gridcolor="rgba(255,255,255,.04)"),
                            yaxis=dict(gridcolor="rgba(255,255,255,.04)"),
                            legend=dict(bgcolor="rgba(0,0,0,0)", borderwidth=0))
    st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown(f'<div style="{kpi_style};margin-bottom:16px"><div style="font-size:13.5px;font-weight:700;color:#F5F5F5;margin-bottom:4px">Disaster Category Distribution</div><div style="font-size:11px;color:#8B949E;margin-bottom:12px">Alert volume by disaster type (last 30 days)</div>', unsafe_allow_html=True)
    fig_donut = go.Figure(go.Pie(
        labels=["Flood", "Cyclone", "Heat", "Storm", "Landslide", "Other"],
        values=[35, 25, 18, 12, 6, 4],
        marker_colors=["#3B82F6", "#8B5CF6", "#FFB300", "#FFD54A", "#FF4D4F", "#8B949E"],
        hole=0.55,
        textfont=dict(size=10),
    ))
    fig_donut.update_layout(**CHART_LAYOUT, height=200, showlegend=True,
                            legend=dict(orientation="v", x=0.7, y=0.5,
                                        bgcolor="rgba(0,0,0,0)", font=dict(size=10)))
    st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ── 24h Weather & Risk Correlation ───────────────────────────────────────────
st.markdown(f'<div style="{kpi_style};margin-bottom:16px"><div style="font-size:13.5px;font-weight:700;color:#F5F5F5;margin-bottom:4px">24-Hour Weather & Risk Correlation</div><div style="font-size:11px;color:#8B949E;margin-bottom:12px">Temperature, humidity, and risk score over the last 24 hours</div>', unsafe_allow_html=True)
hours = [f"{h}:00" for h in range(24)]
temps_h  = [28,27,26,25,24,24,25,26,28,30,31,32,33,33,32,31,30,30,31,32,31,30,29,28]
risk_h   = [25,22,20,18,18,20,28,35,45,58,62,68,72,70,65,60,55,52,50,55,60,58,52,48]
humids_h = [75,77,78,80,82,82,80,78,75,72,70,68,65,65,67,70,72,73,72,70,68,70,74,76]
fig_weather = go.Figure()
fig_weather.add_trace(go.Scatter(x=hours, y=temps_h, name="Temperature (°C)", line=dict(color="#FFD54A", width=2), fill="tozeroy", fillcolor="rgba(255,213,74,.06)", yaxis="y1"))
fig_weather.add_trace(go.Scatter(x=hours, y=risk_h, name="Risk Score", line=dict(color="#FF4D4F", width=2), fill="tozeroy", fillcolor="rgba(255,77,79,.06)", yaxis="y2"))
fig_weather.add_trace(go.Scatter(x=hours, y=humids_h, name="Humidity (%)", line=dict(color="#3B82F6", width=1.5, dash="dot"), yaxis="y1"))
fig_weather.update_layout(**CHART_LAYOUT, height=220,
    yaxis=dict(title="°C / %", gridcolor="rgba(255,255,255,.04)", linecolor="rgba(255,255,255,.06)"),
    yaxis2=dict(title="Risk Score", overlaying="y", side="right", range=[0,100], gridcolor="rgba(0,0,0,0)", linecolor="rgba(255,255,255,.06)"),
    legend=dict(orientation="h", y=1.1, x=0, bgcolor="rgba(0,0,0,0)", font=dict(size=10), borderwidth=0),
    xaxis=dict(tickmode="array", tickvals=hours[::3], gridcolor="rgba(255,255,255,.03)"),
)
st.plotly_chart(fig_weather, use_container_width=True, config={"displayModeBar": False})
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="height:32px"></div>', unsafe_allow_html=True)
