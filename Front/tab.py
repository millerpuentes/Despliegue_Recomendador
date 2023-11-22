import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
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

#USER = os.getenv('USER')
#PASSWORD = os.getenv('PASSWORD')
#HOST = os.getenv('HOST')
#PORT = os.getenv('PORT')
#DBNAME = os.getenv('DBNAME')

#try:
#    engine = psycopg2.connect(
#        dbname=DBNAME,
#        user=USER,
#        password=PASSWORD,
#        host=HOST,
#        port=PORT
#    )
    # Resto del código
#except psycopg2.Error as e:
#    print(f"Error de psycopg2: {e}")
#finally:
#    engine.close()



def create_layout():
    return html.Div([
        html.Div(children=[dbc.Row(dbc.Col(html.H2("Bienvenido a tu recomendador de noticias DSA"),style={'textAlign': 'center', 'color': '#0380C4'}, width={"offset": 1}))]),
        html.Br(),
        html.Div(children=[dbc.Row(dbc.Col(html.H5("Todos los campos deben ser diligenciados"), style={'textAlign': 'center', 'color':'#8b0000'},width={"size": 8, "offset": 2}))]),
        html.Hr(),
        html.Br(),
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
                min_date_allowed=date(2022, 1, 1),
                max_date_allowed=date(2022, 12, 31),
                initial_visible_month=date(2022, 7, 30),
                date=date(2022, 7, 30),
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Button("Buscar", id="enviar-button", n_clicks=0),
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
 ],style={'textAlign': 'center' , "margin-left": "15%", "margin-right": "15%", "margin-bottom": "5%"}
)


app.layout = create_layout()

@app.callback(
    Output(component_id='table', component_property='data'),
    [State(component_id='nit-input', component_property='value'),
    State(component_id='noticia-input', component_property='value'),
    State(component_id='fecha-input', component_property='date'),
    Input(component_id='enviar-button', component_property='n_clicks'),

    ],prevent_initial_call =True
)
def update_table_data(n_clicks,nit, noticia, fecha):
    cursor = engine.cursor()
    
    query_not = """
        SELECT Fecha,Tema_noticia,Titulo_noticia,Url
        FROM df_stemming
        WHERE Fecha = %s;
        """
    cursor.execute(query_not, (fecha,))
    result_not = cursor.fetchall()

    data = [{'Fecha': row[0], 'Tema_noticia': row[1], 'Titulo_noticia': row[2], 'Url': row[3]} for row in result_not]

    #Nit,Nombre,Sector
    query_nit = """
        SELECT Nit,Nombre,Sector
        FROM df_clientes
        WHERE Nit = %s;
        """
    cursor.execute(query_nit, (nit,))
    result_nit = cursor.fetchall()


    return data

if __name__ == '__main__':
    app.run_server(debug=True, port=8040)
