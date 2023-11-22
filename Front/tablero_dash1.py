import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_table
import psycopg2
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import date
import dash_bootstrap_components as dbc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

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

def create_layout():
    return html.Div([
        html.H1(children='Bienvenido a tu recomendador de noticias DSA', style={'textAlign':'center'}),
        html.Br(),
        html.Br(),
        html.Div([
            html.H6("Ingrese un Nit"),
            dcc.Input(id='nit-input', type='text', value=''),
            html.Br(),
            html.Br(),
            html.H6("Ingrese el número de Noticias"),
            dcc.Input(id='noticia-input', type='text', value=''),
            html.Br(),
            html.Br(),
            html.H6("Selecciona la fecha"),
            dcc.DatePickerSingle(
                id='fecha-input',
                min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date(2017, 9, 19),
                initial_visible_month=date(2017, 8, 5),
                date=date(2017, 8, 25),
            ),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Button('Enviar', id='enviar-button'),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.H6("Noticias"),
            dash_table.DataTable(
                id='table',
                columns=[
                    {'name': 'Fecha', 'id': 'Fecha'},
                    {'name': 'Tema_noticia', 'id': 'Tema_noticia'},
                    {'name': 'Titulo_noticia', 'id': 'Titulo_noticia'},
                    {'name': 'Url', 'id': 'Url'},
                ],
                style_table={'height': '300px', 'overflowY': 'auto'},
            ),
        ]),
    ])

app.layout = create_layout()

@app.callback(
    Output(component_id='table', component_property='data'),
    Input(component_id='nit-input', component_property='value'),
    Input(component_id='noticia-input', component_property='value'),
    Input(component_id='fecha-input', component_property='value')
)
def update_table_data(nit, noticias, fecha):
    cursor = engine.cursor()
    try:
        if nit:
            query_nit = """
            SELECT Fecha,Tema_noticia,Titulo_noticia,Url
            FROM df_stemming_BD
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
        SELECT Fecha,Tema_noticia,Titulo_noticia,Url
        FROM df_stemming_BD;
        """

        cursor.execute(query_all)
        result_all = cursor.fetchall()

        # Convertir los resultados en un DataFrame
        #columns = ['nit', 'url', 'subsector']
        #df = pd.DataFrame(result_all, columns=columns)

        # Obtener los resultados en formato de lista de diccionarios
        #data = recomendador(nit, 10, df_bd_stemming_f2)

        #data_list = data.to_dict('records')

        #return url, subsector, data_list
    except Exception as e:
        print(f"Error: {str(e)}")
        return f"Error: {str(e)}", "", []

if __name__ == '__main__':
    app.run_server(debug=True, port=8040)
