import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def show_history():
    st.title("📈 Sağlık Takip ve Analiz Sayfası")
    
    # Simüle edilmiş geçmiş veri (Gerçek uygulamada veritabanından çekilecek)
    data = {
        'Tarih': [datetime.now() - timedelta(days=1), datetime.now()],
        'Kilo': [71.0, 70.0],
        'BİA': [490, 500],
        'Ateş': [36.8, 36.5],
        'Ağrı': [5, 3]
    }
    df = pd.DataFrame(data)

    # --- KARŞILAŞTIRMALI ANALİZ (Yorum Yapmaya Müsait) ---
    st.subheader("🔄 Dün vs Bugün Karşılaştırması")
    col1, col2, col3 = st.columns(3)
    
    # Kilo Değişimi
    kilo_diff = df['Kilo'].iloc[-1] - df['Kilo'].iloc[-2]
    col1.metric("Kilo Değişimi", f"{df['Kilo'].iloc[-1]} kg", f"{kilo_diff:.1f} kg", delta_color="inverse")
    
    # BİA Değişimi
    bia_diff = df['BİA'].iloc[-1] - df['BİA'].iloc[-2]
    col2.metric("BİA (Kas/Su) Değişimi", f"{df['BİA'].iloc[-1]} Ohm", f"{bia_diff:+d}")
    
    # Ağrı Değişimi
    pain_diff = df['Ağrı'].iloc[-1] - df['Ağrı'].iloc[-2]
    col3.metric("Ağrı Seviyesi", f"{df['Ağrı'].iloc[-1]}/10", f"{pain_diff:+d}", delta_color="inverse")

    st.info(f"💡 **Klinik Yorum:** Son 24 saatte kilonuzda {abs(kilo_diff)} kg azalma görülürken, BİA değerinizdeki artış kas kütlesinin korunduğunu işaret ediyor.")

    # --- GRAFİKSEL GÖSTERİM ---
    st.subheader("📊 Zaman Serisi Grafikleri")
    st.line_chart(df.set_index('Tarih')[['Kilo', 'BİA']])
    # app.py içindeki "SUBMIT TO CLINICAL HUB" butonunun altı için:
if st.button("💾 Günlük Kayıtları Kaydet ve Rapor Hazırla"):
    st.success("Veriler kaydedildi. Raporunuz analiz için hazır.")
    
    # Rapor Taslağı
    report_content = f"""
    🏥 EVEYES 360 KLİNİK RAPOR
    --------------------------
    Tarih: {datetime.now().strftime('%d/%m/%Y')}
    Kilo: {weight} kg (Değişim: -1.0kg)
    BİA: {bia} Ohm
    Ateş: {temp} °C
    Ağrı: {pain_level}/10
    Klinik Not: Kaşeksi riski düşük, metabolik uyum iyi.
    --------------------------
    """
    
    st.text_area("Hazırlanan Rapor Özeti", report_content, height=150)
    
    st.subheader("📤 Doktoruna Gönder")
    c1, c2 = st.columns(2)
    
    with c1:
        # WhatsApp Gönderimi
        encoded_msg = report_content.replace("\n", "%0A")
        st.markdown(f'''
            <a href="https://wa.me/905XXXXXXXXX?text={encoded_msg}" target="_blank">
                <button style="background-color:#25D366; color:white; border:none; padding:10px 20px; border-radius:5px; width:100%;">
                    WhatsApp ile Gönder
                </button>
            </a>''', unsafe_allow_html=True)
            
    with c2:
        # E-Posta Gönderimi
        subject = "EVEYES 360 Gunluk Klinik Rapor"
        mail_link = f"mailto:doktor@email.com?subject={subject}&body={encoded_msg}"
        st.markdown(f'<a href="{mail_link}"><button style="background-color:#0078D4; color:white; border:none; padding:10px 20px; border-radius:5px; width:100%;">E-Posta ile Gönder</button></a>', unsafe_allow_html=True)

