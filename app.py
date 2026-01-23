import streamlit as st
from modules import metabolic, neuro, pediatric, derma, resp_sonic, therapy

st.set_page_config(page_title="EVEYES 360 Platinum", layout="wide", page_icon="🏥")

# --- LOGIN / ROLE SELECTION ---
st.sidebar.title("🏥 EVEYES 360")
user_role = st.sidebar.radio("Select Portal", ["Patient Portal", "Specialist Hub"])

if user_role == "Patient Portal":
    # Hastanın göreceği sade menü
    st.sidebar.divider()
    menu = ["🏠 My Dashboard", "💊 Therapy & Med-Tracker", "📸 Visual Exam Upload"]
    choice = st.sidebar.selectbox("Patient Menu", menu)

    if choice == "🏠 My Dashboard":
        st.title("Welcome back, Patient")
        st.info("Keep your daily logs updated for a better clinical assessment.")
        # Basit bir özet gösterimi
        st.metric("OMAD Adherence", "95%", "+2%")
        

    elif choice == "💊 Therapy & Med-Tracker":
        therapy.show_therapy() # Hastanın en çok kullanacağı modül

    elif choice == "📸 Visual Exam Upload":
        st.subheader("Visual Documentation")
        st.write("Capture images requested by your physician (Wounds, Moles, or Throat).")
        st.camera_input("Take Clinical Photo")

else:
    # SENİN (UZMANIN) GÖRECEĞİ DEV YAPI
    st.sidebar.divider()
    menu = ["🏠 Master Dashboard", "⚖️ Metabolic-360", "🧠 Neuro-Guard", 
            "👶 Pediatric-Pro", "🤳 Derma-Scan", "🫁 Resp-Sonic", "📊 Patient Analytics"]
    choice = st.sidebar.selectbox("Specialist Menu", menu)

    if choice == "🏠 Master Dashboard":
        st.title("🏥 Specialist Command Center")
        st.write("Review all clinical modules and patient synchronizations.")
        # Büyük yapı buraya geliyor
        col1, col2 = st.columns(2)
        with col1: st.info("### Active Patients: 124")
        with col2: st.warning("### Pending Reports: 8")
        

    elif choice == "⚖️ Metabolic-360": metabolic.show_metabolic()
    elif choice == "🧠 Neuro-Guard": neuro.show_neuro()
    # ... Diğer modüller buraya devam eder
