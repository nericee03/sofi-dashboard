import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="SOFI 2035 — Vietnam vs Philippines",
    layout="wide",
    initial_sidebar_state="expanded"
)

PBI_URL  = "https://app.powerbi.com/view?r=eyJrIjoiYzBlOGEwYTItOTIxZC00NGY1LTg3NjctNmNiOGJjYmY0NTcxIiwidCI6IjExMTNiZTM0LWFlZDEtNGQwMC1hYjRiLWNkZDAyNTEwYmU5MSIsImMiOjN9"

# ── Color palette from the attached image ─────────────────────────────────────
# platinum: #E8ECF0  smoke: #C8D6E5  light blue: #A8BFDA  cadet gray: #7A90A8  cool gray: #4F6480
C = {
    "platinum":  "#E8ECF0",   # page background
    "smoke":     "#C8D6E5",   # card borders, sidebar accent
    "lblue":     "#A8BFDA",   # section accents, active elements
    "cadet":     "#7A90A8",   # muted text, icons
    "coolgray":  "#4F6480",   # sidebar bg, dark elements
    "white":     "#FFFFFF",
    "text":      "#1E2A3A",   # primary text — very dark navy
    "subtext":   "#4F6480",   # secondary text — cool gray
    "muted":     "#7A90A8",   # cadet gray for placeholders
    "vn":        "#1E2A3A",   # Vietnam — darkest navy
    "ph":        "#4F6480",   # Philippines — cool gray
    "eco":       "#5B7FA6",   # light blue family
    "hlt":       "#7A9E87",   # muted green
    "env":       "#7A90A8",   # cadet gray
    "soc":       "#8E7FA8",   # muted purple
    "border":    "#C8D6E5",   # smoke
    "bg":        "#E8ECF0",   # platinum
    "grid":      "#F0F4F8",
    "card":      "#FFFFFF",
    "sidebar":   "#4F6480",   # cool gray sidebar
}

DOM_C    = {"Economic": C["eco"], "Health": C["hlt"], "Environment": C["env"], "Social": C["soc"]}
DOM_VN   = ["VN_Economic","VN_Health","VN_Environment","VN_Social"]
DOM_PH   = ["PH_Economic","PH_Health","PH_Environment","PH_Social"]
DOMAINS  = ["Economic","Health","Environment","Social"]

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* Remove slider container box */
[data-testid="stSidebar"] [data-testid="stSlider"] > div {{
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}}
            
*, html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
.main {{ background: {C["bg"]}; }}
.block-container {{ padding: 1.6rem 2rem 3rem; max-width: 1440px; }}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background: {C["coolgray"]};
    border-right: 1px solid {C["cadet"]};
}}
[data-testid="stSidebar"] * {{ color: {C["platinum"]} !important; }}
[data-testid="stSidebar"] .stSelectbox > div > div {{
    background: #3D5068 !important;
    border-color: {C["cadet"]} !important;
    color: {C["platinum"]} !important;
}}
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] {{
    background: {C["smoke"]};
}}

/* ── Top bar ── */
.top-bar {{
    background: {C["coolgray"]};
    border-radius: 14px;
    padding: 1.4rem 2rem;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 1rem;
}}
.top-title {{
    font-size: 1.45rem; font-weight: 800;
    color: {C["white"]}; margin: 0; letter-spacing: -0.02em;
}}
.top-sub {{
    font-size: 12px; color: {C["smoke"]}; margin-top: 4px;
}}
.top-tagline {{
    font-size: 12.5px; color: {C["lblue"]};
    margin-top: 3px; font-style: italic;
}}
.pbi-btn {{
    background: {C["lblue"]}; color: {C["text"]};
    border-radius: 8px; padding: 8px 18px;
    font-size: 13px; font-weight: 700;
    text-decoration: none; display: inline-block;
    margin-top: 6px;
}}
.pbi-btn:hover {{ background: {C["smoke"]}; }}

/* ── KPI row ── */
.kpi-row {{ display: grid; grid-template-columns: repeat(6,1fr); gap: 10px; margin-bottom: 0.6rem; }}
.kpi {{
    background: {C["white"]}; border: 1px solid {C["border"]};
    border-radius: 11px; padding: 13px 14px;
    position: relative; overflow: hidden;
    box-shadow: 0 1px 4px rgba(79,100,128,0.08);
    transition: box-shadow 0.2s;
}}
.kpi:hover {{ box-shadow: 0 4px 14px rgba(79,100,128,0.14); }}
.kpi::before {{
    content: ''; position: absolute;
    top: 0; left: 0; right: 0; height: 3px;
    background: {C["lblue"]};
}}
.kpi.ph::before {{ background: {C["cadet"]}; }}
.kpi.eco::before {{ background: {C["eco"]}; }}
.kpi.hlt::before {{ background: {C["hlt"]}; }}
.kpi.env::before {{ background: {C["env"]}; }}
.kpi.soc::before {{ background: {C["soc"]}; }}
.kpi-l {{ font-size: 10px; color: {C["muted"]}; font-weight: 600; text-transform: uppercase; letter-spacing: 0.07em; }}
.kpi-v {{ font-size: 1.4rem; font-weight: 800; color: {C["text"]}; font-family: 'JetBrains Mono', monospace; margin: 3px 0 1px; }}
.kpi-s {{ font-size: 11px; color: {C["subtext"]}; font-weight: 500; }}

/* ── Section headers ── */
.sh {{ font-size: 14px; font-weight: 700; color: {C["text"]}; margin: 0 0 2px; }}
.sd {{ font-size: 12px; color: {C["muted"]}; margin-bottom: 10px; }}

