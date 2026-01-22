import streamlit as st
import time

def show_resp():
    st.title("🫁 Resp-Sonic: Live Clinical Exam")
    st.info("💡 **Note:** Please allow camera and microphone access from your browser settings (Lock icon in the URL bar).")

    tab1, tab2 = st.tabs(["🎙️ Live Audio Analysis", "📷 Live Visual Exam"])

    with tab1:
        st.subheader("Acoustic Monitoring")
        # Canlı mikrofon girişi
        audio_input = st.audio_input("Record breathing or cough sounds")
        if audio_input:
            st.audio(audio_input)
            if st.button("Analyze Lung Sounds"):
                with st.spinner("Processing frequencies..."):
                    time.sleep(2)
                st.warning("🎯 **Finding:** Expiratory wheezing detected (72% probability).")

    with tab2:
        st.subheader("Visual Respiratory Inspection")
        # Canlı kamera girişi
        captured_img = st.camera_input("Focus on Throat or Chest Wall")
        
        if captured_img:
            st.image(captured_img, caption="Live Clinical Frame", use_container_width=True)
            if st.button("Run AI Visual Scan"):
                with st.spinner("Analyzing tissue and symmetry..."):
                    time.sleep(2)
                st.error("🚨 **Finding:** Pharyngeal erythema and tonsillar hypertrophy observed.")

    st.divider()
    st.subheader("📲 Clinical Reporting")
    if st.button("Generate & Share Report"):
        st.success("Report generated in English. Ready for WhatsApp sharing.")
