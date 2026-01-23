import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# --- 1. CONFIGURATION & CLINICAL THEMING (Görselleştirme & Mobil Arayüz) ---
st.set_page_config(page_title="EVEYES 360 Platinum", layout="wide", page_icon="🏥")

# Mobil Optimizasyon ve Klinik Tema için CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    [data-testid="stSidebar"] { background-color: #1a2a3a; color: white; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
    @media (max-width: 640px) { .main { padding: 10px; } }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA ENGINE & ENHANCED PARAMETERS (Boy, BMI, BIA Analizi) ---
if 'patient_db' not in st.session_state:
    st.session_state.patient_db = pd.DataFrame({
        'Date': [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(4, -1, -1)],
        'Weight': [75.0, 74.8, 75.2, 77.5, 78.0],
        'Height': [175, 175, 175, 175, 175],
        'Systolic': [120, 122, 125, 145, 150],
        'Diastolic': [80, 81, 82, 95, 100],
        'Pulse': [72, 74, 75, 88, 92],
        'SpO2': [98, 97, 98, 96, 94],
        'BIA_Fat': [22.0, 21.8, 22.1, 23.5, 24.0],
        'Mood_Score': [8, 7, 7, 4, 3] # Facial/Body Movement Analysis Proxy
    })

df = st.session_state.patient_db
today = df.iloc[-1]
yesterday = df.iloc[-2]




if user_role == "Patient Portal":
    tabs = st.tabs(["🏠 Clinical Dashboard", "📝 Vital Entry", "📷 AI Vision Scan"])

    with tabs[0]: # Görselleştirme & Parametreler
        st.subheader("📊 Comparative Analytics")
        # BMI Calculation
        bmi = today['Weight'] / ((today['Height']/100)**2)
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("BMI Index", f"{bmi:.1f}", f"{bmi - (yesterday['Weight'] / ((yesterday['Height']/100)**2)):.1f}", delta_color="inverse")
        c2.metric("BP (Sys/Dia)", f"{today['Systolic']}/{today['Diastolic']}", f"{today['Systolic']-yesterday['Systolic']}/ {today['Diastolic']-yesterday['Diastolic']}", delta_color="inverse")
        c3.metric("Pulse (BPM)", f"{today['Pulse']}", f"{today['Pulse']-yesterday['Pulse']}", delta_color="inverse")
        c4.metric("Mood/Gait Score", f"{today['Mood_Score']}/10", f"{today['Mood_Score']-yesterday['Mood_Score']}", delta_color="normal")

        # Growth Curve / Trend
        st.subheader("📈 Physiological Trends")
        st.line_chart(df.set_index('Date')[['Weight', 'Systolic', 'Pulse']])

    with tabs[1]: # Akıllı İşleme & Sorgu
        st.subheader("📝 Advanced Data Entry")
        with st.form("advanced_vitals"):
            col1, col2 = st.columns(2)
            w = col1.number_input("Weight (kg)", 30.0, 250.0, 75.0)
            h = col2.number_input("Height (cm)", 50, 250, 175)
            
            # Pain Scale (Visual Analog Scale representation)
            pain_type = st.select_slider("Pain Intensity (Visual/Numeric Scale)", 
                                       options=["😊 0", "😐 2", "😟 4", "😫 6", "😭 8", "😱 10"])
            
            # Genetic/Neuro Screening
            st.write("---")
            st.subheader("Genetic & Neuro Screening")
            q1 = st.checkbox("History of Genetic Disorders in Family?")
            q2 = st.checkbox("Neurological Symptoms (Tremor/Asymmetry)?")
            autism_check = st.radio("Social/Communication Interaction Status (Autism Screening):", ["Typical", "Atypical Observations"])
            
            submit = st.form_submit_button("💾 Process & Validate")
            
            if submit: # Akıllı İşleme: Hard Limits
                if w > 200 or h < 50: st.warning("⚠️ High Deviation in measurements. Please re-verify.")
                else: st.success("Data synced with clinical hub.")

    with tabs[2]: # AI Vision Scan (Mood & Facial Analysis)
        st.subheader("📷 Patient Mood & Body Movement Analysis")
        st.info("AI is analyzing facial micro-expressions and body symmetry for Gait/Mood assessment.")
        st.camera_input("Facial & Posture Scan")
        st.file_uploader("Upload Gait/Movement Video", type=["mp4", "mov"])

# ==========================================
# 5. SPECIALIST DASHBOARD (Triyaj & NLG)
# ==========================================
else:
    st.title(f"👨‍⚕️ {branch} Decision Support")
    
    # Triyaj Paneli
    c1, c2, c3 = st.columns(3)
    c1.error("🔴 CRITICAL: John Doe (Hypertension Spike)")
    c2.warning("🟡 FOLLOW-UP: Jane Smith (BIA Oedema Risk)")
    c3.success("🟢 STABLE: 15 Patients")

    # NLG Özeti (Smart Processing)
    st.divider()
    st.subheader("🧠 AI Clinical Summary (NLG)")
    
    # BIA Oedema/Cachexia Logic
    weight_delta = today['Weight'] - yesterday['Weight']
    # Simulated Logic
    bia_oedema = True if weight_delta > 1.5 else False
    bia_cachexia = True if weight_delta < -2.0 else False

    report = (
        f"PATIENT REPORT: John Doe\n"
        f"STATUS: {'ALERT - OEDEMA RISK' if bia_oedema else 'STABLE'}\n"
        f"OBSERVATION: Systolic pressure trending at {today['Systolic']} mmHg. "
        f"Mood score has declined to {today['Mood_Score']}/10, suggesting potential distress or neurological fatigue."
    )
    st.info(report)
    
    if st.button("📤 Dispatch Report to Doctor"):
        st.success("Report transmitted via secure clinical channel.")






