import streamlit as st
from modules import metabolic, neuro, pediatric, derma, resp_sonic

st.set_page_config(page_title="EVEYES 360", layout="wide", page_icon="🏥")

languages = {
    "Türkçe": {
        "menu": "Klinik Modül", "dash": "🏠 Dashboard", "welcome": "🏥 EVEYES 360 Klinik Merkez",
        "met": "### ⚖️ Metabolic-360\n* Ödem Takibi", "neu": "### 🧠 Neuro-Guard\n* Titreşim Analizi",
        "ped": "### 👶 Pediatric-Pro\n* Gelişim Takibi", "der": "### 🤳 Derma-Scan\n* Yara Analizi",
        "res": "### 🫁 Resp-Sonic\n* Ses & Görüntü"
    },
    "English": {
        "menu": "Clinical Module", "dash": "🏠 Dashboard", "welcome": "🏥 EVEYES 360 Clinical Hub",
        "met": "### ⚖️ Metabolic-360\n* Edema Tracking", "neu": "### 🧠 Neuro-Guard\n* Tremor Analysis",
        "ped": "### 👶 Pediatric-Pro\n* Growth Tracking", "der": "### 🤳 Derma-Scan\n* Wound Analysis",
        "res": "### 🫁 Resp-Sonic\n* Audio-Visual"
    }
}

lang = st.sidebar.radio("🌐 Language", ["Türkçe", "English"], horizontal=True)
t = languages[lang]

menu = [t["dash"], "Metabolic-360", "Neuro-Guard", "Pediatric-Pro", "Derma-Scan", "Resp-Sonic"]
choice = st.sidebar.selectbox(t["menu"], menu)

if choice == t["dash"]:
    st.title(t["welcome"])
    st.divider()
    c1, c2, c3 = st.columns(3)
    with c1: st.info(t["met"]); st.error(t["der"])
    with c2: st.warning(t["neu"]); st.success(t["res"])
    with c3: st.success(t["ped"])
elif choice == "Metabolic-360": metabolic.show_metabolic()
elif choice == "Neuro-Guard": neuro.show_neuro()
elif choice == "Pediatric-Pro": pediatric.show_pediatric()
elif choice == "Derma-Scan": derma.show_derma()
elif choice == "Resp-Sonic": resp_sonic.show_resp()
