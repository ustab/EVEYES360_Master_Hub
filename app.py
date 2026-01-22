import streamlit as st
from modules import metabolic, neuro, pediatric, derma, resp_sonic

# 1. Sayfa Konfigürasyonu
st.set_page_config(page_title="EVEYES 360", layout="wide", page_icon="🏥")

# 2. Dil Sözlüğü (Tüm metinleri tek yerden yönetiyoruz)
languages = {
    "Türkçe": {
        "menu_title": "Klinik Modül",
        "dash_name": "🏠 Dashboard",
        "welcome": "🏥 EVEYES 360 Klinik Merkez",
        "subtitle": "Klinik analize başlamak için soldan bir modül seçin.",
        "met": "### ⚖️ Metabolic-360\n* Ödem ve Kaşeksi Takibi",
        "neu": "### 🧠 Neuro-Guard\n* Yürüyüş ve Titreşim Analizi",
        "ped": "### 👶 Pediatric-Pro\n* M-CHAT ve Büyüme Takibi",
        "der": "### 🤳 Derma-Scan\n* Yara ve Ben Analizi",
        "res": "### 🫁 Resp-Sonic\n* Ses ve Görüntü Muayenesi"
    },
    "English": {
        "menu_title": "Clinical Module",
        "dash_name": "🏠 Dashboard",
        "welcome": "🏥 EVEYES 360 Clinical Hub",
        "subtitle": "Select a module from the sidebar to start analysis.",
        "met": "### ⚖️ Metabolic-360\n* Edema & Cachexia Tracking",
        "neu": "### 🧠 Neuro-Guard\n* Gait & Tremor Analysis",
        "ped": "### 👶 Pediatric-Pro\n* M-CHAT & Growth Tracking",
        "der": "### 🤳 Derma-Scan\n* Wound & Mole Analysis",
        "res": "### 🫁 Resp-Sonic\n* Audio-Visual Inspection"
    }
}

# 3. Sidebar: Dil Seçimi
lang = st.sidebar.radio("🌐 Language / Dil", ["Türkçe", "English"], horizontal=True)
t = languages[lang]

# 4. Sidebar: Menü Seçimi
# NOT: Menü isimleri sabit kalmalı ki modülleri çağırırken hata olmasın
menu = [t["dash_name"], "Metabolic-360", "Neuro-Guard", "Pediatric-Pro", "Derma-Scan", "Resp-Sonic"]
choice = st.sidebar.selectbox(t["menu_title"], menu)

# 5. Sayfa İçerikleri (Hangi modülün açılacağını burası belirler)
if choice == t["dash_name"]:
    st.title(t["welcome"])
    st.write(t["subtitle"])
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(t["met"])
        st.warning(t["neu"])
    with col2:
        st.success(t["ped"])
        st.error(t["der"])
    
    st.divider()
    st.help(t["res"])

# BURASI ÇOK ÖNEMLİ: Menüdeki isimle alttakiler birebir aynı olmalı
elif choice == "Metabolic-360":
    metabolic.show_metabolic()

elif choice == "Neuro-Guard":
    neuro.show_neuro()

elif choice == "Pediatric-Pro":
    pediatric.show_pediatric()

elif choice == "Derma-Scan":
    derma.show_derma()

elif choice == "Resp-Sonic":
    resp_sonic.show_resp()

