import dash
import os
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from modules.loader import load_all_data
from modules.plots.map_departamento import get_fig as get_mapa_fig
from modules.plots.line_muertes_mes import get_fig as get_linea_fig
from modules.plots.barras_violencia import get_fig as get_violencia_fig
from modules.plots.circular_menor_mortalidad import get_fig as get_circular_fig
from modules.plots.tabla_causas import get_table as get_tabla_causas
from modules.plots.barras_sexo_dep import get_fig as get_sexo_fig
from modules.plots.hist_edad import get_fig as get_hist_edad_fig

data = load_all_data()
max_muertes = int(data["muertes_mun"]["MUERTES"].max())
puntos_control = [1, 5000, 10000, 20000, max_muertes]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1("Dashboard Mortalidad en Colombia", style={
                    "fontWeight": 900,
                    "fontSize": "2.2rem",
                    "color": "#E57373"
                }),
                html.P("Análisis interactivo de mortalidad en Colombia 2019", className="lead",
                    style={"fontWeight":"bold", "color": "#B71C1C", "fontSize":"1.2rem"})
            ], className="main-header", style={
                "background": "#fff",
                "borderBottom": "3px solid #E57373",
                "paddingBottom": "0.5rem",
                "marginBottom":"1.4rem"
            }),
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H5("Visualizaciones", style={"color": "#B71C1C", "fontWeight":"bold"}),
                dcc.RadioItems(
                    id='menu-graficos',
                    options=[
                        {'label': ' 🗺️ Mapa por departamento', 'value': 'mapa'},
                        {'label': ' 📈 Muertes por mes', 'value': 'linea'},
                        {'label': ' ⚔️ Top ciudades violentas', 'value': 'barras_violencia'},
                        {'label': ' 🏙️ Menor mortalidad', 'value': 'circular'},
                        {'label': ' 📋 Causas principales', 'value': 'tabla_causas'},
                        {'label': ' ♀♂ Sexo/departamento', 'value': 'sexo_dep'},
                        {'label': ' 👶🧓 Grupos de edad', 'value': 'hist_edad'},
                    ],
                    value='mapa',
                    style={"fontSize": "1.03rem"},
                    inputStyle={"marginRight": "8px", "marginLeft": "1.1rem"}
                ),
                html.Div([
                    html.Div([
                        html.Label("Umbral mínimo de muertes:", style={"fontWeight":"bold", "color": "#B71C1C"}),
                        dcc.Slider(
                            id='slider-umbral',
                            min=1,
                            max=max_muertes,
                            step=1,
                            value=2,
                            marks={v: str(v) for v in puntos_control},
                            tooltip={"placement": "bottom", "always_visible": False}
                        ),
                        dcc.Input(
                            id="input-umbral",
                            type="number",
                            value=2,
                            min=1,
                            max=max_muertes,
                            style={"marginLeft":"14px","width":"85px"}
                        ),
                        html.Span(id="umbral-actual", style={"marginLeft":"18px", "color":"#C62828","fontWeight":"bold"}),
                    ], id="controles-circular", style={"marginTop":"0.5rem","marginBottom":"1.5rem", "display":"none"})
                ], id='controles-adicionales')
            ], className="sidebar-menu"),
        ], xs=12, sm=12, md=4, lg=3),
        dbc.Col([
            html.Div(id='contenido-principal', className="content-card")
        ], xs=12, sm=12, md=8, lg=9)
    ])
], fluid=True, style={"background": "#fff8f6", "minHeight": "100vh"})

# Mostrar controles del circular solo cuando se requiere
@app.callback(
    Output('controles-circular', 'style'),
    Input('menu-graficos', 'value')
)
def hide_show_controls(viz):
    if viz == "circular":
        return {"marginTop":"0.5rem","marginBottom":"1.5rem"}
    return {"display": "none"}

# Sincronía slider/input y actualización de gráfico y texto
@app.callback(
    Output('contenido-principal', 'children'),
    Output('slider-umbral', 'value'),
    Output('input-umbral', 'value'),
    Output('umbral-actual', 'children'),
    Input('menu-graficos', 'value'),
    Input('slider-umbral', 'value'),
    Input('input-umbral', 'value')
)
def actualizar_contenido(viz, slider_value, input_value):
    # Valor seguro de umbral
    umbral = slider_value if slider_value is not None else input_value if input_value is not None else 2
    umbral = int(max(1, min(umbral, max_muertes)))
    # --- Circular ---
    if viz == "circular":
        fig = get_circular_fig(data['muertes_mun'], umbral=umbral)
        box = dcc.Graph(figure=fig, style={"height": "450px"})
        return box, umbral, umbral, f"Actual: {umbral}"
    # --- Mapa ---
    if viz == "mapa":
        fig = get_mapa_fig(data['df_completo'], data['geojson_col'])
        return dcc.Graph(figure=fig,style={"height": "600px"}), 2, 2, ""
    # --- Línea mensual ---
    if viz == "linea":
        fig = get_linea_fig(data['datos_mes'])
        return dcc.Graph(figure=fig,style={"height": "500px"}), 2, 2, ""
    # --- Barras violencia ---
    if viz == "barras_violencia":
        fig = get_violencia_fig(data['top_homicidios'])
        return dcc.Graph(figure=fig,style={"height": "500px"}), 2, 2, ""
    # --- Tabla causas ---
    if viz == "tabla_causas":
        tabla = get_tabla_causas(data['mortalidad'], data['anexo2'])
        return tabla, 2, 2, ""
    #--- Barras sexo/departamento ---
    if viz == "sexo_dep":
        fig = get_sexo_fig(data['mortalidad'], data['divipola'])
        return dcc.Graph(figure=fig,style={"height": "600px"}), 2, 2, ""
    #--- Histograma grupos de edad ---
    if viz == "hist_edad":
        fig = get_hist_edad_fig(data['mortalidad'])
        return dcc.Graph(figure=fig,style={"height": "500px"}), 2, 2, ""
    # ---
    return html.Div("Seleccione una visualización."), 2, 2, ""

if __name__ == "__main__":
    # Detecta el puerto que Render le asigna automáticamente a la app
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port, debug=True)

