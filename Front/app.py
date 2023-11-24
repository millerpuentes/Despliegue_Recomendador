import dash
from dash import dcc, html
import dash_labs as dl
from dash.dependencies import Input, Output, State
import dash_table
import psycopg2
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import date
import dash_bootstrap_components as dbc
from dash_labs.plugins.pages import register_page


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

#nit="801004045"
# Consulta a la base de datos bd_clientes
#sql_clientes = """SELECT * FROM bd_clientes WHERE 0={}""".format(nit)
sql_clientes = """SELECT * FROM bd_clientes"""
cursor.execute(sql_clientes)
data_clientes = cursor.fetchall()
        
df_stemming = pd.DataFrame(data_stemming, columns=['Fecha', 'Tema_noticia', 'Titulo_noticia', 'Url'])
df_clientes = pd.DataFrame(data_clientes, columns=['Nit', 'Nombre', 'Sector'])

#df_stemming = pd.DataFrame(data_stemming)
#df_clientes = pd.DataFrame(data_clientes)
print(df_stemming) 
print(df_clientes)

resultados = pd.DataFrame([])

""" ------------------------------------------- Layout ------------------------------------------"""
def create_navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Nosotros", href="/Nosotros")),
            dbc.NavItem(dbc.NavLink("Contexto", href="/Contexto")),
            # Agrega más enlaces según sea necesario
        ],
        brand="Recomendador",
        brand_href="/",
        color="primary",
        dark=True,
        style={'fontSize': '25px'}
    )
    return navbar

