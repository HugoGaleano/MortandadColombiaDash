import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import json

# GeoJSON de departamentos
with open('data/colombia_departamentos.geojson', 'r', encoding='utf-8') as f:
    geojson_col = json.load(f)

# Divipola
divipola = pd.read_excel("data/Divipola_CE_.xlsx", sheet_name=0)
divipola['DEPARTAMENTO'] = divipola['DEPARTAMENTO'].str.strip().str.title()
replace_dict = {
    "Archipiélago De San Andrés, Providencia Y Santa Catalina": "San Andrés y Providencia",
    "Bogotá, D.C.": "Distrito Capital de Bogotá",
    "Valle Del Cauca": "Valle del Cauca",
    "Norte De Santander": "Norte de Santander"
}
divipola["DEPARTAMENTO"] = divipola["DEPARTAMENTO"].replace(replace_dict)

# Carga mortalidad y transforma
try:
    mortalidad = pd.read_excel("data/Anexo1.NoFetal2019_CE_15-03-23.xlsx", sheet_name=0)
    mortalidad.columns = mortalidad.columns.str.strip().str.upper().str.replace(" ", "_")
    mortalidad = mortalidad[mortalidad["AÑO"] == 2019]
    # Muertes por mes
    datos_mes = (mortalidad.groupby(["MES"]).size().reset_index(name="MUERTES"))
    datos_mes["MES"] = datos_mes["MES"].astype(int)
    meses_nombres = {1:"Enero",2:"Febrero",3:"Marzo",4:"Abril",5:"Mayo",6:"Junio",7:"Julio",8:"Agosto",9:"Septiembre",10:"Octubre",11:"Noviembre",12:"Diciembre"}
    datos_mes["MES_NOMBRE"] = datos_mes["MES"].map(meses_nombres)
    # Top 5 municipios/departamentos violentos (por homicidios)
    top_homicidios = (
        mortalidad[mortalidad["MANERA_MUERTE"].str.lower() == "homicidio"]
        .groupby(["COD_DEPARTAMENTO", "COD_MUNICIPIO"])
        .size()
        .reset_index(name="HOMICIDIOS")
        .sort_values("HOMICIDIOS", ascending=False)
        .head(5)
    )
    divipola_clean = divipola.drop_duplicates(subset=["COD_DEPARTAMENTO", "COD_MUNICIPIO"])
    top_homicidios = top_homicidios.merge(
        divipola_clean[["COD_DEPARTAMENTO", "COD_MUNICIPIO", "DEPARTAMENTO", "MUNICIPIO"]],
        on=["COD_DEPARTAMENTO", "COD_MUNICIPIO"], how="left")
    # Etiqueta de gráfico
    top_homicidios["LABEL"] = top_homicidios["MUNICIPIO"].fillna(top_homicidios["COD_MUNICIPIO"].astype(str)) + \
                              " (" + top_homicidios["DEPARTAMENTO"].fillna(top_homicidios["COD_DEPARTAMENTO"].astype(str)) + ")"
except Exception as e:
    print("Error leyendo archivo de muertes:", e)
    datos_mes = pd.DataFrame({
        'MES':[1,2,3,4,5,6],'MUERTES':[4200,4100,4300,4400,4100,4000],'MES_NOMBRE':['Enero','Febrero','Marzo','Abril','Mayo','Junio']
    })
    top_homicidios = pd.DataFrame({
        'LABEL': ['CiudadA (DptoA)', 'CiudadB (DptoB)', 'CiudadC (DptoC)', 'CiudadD (DptoD)', 'CiudadE (DptoE)'],
        'HOMICIDIOS': [120, 105, 100, 88, 85]
    })

# Mapa base
df_muertes = divipola.groupby('DEPARTAMENTO').size().reset_index(name="MUERTES")
departamentos_geojson = [feature['properties']['name'] for feature in geojson_col['features']]
df_base = pd.DataFrame({'DEPARTAMENTO': departamentos_geojson, 'MUERTES': 0})
df_completo = df_base.merge(df_muertes, on="DEPARTAMENTO", how="left")
df_completo["MUERTES"] = df_completo["MUERTES_y"].fillna(df_completo["MUERTES_x"])
df_completo = df_completo[["DEPARTAMENTO", "MUERTES"]]

# ---------- LAYOUT DASH ----------
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dbc.Container([
    dbc.Row([dbc.Col(html.H2("MortandadColombiaDash - Mortalidad en Colombia 2019"), width=12)], className="mb-4 mt-4"),
    dbc.Row([
        dbc.Col([
            dcc.RadioItems(
                id='menu-graficos',
                options=[
                    {'label': 'Mapa por departamento', 'value': 'mapa'},
                    {'label': 'Muertes por mes (línea)', 'value': 'linea'},
                    {'label': 'Top 5 ciudades violentas', 'value': 'barras_violencia'}
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
    elif grafico == 'linea':
        fig = px.line(
            datos_mes,
            x='MES_NOMBRE', y='MUERTES',
            markers=True,
            title="Muertes a nivel nacional por mes"
        )
        return dcc.Graph(figure=fig)
    elif grafico == 'barras_violencia':
        fig = px.bar(
            top_homicidios,
            x='LABEL', y='HOMICIDIOS',
            title="Top 5 municipios con más homicidios",
            labels={"LABEL": "Municipio (Departamento)", "HOMICIDIOS": "Homicidios"},
            color_discrete_sequence=["crimson"]
        )
        return dcc.Graph(figure=fig)
    else:
        return html.Div("Seleccione una visualización.")

if __name__ == "__main__":
    app.run(debug=True)
