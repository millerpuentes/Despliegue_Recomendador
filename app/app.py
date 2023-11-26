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
#from dash_labs.plugins.pages import register_page


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
sql_stemming = "SELECT * FROM bd_stemming"
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

resultados = pd.DataFrame(columns=['Fecha', 'Tema_noticia', 'Titulo_noticia', 'Url'])


""" ------------------------------------------- Layout ------------------------------------------"""
def create_navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Nosotros", href="/Nosotros")),
            dbc.NavItem(dbc.NavLink("Contexto", href="/Contexto")),
        ],
        brand="Recomendador",
        brand_href="/",
        color="primary",
        dark=True,
        className="navbar-brand-custom",
        style={'fontSize': '25px'}
    )
    return navbar

def create_footer():
    footer = dbc.NavbarSimple(
        children=[
            dbc.NavItem(
                dbc.NavLink(
                    [
                        html.I(className="bi bi-github"),  # Icono de GitHub
                        " Repositorio del Código"
                    ],
                    href="https://github.com/millerpuentes/Despliegue_Recomendador.git",
                    target="_blank"
                )
            ),
        ],
        brand="© Desarrollado por: Equipo de analítica de datos MIAD.",
        brand_href="/Nosotros",  
        color="primary",
        dark=True,
        style={'fontSize': '14px', 'position': 'fixed', 'bottom': '0', 'width': '100%'},  
        className="navbar-footer",  
    )
    
    # Agrega el enlace de los íconos al head del HTML
    footer.children.append(html.Link(href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.18.0/font/bootstrap-icons.css", rel="stylesheet"))
    
    return footer


def create_layout():
    layout = html.Div(
        children=[
            create_navbar(),  
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
            dbc.Row([
                 dbc.Col(
                      [
                           html.H6("Ingrese su Nit"),
                           dcc.Input(id='nit-input', type='text', value='',style={'height': '40px','width':'300px','text-align': 'center'}, placeholder='Campo obligatorio'),
                           html.Br(),
                    ], width=4  
                    ),
                 dbc.Col(
                     [
                          html.H6("Selecciona la fecha"),
                          dcc.DatePickerSingle(
                               id='fecha-input',
                               min_date_allowed=date(2022, 1, 1),
                               max_date_allowed=date(2022, 12, 31),
                               initial_visible_month=date(2022, 7, 30),
                               date=date(2022, 7, 30),
                               style={'height': '40px', 'width': '300px', 'text-align': 'center'}
                               ),
                          html.Br(),
                    ], width=4  
                    ),
                dbc.Col(
                     [
                          html.H6("Ingrese el número de noticias que desea ver"),
                          dcc.Input(id='not-input', type='text', value='',style={'height': '40px','width':'300px','text-align': 'center'}, placeholder='Campo obligatorio'),
                          html.Br(),
                     ], width=4  
                     ),
                ]),
            html.Br(),
            html.Br(),
            html.Br(),
            dbc.Button("Enviar", id="enviar-button",style={'height': '40px','width':'400px','text-align': 'center'}),
            html.Br(),
            html.Hr(),
            html.Br(),
            html.H2("Noticias"),
            #dash_table.DataTable(id='table-resultados', data=resultados.to_dict('records'), page_size=20, style_table={'width': '100%', 'height': '100%','textAlign': 'center'})

            dash_table.DataTable(
                id='table-resultados',
                data=resultados.to_dict('records'),
                page_size=20,
                style_table={'width': '100%', 'height': '100%', 'textAlign': 'center'},
                columns=[
                    {'id': 'Fecha', 'name': 'Fecha', 'presentation': 'markdown'},
                    {'id': 'Tema_noticia', 'name': 'Temática de la Noticia', 'presentation': 'markdown'},
                    {'id': 'Titulo_noticia', 'name': 'Título de la Noticia', 'presentation': 'markdown'},
                    {'id': 'Url', 'name': 'Dirección electrónica de la Noticia', 'presentation': 'markdown'},
                        ],
                tooltip_data=[
                    {column: {'value': str(value), 'type': 'markdown'}
                     for column, value in row.items()
                    } for row in resultados.to_dict('records')
                    ],
                css=[{
                    'selector': '.dash-table-tooltip',
                    'rule': 'background-color: grey; font-family: monospace; color: white'
                    }],
                tooltip_delay=0,
                tooltip_duration=None,
                style_cell={'textAlign': 'center'},
                style_header={'fontWeight': 'bold'},  # Hacer que los encabezados de las columnas estén en negrita
                style_cell_conditional=[
                    {
                        'if': {'column_id': 'Fecha'},
                        'maxWidth': 50,
                        'maxHeight':500,
                    },
                    
                    {
                        'if': {'column_id': 'Tema_noticia'},
                        'maxWidth': 100,
                        'maxHeight':500,
                    },
                    
                    {
                        'if': {'column_id': 'Url'},
                        'maxWidth': 200,
                        'maxHeight':500,
                    },
                    {
                        'if': {'column_id': 'Titulo_noticia'},
                        'maxWidth': 200,  # Ajusta este ancho según tus necesidades
                        'maxHeight':500,
                    }
                    ],
                style_data_conditional=[
                    {
                        'if': {
                            'filter_query': '{Mensaje} contains "No hay noticias"'
                             },
                             'backgroundColor': '#FFD700',
                             'color': 'black'
        }
    ],

)

            
                ],style={'textAlign': 'center', 'margin-left': '8%', 'margin-right': '8%', 'margin-bottom': '5%', 'background-color': '#F3EFEF'},  # Agrega el fondo crema claro azul verdoso
            ),
            create_footer(), 
        ]
    )
    return layout


