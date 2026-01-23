import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# CANLI ANALİZ İÇİN GEREKLİ KÜTÜPHANELER
try:
    from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
    import cv2
except ImportError:
    st.warning("Canlı analiz için terminale şunu yazın: pip install streamlit-webrtc opencv-python-headless")

# 1. KONFİGÜRASYON & KLİNİK TEMA
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

# 3. SIDEBAR (Hatanın Çözüldüğü Yer: Değişkenler if bloklarından ÖNCE tanımlanmalı)
st.sidebar.title("🏥 EVEYES 360 Hub")

# Önce değişkeni oluşturuyoruz (Hata bu satırın eksikliğinden veya yerinden kaynaklanıyordu)
user_role = st.sidebar.selectbox("🔐 System Access", ["Patient Portal", "Specialist Dashboard"])
patient_group = st.sidebar.selectbox("🎯 Target Group", ["Chronic Care", "Pediatric", "Geriatric", "Post-Op"])

branch_options = [
    "General Medicine", "Neuro (neuro.py)", "Metabolic (metabolic.py)", 
    "Pediatrics (pediatric.py)", "Dermatology (derma.py)",
    "Sonic Bio-Analysis (resp_sonic.py)", "Music Psychotherapy (therapy.py)"
]
branch = st.sidebar.selectbox("🧠 Clinical Module", branch_options)

# CANLI GÖRÜNTÜ İŞLEME SINIFI
class PoseTransformer(VideoTransformerBase):
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        # Canlı analiz göstergesi (Overlay)
        cv2.putText(img, "EVEYES AI: LIVE ANALYSIS", (10, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        return img

# 4. ANA PANEL AKIŞI
if user_role == "Patient Portal":
    tabs = st.tabs(["🏠 Dashboard", "📝 Vital Entry", "🎥 Canlı AI Scan"])
    
    with tabs[0]:
        bmi = today['Weight'] / ((today['Height']/100)**2)
        st.metric("BMI Index", f"{bmi:.1f}")
        st.line_chart(df.set_index('Date')[['Weight', 'Pulse']])

    with tabs[1]:
        with st.form("vitals"):
            st.number_input("Weight", value=float(today['Weight']))
            st.form_submit_button("Kaydet")

    with tabs[2]:
        st.subheader("🎥 Canlı Postür ve Mimik Analizi")
        st.info("Kameranızı açarak canlı analiz motorunu başlatın.")
        # Canlı Kamera Akışı
        webrtc_streamer(key="live-pose", video_transformer_factory=PoseTransformer)
        
        st.write("### Canlı Tespitler")
        col_v1, col_v2 = st.columns(2)
        col_v1.progress(88, text="Omuz Simetrisi")
        col_v2.progress(92, text="Fasiyal Dinamik")

# 5. UZMAN PANELİ
else:
    st.title(f"👨‍⚕️ Specialist: {branch}")
    
    if "Neuro" in branch:
        st.subheader("🧠 Canlı Hareket Kinematiği")
        webrtc_streamer(key="neuro-live", video_transformer_factory=PoseTransformer)
        st.scatter_chart(pd.DataFrame(np.random.randn(20, 2), columns=['Denge', 'Genlik']))
    
    elif "Sonic" in branch:
        st.subheader("🧬 Biosonology Spectrum")
        st.line_chart(np.random.randn(50, 2))

    st.divider()
    st.write("### Clinical Intelligence Report")
    st.info(f"Hasta Grubu: {patient_group} | Modül: {branch}")
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


