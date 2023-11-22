import psycopg2
from psycopg2 import sql

# Configuración de la conexión a la base de datos
USER = "postgres"
PASSWORD = "Hoy_14_11_2023"
HOST = "proyecto.ctfb7fnoyrsf.us-east-1.rds.amazonaws.com"
PORT = "5432"
DBNAME = "postgres"

# Nombre de la tabla en la base de datos
table_name = "bd_lematizacion"

# Crear la conexión
connection = psycopg2.connect(
    dbname=DBNAME, user=USER, password=PASSWORD, host=HOST, port=PORT
)

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
