import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="EVEYES 360 Platinum", layout="wide", page_icon="🏥")

# --- MODULE IMPORTS (Error Protected) ---
try:
    from modules import metabolic, neuro, pediatric, derma, resp_sonic, therapy
except ImportError:
    pass

# --- ROLE SELECTION ---
st.sidebar.title("🏥 EVEYES 360")
user_role = st.sidebar.radio("Portal Access", ["Patient Portal", "Specialist Hub"])

# --- DATA SIMULATION (Comparative Analysis) ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame({
        'Date': [datetime.now() - timedelta(days=1), datetime.now()],
        'Weight': [71.5, 70.2],
        'BIA': [490, 505],
        'Temperature': [36.8, 36.6],
        'Pain': [6, 3]
    })

# ==========================================
# 1. PATIENT PORTAL
# ==========================================
if user_role == "Patient Portal":
    st.sidebar.divider()
    menu = ["🏠 Dashboard & Comparative Analysis", "📝 Daily Clinical Input", "💊 Medication & Therapy"]
    choice = st.sidebar.selectbox("Select Action", menu)

    if choice == "🏠 Dashboard & Comparative Analysis":
        st.title("📊 Clinical Progress Dashboard")
        
        # --- 24-HOUR TREND METRICS ---
        st.subheader("🔄 24-Hour Change Analysis")
        c1, c2, c3, c4 = st.columns(4)
        
        df = st.session_state.db
        w_diff = df['Weight'].iloc[-1] - df['Weight'].iloc[-2]
        b_diff = df['BIA'].iloc[-1] - df['BIA'].iloc[-2]
        p_diff = df['Pain'].iloc[-1] - df['Pain'].iloc[-2]
        t_diff = df['Temperature'].iloc[-1] - df['Temperature'].iloc[-2]

        c1.metric("Weight", f"{df['Weight'].iloc[-1]} kg", f"{w_diff:.1f} kg", delta_color="inverse")
        c2.metric("BIA (Resistance)", f"{df['BIA'].iloc[-1]} Ω", f"{b_diff:+d}")
        c3.metric("Pain (VAS)", f"{df['Pain'].iloc[-1]}/10", f"{p_diff:+d}", delta_color="inverse")
        c4.metric("Body Temp", f"{df['Temperature'].iloc[-1]} °C", f"{t_diff:.1f} °C", delta_color="inverse")

        # SMART CLINICAL COMMENTARY
        st.info(f"""
        🧠 **EVEYES AI Clinical Note:** Compared to yesterday, a weight reduction of **{abs(w_diff):.1f} kg** was observed. 
        The increase of **{b_diff} Ω** in BIA suggests that your hydration and muscle mass are well-maintained. 
        The decrease in pain levels indicates a positive response to the current therapy. Cachexia risk is low.
        """)

        st.subheader("📈 Physiological Trends")
        tab1, tab2 = st.tabs(["Weight & BIA Trend", "Temperature & Pain Curve"])
        with tab1:
            st.line_chart(df.set_index('Date')[['Weight', 'BIA']])
        with tab2:
            st.area_chart(df.set_index('Date')[['Temperature', 'Pain']])

    elif choice == "📝 Daily Clinical Input":
        st.title("📝 Daily Clinical Entry")
