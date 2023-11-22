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

# Nombre de la tabla en la base de datos
table_name = "bd_lematizacion"

# Crear la conexión
connection = psycopg2.connect(**DB_CONFIG)

# Crear un cursor
cursor = connection.cursor()

# Consultar la información sobre la estructura de la tabla
select_query = sql.SQL("""
    SELECT column_name, data_type
    FROM information_schema.columns
    WHERE table_name = {}
""").format(sql.Literal(table_name))

cursor.execute(select_query)

# Obtener los resultados
results = cursor.fetchall()

# Imprimir los resultados
for row in results:
    print(row)

# Cerrar el cursor y la conexión
cursor.close()
connection.close()
