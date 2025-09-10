# Usa Python 3.8 (compatibilidad con tus librerías)
FROM python:3.8-slim

# Evita mensajes interactivos
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copia requirements primero (para aprovechar cache de Docker)
COPY requirements.txt .

# Instala dependencias
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copia el resto de archivos del proyecto
COPY app.py .
COPY model ./model
COPY data ./data   
# opcional, solo si quieres llevar tu CSV para debugging

# Expone el puerto (por defecto 80 dentro del contenedor)
EXPOSE 80

# Comando de inicio (lanza FastAPI con Uvicorn)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
