import plotly.express as px

def get_fig(datos_mes):
    fig = px.line(
        datos_mes,
        x='MES_NOMBRE', y='MUERTES',
        markers=True,
        title="<b style='color:#C62828;'>Evolución mensual de muertes (2019)</b>",
        line_shape="linear"
    )
    fig.update_traces(line_color="#ef5350", marker_color="#ef5350", marker_size=9)
    fig.update_layout(
        font_family="Montserrat",
        font_color="#5d1e1e",
        plot_bgcolor="#fff",
        xaxis_title="Mes",
        yaxis_title="Número de muertes"
    )
    return fig
