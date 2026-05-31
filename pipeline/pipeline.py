"""
Módulo del Pipeline de Recomendación de Anime.

Este módulo orquesta el flujo completo del sistema de recomendación de anime.
Coordina la carga del vector store persistido y la inicialización del recomendador
para exponer una interfaz sencilla que permite generar recomendaciones a partir
de consultas en lenguaje natural.
"""

from src.vector_store import VectorStoreBuilder
from src.recommender import AnimeRecommender
from config.config import GROQ_API_KEY, MODEL_NAME
from utils.logger import get_logger
from utils.custom_exception import CustomException

logger = get_logger(__name__)


class AnimeRecommendationPipeline:
    """
    Pipeline principal para el sistema de recomendación de anime.

    Encapsula la inicialización del vector store y del recomendador,
    proporcionando un punto de entrada único para generar recomendaciones
    de anime basadas en consultas de usuario mediante RAG.

    Attributes:
        recommender (AnimeRecommender): Instancia del recomendador que combina
            el recuperador de documentos con el modelo de lenguaje.
    """

    def __init__(self, persist_dir: str = "chroma_db"):
        """
        Inicializa el pipeline de recomendación de anime.

        Carga el vector store desde el directorio de persistencia y configura
        el recomendador con el modelo y la API key definidos en la configuración.

        Args:
            persist_dir (str): Ruta al directorio donde se encuentra el vector
                store persistido (ChromaDB). Por defecto es 'chroma_db'.

        Raises:
            CustomException: Si ocurre un error al cargar el vector store o
                al inicializar el recomendador.
        """
        try:
            logger.info("Inicializando AnimeRecommendationPipeline...")

            # Construye el acceso al vector store ya persistido (csv_path vacío porque solo se carga)
            vector_build = VectorStoreBuilder(csv_path="", persist_dir=persist_dir)

            # Obtiene el recuperador a partir del vector store cargado
            retriever = vector_build.load_vector_store().as_retriever()

            # Inicializa el recomendador con el recuperador y las credenciales del modelo
            self.recommender = AnimeRecommender(retriever, api_key=GROQ_API_KEY, model_name=MODEL_NAME)
            logger.info("AnimeRecommendationPipeline inicializado correctamente.")
        except Exception as e:
            logger.error(f"Error al inicializar AnimeRecommendationPipeline: {e}")
            raise CustomException(f"Error al inicializar AnimeRecommendationPipeline: {e}")

    def recommend(self, query: str) -> str:
        """
        Genera una recomendación de anime a partir de una consulta de usuario.

        Delega la consulta al recomendador interno, que ejecuta el sistema RAG
        para recuperar documentos relevantes y generar una respuesta personalizada.

        Args:
            query (str): Descripción o pregunta del usuario sobre el tipo de anime
                que desea. Ejemplo: "Recomiéndame un anime de aventura con magia".

        Returns:
            str: Texto con la recomendación generada por el modelo de lenguaje.

        Raises:
            CustomException: Si ocurre un error durante la generación de la recomendación.
        """
        try:
            logger.info(f"Generando recomendación para la consulta: {query}")
            recomendation = self.recommender.get_recommendation(query)
            logger.info("Recomendación generada exitosamente.")
            return recomendation
        except Exception as e:
            logger.error(f"Error al generar la recomendación: {e}")
            raise CustomException(f"Error al generar la recomendación: {e}")