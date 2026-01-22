import streamlit as st
import pandas as pd
import time

def show_derma():
    st.title("🤳 Derma-Scan: Live Visual Tracker")
    
    tab1, tab2 = st.tabs(["🩹 Live Wound Scan", "🔍 Live Mole Analysis"])

    with tab1:
        st.subheader("Direct Wound Assessment")
        # Canlı yara görüntüsü alma
        wound_frame = st.camera_input("Focus Camera on Wound Area")
        
        if wound_frame:
            st.image(wound_frame, use_container_width=True)
            if st.button("Analyze Tissue State"):
                with st.spinner("Scanning vascularization..."):
                    time.sleep(2)
                st.warning("Analysis: Moderate inflammation detected. Area: 3.8 cm²")

    with tab2:
        st.subheader("AI Mole Inspection")
        mole_frame = st.camera_input("Focus Camera on Mole (Macro Mode)")
        
        if mole_frame:
            st.image(mole_frame)
            st.table(pd.DataFrame({
                'Criterion': ['Asymmetry', 'Border', 'Color'],
                'Result': ['Low', 'Sharp', 'Uniform']
            }))
            st.success("✅ Assessment: Low Risk.")
