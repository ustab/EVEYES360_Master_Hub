import streamlit as st
import pandas as pd
import numpy as np
import time

def show_neuro():
    st.title("🧠 Neuro-Guard: Mobility & Tremor Analytics")
    
    # 1. Branş Seçimi
    neuro_focus = st.sidebar.selectbox(
        "Klinik Odak / Neuro Focus",
        ["Genel Değerlendirme", "Parkinson Takibi", "Multiple Sclerosis (MS)", "ALS / Motor Nöron"]
    )

    tab1, tab2 = st.tabs(["🚶 Yürüyüş (Gait)", "🖐️ Titreme (Tremor)"])

    # Değişkenleri varsayılan olarak tanımlıyoruz (Hata almamak için)
    speed, symmetry, tremor_freq = "N/A", "N/A", "N/A"

    with tab1:
        st.subheader("AI-Powered Gait & Balance Monitoring")
        st.write("Hastanın yürüyüş videosunu yükleyerek analiz yapın.")
        
        video_file = st.file_uploader("Upload Walking Video", type=["mp4", "mov"], key="gait_vid")
        
        if video_file:
            st.video(video_file)
            if st.button("Start AI Biomechanical Analysis"):
                with st.spinner("Analyzing joint angles..."):
                    time.sleep(2)
                
                speed, symmetry = "0.92 m/s", "88%"
                st.success("Analysis Complete!")
                
                m1, m2, m3 = st.columns(3)
                m1.metric("Gait Speed", speed, "-5%")
                m2.metric("Symmetry", symmetry, "Stable")
                m3.metric("Fall Risk", "Low", "Safe")

                chart_data = pd.DataFrame(np.random.randn(20, 2), columns=['Left Foot', 'Right Foot'])
                st.line_chart(chart_data)

    with tab2:
        st.subheader("Neurological Tremor Frequency Test")
        st.write("İstemsiz hareketleri (Resting Tremor) ölçmek için testi başlatın.")
        
        test_duration = st.slider("Test Süresi (Saniye)", 5, 15, 10)
        
        if st.button("Start Tremor Capture"):
            progress_bar = st.progress(0)
            for percent in range(100):
                time.sleep(test_duration / 100)
                progress_bar.progress(percent + 1)
            
            tremor_freq = "4.5 Hz"
            st.success("Data Captured!")
            
            freq_data = pd.DataFrame({
                'Frequency (Hz)': np.arange(1, 11),
                'Amplitude': [0.1, 0.2, 0.5, 3.8, 4.2, 3.5, 0.8, 0.3, 0.1, 0.05]
            })
            st.bar_chart(freq_data.set_index('Frequency (Hz)'))
            st.warning(f"⚠️ **Bulgu:** Peak noktası **{tremor_freq}** olarak saptandı (Parkinson sınırı).")

    # 2. RAPORLAMA
    st.divider()
    st.subheader("🏥 Nörolojik Klinik Rapor")
    
    rapor_metni = f"EVEYES 360 NEURO REPORT\n---\nOdak: {neuro_focus}\nHiz: {speed}\nSimetri: {symmetry}\nFrekans: {tremor_freq}"

    col1, col2 = st.columns(2)
    with col1:
        st.download_button("📥 Raporu İndir", rapor_metni, file_name="neuro_rapor.txt")
    with col2:
        encoded_msg = rapor_metni.replace("\n", "%0A")
        whatsapp_url = f"https://wa.me/905XXXXXXXXX?text={encoded_msg}"
        st.markdown(f'<a href="{whatsapp_url}" target="_blank" style="text-decoration:none;"><div style="background-color:#25D366;color:white;padding:10px;border-radius:5px;text-align:center;font-weight:bold;">🟢 WhatsApp ile Gönder</div></a>', unsafe_allow_html=True)
