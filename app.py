import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# --- CONFIGURATION & STYLING ---
st.set_page_config(page_title="EVEYES 360 RPM", layout="wide", page_icon="🏥")

# --- DATA STORAGE SIMULATION ---
if 'patient_db' not in st.session_state:
    st.session_state.patient_db = pd.DataFrame({
        'Date': [datetime.now() - timedelta(days=i) for i in range(5, 0, -1)],
        'Weight': [75.0, 74.8, 75.2, 77.5, 78.0], # Simulated edema spike
        'BIA_Muscle': [32.0, 31.9, 32.1, 32.0, 31.8],
        'BIA_Oedema': [32.0, 31.9, 32.1, 32.0, 31.8],
        'Systolic': [120, 122, 125, 145, 150], # Simulated hypertension trend
        'SpO2': [98, 97, 98, 96, 94], # Simulated respiratory decline
        'Pain': [4, 4, 5, 7, 8]
    })
# --- 3. ANALİZ MOTORU (Kritik Değişkenler) ---
# Kodun ilerleyen yerlerinde hata almamak için farkları burada hesaplıyoruz
df = st.session_state.patient_db
today = df.iloc[-1]      # Listenin en sonundaki (bugünkü) veri
yesterday = df.iloc[-2]  # Listenin sondan ikinci (dünkü) verisi
# KARŞILAŞTIRMA DEĞİŞKENLERİ
w_diff = today['Weight'] - yesterday['Weight']
s_diff = today['Systolic'] - yesterday['Systolic']
b_diff = today['BIA_Muscle'] - yesterday['BIA_Muscle']
p_diff = today['Pain'] - yesterday['Pain']



# --- SIDEBAR NAVIGATION ---
# --- 4. YAN MENÜ YAPILANDIRMASI ---
st.sidebar.title("🏥 EVEYES 360 RPM")
user_role = st.sidebar.selectbox("System Access", ["Patient Portal", "Specialist Dashboard"])

# ==========================================
# 1. PATIENT PORTAL (Data Intake & Validation)
# ==========================================

# Kullanıcı Rolü Seçimi
user_role = st.sidebar.selectbox(
    "Select System Access", 
    ["Patient Portal", "Specialist Dashboard"]
)


# --- 5. ROL BAZLI YÖNLENDİRME (Ana Mantık) ---
if user_role == "Patient Portal":
    # Hastanın göreceği alt menüler
    st.sidebar.subheader("Patient Menu")
    patient_menu = [
        "🏠 Dashboard (Comparison)", 
        "📝 Daily Vital Entry", 
        "📊 Analytics & Report"
    ]
    choice = st.sidebar.radio("Navigation", patient_menu)



  # --- 6. HASTA DASHBOARD EKRANI ---
if choice == "🏠 Dashboard (Comparison)":
    st.title("📊 Clinical Progress: Yesterday vs Today")
    
    # Sayfayı 4 ana sütuna bölüyoruz
    c1, c2, c3, c4 = st.columns(4)
    
    # 1. Kolon: Kilo (Delta: inverse çünkü kilo artışı genelde ödem/risk demektir)
    c1.metric(
        label="Current Weight", 
        value=f"{today['Weight']} kg", 
        delta=f"{w_diff:.1f} kg", 
        delta_color="inverse"
    )
    # 2. Kolon: Tansiyon (Delta: inverse çünkü tansiyon artışı risk demektir)
    c2.metric(
        label="Systolic BP", 
        value=f"{today['Systolic']} mmHg", 
        delta=f"{s_diff:+d}", 
        delta_color="inverse"
    )
    
    # 3. Kolon: Kas Kütlesi (BIA)
    c3.metric(
        label="Muscle Mass (BIA)", 
        value=f"{today['BIA_Muscle']} kg", 
        delta=f"{b_diff:.1f} kg"
    )
    
    # 4. Kolon: Oksijen Satürasyonu (SpO2)
    spo2_diff = today['SpO2'] - yesterday['SpO2']
    c4.metric(
        label="SpO2 (%)", 
        value=f"{today['SpO2']}%", 
        delta=f"{spo2_diff}%"
    )

    st.divider()

    # Görselleştirme: Trend Grafiği
    st.subheader("📈 Physiological Trends (Last 5 Days)")
    # Kullanıcıya grafikte neyi görmek istediğini seçtiriyoruz
    chart_selection = st.multiselect(
        "Select parameters to view on chart:",
        ["Weight", "Systolic", "SpO2", "BIA_Muscle", "Pain"],
        default=["Weight", "Systolic"]
    )
    st.line_chart(df.set_index('Date')[chart_selection])

 

