import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# --- CONFIGURATION ---
st.set_page_config(page_title="EVEYES 360 RPM Platinum", layout="wide", page_icon="🏥")

# --- DATA STORAGE SIMULATION ---
if 'patient_db' not in st.session_state:
    # Creating a 5-day history for trend analysis
    st.session_state.patient_db = pd.DataFrame({
        'Date': [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(4, -1, -1)],
        'Weight': [75.0, 74.8, 75.2, 77.5, 78.0],
        'BIA_Muscle': [32.0, 31.9, 32.1, 32.0, 31.8],
        'Systolic': [120, 122, 125, 145, 150],
        'SpO2': [98, 97, 98, 96, 94],
        'Pain': [4, 4, 5, 7, 8]
    })

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🏥 EVEYES 360 RPM")
user_role = st.sidebar.selectbox("System Access", ["Patient Portal", "Specialist Dashboard"])

# ==========================================
# 1. PATIENT PORTAL
# ==========================================
if user_role == "Patient Portal":
    st.title("📱 Patient Clinical Terminal")
    
    tabs = st.tabs(["🏠 My Dashboard", "📝 Daily Input", "📤 Reports & Dispatch"])

    # --- TAB 1: THE OLD FAVORITE DASHBOARD (Yesterday vs Today) ---
    with tabs[0]:
        st.subheader("🔄 24-Hour Clinical Comparison")
        df = st.session_state.patient_db
        
        # Calculate Deltas
        w_diff = df['Weight'].iloc[-1] - df['Weight'].iloc[-2]
        s_diff = df['Systolic'].iloc[-1] - df['Systolic'].iloc[-2]
        p_diff = df['Pain'].iloc[-1] - df['Pain'].iloc[-2]
        b_diff = df['BIA_Muscle'].iloc[-1] - df['BIA_Muscle'].iloc[-2]

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Current Weight", f"{df['Weight'].iloc[-1]} kg", f"{w_diff:.1f} kg", delta_color="inverse")
        c2.metric("Systolic BP", f"{df['Systolic'].iloc[-1]} mmHg", f"{s_diff:+d}", delta_color="inverse")
        c3.metric("Pain Level", f"{df['Pain'].iloc[-1]}/10", f"{p_diff:+d}", delta_color="inverse")
        c4.metric("Muscle Mass (BIA)", f"{df['BIA_Muscle'].iloc[-1]} kg", f"{b_diff:.1f} kg")

        st.divider()
        st.subheader("📈 Trend Visualization")
        st.line_chart(df.set_index('Date')[['Weight', 'Systolic', 'Pain']])

    # --- TAB 2: DATA INTAKE ---
    with tabs[1]:
        st.subheader("Enter Daily Measurements")
        with st.form("input_form"):
            col1, col2, col3 = st.columns(3)
            new_w = col1.number_input("Weight (kg)", 30.0, 250.0, 78.0)
            new_s = col2.number_input("Systolic BP", 50, 250, 150)
            new_sp = col3.number_input("SpO2 (%)", 50, 100, 94)
            new_p = st.slider("Pain Level", 0, 10, 8)
            save = st.form_submit_button("💾 Save to Record")
            if save: st.success("Data stored in clinical history.")

    # --- TAB 3: SMART REPORTING & AUTO-SEND ---
    with tabs[2]:
        st.subheader("📊 Clinical Statistical Report")
        
        if st.button("📝 Generate & Analyze Statistics"):
            df = st.session_state.patient_db
            
            # Statistical Interpretations
            avg_bp = df['Systolic'].mean()
            weight_trend = "INCREASING" if w_diff > 0 else "DECREASING"
            
            report_body = f"""
🏥 EVEYES 360 CLINICAL ANALYTICS REPORT
--------------------------------------
Patient: John Doe | Category: Chronic Care
Date of Report: {datetime.now().strftime('%Y-%m-%d')}

1. STATISTICAL SUMMARY:
- Weight Trend: {weight_trend} ({w_diff:+.1f} kg in
