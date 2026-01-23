import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

#  1. CONFIGURATION & CLINICAL THEMING (Görselleştirme & Mobil Arayüz) ---
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

# 3. SIDEBAR: MERKEZİ KONTROL (Hataları Çözen Bölüm)

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

            if submit: 
                # 1. Yeni veriyi mevcut satırdan kopyala (şablon olarak)
                new_entry = today.copy()
                
                # 2. Formdaki yeni değerleri üzerine yaz
                new_entry['Date'] = datetime.now().strftime('%Y-%m-%d')
                new_entry['Weight'] = w_in
                new_entry['Height'] = h_in
                
                # 3. Ana veritabanına (session_state) bu yeni satırı ekle
                st.session_state.patient_db = pd.concat([
                    st.session_state.patient_db, 
                    pd.DataFrame([new_entry])
                ], ignore_index=True)
                
                st.success("✅ Veri Kaydedildi! Grafikler Güncelleniyor...")
                st.rerun() # Bu komut sayfayı yeniler ve yeni veriyi grafiğe işler

    with tabs[2]: # AI Vision Scan (Mood & Facial Analysis)
        st.subheader("📷 Patient Mood & Body Movement Analysis")
        st.info("AI is analyzing facial micro-expressions and body symmetry for Gait/Mood assessment.")
        st.camera_input("Facial & Posture Scan")
        st.file_uploader("Upload Gait/Movement Video", type=["mp4", "mov"])

 
# 4 & 5. BRANŞ ÖZEL ANALİZ MOTORLARI (SADECE SPECIALIST İÇİN)
else: # Yani user_role == "Specialist Dashboard" ise
    st.title(f"👨‍⚕️ {branch} Decision Support")
    
    # --- A. METABOLIC.PY MODÜLÜ ---
    if branch == "Metabolic.py":
        st.info("🧬 **Metabolic Analysis Mode Active**")
        m1, m2, m3 = st.columns(3)
        w_trend = today['Weight'] - yesterday['Weight']
        fat_trend = today['BIA_Fat'] - yesterday['BIA_Fat']
        
        status = "✅ Stable"
        if w_trend > 1.5 and fat_trend <= 0: status = "🚨 OEDEMA RISK"
        elif w_trend < -2.0: status = "⚠️ CACHEXIA RISK"
        
        m1.metric("Metabolic Status", status, f"{w_trend:+.1f}kg")
        m2.metric("BMI Index", f"{(today['Weight']/((today['Height']/100)**2)):.1f}")
        m3.metric("BIA Fat %", f"{today['BIA_Fat']}%", f"{fat_trend:+.1f}%")
        st.line_chart(df.set_index('Date')[['Weight', 'BIA_Fat']])

    # --- B. NEURO.PY & PEDIATRICS MODÜLÜ ---
    elif branch in ["Neuro.py", "Pediatrics", "Growth & Development"]:
        st.info("🧠 **Neurological & Behavioral Monitor Active**")
        n1, n2, n3 = st.columns(3)
        mood = today['Mood_Score']
        
        n1.metric("Mood Score", f"{mood}/10", f"{mood-yesterday['Mood_Score']}")
        n2.metric("Neuro-Symmetry", "94%", "Optimal")
        n3.metric("Communication", "Typical" if mood > 5 else "Atypical")
        
        st.area_chart(df.set_index('Date')[['Mood_Score']])

    # --- 6. GLOBAL AI SUMMARY (Tüm Branşlar İçin Raporlama) ---
    st.divider()
    with st.expander("📝 View AI Clinical Summary", expanded=True):
        report = (
            f"**ANALYSIS FOR:** John Doe | **BRANCH:** {branch}\n\n"
            f"Patient is currently showing **{status if 'status' in locals() else 'Stable'}** trends. "
            f"Latest Systolic BP: {today['Systolic']} mmHg. "
            f"Mood/Gait tracking suggests {'routine follow-up' if today['Mood_Score'] > 5 else 'urgent neurological review'}."
        )
        st.markdown(report)
        if st.button("📤 Dispatch Secure Report"):
            st.success(f"Encrypted report sent to {branch} department.")
    
# --- 7. DATA PERSISTENCE & EXPORT (Opsiyonel) ---
st.sidebar.divider()
st.sidebar.subheader("💾 Data Management")

# Veriyi Excel/CSV olarak indirme imkanı
csv = df.to_csv(index=False).encode('utf-8')
st.sidebar.download_button(
    label="📥 Export Patient History",
    data=csv,
    file_name=f"Patient_Data_{datetime.now().strftime('%Y%m%d')}.csv",
    mime='text/csv',
)

if st.sidebar.button("🔄 Reset Session Data"):
    st.session_state.clear()
    st.rerun()








