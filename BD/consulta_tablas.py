import psycopg2
from psycopg2 import sql

# Configuración de la conexión a la base de datos
USER = "postgres"
PASSWORD = "Hoy_14_11_2023"
HOST = "proyecto.ctfb7fnoyrsf.us-east-1.rds.amazonaws.com"
PORT = "5432"
DBNAME = "postgres"

# Declarar variables fuera del bloque try para que tengan un alcance más amplio
connection = None
cursor = None

try:
    # Crear la conexión
    connection = psycopg2.connect(
        dbname=DBNAME, user=USER, password=PASSWORD, host=HOST, port=PORT, sslmode='require'
    )

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
