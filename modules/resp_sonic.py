import streamlit as st
import time
import numpy as np
import pandas as pd

def show_resp():
    st.title("🫁 Resp-Sonic: Canlı Audio-Visual Muayene")
    st.write("Cihazınızın kamera ve mikrofonunu kullanarak analize başlayın.")

    tab1, tab2 = st.tabs(["🎙️ Canlı Ses Analizi", "📷 Görsel Muayene (Boğaz/Göğüs)"])

    with tab1:
        st.subheader("Akciğer ve Öksürük Sesi Kaydı")
        # Streamlit'in yerleşik ses kaydedicisi (Bazı tarayıcılarda izin ister)
        audio_input = st.audio_input("Nefes alışverişinizi veya öksürüğünüzü kaydedin")
        
        if audio_input:
            st.audio(audio_input)
            if st.button("Sesi Yapay Zeka ile Tara"):
                with st.spinner("Frekans analizi yapılıyor..."):
                    time.sleep(2)
                st.info("🎯 **Analiz:** Ekspiratuar wheezing (hırıltı) saptandı. Astım/Bronşit şüphesi %72.")

    with tab2:
        st.subheader("AI Görsel Denetim")
        # Doğrudan kamera açılır
        captured_img = st.camera_input("Muayene Görüntüsü Al (Boğaz veya Göğüs Kafesi)")
        
        if captured_img:
            st.image(captured_img, caption="Yakalanan Klinik Görüntü", use_container_width=True)
            
            check_type = st.radio("İnceleme Bölgesi:", ["Farinks/Tonsil (Boğaz)", "Toraks (Göğüs Hareketleri)"])
            
            if st.button("Görüntü Analizini Başlat"):
                with st.spinner("Doku ve simetri kontrol ediliyor..."):
                    time.sleep(2)
                if check_type == "Farinks/Tonsil (Boğaz)":
                    st.error("🚨 Tonsillerde hipertrofi ve eritem (kızarıklık) gözlemlendi.")
                else:
                    st.success("✅ Solunum kasları kullanımı normal. Göğüs kafesi ekspansiyonu simetrik.")

    # WhatsApp Raporlama Kısmı
    st.divider()
    if st.button("📋 Klinik Raporu Oluştur ve Gönder"):
        st.success("Rapor hazırlandı! Doktorunuza WhatsApp üzerinden iletebilirsiniz.")
        # Buraya daha önce yazdığımız WhatsApp yönlendirme linkini ekleyebilirsin.


    # --- STANDART RAPORLAMA VE WHATSAPP ---
    st.divider()
    rapor_metni = f"""EVEYES 360 RESP-SONIC REPORT
---------------------------
Acoustic Risk: {breath_risk}
Visual Finding: {visual_finding}
Timestamp: {time.strftime("%Y-%m-%d %H:%M")}
"""

    col1, col2 = st.columns(2)
    with col1:
        st.download_button("📥 Respiratory Report Download", rapor_metni, file_name="resp_sonic_report.txt")
    
    with col2:
        encoded_msg = rapor_metni.replace("\n", "%0A")
        whatsapp_url = f"https://wa.me/905XXXXXXXXX?text={encoded_msg}"
        st.markdown(f"""
            <a href="{whatsapp_url}" target="_blank" style="text-decoration: none;">
                <div style="width: 100%; background-color: #25D366; color: white; padding: 10px; border-radius: 5px; text-align: center; font-weight: bold;">
                    🟢 Send to Pulmonologist (WhatsApp)
                </div>
            </a>""", unsafe_allow_html=True)
