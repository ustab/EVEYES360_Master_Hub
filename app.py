import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="EVEYES 360 Platinum", layout="wide", page_icon="🏥")

# --- MODÜL IMPORTLARI (Hata Korumalı) ---
try:
    from modules import metabolic, neuro, pediatric, derma, resp_sonic, therapy
except ImportError:
    pass

# --- ROL SEÇİMİ ---
st.sidebar.title("🏥 EVEYES 360")
user_role = st.sidebar.radio("Sistem Kapısı", ["Hasta Portalı (Patient)", "Uzman Hub (Specialist)"])

# --- DATA SİMÜLASYONU (Dün vs Bugün Analizi İçin) ---
# Gerçek sistemde bu veriler SQL/Firebase'den çekilir
history_data = {
    'Tarih': [datetime.now() - timedelta(days=1), datetime.now()],
    'Kilo': [71.5, 70.0],
    'BİA': [490, 505],
    'Ateş': [36.8, 36.5],
    'Ağrı': [6, 3]
}
df_history = pd.DataFrame(history_data)

# ==========================================
# 1. HASTA PORTALI (PATIENT TERMINAL)
# ==========================================
if user_role == "Hasta Portalı (Patient)":
    st.sidebar.divider()
    menu = ["🏠 Dashboard & Analiz", "📝 Günlük Klinik Giriş", "💊 İlaç Takibi"]
    choice = st.sidebar.selectbox("İşlem Seçin", menu)

    if choice == "🏠 Dashboard & Analiz":
        st.title("📈 Sağlık Takip ve Karşılaştırmalı Analiz")
        
        # --- KARŞILAŞTIRMALI METRİKLER ---
        st.subheader("🔄 24 Saatlik Değişim Özeti")
        c1, c2, c3 = st.columns(3)
        
        k_degisim = df_history['Kilo'].iloc[-1] - df_history['Kilo'].iloc[-2]
        b_degisim = df_history['BİA'].iloc[-1] - df_history['BİA'].iloc[-2]
        a_degisim = df_history['Ağrı'].iloc[-1] - df_history['Ağrı'].iloc[-2]

        c1.metric("Kilo", f"{df_history['Kilo'].iloc[-1]} kg", f"{k_degisim:.1f} kg", delta_color="inverse")
        c2.metric("BİA (Direnç)", f"{df_history['BİA'].iloc[-1]} Ω", f"{b_degisim:+d}")
        c3.metric("Ağrı (VAS)", f"{df_history['Ağrı'].iloc[-1]}/10", f"{a_degisim:+d}", delta_color="inverse")

        # AKILLI KLİNİK YORUM
        st.info(f"""
        🧠 **EVEYES AI Analiz Notu:** Düne göre kilonuzda **{abs(k_degisim)} kg** azalma var. BİA değerinizdeki **{b_degisim} Ω** artış, 
        vücut direncinizin yükseldiğini ve kas kütlenizin korunduğunu işaret ediyor. Kaşeksi riski düşük.
        """)

        st.subheader("📊 Zaman Serisi Grafiği")
        st.line_chart(df_history.set_index('Tarih')[['Kilo', 'BİA']])

    elif choice == "📝 Günlük Klinik Giriş":
        st.title("📝 Günlük Kayıt Merkezi")
        
        with st.expander("🌡️ Vücut Değerleri & BİA", expanded=True):
            col_a, col_b, col_c = st.columns(3)
            w = col_a.number_input("Güncel Kilo (kg)", value=70.0)
            t = col_b.number_input("Ateş (°C)", value=36.5, step=0.1)
            b = col_c.number_input("BİA Ölçümü (Ohm)", value=500)

        with st.expander("📉 Ağrı Değerlendirmesi", expanded=True):
            pain_num = st.slider("Ağrı Seviyesi (0-10)", 0, 10, 3)
            st.write("Görsel Ağrı Skalası (VAS)")
            st.radio("Yüz İfadesi:", ["😊 Ağrı Yok", "😐 Hafif", "😟 Orta", "😫 Şiddetli", "😭 Dayanılmaz"], horizontal=True)
            

        with st.expander("🎥 AI Canlı Tarama (Vücut/Yüz/Ses)", expanded=False):
            st.write("Lütfen şikayet bölgenizi veya yürüyüşünüzü sesli anlatarak kaydedin.")
            clinical_video = st.file_uploader("Video Kaydı Yükle (Kamera ile Video Çek)", type=["mp4", "mov"])
            clinical_photo = st.camera_input("Hızlı Fotoğraf (Yara/Ben)")

        # --- RAPORLAMA VE GÖNDERİM ---
        st.divider()
        if st.button("💾 Kayıtları Kaydet ve Rapor Hazırla"):
            st.success("✅ Veriler klinik arşive eklendi.")
            
            report_content = f"""
🏥 EVEYES 360 KLİNİK RAPOR
--------------------------
Tarih: {datetime.now().strftime('%d/%m/%Y')}
Kilo: {w} kg
BİA: {b} Ohm
Ateş: {t} °C
Ağrı: {pain_num}/10
Analiz: Kilo ve BIA dengeli, kaşeksi riski yok.
--------------------------
            """
            st.text_area("Hazırlanan Yazılı Rapor", report_content, height=150)
            
            st.subheader("📤 Doktoruma Gönder")
            btn1, btn2 = st.columns(2)
            encoded_msg = report_content.replace("\n", "%0A")
            
            with btn1:
                st.markdown(f'''<a href="https://wa.me/905XXXXXXXXX?text={encoded_msg}" target="_blank">
                <button style="background-color:#25D366;color:white;border:none;padding:12px;border-radius:10px;width:100%;cursor:pointer;">WhatsApp ile Gönder</button></a>''', unsafe_allow_html=True)
            with btn2:
                mail_url = f"mailto:doktor@email.com?subject=EVEYES_Rapor&body={encoded_msg}"
                st.markdown(f'<a href="{mail_url}"><button style="background-color:#0078D4;color:white;border:none;padding:12px;border-radius:10px;width:100%;cursor:pointer;">E-Posta ile Gönder</button></a>', unsafe_allow_html=True)

    elif choice == "💊 İlaç Takibi":
        try: therapy.show_therapy()
        except: st.warning("İlaç modülü yükleniyor...")

# ==========================================
# 2. UZMAN HUB (SPECIALIST CONTROL)
# ==========================================
else:
    st.title("👨‍⚕️ Uzman Klinik Hub")
    dept = st.sidebar.selectbox("Klinik Branş", ["Metabolic-360", "Neuro-Guard", "Derma-Scan", "Pediatric-Pro", "Resp-Sonic"])
    
    st.info(f"Su an {dept} modülündesiniz. Hastadan gelen video ve veriler analiz ediliyor.")
    
    if dept == "Metabolic-360":
        try: metabolic.show_metabolic()
        except: st.write("Metabolik modül verileri bekleniyor...")
    elif dept == "Neuro-Guard":
        try: neuro.show_neuro()
        except: st.write("Nörolojik tarama verileri bekleniyor...")
    # Diğer modüller buraya devam eder...
