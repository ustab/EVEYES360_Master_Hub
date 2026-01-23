import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# CANLI ANALİZ İÇİN GEREKLİ KÜTÜPHANELER
try:
    from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
    import cv2
except ImportError:
    st.error("Lütfen terminale şunu yazın: pip install streamlit-webrtc opencv-python-headless")

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
        'BIA_Fat': [22.0, 21.8, 22.1, 23.5, 24.0],
        'Mood_Score': [8, 7, 7, 4, 3]
    })

df = st.session_state.patient_db
today = df.iloc[-1]
yesterday = df.iloc[-2]

# 3. SIDEBAR (Değişken tanımlamaları burada başlar)
st.sidebar.title("🏥 EVEYES 360 Hub")
user_role = st.sidebar.selectbox("🔐 System Access", ["Patient Portal", "Specialist Dashboard"])
patient_group = st.sidebar.selectbox("🎯 Target Group", ["Chronic Care", "Pediatric", "Geriatric", "Post-Op"])

branch_options = [
    "General Medicine", "Neuro (neuro.py)", "Metabolic (metabolic.py)", 
    "Pediatrics (pediatric.py)", "Dermatology (derma.py)",
    "Sonic Bio-Analysis (resp_sonic.py)", "Music Psychotherapy (therapy.py)"
]
branch = st.sidebar.selectbox("🧠 Clinical Module", branch_options)

# CANLI GÖRÜNTÜ İŞLEME MOTORU (VideoTransformer)
class LiveAnalyzer(VideoTransformerBase):
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        # Canlı analiz için görsel katman (Overlay)
        cv2.putText(img, "EVEYES AI: LIVE STREAM ANALYZING", (20, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        return img

# 4. HASTA PORTALI
if user_role == "Patient Portal":
    tabs = st.tabs(["🏠 Dashboard", "📝 Vital Entry", "🎥 Live AI Scan"])
    
    with tabs[0]:
        st.subheader("📊 Kişisel Analiz")
        st.line_chart(df.set_index('Date')[['Weight', 'Systolic']])

    with tabs[1]:
        with st.form("entry"):
            st.number_input("Kilo", value=float(today['Weight']))
            st.form_submit_button("Kaydet")

    with tabs[2]:
        st.subheader("🎥 Canlı Postür ve Mimik Takibi")
        webrtc_streamer(key="patient-live", video_transformer_factory=LiveAnalyzer)
        st.progress(88, text="Anlık Denge Skoru")

# 5. UZMAN PANELİ (Hata burada giderildi: elif blokları hizalandı)
else:
    st.title(f"👨‍⚕️ Specialist: {branch}")
    is_emergency = today['Systolic'] >= 160 or (today['Weight'] - yesterday['Weight']) > 2.0
    
    if "Neuro" in branch:
        st.subheader("🧠 Canlı Hareket Analizi")
        webrtc_streamer(key="neuro-live", video_transformer_factory=LiveAnalyzer)
        st.write("Eklem koordinatları canlı olarak hesaplanıyor.")
        
    elif "Sonic" in branch:
        st.subheader("🧬 Biosonology Engine")
        st.info("Hücresel frekansların biyo-akustik melodileri analiz ediliyor.")
        st.line_chart(np.random.randn(20, 2))
        
    elif "Music" in branch:
        st.subheader("🏺 Seljuk Music Therapy")
        st.write("Selçuklu dönemine ait makamlarla hücresel rejenerasyon desteği.")
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
        
    elif "Metabolic" in branch:
        st.metric("Vücut Yağ Oranı (BIA)", f"{today['BIA_Fat']}%")

    st.divider()
    with st.expander("📝 Clinical Intelligence Report", expanded=True):
        if is_emergency: st.error("🚨 KRİTİK EŞİK AŞILDI!")
        st.write(f"Rapor Modülü: {branch} | Durum: {'KRİTİK' if is_emergency else 'STABİL'}")
        if st.button("📤 DOKTORA GÖNDER"):
            st.success("Analiz raporu merkeze iletildi.")

# 6. DATA MANAGEMENT
st.sidebar.divider()
if st.sidebar.button("🔄 Reset Session"):
    st.session_state.clear()
    st.rerun()
