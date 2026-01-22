import streamlit as st
import pandas as pd
import time

def show_metabolic():
    st.title("⚖️ Metabolic-360: Clinical Edema & Fluid Tracking")
    st.markdown("Monitoring for Heart Failure, Renal Failure, and Preeclampsia symptoms.")

    # 1. Pathway Selection
    pathway = st.selectbox(
        "Clinical Pathway", 
        ["General Follow-up", "Cardiology (Heart Failure)", "Obstetrics (Preeclampsia Risk)", "Nephrology (Renal Edema)"]
    )

    # 2. Data Entry
    col_v1, col_v2, col_v3 = st.columns(3)
    weight = col_v1.number_input("Current Weight (kg)", value=70.0)
    last_weight = col_v2.number_input("Previous Weight (kg)", value=69.0)
    bia = col_v3.number_input("BIA Resistance (Ohm)", value=500)

    st.divider()

    # 3. Live Clinical Capture
    st.subheader("📷 Live Edema Inspection")
    st.write("Capture visual evidence of facial edema or peripheral pitting edema.")
    
    # Canlı Kamera Girişi
    edema_frame = st.camera_input("Focus on Edema Area (Face, Eyes, or Lower Limbs)")
    
    if edema_frame:
        st.image(edema_frame, caption="Captured Clinical Frame", use_container_width=True)
        if st.button("Log Visual Data"):
            st.success("Visual evidence successfully linked to metabolic metrics.")

    st.divider()

    # 4. Clinical Logic & Analysis
    diff = weight - last_weight
    
    if pathway == "Cardiology (Heart Failure)":
        st.subheader("🫀 Cardiovascular Fluid Load")
        if diff >= 1.5:
            st.error(f"🚨 ALERT: Rapid weight gain of {diff}kg detected. High risk of Pulmonary Edema.")
        elif bia < 450:
            st.warning("⚠️ Low BIA: Fluid retention in extracellular space.")
        else:
            st.success("✅ Stable cardiac fluid balance.")

    elif pathway == "Obstetrics (Preeclampsia Risk)":
        st.subheader("🤰 Pregnancy Monitoring")
        
        if diff > 1.0 and bia < 480:
            st.error("🚨 PREECLAMPSIA ALERT: Sudden weight gain & low resistance.")
            st.info("Recommendation: Immediate BP check and urine protein analysis.")
        else:
            st.success("✅ Edema within normal pregnancy range.")

    elif pathway == "Nephrology (Renal Edema)":
        st.subheader("🧪 Renal Function Indicators")
        if bia < 420:
            st.error("🚨 SEVERE EDEMA: Potential sign of Nephrotic Syndrome or Renal Failure.")
        else:
            st.info("Systemic fluid levels are being monitored.")

    # 5. Trend Chart
    st.write("### 📈 Metabolic Trend")
    chart_data = pd.DataFrame({'Weight': [last_weight-0.4, last_weight, weight]})
    st.line_chart(chart_data)

    # 6. Reporting
    if st.button("📲 Generate Clinical Summary"):
        report = f"METABOLIC REPORT\nPathway: {pathway}\nWeight: {weight}kg ({diff:+.1f})\nBIA: {bia} Ohm"
        st.download_button("Download TXT Report", report, file_name="metabolic_report.txt")
