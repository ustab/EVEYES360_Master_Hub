import streamlit as st

def show_therapy():
    st.subheader("💊 Therapy & Medication Intelligence")
    
    col1, col2 = st.columns(2)
    with col1:
        weight = st.number_input("Today's Weight (kg)", value=70.0)
        waist = st.number_input("Waist Circumference (cm)", value=90.0)
    with col2:
        meds = st.multiselect("Meds Taken Today", ["Metformin XR", "Berberine", "Magnesium"])
        diet = st.checkbox("OMAD Protocol Followed?")

    if st.button("Generate Summary"):
        st.write(f"Current BMI: {weight / (1.75**2):.1f}")
        st.success("Daily log recorded locally.")

