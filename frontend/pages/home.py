"""DisasterShield AI — Dashboard (Home)"""
import json, time
import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
from frontend.design.premium_css import inject, top_navbar, metric_widgets, trigger_push_alerts
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
country = weather.get("country", "")
temp_c  = weather.get("temperature_c", "--")
feels   = weather.get("feels_like_c",  "--")
desc    = weather.get("description",   "Clear")
hum     = weather.get("humidity_pct",  "--")
wind    = weather.get("wind_kmh") or "--"

top_risk    = preds[0] if preds else None
risk_lvl    = top_risk["risk_level"]          if top_risk else "Low"
risk_sc     = top_risk["risk_score"]          if top_risk else 0
risk_reason = top_risk["reason"]              if top_risk else "All systems nominal."
risk_action = top_risk["recommended_action"]  if top_risk else "Continue monitoring."

rc = {"Low":"#00C853","Moderate":"#FFB300","High":"#FF4D4F","Critical":"#8B5CF6"}
risk_color = rc.get(risk_lvl, "#00C853")
city_full  = f"{city}, {country}" if country else city
ts         = time.strftime("%H:%M")
date_str   = time.strftime("%a %d %b %Y")

top_navbar("dashboard", city_full, str(temp_c))
trigger_push_alerts(preds)

# ── Hero ──────────────────────────────────────────────────────────────────────
alert_rows = ""
sev_map = {
    "Low":      ("#00C853", "rgba(0,200,83,.12)",  "LOW"),
    "Moderate": ("#FFB300", "rgba(255,179,0,.12)", "MOD"),
    "High":     ("#FF4D4F", "rgba(255,77,79,.12)", "HIGH"),
    "Critical": ("#8B5CF6", "rgba(139,92,246,.12)","CRIT"),
}
dis_icons = {"Flood":"🌊","Cyclone":"🌀","Thunderstorm":"⚡","Heatwave":"🌡",
             "Heavy Rain":"🌧","Landslide":"⛰","Drought":"☀","Wildfire":"🔥"}
for p in (preds or [{"disaster":"Monitoring","risk_level":"Low","risk_score":0}])[:3]:
    col2, bg2, lbl = sev_map.get(p["risk_level"], ("#00C853","rgba(0,200,83,.12)","LOW"))
    ico = dis_icons.get(p["disaster"], "⚠")
    alert_rows += f"""
<div style="display:flex;align-items:center;gap:9px;padding:9px 0;
  border-bottom:1px solid rgba(255,255,255,.05)">
  <div style="width:28px;height:28px;border-radius:8px;background:{bg2};
    display:flex;align-items:center;justify-content:center;font-size:13px">{ico}</div>
  <div style="flex:1">
    <div style="font-size:12px;font-weight:600;color:#F5F5F5">{p["disaster"]}</div>
    <div style="font-size:10px;color:#8B949E;margin-top:1px">{city_full}</div>
  </div>
  <div style="font-size:9px;font-weight:700;padding:2px 7px;border-radius:99px;
    background:{bg2};color:{col2};letter-spacing:.05em">{lbl}</div>
</div>"""

