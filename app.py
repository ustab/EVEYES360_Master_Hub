import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 1. KONFİGÜRASYON & KLİNİK TEMA
st.set_page_config(page_title="EVEYES 360 Platinum", layout="wide", page_icon="🏥")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    [data-testid="stSidebar"] { background-color: #1a2a3a; }
    [data-testid="stSidebar"] .stSelectbox label, [data-testid="stSidebar"] p { color: white !important; font-weight: bold; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. VERİ MOTORU
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
        'Mood_Score': [8, 7, 7, 4, 3]
    })

df = st.session_state.patient_db
today = df.iloc[-1]
yesterday = df.iloc[-2]

# 3. SIDEBAR: MERKEZİ KONTROL
st.sidebar.title("🏥 EVEYES 360 Hub")

patient_group = st.sidebar.selectbox(
    "🎯 Target Group", 
    ["Chronic Care", "Pediatric", "Geriatric", "Pregnancy", "Post-Op"],
    key="fixed_tg"
)

user_role = st.sidebar.selectbox(
    "🔐 System Access", 
    ["Patient Portal", "Specialist Dashboard"],
    key="fixed_role"
)

branch = "General Medicine" # Varsayılan branş
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

# --- ANA PANEL ---
if user_role == "Patient Portal":
    tabs = st.tabs(["🏠 Clinical Dashboard", "📝 Vital Entry", "📷 AI Vision Scan"])

    with tabs[0]:
        st.subheader("📊 Comparative Analytics")
        bmi = today['Weight'] / ((today['Height']/100)**2)
        prev_bmi = yesterday['Weight'] / ((yesterday['Height']/100)**2)
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("BMI Index", f"{bmi:.1f}", f"{bmi - prev_bmi:.1f}", delta_color="inverse")
        c2.metric("BP (Sys/Dia)", f"{today['Systolic']}/{today['Diastolic']}", f"{today['Systolic']-yesterday['Systolic']}/ {today['Diastolic']-yesterday['Diastolic']}", delta_color="inverse")
        c3.metric("Pulse (BPM)", f"{today['Pulse']}", f"{today['Pulse']-yesterday['Pulse']}", delta_color="inverse")
        c4.metric("Mood/Gait Score", f"{today['Mood_Score']}/10", f"{today['Mood_Score']-yesterday['Mood_Score']}", delta_color="normal")

        st.subheader("📈 Physiological Trends")
        st.line_chart(df.set_index('Date')[['Weight', 'Systolic', 'Pulse']])

    with tabs[1]:
        st.subheader("📝 Advanced Data Entry")
        with st.form("advanced_vitals"):
            col1, col2 = st.columns(2)
            w_input = col1.number_input("Weight (kg)", 30.0, 250.0, float(today['Weight']))
            h_input = col2.number_input("Height (cm)", 50, 250, int(today['Height']))
            
            pain_type = st.select_slider("Pain Intensity", options=["😊 0", "😐 2", "😟 4", "😫 6", "😭 8", "😱 10"])
            
            st.write("---")
            st.subheader("Genetic & Neuro Screening")
            q1 = st.checkbox("History of Genetic Disorders in Family?")
            q2 = st.checkbox("Neurological Symptoms?")
            autism_check = st.radio("Social/Communication Interaction Status:", ["Typical", "Atypical Observations"])
            
            submit = st.form_submit_button("💾 Process & Validate")

            if submit: 
                new_entry = today.copy()
                new_entry['Date'] = datetime.now().strftime('%Y-%m-%d')
                new_entry['Weight'] = w_input
                new_entry['Height'] = h_input
                
                st.session_state.patient_db = pd.concat([st.session_state.patient_db, pd.DataFrame([new_entry])], ignore_index=True)
                st.success("✅ Veri Kaydedildi!")
                st.rerun()

    with tabs[2]:
        st.subheader("📷 Patient Mood & Body Movement Analysis")
        st.camera_input("Facial & Posture Scan")
        st.file_uploader("Upload Gait/Movement Video", type=["mp4", "mov"])

else: # Specialist Dashboard
    st.title(f"👨‍⚕️ {branch} Decision Support")
    
    if branch == "Metabolic.py":
        st.info("🧬 **Metabolic Analysis Mode Active**")
        m1, m2, m3 = st.columns(3)
        w_trend = today['Weight'] - yesterday['Weight']
        fat_trend = today['BIA_Fat'] - yesterday['BIA_Fat']
        
        status = "✅ Stable"
        if w_trend > 1.5: status = "🚨 OEDEMA RISK"
        elif w_trend < -2.0: status = "⚠️ CACHEXIA RISK"
        
        m1.metric("Metabolic Status", status, f"{w_trend:+.1f}kg")
        m2.metric("BMI Index", f"{(today['Weight']/((today['Height']/100)**2)):.1f}")
        m3.metric("BIA Fat %", f"{today['BIA_Fat']}%", f"{fat_trend:+.1f}%")
        st.line_chart(df.set_index('Date')[['Weight', 'BIA_Fat']])

    elif branch in ["Neuro.py", "Pediatrics", "Growth & Development"]:
        st.info("🧠 **Neurological & Behavioral Monitor Active**")
        n1, n2, n3 = st.columns(3)
        mood = today['Mood_Score']
        n1.metric("Mood Score", f"{mood}/10", f"{mood-yesterday['Mood_Score']}")
        n2.metric("Neuro-Symmetry", "94%", "Optimal")
        n3.metric("Communication", "Typical" if mood > 5 else "Atypical")
        st.area_chart(df.set_index('Date')[['Mood_Score']])

    # AKILLI RAPOR & ALARM SİSTEMİ (Uzman Paneli İçinde)
    st.divider()
    st.subheader("📝 Clinical Intelligence Report")
    
    weight_delta = float(today['Weight'] - yesterday['Weight'])
    is_emergency = False
    emergency_msg = ""

    if today['Systolic'] >= 160:
        is_emergency = True
        emergency_msg = "🚨 KRİTİK TANSİYON YÜKSEKLİĞİ!"
    elif weight_delta > 2.0:
        is_emergency = True
        emergency_msg = "🚨 ANİ KİLO ARTIŞI (ÖDEM RİSKİ)!"
    elif today['Mood_Score'] <= 3:
        is_emergency = True
        emergency_msg = "🚨 NÖROLOJİK / MOOD KRİZİ!"

    with st.expander("📄 Rapor Detayını Görüntüle", expanded=True):
        if is_emergency:
            st.error(f"**ACİL DURUM UYARISI:** {emergency_msg}")
        st.markdown(f"**HASTA:** John Doe | **TARİH:** {today['Date']} | **BRANŞ:** {branch}")
        st.write(f"- Kilo Değişimi: {weight_delta:+.1f} kg")
        st.write(f"- Tansiyon: {today['Systolic']}/{today['Diastolic']} mmHg")
        st.write(f"- Durum: {'🔴 KRİTİK' if is_emergency else '🟢 STABİL'}")

    c_send, c_status = st.columns([1, 2])
    if c_send.button("📤 DOKTORUMA GÖNDER"):
        st.success("✅ Rapor iletildi.")
    if is_emergency:
        c_status.warning("⚠️ Sistem otomatik kritik bildirim oluşturdu.")

# 7. DATA MANAGEMENT
st.sidebar.divider()
csv = df.to_csv(index=False).encode('utf-8')
st.sidebar.download_button("📥 Export Patient History", data=csv, file_name="Patient_Data.csv", mime='text/csv')
if st.sidebar.button("🔄 Reset Session Data"):
    st.session_state.clear()
    st.rerun()
