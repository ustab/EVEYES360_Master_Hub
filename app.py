import streamlit as st
import pandas as pd
import numpy as np

# Modülleri güvenli çağır
try:
    from modules import metabolic, neuro, pediatric, derma, resp_sonic, therapy
except:
    pass

st.set_page_config(page_title="EVEYES 360 Platinum", layout="wide")

# --- ROLE SELECTION ---
user_role = st.sidebar.radio("Portal", ["Patient Terminal", "Specialist Hub"])

if user_role == "Patient Terminal":
    st.sidebar.title("🏥 Patient Menu")
    menu = ["🏠 Dashboard (My Stats)", "📝 Daily Clinical Input", "💊 Medication Tracker"]
    choice = st.sidebar.selectbox("Go to:", menu)

    if choice == "🏠 Dashboard (My Stats)":
        st.title("📊 My Health Dashboard")
        
        # --- ÖZET METRİKLER ---
        st.subheader("Current Status")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Current Weight", "70.2 kg", "-0.8 kg")
        m2.metric("BIA (Resistance)", "510 Ohm", "+5 Ohm")
        m3.metric("BMI", "22.9", "Stable")
        m4.metric("Muscle Mass", "High", "Kaşeksi Riski Yok")

        # --- KİLO & BİA TAKİP GRAFİĞİ ---
        st.subheader("📈 Body Composition Trends")
        chart_data = pd.DataFrame({
            'Day': range(1, 8),
            'Weight (kg)': [72.0, 71.5, 71.2, 70.8, 70.5, 70.3, 70.2],
            'BIA (Ohm)': [480, 485, 490, 495, 500, 505, 510]
        })
        
        tab1, tab2 = st.tabs(["Weight Trend", "BİA & Hydration Trend"])
        with tab1:
            st.line_chart(chart_data.set_index('Day')['Weight (kg)'])
        with tab2:
            st.area_chart(chart_data.set_index('Day')['BIA (Ohm)'])
            st.info("💡 BİA değerindeki artış vücut direncinin (kas/yağ dengesi) değişimini gösterir.")

    elif choice == "📝 Daily Clinical Input":
        # Senin istediğin o devasa giriş formu burada
        st.title("📝 Clinical Input Terminal")
        
        with st.expander("🌡️ Vitals & BİA Data", expanded=True):
            c1, c2, c3 = st.columns(3)
            w = c1.number_input("Kilo (kg)", value=70.0)
            t = c2.number_input("Ateş (°C)", value=36.5)
            b = c3.number_input("BİA (Ohm)", value=500)

        with st.expander("📉 Pain Scales (VAS & Numeric)", expanded=True):
            pain_num = st.slider("Ağrı Seviyesi (0-10)", 0, 10, 3)
            st.write("Görsel Ağrı Skalası (VAS)")
            st.radio("Durum:", ["😊 Ağrı Yok", "😐 Hafif", "😟 Orta", "😫 Şiddetli", "😭 Dayanılmaz"], horizontal=True)

        with st.expander("🎥 AI Live Scan (Face, Body, Voice)", expanded=False):
            st.file_uploader("Canlı Video Kaydı (Vücut/Yüz Tarama)", type=["mp4", "mov"])

    elif choice == "💊 Medication Tracker":
        therapy.show_therapy()

else:
    # UZMAN PORTALI (Modüller burada)
    st.title("👨‍⚕️ Specialist Analysis Center")
    dept = st.sidebar.selectbox("Branş Modülleri", ["Metabolic", "Neuro", "Derma", "Pediatric"])
    
    if dept == "Metabolic": metabolic.show_metabolic()
    # ... diğer branşlar