def create_layout():
    layout = html.Div(
        children=[
            create_navbar(),  # Agrega la barra de navegación
            dbc.Container(
                children=[
            html.Br(),
            dbc.Row(
                dbc.Col(
                    html.H1(
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
            html.Br(),
            html.Br(),
            html.H6("Ingrese un Número de noticias que desea ver"),
            dcc.Input(id='not-input', type='text', value=''),
            html.Br(),
            html.Br(),
            dbc.Button("Enviar", id="enviar-button"),
            html.Br(),
            html.Hr(),
            html.H2("Noticias"),
            #dash_table.DataTable(id='table-resultados', data=resultados.to_dict('records'), page_size=20, style_table={'overflowX': 'auto'}),
            dash_table.DataTable(id='table-resultados', data=resultados.to_dict('records'), page_size=20, style_table={'width': '100%', 'height': '100%','textAlign': 'center'})
         
            
                ],style={'textAlign': 'center', "margin-left": "15%", "margin-right": "15%", "margin-bottom": "5%"},
            ),
        ]
    )
    return layout


app = dash.Dash(
    __name__, 
    plugins=[dl.plugins.pages], 
    external_stylesheets=[dbc.themes.FLATLY], 
    update_title='Cargando...',
    suppress_callback_exceptions=True 
)


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")],
)
def display_page(pathname):
    if pathname == "/Nosotros":
        return layout_nosotros()
    elif pathname == "/Contexto":
        return layout_Contexto()
    # Agrega más condiciones para otras páginas según sea necesario
    else:
        return create_layout()

# Funciones de diseño para páginas adicionales
def layout_nosotros():
    return html.Div(
        children=[
            create_navbar(),  # Agrega la barra de navegación
                dbc.Col([
                dbc.Row(["Equipo 7"], className= "flex-fill ", style={'textAlign': 'center', 'color':'#0380C4'})
                ], className = "d-flex display-4 align-self-center flex-column align-items-center"),

                dbc.Col([
                html.Br(),    
                html.Br(),
                dbc.Row([
                html.Img(
                        src='https://raw.githubusercontent.com/millerpuentes/Despliegue_Recomendador/main/Imagenes/image_Catalina.png',
                        className="img-fluid",
                        style={'width': '200px', 'height': 'auto'}
                        )
                ], className="d-flex justify-content-center align-items-center"),
                html.H3("Catalina Cárdenas",style={'textAlign': 'center', 'color': '#008080'}),

                html.Br(),    
                html.Br(),
                dbc.Row([
                html.Img(
                        src='https://raw.githubusercontent.com/millerpuentes/Despliegue_Recomendador/main/Imagenes/image_Grace.png',
                        className="img-fluid",
                        style={'width': '200px', 'height': 'auto'}
                        )
                ], className="d-flex justify-content-center align-items-center"),
                html.H3("Grace González",style={'textAlign': 'center', 'color': '#008080'}),

                html.Br(),    
                html.Br(),
                dbc.Row([
                html.Img(
                        src='https://raw.githubusercontent.com/millerpuentes/Despliegue_Recomendador/main/Imagenes/image_Joan.png',
                        className="img-fluid",
                        style={'width': '200px', 'height': 'auto'}
                        )
                ], className="d-flex justify-content-center align-items-center"),
                html.H3("Joan Chacón",style={'textAlign': 'center', 'color': '#008080'}),


                html.Br(),    
                html.Br(),
                dbc.Row([
                html.Img(
                        src='https://raw.githubusercontent.com/millerpuentes/Despliegue_Recomendador/main/Imagenes/image_MP.png',
                        className="img-fluid",
                        style={'width': '200px', 'height': 'auto'}
                        )
                ], className="d-flex justify-content-center align-items-center"),
                html.H3("Miller Puentes",style={'textAlign': 'center', 'color': '#008080'}),
              
                ]),

                dbc.Row([
                dbc.Col([html.Div(),], className = 'p-5'),
                ]),
                
                dbc.Row([
                dbc.Col([html.Div(),], className = 'p-5'),
                ]),
])

def layout_Contexto():
    return html.Div(
        children=[
            create_navbar(),  # Agrega la barra de navegación
            html.H1("Contexto de Negocio"),
            html.H6("Como parte de la estrategia comercial y de fidelización de clientes\
                    en una entidad bancaria, se desarrolló una herramienta informativa basada en\
                    aprendizaje automático para ofrecer a los clientes recomendaciones de noticias\
                    relevantes y confiables de acuerdo a su sector. Se analizó una base de datos vinculando\
                    información de clientes y noticias mediante algoritmos de PLN, dada su composición\
                    textual predominante. La clusterización temática de las noticias se efectuó con el\
                    modelo LDA de Gensim, evaluando su eficacia tanto con textos lematizados como con\
                    Stemming. Se realizó además una recategorización de clientes para afinar las recomendaciones\
                    según la relevancia temática para cada sector.", style={'textAlign': 'center', 'color': '#008080'}),
            html.Br(),       
            html.Br(),  
            html.Br(),    
            html.H1("Impacto"), 
            html.H6("La relevancia de este ejercicio analítico radica en fortalecer el conocimiento que el \
                    banco tiene sobre sus clientes corporativos. Mediante el uso de técnicas de aprendizaje no \
                    supervisado como el procesamiento de lenguaje natural (NLP), se busca diseñar un sistema de \
                    recomendación de noticias que extraiga y categorice información relevante de medios de comunicación.\
                     Se crea una herramienta analítica que sirva como una ventaja competitiva en el entendimiento profundo \
                    del cliente. Esta iniciativa aprovecha la inteligencia artificial y el procesamiento de texto para\
                     comprender el lenguaje humano y organizar automáticamente noticias de interés para los clientes. \
                    Con este sistema de recomendación de noticias, se espera mejorar la experiencia del cliente al \
                    proporcionarles información altamente relevante, lo que, a su vez, puede diferenciar a la empresa\
                     en el mercado y fortalecer relaciones con los clientes corporativos.", style={'textAlign': 'center', 'color': '#008080'})
            # Agrega el resto del contenido de la página 2 aquí
        ]
    )


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

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content"),
])

app.run_server(debug=True, port=8040)
