FROM python:3.8.13

# Crear usuario que ejecuta el dash
RUN adduser --disabled-password --gecos '' dash-user

# Definir directorio de trabajo 
WORKDIR /opt/app

RUN apt-get update && apt-get install -y libpq-dev

# Instalar dependencias
ADD ./app /opt/app/
RUN pip install --upgrade pip
RUN pip install -r /opt/app/requirements.txt

# Hacer el directorio de trabajo ejecutable 
RUN chmod +x /opt/app/run.sh
# Cambiar propiedad de la carpeta a dash-user 
RUN chown -R dash-user:dash-user ./

USER dash-user
# Puerto a exponer para el tablero
EXPOSE 8050

# Comandos a ejecutar al correr el contenedor 
CMD ["bash", "./run.sh"]
