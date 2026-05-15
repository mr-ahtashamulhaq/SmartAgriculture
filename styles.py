import streamlit as st


# ─────────────────────────────────────────────────────────────────────────────
# TYPOGRAPHY DECISIONS  (per SKILL.md font-recommendations)
#
# Font family: Inter (Rasmus Andersson)
#   - #1 recommendation for UI/Application design in SKILL.md
#   - Designed specifically for screens; excellent x-height legibility
#   - Covers Thin (100) → Black (900) — well above the 5+ weights rule
#   - Free, Google Fonts, loaded with display=swap to prevent FOIT
#   - Pairing: Inter Bold (h1 800) + Inter SemiBold (headings 600)
#              + Inter Regular (400) body  →  "Unified + Clean" from pairing table
#
# Weights loaded: 400 · 600 · 700 · 800  (only weights actually used; 300/500 dropped)
#
# Weight scale applied:
#   h1 page titles  → 800  (ExtraBold) with letter-spacing: -0.02em
#   section labels  → 600  (SemiBold)  with letter-spacing: 0.06em (ALL CAPS)
#   metric labels   → 600  (SemiBold)  with letter-spacing: 0.06em (ALL CAPS)
#   card/UI labels  → 600  (SemiBold)
#   body / captions → 400  (Regular)
#
# ALL CAPS letter-spacing: 0.06em  (SKILL.md rule: add ≥ 0.05em for uppercase)
# Headline letter-spacing: -0.02em (SKILL.md rule: tighten wide-spaced headline fonts)
# Base font-size: 15px              (SKILL.md: body text should be readable at target size)
# font-display: swap injected via &display=swap on Google Fonts URL
# ─────────────────────────────────────────────────────────────────────────────

