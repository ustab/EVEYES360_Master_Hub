import streamlit as st
from modules import metabolic, neuro, pediatric, derma, resp_sonic

st.set_page_config(page_title="EVEYES 360 Platinum", layout="wide", page_icon="🏥")

# Sidebar Menu - English Only
st.sidebar.title("🏥 EVEYES 360")
menu = ["🏠 Dashboard", "Metabolic-360", "Neuro-Guard", "Pediatric-Pro", "Derma-Scan", "Resp-Sonic"]
choice = st.sidebar.selectbox("Select Clinical Module", menu)

if choice == "🏠 Dashboard":
    st.title("🏥 EVEYES 360 Clinical Hub")
    st.write("Comprehensive AI-powered clinical monitoring system.")
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("### ⚖️ Metabolic-360\n* Edema & Cachexia Tracking")
        st.error("### 🤳 Derma-Scan\n* Wound & Mole Analysis")
    with col2:
        st.warning("### 🧠 Neuro-Guard\n* Gait & Tremor Analysis")
        st.success("### 🫁 Resp-Sonic\n* Audio-Visual Inspection")
    with col3:
        st.success("### 👶 Pediatric-Pro\n* Growth & M-CHAT Tracking")

# Module Routing
elif choice == "Metabolic-360": metabolic.show_metabolic()
elif choice == "Neuro-Guard": neuro.show_neuro()
elif choice == "Pediatric-Pro": pediatric.show_pediatric()
elif choice == "Derma-Scan": derma.show_derma()
elif choice == "Resp-Sonic": resp_sonic.show_resp()
