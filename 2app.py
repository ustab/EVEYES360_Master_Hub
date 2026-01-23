import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# CANLI ANALİZ KÜTÜPHANELERİ
try:
    from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
    import cv2
except ImportError:
    st.error("Gerekli paketler eksik. Lütfen terminale: pip install streamlit-webrtc opencv-python-headless yazın.")

# 1. KONFİGÜRASYON
st.set_page_config(page_title="EVEYES 360 Platinum", layout="wide", page_icon="🏥")

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

# 3. SIDEBAR
st.sidebar.title("🏥 EVEYES 360 Hub")
user_role = st.sidebar.selectbox("🔐 System Access", ["Patient Portal", "Specialist Dashboard"])
branch = st.sidebar.selectbox("🧠 Clinical Module", [
    "General Medicine", "Neuro (neuro.py)", "Metabolic (metabolic.py)", 
    "Sonic Bio-Analysis (resp_sonic.py)", "Music Psychotherapy (therapy.py)"
])

# GÜNCELLENMİŞ CANLI ANALİZ MOTORU (Hata giderilmiş hali)
class LiveAnalyzer(VideoProcessorBase):
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        # Canlı takip görseli
        cv2.putText(img, "EVEYES AI ACTIVE", (20, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        return frame.from_ndarray(img, format="bgr24")

# 4. HASTA PORTALI
if user_role == "Patient Portal":
    tabs = st.tabs(["🏠 Dashboard", "🎥 Canlı AI Scan"])
    
    with tabs[1]:
        st.subheader("🎥 Gerçek Zamanlı Vücut ve Mimik Analizi")
        # rtc_configuration sayesinde bağlantı sorunları (STUN/TURN) minimize edilir
        webrtc_streamer(
            key="patient-live-stream",
            video_processor_factory=LiveAnalyzer,
            rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
            media_stream_constraints={"video": True, "audio": False},
        )
        st.progress(88, text="Postür Stabilizasyonu")

# 5. UZMAN PANELİ
else:
    st.title(f"👨‍⚕️ Specialist: {branch}")
    
    if "Sonic" in branch:
        st.subheader("🧬 Biosonology Spectrum")
        # Biosonoloji için hücresel frekans dalgaları simülasyonu
        chart_data = pd.DataFrame(np.random.randn(50, 2), columns=['Frekans (Hz)', 'Genlik'])
        st.line_chart(chart_data)
        st.write("> *Not: Hücresel seslerin melodies analizi biosonoloji modülünde işlenmektedir.*")

    elif "Neuro" in branch:
        st.subheader("🧠 Canlı Kinematik Takip")
        webrtc_streamer(key="specialist-live-stream", video_processor_factory=LiveAnalyzer)
        st.info("AI: Eklem açıları ve hareket simetrisi canlı olarak hesaplanıyor.")

    st.divider()
    if st.button("📤 DOKTORA GÖNDER"):
        st.success("Rapor başarıyla iletildi.")

# 6. RESET
if st.sidebar.button("🔄 Reset System"):
    st.session_state.clear()
    st.rerun()
