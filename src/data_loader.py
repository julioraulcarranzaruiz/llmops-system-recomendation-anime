"""
Módulo de carga y procesamiento de datos de anime.

Proporciona funcionalidad para cargar datos de anime desde archivos CSV,
validar que contengan las columnas requeridas, y procesarlos en un formato
adecuado para la generación de embeddings y búsqueda vectorial.
"""

import pandas as pd
from sympy import re


class AnimeDataLoader:
    """
    Cargador y procesador de datos de anime desde CSV.
    
    Lee archivos CSV con información de anime, valida que contengan las columnas
    necesarias, y genera un nuevo CSV con información combinada optimizada para
    búsqueda semántica mediante embeddings.
    
    Attributes:
        original_csv (str): Ruta al archivo CSV original con datos de anime.
        processed_csv (str): Ruta donde se guardará el CSV procesado.
    """
    
    def __init__(self, csv_original: str, csv_processed: str):
        """
        Inicializa el cargador de datos de anime.
        
        Args:
            csv_original (str): Ruta al archivo CSV con los datos originales de anime.
                Debe contener las columnas: 'Name', 'Genres', 'Synopsis'.
            csv_processed (str): Ruta donde se guardará el archivo CSV procesado.
        """
        self.original_csv = csv_original
        self.processed_csv = csv_processed
    
    def load_data_process(self):
        """
        Carga, valida y procesa los datos de anime.
        
        Realiza las siguientes operaciones:
        1. Lee el CSV original ignorando líneas con formato incorrecto.
        2. Valida que existan las columnas requeridas.
        3. Combina información de Name, Genres y Synopsis en una sola columna.
        4. Guarda el resultado en un nuevo CSV procesado.
        
        Returns:
            str: Ruta al archivo CSV procesado generado.
        
        Raises:
            ValueError: Si faltan columnas requeridas en el CSV original.
            FileNotFoundError: Si el archivo CSV original no existe.
        """
        # 1. Leer CSV original, omitiendo líneas con errores de formato
        df = pd.read_csv(
            self.original_csv,
            encoding="utf-8",
            on_bad_lines='skip'  # Omitir líneas con errores de formato (reemplaza error_bad_lines deprecado)
            )
        
       
        
        # 2 -Validar columnas requeridas que existan
        required_columns = { 'Name', 'Genres', 'sypnopsis'}
        missing_columns = required_columns - set(df.columns)
        if missing_columns:
            raise ValueError(f"Las siguientes columnas requeridas están ausentes: {missing_columns}")

        # 3 Crear una nueva columna 'combined_info' combinando 'Genres' y 'sypnopsis'
        df['combined_info'] = (
            "Title:" + df['Name'] + "OverView:" + df['sypnopsis'] + "Genres:" + df['Genres']
        )

        
        # 4 - Guardar el DataFrame procesado en un nuevo archivo CSV
        df[['combined_info']].to_csv(self.processed_csv, index=False, encoding='utf-8')

        return self.processed_csv

