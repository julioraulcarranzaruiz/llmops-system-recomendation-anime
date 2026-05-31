"""
Módulo de excepciones personalizadas para el proyecto ANIME.

Este módulo define una clase de excepción personalizada que captura información
detallada sobre errores, incluyendo el nombre del archivo, número de línea y
detalles específicos del error. Facilita el debugging al proporcionar un contexto
completo cuando se lanza una excepción.

Clases:
    CustomException: Excepción personalizada con información detallada del error.
"""

import sys


class CustomException(Exception):
    """
    Excepción personalizada que captura información detallada del contexto de error.
    
    Heredada de Exception, esta clase enriquece los mensajes de error con información
    del archivo fuente y número de línea donde ocurrió el error, facilitando la depuración.
    
    Atributos:
        error_message (str): Mensaje de error detallado que incluye contexto del error.
    
    Ejemplo:
        try:
            # Código que puede generar un error
            result = 1 / 0
        except ZeroDivisionError as e:
            raise CustomException("División por cero detectada", e)
    """
    
    def __init__(self, message: str, error_detail: Exception = None):
        """
        Inicializa la excepción personalizada.
        
        Captura el mensaje de error y detalles adicionales, luego genera un mensaje
        enriquecido que incluye información del archivo y línea de error.
        
        Args:
            message (str): Mensaje de error descriptivo del usuario.
            error_detail (Exception, optional): La excepción original capturada.
                                              Defaults to None.
        """
        self.error_message = self.get_detailed_error_message(message, error_detail)
        super().__init__(self.error_message)

    @staticmethod
    def get_detailed_error_message(message, error_detail):
        """
        Genera un mensaje de error detallado con contexto del traceback.
        
        Extrae información del stack trace actual (archivo y línea) y construye
        un mensaje enriquecido que combina el mensaje del usuario, el error original,
        y el contexto de donde ocurrió.
        
        Args:
            message (str): Mensaje de error del usuario.
            error_detail (Exception): Excepción original capturada.
        
        Returns:
            str: Mensaje de error formateado con contexto completo.
                Formato: "message | Error: error_detail | File: filename | Line: lineno"
        """
        # Obtiene información del traceback actual
        _, _, exc_tb = sys.exc_info()
        
        # Extrae el nombre del archivo del frame actual, o "Unknown File" si no existe
        file_name = exc_tb.tb_frame.f_code.co_filename if exc_tb else "Unknown File"
        
        # Extrae el número de línea del traceback, o "Unknown Line" si no existe
        line_number = exc_tb.tb_lineno if exc_tb else "Unknown Line"
        
        # Construye y retorna el mensaje formateado
        return f"{message} | Error: {error_detail} | File: {file_name} | Line: {line_number}"

    def __str__(self):
        """
        Retorna la representación en string de la excepción.
        
        Returns:
            str: El mensaje de error detallado.
        """
        return self.error_message