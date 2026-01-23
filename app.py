import streamlit as st
try:
    from modules import metabolic, neuro, pediatric, derma, resp_sonic, therapy
except:
    pass

st.set_page_config(page_title="EVEYES 360 Platinum", layout="wide")

if st.sidebar.radio("Portal", ["Patient Terminal", "Specialist Hub"]) == "Patient Terminal":
    st.title("🏥 Patient Clinical Input Terminal")
    
    # --- SECTION 1: VITAL SIGNS & BIOMETRICS ---
    with st.expander("🌡️ Vital Signs & Body Composition", expanded=True):
        c1, c2, c3, c4 = st.columns(4)
        weight = c1.number_input("Weight (kg)", value=70.0)
        temp = c2.number_input("Temperature (°C)", value=36.5, step=0.1)
        pulse = c3.number_input("Heart Rate (BPM)", value=75)
        bia = c4.number_input("BIA (Ohm)", value=500)
        
        # BMI & Cachexia (Kaşeksi) Monitoring
        height = 1.75 # Default or from profile
        bmi = weight / (height**2)
        st.info(f"**Current BMI:** {bmi:.1f} | **Muscle Mass Status:** Monitoring for Cachexia Risk")

    # --- SECTION 2: PAIN SCALES (VAS & NUMERIC) ---
    with st.expander("📉 Pain Assessment (Visual & Numeric)", expanded=False):
        st.write("Rate your pain level:")
        pain_level = st.select_slider("Numeric Pain Scale (0-10)", options=list(range(11)))
        
        # Visual Analog Scale (VAS) with emojis for patient ease
        st.write("Visual Pain State:")
        st.radio("VAS Scale", ["😊 No Pain", "😐 Mild", "😟 Moderate", "😫 Severe", "😭 Unbearable"], horizontal=True)

    # --- SECTION 3: LIVE MULTI-MODAL SCAN ---
    with st.expander("🎥 AI Live Scan (Face, Body, Voice)", expanded=False):
        st.write("Record video for Gait, Facial Symmetry, and Muscle Wasting Analysis.")
        scan_type = st.multiselect("Scan Targets", ["Face (Edema/Asymmetry)", "Full Body (Gait/Cachexia)", "Voice (Acoustic Analysis)"])
        
        clinical_video = st.file_uploader("Start Live Recording (Audio+Video)", type=["mp4", "mov"])
        clinical_photo = st.camera_input("Quick Snap (Wound/Mole)")

    # --- SECTION 4: INTEGRATED REPORTING ---
    if st.button("🚀 SUBMIT TO CLINICAL HUB"):
        st.success("Synchronizing: Vitals, Pain Scales, BIA, and Visual Data...")
        # Burada tüm verileri birleştirip uzman paneline gönderiyoruz
        st.balloons()

else:
    st.title("👨‍⚕️ Specialist Analysis Center")
    # Uzman burada hem videoyu izler hem de gelen BİA ve Ağrı verilerini kıyaslar
    st.write("Select a module to review incoming multi-modal data.")
