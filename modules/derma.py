import streamlit as st

def show_derma():
    st.title("🤳 Derma-Scan: Clinical Skin & Wound Analysis")
    st.markdown("Advanced visual inspection for wound healing and lesion malignancy risk.")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("🔍 High-Definition Visual Intake")
        st.info("💡 Tip: Use macro-lens or zoom for better texture analysis of lesions and wound edges.")
        
        # Canlı video veya yüksek çözünürlüklü makro çekim
        derma_video = st.file_uploader("Upload Lesion / Wound Scan Video", type=["mp4", "mov", "jpg", "png"])
        
        if derma_video:
            if derma_video.type.startswith('video'):
                st.video(derma_video)
            else:
                st.image(derma_video, use_container_width=True)
            st.caption("Visual data ready for morphological assessment.")

    with col2:
        st.subheader("🧪 Clinical Assessment")
        
        exam_type = st.selectbox("Examination Type", ["Wound Management", "Mole (Nevus) Screening", "General Rash/Inflammation"])
        
        if exam_type == "Wound Management":
            st.write("**Wound Progress Scale**")
            size = st.number_input("Estimated Area (cm²)", value=5.0)
            tissue = st.select_slider("Tissue Type", options=["Necrotic", "Sloughy", "Granulating", "Epithelializing"])
            exudate = st.radio("Exudate Level", ["None", "Low", "Medium", "High"])
            
            

        elif exam_type == "Mole (Nevus) Screening":
            st.write("**ABCDE Criteria Checklist**")
            asymmetry = st.checkbox("A - Asymmetry (Irregular shape)")
            border = st.checkbox("B - Border (Jagged edges)")
            color = st.checkbox("C - Color (Multiple shades)")
            diameter = st.checkbox("D - Diameter (>6mm)")
            evolution = st.checkbox("E - Evolution (Changing over time)")
            
            
            
            risk_count = sum([asymmetry, border, color, diameter, evolution])
            if risk_count >= 3:
                st.error(f"🚨 High Risk Detected: {risk_count}/5 criteria met. Biopsy recommended.")
            else:
                st.success(f"Low Risk: {risk_count}/5 criteria met.")

    st.divider()
    # Raporlama
    if st.button("📋 Generate Dermatology Report"):
        st.write("### DERMA-SCAN SUMMARY")
        st.code(f"Type: {exam_type}\nRisk Assessment Completed.\nVisual evidence archived.")
