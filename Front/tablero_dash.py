import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_table
import psycopg2
from dotenv import load_dotenv
import os

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

#env_path = "C:\\Users\\relat\\Dropbox\\Maestría UNIANDES\\6 Ciclo\\Despliegue de soluciones analíticas\\Proyecto\\Creacion BD\\env\\app.env"
env_path = 'app.env'

load_dotenv(dotenv_path=env_path)

USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
DBNAME = os.getenv('DBNAME')

engine = psycopg2.connect(
    dbname=DBNAME,
    user=USER,
    password=PASSWORD,
    host=HOST,
    port=PORT
)

app.layout = html.Div(
    [   html.H1(children='Bienvenido a tu recomendador de noticias DSA', style={'textAlign':'center'}),
        html.Br(),
        html.Br(),
        html.H6("Ingrese un Nit"),
        dcc.Input(id='nit-input', type='text', value=''),  # Ajuste aquí
        html.Br(),
        html.Br(),
        html.H6("Información del nit:"),
        html.Div(["URL:", html.Div(id='output-url')]),
        html.Div(["Subsector:", html.Div(id='output-subsector')]),
        html.Br(),
        html.H6("Tabla de Atributos"),
        dash_table.DataTable(
            id='table',
            columns=[
                {'name': 'Nit', 'id': 'nit'},
                {'name': 'URL', 'id': 'url'},
                {'name': 'Subsector', 'id': 'subsector'},
            ],
            style_table={'height': '300px', 'overflowY': 'auto'},
            filter_action='native',            
        ),
    ]
)

@app.callback(
    Output(component_id='output-url', component_property='children'),
    Output(component_id='output-subsector', component_property='children'),
    Output(component_id='table', component_property='data'),
    Input(component_id='nit-input', component_property='value')
)
def update_output_div(nit):
    cursor = engine.cursor()

    try:
        if nit:
            query_nit = """
            SELECT url, subsector
            FROM nombre_de_tabla
            WHERE nit = %s;
            """

            cursor.execute(query_nit, (nit,))
            result_nit = cursor.fetchone()

            if result_nit:
                url, subsector = result_nit
            else:
                url, subsector = "Nit no encontrado", ""
        else:
            url, subsector = "", ""

        query_all = """
        SELECT nit, url, subsector
        FROM nombre_de_tabla;
        """

        cursor.execute(query_all)
        result_all = cursor.fetchall()

        data = [{'nit': row[0], 'url': row[1], 'subsector': row[2]} for row in result_all if nit in str(row[0])]

        return url, subsector, data
    except Exception as e:
        print(f"Error: {str(e)}")
        return f"Error: {str(e)}", "", []

if __name__ == '__main__':
    app.run_server(debug=True, port=8040)