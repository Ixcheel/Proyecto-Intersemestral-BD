#Imagen Python
FROM python:3.11-slim

# Directorio
WORKDIR /app

# Archivo de requerimientos e instalarlos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Código fuente
COPY . .

# Puerto de Flask
EXPOSE 5001

# Ejecutar
CMD ["flask", "--app", "src/app.py", "run", "--host=0.0.0.0"]