/* ── Note box ── */
.note {{
    background: {C["platinum"]}; border-left: 3px solid {C["lblue"]};
    border-radius: 0 8px 8px 0; padding: 11px 14px;
    font-size: 13px; color: {C["text"]}; line-height: 1.7;
    margin: 8px 0 14px;
}}

/* ── Info cards ── */
.info-card {{
    background: {C["white"]}; border: 1px solid {C["border"]};
    border-radius: 12px; padding: 1.1rem 1.3rem; height: 100%;
}}
.info-card h4 {{
    font-size: 13px; font-weight: 700; color: {C["text"]};
    margin: 0 0 8px; border-bottom: 1px solid {C["border"]};
    padding-bottom: 8px;
}}
.info-card ul {{
    margin: 0; padding-left: 15px;
    font-size: 12.5px; color: {C["subtext"]}; line-height: 1.85;
}}

/* ── Stat pills ── */
.stat-row {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 10px 0 16px; }}
.stat-pill {{
    background: {C["white"]}; border: 1px solid {C["border"]};
    border-radius: 8px; padding: 7px 14px;
}}
.sp-v {{ font-size: 1.15rem; font-weight: 800; color: {C["text"]}; font-family: 'JetBrains Mono', monospace; }}
.sp-l {{ font-size: 10px; color: {C["muted"]}; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; }}

/* ── PBI page cards ── */
.pg-card {{
    background: {C["white"]}; border: 1px solid {C["border"]};
    border-radius: 10px; padding: 12px 14px; height: 100%;
    border-top: 3px solid {C["lblue"]};
}}
.pg-num {{ font-size: 10px; color: {C["muted"]}; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 4px; }}
.pg-title {{ font-size: 13px; font-weight: 700; color: {C["text"]}; margin-bottom: 5px; }}
.pg-desc {{ font-size: 12px; color: {C["subtext"]}; line-height: 1.55; }}

/* ── PBI embed wrapper ── */
.pbi-wrap {{
    background: {C["white"]}; border: 1px solid {C["border"]};
    border-radius: 14px; overflow: hidden;
    box-shadow: 0 2px 10px rgba(79,100,128,0.08);
}}
.pbi-hdr {{
    background: {C["coolgray"]}; padding: 11px 18px;
    display: flex; align-items: center; justify-content: space-between;
}}
.pbi-hdr-t {{ color: {C["white"]}; font-weight: 700; font-size: 13px; }}

/* ── Reset button ── */
.reset-btn {{
    display: inline-block; background: {C["platinum"]};
    border: 1px solid {C["border"]}; border-radius: 7px;
    padding: 6px 14px; font-size: 12px; font-weight: 600;
    color: {C["subtext"]}; cursor: pointer; text-decoration: none;
}}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {{
    gap: 0; background: {C["white"]}; border-radius: 10px;
    padding: 5px; border: 1px solid {C["border"]};
    box-shadow: 0 1px 4px rgba(79,100,128,0.06);
    margin-bottom: 1.3rem;
}}
.stTabs [data-baseweb="tab"] {{
    background: transparent; border: none; border-radius: 7px;
    color: {C["muted"]}; font-size: 13px; font-weight: 600;
    padding: 7px 18px;
}}
.stTabs [aria-selected="true"] {{
    background: {C["coolgray"]} !important;
    color: {C["white"]} !important;
}}

hr {{ border-color: {C["border"]}; margin: 1.1rem 0; }}
::-webkit-scrollbar {{ width: 5px; height: 5px; }}
::-webkit-scrollbar-track {{ background: {C["bg"]}; }}
::-webkit-scrollbar-thumb {{ background: {C["smoke"]}; border-radius: 3px; }}
</style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load():
    sofi  = pd.read_csv("data/final_sofi_scores.csv")
    long_ = pd.read_csv("data/final_master_long.csv")
    summ  = pd.read_csv("data/final_indicator_summary.csv")
    xl = pd.read_excel("data/SOFI_final_v5.xlsx", sheet_name="SOFI")
    xl = xl[xl["Year"].apply(lambda x: str(x).strip().isdigit() if pd.notna(x) else False)].copy()
    xl["Year"] = xl["Year"].astype(int)
    xl.columns = [str(c).strip() for c in xl.columns]
    xl = xl.rename(columns={
        "Vietnam SOFI":"VN_SOFI","Philippines SOFI":"PH_SOFI",
        "VN Economic":"VN_Economic","VN Health":"VN_Health",
        "VN Environment":"VN_Environment","VN Social":"VN_Social",
        "PH Economic":"PH_Economic","PH Health":"PH_Health",
        "PH Environment":"PH_Environment","PH Social":"PH_Social",
        "Gap (VN–PH)":"Gap","Leader":"Leader"
    })
    for c in ["VN_SOFI","PH_SOFI","VN_Economic","VN_Health","VN_Environment","VN_Social",
              "PH_Economic","PH_Health","PH_Environment","PH_Social","Gap"]:
        xl[c] = pd.to_numeric(xl[c], errors="coerce")
    xl["Period"] = xl["Year"].apply(lambda y: "Historical" if y<=2023 else "Projected")
    return sofi, long_, summ, xl

sofi_csv, long_df, summ_df, xl = load()
xl_hist      = xl[xl["Year"]<=2023].copy()
years_hist   = sorted(xl_hist["Year"].unique())
indicators_all = sorted(long_df["SOFI_Name"].dropna().unique())

