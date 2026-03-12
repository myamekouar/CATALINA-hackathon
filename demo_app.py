# ─────────────────────────────────────────────────────────────────────────────
# GreenBasket · Shopper Intelligence Demo
# Catalina Hackathon — Omnichannel Activation & Gamification Platform
# Run: streamlit run demo_app.py
# ─────────────────────────────────────────────────────────────────────────────

import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GreenBasket · Catalina",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Colour palette ────────────────────────────────────────────────────────────
C_BLUE   = "#004A97"
C_RED    = "#CC0000"
C_GREEN  = "#2E7D32"
C_AMBER  = "#F57F17"
C_LTBL   = "#E8F1FB"

TIER_COL = {
    "Bronze": "#CD7F32", "Silver": "#757575",
    "Gold": "#F9A825",   "Platinum": "#546E7A",
}
PERSONA_COL = {
    "Health Pioneer":    ("#E8F5E9", "#2E7D32"),
    "Eco Explorer":      ("#E0F2F1", "#00695C"),
    "Family Organiser":  ("#E3F2FD", "#1565C0"),
    "Budget-Conscious":  ("#FFF8E1", "#E65100"),
    "Routine Loyalist":  ("#F3E5F5", "#6A1B9A"),
    "Weekend Foodie":    ("#FFF3E0", "#BF360C"),
    "Eco-Progressive":   ("#E8F5E9", "#2E7D32"),
    "Convenience Seeker":("#E8EAF6", "#283593"),
}
NUTRI_ECO_COL = {
    "A": "#038141", "B": "#85BB2F", "C": "#FFCC00",
    "D": "#EE8100", "E": "#E63312",
}
BADGE_ICON = {
    "Family Hero": "👨‍👩‍👧", "Loyal Explorer": "⭐", "Bulk Buyer": "📦",
    "First Steps": "🌱",   "Green Champion": "🌿", "Health Habit": "🥗",
    "Planet Saver": "🌍",  "Eco Leader": "♻️",    "E-shopper": "📱",
    "Foodie Explorer": "🍴","Weekend Warrior": "🏃","Green Explorer": "🔍",
}
CH_ICON = {
    "App Push Notification": "📱", "Email Campaign": "📧",
    "In-Store Coupon": "🏪",       "Email and App Push": "📱📧",
    "App Push": "📱",
}

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
html, body, [class*="css"] { font-family: "Segoe UI", Arial, sans-serif; }
.block-container { padding-top: 1.2rem !important; max-width: 1100px !important; }
section[data-testid="stSidebar"] > div:first-child {
    background: linear-gradient(180deg,#002f6c 0%,#004A97 100%);
}
#MainMenu, footer, header { visibility: hidden; }
button[data-baseweb="tab"] {
    font-size: 13px !important; font-weight: 600 !important;
    letter-spacing: .4px !important; padding: 10px 26px !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #004A97 !important;
    border-bottom: 3px solid #004A97 !important;
}
div[data-testid="metric-container"] { background: white; border-radius: 10px;
    padding: 14px 16px; box-shadow: 0 2px 8px rgba(0,0,0,.06); }
</style>
""", unsafe_allow_html=True)

# ── Data loading ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "demo_shopper_profiles.csv")
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip().str.lower()
    return df

df = load_data()

# ── Helpers ───────────────────────────────────────────────────────────────────
def g(row, key, default="—"):
    v = row.get(key, default)
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return default
    return v

def safe_float(row, key, default=0.0):
    try:
        return float(g(row, key, default))
    except Exception:
        return float(default)

def safe_int(row, key, default=0):
    try:
        return int(float(g(row, key, default)))
    except Exception:
        return int(default)

def kpi_card(label, value, color=C_BLUE, sub=None):
    sub_html = f'<div style="font-size:11px;color:#aaa;margin-top:4px">{sub}</div>' if sub else ""
    return (
        f'<div style="background:#fff;border-radius:10px;padding:18px 16px;'
        f'box-shadow:0 2px 8px rgba(0,0,0,.07);border-top:4px solid {color};text-align:center">'
        f'<div style="font-size:10px;color:#999;text-transform:uppercase;letter-spacing:1px;margin-bottom:7px">{label}</div>'
        f'<div style="font-size:26px;font-weight:900;color:{color};line-height:1.1">{value}</div>'
        f'{sub_html}</div>'
    )

def section_hdr(text):
    st.markdown(
        f'<div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:2px;'
        f'color:{C_BLUE};margin:26px 0 14px;padding-bottom:7px;border-bottom:2px solid {C_LTBL}">'
        f'{text}</div>', unsafe_allow_html=True
    )

# ── Charts ────────────────────────────────────────────────────────────────────
def chart_donut(row):
    ins  = safe_float(row, "channel_instore", 70)
    eco  = safe_float(row, "channel_ecommerce", 20)
    cc   = safe_float(row, "channel_clickcollect", 10)
    fig = go.Figure(go.Pie(
        labels=["In-Store", "E-commerce", "Click & Collect"],
        values=[ins, eco, cc],
        hole=0.62,
        marker=dict(colors=[C_BLUE, C_RED, C_AMBER], line=dict(color="white", width=2)),
        textinfo="label+percent",
        textfont=dict(size=11),
        hovertemplate="%{label}: %{value:.0f}%<extra></extra>",
    ))
    fig.update_layout(showlegend=False, margin=dict(l=10,r=10,t=10,b=10),
                      paper_bgcolor="white", height=210)
    return fig

def chart_categories(row):
    cats = [g(row,"category_1","—"), g(row,"category_2","—"), g(row,"category_3","—")]
    vals = [safe_float(row,"cat_1_share",30), safe_float(row,"cat_2_share",20), safe_float(row,"cat_3_share",15)]
    colors = [C_BLUE, f"rgba(0,74,151,.65)", f"rgba(0,74,151,.40)"]
    fig = go.Figure(go.Bar(
        x=vals, y=cats, orientation="h",
        marker_color=colors,
        text=[f"{v:.0f}%" for v in vals], textposition="outside",
        textfont=dict(size=11, color="#555"),
        hovertemplate="%{y}: %{x}%<extra></extra>",
    ))
    fig.update_layout(
        xaxis=dict(visible=False, range=[0, max(vals)*1.35]),
        yaxis=dict(autorange="reversed", tickfont=dict(size=11, color="#444")),
        margin=dict(l=10,r=50,t=10,b=10),
        paper_bgcolor="white", plot_bgcolor="white",
        height=150, bargap=0.35,
    )
    return fig

def chart_radar(row):
    tier_score = {"Bronze":20,"Silver":45,"Gold":70,"Platinum":95}.get(str(g(row,"loyalty_tier","")), 50)
    freq_score = min(int(safe_float(row,"visits_per_month",5) / 15 * 100), 100)
    eng_score  = min(safe_int(row,"streak_weeks",0) * 10 + 20, 100)
    vals = [
        safe_float(row,"health_score",50),
        safe_float(row,"sustainability_score",50),
        freq_score, eng_score,
        safe_float(row,"channel_ecommerce",20),
        tier_score,
    ]
    cats = ["Health","Sustain-<br>ability","Frequency","Engage-<br>ment","E-com","Loyalty"]
    fig = go.Figure(go.Scatterpolar(
        r=vals + [vals[0]], theta=cats + [cats[0]],
        fill="toself", fillcolor="rgba(0,74,151,.18)",
        line=dict(color=C_BLUE, width=2.5),
        marker=dict(color=C_BLUE, size=5),
        hovertemplate="%{theta}: %{r:.0f}<extra></extra>",
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=False, range=[0,100]),
            angularaxis=dict(tickfont=dict(size=11, color="#555"), gridcolor="#ddd"),
            gridshape="linear", bgcolor="#F8F9FA",
        ),
        showlegend=False,
        margin=dict(l=44,r=44,t=28,b=28),
        paper_bgcolor="white", height=260,
    )
    return fig

def chart_impact(row):
    labels = ["Engagement\nUplift","Healthier\nBasket","Sustainability\nGain","Retention"]
    vals   = [
        safe_int(row,"engagement_uplift",20),
        safe_int(row,"basket_health_shift",12),
        safe_int(row,"sustainability_gain",10),
        safe_int(row,"retention_pct",70),
    ]
    fig = go.Figure(go.Bar(
        x=labels, y=vals,
        marker_color=[C_GREEN, C_GREEN, "#43A047", C_BLUE],
        text=[f"{v}%" for v in vals], textposition="outside",
        textfont=dict(size=13), width=0.5,
    ))
    fig.update_layout(
        xaxis=dict(tickfont=dict(size=11, color="#444")),
        yaxis=dict(range=[0,max(vals)*1.3], showgrid=True, gridcolor="#F0F0F0",
                   ticksuffix="%", tickfont=dict(size=11,color="#aaa")),
        margin=dict(l=20,r=20,t=10,b=10),
        paper_bgcolor="white", plot_bgcolor="white",
        height=230, bargap=0.4,
    )
    return fig

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="background:rgba(0,0,0,.22);padding:18px 16px 14px;margin-bottom:4px">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:5px">
        <div style="background:#CC0000;padding:4px 10px;border-radius:5px;
                    font-size:12px;font-weight:900;color:#fff">Catalina</div>
        <div style="font-size:16px;font-weight:800;color:#fff">GreenBasket</div>
      </div>
      <div style="font-size:10px;color:rgba(255,255,255,.5);letter-spacing:.6px">
        Shopper Intelligence Demo
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="padding:12px 16px 4px;font-size:10px;color:rgba(255,255,255,.5);
                text-transform:uppercase;letter-spacing:1.2px;font-weight:600">
      Select Profile
    </div>
    """, unsafe_allow_html=True)

    opts = {
        f"{r['name']}  ·  {r['persona']}": r["shopper_id"]
        for _, r in df.sort_values(["segment","persona"]).iterrows()
    }
    chosen = st.selectbox("shopper", list(opts.keys()), label_visibility="collapsed")
    row = df[df["shopper_id"] == opts[chosen]].iloc[0].to_dict()

    st.markdown(
        '<div style="padding:10px 16px 16px;font-size:10px;'
        'color:rgba(255,255,255,.28);text-align:center">Synthetic data · Demo only</div>',
        unsafe_allow_html=True,
    )

