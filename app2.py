import streamlit as st
import numpy as np
import pickle

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Mobile Price Predictor",
    page_icon="📱",
    layout="wide"
)

# ── Load model & scaler ───────────────────────────────────────────────────────
model  = pickle.load(open("mobile_price_model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* General */
    .main { background-color: #f8f9fb; }
    .block-container { padding: 2rem 3rem; }

    /* Header */
    .app-header {
        background: linear-gradient(135deg, #534AB7, #1D9E75);
        padding: 2.5rem 2rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
    }
    .app-header h1 { font-size: 2.2rem; font-weight: 700; margin: 0; }
    .app-header p  { font-size: 1rem; opacity: 0.9; margin: 0.5rem 0 0; }

    /* Section cards */
    .section-card {
        background: white;
        border-radius: 14px;
        padding: 1.5rem 1.8rem;
        border: 1px solid #e8eaf0;
        margin-bottom: 1.2rem;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }
    .section-title {
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #888;
        margin-bottom: 1.1rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .dot {
        width: 8px; height: 8px;
        border-radius: 50%;
        display: inline-block;
    }

    /* Predict button */
    .stButton > button {
        width: 100%;
        padding: 0.85rem;
        background: linear-gradient(135deg, #534AB7, #3C3489);
        color: white;
        font-size: 1.05rem;
        font-weight: 600;
        border: none;
        border-radius: 12px;
        cursor: pointer;
        letter-spacing: 0.03em;
        margin-top: 0.5rem;
    }
    .stButton > button:hover { opacity: 0.9; }

    /* Result cards */
    .result-box {
        border-radius: 14px;
        padding: 1.8rem 2rem;
        text-align: center;
        margin-top: 1rem;
        border: 1.5px solid;
    }
    .result-label  { font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.07em; opacity: 0.7; }
    .result-value  { font-size: 2rem; font-weight: 700; margin: 0.3rem 0 0.2rem; }
    .result-sub    { font-size: 0.9rem; opacity: 0.75; }
    .result-range  { font-size: 0.78rem; margin-top: 0.5rem; opacity: 0.6; }

    /* Range indicator pills */
    .range-row { display: flex; gap: 8px; justify-content: center; margin-top: 1rem; }
    .range-pill {
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 600;
        background: #f0f0f0;
        color: #aaa;
    }
    .range-pill.active-0 { background: #EAF3DE; color: #3B6D11; }
    .range-pill.active-1 { background: #FAEEDA; color: #854F0B; }
    .range-pill.active-2 { background: #E1F5EE; color: #085041; }
    .range-pill.active-3 { background: #FCEBEB; color: #A32D2D; }

    /* Accuracy badge */
    .acc-badge {
        display: inline-block;
        background: #EAF3DE;
        color: #3B6D11;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }

    /* Divider */
    hr { border: none; border-top: 1px solid #eee; margin: 1.5rem 0; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <h1>📱 Mobile Price Predictor</h1>
    <p>Enter phone specifications below to predict the price range</p>
</div>
""", unsafe_allow_html=True)

# ── Input Sections ────────────────────────────────────────────────────────────

# ROW 1 — Hardware + Camera
col1, col2 = st.columns(2)

with col1:
    st.markdown("""<div class="section-card">
    <div class="section-title"><span class="dot" style="background:#534AB7"></span>Hardware Specs</div>
    """, unsafe_allow_html=True)

    battery_power = st.number_input("🔋 Battery Power (mAh)", min_value=500,  max_value=2000, value=1500)
    ram           = st.number_input("💾 RAM (MB)",             min_value=256,  max_value=4000, value=2048)
    int_memory    = st.number_input("📦 Internal Memory (GB)", min_value=2,    max_value=64,   value=16)
    clock_speed   = st.number_input("⚡ Clock Speed (GHz)",    min_value=0.5,  max_value=3.0,  value=1.5, step=0.1)
    n_cores       = st.number_input("🔧 Number of Cores",      min_value=1,    max_value=8,    value=4)
    mobile_wt     = st.number_input("⚖️ Mobile Weight (g)",    min_value=80,   max_value=200,  value=140)
    m_dep         = st.number_input("📐 Mobile Depth (cm)",    min_value=0.1,  max_value=1.0,  value=0.5, step=0.1)
    talk_time     = st.number_input("📞 Talk Time (hours)",    min_value=2,    max_value=20,   value=10)

    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("""<div class="section-card">
    <div class="section-title"><span class="dot" style="background:#1D9E75"></span>Camera & Display</div>
    """, unsafe_allow_html=True)

    pc         = st.number_input("📷 Primary Camera (MP)",  min_value=0,  max_value=20, value=8)
    fc         = st.number_input("🤳 Front Camera (MP)",    min_value=0,  max_value=20, value=5)
    sc_h       = st.number_input("📏 Screen Height (cm)",   min_value=5,  max_value=19, value=12)
    sc_w       = st.number_input("📏 Screen Width (cm)",    min_value=0,  max_value=18, value=6)
    px_height  = st.number_input("🖥️ Pixel Height",         min_value=0,  max_value=1960, value=720)
    px_width   = st.number_input("🖥️ Pixel Width",          min_value=500, max_value=1998, value=1080)

    st.markdown("</div>", unsafe_allow_html=True)

# ROW 2 — Connectivity
st.markdown("""<div class="section-card">
<div class="section-title"><span class="dot" style="background:#378ADD"></span>Connectivity Features</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1: blue        = 1 if st.checkbox("📶 Bluetooth",    value=True)  else 0
with c2: four_g      = 1 if st.checkbox("📡 4G",           value=True)  else 0
with c3: dual_sim    = 1 if st.checkbox("📲 Dual SIM",     value=False) else 0
with c4: three_g     = 1 if st.checkbox("📡 3G",           value=True)  else 0
with c5: touch_screen= 1 if st.checkbox("👆 Touch Screen", value=True)  else 0
with c6: wifi        = 1 if st.checkbox("📶 WiFi",         value=True)  else 0

st.markdown("</div>", unsafe_allow_html=True)

# ── Predict Button ────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
predict_clicked = st.button("🔍 Predict Price Category")

# ── Prediction Logic ──────────────────────────────────────────────────────────
if predict_clicked:

    # Build input in EXACT column order as training data
    input_data = np.array([[
        battery_power, blue, clock_speed, dual_sim, fc,
        four_g, int_memory, m_dep, mobile_wt, n_cores,
        pc, px_height, px_width, ram, sc_h,
        sc_w, talk_time, three_g, touch_screen, wifi
    ]])

    # Scale input using saved scaler
    input_scaled = scaler.transform(input_data)

    # Predict
    prediction = model.predict(input_scaled)[0]

    # Result config
    result_config = {
        0: {
            "label": "Low Cost Phone",
            "emoji": "💵",
            "sub": "Budget-friendly device",
            "range_text": "Price Range: 0 (Lowest)",
            "bg": "#EAF3DE",
            "border": "#3B6D11",
            "text": "#3B6D11"
        },
        1: {
            "label": "Medium Cost Phone",
            "emoji": "💳",
            "sub": "Mid-range device",
            "range_text": "Price Range: 1 (Medium)",
            "bg": "#FAEEDA",
            "border": "#854F0B",
            "text": "#854F0B"
        },
        2: {
            "label": "High Cost Phone",
            "emoji": "💰",
            "sub": "Premium device",
            "range_text": "Price Range: 2 (High)",
            "bg": "#E1F5EE",
            "border": "#085041",
            "text": "#085041"
        },
        3: {
            "label": "Very High Cost Phone",
            "emoji": "💎",
            "sub": "Flagship device",
            "range_text": "Price Range: 3 (Highest)",
            "bg": "#FCEBEB",
            "border": "#A32D2D",
            "text": "#A32D2D"
        }
    }

    r = result_config[prediction]

    # Range pills HTML
    pills = ""
    names = ["Low", "Medium", "High", "Very High"]
    for i, name in enumerate(names):
        active_class = f"active-{i}" if i == prediction else ""
        pills += f'<div class="range-pill {active_class}">{name}</div>'

    st.markdown(f"""
    <div class="result-box" style="background:{r['bg']}; border-color:{r['border']};">
        <div class="result-label" style="color:{r['text']}">Predicted Price Category</div>
        <div class="result-value" style="color:{r['text']}">{r['emoji']} {r['label']}</div>
        <div class="result-sub" style="color:{r['text']}">{r['sub']}</div>
        <div class="result-range" style="color:{r['text']}">{r['range_text']}</div>
        <div class="range-row">{pills}</div>
    </div>
    <div style="text-align:center; margin-top:0.8rem;">
        <span class="acc-badge">✅ Model Accuracy: 97.5% (Logistic Regression)</span>
    </div>
    """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("""
<p style="text-align:center; color:#aaa; font-size:0.78rem;">
    Built with Streamlit · Logistic Regression · Scikit-learn
</p>
""", unsafe_allow_html=True)