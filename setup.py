"""
Script de configuración para el paquete ANIME.

Este archivo define la configuración necesaria para instalar el paquete Python 'ANIME'
utilizando setuptools. Especifica metadatos del proyecto, dependencias y configuración
de empaquetado.

Módulos requeridos:
    - setuptools: Para empaquetar y distribuir el paquete Python
"""

from setuptools import setup, find_packages

# Lectura de dependencias desde archivo de requisitos
# ====================================================
# Se abre el archivo 'requeriments.txt' y se leen todas las líneas
# que contienen los paquetes necesarios para ejecutar el proyecto.
with open("requeriments.txt") as f:
    requirements = f.read().splitlines()


# Configuración del paquete
# ==========================
# Define los metadatos y parámetros de instalación del paquete ANIME.
setup(
    name="ANIME",  # Nombre del paquete
    version="0.1.0",  # Versión del paquete (semantic versioning: major.minor.patch)
    author="Julio Carranza",  # Autor del proyecto
    packages=find_packages(),  # Descubre automáticamente todos los paquetes Python en el directorio
    install_requires=requirements,  # Lista de dependencias a instalar desde requeriments.txt
)
