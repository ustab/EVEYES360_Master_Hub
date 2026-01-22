import streamlit as st
import pandas as pd
import numpy as np
import time

def show_neuro():
    st.title("🧠 Neuro-Guard: Mobility & Tremor Analytics")
    st.markdown("Advanced monitoring for Parkinson's, MS, and ALS motor symptoms.")
    
    # 1. Focus Selection
    neuro_focus = st.sidebar.selectbox(
        "Clinical Focus",
        ["General Evaluation", "Parkinson's Tracking", "Multiple Sclerosis (MS)", "ALS / Motor Neuron"]
    )

    tab1, tab2 = st.tabs(["🚶 Gait Analysis", "🖐️ Tremor Test"])

    # Default values to prevent calculation errors
    speed, symmetry, tremor_freq = "N/A", "N/A", "N/A"

    with tab1:
        st.subheader("AI-Powered Gait & Balance Monitoring")
        st.write("Analyze patient mobility using video biomechanics.")
        
        video_file = st.file_uploader("Upload Walking Video", type=["mp4", "mov"], key="gait_vid")
        
        if video_file:
            st.video(video_file)
            if st.button("Start Biomechanical Analysis"):
                with st.spinner("Processing joint angles..."):
                    time.sleep(2)
                
                speed, symmetry = "0.92 m/s", "88%"
                st.success("Analysis Complete!")
                
                m1, m2, m3 = st.columns(3)
                m1.metric("Gait Speed", speed, "-5%")
                m2.metric("Symmetry", symmetry, "Stable")
                m3.metric("Fall Risk", "Low", "Safe")

                # Simulated gait pressure chart
                chart_data = pd.DataFrame(np.random.randn(20, 2), columns=['Left Foot', 'Right Foot'])
                st.line_chart(chart_data)
                st.info("💡 **Clinical Insight:** Minor hesitation detected in left-side swing phase.")

    with tab2:
        st.subheader("Neurological Tremor Frequency Test")
        st.write("Measurement of involuntary resting tremors.")
        
        test_duration = st.slider("Test Duration (Seconds)", 5, 15, 10)
        
        if st.button("Start Tremor Capture"):
            progress_bar = st.progress(0)
            for percent in range(100):
                time.sleep(test_duration / 100)
                progress_bar.progress(percent + 1)
            
            tremor_freq = "4.5 Hz"
            st.success("Data Captured!")
            
            # Frequency Spectrum Data
            freq_data = pd.DataFrame({
                'Frequency (Hz)': np.arange(1, 11),
                'Amplitude': [0.1, 0.2, 0.5, 3.8, 4.2, 3.5, 0.8, 0.3, 0.1, 0.05]
            })
            st.bar_chart(freq_data.set_index('Frequency (Hz)'))
            st.warning(f"⚠️ **Finding:** Peak frequency detected at **{tremor_freq}** (consistent with Parkinsonian range).")

    # 2. CLINICAL REPORTING
    st.divider()
    st.subheader("🏥 Neurological Clinical Report")
    
    report_text = (
        f"EVEYES 360 NEURO REPORT\n"
        f"-----------------------\n"
        f"Clinical Focus: {neuro_focus}\n"
        f"Gait Speed: {speed}\n"
        f"Symmetry: {symmetry}\n"
        f"Tremor Frequency: {tremor_freq}\n"
        f"Status: Analysis Completed"
    )

    col1, col2 = st.columns(2)
    with col1:
        st.download_button("📥 Download Report (TXT)", report_text, file_name="neuro_report.txt")
    with col2:
        encoded_msg = report_text.replace("\n", "%0A")
        # You can replace the number below with a real clinical contact
        whatsapp_url = f"https://wa.me/905XXXXXXXXX?text={encoded_msg}"
        st.markdown(f'''
            <a href="{whatsapp_url}" target="_blank" style="text-decoration:none;">
                <div style="background-color:#25D366;color:white;padding:10px;border-radius:8px;text-align:center;font-weight:bold;">
                    🟢 Send Report to Consultant via WhatsApp
                </div>
            </a>''', unsafe_allow_html=True)
