import streamlit as st
from textblob import TextBlob
from googletrans import Translator
from streamlit_lottie import st_lottie
import json
import matplotlib.pyplot as plt

# =============================
# 🎨 Configuración visual
# =============================

st.set_page_config(page_title="Analizador de Sentimientos", layout="centered")

# Tema oscuro personalizado
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #0E1117;
    color: #FFFFFF;
}
[data-testid="stSidebar"] {
    background-color: #1E1E1E;
}
[data-testid="stMarkdownContainer"] h1, h2, h3, h4 {
    color: #FFFFFF !important;
}
.stTextInput, .stTextArea {
    background-color: #262730;
    color: #FFFFFF;
}
</style>
""", unsafe_allow_html=True)

# =============================
# 🧸 Cargar animaciones Lottie
# =============================

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

dancing_bear = load_lottiefile("Dancing Bear.json")
happy_dog = load_lottiefile("Happy Dog.json")
shiba_sad = load_lottiefile("Shiba Sad.json")

# =============================
# 🔍 Análisis de sentimiento
# =============================

translator = Translator()
st.title('🐻 Analizador de Sentimientos con TextBlob')

st.subheader("Escribe una frase para analizar su polaridad y subjetividad")

with st.sidebar:
    st.subheader("📘 Conceptos clave")
    st.markdown("""
        **Polaridad:**  
        Indica si el sentimiento expresado en el texto es positivo, negativo o neutral.  
        Su valor oscila entre -1 (muy negativo) y 1 (muy positivo).  

        **Subjetividad:**  
        Mide cuánto del contenido es subjetivo (opiniones, emociones, creencias) frente a objetivo (hechos).  
        Va de 0 a 1, donde 0 es completamente objetivo y 1 es completamente subjetivo.
    """)

with st.expander('🔎 Analizar Polaridad y Subjetividad en un texto'):
    text1 = st.text_area('Escribe aquí el texto a analizar:')

    if text1:
        # Traducción automática
        translation = translator.translate(text1, src="es", dest="en")
        trans_text = translation.text
        blob = TextBlob(trans_text)

        # Resultados numéricos
        polarity = round(blob.sentiment.polarity, 2)
        subjectivity = round(blob.sentiment.subjectivity, 2)

        st.write(f"**Polaridad:** {polarity}")
        st.write(f"**Subjetividad:** {subjectivity}")

        # =============================
        # 📊 Visualización de polaridad
        # =============================
        st.write("### Visualización del sentimiento")
        fig, ax = plt.subplots()
        ax.barh(['Sentimiento'], [polarity],
                color='green' if polarity > 0 else 'red' if polarity < 0 else 'gray')
        ax.set_xlim(-1, 1)
        ax.set_xlabel('Escala de sentimiento (-1 a 1)')
        ax.set_facecolor("#0E1117")
        fig.patch.set_alpha(0)
        st.pyplot(fig)

        # =============================
        # 😊 Mostrar animaciones y mensajes
        # =============================
        if polarity >= 0.5:
            st.success('Es un sentimiento **Positivo** 😊')
            st_lottie(dancing_bear, height=250, key="positive")
        elif polarity <= -0.5:
            st.error('Es un sentimiento **Negativo** 😔')
            st_lottie(shiba_sad, height=250, key="negative")
        else:
            st.info('Es un sentimiento **Neutral** 😐')
            st_lottie(happy_dog, height=250, key="neutral")

with st.expander('📝 Corrección en inglés'):
    text2 = st.text_area('Escribe en inglés para corregir:', key='4')
    if text2:
        blob2 = TextBlob(text2)
        st.write("**Texto corregido:**")
        st.write(blob2.correct())
