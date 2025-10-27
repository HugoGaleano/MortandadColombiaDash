import plotly.express as px

def get_fig(muertes_mun, umbral=2):
    filtered = muertes_mun[muertes_mun["MUERTES"] >= umbral]
    ciudades_menor_mortalidad = filtered.sort_values("MUERTES", ascending=True).head(10)
    fig = px.pie(
        ciudades_menor_mortalidad,
        values='MUERTES',
        names='LABEL',
        title="<b style='color:#C62828;'>10 municipios con menor mortalidad</b>",
        color_discrete_sequence=px.colors.sequential.Reds_r
    )
    fig.update_layout(
        font_family="Montserrat",
        font_color="#A50F15",
        plot_bgcolor="#fff"
    )
    return fig
