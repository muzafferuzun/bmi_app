import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_option_menu import option_menu

# Sayfa ayarları
st.set_page_config(page_title="BMI Hesaplayıcı", layout="centered")

# Başlık ve kullanıcı adı girişi
st.sidebar.title("⚙️ Ayarlar")
kullanici_adi = st.sidebar.text_input("Adınız", value="Muzo")
tema = st.sidebar.radio("Tema", ["Açık", "Karanlık"])

# Tema stili
if tema == "Karanlık":
    st.markdown(
        "<style>body{background-color: #0e1117; color: white;} .stButton>button{background-color: #5c6bc0; color: white;}</style>",
        unsafe_allow_html=True
    )
else:
    st.markdown(
        "<style>.stButton>button{background-color: #4CAF50; color: white;}</style>",
        unsafe_allow_html=True
    )

# Menü
secim = option_menu(
    menu_title=None,
    options=["🏠 Ana Sayfa", "📈 Geçmiş", "ℹ️ Hakkında"],
    icons=["house", "bar-chart-line", "info-circle"],
    orientation="horizontal"
)

if secim == "🏠 Ana Sayfa":
    st.title(f"💪 Merhaba {kullanici_adi}, BMI Hesaplayıcıya Hoş Geldin!")

    boy = st.number_input("📏 Boyunuzu girin (cm)", min_value=100, max_value=250, step=1)
    kilo = st.number_input("⚖️ Kilonuzu girin (kg)", min_value=30, max_value=200, step=1)
    cinsiyet = st.radio("🚻 Cinsiyetiniz", ("Erkek", "Kadın"), horizontal=True)

    def ideal_kilo_hesapla(boy, cinsiyet):
        if cinsiyet == "Erkek":
            return round(50 + 0.91 * (boy - 152.4), 1)
        else:
            return round(45.5 + 0.91 * (boy - 152.4), 1)

    def akilli_yorum(bmi, boy, kilo):
        if bmi < 18.5:
            return f"Boyunuz {boy} cm ve kilonuz {kilo} kg. Bu, BMI değerinizin {bmi:.1f} olduğunu gösteriyor. Bu değer zayıf kategorisine giriyor. Daha dengeli ve yeterli beslenerek sağlıklı kilonuza ulaşabilirsiniz."
        elif 18.5 <= bmi < 25:
            return f"Tebrikler! Boyunuz {boy} cm ve kilonuz {kilo} kg ile BMI değeriniz {bmi:.1f}. Bu değer normal aralıktadır. Bu formu korumak için dengeli beslenmeye ve düzenli aktiviteye devam edin."
        elif 25 <= bmi < 30:
            return f"Boyunuz {boy} cm ve kilonuz {kilo} kg. BMI değeriniz {bmi:.1f}, yani fazla kilolu kategorisindesiniz. Haftalık yürüyüş ve karbonhidrat azaltımı ile ideal kiloya ulaşmanız mümkündür."
        else:
            return f"Boyunuz {boy} cm ve kilonuz {kilo} kg. BMI değeriniz {bmi:.1f}. Bu, obezite kategorisine giriyor. Uzman eşliğinde diyet ve egzersiz planı uygulamanız önerilir."

    if st.button("📊 Hesapla"):
        if boy > 0:
            boy_metre = boy / 100
            bmi = kilo / (boy_metre ** 2)

            st.success(f"📌 Vücut Kitle İndeksiniz: **{bmi:.2f}**")

            ideal_kilo = ideal_kilo_hesapla(boy, cinsiyet)
            st.markdown(f"🎯 **İdeal Kilo:** `{ideal_kilo} kg`")

            st.markdown("### 🧠 Akıllı Yorum")
            yorum = akilli_yorum(bmi, boy, kilo)
            st.info(yorum)

            st.markdown("### 📤 Paylaş")
            paylasilabilir = f"Benim BMI değerim {bmi:.1f} ({boy}cm/{kilo}kg), ideal kiloya {abs(kilo - ideal_kilo):.1f}kg kaldı."
            st.code(paylasilabilir)

            tarih = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            yeni_kayit = pd.DataFrame([[tarih, boy, kilo, bmi]], columns=["Tarih", "Boy", "Kilo", "BMI"])
            try:
                onceki = pd.read_csv("bmi_kayitlari.csv")
                guncel = pd.concat([onceki, yeni_kayit], ignore_index=True)
            except FileNotFoundError:
                guncel = yeni_kayit
            guncel.to_csv("bmi_kayitlari.csv", index=False)

elif secim == "📈 Geçmiş":
    st.title("📈 BMI Geçmişi")
    try:
        veri = pd.read_csv("bmi_kayitlari.csv")
        st.line_chart(veri["BMI"])
        st.dataframe(veri.tail(10))
    except FileNotFoundError:
        st.warning("Henüz kayıt bulunamadı.")

elif secim == "ℹ️ Hakkında":
    st.title("ℹ️ Uygulama Hakkında")
    st.markdown("""
    Bu uygulama, vücut kitle indeksinizi hesaplayarak sağlığınız hakkında bilgi verir.

    - 📏 Boy ve kilo bilgilerinizi girin
    - 🧠 Akıllı yorumları okuyun
    - 📈 Geçmiş verilerinizi takip edin
    - 🌙 Tema seçimiyle görünümü kişiselleştirin

    Hazırlayan: **Muzaffer Uzun**
    """)
