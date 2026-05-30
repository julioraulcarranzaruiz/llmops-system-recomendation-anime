from langchain_classic.prompts import PromptTemplate

def get_anime_prompt():
    """
    Crea y retorna el prompt especializado para el recomendador de anime.

    Construye un PromptTemplate con instrucciones detalladas para generar
    recomendaciones de anime estructuradas. Compatible con RetrievalQA
    de langchain_classic usando las variables {context} y {question}.

    Returns:
        PromptTemplate: Template listo para usar en la cadena RetrievalQA.
    """
    template = """
Eres un experto recomendador de anime. Tu trabajo es ayudar a los usuarios a encontrar el anime perfecto según sus preferencias.

Utilizando el siguiente contexto, proporciona una respuesta detallada y atractiva a la pregunta del usuario.

Para cada consulta, sugiere exactamente tres títulos de anime. Para cada recomendación incluye:
1. El título del anime.
2. Un resumen breve de la trama (2-3 oraciones).
3. Una explicación clara de por qué este anime coincide con las preferencias del usuario.

Presenta tus recomendaciones en formato de lista numerada para facilitar la lectura.

Si no conoces la respuesta, dilo con honestidad — no inventes información.

Contexto:
{context}

Pregunta del usuario:
{question}

Tu respuesta bien estructurada:
"""

    return PromptTemplate(template=template, input_variables=["context", "question"])