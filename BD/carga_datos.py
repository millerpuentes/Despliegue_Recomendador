import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os
import pandas as pd

# Configuracion de la base de datos
load_dotenv('app.env')
DB_CONFIG = {
    'user': os.getenv('USER'),
    'password': os.getenv('PASSWORD'),
    'host': os.getenv('HOST'),
    'port': os.getenv('PORT'),
    'dbname': os.getenv('DBNAME'),
}


""" Se cargan los datos de Stemming"""
# Ruta del archivo CSV
csv_file_path = '../Data/df_stemming_BD.csv'
# Nombre de la tabla en la base de datos
table_name = "bd_stemming"
#Fecha,Tema_noticia,Titulo_noticia,Url

""" Se cargan los datos de Lematizacion"""
# Ruta del archivo CSV
#csv_file_path = '../Data/df_lemat_BD.csv'
# Nombre de la tabla en la base de datos
#table_name = "bd_lematizacion"
#Fecha,Tema_noticia,Titulo_noticia,Url

""" Se cargan los datos de los clientes"""
# Ruta del archivo CSV
#csv_file_path = '../Data/df_clientes_BD.csv'
# Nombre de la tabla en la base de datos
#table_name = "bd_clientes"
#Nit,Nombre,Sector

connection = psycopg2.connect(**DB_CONFIG)

# Crear un cursor
cursor = connection.cursor()

# Eliminar la tabla si existe
drop_table_query = sql.SQL("DROP TABLE IF EXISTS {}").format(sql.Identifier(table_name))
cursor.execute(drop_table_query)
connection.commit()

# Leer el CSV con pandas
df = pd.read_csv(csv_file_path)

#Fecha,Tema_noticia,Titulo_noticia,Url
# Crear la tabla con tipos de datos específicos
column_data_types = {
    'Fecha': 'DATE',
    'Tema_noticia': 'VARCHAR(255)',
    'Titulo_noticia': 'TEXT',
    'Url': 'TEXT',
}

#Nit,Nombre,Sector
#column_data_types = {
#    'Nit': 'VARCHAR(255)',
#    'Nombre': 'VARCHAR(255)',
#    'Sector': 'VARCHAR(255)'
#}

columns_with_types = [
    f'"{column}" {column_data_types.get(column, "VARCHAR(255)")}'
    for column in df.columns
]
create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns_with_types)})"
cursor.execute(create_table_query)
connection.commit()

# Cargar datos desde el CSV
with open(csv_file_path, 'r', encoding='utf-8') as f:
    cursor.copy_expert(f"COPY {table_name} FROM stdin WITH CSV HEADER DELIMITER as ','", f)

# Realizar una consulta para obtener los primeros 5 datos de la tabla
select_query = sql.SQL("SELECT * FROM {} LIMIT 5").format(sql.Identifier(table_name))
cursor.execute(select_query)
data = cursor.fetchall()
data = pd.DataFrame(data)


print(data.head(5))

# Commit y cerrar la conexión
connection.commit()
cursor.close()
connection.close()

print("Carga de datos completada con éxito de la BD", table_name)




