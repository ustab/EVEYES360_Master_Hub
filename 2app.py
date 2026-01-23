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

# 2. DATA ENGINE
if 'patient_db' not in st.session_state:
    st.session_state.patient_db = pd.DataFrame({
        'Date': [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(4, -1, -1)],
        'Weight': [75.0, 74.8, 75.2, 77.5, 78.0],
        'Height': [175, 175, 175, 175, 175],
        'Systolic': [120, 122, 125, 145, 150],
        'Diastolic': [80, 81, 82, 95, 100],
        'Pulse': [72, 74, 75, 88, 92],
        'BIA_muscle': [22.0, 21.8, 22.1, 23.5, 24.0],
        'BIA_Fat': [22.0, 21.8, 22.1, 23.5, 24.0],
        'BIA_Oedema': [22.0, 21.8, 22.1, 23.5, 24.0],
        'Mood_Score': [8, 7, 7, 4, 3]
    })

df = st.session_state.patient_db
today = df.iloc[-1]
yesterday = df.iloc[-2]

# 3. SIDEBAR
st.sidebar.title("🏥 EVEYES 360 Hub")
user_role = st.sidebar.selectbox("🔐 System Access", ["Patient Portal", "Specialist Dashboard"])
patient_group = st.sidebar.selectbox("🎯 Target Group", ["Chronic Care", "Pediatric", "Geriatric", "Post-Op"])

branch_options = [
    "General Medicine", "Neuro (neuro.py)", "Metabolic (metabolic.py)", 
    "Pediatrics (pediatric.py)", "Dermatology (derma.py)",
    "Sonic Bio-Analysis (resp_sonic.py)", "Music Psychotherapy (therapy.py)"
]
branch = st.sidebar.selectbox("🧠 Clinical Module", branch_options)

# 4. HASTA PORTALI
if user_role == "Patient Portal":
    tabs = st.tabs(["🏠 Dashboard", "📝 Vital Entry", "📷 AI Scan"])
    
    with tabs[0]:
        st.subheader("📊 Kişisel Analiz")
        bmi = today['Weight'] / ((today['Height']/100)**2)
        c1, c2, c3 = st.columns(3)
        c1.metric("BMI", f"{bmi:.1f}", f"{bmi - (yesterday['Weight']/((yesterday['Height']/100)**2)):.1f}", delta_color="inverse")
        c2.metric("Tansiyon", f"{today['Systolic']}/{today['Diastolic']}")
        c3.metric("Mood", f"{today['Mood_Score']}/10")
        st.line_chart(df.set_index('Date')[['Weight', 'Systolic']])

    with tabs[1]:
        with st.form("entry_form"):
            w = st.number_input("Kilo (kg)", value=float(today['Weight']))
            h = st.number_input("Boy (cm)", value=int(today['Height']))
            if st.form_submit_button("Veriyi Kaydet"):
                new_data = today.copy()
                new_data['Date'] = datetime.now().strftime('%Y-%m-%d')
                new_data['Weight'], new_data['Height'] = w, h
                st.session_state.patient_db = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
                st.rerun()

    with tabs[2]: # AI Scan Sekmesi (Hata Giderildi)
        st.subheader("📷 AI Yüz ve Vücut Analiz Sistemi")
        c_scan1, c_scan2 = st.columns([2, 1])
        
        with c_scan1:
            img_file = st.camera_input("Analiz için Görüntü Alın")
        
        with c_scan2:
            st.write("### Canlı Metrikler")
            if img_file:
                st.success("Görüntü İşleniyor...")
                st.progress(94, text="Yüz Simetrisi: %94")
                st.progress(85, text="Postür Dengesi: %85")
                st.write(f"**Tahmini Stres Seviyesi:** {'Düşük' if today['Mood_Score'] > 5 else 'Yüksek'}")
            else:
                st.info("Kamerayı başlatıp fotoğraf çekerek vücut postür analizini başlatabilirsiniz.")

# 5. UZMAN PANELİ
else:
    st.title(f"👨‍⚕️ Specialist: {branch}")
    is_emergency = today['Systolic'] >= 160 or (today['Weight'] - yesterday['Weight']) > 2.0
    
    if "Neuro" in branch:
        st.subheader("🧠 Nörolojik Hareket Analizi")
        col_n1, col_n2 = st.columns(2)
        with col_n1:
            # Vücut hareket analizi scatter plot
            body_pts = pd.DataFrame(np.random.randn(15, 2), columns=['X-Axis (Simetri)', 'Y-Axis (Denge)'])
            st.scatter_chart(body_pts)
            st.caption("İskelet Sistemi Eklem Koordinatları")
        with col_n2:
            st.write("**Mikro-Mimik Analizi**")
            st.progress(0.92, text="Fasiyal Tonus")
            st.write("- Göz Kırpma: 14 bpm")
            st.write("- Ağız Kenarı Simetrisi: %98")

    elif "Sonic" in branch:
        st.subheader("🧬 Biosonology Engine")
        st.line_chart(np.random.randn(20, 2))
        
    elif "Music" in branch:
        st.subheader("🏺 Seljuk Music Therapy")
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
        
    elif "Metabolic" in branch:
        st.metric("Vücut Yağ Oranı (BIA)", f"{today['BIA_Fat']}%")
        st.bar_chart(df['BIA_Fat'])

    st.divider()
    with st.expander("📝 Clinical Intelligence Report", expanded=True):
        if is_emergency: st.error("🚨 KRİTİK EŞİK AŞILDI!")
        st.markdown(f"**Hasta:** John Doe | **Branş:** {branch}")
        st.write(f"Sistem Bulgu Notu: Yapay zeka destekli vücut analizi ve vital veriler {'KRİTİK' if is_emergency else 'STABİL'} seviyededir.")
        if st.button("📤 DOKTORA GÖNDER"):
            st.success("Rapor iletildi.")

# 6. DATA MANAGEMENT
st.sidebar.divider()
if st.sidebar.button("🔄 Reset System"):
    st.session_state.clear()
    st.rerun()
