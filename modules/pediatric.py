import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def show_pediatric():  # <--- Hata buradaki isim uyumsuzluğundan kaynaklanıyor
    st.title("👶 Pediatric-Pro: Growth & Development")
    st.write("Physical Growth Tracking & Autism Screening (M-CHAT)")

    tab1, tab2 = st.tabs(["📏 Physical Growth", "🧠 M-CHAT Screening"])

    with tab1:
        st.subheader("Physical Growth Analysis")
        c1, c2, c3 = st.columns(3)
        age = c1.number_input("Age (Months)", min_value=0, max_value=60, value=12)
        weight = c2.number_input("Weight (kg)", value=10.0)
        height = c3.number_input("Height (cm)", value=75.0)
        
        # Basit bir persentil grafiği simülasyonu
        fig, ax = plt.subplots()
        ax.plot([0, 12, 24, 36], [3, 10, 13, 15], label="Normal Growth")
        ax.scatter([age], [weight], color='red', label="Current Child")
        ax.legend()
        st.pyplot(fig)

    with tab2:
        st.subheader("M-CHAT: Autism Early Warning")
        q1 = st.radio("Does your child look you in the eye?", ["Yes", "No"])
        if st.button("Calculate Risk"):
            if q1 == "No":
                st.warning("Potential risk detected. Consult a specialist.")
            else:
                st.success("Development appears normal.")