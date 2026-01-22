import streamlit as st
import pandas as pd
import time

def show_pediatric():
    st.title("👶 Pediatric-Pro: Growth & Development")
    st.markdown("Clinical tracking for physical growth and neurodevelopmental milestones.")

    tab1, tab2 = st.tabs(["📏 Physical Growth", "🧠 Neurodevelopmental (M-CHAT)"])

    with tab1:
        st.subheader("Physical Growth Analysis")
        c1, c2, c3 = st.columns(3)
        age = c1.number_input("Age (Months)", min_value=0, max_value=60, value=12)
        weight = c2.number_input("Weight (kg)", value=10.0)
        height = c3.number_input("Height (cm)", value=75.0)
        
        # Growth Chart Simulation
        st.write("**Growth Percentile Trend**")
        chart_data = pd.DataFrame({
            "Months": [0, 12, 24, 36, 48, 60],
            "WHO Standard (kg)": [3.5, 9.5, 12.2, 14.3, 16.3, 18.3],
            "Current Child (kg)": [3.5, weight if age == 12 else 9.5, 12.2, 14.3, 16.3, 18.3]
        })
        st.line_chart(chart_data.set_index("Months"))
        
        

    with tab2:
        st.subheader("Live Clinical Observation")
        st.write("Use the camera to observe the child's interaction, eye contact, and motor response.")
        
        # Canlı Kamera Girişi
        child_frame = st.camera_input("Capture Child's Behavior")
        
        if child_frame:
            st.image(child_frame, caption="Behavioral Frame Captured")
            st.success("Visual data logged for developmental review.")

        st.divider()
        st.subheader("M-CHAT Screening Questions")
        q1 = st.radio("Does the child look you in the eye when you call their name?", ["Yes", "No"])
        q2 = st.radio("Does the child point to things to show interest?", ["Yes", "No"])
        
        if st.button("Assess Screening Risk"):
            if q1 == "No" or q2 == "No":
                st.warning("⚠️ **Alert:** Potential red flags detected. Refer to a Developmental Pediatrician.")
            else:
                st.success("✅ Interaction appears normal for this age group.")

    # Reporting
    st.divider()
    if st.button("📲 Generate Pediatric Report"):
        report = f"Pediatric Report\nAge: {age}mo\nWeight: {weight}kg\nRisk: {'High' if q1 == 'No' else 'Low'}"
        st.download_button("Download Report (TXT)", report, file_name="pediatric_report.txt")
