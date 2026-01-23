import streamlit as st

# Modülleri güvenli bir şekilde import ediyoruz
try:
    from modules import metabolic, neuro, pediatric, derma, resp_sonic, therapy
except ImportError:
    st.error("Missing Module: Please ensure 'therapy.py' exists in the 'modules' folder.")

st.set_page_config(page_title="EVEYES 360 Platinum", layout="wide", page_icon="🏥")

# --- SIDEBAR: ROLE SELECTION ---
st.sidebar.title("🏥 EVEYES 360")
user_role = st.sidebar.radio("Select Portal", ["Patient Portal", "Specialist Hub"])

if user_role == "Patient Portal":
    st.sidebar.divider()
    menu = ["🏠 My Dashboard", "💊 Therapy & Med-Tracker", "📸 Live Clinical Scan"]
    choice = st.sidebar.selectbox("Patient Menu", menu)

    if choice == "🏠 My Dashboard":
        st.title("Welcome back, Patient")
        st.info("Keep your daily logs updated for a better clinical assessment.")
        st.metric("OMAD Adherence", "95%", "+2%")
        
    elif choice == "💊 Therapy & Med-Tracker":
        therapy.show_therapy()

    elif choice == "📸 Live Clinical Scan":
        st.title("🎥 Live Patient-Physician Connect")
        st.markdown("### Visual & Audio Clinical Session")
        st.write("Please record a video showing the area of concern. Describe your symptoms clearly while recording.")
        
        # Branş bağımsız Full Body/Face tarama alanı
        scan_mode = st.selectbox("Scanning Area", ["Full Body Scan", "Facial/Edema Scan", "Respiratory/Chest Scan", "Skin/Mole Scan"])
        
        # Sesli Video Kaydı (file_uploader mobilde kamerayı video modunda açar)
        clinical_video = st.file_uploader(f"Record {scan_mode} Video (Audio included)", type=["mp4", "mov", "avi"])
        
        if clinical_video:
            st.video(clinical_video)
            st.success(f"✅ {scan_mode} video and audio captured successfully.")
            if st.button("📤 Send Scan to Specialist"):
                st.info("Sending encrypted data to your physician...")

else:
    # UZMAN PANELİ (Tüm detaylar senin elinde)
    st.sidebar.divider()
    choice = st.sidebar.selectbox("Specialist Menu", 
                                  ["Metabolic-360", "Neuro-Guard", "Pediatric-Pro", "Derma-Scan", "Resp-Sonic"])
    
    if choice == "Metabolic-360": metabolic.show_metabolic()
    elif choice == "Neuro-Guard": neuro.show_neuro()
    elif choice == "Pediatric-Pro": pediatric.show_pediatric()
    elif choice == "Derma-Scan": derma.show_derma()
    elif choice == "Resp-Sonic": resp_sonic.show_resp()
