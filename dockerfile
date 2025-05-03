
    
    
    # Usa una imagen base de Python
    FROM python:3.9-slim-buster
    
    # Establece el directorio de trabajo dentro del contenedor
    WORKDIR /app
    
    # Copia los archivos de requerimientos
    COPY requirements.txt /app
    
    # Instala las dependencias de Python
    RUN pip install -r requirements.txt
    
    # Copia el código de la aplicación
    COPY . /app
    
    # Expone el puerto en el que la aplicación escucha
    EXPOSE 5000
    
    # Comando para ejecutar la aplicación
    CMD ["python", "app.py"]
    
   