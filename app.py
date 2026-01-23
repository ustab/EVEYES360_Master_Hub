import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# --- CONFIGURATION ---
st.set_page_config(page_title="EVEYES 360 RPM Platinum", layout="wide", page_icon="🏥")

# --- DATA STORAGE SIMULATION ---
if 'patient_db' not in st.session_state:
    st.session_state.patient_db = pd.DataFrame({
        'Date': [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(4, -1, -1)],
        'Weight': [75.0, 74.8, 75.2, 77.5, 78.0],
        'BIA_Muscle': [32.0, 31.9, 32.1, 32.0, 31.8],
        'Systolic': [120, 122, 125, 145, 150],
        'SpO2': [98, 97, 98, 96, 94],
        'Pain': [4, 4, 5, 7, 8]
    })

# --- SIDEBAR ---
st.sidebar.title("🏥 EVEYES 360 RPM")
user_role = st.sidebar.selectbox("System Access", ["Patient Portal", "Specialist Dashboard"])

if user_role == "Patient Portal":
    st.title("📱 Patient Clinical Terminal")
    tabs = st.tabs(["🏠 My Dashboard", "📝 Daily Input", "📤 Reports & Dispatch"])

    # --- TAB 1: COMPARATIVE DASHBOARD ---
    with tabs[0]:
        st.subheader("🔄 24-Hour Clinical Comparison")
        df = st.session_state.patient_db
        w_diff = df['Weight'].iloc[-1] - df['Weight'].iloc[-2]
        s_diff = df['Systolic'].iloc[-1] - df['Systolic'].iloc[-2]
        p_diff = df['Pain'].iloc[-1] - df['Pain'].iloc[-2]
        b_diff = df['BIA_Muscle'].iloc[-1] - df['BIA_Muscle'].iloc[-2]

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Current Weight", f"{df['Weight'].iloc[-1]} kg", f"{w_diff:.1f} kg", delta_color="inverse")
        c2.metric("Systolic BP", f"{df['Systolic'].iloc[-1]} mmHg", f"{s_diff:+d}", delta_color="inverse")
        c3.metric("Pain Level", f"{df['Pain'].iloc[-1]}/10", f"{p_diff:+d}", delta_color="inverse")
        c4.metric("Muscle Mass (BIA)", f"{df['BIA_Muscle'].iloc[-1]} kg", f"{b_diff:.1f} kg")
        st.line_chart(df.set_index('Date')[['Weight', 'Systolic', 'Pain']])

    # --- TAB 2: DAILY INPUT ---
    with tabs[1]:
        st.subheader("Enter Daily Measurements")
        with st.form("input_form"):
            col1, col2, col3 = st.columns(3)
            new_w = col1.number_input("Weight (kg)", 30.0, 250.0, 78.0)
            new_s = col2.number_input("Systolic BP", 50, 250, 150)
            new_sp = col3.number_input("SpO2 (%)", 50, 100, 94)
            new_p = st.slider("Pain Level", 0, 10, 8)
            save = st.form_submit_button("💾 Save to Record")
            if save: st.success("Data stored in clinical history.")

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
