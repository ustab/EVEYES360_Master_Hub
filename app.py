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

# ==========================================
# 3. SIDEBAR: MERKEZİ KONTROL (Hataları Çözen Bölüm)
# ==========================================
st.sidebar.title("🏥 EVEYES 360 Hub")

# CSS: Siyah yazıları BEYAZ yapar (image_be5791 hatası çözümü)
st.markdown("""<style>
    [data-testid="stSidebar"] .stSelectbox label { color: white !important; font-weight: bold; }
    [data-testid="stSidebar"] p { color: white !important; }
</style>""", unsafe_allow_html=True)

# Değişkenleri en başta tanımlayarak NameError'ı engelliyoruz
branch = "General Medicine" 

# 1. HEDEF GRUP
patient_group = st.sidebar.selectbox(
    "🎯 Target Group", 
    ["Chronic Care", "Pediatric", "Geriatric", "Pregnancy", "Post-Op"],
    key="fixed_tg"
)

# 2. SİSTEM GİRİŞİ (Satır 41'deki hatayı çözen satır)
user_role = st.sidebar.selectbox(
    "🔐 System Access", 
    ["Patient Portal", "Specialist Dashboard"],
    key="fixed_role"
)

# 3. BRANŞ SEÇİMİ (Satır 111'deki hatayı çözen satır)
if user_role == "Specialist Dashboard":
    if patient_group == "Pediatric":
        options = ["Pediatrics", "Growth & Development", "Genetic Screening"]
    elif patient_group == "Chronic Care":
        options = ["Metabolic.py", "Cardio-Renal", "General Medicine"]
    elif patient_group == "Geriatric":
        options = ["Neuro.py", "Mobility & Gait", "Dementia Care"]
    else:
        options = ["General Medicine", "Custom Module"]
    
    branch = st.sidebar.selectbox("🧠 Clinical Module", options, key="fixed_branch")

st.sidebar.divider()


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
# 6. BRANŞ ÖZEL ANALİZ MOTORLARI
# ==========================================

# --- A. METABOLIC.PY MODÜLÜ (Diyabet & Obezite & Ödem) ---
if branch == "Metabolic.py":
    st.info("🧬 **Metabolic Analysis Mode Active**")
    m1, m2, m3 = st.columns(3)
    
    # Akıllı Parametre: BIA Ödem & Kaşeksi Analizi
    # Taslağındaki 2. Madde: BIA_OEDEMA, BIA_CAHEXIA
    w_trend = today['Weight'] - yesterday['Weight']
    fat_trend = today['BIA_Fat'] - yesterday['BIA_Fat']
    
    if w_trend > 1.5 and fat_trend <= 0:
        status = "🚨 OEDEMA RISK (High Weight / Stable Fat)"
        color = "red"
    elif w_trend < -2.0 and fat_trend < -0.5:
        status = "⚠️ CACHEXIA RISK (Rapid Muscle/Fat Loss)"
        color = "orange"
    else:
        status = "✅ Metabolic Stability"
        color = "green"
    
    m1.metric("Metabolic Status", "Active", status)
    m2.metric("BMI", f"{(today['Weight']/((today['Height']/100)**2)):.1f}")
    m3.metric("Daily Weight Delta", f"{w_trend:+.1f} kg")

    # Boy-Kilo-Yaş İlişkili Büyüme Eğrisi Simülasyonu
    st.subheader("📊 Growth & Metabolic Curve")
    st.line_chart(df.set_index('Date')[['Weight', 'BIA_Fat']])

# --- B. NEURO.PY MODÜLÜ (Nöroloji & Hareket & Otizm) ---
elif branch == "Neuro.py" or branch == "Pediatrics":
    st.info("🧠 **Neurological & Behavioral Monitor Active**")
    n1, n2, n3 = st.columns(3)
    
    # Mood & Facial Analysis (Taslağındaki Mood/Facial/Body Movement)
    mood = today['Mood_Score']
    if mood <= 4:
        neuro_note = "🚨 Clinical Depression / Neuro-Fatigue"
    elif mood >= 8:
        neuro_note = "✅ Stable Cognitive Function"
    else:
        neuro_note = "🟡 Moderate Engagement"

    n1.metric("Mood/Gait Score", f"{mood}/10", f"{mood-yesterday['Mood_Score']}")
    n2.metric("Neuro-Symmetry", "92%", "Stable")
    n3.metric("Pain Scale (VAS)", f"{today['Mood_Score']}") # Pain proxy

    # Otizm & Genetik Sorgu Analizi
    st.warning(f"📝 **Clinical Observation:** {neuro_note}")
    st.write("---")
    st.subheader("🤖 AI Motion & Gait Analysis")
    st.caption("Analyzing body movement symmetry and facial micro-expressions...")
    # Görselleştirme (Taslağındaki 5. Madde: Grafik tarzı)
    st.area_chart(df.set_index('Date')[['Mood_Score']])

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