app = dash.Dash(
    __name__, 
    #plugins=[dl.plugins.pages], 
    external_stylesheets=[dbc.themes.FLATLY], 
    update_title='Cargando...',
    suppress_callback_exceptions=True 
)

@app.callback(
    Output("enviar-button", "disabled"),
    [Input("nit-input", "value"),
     Input("fecha-input", "date"),
     Input("not-input", "value")]
)
def update_button_disabled(nit, fecha, noticias):
    return not (nit and fecha and noticias)

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")],
)
def display_page(pathname):
    if pathname == "/Nosotros":
        return layout_nosotros()
    elif pathname == "/Contexto":
        return layout_Contexto()
    else:
        return create_layout()

# Funciones de diseño para páginas adicionales
def layout_nosotros():
    return html.Div(
        children=[
            create_navbar(),  # Agrega la barra de navegación
                dbc.Col([
                html.Br(),    
                html.Br(),
                dbc.Row(["Equipo 7"], className= "flex-fill ", style={'textAlign': 'center', 'color':'#0380C4'})
                ], className = "d-flex display-4 align-self-center flex-column align-items-center"),
                html.Br(),    
                html.Br(),
                dbc.Col([
                html.Br(),    
                html.Br(),
                dbc.Row([
                html.Img(
                        src='https://raw.githubusercontent.com/millerpuentes/Despliegue_Recomendador/main/Imagenes/equipo.png',
                        className="img-fluid",
                        style={'width': '9000px', 'height': 'auto'}
                        )
                ], className="d-flex justify-content-center align-items-center"),

              
                ]),

                dbc.Row([
                dbc.Col([html.Div(),], className = 'p-5'),
                ]),
                
                dbc.Row([
                dbc.Col([html.Div(),], className = 'p-5'),
                ]),
                create_footer()
])


