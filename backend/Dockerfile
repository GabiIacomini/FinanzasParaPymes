# 1. Usar una imagen base oficial de Python
FROM python:3.11-slim

# 2. Establecer el directorio de trabajo
WORKDIR /code

# 3. Copiar el archivo de dependencias
COPY ./requirements.txt /code/requirements.txt

# 4. Instalar las dependencias
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 5. Copiar el código de la aplicación
COPY ./app /code/app

# 6. Exponer el puerto en el que corre la aplicación
EXPOSE 8000

# 7. Comando para correr la aplicación con uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
