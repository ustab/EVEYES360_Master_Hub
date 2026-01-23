import streamlit as st

def show_metabolic():
    st.title("⚖️ Metabolic-360 Specialist Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Video Evidence Review")
        # Uzman hastadan gelen videoyu buraya yükleyip izler
        uploaded_video = st.file_uploader("Upload Patient Video for Analysis", type=["mp4", "mov"])
        if uploaded_video:
            st.video(uploaded_video)
    
    with col2:
        st.subheader("Clinical Grading")
        # Gode bırakan ödem (Pitting Edema) skalası
        edema_level = st.select_slider(
            "Pitting Edema Grade",
            options=["Grade 0", "Grade +1", "Grade +2", "Grade +3", "Grade +4"]
        )
        
        st.info(f"Selected: {edema_level}")
        
        # Klinik yorum alanı
        clinical_note = st.text_area("Physician's Observation Note", "Facial puffiness observed, bilateral lower extremity edema present.")
        
        if st.button("Finalize Metabolic Assessment"):
            st.success("Assessment logged into patient history.")