GLOBAL_CSS = """
<style>
/* ── Google Fonts: Inter (400,600,700,800) + Material Symbols ────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

/* ── Hide Streamlit auto-generated sidebar nav ───────────────────────────── */
[data-testid="stSidebarNav"] {
    display: none !important;
}

/* ── Root Variables (LIGHT THEME) ────────────────────────────────────────── */
:root {
    --bg-primary:    #f8fafc;
    --bg-card:       #ffffff;
    --accent-green:  #16a34a;
    --accent-blue:   #2563eb;
    --accent-amber:  #d97706;
    --accent-rose:   #e11d48;
    --accent-violet: #7c3aed;
    --text-primary:  #0f172a;
    --text-secondary:#374151;
    --text-muted:    #64748b;
    --border:        #e2e8f0;
    --radius:        14px;
    --radius-sm:     8px;
    --shadow:        0 1px 8px rgba(15,23,42,0.08), 0 4px 16px rgba(15,23,42,0.04);
    --shadow-hover:  0 4px 20px rgba(15,23,42,0.12), 0 8px 32px rgba(15,23,42,0.06);

    /* Typography tokens */
    --font-body:     'Inter', -apple-system, Segoe UI, Roboto, sans-serif;
    --size-base:     15px;      /* comfortable body text floor */
    --size-sm:       0.8rem;    /* ~12px — minimum for UI labels */
    --size-xs:       0.72rem;   /* captions / metadata only */
    --ls-caps:       0.06em;    /* ALL CAPS letter-spacing (SKILL.md ≥ 0.05em) */
    --ls-headline:   -0.02em;   /* tighten bold headlines (SKILL.md rule) */
    --ls-tight:      -0.01em;   /* medium-weight display text */
}

/* ── Global Base ─────────────────────────────────────────────────────────── */
html, body, [data-testid="stAppViewContainer"] {
    font-family: var(--font-body) !important;
    font-size: var(--size-base) !important;
    font-weight: 400 !important;
    line-height: 1.6 !important;
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    -webkit-font-smoothing: antialiased !important;
    text-rendering: optimizeLegibility !important;
}

[data-testid="stMain"] {
    background-color: var(--bg-primary) !important;
}

.block-container {
    padding: 2rem 2.5rem 3rem !important;
    max-width: 1400px;
}

/* ── Headings ────────────────────────────────────────────────────────────── */
/* page_header h1 — ExtraBold, tightened letter-spacing (SKILL.md) */
h1 {
    font-family: var(--font-body) !important;
    font-weight: 800 !important;
    letter-spacing: var(--ls-headline) !important;
    color: var(--text-primary) !important;
    line-height: 1.2 !important;
}

/* section sub-headings — SemiBold only */
h2, h3, h4, h5 {
    font-family: var(--font-body) !important;
    font-weight: 600 !important;
    letter-spacing: var(--ls-tight) !important;
    color: var(--text-primary) !important;
    line-height: 1.3 !important;
}

/* ── Sidebar ─────────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid var(--border) !important;
    box-shadow: 2px 0 12px rgba(15,23,42,0.04) !important;
}

/* Target only text elements — NOT icon spans — to avoid breaking Material Symbols */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span:not([style*="Material"]):not(.ms):not([data-testid]),
[data-testid="stSidebar"] div:not([data-testid]) {
    font-family: var(--font-body);
}

[data-testid="stSidebar"] [data-testid="stPageLink"] a {
    border-radius: var(--radius-sm) !important;
    margin: 1px 0 !important;
    padding: 7px 10px !important;
    transition: background 0.2s ease, color 0.2s ease !important;
    font-weight: 500 !important;
    font-size: 0.875rem !important;
    color: var(--text-secondary) !important;
    text-decoration: none !important;
}

[data-testid="stSidebar"] [data-testid="stPageLink"] a:hover {
    background: #f0fdf4 !important;
    color: var(--accent-green) !important;
}

[data-testid="stSidebar"] [data-testid="stPageLink"] a[aria-current="page"] {
    background: #dcfce7 !important;
    color: #15803d !important;
    border-left: 3px solid var(--accent-green) !important;
    font-weight: 600 !important;
}

/* ── KPI / Metric Cards ──────────────────────────────────────────────────── */
[data-testid="metric-container"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 20px 24px !important;
    box-shadow: var(--shadow) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}

[data-testid="metric-container"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: var(--shadow-hover) !important;
}

/* Metric label — ALL CAPS SemiBold per SKILL.md rule */
[data-testid="metric-container"] label {
    font-family: var(--font-body) !important;
    color: var(--text-muted) !important;
    font-size: var(--size-sm) !important;      /* ≥ 0.8rem — legibility floor */
    font-weight: 600 !important;               /* SemiBold, not Bold */
    text-transform: uppercase !important;
    letter-spacing: var(--ls-caps) !important; /* 0.06em for ALL CAPS */
}

/* Metric value — Bold, no all-caps tracking */
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: var(--font-body) !important;
    color: var(--text-primary) !important;
    font-size: 1.9rem !important;
    font-weight: 700 !important;
    letter-spacing: var(--ls-tight) !important;
    line-height: 1.2 !important;
}

/* ── Buttons ─────────────────────────────────────────────────────────────── */
[data-testid="stButton"] > button {
    font-family: var(--font-body) !important;
    font-weight: 600 !important;               /* SemiBold for action labels */
    font-size: 0.875rem !important;
    letter-spacing: 0.01em !important;
    background: linear-gradient(135deg, #15803d, #16a34a) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.5rem 1.25rem !important;
    transition: opacity 0.2s ease, transform 0.15s ease, box-shadow 0.2s ease !important;
    box-shadow: 0 2px 8px rgba(22,163,74,0.3) !important;
}

[data-testid="stButton"] > button:hover {
    opacity: 0.92 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(22,163,74,0.35) !important;
}

/* ── Form Labels ─────────────────────────────────────────────────────────── */
/* Streamlit widget labels — Regular, readable size */
[data-testid="stWidgetLabel"] p,
label[data-testid],
.stSelectbox label,
.stTextInput label,
.stNumberInput label,
.stTextArea label,
.stDateInput label,
.stTimeInput label,
.stCheckbox label {
    font-family: var(--font-body) !important;
    font-size: 0.875rem !important;            /* 13px minimum for form labels */
    font-weight: 600 !important;               /* SemiBold — not Bold */
    color: var(--text-secondary) !important;
    letter-spacing: 0 !important;             /* no extra tracking on mixed case */
}

/* ── Inputs / Selectboxes ────────────────────────────────────────────────── */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stSelectbox"] > div > div {
    font-family: var(--font-body) !important;
    font-size: 0.9375rem !important;           /* 15px — comfortable input size */
    font-weight: 400 !important;
    background: #ffffff !important;
    border: 1.5px solid #cbd5e1 !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
}

[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: var(--accent-green) !important;
    box-shadow: 0 0 0 3px rgba(22,163,74,0.12) !important;
}

/* ── Caption / Helper Text ───────────────────────────────────────────────── */
[data-testid="stCaptionContainer"] p,
small {
    font-family: var(--font-body) !important;
    font-size: var(--size-xs) !important;      /* captions only at 0.72rem */
    font-weight: 400 !important;
    color: var(--text-muted) !important;
}

/* ── DataFrames / Tables ─────────────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border-radius: var(--radius) !important;
    overflow: hidden !important;
    border: 1px solid var(--border) !important;
    box-shadow: var(--shadow) !important;
}

/* ── Alerts ──────────────────────────────────────────────────────────────── */
[data-testid="stAlert"] {
    border-radius: var(--radius-sm) !important;
    border-left-width: 4px !important;
}

[data-testid="stAlert"] p {
    font-family: var(--font-body) !important;
    font-size: 0.9rem !important;
    font-weight: 400 !important;
}

/* ── Divider ─────────────────────────────────────────────────────────────── */
hr {
    border-color: var(--border) !important;
    margin: 1.5rem 0 !important;
}

/* ── Tab style ───────────────────────────────────────────────────────────── */
[data-testid="stTab"] button {
    font-family: var(--font-body) !important;
    font-size: 0.875rem !important;
    font-weight: 600 !important;               /* SemiBold for tabs */
    color: var(--text-muted) !important;
    letter-spacing: 0 !important;
}

[data-testid="stTab"] button[aria-selected="true"] {
    color: var(--accent-green) !important;
    font-weight: 700 !important;               /* Bold only for active tab */
    border-bottom: 2px solid var(--accent-green) !important;
}

/* ── Expander ────────────────────────────────────────────────────────────── */
[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    box-shadow: var(--shadow) !important;
}

/* ── Material Symbols utility class ──────────────────────────────────────── */
/* !important needed so it wins against any wildcard sidebar font override   */
.ms {
    font-family: 'Material Symbols Outlined' !important;
    font-size: 18px !important;
    font-style: normal !important;
    font-weight: normal !important;
    line-height: 1 !important;
    vertical-align: middle;
    display: inline-block;
    font-variation-settings: 'FILL' 1, 'wght' 400, 'GRAD' 0, 'opsz' 24;
}
</style>
"""


