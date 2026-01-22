import streamlit as st
import pandas as pd

def show_pediatric():
    st.title("👶 Pediatric-Pro: Growth & Development")
    st.write("Physical Growth Tracking & Autism Screening (M-CHAT)")

    tab1, tab2 = st.tabs(["📏 Physical Growth", "🧠 M-CHAT Screening"])

    with tab1:
        st.subheader("Physical Growth Analysis")
        c1, c2, c3 = st.columns(3)
        age = c1.number_input("Age (Months)", min_value=0, max_value=60, value=12)
        weight = c2.number_input("Weight (kg)", value=10.0)
        height = c3.number_input("Height (cm)", value=75.0)
        
        # Grafik için veri hazırlığı (Matplotlib yerine Streamlit Chart)
        chart_data = pd.DataFrame({
            "Months": [0, 12, 24, 36, 48, 60],
            "Normal Weight (kg)": [3.5, 10, 12.5, 14.5, 16.5, 18.5],
            "Child Weight (kg)": [3.5, weight if age == 12 else 10, 12.5, 14.5, 16.5, 18.5]
        })
        st.line_chart(chart_data.set_index("Months"))
        st.info("💡 Red line indicates the average growth percentile.")

    with tab2:
        st.subheader("M-CHAT: Autism Early Warning")
        st.write("Please answer the following questions based on the child's behavior.")
        
        q1 = st.radio("Does your child look you in the eye?", ["Yes", "No"], key="q1")
        q2 = st.radio("Does your child point to things he/she wants?", ["Yes", "No"], key="q2")
        
        if st.button("Calculate Development Risk"):
            if q1 == "No" or q2 == "No":
                st.warning("⚠️ **Risk detected.** Further clinical evaluation is recommended.")
            else:
                st.success("✅ Development appears within normal range for this age.")

    # WhatsApp Raporlama
    st.divider()
    if st.button("📲 Send Report to Pediatrician"):
        report = f"Pediatric Report - Age: {age}mo, Weight: {weight}kg, Height: {height}cm"
        encoded_report = report.replace(" ", "%20")
        st.markdown(f'[🟢 WhatsApp Report](https://wa.me/905XXXXXXXXX?text={encoded_report})', unsafe_allow_html=True)
