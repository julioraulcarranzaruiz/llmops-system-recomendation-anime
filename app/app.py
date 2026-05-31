"""
Interfaz web del sistema de recomendación de anime.

Este módulo implementa la interfaz de usuario con Streamlit para el sistema
de recomendación de anime. Permite al usuario ingresar sus preferencias en
lenguaje natural y obtener recomendaciones personalizadas generadas por el
pipeline RAG (Retrieval-Augmented Generation).

Uso:
    streamlit run app/app.py
"""

import streamlit as st
from pipeline.pipeline import AnimeRecommendationPipeline
from dotenv import load_dotenv


# Configuración de la página: título, ícono y diseño en modo amplio
st.set_page_config(page_title="Anime Recommender", page_icon="🎬", layout="wide")

# Carga las variables de entorno definidas en el archivo .env (API keys, etc.)
load_dotenv()


@st.cache_resource
def init_pipeline():
    """
    Inicializa el pipeline de recomendación de anime una sola vez.
    
    El decorador @st.cache_resource garantiza que el pipeline se instancie
    únicamente en el primer arranque de la aplicación, reutilizándolo en
    interacciones posteriores para evitar cargar el vector store repetidamente.
    
    Returns:
        AnimeRecommendationPipeline: Instancia del pipeline lista para generar
            recomendaciones.
    """
    return AnimeRecommendationPipeline()


# Inicializa el pipeline (se carga desde caché en recargas posteriores)
pipeline = init_pipeline()

# Título principal de la interfaz
st.title("🎬 Sistema de Recomendación de Anime")

# Campo de texto donde el usuario ingresa sus preferencias en lenguaje natural
query = st.text_input("Ingresa tus preferencias de anime (ej: 'Me gustan los anime de acción y fantasía con personajes fuertes'):")

if query:
    # Muestra un spinner mientras se genera la recomendación
    with st.spinner("Generando recomendaciones..."):
        try:
            recommendation = pipeline.recommend(query)
            st.subheader("Anime Recomendado:")
            st.write(recommendation)
        except Exception as e:
            st.error(f"Error al generar las recomendaciones: {e}")
