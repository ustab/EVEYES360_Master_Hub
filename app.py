import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="EVEYES 360 RPM Demo", layout="wide")

# --- SIMULATED EMERGENCY CONTACT ---
DOCTOR_WHATSAPP = "905XXXXXXXXX" 

# --- DATA STORAGE ---
if 'history' not in st.session_state:
    st.session_state.history = []

# --- APP LAYOUT ---
st.sidebar.title("🏥 EVEYES 360 Hub")
mode = st.sidebar.radio("Navigation", ["Patient Terminal", "Specialist Dashboard"])

if mode == "Patient Terminal":
    st.title("📱 Patient Input & Emergency Portal")
    
    with st.form("daily_entry"):
        st.subheader("Vital Signs Entry")
        c1, c2, c3 = st.columns(3)
        sys = c1.number_input("Systolic BP (mmHg)", 70, 250, 120)
        spo2 = c2.number_input("SpO2 (%)", 50, 100, 98)
        weight = c3.number_input("Weight (kg)", 30.0, 200.0, 75.0)
        
        bia = st.slider("BIA Resistance (Ohm)", 300, 800, 500)
        note = st.text_area("Symptoms / Notes", "Feeling okay today.")
        
        submit = st.form_submit_button("💾 Save & Analyze")

    if submit:
        # Save to history
        entry = {"date": datetime.now(), "sys": sys, "spo2": spo2, "weight": weight, "bia": bia}
        st.session_state.history.append(entry)
        
        # --- 🚨 AUTOMATIC EMERGENCY LOGIC ---
        is_emergency = False
        alert_msg = ""
        
        if sys > 180:
            is_emergency = True
            alert_msg = f"CRITICAL HYPERTENSION DETECTED ({sys} mmHg)!"
        elif spo2 < 92:
            is_emergency = True
            alert_msg = f"CRITICAL HYPOXIA DETECTED (SpO2: {spo2}%)!"
            
        if is_emergency:
            st.error(f"⚠️ {alert_msg}")
            # Automatic WhatsApp Trigger for Emergencies
            auto_report = f"🚨 *EMERGENCY ALERT*%0AUser: John Doe%0AStatus: {alert_msg}%0ABIA: {bia} Ohm"
            st.markdown(f'''
                <a href="https://wa.me/{DOCTOR_WHATSAPP}?text={auto_report}" target="_blank">
                    <button style="background-color:#FF4B4B; color:white; border:none; padding:15px; border-radius:10px; width:100%; font-weight:bold;">
                        AUTO-ALERT: Notify Doctor Immediately
                    </button>
                </a>''', unsafe_allow_html=True)
        else:
            st.success("✅ Vitals are within stable range.")

    # --- 📤 MANUAL REPORT OPTION ---
    st.divider()
    st.subheader("Manual Reporting")
    if st.button("📄 Generate Full Clinical Report"):
        full_report = f"🏥 *EVEYES 360 CLINICAL UPDATE*%0AWeight: {weight}kg%0ABP: {sys} mmHg%0ASpO2: {spo2}%%0ANote: {note}"
        st.markdown(f'''
            <a href="https://wa.me/{DOCTOR_WHATSAPP}?text={full_report}" target="_blank">
                <button style="background-color:#25D366; color:white; border:none; padding:12px; border-radius:8px; width:100%;">
                    Send Full Report to Physician (WhatsApp)
                </button>
            </a>''', unsafe_allow_html=True)

else:
    # --- SPECIALIST DASHBOARD ---
    st.title("👨‍⚕️ Specialist Decision Support")
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        
        # Triage Display
        latest = df.iloc[-1]
        status = "🔴 CRITICAL" if (latest['sys'] > 180 or latest['spo2'] < 92) else "🟢 STABLE"
        
        st.metric("Patient Status", status)
        st.subheader("Vital Trends")
        st.line_chart(df.set_index('date')[['sys', 'spo2']])
    else:
        st.info("No patient data available yet.")

