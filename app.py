import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- CONFIGURATION ---
st.set_page_config(page_title="EVEYES 360 Platinum", layout="wide")

# --- DATA ENGINE (Yesterday vs Today Logic) ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame({
        'Date': [datetime.now() - timedelta(days=1), datetime.now()],
        'Weight': [71.5, 70.2],
        'BIA': [490, 505],
        'Systolic': [125, 145], # Example of a spike
        'SpO2': [98, 96],
        'Pain': [6, 3]
    })

# --- SIDEBAR ---
st.sidebar.title("🏥 EVEYES 360")
user_role = st.sidebar.radio("Portal Access", ["Patient Portal", "Specialist Hub"])

if user_role == "Patient Portal":
    menu = ["🏠 Dashboard (Compare & Analyze)", "📝 Daily Clinical Entry", "💊 Therapy Tracker"]
    choice = st.sidebar.selectbox("Navigation", menu)

    # --- THE IMPROVED OLD DASHBOARD ---
    if choice == "🏠 Dashboard (Compare & Analyze)":
        st.title("📊 Clinical Progress: Yesterday vs Today")
        
        df = st.session_state.db
        # Calculate Deltas
        w_diff = df['Weight'].iloc[-1] - df['Weight'].iloc[-2]
        b_diff = df['BIA'].iloc[-1] - df['BIA'].iloc[-2]
        p_diff = df['Pain'].iloc[-1] - df['Pain'].iloc[-2]
        s_diff = df['Systolic'].iloc[-1] - df['Systolic'].iloc[-2]

        # --- KEY METRICS (Original Layout) ---
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Weight", f"{df['Weight'].iloc[-1]} kg", f"{w_diff:.1f} kg", delta_color="inverse")
        c2.metric("BIA (Muscle/Fluid)", f"{df['BIA'].iloc[-1]} Ω", f"{b_diff:+d}")
        c3.metric("Pain Level", f"{df['Pain'].iloc[-1]}/10", f"{p_diff:+d}", delta_color="inverse")
        c4.metric("Systolic BP", f"{df['Systolic'].iloc[-1]} mmHg", f"{s_diff:+d}", delta_color="inverse")

        # --- AI CLINICAL INSIGHT ---
        st.info(f"""
        🧠 **EVEYES AI Analysis:** Your weight decreased by **{abs(w_diff):.1f} kg**, while BIA increased by **{b_diff} Ω**. 
        This suggests healthy fluid loss while maintaining muscle mass. However, your Blood Pressure rose by **{s_diff} units**; please monitor closely.
        """)
        
        st.subheader("📈 Physiological Trends")
        st.line_chart(df.set_index('Date')[['Weight', 'BIA', 'Systolic']])

    # --- DAILY ENTRY WITH AUTO-ALERTS ---
    elif choice == "📝 Daily Clinical Entry":
        st.title("📝 Data Intake & Emergency Check")
        
        with st.form("clinical_form"):
            col_a, col_b, col_c = st.columns(3)
            weight = col_a.number_input("Current Weight (kg)", 30.0, 200)

