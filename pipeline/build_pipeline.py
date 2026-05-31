"""
Módulo de construcción del pipeline de recomendación de anime.

Este script es el punto de entrada para construir el vector store que alimenta
el sistema de recomendación. Realiza dos pasos principales:
  1. Carga y procesa los datos de anime desde archivos CSV.
  2. Genera y persiste el vector store en ChromaDB usando embeddings de HuggingFace.

Debe ejecutarse una única vez (o cuando los datos cambien) antes de usar el
pipeline de recomendación. El vector store generado es reutilizado por
AnimeRecommendationPipeline en tiempo de inferencia.

Uso:
    python pipeline/build_pipeline.py
"""

from src.data_loader import AnimeDataLoader
from src.vector_store import VectorStoreBuilder
from dotenv import load_dotenv
from utils.logger import get_logger
from utils.custom_exception import CustomException


load_dotenv()
logger = get_logger(__name__)


def main():
    """
    Ejecuta el pipeline de construcción del vector store de anime.

    Orquesta la carga de datos desde los CSV originales, su procesamiento
    y la creación del vector store persistido en disco. Este vector store
    será utilizado posteriormente por el pipeline de recomendación.

    Raises:
        CustomException: Si ocurre un error durante la carga de datos
            o la construcción del vector store.
    """
    try:
        logger.info("Iniciando el pipeline de construcción de recomendación de anime...")

        # Carga y procesa los datos de anime desde los archivos CSV
        # Utiliza el CSV disponible con sinopsis de anime
        loader = AnimeDataLoader("data/anime_with_synopsis.csv", "data/anime_processed.csv")
        processed_csv = loader.load_data_process()

        logger.info("Datos cargados y procesados correctamente.")

        # Construye el vector store a partir de los datos procesados y lo persiste en disco
        vector_builder = VectorStoreBuilder(processed_csv)
        vector_builder.build_and_save_vector_store()

        logger.info("Pipeline de construcción completado exitosamente.")

    except Exception as e:
        logger.error(f"Error en el pipeline de construcción: {e}")
        raise CustomException(f"Error al ejecutar el pipeline de construcción: {e}")


if __name__ == "__main__":
    main()