import streamlit as st
from textblob import TextBlob
from googletrans import Translator
from streamlit_lottie import st_lottie
import json

# Función para cargar animaciones Lottie desde archivo
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# Cargar las animaciones
dancing_bear = load_lottiefile("Dancing Bear.json")
happy_dog = load_lottiefile("Happy Dog.json")
shiba_sad = load_lottiefile("Shiba Sad.json")

translator = Translator()
st.title('Uso de textblob')

st.subheader("Por favor escribe en el campo de texto la frase que deseas analizar")

with st.sidebar:
    st.subheader("Polaridad y Subjetividad")
    st.markdown("""
        **Polaridad:** Indica si el sentimiento expresado en el texto es positivo, negativo o neutral. 
        Su valor oscila entre -1 (muy negativo) y 1 (muy positivo), con 0 representando un sentimiento neutral.
        
        **Subjetividad:** Mide cuánto del contenido es subjetivo (opiniones, emociones, creencias) frente a objetivo
        (hechos). Va de 0 a 1, donde 0 es completamente objetivo y 1 es completamente subjetivo.
    """)

with st.expander('Analizar Polaridad y Subjetividad en un texto'):
    text1 = st.text_area('Escribe por favor: ')
    if text1:
        translation = translator.translate(text1, src="es", dest="en")
        trans_text = translation.text
        blob = TextBlob(trans_text)

        st.write('Polarity:', round(blob.sentiment.polarity, 2))
        st.write('Subjectivity:', round(blob.sentiment.subjectivity, 2))
        x = round(blob.sentiment.polarity, 2)

        # Mostrar mensaje y animación según resultado
        if x >= 0.5:
            st.success('Es un sentimiento Positivo 😊')
            st_lottie(dancing_bear, height=250, key="positive")
        elif x <= -0.5:
            st.error('Es un sentimiento Negativo 😔')
            st_lottie(shiba_sad, height=250, key="negative")
        else:
            st.info('Es un sentimiento Neutral 😐')
            st_lottie(happy_dog, height=250, key="neutral")

with st.expander('Corrección en inglés'):
    text2 = st.text_area('Escribe por favor: ', key='4')
    if text2:
        blob2 = TextBlob(text2)
        st.write(blob2.correct())
