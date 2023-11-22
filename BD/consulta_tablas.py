import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

# Configuracion de la base de datos
load_dotenv('app.env')
DB_CONFIG = {
    'user': os.getenv('USER'),
    'password': os.getenv('PASSWORD'),
    'host': os.getenv('HOST'),
    'port': os.getenv('PORT'),
    'dbname': os.getenv('DBNAME'),
}
try:
    # Crear la conexión
    connection = psycopg2.connect(**DB_CONFIG)

    # Crear un cursor
    cursor = connection.cursor()

    # Consulta SQL para obtener las tablas en la base de datos
    table_query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
    """

    # Ejecutar la consulta
    cursor.execute(table_query)

    # Obtener los resultados
    tables = cursor.fetchall()

    # Imprimir las tablas
    print("Tablas en la base de datos:")
    for table in tables:
        print(table[0])

except Exception as e:
    print(f"Error de conexión: {e}")

finally:
    # Cerrar el cursor y la conexión en el bloque 'finally' para garantizar que siempre se cierren.
    if cursor:
        cursor.close()
    if connection:
        connection.close()
