import streamlit as st
import pandas as pd

def show_metabolic():
    st.title("⚖️ Metabolic-360: Analysis")
    
    pathway = st.selectbox("Clinical Pathway", 
                          ["General", "Cardiology (Heart Failure)", "Oncology (Cachexia)"])

    col1, col2 = st.columns(2)
    weight = col1.number_input("Weight (kg)", value=70.0)
    bia = col2.number_input("BIA Resistance (Ohm)", value=500)

    st.divider()
    if pathway == "Cardiology (Heart Failure)":
        if bia < 450: st.error("🚨 ALERT: Fluid retention detected!")
        else: st.success("✅ Stable cardiac load.")
    
    chart_data = pd.DataFrame({'Weight': [69.5, 69.8, weight]})
    st.line_chart(chart_data)