def inject_styles():
    """Inject global CSS into any Streamlit page."""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def render_sidebar():
    """
    Render the branded sidebar with icon-based navigation.
    Call this inside every page AFTER inject_styles().
    """
    with st.sidebar:
        # Brand: ExtraBold name, tightened letter-spacing per SKILL.md headline rule
        st.markdown("""
        <div style="padding: 1.25rem 0 0.75rem; text-align:center;">
            <div style="
                width:52px; height:52px; border-radius:14px; margin:0 auto 8px;
                background:linear-gradient(135deg,#15803d,#16a34a);
                display:flex; align-items:center; justify-content:center;
                box-shadow: 0 4px 12px rgba(22,163,74,0.25);
            ">
                <span class="ms" style="font-size:26px; color:#fff;">
                    potted_plant
                </span>
            </div>
            <div style="
                font-family:'Inter',sans-serif;
                font-size:1.1rem; font-weight:800; color:#0f172a;
                letter-spacing:-0.02em; margin-top:6px;
            ">Smart Agriculture Platform</div>

        </div>
        <hr style="border-color:#e2e8f0; margin:0.5rem 0 0.75rem;">
        <div style="
            font-family:'Inter',sans-serif;
            font-size:0.68rem; font-weight:600; color:#94a3b8;
            text-transform:uppercase; letter-spacing:0.06em;
            padding:0 0.25rem 0.4rem;
        ">Main Menu</div>
        """, unsafe_allow_html=True)

        st.page_link("app.py",              label="Dashboard",   icon=":material/dashboard:")
        st.page_link("pages/farmers.py",    label="Farmers",     icon=":material/person:")
        st.page_link("pages/farms.py",      label="Farms",       icon=":material/home:")
        st.page_link("pages/fields.py",     label="Fields",      icon=":material/grass:")
        st.page_link("pages/corps.py",      label="Crops",       icon=":material/agriculture:")
        st.page_link("pages/sensors.py",    label="Sensors",     icon=":material/sensors:")
        st.page_link("pages/soildata.py",   label="Soil Data",   icon=":material/science:")
        st.page_link("pages/weather.py",    label="Weather",     icon=":material/cloud:")
        st.page_link("pages/irrigation.py", label="Irrigation",  icon=":material/water_drop:")

        st.markdown("""
        <hr style="border-color:#e2e8f0; margin:1rem 0 0.75rem;">
        <div style="
            font-family:'Inter',sans-serif;
            font-size:0.75rem; text-align:center; padding-bottom:0.5rem;
        ">
            <div style="font-weight:600; color:#475569; letter-spacing:-0.01em;">
                Ahtasham &amp; Faizan
            </div>
            <div style="font-size:0.7rem; color:#94a3b8; margin-top:2px; font-weight:400;">
                DBMS Semester Project
            </div>
        </div>
        """, unsafe_allow_html=True)


