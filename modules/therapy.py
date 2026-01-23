import streamlit as st
import pandas as pd

def show_therapy():
    st.subheader("💊 Daily Therapy Log")
    
    col1, col2 = st.columns(2)
    with col1:
        weight = st.number_input("Today's Weight (kg)", value=75.0)
        waist = st.number_input("Waist Circumference (cm)", value=95.0)
    
    with col2:
        meds = st.multiselect("Meds Taken", ["Metformin", "Berberine", "Magnesium"])
        diet = st.checkbox("OMAD Protocol Completed?")

    if st.button("📤 Send Comprehensive Report to Doctor"):
        report = f"PATIENT REPORT\nWeight: {weight}\nWaist: {waist}\nMeds: {meds}\nDiet: {diet}"
        # WhatsApp Entegrasyonu
        msg = report.replace("\n", "%0A")
        st.markdown(f'[Click to Send via WhatsApp](https://wa.me/905XXXXXXXXX?text={msg})')
