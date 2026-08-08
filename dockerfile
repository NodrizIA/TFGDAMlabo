# Usamos una versión ligera de Python
FROM python:3.10-slim

# Creamos una carpeta para nuestra app
WORKDIR /app

# Copiamos la "receta" y la instalamos
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiamos el resto de nuestro código
COPY . .

# Exponemos el puerto por defecto de Flask
EXPOSE 5000

# Comando para arrancar la app
CMD ["flask", "run", "--host=0.0.0.0"]