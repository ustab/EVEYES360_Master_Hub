import streamlit as st

def show_neuro():
    st.title("🧠 Neuro-Guard: Video Gait & Motor Scan")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Gait & Tremor Video Feed")
        neuro_video = st.file_uploader("Upload Patient Movement Video", type=["mp4", "mov"])
        if neuro_video:
            st.video(neuro_video)
            
    with col2:
        st.subheader("Neurological Markers")
        gait_stability = st.radio("Gait Stability", ["Stable", "Ataxic", "Shuffling Steps", "Unstable"])
        facial_symmetry = st.select_slider("Facial Symmetry Scale", options=["Normal", "Mild Droop", "Significant Asymmetry"])
        
        # Otomatik risk skoru simülasyonu
        risk_score = 0
        if gait_stability != "Stable": risk_score += 40
        if facial_symmetry != "Normal": risk_score += 30
        
        st.metric("Neuro-Disability Risk", f"%{risk_score}")
        
        if st.button("Generate Neuro Report"):
            st.write("Report ready for export.")
