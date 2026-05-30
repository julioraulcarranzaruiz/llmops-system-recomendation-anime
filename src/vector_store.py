"""
Módulo de construcción y gestión del vector store de ChromaDB.

Proporciona funcionalidad para crear embeddings de documentos de anime,
construir un vector store persistido usando ChromaDB y embeddings de HuggingFace,
y recuperar el vector store para su uso en consultas semánticas.
"""

import os

from langchain_text_splitters import CharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_huggingface import HuggingFaceEmbeddings


from dotenv import load_dotenv
load_dotenv()

HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")


class VectorStoreBuilder:
    """
    Constructor del vector store de ChromaDB para búsqueda semántica.
    
    Encapsula la lógica para:
    - Cargar datos de anime desde CSV.
    - Dividir documentos en fragmentos manejables.
    - Generar embeddings usando el modelo all-MiniLM-L6-v2 de HuggingFace.
    - Crear y persistir un vector store en ChromaDB.
    - Recuperar el vector store para búsquedas posteriores.
    
    Attributes:
        csv_path (str): Ruta al archivo CSV procesado con datos de anime.
        persist_dir (str): Directorio donde se persiste el vector store.
        embeddings (HuggingFaceEmbeddings): Generador de embeddings usando HuggingFace.
    """
    
    def __init__(self, csv_path: str, persist_dir: str = "chroma_db"):
        """
        Inicializa el constructor del vector store.
        
        Args:
            csv_path (str): Ruta al archivo CSV que contiene los datos procesados de anime.
                Debe estar en formato compatible con CSVLoader de LangChain.
            persist_dir (str): Directorio donde se almacenará el vector store persistido.
                Por defecto es 'chroma_db'.
        """
        self.csv_path = csv_path
        self.persist_dir = persist_dir
        # Inicializa el modelo de embeddings (all-MiniLM-L6-v2: 384 dimensiones, rápido y eficiente)
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    def build_and_save_vector_store(self):
        """
        Construye el vector store a partir del CSV y lo persiste en disco.
        
        Realiza los siguientes pasos:
        1. Carga los datos del CSV especificado.
        2. Divide los documentos en fragmentos (chunks) de 1000 caracteres con 200 de solapamiento.
        3. Genera embeddings para cada fragmento usando HuggingFace.
        4. Crea y persiste el vector store en ChromaDB.
        
        Note:
            En ChromaDB v0.4+, la persistencia es automática cuando se especifica
            persist_directory. El método persist() fue deprecado.
        
        Raises:
            FileNotFoundError: Si el archivo CSV no existe.
            ValueError: Si el CSV está vacío o mal formado.
        """
        # Carga el CSV y convierte las filas en documentos LangChain
        loader = CSVLoader(
            file_path=self.csv_path,
            encoding="utf-8",
            metadata_columns=[])
        
        data = loader.load()

        # Divide los documentos en fragmentos más pequeños para embedding
        # chunk_size=1000: cada fragmento tiene ~1000 caracteres
        # chunk_overlap=200: solapamiento de 200 caracteres para mantener contexto
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(data)

        # Crea el vector store con ChromaDB
        # Los embeddings se generan automáticamente para cada fragmento
        # persist_directory especifica donde guardar los datos
        db = Chroma.from_documents(
            texts,
            self.embeddings,
            persist_directory=self.persist_dir
        )

        # Nota: persist() fue eliminado en ChromaDB v0.4+
        # ChromaDB persiste automáticamente cuando se especifica persist_directory

    def load_vector_store(self):
        """
        Carga el vector store ya construido desde el directorio de persistencia.
        
        Recupera un vector store previamente construido y persistido en disco.
        Este método se utiliza durante la inferencia para consultas semánticas.
        
        Returns:
            Chroma: Instancia del vector store cargado lista para consultas.
        
        Raises:
            ValueError: Si el directorio de persistencia no existe o está vacío.
        """
        return Chroma(
            persist_directory=self.persist_dir,
            embedding_function=self.embeddings
        )