hero_html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
*{{margin:0;padding:0;box-sizing:border-box;font-family:'Inter',system-ui,sans-serif}}
body{{background:#050505;overflow:hidden;height:580px}}
.hero{{position:relative;height:580px;display:flex;align-items:center;overflow:hidden}}
canvas#earth{{position:absolute;right:0;top:0;width:100%;height:100%;opacity:.9}}
.hero-content{{position:relative;z-index:10;padding:0 60px;max-width:560px}}
.eyebrow{{
  display:inline-flex;align-items:center;gap:7px;padding:5px 12px;
  background:rgba(255,213,74,.08);border:1px solid rgba(255,213,74,.2);
  border-radius:99px;margin-bottom:20px;
}}
.eyebrow-dot{{width:6px;height:6px;border-radius:50%;background:#FFD54A;
  animation:pulse 1.8s ease infinite}}
.eyebrow-text{{font-size:10.5px;font-weight:700;letter-spacing:.12em;
  text-transform:uppercase;color:#D4AF37}}
h1{{font-size:52px;font-weight:900;line-height:1.0;letter-spacing:-.04em;
  color:#F5F5F5;margin-bottom:10px}}
h1 em{{font-style:normal;
  background:linear-gradient(90deg,#FFD54A 0%,#D4AF37 60%,#A08020 100%);
  -webkit-background-clip:text;background-clip:text;color:transparent}}
.hero-desc{{font-size:14.5px;color:#8B949E;line-height:1.7;margin-bottom:28px;max-width:420px}}
.cta-row{{display:flex;flex-wrap:wrap;gap:10px}}
.btn-primary{{
  display:inline-flex;align-items:center;gap:8px;padding:13px 24px;
  border-radius:12px;font-size:13.5px;font-weight:700;letter-spacing:-.01em;
  background:linear-gradient(135deg,#FFD54A,#D4AF37);color:#050505;
  box-shadow:0 0 30px rgba(255,213,74,.3);cursor:pointer;border:none;
  transition:all .2s;text-decoration:none;
}}
.btn-primary:hover{{transform:translateY(-2px);box-shadow:0 0 40px rgba(255,213,74,.45)}}
.btn-danger{{
  display:inline-flex;align-items:center;gap:8px;padding:13px 24px;
  border-radius:12px;font-size:13.5px;font-weight:700;
  background:rgba(255,77,79,.1);color:#FF4D4F;
  border:1px solid rgba(255,77,79,.3);cursor:pointer;
  transition:all .2s;text-decoration:none;
}}
.btn-danger:hover{{background:rgba(255,77,79,.18);transform:translateY(-2px)}}
.btn-ghost{{
  display:inline-flex;align-items:center;gap:8px;padding:13px 22px;
  border-radius:12px;font-size:13.5px;font-weight:600;
  background:rgba(255,255,255,.05);color:#8B949E;
  border:1px solid rgba(255,255,255,.08);cursor:pointer;
  transition:all .2s;text-decoration:none;
}}
.btn-ghost:hover{{color:#F5F5F5;background:rgba(255,255,255,.08);transform:translateY(-2px)}}
.alert-panel{{
  position:absolute;right:56px;top:50%;transform:translateY(-50%);
  width:260px;z-index:15;
  background:rgba(11,13,16,.92);backdrop-filter:blur(24px);
  border:1px solid rgba(255,213,74,.12);border-radius:20px;
  padding:16px;
  box-shadow:0 24px 60px rgba(0,0,0,.7);
  animation:float 5s ease-in-out infinite;
}}
@keyframes float{{0%,100%{{transform:translateY(-50%)}}50%{{transform:translateY(calc(-50% - 10px))}}}}
.ap-head{{display:flex;align-items:center;gap:7px;margin-bottom:12px;
  font-size:10.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#FFD54A}}
.ap-dot{{width:7px;height:7px;border-radius:50%;background:#FF4D4F;
  animation:pulse 1.2s ease infinite}}
.risk-pill{{
  position:absolute;top:24px;right:340px;z-index:20;
  display:flex;align-items:center;gap:7px;
  background:rgba(5,5,5,.85);border:1px solid {risk_color}44;
  border-radius:99px;padding:7px 14px;
  box-shadow:0 0 20px {risk_color}22;
}}
.risk-dot{{width:7px;height:7px;border-radius:50%;background:{risk_color};
  animation:pulse 2s ease infinite}}
.risk-label{{font-size:11px;font-weight:700;letter-spacing:.06em;
  text-transform:uppercase;color:{risk_color}}}
.status-row{{
  display:flex;gap:20px;margin-top:24px;padding-top:20px;
  border-top:1px solid rgba(255,255,255,.06)
}}
.stat-val{{font-size:18px;font-weight:800;color:#F5F5F5;letter-spacing:-.03em}}
.stat-lbl{{font-size:10px;color:#8B949E;margin-top:2px;text-transform:uppercase;
  letter-spacing:.07em;font-weight:600}}
@keyframes pulse{{0%,100%{{opacity:1;transform:scale(1)}}50%{{opacity:.3;transform:scale(1.5)}}}}
@keyframes fadeUp{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:translateY(0)}}}}
.hero-content > *{{animation:fadeUp .5s ease both}}
.hero-content > *:nth-child(1){{animation-delay:.0s}}
.hero-content > *:nth-child(2){{animation-delay:.08s}}
.hero-content > *:nth-child(3){{animation-delay:.16s}}
.hero-content > *:nth-child(4){{animation-delay:.24s}}
.hero-content > *:nth-child(5){{animation-delay:.32s}}
</style></head><body>
<div class="hero">
  <canvas id="earth"></canvas>
  <div class="hero-content">
    <div class="eyebrow">
      <div class="eyebrow-dot"></div>
      <div class="eyebrow-text">Live AI Monitoring · {city_full}</div>
    </div>
    <h1>AI Powered<br><em>Disaster Intelligence</em></h1>
    <p class="hero-desc">
      Real-time disaster monitoring, AI-driven early warning,
      and emergency response coordination — all in one platform.
    </p>
    <div class="cta-row">
      <a href="assistant" data-navigate="assistant" class="btn-primary">
        ⚡ Launch AI Assistant
      </a>
      <a href="emergency" data-navigate="emergency" class="btn-danger">
        🆘 Emergency SOS
      </a>
      <a href="risk" data-navigate="risk" class="btn-ghost">
        📊 Risk Monitor
      </a>
    </div>
    <div class="status-row">
      <div class="stat">
        <div class="stat-val">{temp_c}°C</div>
        <div class="stat-lbl">Temperature</div>
      </div>
      <div class="stat">
        <div class="stat-val" style="color:{risk_color}">{risk_lvl}</div>
        <div class="stat-lbl">Risk Level</div>
      </div>
      <div class="stat">
        <div class="stat-val">{ts}</div>
        <div class="stat-lbl">Local Time</div>
      </div>
      <div class="stat">
        <div class="stat-val">{hum}%</div>
        <div class="stat-lbl">Humidity</div>
      </div>
    </div>
  </div>

  <div class="risk-pill">
    <div class="risk-dot"></div>
    <div class="risk-label">{risk_lvl} Risk · {risk_sc}/100</div>
  </div>

  <div class="alert-panel">
    <div class="ap-head"><div class="ap-dot"></div>Live Active Alerts</div>
    {alert_rows}
  </div>
</div>

<script>
(function(){{
  const C = document.getElementById('earth');
  const ctx = C.getContext('2d');
  let W, H, CX, CY, R, tick = 0;

  function resize() {{
    W = C.width  = C.offsetWidth;
    H = C.height = C.offsetHeight;
    CX = W * .62; CY = H * .48; R = Math.min(W, H) * .38;
  }}
  resize();
  window.addEventListener('resize', resize);

  const rng = s => {{ let x = (s * 1234567) >>> 0; x = (x ^ x << 13) >>> 0; x = (x ^ x >> 7) >>> 0; return (x % 10000) / 10000; }};

  const lights = Array.from({{length:220}}, (_,i) => ({{
    lat: (rng(i*3)-.2)*160, lng: rng(i*3+1)*360-180,
    b: rng(i*3+2), sz: rng(i*3+3)
  }}));

  const hubs = [
    {{lat:13.08,lng:80.27}},{{lat:28.6,lng:77.2}},{{lat:19.1,lng:72.9}},
    {{lat:51.5,lng:-0.1}},{{lat:40.7,lng:-74}},{{lat:35.7,lng:139.7}},
    {{lat:-33.9,lng:151.2}},{{lat:48.9,lng:2.3}},
  ];

  function ll3d(lat, lng) {{
    const phi = (90 - lat) * Math.PI / 180;
    const th  = (lng + 180) * Math.PI / 180;
    return {{ x: Math.sin(phi)*Math.cos(th), y: Math.cos(phi), z: Math.sin(phi)*Math.sin(th) }};
  }}

  function project(p, rotY) {{
    const c = Math.cos(rotY), s = Math.sin(rotY);
    return {{ sx: CX+(p.x*c-p.z*s)*R, sy: CY-p.y*R, z: p.x*s+p.z*c }};
  }}

  let rotY = .3;

  function draw() {{
    ctx.clearRect(0, 0, W, H);
    const ga = ctx.createRadialGradient(CX,CY,R*.3,CX,CY,R*1.6);
    ga.addColorStop(0,'rgba(255,213,74,.04)');ga.addColorStop(.6,'rgba(18,20,26,.02)');ga.addColorStop(1,'transparent');
    ctx.fillStyle=ga; ctx.fillRect(0,0,W,H);

    ctx.save(); ctx.beginPath(); ctx.arc(CX,CY,R,0,Math.PI*2); ctx.clip();
    const gb=ctx.createRadialGradient(CX-R*.3,CY-R*.3,R*.1,CX,CY,R);
    gb.addColorStop(0,'#1a2035');gb.addColorStop(.5,'#0d1525');gb.addColorStop(.85,'#040810');gb.addColorStop(1,'#020408');
    ctx.fillStyle=gb; ctx.fillRect(CX-R-2,CY-R-2,R*2+4,R*2+4);

    ctx.strokeStyle='rgba(255,213,74,.055)'; ctx.lineWidth=.6;
    for(let la=-60;la<=60;la+=30){{ctx.beginPath();let f=true;for(let ln=0;ln<=360;ln+=3){{const p=project(ll3d(la,ln-180+rotY*180/Math.PI),0);if(p.z<0){{f=true;continue;}}f?ctx.moveTo(p.sx,p.sy):ctx.lineTo(p.sx,p.sy);f=false;}}ctx.stroke();}}
    for(let ln=0;ln<360;ln+=30){{ctx.beginPath();let f=true;for(let la=-80;la<=80;la+=3){{const p=project(ll3d(la,ln-180+rotY*180/Math.PI),0);if(p.z<0){{f=true;continue;}}f?ctx.moveTo(p.sx,p.sy):ctx.lineTo(p.sx,p.sy);f=false;}}ctx.stroke();}}

    for(const l of lights){{const p=project(ll3d(l.lat,l.lng+rotY*180/Math.PI),0);if(p.z<0)continue;const sz=.7+l.sz*2,al=.35+l.b*.6;ctx.beginPath();ctx.arc(p.sx,p.sy,sz,0,Math.PI*2);ctx.fillStyle=`rgba(255,${{Math.floor(185+l.b*70)}},${{Math.floor(l.b*60)}},${{al}})`;ctx.fill();}}

    const visible=hubs.map(h=>project(ll3d(h.lat,h.lng+rotY*180/Math.PI),0)).filter(p=>p.z>0);
    ctx.strokeStyle='rgba(255,213,74,.22)';ctx.lineWidth=.8;ctx.setLineDash([3,5]);
    for(let i=0;i<visible.length;i++)for(let j=i+1;j<visible.length;j++){{ctx.beginPath();ctx.moveTo(visible[i].sx,visible[i].sy);ctx.lineTo(visible[j].sx,visible[j].sy);ctx.stroke();}}
    ctx.setLineDash([]);

    for(let i=0;i<hubs.length;i++){{const p=project(ll3d(hubs[i].lat,hubs[i].lng+rotY*180/Math.PI),0);if(p.z<0)continue;const t=tick*.02,phase=(t-i*.3)%1.2;if(phase>0&&phase<1){{ctx.beginPath();ctx.arc(p.sx,p.sy,phase*18,0,Math.PI*2);ctx.strokeStyle=`rgba(255,213,74,${{(1-phase)*.4}})`;ctx.lineWidth=1;ctx.stroke();}}ctx.beginPath();ctx.arc(p.sx,p.sy,3,0,Math.PI*2);ctx.fillStyle=i===0?'#FF4D4F':'#FFD54A';ctx.fill();ctx.beginPath();ctx.arc(p.sx,p.sy,1.2,0,Math.PI*2);ctx.fillStyle='#fff';ctx.fill();}}

    const sweepAngle=(tick*.018)%(Math.PI*2);
    for(let ri=1;ri<=3;ri++){{const pr=(tick*.012-ri*.25)%1;if(pr>=0){{ctx.beginPath();ctx.arc(CX,CY,R*.12+R*pr*.6,0,Math.PI*2);ctx.strokeStyle=`rgba(255,77,79,${{(1-pr)*.3}})`;ctx.lineWidth=1;ctx.stroke();}}}}
    ctx.beginPath();ctx.moveTo(CX,CY);ctx.arc(CX,CY,R*.7,sweepAngle,sweepAngle+1.2);ctx.closePath();
    const grd=ctx.createRadialGradient(CX,CY,0,CX,CY,R*.7);grd.addColorStop(0,'rgba(255,213,74,.0)');grd.addColorStop(1,'rgba(255,213,74,.07)');ctx.fillStyle=grd;ctx.fill();
    ctx.restore();

    ctx.beginPath();ctx.arc(CX,CY,R,0,Math.PI*2);ctx.strokeStyle='rgba(255,213,74,.14)';ctx.lineWidth=1.2;ctx.stroke();
    const atm=ctx.createRadialGradient(CX,CY,R*.94,CX,CY,R*1.08);atm.addColorStop(0,'rgba(255,213,74,.08)');atm.addColorStop(1,'transparent');ctx.beginPath();ctx.arc(CX,CY,R*1.08,0,Math.PI*2);ctx.fillStyle=atm;ctx.fill();

    const sa=tick*.015+1;
    const sx=CX+R*1.28*Math.cos(sa),sy=CY+R*.52*Math.sin(sa)*.55-20;
    ctx.fillStyle='rgba(255,213,74,.9)';ctx.beginPath();ctx.arc(sx,sy,2.5,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='rgba(100,180,255,.55)';ctx.fillRect(sx-9,sy-1.5,6,3);ctx.fillRect(sx+3,sy-1.5,6,3);

    tick++; rotY+=.003;
    requestAnimationFrame(draw);
  }}
  draw();
}})();
</script>
</body></html>"""

components.html(hero_html, height=585, scrolling=False)

# ── Status Strip ──────────────────────────────────────────────────────────────
items = [
    ("📍", "Location",    city_full),
    ("⛅", "Weather",     f"{temp_c}°C · {desc}"),
    (f'<span style="color:{risk_color}">●</span>', "Risk Status",
     f'<span style="color:{risk_color};font-weight:600">{risk_lvl} · {risk_sc}/100</span>'),
    ("🕐", "Local Time",  f'{ts} <span style="font-size:9px;color:var(--success);font-weight:700;'
     f'padding:1px 6px;background:rgba(0,200,83,.1);border-radius:4px;margin-left:4px">LIVE</span>'),
    ("📅", "Date",        date_str),
    ("💨", "Wind",        f"{wind} km/h · {hum}% humidity"),
]
strip = ""
for ico, lbl, val in items:
    strip += f"""
<div style="flex:1;display:flex;align-items:center;gap:9px;padding:12px 20px;
  border-right:1px solid var(--border2)">
  <div style="font-size:15px;opacity:.7">{ico}</div>
  <div>
    <div style="font-size:9px;text-transform:uppercase;letter-spacing:.1em;
      color:var(--gray);font-weight:600;margin-bottom:2px">{lbl}</div>
    <div style="font-size:12px;font-weight:600;color:var(--white)">{val}</div>
  </div>
</div>"""

st.markdown(f"""
<div style="display:flex;background:rgba(11,13,16,.9);
  border-top:1px solid var(--border2);border-bottom:1px solid var(--border2);
  font-family:var(--font)">
  {strip}
</div>""", unsafe_allow_html=True)

# ── Analytics Strip ───────────────────────────────────────────────────────────
st.markdown("""
<div style="padding:24px 24px 4px;display:flex;align-items:center;justify-content:space-between">
  <div>
    <div style="font-size:15px;font-weight:700;color:var(--white);margin-bottom:3px">
      Live Weather &amp; Environmental Data
    </div>
    <div style="font-size:12px;color:var(--gray)">
      <span style="display:inline-block;width:7px;height:7px;border-radius:50%;
        background:var(--success);margin-right:5px;animation:pulse 1.5s ease infinite"></span>
      Real-time · Auto-refreshes every 5 minutes
    </div>
  </div>
  <div style="font-size:11px;color:var(--gold);font-weight:600;cursor:pointer"
       data-navigate="analytics">View Analytics →</div>
</div>""", unsafe_allow_html=True)
metric_widgets(weather)

# ── Live Map + Feed ───────────────────────────────────────────────────────────
st.markdown(f'<div style="padding:28px 24px 8px;display:flex;align-items:center;justify-content:space-between"><div><div style="font-size:15px;font-weight:700;color:var(--white);margin-bottom:3px">Live Threat Map</div><div style="font-size:12px;color:var(--gray)">Real-time disaster visualization · Plotly interactive map</div></div><a href="risk" data-navigate="risk" style="font-size:11px;color:var(--gold);font-weight:600;text-decoration:none">Full Risk Monitor →</a></div>', unsafe_allow_html=True)

map_col, feed_col = st.columns([3, 2])

with map_col:
    fig_map = go.Figure()
    # Risk zones as scatter circles
    zone_data = [
        (lat+0.1, lon-0.1, "🌊 Flood Risk Zone", "#3B82F6", 18),
        (lat-0.15, lon+0.2, "🌊 Flood Watch", "#3B82F6", 12),
        (lat+0.4, lon+1.2, "🌀 Cyclone Warning", "#8B5CF6", 35),
        (lat+0.05, lon+0.0, "🌡 Heat Island", "#FFB300", 25),
    ]
    for zlat, zlon, name, col, size in zone_data:
        fig_map.add_trace(go.Scattermapbox(lat=[zlat], lon=[zlon], mode="markers",
            marker=dict(size=size, color=col, opacity=0.35), name=name, hovertext=name, hoverinfo="text"))
    # POI markers
    poi = [
        (lat+0.05, lon+0.08, "🏠 Emergency Shelter", "#00C853", 14),
        (lat-0.03, lon+0.15, "🏠 Community Shelter", "#00C853", 14),
        (lat+0.02, lon-0.03, "🏥 Government Hospital", "#3B82F6", 14),
        (lat-0.04, lon+0.07, "🏥 Apollo Hospital", "#3B82F6", 14),
    ]
    for plat, plon, name, col, size in poi:
        fig_map.add_trace(go.Scattermapbox(lat=[plat], lon=[plon], mode="markers",
            marker=dict(size=size, color=col, opacity=0.9), name=name, hovertext=name, hoverinfo="text"))
    # User location
    fig_map.add_trace(go.Scattermapbox(lat=[lat], lon=[lon], mode="markers+text",
        marker=dict(size=16, color="#FFD54A"), text=["📍"], textposition="top center",
        name=f"📍 {city}", hovertext=f"📍 {city}", hoverinfo="text"))
    fig_map.update_layout(
        mapbox=dict(style="open-street-map", center=dict(lat=lat, lon=lon), zoom=8),
        paper_bgcolor="rgba(13,13,13,1)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0), height=420,
        legend=dict(bgcolor="rgba(11,13,16,.9)", font=dict(color="#8B949E", size=10),
                    bordercolor="rgba(255,255,255,.06)", borderwidth=1, x=0, y=0),
        font=dict(family="Inter, system-ui, sans-serif", color="#8B949E"),
    )
    st.plotly_chart(fig_map, use_container_width=True, config={"displayModeBar": False})

with feed_col:
    feed_html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box;font-family:'Inter',system-ui,sans-serif}}
body{{background:rgba(11,13,16,.98);color:#F5F5F5;height:420px;display:flex;flex-direction:column;overflow:hidden;border:1px solid rgba(255,255,255,.06);border-radius:12px}}
.feed-head{{padding:14px 16px;border-bottom:1px solid rgba(255,255,255,.06);flex-shrink:0;display:flex;align-items:center;justify-content:space-between}}
.feed-title{{font-size:13px;font-weight:700}}
.feed-live{{display:flex;align-items:center;gap:5px;font-size:10px;font-weight:600;color:#00C853}}
.dot{{width:5px;height:5px;border-radius:50%;background:#00C853;animation:pulse 1.5s ease infinite}}
@keyframes pulse{{0%,100%{{opacity:1;transform:scale(1)}}50%{{opacity:.3;transform:scale(1.6)}}}}
.feed-filter{{padding:8px;border-bottom:1px solid rgba(255,255,255,.05);flex-shrink:0;display:flex;gap:4px}}
.ff{{font-size:10.5px;font-weight:600;padding:4px 10px;border-radius:6px;cursor:pointer;color:#8B949E;transition:all .14s;border:none;background:none}}
.ff.active{{background:rgba(255,213,74,.1);color:#FFD54A}}
.feed-body{{flex:1;overflow-y:auto;padding:8px}}
.feed-body::-webkit-scrollbar{{width:3px}}
.feed-body::-webkit-scrollbar-thumb{{background:rgba(255,213,74,.15);border-radius:99px}}
.card{{padding:10px 12px;border-radius:10px;margin-bottom:6px;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.05);cursor:pointer;position:relative}}
.card:hover{{background:rgba(255,255,255,.055)}}
.cb{{position:absolute;left:0;top:0;bottom:0;width:3px;border-radius:2px}}
.ct{{font-size:12.5px;font-weight:600;color:#F5F5F5;margin-bottom:3px;padding-left:8px}}
.cd{{font-size:11px;color:#8B949E;line-height:1.4;padding-left:8px;margin-bottom:4px}}
.cm{{font-size:10px;color:#8B949E;padding-left:8px;display:flex;gap:8px;flex-wrap:wrap}}
.badge{{font-size:9px;font-weight:700;padding:2px 6px;border-radius:99px;text-transform:uppercase}}
</style></head><body>
<div class="feed-head"><div class="feed-title">📡 Live Disaster Feed</div><div class="feed-live"><div class="dot"></div>Live</div></div>
<div class="feed-filter">
  <button class="ff active" onclick="filter('all',this)">All</button>
  <button class="ff" style="color:#FF4D4F" onclick="filter('critical',this)">🔴 Critical</button>
  <button class="ff" style="color:#FFB300" onclick="filter('high',this)">🟡 High</button>
  <button class="ff" onclick="filter('info',this)">🟢 Info</button>
</div>
<div class="feed-body" id="fb"></div>
<script>
const A=[
  {{s:'critical',c:'#FF4D4F',i:'🌊',t:'Flash Flood Warning',l:'{city}',tm:'2 min ago',d:'Heavy rainfall causing rapid water rise. Evacuate immediately.'}},
  {{s:'high',c:'#FFB300',i:'🌀',t:'Cyclone Watch',l:'Bay of Bengal',tm:'18 min ago',d:'Cyclonic storm forming. Expected to reach land in 48 hours.'}},
  {{s:'high',c:'#FFB300',i:'⚡',t:'Severe Thunderstorm',l:'Coastal Zone',tm:'35 min ago',d:'Lightning and strong winds expected. Avoid open areas.'}},
  {{s:'moderate',c:'#8B5CF6',i:'🌡',t:'Heatwave Advisory',l:'{city}',tm:'1 hr ago',d:'Temperatures expected to reach 42°C. Stay hydrated.'}},
  {{s:'info',c:'#00C853',i:'☁️',t:'Cloud Formation Detected',l:'Arabian Sea',tm:'2 hr ago',d:'AI detected unusual cloud patterns. Monitoring.'}},
  {{s:'info',c:'#3B82F6',i:'🏛️',t:'Government Advisory',l:'Tamil Nadu',tm:'3 hr ago',d:'Orange alert for heavy rainfall in northern districts.'}},
];
let cf='all';
function render(){{const b=document.getElementById('fb');const list=cf==='all'?A:A.filter(a=>a.s===cf);b.innerHTML=list.map(a=>`<div class="card"><div class="cb" style="background:${{a.c}}"></div><div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:2px"><div class="ct">${{a.i}} ${{a.t}}</div><span class="badge" style="background:${{a.c}}22;color:${{a.c}}">${{a.s}}</span></div><div class="cd">${{a.d}}</div><div class="cm"><span>📍${{a.l}}</span><span>🕐${{a.tm}}</span></div></div>`).join('');}}
window.filter=function(f,el){{cf=f;document.querySelectorAll('.ff').forEach(t=>t.classList.remove('active'));el.classList.add('active');render();}};
render();
</script></body></html>"""
    components.html(feed_html, height=420, scrolling=False)

st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns([2,1,2])
with col2:
    if st.button("🔄 Refresh Live Data", use_container_width=True):
        _weather.clear(); _risks.clear()
        st.rerun()
st.markdown('<div style="height:32px"></div>', unsafe_allow_html=True)
