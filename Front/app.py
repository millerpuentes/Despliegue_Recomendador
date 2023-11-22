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

# Configuracion de la base de datos
load_dotenv('app.env')
DB_CONFIG = {
    'user': os.getenv('USER'),
    'password': os.getenv('PASSWORD'),
    'host': os.getenv('HOST'),
    'port': os.getenv('PORT'),
    'dbname': os.getenv('DBNAME'),
}

conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()

# Consulta a la base de datos bd_stemming
sql_stemming = """SELECT * FROM bd_stemming"""
cursor.execute(sql_stemming)
data_stemming = cursor.fetchall()

# Consulta a la base de datos bd_clientes
sql_clientes = """SELECT * FROM bd_clientes"""
cursor.execute(sql_clientes)
data_clientes = cursor.fetchall()
        
df_stemming = pd.DataFrame(data_stemming, columns=['Fecha', 'Tema_noticia', 'Titulo_noticia', 'Url'])
df_clientes = pd.DataFrame(data_clientes, columns=['Nit', 'Nombre', 'Sector'])


print(df_stemming) 
print(df_clientes)

resultados = pd.DataFrame([])

        
def create_layout():
    return html.Div(
        children=[
            dbc.Row(
                dbc.Col(
                    html.H2(
                        "Bienvenido a tu recomendador de noticias DSA",
                        style={'textAlign': 'center', 'color': '#0380C4'},
                    ),
                    width={"offset": 1},
                )
            ),
            html.Br(),
            dbc.Row(
                dbc.Col(
                    html.H5(
                        "Todos los campos deben ser diligenciados",
                        style={'textAlign': 'center', 'color':'#8b0000'},
                    ),
                    width={"size": 8, "offset": 2},
                )
            ),
            html.Hr(),
            html.Br(),
            html.H6("Ingrese un Nit"),
            dcc.Input(id='nit-input', type='text', value=''),
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
            html.Hr(),
            html.Br(),
            html.H6("Ingrese un Número de noticias que desea ver"),
            dcc.Input(id='not-input', type='text', value=''),
            html.Br(),
            html.Br(),
            dbc.Button("Enviar", id="enviar-button"),
            html.Br(),
            html.Br(),
            html.H6("Noticias"),
            #dash_table.DataTable(id='table-resultados', data=resultados.to_dict('records'), page_size=20, style_table={'overflowX': 'auto'}),
            dash_table.DataTable(id='table-resultados', data=resultados.to_dict('records'), page_size=20, style_table={'width': '100%', 'height': '100%','textAlign': 'center',},
)
         
            ],
        style={'textAlign': 'center', "margin-left": "15%", "margin-right": "15%", "margin-bottom": "5%"},
)

app = dash.Dash(__name__)

@app.callback(
    Output(component_id='table-resultados', component_property='data'),
    [State(component_id='nit-input', component_property='value'),
     State(component_id='fecha-input', component_property='date'),
     State(component_id='not-input', component_property='value'),
     Input(component_id='enviar-button', component_property='n_clicks')
    ],
    prevent_initial_call=True,
)


def update_table_data(nit, fecha,noticias, n_clicks):
    if n_clicks > 0:
            
            fecha = date.fromisoformat(fecha)
            num_noticias = int(noticias)


            df_stemming2 = df_stemming[df_stemming['Fecha']==fecha]

            # Se les da el valor dependiendo del cliente
            def asignar_valor(row, sector):
                 temas = {'Salud': [1, 9],
                          'Sostenibilidad': [2, 3],
                          'Innovación': [3, 4],
                          'Regulaciones': [4, 5],
                          'Deportes': [5, 10],
                          'Cultura': [6, 8],
                          'Reputación': [7, 7],
                          'Macroeconómicas': [8, 1],
                          'Política': [9, 2],
                          'Alianzas': [10, 6]
                        }
                 tema = row['Tema_noticia']

                 if sector == 'Salud':
                      return temas.get(tema, [11, 0])[0]
                 else:
                      return temas.get(tema, [11, 0])[1]
            
            # Se identifica el sector del Nit
            s = df_clientes[df_clientes['Nit'] == nit]['Sector'].iloc[0]

            # Se le aplica el valor asignado con la función asignar_valor
            df_stemming2['valor_asignado'] = df_stemming2.apply(lambda row: asignar_valor(row, s), axis=1)

            # Ordena el DataFrame por la columna 'valor_asignado'
            df_stemming2 = df_stemming2.sort_values(by='valor_asignado')
            
            # Agrupa el DataFrame por 'valor_asignado' y aplica la función para seleccionar aleatoriamente dos noticias
            resultados = df_stemming2.groupby('valor_asignado', group_keys=False).apply(lambda group: group.sample(n=min(2, len(group))))

            resultados.drop('valor_asignado', axis=1, inplace=True)

            resultados.reset_index(drop=True, inplace=True)

            resultados = resultados.head(num_noticias)

    return resultados.to_dict('records')

app.layout = create_layout()

app.run_server(debug=True, port=8040)
