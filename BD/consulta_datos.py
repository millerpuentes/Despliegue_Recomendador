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
table_name = "bd_stemming"
#table_name = "bd_lematizacion"
#table_name = "bd_clientes"

# Crear la conexión
connection = psycopg2.connect(**DB_CONFIG)

# Crear un cursor
cursor = connection.cursor()

# Ejecutar una consulta SELECT
select_query = sql.SQL("SELECT * FROM {} LIMIT 5").format(sql.Identifier(table_name))
cursor.execute(select_query)

# Obtener los resultados
results = cursor.fetchall()

# Imprimir los resultados de manera más estructurada
print("Resultados de la tabla '{}':".format(table_name))
print("{:<15} {:<20} {:<50} {:<}".format("Fecha", "Tema", "Título", "URL"))
print("-" * 120)

for row in results:
    print("{:<15} {:<20} {:<50} {:<}".format(row[0].strftime("%Y-%m-%d"), row[1], row[2], row[3]))


# Imprimir los resultados de manera más estructurada
#print("Resultados de la tabla '{}':".format(table_name))
#print("{:<15} {:<20} {:<50}".format("Nit","Nombre","Sector"))
#print("-" * 120)

for row in results:
    print("{:<15} {:<20} {:<50}".format(row[0], row[1], row[2]))


# Cerrar el cursor y la conexión
cursor.close()
connection.close()


