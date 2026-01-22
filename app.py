import streamlit as st
from modules import metabolic, neuro, pediatric, derma, resp_sonic
import sys
import os
from modules import resp_sonic

# 1. Sayfa Ayarları
st.set_page_config(page_title="EVEYES 360 Platinum", layout="wide", page_icon="🏥")

# 2. DİL SÖZLÜĞÜ (Tüm ifadeler burada toplanır)
languages = {
    "Türkçe": {
        "menu_title": "Klinik Modül Seçin",
        "dashboard": "🏠 Dashboard",
        "welcome": "🏥 EVEYES 360 Klinik Merkez",
        "subtitle": "Klinik analize başlamak için soldan bir modül seçin.",
        "met_desc": "### ⚖️ Metabolic-360\n* Ödem Takibi\n* Kaşeksi İzleme",
        "neu_desc": "### 🧠 Neuro-Guard\n* Yürüyüş Analizi\n* Titreşim Frekansı",
        "ped_desc": "### 👶 Pediatric-Pro\n* M-CHAT Tarama\n* Büyüme Analitiği",
        "der_desc": "### 🤳 Derma-Scan\n* Yara İzleme\n* Ben Analizi",
        "res_desc": "### 🫁 Resp-Sonic\n* Ses ve Görüntü Analizi\n* Öksürük & Boğaz Muayenesi"
    },
    "English": {
        "menu_title": "Select Clinical Module",
        "dashboard": "🏠 Dashboard",
        "welcome": "🏥 EVEYES 360 Clinical Hub",
        "subtitle": "Select a module from the sidebar to start analysis.",
        "met_desc": "### ⚖️ Metabolic-360\n* Edema Tracking\n* Cachexia Monitoring",
        "neu_desc": "### 🧠 Neuro-Guard\n* Gait Analysis\n* Tremor Frequency",
        "ped_desc": "### 👶 Pediatric-Pro\n* M-CHAT Screening\n* Growth Analytics",
        "der_desc": "### 🤳 Derma-Scan\n* Wound Monitoring\n* Mole Analysis",
        "res_desc": "### 🫁 Resp-Sonic\n* Audio-Visual Analysis\n* Cough & Throat Inspection"
    }
}

# 3. DİL SEÇİMİ (Sidebar'ın en üstünde)
lang_choice = st.sidebar.radio("🌐 Language / Dil", ["Türkçe", "English"], horizontal=True)
t = languages[lang_choice] # Seçilen dilin paketini yükle

# 4. MENÜ
menu = [t["dashboard"], "Metabolic-360", "Neuro-Guard", "Pediatric-Pro", "Derma-Scan", "Resp-Sonic"]
choice = st.sidebar.selectbox(t["menu_title"], menu)

# 5. İÇERİK MANTIĞI
if choice == t["dashboard"]:
    st.title(t["welcome"])
    st.write(t["subtitle"])
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(t["met_desc"])
        st.warning(t["neu_desc"])
    with col2:
        st.success(t["ped_desc"])
        st.error(t["der_desc"])
    
    st.divider()
    st.help(t["res_desc"])

elif choice == "Metabolic-360":
    metabolic.show_metabolic()
# ... Diğer elif blokları aynı şekilde devam eder ...
