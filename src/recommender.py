"""
Módulo de Recomendador de Anime.

Este módulo proporciona la funcionalidad para generar recomendaciones de anime
utilizando un modelo de lenguaje (LLM) con capacidades de recuperación de documentos.
Implementa un sistema RAG (Retrieval-Augmented Generation) que utiliza LangChain
y el modelo Groq para procesar consultas de usuarios y devolver recomendaciones
personalizadas basadas en una base de datos de anime.
"""

from langchain_classic.chains import RetrievalQA
from langchain_groq import ChatGroq
from src.prompt_template import get_anime_prompt


class AnimeRecommender:
    """
    Clase para generar recomendaciones de anime utilizando RAG.
    
    Implementa un sistema de preguntas y respuestas (Q&A) que combina un modelo
    de lenguaje (LLM) con un recuperador de documentos. Utiliza el modelo Groq
    y un prompt especializado para generar recomendaciones de anime coherentes
    y relevantes basadas en consultas de usuarios.
    
    Attributes:
        llm (ChatGroq): Instancia del modelo de lenguaje Groq con temperatura 0
            para respuestas más determinísticas.
        prompt: Template de prompt especializado para recomendaciones de anime.
        qa_chain (RetrievalQA): Cadena RAG que combina recuperación y generación.
    """
    
    def __init__(self, retriever, api_key: str, model_name: str):
        """
        Inicializa el recomendador de anime.
        
        Configura el modelo de lenguaje, el prompt personalizado y la cadena de
        preguntas y respuestas que integra el recuperador de documentos.
        
        Args:
            retriever: Objeto recuperador que obtiene documentos relevantes de
                la base de datos de anime. Típicamente se trata de un vector store.
            api_key (str): Clave API para autenticarse con el servicio Groq.
            model_name (str): Nombre del modelo a utilizar (ej: 'llama-2-70b-chat').
        
        Returns:
            None
        """
        # Inicializa el modelo de lenguaje Groq con temperatura 0 para respuestas determinísticas
        self.llm = ChatGroq(api_key=api_key, model=model_name, temperature=0)
        
        # Carga el template de prompt especializado para recomendaciones de anime
        self.prompt = get_anime_prompt()
        
        # Configura la cadena RAG que combina recuperación de documentos y generación de texto
        # chain_type="stuff": concatena todos los documentos recuperados en el contexto
        # return_source_documents=True: rastrea qué documentos fueron usados para la respuesta
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt}
        )
        
    def get_recommendation(self, query: str):
        """
        Obtiene una recomendación de anime basada en una consulta de usuario.
        
        Procesa la consulta del usuario a través de la cadena RAG. El sistema
        retrieves documentos relevantes de la base de datos y utiliza el modelo
        de lenguaje para generar una recomendación personalizada.
        
        Args:
            query (str): Consulta o descripción del tipo de anime deseado.
                Ejemplo: "Quiero un anime de acción con un protagonista fuerte"
        
        Returns:
            str: Recomendación de anime generada por el modelo. Incluye sugerencias
                personalizadas basadas en la consulta y los documentos recuperados.
        
        Note:
            La cadena RAG también rastrea los documentos fuente utilizados,
            aunque solo se retorna el resultado final (el resumen de la recomendación).
        """
        # Ejecuta la cadena RAG con la consulta del usuario
        # La cadena recupera documentos relevantes y genera una respuesta
        result = self.qa_chain({"query": query})

        # Retorna solo el texto de la recomendación (sin los documentos fuente)
        return result['result'] 