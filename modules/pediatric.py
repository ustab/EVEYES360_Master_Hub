import streamlit as st
import pandas as pd

def show_pediatric():
    st.title("👶 Pediatric-Pro: Neuro-Developmental Video Analysis")
    st.markdown("Monitor developmental milestones and physical growth through visual evidence.")

    # Uzman Analiz Paneli
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📹 Clinical Observation Video")
        st.info("💡 Review video for: Eye contact, social smiling, motor coordination, and primitive reflexes.")
        ped_video = st.file_uploader("Upload Pediatric Observation Video", type=["mp4", "mov"])
        
        if ped_video:
            st.video(ped_video)
            st.caption("Scan video for spontaneous movements or behavioral red flags.")

    with col2:
        st.subheader("🧠 Developmental Assessment")
        
        # M-CHAT & Milestone Puanlaması
        eye_contact = st.select_slider("Social Interaction / Eye Contact", options=["Absent", "Poor", "Occasional", "Typical"])
        motor_milestone = st.selectbox("Motor Milestone Status", ["Delayed", "Emerging", "Age-Appropriate", "Advanced"])
        
        st.divider()
        st.subheader("📏 Physical Metrics")
        weight = st.number_input("Weight (kg)", value=10.0)
        height = st.number_input("Height (cm)", value=75.0)
        head_circ = st.number_input("Head Circumference (cm)", value=45.0)

    # Büyüme Eğrisi Analizi
    st.divider()
    st.subheader("📈 WHO Growth Percentile Simulation")
    # Örnek veri seti
    growth_data = pd.DataFrame({
        'Month': [0, 6, 12, 18, 24],
        'WHO 50th Percentile': [3.5, 7.5, 9.5, 11.0, 12.2],
        'Patient Growth': [3.5, 7.2, 9.2, 10.5, weight]
    })
    st.line_chart(growth_data.set_index('Month'))
    

    # Klinik Karar ve Raporlama
    if st.button("📋 Generate Pediatric Development Report"):
        risk = "High" if eye_contact in ["Absent", "Poor"] else "Normal"
        summary = f"PEDIATRIC REPORT\nStatus: {motor_milestone}\nSocial Risk: {risk}\nBMI/Growth: Tracked"
        st.code(summary)
        st.success("Report ready for physician's final signature.")
