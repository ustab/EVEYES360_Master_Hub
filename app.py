import streamlit as st

# Modülleri güvenli bir şekilde import ediyoruz
try:
    from modules import metabolic, neuro, pediatric, derma, resp_sonic, therapy
except ImportError:
    st.error("Missing Module: Please ensure all files exist in the 'modules' folder.")

st.set_page_config(page_title="EVEYES 360 Platinum", layout="wide", page_icon="🏥")

# --- SIDEBAR: ROLE SELECTION ---
st.sidebar.title("🏥 EVEYES 360")
user_role = st.sidebar.radio("Select Portal", ["Patient Portal", "Specialist Hub"])

if user_role == "Patient Portal":
    st.sidebar.divider()
    menu = ["🏠 My Dashboard", "💊 Therapy & Med-Tracker", "🎥 LIVE CLINICAL SCAN"]
    choice = st.sidebar.selectbox("Patient Menu", menu)

    if choice == "🏠 My Dashboard":
        st.title("Welcome back, Patient")
        st.info("Keep your daily logs updated for clinical assessment.")
        
    elif choice == "💊 Therapy & Med-Tracker":
        therapy.show_therapy()

    elif choice == "🎥 LIVE CLINICAL SCAN":
        st.title("📹 Live Audio-Visual Examination")
        st.warning("🔔 **Instruction:** When you click 'Start Recording', select 'Camera' and switch to **VIDEO** mode. Talk while recording to capture your voice.")
        
        # Bu bileşen mobilde doğrudan cihazın kamerasını video/ses kapasitesiyle tetikler
        clinical_video = st.camera_input("Take a Photo for Quick Reference") 
        
        st.write("--- OR ---")
        
        # ASIL VİDEO KAYIT ALANI (Sesli ve Canlı)
        video_data = st.file_uploader("Click here to Record Live Video & Audio", type=["mp4", "mov", "avi"])
        
        if video_data:
            st.video(video_data)
            st.success("✅ Video and Audio recorded and uploaded.")
            if st.button("📤 Sync with Specialist Hub"):
                st.balloons()
                st.info("Clinical data sent to your physician.")

else:
    # UZMAN PANELİ
    st.sidebar.divider()
    choice = st.sidebar.selectbox("Specialist Menu", 
                                  ["Metabolic-360", "Neuro-Guard", "Pediatric-Pro", "Derma-Scan", "Resp-Sonic"])
    
    # Modülleri gösterme mantığı aynı kalıyor
    if choice == "Metabolic-360": metabolic.show_metabolic()
    elif choice == "Neuro-Guard": neuro.show_neuro()
    elif choice == "Pediatric-Pro": pediatric.show_pediatric()
    elif choice == "Derma-Scan": derma.show_derma()
    elif choice == "Resp-Sonic": resp_sonic.show_resp()
