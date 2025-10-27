import streamlit as st
import random

# --- Base de Datos de Preguntas (un simple diccionario de Python) ---
# En una app real, esto podría venir de un archivo CSV, JSON o una base de datos.
BANCO_DE_PREGUNTAS = {
    "Ciencias": [
        {"pregunta": "¿Cuál es el planeta más grande del sistema solar?", "respuesta": "Júpiter"},
        {"pregunta": "¿Qué gas respiran las plantas?", "respuesta": "Dióxido de carbono"}
    ],
    "Historia": [
        {"pregunta": "¿En qué año llegó Colón a América?", "respuesta": "1492"},
        {"pregunta": "¿Quién fue el primer presidente de Estados Unidos?", "respuesta": "George Washington"}
    ],
    "Geografía": [
        {"pregunta": "¿Cuál es la capital de Japón?", "respuesta": "Tokio"},
        {"pregunta": "¿Qué río es el más largo del mundo?", "respuesta": "Amazonas"}
    ]
}

# --- Interfaz de la Aplicación Web ---
st.title("🎓 Banco de Preguntas Básico")

# Selector de categoría
categoria = st.selectbox("Elige una categoría:", list(BANCO_DE_PREGUNTAS.keys()))

if st.button("Dame una pregunta aleatoria"):
    preguntas_categoria = BANCO_DE_PREGUNTAS[categoria]
    pregunta_elegida = random.choice(preguntas_categoria)
    
    st.subheader("Pregunta:")
    st.write(pregunta_elegida["pregunta"])
    
    # Usamos un "expander" para ocultar la respuesta inicialmente
    with st.expander("Ver Respuesta"):
        st.write(pregunta_elegida["respuesta"])
