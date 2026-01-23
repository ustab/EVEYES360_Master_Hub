import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# --- CONFIGURATION & STYLING ---
st.set_page_config(page_title="EVEYES 360 RPM", layout="wide", page_icon="🏥")

# --- DATA STORAGE SIMULATION ---
if 'patient_db' not in st.session_state:
    st.session_state.patient_db = pd.DataFrame({
        'Date': [datetime.now() - timedelta(days=i) for i in range(5, 0, -1)],
        'Weight': [75.0, 74.8, 75.2, 77.5, 78.0], # Simulated edema spike
        'BIA_Muscle': [32.0, 31.9, 32.1, 32.0, 31.8],
        'Systolic': [120, 122, 125, 145, 150], # Simulated hypertension trend
        'SpO2': [98, 97, 98, 96, 94] # Simulated respiratory decline
    })

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🏥 EVEYES 360 RPM")
user_role = st.sidebar.selectbox("System Access", ["Patient Portal", "Specialist Dashboard"])

# ==========================================
# 1. PATIENT PORTAL (Data Intake & Validation)
# ==========================================
if user_role == "Patient Portal":
    st.title("📱 Patient Clinical Input Terminal")
    
    # Target Group Selection for Contextual Input
    patient_group = st.sidebar.selectbox("Patient Category", 
        ["Chronic Care", "Geriatric", "Post-Operative", "High-Risk Pregnancy", "Rehabilitation"])

    tabs = st.tabs(["📝 Vitals & BIA", "📷 Visual Scan", "📊 My Trends"])

    with tabs[0]:
        st.subheader("Physical & Biometric Data")
        c1, c2, c3 = st.columns(3)
        
        # Section A: Input Validation (Hard Limits Implementation)
        weight = c1.number_input("Weight (kg)", min_value=30.0, max_value=250.0, value=75.0)
        systolic = c2.number_input("Systolic BP (mmHg)", min_value=50, max_value=250, value=120)
        spo2 = c3.number_input("SpO2 (%)", min_value=50, max_value=100, value=98)
        
        # Section B: BIA Entegration
        bia_muscle = st.slider("BIA Muscle Mass (kg)", 10.0, 60.0, 32.0)
        
        if systolic > 180 or spo2 < 90:
            st.error("⚠️ CRITICAL VALUES DETECTED: Please contact your doctor immediately or call emergency services.")

    with tabs[1]:
        st.subheader("Camera & Imaging Analysis")
        scan_type = st.selectbox("Scan Type", ["Wound Recovery", "Movement/Range of Motion", "Edema Check"])
        st.camera_input("Capture Clinical Evidence")
        st.file_uploader("Upload Movement Video (Rehab/Gait)", type=["mp4", "mov"])

    with tabs[2]:
        st.subheader("Personal Progress Report")
        df = st.session_state.patient_db
        st.line_chart(df.set_index('Date')[['Weight', 'Systolic']])
        
    if st.button("📤 Sync Data to Clinical Hub"):
        st.success("Data validated and transmitted successfully.")
        st.balloons()

# ==========================================
# 2. SPECIALIST DASHBOARD (Decision Support)
# ==========================================
else:
    st.title("👨‍⚕️ Specialist Decision Support System")
    
    # 4. Triage System (Priority Categorization)
    st.subheader("🚨 Patient Triage & Alerts")
    t1, t2, t3 = st.columns(3)
    t1.metric("Critical (Red)", "2 Patients", "Action Required", delta_color="inverse")
    t2.metric("Stable", "14 Patients", "Normal")
    t3.metric("Follow-up", "5 Patients", "Pending Review")

    st.divider()

    # 3. Smart Data Processing (Anomaly & Correlation)
    st.subheader("🔍 Smart Trend Analysis (Patient: John Doe)")
    df = st.session_state.patient_db
    
    # Automated NLG (Natural Language Generation) Summary
    last_weight_change = df['Weight'].iloc[-1] - df['Weight'].iloc[-2]
    last_spo2 = df['SpO2'].iloc[-1]
    
    if last_weight_change > 1.5:
        st.warning(f"📊 **Anomaly Detected:** Rapid weight gain of {last_weight_change}kg in 24h. Possible Edema/Heart Failure exacerbation.")
    
    if last_spo2 < 95:
        st.error(f"🫁 **Correlation Alert:** SpO2 has dropped to {last_spo2}%. Cross-referencing with weight gain suggests fluid overload.")

    

    # Visualizing Correlations
    st.subheader("📈 Multi-Parametric Correlation")
    chart_choice = st.multiselect("Select Parameters to Overlay", ["Weight", "Systolic", "SpO2", "BIA_Muscle"], default=["Weight", "Systolic"])
    st.line_chart(df.set_index('Date')[chart_choice])

    if st.button("📝 Generate Automated Summary Report"):
        st.code(f"""
        FINAL CLINICAL SUMMARY:
        - Blood Pressure: Trending Upwards (Current: {df['Systolic'].iloc[-1]} mmHg)
        - SpO2: Critical Decline detected in last 48 hours.
        - Muscle Mass: Stable (BIA: {df['BIA_Muscle'].iloc[-1]}kg), confirming weight gain is likely fluid.
        - RECOMMENDATION: Adjust Diuretic Dosage / Immediate Clinical Visit.
        """)


