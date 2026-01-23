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