def page_header(icon_name: str, title: str, subtitle: str = ""):
    """
    Page header — h1 at weight 800 with -0.02em letter-spacing per SKILL.md.
    Subtitle at Regular 400 / 0.88rem for contrast against the heavy title.
    """
    sub_html = (
        f'<p style="margin:5px 0 0; font-family:Inter,sans-serif; font-weight:400; '
        f'font-size:0.88rem; color:#64748b; letter-spacing:0; line-height:1.5;">'
        f'{subtitle}</p>'
        if subtitle else ""
    )
    st.markdown(f"""
    <div style="padding:1.25rem 0 1rem; border-bottom:1px solid #e2e8f0; margin-bottom:1.75rem;">
        <div style="display:flex; align-items:center; gap:0.75rem; margin-bottom:0.1rem;">
            <div style="
                width:40px; height:40px; border-radius:10px;
                background:linear-gradient(135deg,#15803d,#16a34a);
                display:flex; align-items:center; justify-content:center; flex-shrink:0;
                box-shadow:0 2px 8px rgba(22,163,74,0.25);
            ">
                <span class="ms" style="font-size:22px; color:#fff;">
                    {icon_name}
                </span>
            </div>
            <h1 style="
                margin:0;
                font-family:'Inter',sans-serif;
                font-size:1.65rem;
                font-weight:800;
                letter-spacing:-0.02em;
                color:#0f172a;
                line-height:1.2;
            ">{title}</h1>
        </div>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)


def section_header(title: str):
    """
    Section label — SemiBold (600) ALL CAPS with 0.06em letter-spacing per SKILL.md.
    Intentionally NOT Bold (700/800) — reserve those weights for page titles only.
    """
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:0.5rem; margin:1.75rem 0 0.75rem;">
        <div style="
            width:4px; height:18px; border-radius:2px;
            background:linear-gradient(180deg,#16a34a,#2563eb);
        "></div>
        <span style="
            font-family:'Inter',sans-serif;
            font-size:0.72rem;
            font-weight:600;
            text-transform:uppercase;
            letter-spacing:0.06em;
            color:#64748b;
        ">{title}</span>
    </div>
    """, unsafe_allow_html=True)


# ── Plotly shared layout — Inter font applied consistently everywhere ──────────
# All chart text uses the same Inter stack so no chart reverts to browser default.
PLOTLY_FONT = dict(family="Inter, -apple-system, Segoe UI, sans-serif", color="#475569", size=12)

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=PLOTLY_FONT,
    margin=dict(l=20, r=20, t=40, b=20),
    legend=dict(
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor="#e2e8f0",
        borderwidth=1,
        font=dict(family="Inter, sans-serif", color="#374151", size=12)
    ),
    xaxis=dict(
        showgrid=True,
        gridcolor="#f1f5f9",
        linecolor="#e2e8f0",
        tickfont=dict(family="Inter, sans-serif", color="#94a3b8", size=11),
        title_font=dict(family="Inter, sans-serif", color="#64748b", size=12)
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor="#f1f5f9",
        linecolor="#e2e8f0",
        tickfont=dict(family="Inter, sans-serif", color="#94a3b8", size=11),
        title_font=dict(family="Inter, sans-serif", color="#64748b", size=12)
    )
)

COLORS = {
    "green":  "#16a34a",
    "blue":   "#2563eb",
    "amber":  "#d97706",
    "rose":   "#e11d48",
    "violet": "#7c3aed",
    "cyan":   "#0891b2",
    "orange": "#ea580c",
}
