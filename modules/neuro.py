import streamlit as st
import pandas as pd
import numpy as np
import time

def show_neuro():
    st.title("🧠 Neuro-Guard: Mobility & Tremor Analytics")
    st.markdown("""
    This module focuses on **Neuro-Degenerative diseases** (Parkinson's, MS, ALS). 
    It tracks patient motor skills using video gait analysis and tremor frequency detection.
    """)

    tab1, tab2 = st.tabs(["🚶 Gait Analysis (Yürüyüş)", "🖐️ Tremor Test (Titreme)"])

import streamlit as st
import pandas as pd
import time
from PIL import Image
import numpy as np

def show_derma():
    st.title("🤳 Derma-Scan: Vision-Based Wound & Mole Tracker")
    st.markdown("""
    This module uses **Computer Vision** to monitor skin health. 
    It tracks wound healing progress and analyzes suspicious moles using the **ABCDE** clinical criteria.
    """)

    tab1, tab2 = st.tabs(["🩹 Wound Tracking (Diabetic Foot)", "🔍 Mole Analysis (Skin Cancer)"])

    with tab1:
        st.subheader("Diabetic Wound Progression")
        st.write("Upload a photo of the wound to analyze healing rate and infection signs.")
        
        img_file = st.file_uploader("Upload Wound Photo", type=["jpg", "png", "jpeg"], key="wound_up")
        
        if img_file:
            st.image(img_file, caption="Current Wound State", use_container_width=True)
            if st.button("Analyze Wound Healing"):
                with st.spinner("Calculating tissue area and vascularization..."):
                    time.sleep(2)
                
                # İyileşme Verileri
                st.success("Analysis Complete!")
                c1, c2 = st.columns(2)
                c1.metric("Wound Area", "4.2 cm²", "-0.5 cm² (Improving)")
                c2.metric("Infection Risk", "Low", "Normal Temp")
                
                # İyileşme Grafiği
                st.write("**Healing Progress Over 4 Weeks**")
                healing_data = pd.DataFrame({
                    'Week': [1, 2, 3, 4],
                    'Area (cm²)': [5.8, 5.2, 4.7, 4.2]
                })
                st.line_chart(healing_data.set_index('Week'))
                st.info("💡 **Clinical Note:** Granulation tissue is healthy. Keep current dressing protocol.")

    with tab2:
        st.subheader("ABCDE Mole Assessment")
        st.write("Upload a photo of a mole to check for clinical warning signs of Melanoma.")
        
        mole_file = st.file_uploader("Upload Mole Photo", type=["jpg", "png", "jpeg"], key="mole_up")
        
        if mole_file:
            st.image(mole_file, caption="Analyzing Surface Patterns...", use_container_width=True)
            
            st.write("### AI Risk Scoring")
            # Simüle edilmiş ABCDE Analizi
            st.table(pd.DataFrame({
                'Criterion': ['Asymmetry', 'Border', 'Color', 'Diameter', 'Evolution'],
                'Result': ['Regular', 'Sharp', 'Uniform', '4mm', 'Stable'],
                'Risk': ['Low', 'Low', 'Low', 'Low', 'Low']
            }))
            
            st.success("✅ Overall Assessment: Low Risk. Suggest annual check-up.")
import streamlit as st
import pandas as pd
import time

def show_neuro():
    st.title("🧠 Neuro-Guard: Mobility & Tremor Analytics")
    
    # 1. Branş Seçimi
    neuro_focus = st.selectbox(
        "Klinik Odak / Neuro Focus",
        ["Genel Değerlendirme", "Parkinson Takibi", "Multiple Sclerosis (MS)", "ALS / Motor Nöron"]
    )

    tab1, tab2 = st.tabs(["🚶 Yürüyüş (Gait)", "🖐️ Titreme (Tremor)"])

    with tab1:
        st.subheader("AI-Powered Gait & Balance Monitoring")
        st.write("Upload a video of the patient walking to measure symmetry, step length, and fall risk.")
        
        video_file = st.file_uploader("Upload Walking Video", type=["mp4", "mov"])
        
        if video_file:
            st.video(video_file)
            if st.button("Start AI Biomechanical Analysis"):
                with st.spinner("Analyzing joint angles and step patterns..."):
                    time.sleep(3) # Analiz simülasyonu
                    
                st.success("Analysis Complete!")
                
                # Klinik Metrikler
                m1, m2, m3 = st.columns(3)
                m1.metric("Gait Speed", "0.92 m/s", "-5%")
                m2.metric("Symmetry", "88%", "Stable")
                m3.metric("Fall Risk", "Low", "Safe")

                # Yürüyüş Grafiği
                st.write("**Step Pressure & Timing Distribution**")
                chart_data = pd.DataFrame(
                    np.random.randn(20, 2),
                    columns=['Left Foot', 'Right Foot']
                )
                st.line_chart(chart_data)
                st.info("💡 **Clinical Insight:** Minor hesitation detected in left-side swing phase. Recommend physical therapy for balance.")

    with tab2:
        st.subheader("Neurological Tremor Frequency Test")
        st.write("This test measures involuntary movements (Resting Tremor).")
        
        test_duration = st.slider("Test Duration (Seconds)", 5, 15, 10)
        
        if st.button("Start Tremor Capture"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for percent in range(100):
                time.sleep(test_duration / 100)
                progress_bar.progress(percent + 1)
                status_text.text(f"Capturing micro-vibrations... {percent+1}%")
            
            st.success("Data Captured!")
            
            # Titreme Frekansı Grafiği (Parkinson aralığı 4-6 Hz)
            st.write("**Frequency Spectrum Analysis (Hz)**")
            freq_data = pd.DataFrame({
                'Frequency (Hz)': np.arange(1, 11),
                'Amplitude': [0.1, 0.2, 0.5, 3.8, 4.2, 3.5, 0.8, 0.3, 0.1, 0.05]
            })
            st.bar_chart(freq_data.set_index('Frequency (Hz)'))
            
            st.warning("⚠️ **Alert:** Peak detected at **4.5 Hz**. This is consistent with Parkinsonian resting tremor. Data sent to consultant.")
    

    # 2. RAPORLAMA STANDARTI (Metabolic modülü ile aynı yapıda)
    st.divider()
    st.subheader("🏥 Nörolojik Klinik Rapor")
    
    rapor_metni = f"""
    EVEYES 360 NEURO REPORT
    -----------------------
    Odak: {neuro_focus}
    Adım Hızı: {speed} m/s
    Simetri: %{symmetry}
    Titreme: {tremor_freq} Hz ({tremor_amp})
    """

    col1, col2 = st.columns(2)
    with col1:
        st.download_button("📥 Raporu TXT Olarak İndir", rapor_metni, file_name="neuro_rapor.txt")

    with col2:
        encoded_msg = rapor_metni.replace("\n", "%0A")
        whatsapp_url = f"https://wa.me/905XXXXXXXXX?text={encoded_msg}"
        st.markdown(f"""
            <a href="{whatsapp_url}" target="_blank" style="text-decoration: none;">
                <div style="width: 100%; background-color: #25D366; color: white; padding: 10px; border-radius: 5px; text-align: center; font-weight: bold;">
                    🟢 WhatsApp ile Nöroloğa Gönder
                </div>
            </a>""", unsafe_allow_html=True)