def layout_Contexto():
    return html.Div(
        children=[
            create_navbar(),  # Agrega la barra de navegación

            html.Br(),  
            
            html.H2("Contexto de Negocio", style={'textAlign': 'center', 'color': '#0380C4'}),
            
            html.H4(
                "Como parte de nuestra estrategia comercial y de fidelización de clientes en una entidad bancaria, "
                "hemos desarrollado una herramienta informativa basada en aprendizaje automático. Su objetivo es ofrecer a los clientes "
                "recomendaciones de noticias relevantes y confiables, adaptadas a su sector. Hemos analizado una base de datos que vincula "
                "información de clientes y noticias mediante algoritmos de Procesamiento de Lenguaje Natural (PLN). Esto se hizo dada la "
                "composición predominante de texto en la información disponible. Utilizamos algoritmos de clustering temático, como el modelo "
                "LDA de Gensim, evaluando su eficacia tanto con textos lematizados como con Stemming. También llevamos a cabo una recategorización "
                "de clientes para afinar las recomendaciones según la relevancia temática para cada sector.",
                style={'textAlign': 'justify', 'color': '#008080','margin': '50px'}
            ),
            
            html.Br(),       
          
            html.H2("Impacto", style={'textAlign': 'center', 'color': '#0380C4'}), 
            
            html.H4(
                "La relevancia de este ejercicio analítico radica en fortalecer nuestro conocimiento sobre nuestros clientes corporativos. "
                "Mediante el uso de técnicas de aprendizaje no supervisado, como el Procesamiento de Lenguaje Natural (NLP), buscamos diseñar un "
                "sistema de recomendación de noticias que extraiga y categorice información relevante de los medios de comunicación. Creamos "
                "una herramienta analítica que sirva como una ventaja competitiva en el entendimiento profundo del cliente. Esta iniciativa "
                "aprovecha la inteligencia artificial y el procesamiento de texto para comprender el lenguaje humano y organizar automáticamente "
                "noticias de interés para nuestros clientes. Con este sistema de recomendación de noticias, esperamos mejorar la experiencia del cliente "
                "proporcionándoles información altamente relevante, lo que, a su vez, puede diferenciar a nuestra empresa en el mercado y fortalecer "
                "relaciones con nuestros clientes corporativos.",
                style={'textAlign': 'justify', 'color': '#008080','margin': '50px'}
            ),
            html.Img(src='https://raw.githubusercontent.com/millerpuentes/Despliegue_Recomendador/main/Imagenes/image_banco.jpg',
                        className="img-fluid mx-auto d-block",
                        style={'width': '900px', 'height': 'auto', 'marginTop': '0px'}
                        ),

            create_footer()
        ],
        style={'margin': '5px'} 
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
def update_table_data(nit, fecha, noticias, n_clicks):
    if n_clicks > 0:
        num_noticias = int(noticias)
        fecha = date.fromisoformat(fecha)
        df_stemming2 = df_stemming[df_stemming['Fecha'] == fecha]

        if len(df_stemming2) == 0:
            #return [{'Mensaje': 'No existen noticias registradas para esas fechas'}]
            return [{'Fecha': '', 'Tema_noticia': '', 'Titulo_noticia': '', 'Url': '', 'Mensaje': 'No hay noticias'}]
        
        else:
            df_stemming2 = df_stemming2.sample(n=num_noticias, random_state=42)
            # Se identifica el sector del Nit (moví esta línea fuera del bloque 'else')
            s = df_clientes[df_clientes['Nit'] == nit]['Sector'].iloc[0]

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

            # Se le aplica el valor asignado con la función asignar_valor
            df_stemming2['valor_asignado'] = df_stemming2.apply(lambda row: asignar_valor(row, s), axis=1)

            # Ordena el DataFrame por la columna 'valor_asignado'
            df_stemming2 = df_stemming2.sort_values(by='valor_asignado')

            df_stemming2.drop('valor_asignado', axis=1, inplace=True)

            resultados_dict = df_stemming2.to_dict('records')

        return resultados_dict



app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content"),
])

app.run_server(debug=True, port=8040)
#app.run_server(host="0.0.0.0", debug=True)