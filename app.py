import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="BMI Hesaplayıcı",
    layout="centered",
    initial_sidebar_state="auto"
)

# Stil
st.markdown(
    """
    <style>
    .main {
        background-color: #f4f6f9;
        font-family: 'Segoe UI', sans-serif;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 0.5em 2em;
        font-size: 1.1em;
    }
    .stNumberInput>div>div>input {
        font-size: 1.1em;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("💪 Vücut Kitle İndeksi (BMI) Hesaplayıcı")

# Girişler
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

        if bmi < 18.5:
            st.info("💡 Zayıf kategorisindesiniz.")
        elif 18.5 <= bmi < 25:
            st.success("✅ Normal kilodasınız.")
        elif 25 <= bmi < 30:
            st.warning("⚠️ Fazla kilolusunuz.")
        else:
            st.error("🚨 Obezite sınırındasınız.")

        ideal_kilo = ideal_kilo_hesapla(boy, cinsiyet)
        st.markdown(f"🎯 **Boyunuza göre ideal kilo:** `{ideal_kilo} kg`")

        # Akıllı öneri
        st.markdown("### 🧠 Akıllı Yorum")
        yorum = akilli_yorum(bmi, boy, kilo)
        st.info(yorum)

        # Paylaşılabilir metin
        st.markdown("### 📤 Sonucunuzu paylaşın")
        paylasilabilir = f"Benim BMI değerim {bmi:.1f} ve {boy}cm boy / {kilo}kg ile {ideal_kilo}kg ideal kilonun {abs(kilo - ideal_kilo):.1f}kg kadar dışındayım."
        st.code(paylasilabilir, language="markdown")
        st.caption("Bu metni kopyalayıp arkadaşlarınla paylaşabilirsin!")

        # Veriyi CSV'ye yaz
        tarih = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        yeni_kayit = pd.DataFrame([[tarih, boy, kilo, bmi]], columns=["Tarih", "Boy", "Kilo", "BMI"])
        try:
            onceki = pd.read_csv("bmi_kayitlari.csv")
            guncel = pd.concat([onceki, yeni_kayit], ignore_index=True)
        except FileNotFoundError:
            guncel = yeni_kayit
        guncel.to_csv("bmi_kayitlari.csv", index=False)

        # Grafik
        st.markdown("### 📈 BMI Geçmişiniz")
        st.line_chart(guncel[["BMI"]])
    else:
        st.error("Lütfen geçerli bir boy girin.")