# --- 7. VERİ GİRİŞ EKRANI ---
elif choice == "📝 Daily Vital Entry":
    st.title("📝 Daily Clinical Entry")
    
    # Hedef Hasta Grubu (Senin taslağındaki 1. Madde)
    st.sidebar.info("Category: Chronic Care") 

    with st.form("vital_entry_form"):
        st.subheader("Physical & Biometric Data")
        
        c1, c2, c3 = st.columns(3)
        
        # Giriş Doğrulama (Hard Limits): Tıbben imkansız değerleri sınırlıyoruz
        new_w = c1.number_input("Weight (kg)", min_value=30.0, max_value=250.0, value=float(today['Weight']))
        new_s = c2.number_input("Systolic BP (mmHg)", min_value=50, max_value=250, value=int(today['Systolic']))
        new_sp = c3.number_input("SpO2 (%)", min_value=50, max_value=100, value=int(today['SpO2']))
        bia_muscle = st.slider("BIA Muscle Mass (kg)", 10.0, 60.0, 32.0)
        bia_oedema = st.slider("BIA oedema (kg)", 10.0, 60.0, 32.0)
        if systolic > 180 or spo2 < 90 or BIA increae:
            st.error("⚠️ CRITICAL VALUES DETECTED: Please contact your doctor immediately or call emergency services.")
        st.divider()



       st.subheader("BIA & Subjective Data")
        col_a, col_b = st.columns(2)
        new_b = col_a.slider("Muscle Mass (BIA - kg)", 10.0, 60.0, float(today['BIA_Muscle']))
        new_p = col_b.slider("Pain Level (0-10)", 0, 10, int(today['Pain']))

        
        st.subheader("BIA & Subjective Data")
        col_a, col_b = st.columns(2)
        new_b = col_a.slider("Muscle Mass (BIA - kg)", 10.0, 60.0, float(today['BIA_Muscle']))
        new_p = col_b.slider("Pain Level (0-10)", 0, 10, int(today['Pain']))
        new_oedema=col_c.slider("oedema Level (0-10)", 0, 10, int(today['oedema']))
        submit_button = st.form_submit_button("💾 Save & Check for Risks")

    # --- 8. ANOMALİ TESPİTİ VE UYARI SİSTEMİ ---
    if submit_button:
        # Kritik Durum Kontrolü (Red Alarm)
        if new_s > 180 or new_sp < 90 or  new_oedema> 5:
            st.error(f"🚨 CRITICAL ALERT: Your values (BP: {new_s}, SpO2: {new_sp}%) are at risk! Please contact your doctor.")
            
            # Acil Durum WhatsApp Butonu (Anında belirir)
            emergency_msg = f"EMERGENCY ALERT! Patient John Doe. BP: {new_s}, SpO2: {new_sp}%"
            st.markdown(f'''<a href="https://wa.me/905XXXXXXXXX?text={emergency_msg}" target="_blank">
            <button style="background-color:red;color:white;width:100%;padding:15px;border-radius:10px;font-weight:bold;cursor:pointer;">🚨 AUTO-ALERT DOCTOR NOW</button></a>''', unsafe_allow_html=True)
        else:
            st.success("✅ Your data has been successfully recorded and is within stable limits.")
            st.balloons() # Moral desteği için görsel efekt





BESINCI ADIMDAN DEVAM







    
    with tabs[1]:
        st.subheader("Camera & Imaging Analysis")
        scan_type = st.selectbox("Scan Type", ["Wound Recovery", "Movement/Range of Motion", "Edema Check"])
        st.camera_input("Capture Clinical Evidence")
        st.file_uploader("Upload Movement Video (Rehab/Gait)", type=["mp4", "mov"])

    with tabs[2]:
        st.subheader("Personal Progress Report")
        df = st.session_state.patient_db
        st.line_chart(df.set_index('Date')[['Weight', 'Systolic']])
        
    if st.button("📤 Sync Data to Clinical Hub"):
        st.success("Data validated and transmitted successfully.")
        st.balloons()