if "indicator" not in st.session_state:
    st.session_state["indicator"] = "Select an indicator"

if "domain" not in st.session_state:
    st.session_state["domain"] = "Select a domain"

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style='padding:1rem 0 1rem;border-bottom:1px solid {C["cadet"]};margin-bottom:1rem;'>
      <div style='font-size:1.05rem;font-weight:800;color:{C["white"]};'>SOFI 2035</div>
      <div style='font-size:11px;color:{C["smoke"]};margin-top:2px;'>State of Future Index</div>
      <div style='font-size:11px;color:{C["smoke"]};'>Vietnam vs Philippines</div>
    </div>

    <div style='font-size:10px;color:{C["cadet"]};font-weight:700;text-transform:uppercase;
      letter-spacing:0.07em;margin-bottom:4px;'>CLIENT:</div>
    <div style='font-size:12px;color:{C["smoke"]};margin-bottom:12px;line-height:1.7;'>
      Elizabeth Florescu<br>~The Millennium Project
    </div>

    <div style='font-size:10px;color:{C["cadet"]};font-weight:700;text-transform:uppercase;
      letter-spacing:0.07em;margin-bottom:4px;'>TEAM D:</div>
    <div style='font-size:12px;color:{C["smoke"]};line-height:1.75;margin-bottom:4px;'>
      Nerice Rodrigues<br>Rachana Dharani<br>Tanvica Samudrala<br>Pooja Reddy<br>Shubham Khupase
    </div>
    <div style='font-size:11px;color:{C["cadet"]};margin-bottom:1.2rem;'>
      ~INDIANA UNIVERSITY, BLOOMINGTON
    </div>

    <hr style='border-color:{C["cadet"]};margin:0.8rem 0;'>
    """, unsafe_allow_html=True)

    st.markdown(f"<div style='font-size:10px;color:{C['cadet']};font-weight:700;text-transform:uppercase;letter-spacing:0.07em;margin-bottom:5px;'>Year Range</div>", unsafe_allow_html=True)
    show_fcst = st.toggle("Include 2024–2035 Projection", value=True)
    max_yr = 2035 if show_fcst else 2023
    yr_start, yr_end = st.select_slider(
        "",
        options=list(range(2000, max_yr+1)),
        value=(2000, max_yr),
        label_visibility="collapsed"
    )
    yr_range = (yr_start, yr_end)

    st.markdown(f"<div style='font-size:10px;color:{C['cadet']};font-weight:700;text-transform:uppercase;letter-spacing:0.07em;margin:10px 0 5px;'>Spotlight Year</div>", unsafe_allow_html=True)
    spot_yr = st.select_slider(" ", options=years_hist, value=2023, label_visibility="collapsed")

    st.markdown(f"<div style='font-size:10px;color:{C['cadet']};font-weight:700;text-transform:uppercase;letter-spacing:0.07em;margin:10px 0 5px;'>Domain</div>", unsafe_allow_html=True)
    sel_dom = st.selectbox(
    "",
    ["Select a domain"] + DOMAINS,
    key="domain",
    label_visibility="collapsed"
    )
    active_doms  = DOMAINS if sel_dom == "Select a domain" else [sel_dom]
    dom_filtered = sel_dom != "Select a domain"

    st.markdown(f"<div style='font-size:10px;color:{C['cadet']};font-weight:700;text-transform:uppercase;letter-spacing:0.07em;margin:10px 0 5px;'>Indicator (22 total)</div>", unsafe_allow_html=True)
    ind_choice = st.selectbox(
    "  ",
    ["Select an indicator"] + indicators_all,
    key="indicator",
    label_visibility="collapsed"
  )

    st.markdown(f"""
    <div style='border-top:1px solid {C["cadet"]};margin-top:1.2rem;padding-top:0.9rem;
      font-size:11px;color:{C["cadet"]};line-height:1.9;'>
      Data: WDI + OWID CO2<br>
      Historical: 2000 – 2023<br>
      Forecast: 2024 – 2035<br>
      22 indicators · 4 domains<br>
      1,017 historical records
    </div>
    """, unsafe_allow_html=True)

# ── Filters ───────────────────────────────────────────────────────────────────
xl_f   = xl[(xl["Year"]>=yr_range[0]) & (xl["Year"]<=yr_range[1])]
hist_f = xl_f[xl_f["Year"]<=2023]
fore_f = xl_f[xl_f["Year"]>=2023]
long_f = long_df[(long_df["Year"]>=yr_range[0]) & (long_df["Year"]<=min(yr_range[1],2023))]
spot   = xl_hist[xl_hist["Year"]==spot_yr]
def gv(c):
    if len(spot)==0: return None
    v = spot[c].values[0]
    return float(v) if not pd.isna(v) else None
leader = spot["Leader"].values[0] if len(spot)>0 else "—"

# ── Plotly helpers ────────────────────────────────────────────────────────────
def PL(h=380, title=None):
    d = dict(
        paper_bgcolor=C["white"], plot_bgcolor="#F8FAFC",
        font=dict(family="Inter", color=C["muted"], size=12),
        legend=dict(bgcolor=C["white"], font=dict(color=C["text"], size=11),
                    bordercolor=C["border"], borderwidth=1),
        margin=dict(l=8, r=8, t=46 if title else 16, b=8),
        hoverlabel=dict(bgcolor=C["white"], font_color=C["text"],
                        bordercolor=C["border"], font_family="Inter"),
        height=h,
    )
    if title:
        d["title"] = dict(text=title,
                          font=dict(family="Inter", size=14, color=C["text"]),
                          x=0.01, xanchor="left")
    return d

def AX(**kw):
    return dict(gridcolor=C["grid"], linecolor=C["border"],
                zerolinecolor=C["border"],
                tickfont=dict(color=C["muted"], size=11, family="Inter"), **kw)

# ── TOP BAR ───────────────────────────────────────────────────────────────────
vn_s = gv("VN_SOFI"); ph_s = gv("PH_SOFI"); gap_v = gv("Gap")

st.markdown(f"""
<div class="top-bar">
  <div>
    <div class="top-title">State of Future Index 2035</div>
    <div class="top-sub">Vietnam vs Philippines &nbsp;|&nbsp; Client: Elizabeth Florescu, The Millennium Project</div>
    <div class="top-tagline">Applying the SOFI methodology at country level — 22 indicators across Economic, Health, Environment and Social domains</div>
  </div>
  <div style="text-align:right;">
    <a href="{PBI_URL}" target="_blank" class="pbi-btn">Open Power BI Dashboard</a>
  </div>