# ── GLOBAL HEADER ─────────────────────────────────────────────────────────────
_tc       = TIER_COL.get(str(g(row,"loyalty_tier","Bronze")), "#777")
_pbg,_pcol = PERSONA_COL.get(str(g(row,"persona","")), (C_LTBL, C_BLUE))

st.markdown(f"""
<div style="background:linear-gradient(135deg,#003478 0%,#0058b8 100%);
            border-radius:12px;padding:22px 28px;margin-bottom:20px;
            display:flex;align-items:center;justify-content:space-between;
            box-shadow:0 4px 20px rgba(0,52,120,.28)">
  <div>
    <div style="font-size:10px;color:#90BBE8;text-transform:uppercase;
                letter-spacing:2px;margin-bottom:6px">
      Catalina · GreenBasket Intelligence Demo
    </div>
    <div style="font-size:28px;font-weight:800;color:#fff;margin-bottom:10px">
      {g(row,'name')}
    </div>
    <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">
      <span style="background:{_pbg};color:{_pcol};padding:5px 14px;
                   border-radius:20px;font-size:13px;font-weight:700">
        ✦ {g(row,'persona')}
      </span>
      <span style="background:rgba(255,255,255,.15);color:#fff;padding:5px 14px;
                   border-radius:20px;font-size:12px">
        {g(row,'segment')}
      </span>
      <span style="background:{_tc};color:#fff;padding:5px 14px;
                   border-radius:20px;font-size:12px;font-weight:700">
        ★ {g(row,'loyalty_tier')}
      </span>
    </div>
  </div>
  <div style="text-align:right;flex-shrink:0;margin-left:24px">
    <div style="font-size:11px;color:#90BBE8;margin-bottom:3px">Age Group</div>
    <div style="font-size:26px;font-weight:700;color:#fff">{g(row,'age_group')}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["  Business View  ","  Shopper View  ","  Checkout Journey  "])


# ═════════════════════════════════════════════════════════════════════════════
# TAB 1 · BUSINESS VIEW
# ═════════════════════════════════════════════════════════════════════════════
with tab1:

    # ── KPI cards ────────────────────────────────────────────────────────────
    section_hdr("Shopper Profile")

    c1,c2,c3,c4 = st.columns(4)
    spend = safe_float(row,"annual_spend",0)
    abv   = safe_float(row,"avg_basket_value",0)
    vpm   = safe_float(row,"visits_per_month",0)
    pts   = safe_int(row,"points_balance",0)
    ec    = safe_float(row,"channel_ecommerce",0)

    with c1: st.markdown(kpi_card("Annual Spend",f"€{spend:,.0f}",C_BLUE), unsafe_allow_html=True)
    with c2: st.markdown(kpi_card("Avg Basket Value",f"€{abv:.1f}",C_RED), unsafe_allow_html=True)
    with c3: st.markdown(kpi_card("Visits / Month",f"{vpm:.1f}",C_GREEN,f"{ec:.0f}% online"), unsafe_allow_html=True)
    with c4: st.markdown(kpi_card("Points Balance",f"{pts:,}",C_AMBER,f"{safe_int(row,'next_reward_gap',0):,} to next reward"), unsafe_allow_html=True)

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    # ── Behavioural overview ─────────────────────────────────────────────────
    section_hdr("Behavioural Overview")

    col_don, col_cat, col_hs = st.columns([1,1,1])

    with col_don:
        st.markdown(
            f'<div style="background:#fff;border-radius:10px;padding:14px 14px 4px;'
            f'box-shadow:0 2px 8px rgba(0,0,0,.06)">'
            f'<div style="font-size:11px;font-weight:700;color:#666;text-transform:uppercase;'
            f'letter-spacing:1px">Channel Mix</div></div>',
            unsafe_allow_html=True
        )
        st.plotly_chart(chart_donut(row), use_container_width=True, config={"displayModeBar":False})

    with col_cat:
        st.markdown(
            f'<div style="background:#fff;border-radius:10px;padding:14px 14px 4px;'
            f'box-shadow:0 2px 8px rgba(0,0,0,.06)">'
            f'<div style="font-size:11px;font-weight:700;color:#666;text-transform:uppercase;'
            f'letter-spacing:1px">Top Categories</div></div>',
            unsafe_allow_html=True
        )
        st.plotly_chart(chart_categories(row), use_container_width=True, config={"displayModeBar":False})

    with col_hs:
        hs  = safe_int(row,"health_score",50)
        ss  = safe_int(row,"sustainability_score",50)
        ns  = str(g(row,"nutri_score","C"))
        es  = str(g(row,"eco_score","C"))
        nc  = NUTRI_ECO_COL.get(ns,"#aaa")
        ecc = NUTRI_ECO_COL.get(es,"#aaa")
        hc  = C_GREEN if hs >= 70 else (C_AMBER if hs >= 50 else C_RED)
        sc  = C_GREEN if ss >= 70 else (C_AMBER if ss >= 50 else C_RED)
        streak = safe_int(row,"streak_weeks",0)
        st.markdown(f"""
        <div style="background:#fff;border-radius:10px;padding:16px;
                    box-shadow:0 2px 8px rgba(0,0,0,.06);height:100%">
          <div style="font-size:11px;font-weight:700;color:{C_GREEN};text-transform:uppercase;
                      letter-spacing:1px;margin-bottom:12px">Health & Sustainability</div>
          <div style="display:flex;gap:10px;margin-bottom:14px">
            <div style="background:{nc};color:#fff;width:50px;height:50px;border-radius:9px;
                        display:flex;flex-direction:column;align-items:center;justify-content:center;
                        font-size:20px;font-weight:900;flex-shrink:0">
              {ns}<span style="font-size:7px;font-weight:400">NUTRI</span>
            </div>
            <div style="background:{ecc};color:#fff;width:50px;height:50px;border-radius:9px;
                        display:flex;flex-direction:column;align-items:center;justify-content:center;
                        font-size:20px;font-weight:900;flex-shrink:0">
              {es}<span style="font-size:7px;font-weight:400">ECO</span>
            </div>
            <div style="font-size:11px;color:#666;line-height:1.8">
              <div>Top category: <strong>{g(row,'category_1')}</strong></div>
              <div>E-commerce: <strong>{ec:.0f}%</strong></div>
            </div>
          </div>
          <div style="margin-bottom:10px">
            <div style="display:flex;justify-content:space-between;font-size:11px;color:#555;margin-bottom:4px">
              <span>Health Score</span><span style="font-weight:700;color:{hc}">{hs}/100</span>
            </div>
            <div style="background:#F0F0F0;border-radius:5px;height:7px">
              <div style="width:{hs}%;height:7px;border-radius:5px;background:{hc}"></div>
            </div>
          </div>
          <div style="margin-bottom:12px">
            <div style="display:flex;justify-content:space-between;font-size:11px;color:#555;margin-bottom:4px">
              <span>Sustainability Score</span><span style="font-weight:700;color:{sc}">{ss}/100</span>
            </div>
            <div style="background:#F0F0F0;border-radius:5px;height:7px">
              <div style="width:{ss}%;height:7px;border-radius:5px;background:{sc}"></div>
            </div>
          </div>
          <div style="background:#FFF8E1;border-radius:8px;padding:7px 11px;font-size:12px;
                      font-weight:600;color:{C_AMBER};text-align:center">
            🔥 {streak}-week healthy basket streak
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Persona ───────────────────────────────────────────────────────────────
    section_hdr("Shopper Persona")

    persona = str(g(row,"persona",""))
    pbg2, pcol2 = PERSONA_COL.get(persona, (C_LTBL, C_BLUE))

    col_persona, col_radar = st.columns([1.3,1])

    with col_persona:
        mission_desc = g(row,"mission_description","—")
        act_reason   = g(row,"activation_reason","—")
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,{C_LTBL} 0%,#EBF3FF 100%);
                    border:1.5px solid #C5DCEF;border-radius:12px;padding:20px 22px;height:100%">
          <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px">
            <div style="background:{pbg2};color:{pcol2};width:52px;height:52px;border-radius:11px;
                        font-size:26px;display:flex;align-items:center;justify-content:center;
                        flex-shrink:0">{PERSONA_COL.get(persona,(_,""))[0][:2] if False else "👤"}</div>
            <div>
              <div style="font-size:18px;font-weight:800;color:{C_BLUE}">{persona}</div>
              <div style="margin-top:4px">
                <span style="background:{C_BLUE};color:#fff;padding:3px 10px;border-radius:20px;
                             font-size:11px;font-weight:600">{g(row,'segment')}</span>
                &nbsp;
                <span style="background:{pbg2};color:{pcol2};padding:3px 10px;border-radius:20px;
                             font-size:11px;font-weight:600;border:1px solid {pcol2}33">{g(row,'age_group')}</span>
              </div>
            </div>
          </div>
          <div style="font-size:13px;color:#444;line-height:1.65;margin-bottom:14px">
            {mission_desc}
          </div>
          <div style="background:rgba(255,255,255,.75);border-radius:8px;padding:11px 14px">
            <div style="font-size:10px;color:#999;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">
              Why this activation?
            </div>
            <div style="font-size:12px;color:#333;line-height:1.55">{act_reason}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_radar:
        st.markdown(
            f'<div style="background:#fff;border-radius:12px;padding:14px 14px 4px;'
            f'box-shadow:0 2px 8px rgba(0,0,0,.06)">'
            f'<div style="font-size:11px;font-weight:700;color:{C_BLUE};text-transform:uppercase;'
            f'letter-spacing:1.5px">Behavioural Profile</div></div>',
            unsafe_allow_html=True
        )
        st.plotly_chart(chart_radar(row), use_container_width=True, config={"displayModeBar":False})

    # ── Rewards Journey ───────────────────────────────────────────────────────
    section_hdr("Rewards Journey")

    pts_total = pts + safe_int(row,"next_reward_gap",1)
    prog_pct  = int(pts / pts_total * 100) if pts_total > 0 else 0
    badges    = [str(g(row,b,"")) for b in ["badge_1","badge_2","badge_3"]]
    badges    = [b for b in badges if b and b != "—"]

    badge_chips = "".join(
        f'<span style="background:{C_LTBL};color:{C_BLUE};padding:4px 12px;border-radius:20px;'
        f'font-size:12px;font-weight:600;margin:2px 3px;display:inline-block;border:1px solid #C5DCEF">'
        f'{BADGE_ICON.get(b,"🏅")} {b}</span>'
        for b in badges
    ) or f'<span style="color:#aaa;font-size:12px">Complete missions to earn badges</span>'

    col_rj, col_mission = st.columns([1,1.2])

    with col_rj:
        st.markdown(f"""
        <div style="background:#fff;border-radius:12px;padding:20px;
                    box-shadow:0 2px 8px rgba(0,0,0,.06)">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
            <span style="font-size:13px;color:#555">Progress to next reward</span>
            <span style="font-size:15px;font-weight:900;color:{C_BLUE}">{prog_pct}%</span>
          </div>
          <div style="background:#E8EAED;border-radius:7px;height:12px;overflow:hidden;margin-bottom:5px">
            <div style="width:{prog_pct}%;height:12px;border-radius:7px;
                        background:linear-gradient(90deg,{C_BLUE},{C_BLUE}cc)"></div>
          </div>
          <div style="display:flex;justify-content:space-between;font-size:11px;color:#aaa;margin-bottom:16px">
            <span>{pts:,} pts</span>
            <span>{safe_int(row,'next_reward_gap',0):,} pts needed</span>
          </div>
          <div style="font-size:11px;font-weight:700;color:#666;text-transform:uppercase;
                      letter-spacing:1px;margin-bottom:8px">Earned Badges</div>
          <div>{badge_chips}</div>
        </div>
        """, unsafe_allow_html=True)

    with col_mission:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,{C_LTBL} 0%,#EBF3FF 100%);
                    border:1.5px solid #C5DCEF;border-radius:12px;padding:20px">
          <div style="font-size:11px;font-weight:700;color:{C_BLUE};text-transform:uppercase;
                      letter-spacing:1px;margin-bottom:10px">Active Mission</div>
          <div style="font-size:15px;font-weight:700;color:#1a1a2e;margin-bottom:12px;line-height:1.55">
            {g(row,'activation_message')}
          </div>
          <div style="background:white;border-radius:8px;padding:10px 14px;border-left:4px solid {C_AMBER}">
            <div style="font-size:10px;color:#999;margin-bottom:2px">Offer type</div>
            <div style="font-size:13px;font-weight:700;color:#333">🎁 {g(row,'activation_offer_type')}</div>
          </div>
          <div style="margin-top:11px;display:flex;gap:8px">
            <div style="flex:1;background:white;border-radius:8px;padding:9px;text-align:center">
              <div style="font-size:10px;color:#999;margin-bottom:2px">Streak</div>
              <div style="font-size:18px;font-weight:800;color:{C_AMBER}">🔥 {safe_int(row,'streak_weeks',0)}w</div>
            </div>
            <div style="flex:1;background:white;border-radius:8px;padding:9px;text-align:center">
              <div style="font-size:10px;color:#999;margin-bottom:2px">Points</div>
              <div style="font-size:18px;font-weight:800;color:{C_BLUE}">{pts:,}</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Activation recommendation ─────────────────────────────────────────────
    section_hdr("Omnichannel Activation")

    ch      = str(g(row,"activation_channel","—"))
    timing  = str(g(row,"activation_timing","—"))
    off_type= str(g(row,"activation_offer_type","—"))
    message = str(g(row,"activation_message","—"))
    reason  = str(g(row,"activation_reason","—"))
    ch_icon = CH_ICON.get(ch, "📣")

    col_act, col_why = st.columns([1,1.4])

    with col_act:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#FFF5F5 0%,#FFF0F0 100%);
                    border:1.5px solid #FFCDD2;border-left:5px solid {C_RED};
                    border-radius:12px;padding:20px">
          <div style="font-size:10px;color:#999;text-transform:uppercase;letter-spacing:1px;margin-bottom:14px">
            Recommended Activation
          </div>
          <div style="font-size:18px;font-weight:800;color:{C_RED};margin-bottom:14px">
            {ch_icon} {ch}
          </div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px">
            <div style="background:rgba(255,255,255,.8);border-radius:8px;padding:10px">
              <div style="font-size:10px;color:#aaa;text-transform:uppercase;letter-spacing:1px;margin-bottom:3px">Timing</div>
              <div style="font-size:13px;font-weight:700;color:#333">⏰ {timing}</div>
            </div>
            <div style="background:rgba(255,255,255,.8);border-radius:8px;padding:10px">
              <div style="font-size:10px;color:#aaa;text-transform:uppercase;letter-spacing:1px;margin-bottom:3px">Offer Type</div>
              <div style="font-size:13px;font-weight:700;color:#333">🎁 {off_type}</div>
            </div>
          </div>
          <div style="background:rgba(255,255,255,.9);border-radius:8px;padding:10px 12px">
            <div style="font-size:11px;color:#555;line-height:1.55">
              <strong>Message:</strong> {message}
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_why:
        st.markdown(f"""
        <div style="background:#fff;border-radius:12px;padding:20px;
                    box-shadow:0 2px 8px rgba(0,0,0,.06);height:100%">
          <div style="font-size:11px;font-weight:700;color:#666;text-transform:uppercase;
                      letter-spacing:1px;margin-bottom:12px">Why this activation?</div>
          <div style="font-size:13px;color:#444;line-height:1.7;margin-bottom:16px">{reason}</div>
          <div style="background:{C_LTBL};border-radius:8px;padding:12px 14px">
            <div style="font-size:10px;color:{C_BLUE};font-weight:700;text-transform:uppercase;
                        letter-spacing:1px;margin-bottom:8px">Data signals used</div>
            <div style="display:flex;flex-wrap:wrap;gap:6px">
              {"".join(f'<span style="background:white;color:{C_BLUE};padding:3px 10px;border-radius:20px;font-size:11px;border:1px solid #C5DCEF">{s}</span>' for s in ["📊 Purchase frequency","🛒 Channel preference","🌿 Health trajectory","🎯 Offer response history","🏷️ Nutri / Eco scores"])}
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Simulated impact ──────────────────────────────────────────────────────
    section_hdr("Simulated Business Impact")
    st.markdown('<div style="font-size:11px;color:#aaa;margin-top:-10px;margin-bottom:14px">Simulated model output — for demonstration purposes</div>', unsafe_allow_html=True)

    ci1,ci2,ci3,ci4 = st.columns(4)
    impact_data = [
        (ci1,"Engagement Uplift",f"+{safe_int(row,'engagement_uplift',0)}%",C_GREEN,"#F1F8F2"),
        (ci2,"Healthier Basket",f"+{safe_int(row,'basket_health_shift',0)}%","#43A047","#F1F8F2"),
        (ci3,"Sustainability Gain",f"+{safe_int(row,'sustainability_gain',0)}%","#66BB6A","#F1F8F2"),
        (ci4,"Retention Likelihood",f"{safe_int(row,'retention_pct',0)}%",C_BLUE,"#EFF4FB"),
    ]
    for col,label,val,color,bg in impact_data:
        with col:
            st.markdown(
                f'<div style="background:{bg};border-radius:10px;padding:18px;text-align:center;'
                f'border-bottom:3px solid {color}">'
                f'<div style="font-size:28px;font-weight:900;color:{color}">{val}</div>'
                f'<div style="font-size:11px;color:#555;margin-top:5px">{label}</div>'
                f'</div>', unsafe_allow_html=True
            )

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.plotly_chart(chart_impact(row), use_container_width=True, config={"displayModeBar":False})

    st.markdown(
        f'<div style="text-align:center;font-size:11px;color:#ccc;padding:18px 0 4px;'
        f'border-top:1px solid #eee;margin-top:6px">'
        f'Catalina Shopper Intelligence · GreenBasket Demo · Synthetic data for presentation purposes only</div>',
        unsafe_allow_html=True
    )


# ═════════════════════════════════════════════════════════════════════════════
# TAB 2 · SHOPPER VIEW
# ═════════════════════════════════════════════════════════════════════════════
with tab2:
    fname   = str(g(row,"name","Shopper")).split()[0]
    tier    = str(g(row,"loyalty_tier","Bronze"))
    tc_s    = TIER_COL.get(tier,"#777")
    pts_s   = safe_int(row,"points_balance",0)
    gap_s   = safe_int(row,"next_reward_gap",1)
    total_s = pts_s + gap_s
    prog_s  = int(pts_s / total_s * 100) if total_s > 0 else 0
    streak_s= safe_int(row,"streak_weeks",0)
    badges_s= [str(g(row,b,"")) for b in ["badge_1","badge_2","badge_3"]]
    badges_s= [b for b in badges_s if b and b != "—"]
    p_icon  = {"Health Pioneer":"🥦","Eco Explorer":"🌍","Family Organiser":"👨‍👩‍👧",
               "Budget-Conscious":"💰","Routine Loyalist":"🔁","Weekend Foodie":"🍷",
               "Eco-Progressive":"♻️","Convenience Seeker":"⚡"}.get(str(g(row,"persona","")), "👤")

    # Products for this shopper
    products_s = []
    for i in [1,2,3,4]:
        pname  = str(g(row,f"rec_p{i}_name","—"))
        pbrand = str(g(row,f"rec_p{i}_brand","—"))
        pprice = safe_float(row,f"rec_p{i}_price",2.99)
        ppts   = safe_int(row,f"rec_p{i}_pts",20)
        products_s.append((pname,pbrand,pprice,ppts))

    validity_map = {
        "Saturday":"Valid this Saturday only","Sunday":"Valid this Sunday only",
        "Weekend":"Valid this weekend","Friday":"Valid this Friday",
        "Friday Evening":"Valid this Friday evening","Thursday":"Valid this Thursday",
        "Wednesday":"Valid this Wednesday","Monday Morning":"Valid this Monday morning",
    }
    validity = validity_map.get(str(g(row,"activation_timing","—")), "Valid this week")
    ch_s = str(g(row,"activation_channel","—"))
    ch_icon_s = CH_ICON.get(ch_s,"📣")

    # Mission
    mission_msg  = str(g(row,"activation_message","—"))
    mission_type = str(g(row,"activation_offer_type","—"))

    # Badge chips HTML
    badge_rows_html = ""
    for b in badges_s:
        icon = BADGE_ICON.get(b,"🏅")
        badge_rows_html += (
            f'<div style="display:flex;align-items:center;gap:10px;background:#fff;'
            f'border-radius:10px;padding:10px 14px;box-shadow:0 2px 6px rgba(0,0,0,.05)">'
            f'<span style="font-size:22px">{icon}</span>'
            f'<div><div style="font-size:13px;font-weight:700;color:#222">{b}</div>'
            f'<div style="font-size:10px;color:#aaa">Earned badge</div></div>'
            f'</div>'
        )
    if not badge_rows_html:
        badge_rows_html = '<div style="font-size:13px;color:#aaa;padding:6px 0">Complete missions to earn your first badge</div>'

    # Product cards HTML
    prod_cards_html = ""
    for pname, pbrand, pprice, ppts in products_s:
        prod_cards_html += (
            f'<div style="background:#fff;border-radius:14px;padding:14px 12px;'
            f'box-shadow:0 2px 8px rgba(0,0,0,.07);text-align:center;border-bottom:3px solid {C_GREEN}">'
            f'<div style="font-size:11px;font-weight:700;color:#222;margin-bottom:3px">{pname}</div>'
            f'<div style="font-size:10px;color:#aaa;margin-bottom:8px">{pbrand}</div>'
            f'<div style="font-size:13px;font-weight:700;color:{C_BLUE};margin-bottom:4px">€{pprice:.2f}</div>'
            f'<div style="font-size:12px;font-weight:800;color:{C_AMBER}">+{ppts} pts</div>'
            f'</div>'
        )

    _, col_center, _ = st.columns([1,1.6,1])
    with col_center:

        # 1 · Greeting
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#003478 0%,#0058b8 100%);
                    border-radius:16px;padding:24px 22px 20px;margin-bottom:14px;
                    box-shadow:0 4px 18px rgba(0,52,120,.25)">
          <div style="font-size:10px;color:#90BBE8;letter-spacing:2px;text-transform:uppercase;margin-bottom:6px">
            GreenBasket Rewards
          </div>
          <div style="font-size:24px;font-weight:900;color:#fff;margin-bottom:12px">
            Hello, {fname}! 👋
          </div>
          <div style="display:flex;gap:8px;flex-wrap:wrap">
            <div style="background:{tc_s};color:#fff;padding:5px 14px;border-radius:20px;
                        font-size:12px;font-weight:700">★ {tier} Member</div>
            <div style="background:rgba(255,255,255,.15);color:#fff;padding:5px 14px;
                        border-radius:20px;font-size:12px">{p_icon} {g(row,'persona')}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # 2 · Points + streak
        st.markdown(f"""
        <div style="background:#fff;border-radius:16px;padding:20px 20px 16px;
                    margin-bottom:14px;box-shadow:0 2px 10px rgba(0,0,0,.07)">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:14px">
            <div>
              <div style="font-size:10px;color:#aaa;text-transform:uppercase;letter-spacing:1.2px;margin-bottom:4px">
                Your Points
              </div>
              <div style="font-size:40px;font-weight:900;color:{C_BLUE};line-height:1">{pts_s:,}</div>
              <div style="font-size:11px;color:#aaa;margin-top:4px">{gap_s:,} pts to next reward</div>
            </div>
            <div style="text-align:right">
              <div style="font-size:10px;color:#aaa;text-transform:uppercase;letter-spacing:1.2px;margin-bottom:4px">
                Streak
              </div>
              <div style="font-size:32px;font-weight:900;color:{C_AMBER}">🔥 {streak_s}w</div>
            </div>
          </div>
          <div style="background:#EAECEF;border-radius:7px;height:10px;overflow:hidden;margin-bottom:5px">
            <div style="width:{prog_s}%;height:10px;border-radius:7px;
                        background:linear-gradient(90deg,{C_BLUE},{C_BLUE}bb)"></div>
          </div>
          <div style="display:flex;justify-content:space-between;font-size:11px;color:#aaa">
            <span>Progress to next reward</span>
            <span style="font-weight:700;color:{C_BLUE}">{prog_s}%</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # 3 · Active mission
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,{C_LTBL} 0%,#DEEEFF 100%);
                    border:1.5px solid #C5DCEF;border-radius:16px;padding:18px 20px;margin-bottom:14px">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
            <div style="font-size:11px;font-weight:700;color:{C_BLUE};text-transform:uppercase;letter-spacing:1px">
              Your Active Mission
            </div>
            <span style="background:{C_GREEN};color:#fff;font-size:10px;font-weight:700;
                         padding:3px 11px;border-radius:20px">{mission_type}</span>
          </div>
          <div style="font-size:15px;font-weight:700;color:#1a1a2e;line-height:1.6;margin-bottom:14px">
            {mission_msg}
          </div>
          <div style="display:flex;gap:10px">
            <div style="flex:1;background:rgba(255,255,255,.85);border-radius:10px;padding:10px 12px">
              <div style="font-size:10px;color:#aaa;text-transform:uppercase;letter-spacing:1px;margin-bottom:3px">Channel</div>
              <div style="font-size:13px;font-weight:700;color:#333">{ch_icon_s} {ch_s}</div>
            </div>
            <div style="flex:1;background:rgba(255,255,255,.85);border-radius:10px;padding:10px 12px">
              <div style="font-size:10px;color:#aaa;text-transform:uppercase;letter-spacing:1px;margin-bottom:3px">Valid</div>
              <div style="font-size:13px;font-weight:700;color:{C_RED}">⏰ {validity}</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # 4 · Recommended products
        st.markdown(
            f'<div style="font-size:11px;font-weight:700;color:{C_BLUE};text-transform:uppercase;'
            f'letter-spacing:1.5px;margin:4px 0 10px;padding-bottom:6px;border-bottom:2px solid {C_LTBL}">'
            f'Recommended For You</div>', unsafe_allow_html=True
        )
        st.markdown(
            f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:18px">'
            f'{prod_cards_html}</div>', unsafe_allow_html=True
        )

        # 5 · Badges
        st.markdown(
            f'<div style="font-size:11px;font-weight:700;color:{C_BLUE};text-transform:uppercase;'
            f'letter-spacing:1.5px;margin:4px 0 10px;padding-bottom:6px;border-bottom:2px solid {C_LTBL}">'
            f'Your Badges</div>', unsafe_allow_html=True
        )
        st.markdown(
            f'<div style="display:flex;flex-direction:column;gap:8px;margin-bottom:20px">'
            f'{badge_rows_html}</div>', unsafe_allow_html=True
        )

        # 6 · CTA
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,{C_RED} 0%,#E53935 100%);
                    border-radius:14px;padding:20px;text-align:center;
                    box-shadow:0 4px 16px rgba(204,0,0,.28);margin-bottom:10px">
          <div style="font-size:17px;font-weight:900;color:#fff;letter-spacing:.4px">Activate Offer</div>
          <div style="font-size:11px;color:rgba(255,255,255,.75);margin-top:4px">Tap to unlock your personalised deal</div>
        </div>
        <div style="text-align:center;font-size:10px;color:#ccc;padding:10px 0 4px">
          GreenBasket · Powered by Catalina
        </div>
        """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# TAB 3 · CHECKOUT JOURNEY
# ═════════════════════════════════════════════════════════════════════════════
with tab3:

    # Reset step when shopper changes
    co_id = str(g(row,"shopper_id",""))
    if st.session_state.get("_co_id") != co_id:
        st.session_state["_co_id"]   = co_id
        st.session_state["_co_step"] = 0

    step = st.session_state.get("_co_step", 0)

    # Products & offer mechanics
    co_products = []
    for i in [1,2,3,4]:
        co_products.append({
            "name":  str(g(row,f"rec_p{i}_name","Product")),
            "brand": str(g(row,f"rec_p{i}_brand","Brand")),
            "price": safe_float(row,f"rec_p{i}_price",2.99),
            "pts":   safe_int(row,f"rec_p{i}_pts",20),
        })

    subtotal     = round(sum(p["price"] for p in co_products), 2)
    disc_pct     = safe_float(row,"offer_discount_pct",0)
    disc_eur     = safe_float(row,"offer_discount_eur",0)
    bonus_pts_co = safe_int(row,"offer_bonus_pts",0)
    offer_label  = str(g(row,"offer_mechanic","GreenBasket Offer"))
    discount_amt = round(min(subtotal * disc_pct / 100 + disc_eur, subtotal), 2)
    final_total  = round(subtotal - discount_amt, 2)
    basket_pts   = int(final_total)
    new_balance  = safe_int(row,"points_balance",0) + basket_pts + bonus_pts_co
    fname_co     = str(g(row,"name","Shopper")).split()[0]

    # Offer description line
    if disc_pct > 0:
        offer_desc = f"{disc_pct:.0f}% discount applied"
    elif disc_eur > 0:
        offer_desc = f"€{disc_eur:.2f} voucher applied"
    elif bonus_pts_co > 0:
        offer_desc = f"+{bonus_pts_co:,} bonus points added"
    else:
        offer_desc = "Loyalty bonus applied"

    # ── Step indicator ────────────────────────────────────────────────────────
    step_labels = ["Basket", "Checkout", "Offer Applied", "Confirmed"]
    parts = []
    for i, lbl in enumerate(step_labels):
        if i < step:
            bg, tc = C_GREEN, "#fff"
        elif i == step:
            bg, tc = C_BLUE, "#fff"
        else:
            bg, tc = "#EAECEF", "#999"
        parts.append(
            f'<div style="flex:1;padding:10px 6px;text-align:center;background:{bg};'
            f'font-size:11px;font-weight:700;color:{tc};letter-spacing:.3px">{lbl}</div>'
        )
    st.markdown(
        '<div style="display:flex;border-radius:10px;overflow:hidden;margin-bottom:20px">'
        + "".join(parts) + "</div>",
        unsafe_allow_html=True,
    )

    _, col_co, _ = st.columns([0.5, 2, 0.5])

    with col_co:

        # ── STEP 0 · Basket ───────────────────────────────────────────────────
        if step == 0:

            # Basket title
            st.markdown(f"""
            <div style="text-align:center;margin-bottom:16px">
              <div style="font-size:22px;font-weight:900;color:{C_BLUE}">{fname_co}'s Basket</div>
              <div style="font-size:12px;color:#aaa;margin-top:3px">
                {len(co_products)} items · Est. €{subtotal:.2f}
              </div>
            </div>
            """, unsafe_allow_html=True)

            # Item cards
            c_a, c_b = st.columns(2)
            for idx, p in enumerate(co_products):
                col = c_a if idx % 2 == 0 else c_b
                with col:
                    st.markdown(f"""
                    <div style="background:#fff;border-radius:12px;padding:13px;
                                box-shadow:0 2px 8px rgba(0,0,0,.07);
                                border-bottom:3px solid {C_BLUE};margin-bottom:10px;
                                display:flex;align-items:center;gap:10px">
                      <div style="flex:1;min-width:0">
                        <div style="font-size:12px;font-weight:700;color:#222">{p['name']}</div>
                        <div style="font-size:10px;color:#aaa">{p['brand']}</div>
                        <div style="font-size:11px;font-weight:600;color:{C_AMBER};margin-top:2px">+{p['pts']} pts</div>
                      </div>
                      <div style="font-size:15px;font-weight:900;color:{C_BLUE};flex-shrink:0">€{p['price']:.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)

            # Offer ready banner
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,{C_LTBL},#DEEEFF);
                        border:1.5px solid #C5DCEF;border-radius:12px;
                        padding:13px 16px;margin-bottom:16px">
              <div style="font-size:10px;color:{C_BLUE};font-weight:700;text-transform:uppercase;
                          letter-spacing:1px;margin-bottom:4px">🌿 GreenBasket Offer Ready</div>
              <div style="font-size:13px;font-weight:700;color:#222">{offer_label}</div>
              <div style="font-size:11px;color:#aaa;margin-top:2px">Applied automatically at checkout</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Proceed to Checkout →", use_container_width=True, key="btn_s0"):
                st.session_state["_co_step"] = 1
                st.rerun()

        # ── STEP 1 · Checkout ─────────────────────────────────────────────────
        elif step == 1:

            items_html = ""
            for p in co_products:
                items_html += (
                    f'<div style="display:flex;justify-content:space-between;align-items:center;'
                    f'padding:9px 0;border-bottom:1px solid #F0F0F0">'
                    f'<div>'
                    f'<div style="font-size:13px;color:#333;font-weight:500">{p["name"]}</div>'
                    f'<div style="font-size:10px;color:#aaa">{p["brand"]}</div>'
                    f'</div>'
                    f'<span style="font-size:13px;font-weight:600;color:#444">€{p["price"]:.2f}</span>'
                    f'</div>'
                )

            offer_pending = (
                f'<div style="display:flex;align-items:center;gap:10px;padding:11px 13px;'
                f'background:#FFF8E1;border-radius:8px;margin:10px 0;border:1.5px dashed {C_AMBER}">'
                f'<span style="font-size:18px">🌿</span>'
                f'<div>'
                f'<div style="font-size:11px;font-weight:700;color:#E65100">GreenBasket Offer Pending</div>'
                f'<div style="font-size:10px;color:#aaa">Tap below to apply your reward</div>'
                f'</div></div>'
            )

            receipt_html = (
                f'<div style="background:#fff;border-radius:16px;overflow:hidden;'
                f'box-shadow:0 4px 20px rgba(0,0,0,.10);margin-bottom:16px">'
                f'<div style="background:linear-gradient(135deg,{C_BLUE} 0%,#0059b3 100%);'
                f'padding:16px 22px;display:flex;justify-content:space-between;align-items:center">'
                f'<div>'
                f'<div style="font-size:10px;color:#90BBE8;letter-spacing:2px;text-transform:uppercase;margin-bottom:2px">Carrefour Market</div>'
                f'<div style="font-size:16px;font-weight:800;color:#fff">🛒 GreenBasket Checkout</div>'
                f'</div>'
                f'<div style="background:rgba(255,255,255,.18);border-radius:9px;padding:7px 14px;text-align:center">'
                f'<div style="font-size:10px;color:#90BBE8;margin-bottom:2px">Shopper</div>'
                f'<div style="font-size:13px;font-weight:800;color:#fff">{fname_co}</div>'
                f'</div></div>'
                f'<div style="padding:18px 22px">'
                f'{items_html}'
                f'<div style="display:flex;justify-content:space-between;padding:10px 0 4px;'
                f'border-top:2px solid #eee;margin-top:4px">'
                f'<span style="font-size:13px;color:#888">Subtotal</span>'
                f'<span style="font-size:13px;font-weight:600;color:#555">€{subtotal:.2f}</span>'
                f'</div>'
                f'{offer_pending}'
                f'<div style="display:flex;justify-content:space-between;padding:12px 0 4px;'
                f'border-top:3px solid #888;margin-top:6px">'
                f'<span style="font-size:16px;font-weight:900;color:#888">TOTAL</span>'
                f'<span style="font-size:16px;font-weight:900;color:#888">€{subtotal:.2f}</span>'
                f'</div></div></div>'
            )
            st.markdown(receipt_html, unsafe_allow_html=True)

            if st.button("Apply GreenBasket Offer 🌿", use_container_width=True, key="btn_s1"):
                st.session_state["_co_step"] = 2
                st.rerun()

        # ── STEP 2 · Offer Applied ────────────────────────────────────────────
        elif step == 2:

            items_html = ""
            for p in co_products:
                items_html += (
                    f'<div style="display:flex;justify-content:space-between;align-items:center;'
                    f'padding:9px 0;border-bottom:1px solid #F0F0F0">'
                    f'<div>'
                    f'<div style="font-size:13px;color:#333;font-weight:500">{p["name"]}</div>'
                    f'<div style="font-size:10px;color:#aaa">{p["brand"]}</div>'
                    f'</div>'
                    f'<span style="font-size:13px;font-weight:600;color:#444">€{p["price"]:.2f}</span>'
                    f'</div>'
                )

            if discount_amt > 0:
                saving_html = f'<span style="font-size:14px;font-weight:900;color:{C_GREEN}">−€{discount_amt:.2f}</span>'
            else:
                saving_html = f'<span style="font-size:14px;font-weight:900;color:{C_GREEN}">✓ Applied</span>'

            offer_applied = (
                f'<div style="display:flex;justify-content:space-between;align-items:center;'
                f'padding:11px 14px;background:#E8F5E9;border-radius:8px;margin:10px 0;border-left:4px solid {C_GREEN}">'
                f'<div>'
                f'<div style="font-size:10px;color:{C_GREEN};font-weight:700;text-transform:uppercase;letter-spacing:1px">'
                f'🌿 GreenBasket Offer Applied</div>'
                f'<div style="font-size:12px;color:#2E7D32;margin-top:2px">{offer_desc}</div>'
                f'</div>'
                f'{saving_html}</div>'
            )

            receipt_html = (
                f'<div style="background:#fff;border-radius:16px;overflow:hidden;'
                f'box-shadow:0 4px 20px rgba(0,0,0,.10);margin-bottom:16px">'
                f'<div style="background:linear-gradient(135deg,{C_BLUE} 0%,#0059b3 100%);'
                f'padding:16px 22px;display:flex;justify-content:space-between;align-items:center">'
                f'<div>'
                f'<div style="font-size:10px;color:#90BBE8;letter-spacing:2px;text-transform:uppercase;margin-bottom:2px">Carrefour Market</div>'
                f'<div style="font-size:16px;font-weight:800;color:#fff">🛒 GreenBasket Checkout</div>'
                f'</div>'
                f'<div style="background:rgba(255,255,255,.18);border-radius:9px;padding:7px 14px;text-align:center">'
                f'<div style="font-size:10px;color:#90BBE8;margin-bottom:2px">Shopper</div>'
                f'<div style="font-size:13px;font-weight:800;color:#fff">{fname_co}</div>'
                f'</div></div>'
                f'<div style="padding:18px 22px">'
                f'{items_html}'
                f'<div style="display:flex;justify-content:space-between;padding:10px 0 4px;'
                f'border-top:2px solid #eee;margin-top:4px">'
                f'<span style="font-size:13px;color:#888">Subtotal</span>'
                f'<span style="font-size:13px;font-weight:600;color:#555">€{subtotal:.2f}</span>'
                f'</div>'
                f'{offer_applied}'
                f'<div style="display:flex;justify-content:space-between;padding:12px 0 4px;'
                f'border-top:3px solid {C_BLUE};margin-top:6px">'
                f'<span style="font-size:16px;font-weight:900;color:{C_BLUE}">TOTAL</span>'
                f'<span style="font-size:16px;font-weight:900;color:{C_BLUE}">€{final_total:.2f}</span>'
                f'</div></div></div>'
            )
            st.markdown(receipt_html, unsafe_allow_html=True)

            if st.button("Confirm Payment →", use_container_width=True, key="btn_s2"):
                st.session_state["_co_step"] = 3
                st.rerun()

        # ── STEP 3 · Confirmed ────────────────────────────────────────────────
        elif step >= 3:
            st.balloons()

            badge_name = badges_s[0] if badges_s else "GreenBasket Member"
            badge_icon = BADGE_ICON.get(badge_name, "🏅")

            confirmed_html = (
                f'<div style="background:linear-gradient(135deg,#E8F5E9 0%,#C8E6C9 100%);'
                f'border:2px solid {C_GREEN};border-radius:16px;padding:26px 22px 22px;'
                f'text-align:center;box-shadow:0 4px 18px rgba(46,125,50,.18);margin-bottom:14px">'
                f'<div style="font-size:46px;margin-bottom:10px">✅</div>'
                f'<div style="font-size:10px;color:{C_GREEN};font-weight:700;text-transform:uppercase;'
                f'letter-spacing:2px;margin-bottom:6px">Payment Confirmed</div>'
                f'<div style="font-size:28px;font-weight:900;color:#1B5E20;margin-bottom:4px">€{final_total:.2f} paid</div>'
                f'<div style="font-size:13px;color:#388E3C;margin-bottom:20px">{offer_desc}</div>'
                f'<div style="background:rgba(255,255,255,.75);border-radius:12px;padding:16px 18px;display:flex">'
                f'<div style="flex:1;text-align:center;padding:0 8px">'
                f'<div style="font-size:10px;color:#aaa;text-transform:uppercase;letter-spacing:1px;margin-bottom:5px">Basket Points</div>'
                f'<div style="font-size:26px;font-weight:900;color:{C_BLUE}">+{basket_pts}</div>'
                f'</div>'
                f'<div style="width:1px;background:#ddd;margin:0 4px"></div>'
                f'<div style="flex:1;text-align:center;padding:0 8px">'
                f'<div style="font-size:10px;color:#aaa;text-transform:uppercase;letter-spacing:1px;margin-bottom:5px">Bonus Points</div>'
                f'<div style="font-size:26px;font-weight:900;color:{C_GREEN}">+{bonus_pts_co}</div>'
                f'</div>'
                f'<div style="width:1px;background:#ddd;margin:0 4px"></div>'
                f'<div style="flex:1;text-align:center;padding:0 8px">'
                f'<div style="font-size:10px;color:#aaa;text-transform:uppercase;letter-spacing:1px;margin-bottom:5px">New Balance</div>'
                f'<div style="font-size:26px;font-weight:900;color:{C_AMBER}">{new_balance:,}</div>'
                f'</div></div></div>'
                f'<div style="background:#fff;border-radius:14px;padding:18px 20px;'
                f'box-shadow:0 2px 10px rgba(0,0,0,.07);text-align:center;'
                f'border-top:4px solid {C_AMBER};margin-bottom:16px">'
                f'<div style="font-size:36px;margin-bottom:8px">{badge_icon}</div>'
                f'<div style="font-size:10px;color:{C_AMBER};font-weight:700;text-transform:uppercase;'
                f'letter-spacing:1.5px;margin-bottom:5px">Badge Progress</div>'
                f'<div style="font-size:16px;font-weight:800;color:#333">{badge_name}</div>'
                f'<div style="font-size:12px;color:#aaa;margin-top:4px">Keep shopping to unlock your next reward</div>'
                f'</div>'
            )
            st.markdown(confirmed_html, unsafe_allow_html=True)

        # ── Reset button (always shown below step >= 1) ───────────────────────
        if step > 0:
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            if st.button("↺  Start Over", use_container_width=True, key="btn_reset"):
                st.session_state["_co_step"] = 0
                st.rerun()
