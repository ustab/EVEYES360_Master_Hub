import streamlit as st
from modules import resp_sonic
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Modülleri içeri aktar
try:
    from modules import metabolic, pediatric, neuro, derma
except ImportError as e:
    st.error(f"Modül yükleme hatası: {e}")
    st.stop()

st.set_page_config(page_title="EVEYES 360 Platinum", layout="wide", page_icon="🛡️")

# --- MENÜ LİSTESİ ---
menu = [
    "🏠 Dashboard", 
    "Metabolic-360", 
    "Neuro-Guard", 
    "Pediatric-Pro", 
    "Derma-Scan",
    "Resp-Sonic (Lung & Throat)"
]

choice = st.sidebar.selectbox("Paket Seçiniz", menu)

# --- BAĞLANTI KONTROLÜ ---
if choice == "🏠 Dashboard":
    st.title("🏥 EVEYES 360 Klinik Merkez")
    st.write("Lütfen soldan bir analiz modülü seçin.")

elif choice == "Metabolic-360":
    metabolic.show_metabolic()

elif choice == "Neuro-Guard":
    neuro.show_neuro()

elif choice == "Pediatric-Pro":
    pediatric.show_pediatric()

elif choice == "Derma-Scan":
    derma.show_derma()
    
elif choice == "Resp-Sonic (Lung & Throat)":
    resp_sonic.show_resp()

# --- SIDEBAR ---
st.sidebar.success(f"Aktif Modül: {choice}") # Hangi modülde olduğunuzu yeşil bir kutuda gösterir
st.sidebar.title("🛡️ EVEYES 360")
st.sidebar.subheader("Clinical Intelligence Hub")

menu = ["🏠 Home / Dashboard", "Metabolic-360", "Neuro-Guard", "Pediatric-Pro", "Derma-Scan"]
choice = st.sidebar.selectbox("Select Health Package", menu)

# --- ANA SAYFA (HOS GELDINIZ) ---
if choice == "🏠 Home / Dashboard":
    st.title("🏥 Welcome to EVEYES 360")
    st.subheader("Your Unified Clinical Command Center")
    
    st.markdown("""
    EVEYES 360 is a modular AI-powered ecosystem designed to transform remote patient care. 
    Select a specialized package from the sidebar to begin clinical analysis.
    """)
    
    st.divider()

    # Paketlerin Özeti (Kart Yapısı)
    col1, col2 = st.columns(2)

    with col1:
        st.info("### ⚖️ Metabolic-360\n**Focus:** Fluid & Tissue Management.\n- Edema Detection\n- Cachexia Prevention\n- Heart & Kidney Monitoring")
        st.warning("### 🧠 Neuro-Guard\n**Focus:** Movement Disorders.\n- AI Gait Analysis\n- Tremor Frequency Tracking\n- Fall Risk Assessment")

    with col2:
        st.success("### 👶 Pediatric-Pro\n**Focus:** Child Development.\n- WHO Growth Percentiles\n- M-CHAT Autism Screening\n- Developmental Milestones")
        st.error("### 🤳 Derma-Scan\n**Focus:** Skin & Wound Vision.\n- Diabetic Foot Monitoring\n- ABCDE Mole Analysis\n- Healing Progress Tracking")

    st.divider()
    st.write("📞 **Need Help?** Contact your physician or our technical support via the secure clinical channel.")

# --- MODÜL YÖNLENDİRMELERİ ---
elif choice == "Metabolic-360":
    metabolic.show_metabolic()
elif choice == "Neuro-Guard":
    neuro.show_neuro()
elif choice == "Pediatric-Pro":
    pediatric.show_pediatric()
elif choice == "Derma-Scan":
    derma.show_derma()