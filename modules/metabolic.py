import streamlit as st
import pandas as pd

def show_metabolic():
    st.title("⚖️ Metabolic-360: Multi-Disciplinary Analysis")
    st.markdown("Kardiyoloji, Onkoloji ve Kadın Doğum için özelleşmiş ödem ve kas takibi.")

    # 1. Branş Seçimi (Kritik nokta)
    clinical_pathway = st.selectbox(
        "Klinik Odak Noktası / Clinical Pathway", 
        ["Genel Takip", "Kardiyoloji (Kalp Yetmezliği)", "Gynecology (Gebelikte Ödem)", "Onkoloji (Kaşeksi Takibi)"]
    )

    # 2. Veri Giriş Alanı
    with st.expander("📊 Hasta Verileri", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            weight = st.number_input("Güncel Kilo (kg)", value=70.0, step=0.1)
        with col2:
            bia = st.number_input("BİA Direnci (Ohm Ω)", value=500, step=1)
        with col3:
            last_weight = st.number_input("Önceki Kilo (kg)", value=69.0, step=0.1)

    # Hesaplamalar
    weight_diff = weight - last_weight
    
    st.divider()

    # 3. Branşa Özel Klinik Mantık
    if clinical_pathway == "Kardiyoloji (Kalp Yetmezliği)":
        st.subheader("🫀 Kardiyovasküler Ödem Analizi")
        if weight_diff >= 1.5: # 24 saatte 1.5kg+ artış kritiktir
            st.error("🚨 KRİTİK UYARI: Hızlı kilo artışı tespit edildi!")
            st.warning("Kalp yetmezliği alevlenmesi ve akciğer ödemi riski. Lütfen doktorunuza başvurun.")
        elif bia < 450:
            st.info("💡 BİA değeri düşük: Vücut sıvısında artış eğilimi var.")
        else:
            st.success("✅ Stabil: Kardiyak yük dengeli görünüyor.")

    elif clinical_pathway == "Gynecology (Gebelikte Ödem)":
        st.subheader("🤰 Gebelik Takibi & Preeklampsi Taraması")
        st.write("Gebelikte ani ödem, tansiyon ve böbrek fonksiyonları açısından izlenmelidir.")
        if weight_diff > 1.0 and bia < 480:
            st.error("🚨 PREEKLAMPSİ RİSKİ: Ani kilo artışı ve düşük BİA direnci.")
            st.info("Öneri: Tansiyonunuzu ölçün ve idrarda protein takibi için doktorunuzu bilgilendirin.")
        else:
            st.success("✅ Gebelik süreci ödem açısından stabil.")

    elif clinical_pathway == "Onkoloji (Kaşeksi Takibi)":
        st.subheader("🎗️ Onkolojik Kas Kütlesi Takibi")
        if weight < last_weight and bia > 550:
            st.error("🚨 KAŞEKSİ (KAS KAYBI) RİSKİ: Kilo düşerken direncin artması kas kaybına işarettir.")
            st.warning("Beslenme desteği ve onkolog görüşü önerilir.")
        else:
            st.success("✅ Beslenme ve kas kütlesi korunuyor.")

    else: # Genel Takip
        st.subheader("📋 Genel Metabolik Durum")
        if weight > last_weight and bia < 500:
            st.warning("Olası ödem başlangıcı. Tuz alımını kısıtlayın.")
        else:
            st.success("Parametreler normal sınırlar içerisinde.")

    # 4. Veri Görselleştirme (Geçmişe dönük simülasyon)
    st.divider()
    st.write("📈 **Trend Analizi (Son 5 Ölçüm)**")
    trend_data = pd.DataFrame({
        'Gün': [1, 2, 3, 4, 5],
        'Kilo': [last_weight-0.5, last_weight-0.2, last_weight, last_weight+0.2, weight],
        'BİA': [520, 515, 510, 505, bia]
    })
    
    c1, c2 = st.columns(2)
    with c1:
        st.line_chart(trend_data.set_index('Gün')['Kilo'])
        st.caption("Kilo Değişimi")
    with c2:
        st.line_chart(trend_data.set_index('Gün')['BİA'])
        st.caption("Direnç (BİA) Değişimi")
# 5. RAPORLAMA VE DOKTORA GÖNDERME
    st.divider()
    st.subheader("🏥 Klinik Raporlama")

    # Rapor metnini oluşturma
    rapor_metni = f"""
    EVEYES 360 KLİNİK RAPORU
    -----------------------
    Seçilen Branş: {clinical_pathway}
    Güncel Kilo: {weight} kg
    BİA Direnci: {bia} Ohm
    Kilo Değişimi: {weight_diff:+.1f} kg
    Durum: {"RİSK TESPİT EDİLDİ" if (weight_diff > 1 or bia < 480) else "STABİL"}
    """

    col_rep1, col_rep2 = st.columns(2)
    
    with col_rep1:
        if st.button("📄 PDF Rapor Oluştur"):
            st.info("PDF raporu hazırlanıyor ve indiriliyor...")
            # Not: Burada gerçek bir PDF kütüphanesi (ReportLab) kullanılabilir.
            st.download_button(
                label="📥 Raporu İndir (.txt)",
                data=rapor_metni,
                file_name="eveyes360_rapor.txt",
                mime="text/plain"
            )

    with col_rep2:
        # WhatsApp İçin Mesaj Hazırlama
        tel_no = "905XXXXXXXXX" # Buraya varsayılan dr numarası gelebilir
        encoded_msg = rapor_metni.replace("\n", "%0A")
        whatsapp_url = f"https://wa.me/{tel_no}?text={encoded_msg}"
        
        # Doğru kod: sadece unsafe_allow_html parametresini kullanıyoruz
        st.markdown(f"""
            <a href="{whatsapp_url}" target="_blank" style="text-decoration: none;">
                <div style="
                    width: 100%;
                    background-color: #25D366;
                    color: white;
                    padding: 10px;
                    border-radius: 5px;
                    text-align: center;
                    font-weight: bold;
                    cursor: pointer;">
                    🟢 WhatsApp ile Dr. Raporu Gönder
                </div>
            </a>
            """, unsafe_allow_html=True) # Hatalı parametre silindi
