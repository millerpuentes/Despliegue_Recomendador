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

    # Eliminar todas las tablas
    for table in tables:
        drop_table_query = sql.SQL("DROP TABLE IF EXISTS {} CASCADE").format(sql.Identifier(table[0]))
        cursor.execute(drop_table_query)

    # Confirmar los cambios
    connection.commit()

    print("Todas las tablas han sido eliminadas correctamente.")

except Exception as e:
    print(f"Error al eliminar las tablas: {e}")

finally:
    # Cerrar el cursor y la conexión en el bloque 'finally' para garantizar que siempre se cierren.
    if cursor:
        cursor.close()
    if connection:
        connection.close()