# ==========================================
# 2. SPECIALIST DASHBOARD (Decision Support)
# ==========================================
else:
    st.title("👨‍⚕️ Specialist Decision Support System")
    
    # 4. Triage System (Priority Categorization)
    st.subheader("🚨 Patient Triage & Alerts")
    t1, t2, t3 = st.columns(3)
    t1.metric("Critical (Red)", "2 Patients", "Action Required", delta_color="inverse")
    t2.metric("Stable", "14 Patients", "Normal")
    t3.metric("Follow-up", "5 Patients", "Pending Review")

    st.divider()

    # 3. Smart Data Processing (Anomaly & Correlation)
    st.subheader("🔍 Smart Trend Analysis (Patient: John Doe)")
    df = st.session_state.patient_db
    
    # Automated NLG (Natural Language Generation) Summary
    last_weight_change = df['Weight'].iloc[-1] - df['Weight'].iloc[-2]
    last_spo2 = df['SpO2'].iloc[-1]
    
    if last_weight_change > 1.5:
        st.warning(f"📊 **Anomaly Detected:** Rapid weight gain of {last_weight_change}kg in 24h. Possible Edema/Heart Failure exacerbation.")
    
    if last_spo2 < 95:
        st.error(f"🫁 **Correlation Alert:** SpO2 has dropped to {last_spo2}%. Cross-referencing with weight gain suggests fluid overload.")

    # Visualizing Correlations
    st.subheader("📈 Multi-Parametric Correlation")
    chart_choice = st.multiselect("Select Parameters to Overlay", ["Weight", "Systolic", "SpO2", "BIA_Muscle"], default=["Weight", "Systolic"])
    st.line_chart(df.set_index('Date')[chart_choice])

    if st.button("📝 Generate Automated Summary Report"):
        st.code(f"""
        FINAL CLINICAL SUMMARY:
        - Blood Pressure: Trending Upwards (Current: {df['Systolic'].iloc[-1]} mmHg)
        - SpO2: Critical Decline detected in last 48 hours.
        - Muscle Mass: Stable (BIA: {df['BIA_Muscle'].iloc[-1]}kg), confirming weight gain is likely fluid.
        - RECOMMENDATION: Adjust Diuretic Dosage / Immediate Clinical Visit.
        """)
        # --- TAB 3: STATISTICS & AUTO-REPORTING ---
    with tabs[2]:
        st.subheader("📊 Clinical Statistical Report & Auto-Dispatch")
        
        if st.button("📝 Generate & Analyze Statistics"):
            df = st.session_state.patient_db
            avg_bp = df['Systolic'].mean()
            weight_trend = "INCREASING" if w_diff > 0 else "DECREASING"
            
            # Formatted Report
            report_body = (
                f"🏥 EVEYES 360 CLINICAL ANALYTICS\n"
                f"--------------------------------------\n"
                f"Date: {datetime.now().strftime('%Y-%m-%d')}\n\n"
                f"1. STATISTICAL SUMMARY:\n"
                f"- Weight Trend: {weight_trend} ({w_diff:+.1f} kg in 24h)\n"
                f"- Mean Systolic BP (5-Day): {avg_bp:.1f} mmHg\n"
                f"- Current SpO2: {df['SpO2'].iloc[-1]}%\n\n"
                f"2. AI INTERPRETATION:\n"
                f"Weight gain detected without muscle mass increase.\n"
                f"Potential FLUID RETENTION (Edema) suspected.\n"
                f"Rising BP and falling SpO2 require urgent review.\n"
                f"--------------------------------------"
            )
            
            st.code(report_body)
            
            # --- AUTO-DISPATCH ---
            encoded_msg = report_body.replace("\n", "%0A").replace(" ", "%20")
            col_wa, col_mail = st.columns(2)
            
            with col_wa:
                st.markdown(f'''<a href="https://wa.me/905XXXXXXXXX?text={encoded_msg}" target="_blank">
                <button style="background-color:#25D366;color:white;width:100%;padding:12px;border:none;border-radius:10px;font-weight:bold;cursor:pointer;">🚀 Send via WhatsApp</button></a>''', unsafe_allow_html=True)
            
            with col_mail:
                mail_url = f"mailto:doctor@hospital.com?subject=Clinical_Alert&body={encoded_msg}"
                st.markdown(f'<a href="{mail_url}"><button style="background-color:#0078D4;color:white;width:100%;padding:12px;border-radius:10px;border:none;font-weight:bold;cursor:pointer;">📧 Send via Email</button></a>', unsafe_allow_html=True)

else:
    st.title("👨‍⚕️ Specialist Dashboard")
    st.dataframe(st.session_state.patient_db, use_container_width=True)