</div>
""", unsafe_allow_html=True)

# ── KPI Row ───────────────────────────────────────────────────────────────────
def kpi(col, lbl, val, sub, cls="vn"):
    col.markdown(f"""<div class="kpi {cls}">
      <div class="kpi-l">{lbl}</div>
      <div class="kpi-v">{f"{val:.4f}" if val is not None else "—"}</div>
      <div class="kpi-s">{sub}</div>
    </div>""", unsafe_allow_html=True)

# Country toggle
kpi_col_toggle, kpi_col_spacer = st.columns([2, 10])
with kpi_col_toggle:
    kpi_country = st.radio(
        "",
        ["Vietnam", "Philippines"],
        horizontal=True,
        label_visibility="collapsed",
        key="kpi_country"
    )

if kpi_country == "Vietnam":
    k1,k2,k3,k4,k5,k6 = st.columns(6)
    kpi(k1, f"SOFI Score {spot_yr}", gv("VN_SOFI"),        "Vietnam", "vn")
    kpi(k2, "Economic Score",        gv("VN_Economic"),    "Vietnam", "eco")
    kpi(k3, "Health Score",          gv("VN_Health"),      "Vietnam", "hlt")
    kpi(k4, "Environment Score",     gv("VN_Environment"), "Vietnam", "env")
    kpi(k5, "Social Score",          gv("VN_Social"),      "Vietnam", "soc")
    kpi(k6, "Gap (VN - PH)",         gv("Gap"),            f"Leader: {leader}", "vn")
else:
    k1,k2,k3,k4,k5,k6 = st.columns(6)
    kpi(k1, f"SOFI Score {spot_yr}", gv("PH_SOFI"),        "Philippines", "ph")
    kpi(k2, "Economic Score",        gv("PH_Economic"),    "Philippines", "eco")
    kpi(k3, "Health Score",          gv("PH_Health"),      "Philippines", "hlt")
    kpi(k4, "Environment Score",     gv("PH_Environment"), "Philippines", "env")
    kpi(k5, "Social Score",          gv("PH_Social"),      "Philippines", "soc")
    kpi(k6, "Gap (VN - PH)",         gv("Gap"),            f"Leader: {leader}", "ph")

st.markdown("<br>", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tab0, tab1, tab2, tab3, tab4 = st.tabs([
    "Overview",
    "Power BI Dashboard",
    "Python Charts",
    "Indicator Explorer",
    "Data",
])

# =============================================================================
# TAB 0 — OVERVIEW
# =============================================================================
with tab0:
    # Three info cards
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="info-card">
          <h4>About This Project</h4>
          <ul>
            <li>Applies the SOFI methodology at country level for Vietnam and Philippines</li>
            <li>22 indicators — 20 from World Bank WDI, 2 from OWID CO2 dataset</li>
            <li>Covers 75.1% of full SOFI weight (1,420 of 1,890 weight points)</li>
            <li>4 domains: Economic (6), Health (6), Environment (5), Social (5)</li>
            <li>Score above 1.0 means better than 2019 baseline; below 1.0 means worse</li>
          </ul>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="info-card">
          <h4>Power BI Dashboard</h4>
          <ul>
            <li>Page 1 — SOFI Overview: KPI cards, trajectory line chart, gap bar chart, year slicer and period filter</li>
            <li>Page 2 — Domain Breakdown: 4 line charts for Economic, Health, Environment, Social</li>
            <li>Page 3 — Scenario Simulator: domain weight slicers, ribbon chart, area chart</li>
          </ul>
          <a href="{PBI_URL}" target="_blank"
            style="display:inline-block;margin-top:10px;background:{C['coolgray']};color:white;
            text-decoration:none;border-radius:7px;padding:6px 14px;font-size:12px;font-weight:700;">
            Open Full Dashboard
          </a>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="info-card">
          <h4>Python Charts</h4>
          <ul>
            <li>Domain Decomposition — stacked bars across snapshot years 2000 to 2023</li>
            <li>Environment Deep Dive — CO2 vs Forest Area scatter (not in Power BI)</li>
            <li>All 22 Indicators Heatmap — normalized scores side by side</li>
            <li>All charts update with Year Range and Domain filter from the sidebar</li>
          </ul>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Key finding note
    st.markdown(f"""<div class="note">
      <strong>Key Finding — {spot_yr}:</strong>
      {leader} leads with a gap of {f"{abs(gap_v):.4f}" if gap_v else "—"} (Philippines: {f"{ph_s:.4f}" if ph_s else "—"} vs Vietnam: {f"{vn_s:.4f}" if vn_s else "—"}).
      Vietnam led from 2000 to 2014 driven by Economic and Health gains, then the Philippines overtook
      around 2015 through steadier broad-based Social and Health growth.
      The Environment domain is the critical weakness for both countries —
      rising CO2 emissions are actively pulling scores down from 2020 onward.
      Forecasts project the Philippines maintaining and extending its lead through 2035.
      Change the Spotlight Year slider in the sidebar to track how all six metrics shift across time.
    </div>""", unsafe_allow_html=True)

    # Stat pills
    st.markdown(f"""<div class="stat-row">
      <div class="stat-pill"><div class="sp-v">22</div><div class="sp-l">Indicators</div></div>
      <div class="stat-pill"><div class="sp-v">4</div><div class="sp-l">Domains</div></div>
      <div class="stat-pill"><div class="sp-v">1,017</div><div class="sp-l">Records</div></div>
      <div class="stat-pill"><div class="sp-v">75.1%</div><div class="sp-l">SOFI Weight</div></div>
      <div class="stat-pill"><div class="sp-v">24</div><div class="sp-l">Hist. Years</div></div>
      <div class="stat-pill"><div class="sp-v">0.82</div><div class="sp-l">Avg Forecast R²</div></div>
    </div>""", unsafe_allow_html=True)

    # Compact domain snapshot
    st.markdown(f'<p class="sh">Domain Score Snapshot — {spot_yr}</p>', unsafe_allow_html=True)
    if len(spot) > 0:
        s = spot.iloc[0]
        fig_snap = go.Figure()
        for dom, vk, pk in zip(DOMAINS, DOM_VN, DOM_PH):
            fig_snap.add_trace(go.Bar(
                name=f"VN – {dom}", x=[f"VN · {dom}"], y=[s[vk]],
                marker_color=DOM_C[dom], opacity=0.92,
                hovertemplate=f"Vietnam {dom}: %{{y:.4f}}<extra></extra>"))
            fig_snap.add_trace(go.Bar(
                name=f"PH – {dom}", x=[f"PH · {dom}"], y=[s[pk]],
                marker_color=DOM_C[dom], opacity=0.45,
                marker_line_color=DOM_C[dom], marker_line_width=1.5,
                hovertemplate=f"Philippines {dom}: %{{y:.4f}}<extra></extra>"))
        fig_snap.update_layout(**PL(250), barmode="group", showlegend=False,
            xaxis=AX(), yaxis=AX(title="Score", range=[0,1.2]))
        st.plotly_chart(fig_snap, use_container_width=True)

# =============================================================================
# TAB 1 — POWER BI
# =============================================================================
with tab1:
    st.markdown('<p class="sh">Power BI Dashboard — 3 Interactive Pages</p>', unsafe_allow_html=True)
    st.markdown('<p class="sd">Navigate between pages using the arrows at the bottom of the embedded report. Use slicers inside to filter by year and period.</p>', unsafe_allow_html=True)

    pc1, pc2, pc3 = st.columns(3)
    with pc1:
        st.markdown("""<div class="pg-card">
          <div class="pg-num">Page 1</div>
          <div class="pg-title">SOFI Overview</div>
          <div class="pg-desc">KPI cards, SOFI trajectory line chart, gap bar chart, year slicer and Historical / Projected period filter</div>
        </div>""", unsafe_allow_html=True)
    with pc2:
        st.markdown("""<div class="pg-card">
          <div class="pg-num">Page 2</div>
          <div class="pg-title">Domain Breakdown</div>
          <div class="pg-desc">4 line charts for Economic, Health, Environment and Social showing Vietnam vs Philippines with 2035 forecast</div>
        </div>""", unsafe_allow_html=True)
    with pc3:
        st.markdown("""<div class="pg-card">
          <div class="pg-num">Page 3</div>
          <div class="pg-title">Scenario Simulator</div>
          <div class="pg-desc">Domain weight slicers, ribbon chart, area chart and scatter — explore how changing domain weights shifts outcomes</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="pbi-wrap">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="pbi-hdr">
      <span class="pbi-hdr-t">SOFI 2035 — Vietnam vs Philippines</span>
      <a href="{PBI_URL}" target="_blank"
        style="color:{C['lblue']};font-size:12px;font-weight:700;text-decoration:none;">
        Open in new tab
      </a>
    </div>
    """, unsafe_allow_html=True)
    st.components.v1.html(f"""
    <iframe title="SOFI Power BI"
      width="100%" height="700"
      src="{PBI_URL}&navContentPaneEnabled=true&filterPaneEnabled=true"
      frameborder="0" allowFullScreen="true" style="display:block;">
    </iframe>
    """, height=710, scrolling=False)
    st.markdown("</div>", unsafe_allow_html=True)
    st.caption("Power BI — Built using SOFI_final_v5.xlsx — navigate pages with the arrows at the bottom of the report")

# =============================================================================
# TAB 2 — PYTHON CHARTS
# =============================================================================
with tab2:
    # ── Chart 1: Domain Decomposition ─────────────────────────────────────────
    st.markdown('<p class="sh">Domain Decomposition — Snapshot Years</p>', unsafe_allow_html=True)
    st.markdown('<p class="sd">Stacked SOFI sub-scores for Vietnam (solid) and Philippines (light outline) across six key years. Shows which domain drives each total score. Domain filter in sidebar applies here.</p>', unsafe_allow_html=True)

    snap_yrs = [y for y in [2000,2005,2010,2015,2019,2023] if y in xl_hist["Year"].values]
    snap = xl_hist[xl_hist["Year"].isin(snap_yrs)]
    bw = 0.35
    fig_dc = go.Figure()
    vbot = np.zeros(len(snap_yrs)); pbot = np.zeros(len(snap_yrs))
    for dom, vk, pk in zip(DOMAINS, DOM_VN, DOM_PH):
        if dom in active_doms:
            vv = snap[vk].values; pv = snap[pk].values
            fig_dc.add_trace(go.Bar(name=f"Vietnam – {dom}",
                x=[y-bw/2-0.02 for y in snap_yrs], y=vv, base=vbot.copy(),
                width=bw, marker_color=DOM_C[dom], opacity=0.9,
                hovertemplate=f"Vietnam {dom} %{{x}}: %{{y:.4f}}<extra></extra>"))
            fig_dc.add_trace(go.Bar(name=f"Philippines – {dom}",
                x=[y+bw/2+0.02 for y in snap_yrs], y=pv, base=pbot.copy(),
                width=bw, marker_color=DOM_C[dom], opacity=0.42,
                marker_line_color=DOM_C[dom], marker_line_width=1.5,
                hovertemplate=f"Philippines {dom} %{{x}}: %{{y:.4f}}<extra></extra>"))
            vbot += vv; pbot += pv

    fig_dc.update_layout(**PL(360, "Domain Decomposition — Vietnam (solid) vs Philippines (light)"),
        barmode="overlay",
        xaxis=AX(title="Year", tickvals=snap_yrs, ticktext=[str(y) for y in snap_yrs]),
        yaxis=AX(title="Cumulative Score"))
    st.plotly_chart(fig_dc, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Chart 2: CO2 vs Forest Area ───────────────────────────────────────────
    st.markdown('<p class="sh">Environment Domain — CO2 Emissions vs Forest Area</p>', unsafe_allow_html=True)
    st.markdown('<p class="sd">Trade-off between industrialization and forest cover. Bubble size = Environment domain score. Hover for exact values and year.</p>', unsafe_allow_html=True)

    env_vn = long_f[(long_f["Country Name"]=="Vietnam")     & (long_f["SOFI_Name"]=="CO2 per Capita")][["Year","Value"]].rename(columns={"Value":"CO2"})
    env_ph = long_f[(long_f["Country Name"]=="Philippines") & (long_f["SOFI_Name"]=="CO2 per Capita")][["Year","Value"]].rename(columns={"Value":"CO2"})
    fa_vn  = long_f[(long_f["Country Name"]=="Vietnam")     & (long_f["SOFI_Name"]=="Forest Area")][["Year","Value"]].rename(columns={"Value":"Forest"})
    fa_ph  = long_f[(long_f["Country Name"]=="Philippines") & (long_f["SOFI_Name"]=="Forest Area")][["Year","Value"]].rename(columns={"Value":"Forest"})

    mvn = env_vn.merge(fa_vn, on="Year").merge(hist_f[["Year","VN_Environment"]], on="Year", how="left")
    mph = env_ph.merge(fa_ph, on="Year").merge(hist_f[["Year","PH_Environment"]], on="Year", how="left")

    fig_env = go.Figure()
    if len(mvn) > 0:
        fig_env.add_trace(go.Scatter(
            x=mvn["CO2"], y=mvn["Forest"], mode="markers+text", name="Vietnam",
            text=mvn["Year"].astype(str), textposition="top center",
            textfont=dict(size=9, color=C["vn"]),
            marker=dict(size=mvn["VN_Environment"].fillna(0.5)*28+8,
                        color=C["vn"], opacity=0.75,
                        line=dict(width=2, color=C["white"])),
            hovertemplate="<b>Vietnam</b><br>Year: %{text}<br>CO2: %{x:.2f} t/person<br>Forest: %{y:.1f}%<extra></extra>"))
    if len(mph) > 0:
        fig_env.add_trace(go.Scatter(
            x=mph["CO2"], y=mph["Forest"], mode="markers+text", name="Philippines",
            text=mph["Year"].astype(str), textposition="top center",
            textfont=dict(size=9, color=C["ph"]),
            marker=dict(size=mph["PH_Environment"].fillna(0.5)*28+8,
                        color=C["cadet"], opacity=0.75,
                        line=dict(width=2, color=C["white"])),
            hovertemplate="<b>Philippines</b><br>Year: %{text}<br>CO2: %{x:.2f} t/person<br>Forest: %{y:.1f}%<extra></extra>"))
    fig_env.update_layout(**PL(360, "CO2 Emissions vs Forest Area — bubble size = Environment Score"),
        xaxis=AX(title="CO2 per Capita (tonnes/person)"),
        yaxis=AX(title="Forest Area (% of land)"))
    st.plotly_chart(fig_env, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Chart 3: All 22 Indicator Heatmap ─────────────────────────────────────
    st.markdown('<p class="sh">All 22 Indicators — Normalized Score Heatmap</p>', unsafe_allow_html=True)
    st.markdown('<p class="sd">Latest available year for all indicators. Darker = higher normalized score. Hover any cell for exact value.</p>', unsafe_allow_html=True)

    latest_yr = long_df["Year"].max()
    heat = long_df[long_df["Year"]==latest_yr][["Country Name","SOFI_Name","Normalized","Domain"]].dropna()
    hp = heat.pivot(index="SOFI_Name", columns="Country Name", values="Normalized")
    dm = long_df[["SOFI_Name","Domain"]].drop_duplicates().set_index("SOFI_Name")["Domain"]
    hp["_d"] = hp.index.map(dm)
    hp = hp.sort_values("_d").drop(columns="_d")
    if dom_filtered:
        dom_inds = long_df[long_df["Domain"]==sel_dom]["SOFI_Name"].unique()
        hp = hp[hp.index.isin(dom_inds)]

    if len(hp) > 0:
        fig_hm = go.Figure(data=go.Heatmap(
            z=hp.values, x=hp.columns.tolist(), y=hp.index.tolist(),
            colorscale=[[0,C["platinum"]],[0.5,C["lblue"]],[1,C["coolgray"]]],
            text=[[f"{v:.2f}" if not np.isnan(v) else "" for v in row] for row in hp.values],
            texttemplate="%{text}", textfont=dict(size=10, color=C["text"]),
            hovertemplate="%{y}<br>%{x}: %{z:.4f}<extra></extra>",
            colorbar=dict(tickfont=dict(color=C["muted"]),
                          outlinecolor=C["border"],
                          title=dict(text="Score", font=dict(color=C["muted"])))))
        fig_hm.update_layout(
            **PL(max(280, len(hp)*32+60), f"Normalized Scores — {len(hp)} Indicators ({latest_yr})"),
            yaxis=dict(autorange="reversed", **AX()), xaxis=AX())
        st.plotly_chart(fig_hm, use_container_width=True)

# =============================================================================
# TAB 3 — INDICATOR EXPLORER
# =============================================================================
with tab3:
    st.markdown('<p class="sh">Indicator Explorer</p>', unsafe_allow_html=True)

    # Reset button
    col_hdr, col_reset = st.columns([4, 1])
    with col_reset:
        def reset_filters():
            st.session_state["indicator"] = "Select an indicator"
            st.session_state["domain"] = "Select a domain"

        st.button("Reset Selection", on_click=reset_filters)

    if ind_choice == "Select an indicator":
        st.markdown(f"""<div class="note">
          Select one of the 22 indicators from the sidebar dropdown to explore its raw values,
          normalized scores and domain context for both countries.
        </div>""", unsafe_allow_html=True)

        # Reference table grouped by domain
        for dom in DOMAINS:
            dom_rows = summ_df[summ_df["Domain"]==dom]
            st.markdown(f"<div style='font-size:12px;font-weight:700;color:{DOM_C[dom]};margin:12px 0 4px;'>{dom}</div>", unsafe_allow_html=True)
            st.dataframe(
                dom_rows[["Indicator","Vietnam_LatestNorm","Philippines_LatestNorm"]].rename(
                    columns={"Indicator":"Indicator",
                             "Vietnam_LatestNorm":"Vietnam (latest normalized)",
                             "Philippines_LatestNorm":"Philippines (latest normalized)"}
                ).reset_index(drop=True),
                use_container_width=True, height="content"
            )
    else:
        sel_ind  = ind_choice
        ind_data = long_f[long_f["SOFI_Name"]==sel_ind]
        vn_ind   = ind_data[ind_data["Country Name"]=="Vietnam"]
        ph_ind   = ind_data[ind_data["Country Name"]=="Philippines"]

        if len(ind_data) > 0:
            meta = ind_data.iloc[0]
            m1,m2,m3,m4 = st.columns(4)
            m1.metric("Domain", meta["Domain"])
            m2.metric("Weight", f"{meta['Weight']:.1f}")
            m3.metric("Direction", "Higher is Better" if meta["Direction"]=="up" else "Lower is Better")
            m4.metric("Unit", str(meta["Unit"]) if pd.notna(meta["Unit"]) else "—")

            st.markdown(f"""<div class="note">
              <strong>{sel_ind}</strong> is in the <strong>{meta["Domain"]}</strong> domain
              with weight <strong>{meta["Weight"]:.1f}</strong>.
              A {"higher" if meta["Direction"]=="up" else "lower"} raw value means better performance.
              Normalized scores convert raw values to a 0–1 scale for cross-indicator comparison.
              The year range slider in the sidebar updates both charts below.
            </div>""", unsafe_allow_html=True)

        cl, cr = st.columns(2)
        with cl:
            st.markdown('<p class="sh">Raw Value</p>', unsafe_allow_html=True)
            fi1 = go.Figure()
            fi1.add_trace(go.Scatter(x=vn_ind["Year"], y=vn_ind["Value"],
                name="Vietnam", line=dict(color=C["vn"], width=3),
                mode="lines+markers",
                marker=dict(size=6, color=C["vn"], line=dict(width=2, color=C["white"])),
                hovertemplate="Vietnam %{x}: %{y:.3f}<extra></extra>"))
            fi1.add_trace(go.Scatter(x=ph_ind["Year"], y=ph_ind["Value"],
                name="Philippines", line=dict(color=C["cadet"], width=3),
                mode="lines+markers",
                marker=dict(size=6, color=C["cadet"], line=dict(width=2, color=C["white"])),
                hovertemplate="Philippines %{x}: %{y:.3f}<extra></extra>"))
            unit = str(ind_data["Unit"].iloc[0]) if len(ind_data)>0 and pd.notna(ind_data["Unit"].iloc[0]) else ""
            fi1.update_layout(**PL(300, f"{sel_ind} — Raw Value"),
                xaxis=AX(title="Year"), yaxis=AX(title=unit))
            st.plotly_chart(fi1, use_container_width=True)

        with cr:
            st.markdown('<p class="sh">Normalized Score (0–1)</p>', unsafe_allow_html=True)
            fi2 = go.Figure()
            fi2.add_trace(go.Scatter(x=vn_ind["Year"], y=vn_ind["Normalized"],
                name="Vietnam", line=dict(color=C["vn"], width=3),
                mode="lines+markers",
                marker=dict(size=6, color=C["vn"], line=dict(width=2, color=C["white"])),
                fill="tozeroy", fillcolor=f"rgba(30,42,58,0.06)",
                hovertemplate="Vietnam %{x}: %{y:.4f}<extra></extra>"))
            fi2.add_trace(go.Scatter(x=ph_ind["Year"], y=ph_ind["Normalized"],
                name="Philippines", line=dict(color=C["cadet"], width=3),
                mode="lines+markers",
                marker=dict(size=6, color=C["cadet"], line=dict(width=2, color=C["white"])),
                fill="tozeroy", fillcolor=f"rgba(122,144,168,0.07)",
                hovertemplate="Philippines %{x}: %{y:.4f}<extra></extra>"))
            fi2.update_layout(**PL(300, f"{sel_ind} — Normalized Score"),
                xaxis=AX(title="Year"),
                yaxis=dict(range=[0,1.05], **AX()))
            st.plotly_chart(fi2, use_container_width=True)

        # Domain comparison bar
        if len(ind_data) > 0:
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown(f'<p class="sh">All Indicators in {meta["Domain"]} Domain — Latest Score</p>', unsafe_allow_html=True)
            dom_ss = summ_df[summ_df["Domain"]==meta["Domain"]]
            fig_sb = go.Figure()
            fig_sb.add_trace(go.Bar(y=dom_ss["Indicator"], x=dom_ss["Vietnam_LatestNorm"],
                name="Vietnam", orientation="h", marker_color=C["vn"], opacity=0.85,
                hovertemplate="%{y}: %{x:.4f}<extra></extra>"))
            fig_sb.add_trace(go.Bar(y=dom_ss["Indicator"], x=dom_ss["Philippines_LatestNorm"],
                name="Philippines", orientation="h", marker_color=C["cadet"], opacity=0.85,
                hovertemplate="%{y}: %{x:.4f}<extra></extra>"))
            fig_sb.update_layout(
                **PL(max(220, len(dom_ss)*42),
                     f"{meta['Domain']} — Latest Normalized Scores"),
                barmode="group",
                xaxis=dict(range=[0,1.08], **AX(title="Normalized Score (0–1)")),
                yaxis=AX())
            st.plotly_chart(fig_sb, use_container_width=True)

# =============================================================================
# TAB 4 — DATA
# =============================================================================
with tab4:
    st.markdown('<p class="sh">Data Explorer</p>', unsafe_allow_html=True)
    st.markdown('<p class="sd">View and download the underlying dataset</p>', unsafe_allow_html=True)

    f1,f2,f3 = st.columns(3)
    with f1: tbl_c = st.selectbox("Country:", ["Both","Vietnam","Philippines"], key="tc")
    with f2: tbl_d = st.selectbox("Domain:", ["All"]+DOMAINS, key="td")
    with f3: tbl_t = st.selectbox("View:", ["SOFI Scores + Forecast","Indicator Data","Indicator Summary"])

    if tbl_t == "SOFI Scores + Forecast":
        cols = ["Year","VN_SOFI","PH_SOFI","VN_Economic","VN_Health","VN_Environment","VN_Social",
                "PH_Economic","PH_Health","PH_Environment","PH_Social","Gap","Leader","Period"]
        tdf = xl[[c for c in cols if c in xl.columns]].copy()
        if tbl_c == "Vietnam":
            tdf = tdf[["Year","VN_SOFI","VN_Economic","VN_Health","VN_Environment","VN_Social","Period"]]
        elif tbl_c == "Philippines":
            tdf = tdf[["Year","PH_SOFI","PH_Economic","PH_Health","PH_Environment","PH_Social","Period"]]
        st.dataframe(tdf, use_container_width=True, height=400)

    elif tbl_t == "Indicator Data":
        tdf = long_df.copy()
        if tbl_c != "Both": tdf = tdf[tdf["Country Name"]==tbl_c]
        if tbl_d != "All":  tdf = tdf[tdf["Domain"]==tbl_d]
        show = ["Year","Country Name","SOFI_Name","Domain","Value","Normalized","Weight","Unit"]
        st.dataframe(tdf[show].reset_index(drop=True), use_container_width=True, height=400)

    else:
        tdf = summ_df.copy()
        if tbl_d != "All": tdf = tdf[tdf["Domain"]==tbl_d]
        st.dataframe(tdf, use_container_width=True, height=400)

    st.markdown("<hr>", unsafe_allow_html=True)
    d1,d2,d3 = st.columns(3)
    with d1: st.download_button("Download SOFI Scores",    sofi_csv.to_csv(index=False), "sofi_scores.csv","text/csv")
    with d2: st.download_button("Download Indicator Data", long_df.to_csv(index=False),  "indicators.csv","text/csv")
    with d3: st.download_button("Download Summary",        summ_df.to_csv(index=False),  "summary.csv","text/csv")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style='text-align:center;color:{C["muted"]};font-size:11px;
  padding:1.2rem 0 0.5rem;border-top:1px solid {C["border"]};margin-top:2rem;'>
  SOFI 2035 — State of Future Index — Vietnam vs Philippines &nbsp;|&nbsp;
  Team D — Indiana University Bloomington &nbsp;|&nbsp;
  Client: Elizabeth Florescu, The Millennium Project
</div>
""", unsafe_allow_html=True)