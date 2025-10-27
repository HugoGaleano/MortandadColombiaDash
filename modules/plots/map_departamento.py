import plotly.express as px

def get_fig(df_completo, geojson_col):
    fig = px.choropleth(
        df_completo,
        geojson=geojson_col,
        locations='DEPARTAMENTO',
        color='MUERTES',
        featureidkey='properties.name',
        hover_name='DEPARTAMENTO',
        color_continuous_scale='Reds'  # Escala rojiza, de claro a oscuro
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        title="Muertes por departamento en Colombia (2019)",
        font_family="Montserrat",
        margin=dict(l=0, r=0, t=55, b=0)
    )
    return fig
