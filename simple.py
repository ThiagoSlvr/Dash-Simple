from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import plotly.express as px
from dash.exceptions import PreventUpdate

app = Dash(__name__, suppress_callback_exceptions=True)

# Definiçao de variaveis

# Definição variaveis mapa
df = px.data.election()
geojson = px.data.election_geojson()

fig = px.choropleth_mapbox(df, geojson=geojson, color="Bergeron",
                           locations="district", featureidkey="properties.district",
                           center={"lat": 45.5517, "lon": -73.7073},
                           mapbox_style="carto-positron", zoom=9)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# layout
app.layout = html.Div(children=[
    dcc.Location(id='url', refresh=False),
    html.Div(id='conteudo')
])

#index

index = html.Div(children=[
    html.H1(children='Sistemas para Internet II - Trabalho IV'),
    dcc.Link(html.Button('Pagina de input'), href="/pg_input"),
    html.Br(),
    html.Br(),
    dcc.Link(html.Button('Pagina do grafico'), href="/pg_graf"),
])

#pg 1

pg_input= html.Div(children=[
    dcc.Link(html.Button('Voltar'), href="/"),
    html.Br(),
    html.Br(),

    dcc.Input(id='input',
    placeholder='Entrada sem state'),
    html.Div(id='saida'),

    html.Br(),

    dcc.Input(id='input_2',
    placeholder='Entrada com state'),
    html.Br(),
    html.Br(),
    html.Button('Enviar', id='enviar'),
    html.Div(id='saida_2'),
])

@app.callback(
    Output(component_id='saida', component_property='children'),
    Input(component_id='input', component_property='value'),
)

def pagina_input(texto):
    return texto

@app.callback(
    Output('saida_2', 'children'),
    Input('enviar','n_clicks'),
    State('input_2','value'),
)

def pagina_input2(n_clicks,texto):
    return texto

#pg 2

pg_graf = html.Div(children=[
    dcc.Link("Voltar", href="/"),
    html.H1('Pagina do grafico'),
    html.Button('Clique aqui para mostrar o grafico', id='botao'),
    html.Br(),
    dcc.Graph(id = 'graf')
])

@app.callback(
    Output('graf', 'figure'),
    Input('botao', 'n_clicks'),
)

def pagina_graf(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        return fig

#callback que cuida das paginas
@app.callback(Output('conteudo', 'children'),
              [Input('url', 'pathname')])

def update_output(path):
    if path == '/pg_graf':
        return pg_graf
    elif path == '/pg_input':
        return pg_input
    else:
        return index

if __name__ == '__main__':
    app.run_server(debug=True)