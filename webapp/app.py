import streamlit as st
import folium
from streamlit_folium import st_folium
from data import DAYS

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="京阪七天七夜",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700&display=swap');

html, body, [class*="css"] { font-family: 'Noto Sans TC', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.stApp { background-color: #FAFAF7; }

/* ── Container width ── */
.block-container {
    padding: 1.2rem 2.5rem 4rem !important;
    max-width: 1100px !important;
    margin: 0 auto !important;
}

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg, #4A9B8E 0%, #6BB5A8 55%, #8ECFC5 100%);
    border-radius: 18px;
    padding: 2.2rem 2.5rem;
    color: white;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: "✈";
    position: absolute;
    right: 2rem; top: 50%;
    transform: translateY(-50%);
    font-size: 6rem;
    opacity: 0.12;
    pointer-events: none;
}
.hero h1 { font-size: 2.2rem; font-weight: 700; margin: 0 0 0.3rem; letter-spacing: 0.04em; }
.hero p  { font-size: 1rem; margin: 0; opacity: 0.88; font-weight: 300; }
.hero .dates { font-size: 0.85rem; margin-top: 0.7rem; opacity: 0.72; font-weight: 300; }

/* ── Day nav pills spacing ── */
[data-testid="stPills"] { margin-bottom: 0.5rem; }
[data-testid="stPills"] button { font-size: 0.85rem !important; padding: 0.35rem 0.85rem !important; }

/* ── Day header ── */
.day-header {
    border-radius: 16px;
    padding: 1.6rem 2rem;
    color: white;
    margin: 1.2rem 0 1rem;
    position: relative;
    overflow: hidden;
}
.day-header .bg-icon {
    position: absolute;
    right: 1.5rem; bottom: -0.5rem;
    font-size: 4.5rem;
    opacity: 0.15;
    pointer-events: none;
}
.day-header .day-num { font-size: 0.78rem; font-weight: 300; opacity: 0.78; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 0.2rem; }
.day-header h2 { font-size: 1.8rem; font-weight: 700; margin: 0 0 0.2rem; }
.day-header .subtitle { font-size: 0.95rem; opacity: 0.85; font-weight: 300; }
.day-header .city-tag { display: inline-block; background: rgba(255,255,255,0.22); border-radius: 20px; padding: 0.18rem 0.75rem; font-size: 0.78rem; margin-top: 0.6rem; letter-spacing: 0.04em; }

/* ── Mood ── */
.mood-box {
    background: #F5F2EE;
    border-left: 3px solid #4A9B8E;
    border-radius: 0 10px 10px 0;
    padding: 1rem 1.3rem;
    margin-bottom: 1.4rem;
    color: #4A4A4A;
    font-size: 0.92rem;
    line-height: 1.8;
    font-style: italic;
    font-weight: 300;
}

/* ── Section title ── */
.section-title {
    font-size: 0.78rem;
    font-weight: 700;
    color: #4A9B8E;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    margin: 1.6rem 0 0.8rem;
    padding-bottom: 0.4rem;
    border-bottom: 2px solid #E5F0EE;
}

/* ── Overview cards ── */
.ov-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.7rem;
    margin-bottom: 1.4rem;
}
.ov-card {
    background: white;
    border-radius: 12px;
    padding: 0.8rem 0.9rem;
    box-shadow: 0 1px 5px rgba(0,0,0,0.05);
    border: 1px solid #EEEBE4;
}
.ov-card .lbl { font-size: 0.68rem; color: #AAA; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.22rem; }
.ov-card .val { font-size: 0.88rem; font-weight: 600; color: #333; line-height: 1.35; }

/* ── Timeline ── */
.timeline-wrap {
    position: relative;
    padding-left: 1.6rem;
    margin-top: 0.5rem;
}
.timeline-wrap::before {
    content: '';
    position: absolute;
    left: 0.48rem; top: 0; bottom: 0;
    width: 2px;
    background: linear-gradient(to bottom, #4A9B8E 0%, #D5D5D5 100%);
    border-radius: 2px;
}
.stop-card {
    background: white;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.65rem;
    box-shadow: 0 1px 6px rgba(0,0,0,0.06);
    border: 1px solid #EEEBE4;
    position: relative;
}
.stop-card::before {
    content: '';
    position: absolute;
    left: -1.28rem; top: 1.1rem;
    width: 11px; height: 11px;
    background: #4A9B8E;
    border-radius: 50%;
    border: 2px solid white;
    box-shadow: 0 0 0 2px #4A9B8E;
}
.stop-card.hotel::before { background: #9B7EA6; box-shadow: 0 0 0 2px #9B7EA6; }
.stop-card.food::before  { background: #C9A832; box-shadow: 0 0 0 2px #C9A832; }

.stop-time { font-size: 0.73rem; font-weight: 500; color: #4A9B8E; letter-spacing: 0.05em; margin-bottom: 0.25rem; }
.stop-name { font-size: 1rem; font-weight: 600; color: #222; margin-bottom: 0.3rem; }
.stop-badge { display: inline-block; font-size: 0.68rem; padding: 0.12rem 0.55rem; border-radius: 8px; font-weight: 500; margin-bottom: 0.45rem; }
.stop-desc { font-size: 0.87rem; color: #555; line-height: 1.65; margin-bottom: 0.3rem; }
.stop-mood { font-size: 0.82rem; color: #6A8A85; font-style: italic; font-weight: 300; line-height: 1.7; margin-top: 0.4rem; padding-left: 0.75rem; border-left: 2px solid #C5DDD9; }
.stop-tips { font-size: 0.78rem; color: #888; margin-top: 0.35rem; padding: 0.42rem 0.65rem; background: #F8F7F4; border-radius: 7px; }
.stop-green { font-size: 0.76rem; color: #5A8A6A; margin-top: 0.3rem; padding: 0.38rem 0.65rem; background: #F0F7F0; border-radius: 7px; }

/* ── Transport card ── */
.tr-card {
    display: flex;
    align-items: flex-start;
    gap: 0.7rem;
    background: #F2EFE8;
    border-radius: 9px;
    padding: 0.6rem 0.9rem;
    margin: 0.3rem 0 0.65rem;
    font-size: 0.8rem;
    color: #666;
    position: relative;
}
.tr-card::before {
    content: '';
    position: absolute;
    left: -1.28rem; top: 50%;
    width: 11px; height: 11px;
    transform: translateY(-50%);
    background: #C8C4BA;
    border-radius: 50%;
    border: 2px solid white;
    box-shadow: 0 0 0 2px #C8C4BA;
}
.tr-card .tr-icon { font-size: 1rem; flex-shrink: 0; margin-top: 0.05rem; }
.tr-card .tr-body { flex: 1; min-width: 0; }
.tr-card .tr-mode { font-weight: 600; color: #555; margin-bottom: 0.15rem; }
.tr-card .tr-detail { color: #777; font-size: 0.75rem; line-height: 1.5; word-break: break-word; }
.tr-card .tr-dur { color: #999; font-size: 0.72rem; margin-top: 0.1rem; }
.tr-card a {
    flex-shrink: 0;
    align-self: flex-start;
    background: #4A9B8E;
    color: white !important;
    padding: 0.28rem 0.8rem;
    border-radius: 16px;
    font-size: 0.72rem;
    text-decoration: none;
    font-weight: 500;
    white-space: nowrap;
    margin-left: auto;
}

/* ── Green footer ── */
.green-banner {
    background: linear-gradient(135deg, #E8F5E9, #F1F8F1);
    border: 1px solid #C8E6C9;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-top: 1.8rem;
    font-size: 0.85rem;
    color: #3A7A4A;
    line-height: 1.7;
}
.green-banner h4 { margin: 0 0 0.5rem; font-size: 0.88rem; font-weight: 600; color: #2E6B3A; }
.green-banner ul { margin: 0; padding-left: 1.1rem; }

/* ── RESPONSIVE ── */
@media (max-width: 768px) {
    .block-container { padding: 0.8rem 1rem 3rem !important; max-width: 100% !important; }
    .hero { padding: 1.4rem 1.5rem; border-radius: 14px; }
    .hero h1 { font-size: 1.5rem; }
    .hero p  { font-size: 0.88rem; }
    .hero::before { font-size: 4rem; right: 1rem; }
    .day-header { padding: 1.2rem 1.4rem; }
    .day-header h2 { font-size: 1.35rem; }
    .ov-grid { grid-template-columns: 1fr 1fr; }
    .ov-card .val { font-size: 0.82rem; }
    .stop-name { font-size: 0.94rem; }
    .tr-card { flex-wrap: wrap; }
    .tr-card a { margin-left: 0; margin-top: 0.4rem; }
    .mood-box { font-size: 0.88rem; }
}
@media (max-width: 480px) {
    .hero h1 { font-size: 1.3rem; }
    .ov-grid { grid-template-columns: 1fr 1fr; gap: 0.5rem; }
    .section-title { font-size: 0.72rem; }
    .stop-card { padding: 0.85rem 1rem; }
    .day-header h2 { font-size: 1.2rem; }
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────

TYPE_STYLE = {
    "古蹟文化": ("#8B6F47", "#FDF6EC"),
    "散步購物": ("#4A78C4", "#EEF3FC"),
    "餐飲":     ("#C97B2A", "#FEF6EA"),
    "午餐":     ("#C97B2A", "#FEF6EA"),
    "晚餐":     ("#C97B2A", "#FEF6EA"),
    "早餐":     ("#C97B2A", "#FEF6EA"),
    "體驗":     ("#7A5CC4", "#F3EFFE"),
    "住宿":     ("#9B7EA6", "#F5EFF8"),
    "交通":     ("#888",    "#F5F5F5"),
    "出發":     ("#4A9B8E", "#EBF6F5"),
    "抵達":     ("#4A9B8E", "#EBF6F5"),
}

CSS_CLASS = {
    "住宿": "hotel",
    "晚餐": "food", "午餐": "food", "早餐": "food", "餐飲": "food",
}

def gmap_url(origin, dest, mode="transit"):
    return (
        f"https://www.google.com/maps/dir/?api=1"
        f"&origin={origin[0]},{origin[1]}"
        f"&destination={dest[0]},{dest[1]}"
        f"&travelmode={mode}"
    )

def build_stop_html(stop):
    fg, bg = TYPE_STYLE.get(stop["type"], ("#555", "#EEE"))
    css_cls = CSS_CLASS.get(stop["type"], "")
    time_str = f"{stop['time']} — {stop['end']}" if stop.get("end") else stop["time"]

    badge  = f'<span class="stop-badge" style="background:{bg};color:{fg};">{stop["type"]}</span>'
    mood   = f'<div class="stop-mood">{stop["mood"]}</div>' if stop.get("mood") else ""
    tips   = f'<div class="stop-tips">💡 {stop["tips"]}</div>' if stop.get("tips") else ""
    green  = f'<div class="stop-green">🌿 {stop["green"]}</div>' if stop.get("green") else ""
    desc   = stop.get("desc", "")

    return (
        f'<div class="stop-card {css_cls}">'
        f'<div class="stop-time">{time_str}</div>'
        f'<div class="stop-name">{stop["icon"]} {stop["name"]}</div>'
        f'{badge}'
        f'<div class="stop-desc">{desc}</div>'
        f'{mood}{tips}{green}'
        f'</div>'
    )

def build_transport_html(tn):
    url    = gmap_url(tn["origin"], tn["dest"], tn.get("travelmode", "transit"))
    mode   = tn.get("mode", "")
    detail = tn.get("detail", "")
    dur    = tn.get("duration", "")
    return (
        f'<div class="tr-card">'
        f'<div class="tr-icon">🚃</div>'
        f'<div class="tr-body">'
        f'<div class="tr-mode">{mode}</div>'
        f'<div class="tr-detail">{detail}</div>'
        f'<div class="tr-dur">{dur}</div>'
        f'</div>'
        f'<a href="{url}" target="_blank">Google Maps →</a>'
        f'</div>'
    )

def build_timeline_html(stops):
    parts = ['<div class="timeline-wrap">']
    for stop in stops:
        parts.append(build_stop_html(stop))
        tn = stop.get("transport_next")
        if tn and not tn.get("walking"):
            parts.append(build_transport_html(tn))
    parts.append('</div>')
    return "".join(parts)

def build_map(stops, color):
    coords = [s["coord"] for s in stops if s.get("coord")]
    if not coords:
        return folium.Map(location=[35.0, 135.7], zoom_start=7, tiles="CartoDB Positron")
    cy = sum(c[0] for c in coords) / len(coords)
    cx = sum(c[1] for c in coords) / len(coords)
    m = folium.Map(location=[cy, cx], zoom_start=12, tiles="CartoDB Positron", prefer_canvas=True)

    if len(coords) > 1:
        folium.PolyLine(coords, color=color, weight=3, opacity=0.65, dash_array="6 4").add_to(m)

    for i, stop in enumerate(stops):
        if not stop.get("coord"):
            continue
        dot_color = color if i in (0, len(stops)-1) else (
            "#9B7EA6" if stop["type"] == "住宿" else "#4A9B8E"
        )
        icon_html = (
            f'<div style="width:28px;height:28px;background:{dot_color};'
            f'border:2px solid white;border-radius:50%;'
            f'display:flex;align-items:center;justify-content:center;'
            f'font-size:12px;box-shadow:0 2px 5px rgba(0,0,0,0.25);">'
            f'{stop["icon"]}</div>'
        )
        folium.Marker(
            location=stop["coord"],
            tooltip=f'{stop["time"]} {stop["name"]}',
            popup=folium.Popup(f'<b>{stop["name"]}</b><br>{stop["time"]}', max_width=180),
            icon=folium.DivIcon(html=icon_html, icon_size=(28, 28), icon_anchor=(14, 14)),
        ).add_to(m)

    lats = [c[0] for c in coords]
    lons = [c[1] for c in coords]
    m.fit_bounds([[min(lats), min(lons)], [max(lats), max(lons)]], padding=(25, 25))
    return m


# ── Session state ─────────────────────────────────────────────────────────────
if "selected_day" not in st.session_state:
    st.session_state.selected_day = 0


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="hero">'
    '<h1>京阪七天七夜</h1>'
    '<p>雙人自由行 · 購物 × 美食 × 文化 × 里山</p>'
    '<div class="dates">2026/06/20（六）— 2026/06/27（六）&nbsp;·&nbsp;TPE ⇄ KIX</div>'
    '</div>',
    unsafe_allow_html=True,
)

# ── Day navigation (pills) ────────────────────────────────────────────────────
NAV_LABELS = ["D0 啟程", "D1 宇治", "D2 東山", "D3 移城", "D4 USJ", "D5 難波", "D6 梅田", "D7 歸途"]

selected_label = st.pills(
    label="",
    options=NAV_LABELS,
    default=NAV_LABELS[st.session_state.selected_day],
    label_visibility="collapsed",
)
if selected_label:
    new_idx = NAV_LABELS.index(selected_label)
    if new_idx != st.session_state.selected_day:
        st.session_state.selected_day = new_idx
        st.rerun()

# ── Selected day ──────────────────────────────────────────────────────────────
day   = DAYS[st.session_state.selected_day]
color = day["color"]

# Day header
icon_char = day["stops"][1]["icon"] if len(day["stops"]) > 1 else "✈️"
st.markdown(
    f'<div class="day-header" style="background:linear-gradient(135deg,{color}EE,{color}88);">'
    f'<div class="bg-icon">{icon_char}</div>'
    f'<div class="day-num">Day {day["day"]} · {day["date"]}</div>'
    f'<h2>{day["theme"]}</h2>'
    f'<div class="subtitle">{day["subtitle"]}</div>'
    f'<span class="city-tag">📍 {day["city"]}</span>'
    f'</div>',
    unsafe_allow_html=True,
)

# Mood
if day.get("mood"):
    st.markdown(f'<div class="mood-box">{day["mood"]}</div>', unsafe_allow_html=True)

# ── Overview cards ────────────────────────────────────────────────────────────
stop_count = sum(1 for s in day["stops"] if s["type"] not in ("住宿", "交通"))
ov_items = [
    ("📅 日期", day["date"]),
    ("🏙️ 區域", day["city"]),
    ("📌 景點數", f"{stop_count} 個地點"),
    ("🏨 住宿", day["hotel"]),
]
cards_html = "".join(
    f'<div class="ov-card"><div class="lbl">{lbl}</div><div class="val">{val}</div></div>'
    for lbl, val in ov_items
)
st.markdown(
    f'<div class="section-title">今日快覽</div>'
    f'<div class="ov-grid">{cards_html}</div>',
    unsafe_allow_html=True,
)

# ── Map ───────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">今日路線地圖</div>', unsafe_allow_html=True)
m = build_map(day["stops"], color)
st_folium(m, height=420, use_container_width=True, returned_objects=[])

# ── Timeline (single HTML call) ───────────────────────────────────────────────
st.markdown('<div class="section-title">詳細行程</div>', unsafe_allow_html=True)
st.markdown(build_timeline_html(day["stops"]), unsafe_allow_html=True)

# ── Green footer ──────────────────────────────────────────────────────────────
green_stops = [s for s in day["stops"] if s.get("green")]
if green_stops:
    items = "".join(f"<li>{s['green']}</li>" for s in green_stops)
    st.markdown(
        f'<div class="green-banner">'
        f'<h4>🌱 今日輕旅行 · 行動提醒</h4>'
        f'<ul>{items}</ul>'
        f'</div>',
        unsafe_allow_html=True,
    )
