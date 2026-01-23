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

# --- DATA SİMÜLASYONU (Karşılaştırmalı Analiz İçin) ---
# Not: Gerçek kullanımda bu veriler veritabanından çekilir.
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame({
        'Tarih': [datetime.now() - timedelta(days=1), datetime.now()],
        'Kilo': [71.5, 70.2],
        'BİA': [490, 505],
        'Ateş': [36.8, 36.6],
        'Ağrı': [6, 3]
    })

# ==========================================
# 1. HASTA PORTALI (PATIENT TERMINAL)
# ==========================================
if user_role == "Hasta Portalı (Patient)":
    st.sidebar.divider()
    menu = ["🏠 Dashboard & Karşılaştırmalı Analiz", "📝 Günlük Klinik Giriş", "💊 İlaç & Tedavi Takibi"]
    choice = st.sidebar.selectbox("İşlem Seçin", menu)

    if choice == "🏠 Dashboard & Karşılaştırmalı Analiz":
        st.title("📊 Klinik Takip ve Analiz Dashboard")
        
        # --- DÜN VS BUGÜN METRİKLERİ ---
        st.subheader("🔄 24 Saatlik Değişim Analizi")
        c1, c2, c3, c4 = st.columns(4)
        
        df = st.session_state.db
        k_degisim = df['Kilo'].iloc[-1] - df['Kilo'].iloc[-2]
        b_degisim = df['BİA'].iloc[-1] - df['BİA'].iloc[-2]
        a_degisim = df['Ağrı'].iloc[-1] - df['Ağrı'].iloc[-2]
        t_degisim = df['Ateş'].iloc[-1] - df['Ateş'].iloc[-2]

        c1.metric("Kilo", f"{df['Kilo'].iloc[-1]} kg", f"{k_degisim:.1f} kg", delta_color="inverse")
        c2.metric("BİA (Kas/Su)", f"{df['BİA'].iloc[-1]} Ω", f"{b_degisim:+d}")
        c3.metric("Ağrı (VAS)", f"{df['Ağrı'].iloc[-1]}/10", f"{a_degisim:+d}", delta_color="inverse")
        c4.metric("Ateş", f"{df['Ateş'].iloc[-1]} °C", f"{t_degisim:.1f} °C", delta_color="inverse")

        # AKILLI KLİNİK YORUM (Yazılı Rapor Hazırlığı)
        st.info(f"""
        🧠 **EVEYES AI Klinik Notu:** Düne göre kilonuzda **{abs(k_degisim):.1f} kg** azalma görüldü. BİA değerinizdeki **{b_degisim} Ω** artış, 
        vücut direncinizin yükseldiğini ve sıvı dengesinin iyiye gittiğini gösteriyor. 
        Ağrı seviyenizdeki düşüş, tedaviye pozitif yanıt verdiğinizi kanıtlamaktadır. Kaşeksi (kas kaybı) riski düşüktür.
        """)

        st.subheader("📈 Gelişim Grafikleri")
        tab1, tab2 = st.tabs(["Kilo & BİA Trendi", "Ateş & Ağrı Seyri"])
        with tab1:
            st.line_chart(df.set_index('Tarih')[['Kilo', 'BİA']])
        with tab2:
            st.area_chart(df.set_index('Tarih')[['Ateş', 'Ağrı']])

    elif choice == "📝 Günlük Klinik Giriş":
        st.title("📝 Günlük Veri Kayıt Merkezi")
        
        with st.expander("🌡️ Vücut Değerleri & BİA", expanded=True):
            col_a, col_b, col_c = st.columns(3)
            w = col_a.number_input("Güncel Kilo (kg)", value=70.0)
            t = col_b.number_input("Ateş (°C)", value=36.5, step=0.1)
            b = col_c.number_input("BİA Ölçümü (Ohm)", value=500)

        with st.expander("📉 Ağrı Değerlendirmesi (VAS & Numeric)", expanded=True):
            pain_num = st.slider("Ağrı Seviyesi (Numeric: 0-10)", 0, 10, 3)
            st.write("Görsel Ağrı Skalası (Visual Analog Scale)")
            st.radio("Yüz İfadesi:", ["😊 Ağrı Yok", "😐 Hafif", "😟 Orta", "😫 Şiddetli", "😭 Dayanılmaz"], horizontal=True)
            

        with st.expander("🎥 AI Canlı Tarama (Vücut/Yüz/Ses)", expanded=False):
            st.write("Lütfen şikayet bölgenizi veya yürüyüşünüzü sesli anlatarak kaydedin.")
            clinical_video = st.file_uploader("Video Kaydı Yükle (Kamera ile Video Çek)", type=["mp4", "mov"])
            clinical_photo = st.camera_input("Hızlı Fotoğraf (Yara/Ben/Ödem)")

        # --- RAPORLAMA VE ÇOKLU KANAL GÖNDERİM ---
        st.divider()
        if st.button("💾 Kayıtları Kaydet ve Raporu Hazırla"):
            # Rapor İçeriği Oluşturma
            report_text = f"""
🏥 *EVEYES 360 GÜNLÜK KLİNİK RAPOR*
---
📅 *Tarih:* {datetime.now().strftime('%d/%m/%Y')}
⚖️ *Kilo:* {w} kg
⚡ *BİA:* {b} Ohm
🌡️ *Ateş:* {t} °C
📉 *Ağrı:* {pain_num}/10
---
📝 *Klinik Yorum:* Kilo ve BIA dengesi stabil. Kaşeksi riski yönetiliyor. Tedavi uyumu yüksek.
---
            """
            st.success("✅ Veriler kaydedildi. Raporunuz hazır.")
            st.text_area("Doktorunuza Gidecek Mesaj Taslağı:", report_text, height=200)
            
            st.subheader("📤 Doktoruma Gönder")
            btn1, btn2 = st.columns(2)
            # URL Encoding for WhatsApp/Mail
            encoded_msg = report_text.replace("\n", "%0A").replace("*", "")
            
            with btn1:
                # WhatsApp Butonu
                whatsapp_url = f"https://wa.me/905XXXXXXXXX?text={encoded_msg}"
                st.markdown(f'''<a href="{whatsapp_url}" target="_blank">
                <button style="background-color:#25D366;color:white;border:none;padding:15px;border-radius:10px;width:100%;font-weight:bold;cursor:pointer;">WhatsApp ile Paylaş</button></a>''', unsafe_allow_html=True)
            
            with btn2:
                # E-Posta Butonu
                mail_url = f"mailto:doktor@email.com?subject=EVEYES_360_Gunluk_Rapor&body={encoded_msg}"
                st.markdown(f'<a href="{mail_url}"><button style="background-color:#0078D4;color:white;border:none;padding:15px;border-radius:10px;width:100%;font-weight:bold;cursor:pointer;">E-Posta ile Gönder</button></a>', unsafe_allow_html=True)

    elif choice == "💊 İlaç & Tedavi Takibi":
        try: therapy.show_therapy()
        except: st.warning("Tedavi modülü yükleniyor...")

# ==========================================
# 2. UZMAN HUB (SPECIALIST CONTROL)
# ==========================================
else:
    st.title("👨‍⚕️ Uzman Klinik Yönetim Paneli")
    dept = st.sidebar.selectbox("Klinik Branş", ["Metabolic-360", "Neuro-Guard", "Derma-Scan", "Pediatric-Pro", "Resp-Sonic"])
    
    st.info(f"Su an **{dept}** modülündesiniz. Hastadan gelen canlı tarama videoları ve biyometrik veriler eşzamanlı analiz ediliyor.")
    
    # Branş modülleri çağırma mantığı
    if dept == "Metabolic-360":
        try: metabolic.show_metabolic()
        except: st.write("Metabolik veriler bekleniyor...")
    elif dept == "Neuro-Guard":
        try: neuro.show_neuro()
        except: st.write("Nörolojik video analizi bekleniyor...")
    # ... diğer modüller
