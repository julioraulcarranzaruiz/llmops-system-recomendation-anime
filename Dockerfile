## Imagen base
FROM python:3.10-slim

## Variables de entorno esenciales
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

## Directorio de trabajo dentro del contenedor
WORKDIR /app

## Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

## Copiar todos los contenidos del local al contenedor
COPY . .

## Ejecutar setup.py
RUN pip install --no-cache-dir -e .

# Puertos utilizados
EXPOSE 8501

# Ejecutar la aplicación
CMD ["streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0","--server.headless=true"]