import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import json

# Carga geojson
with open('data/colombia_departamentos.geojson', 'r', encoding='utf-8') as f:
    geojson_col = json.load(f)

# Carga Divipola
divipola = pd.read_excel("data/Divipola_CE_.xlsx", sheet_name=0)
divipola['DEPARTAMENTO'] = divipola['DEPARTAMENTO'].str.strip().str.title()

# Diccionario de reemplazo para empatar nombres entre Divipola y GeoJSON
replace_dict = {
    "Archipiélago De San Andrés, Providencia Y Santa Catalina": "San Andrés y Providencia",
    "Bogotá, D.C.": "Distrito Capital de Bogotá",
    "Valle Del Cauca": "Valle del Cauca",
    "Norte De Santander": "Norte de Santander"
}
divipola["DEPARTAMENTO"] = divipola["DEPARTAMENTO"].replace(replace_dict)

# Agrupa (por cantidad de municipios solo como ejemplo; reemplaza .size() por .sum() si tienes una columna de muertes)
df_muertes = divipola.groupby('DEPARTAMENTO').size().reset_index(name="MUERTES")

# Obtiene nombres del geojson
departamentos_geojson = [feature['properties']['name'] for feature in geojson_col['features']]
df_base = pd.DataFrame({'DEPARTAMENTO': departamentos_geojson, 'MUERTES': 0})

# Merge para visualizar todos los departamentos (muertes reales donde existan)
df_completo = df_base.merge(df_muertes, on="DEPARTAMENTO", how="left")
df_completo["MUERTES"] = df_completo["MUERTES_y"].fillna(df_completo["MUERTES_x"])
df_completo = df_completo[["DEPARTAMENTO", "MUERTES"]]

print("Nombres de departamentos en geojson:", departamentos_geojson)
print("Nombres de departamentos en df_muertes:", df_muertes['DEPARTAMENTO'].tolist())
print("Faltantes:", df_completo[df_completo["MUERTES"] == 0]["DEPARTAMENTO"].tolist())

# Dash Layout
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dbc.Container([
    dbc.Row([dbc.Col(html.H2("MortandadColombiaDash - Mortalidad en Colombia 2019"), width=12)], className="mb-4 mt-4"),
    dbc.Row([
        dbc.Col([
            dcc.RadioItems(
                id='menu-graficos',
                options=[
                    {'label': 'Mapa por departamento', 'value': 'mapa'}
                ],
                value='mapa',
                labelStyle={'display': 'block'}
            )
        ], md=3),
        dbc.Col([html.Div(id='content-grafico')], md=9)
    ])
], fluid=True)

@app.callback(
    dash.dependencies.Output('content-grafico', 'children'),
    [dash.dependencies.Input('menu-graficos', 'value')]
)
def render_vista_grafico(grafico):
    if grafico == 'mapa':
        fig = px.choropleth(
            df_completo,
            geojson=geojson_col,
            locations='DEPARTAMENTO',
            color='MUERTES',
            featureidkey='properties.name',
            hover_name='DEPARTAMENTO',
            color_continuous_scale='Reds'
        )
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(title='Distribución de muertes por departamento')
        return dcc.Graph(figure=fig)
    else:
        return html.Div("Seleccione una visualización.")

if __name__ == "__main__":
    app.run(debug=True)
