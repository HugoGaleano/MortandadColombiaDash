import plotly.express as px

def get_fig(top_homicidios):
    fig = px.bar(
        top_homicidios,
        x='LABEL', y='HOMICIDIOS',
        title="<b style='color:#C62828;'>Top 5 municipios con más homicidios</b>",
        labels={"LABEL": "Municipio (Departamento)", "HOMICIDIOS": "Homicidios"},
        color_discrete_sequence=["#e57373"]
    )
    fig.update_layout(
        font_family="Montserrat",
        font_color="#810101",
        plot_bgcolor="#fff",
        xaxis_title="Municipio",
        yaxis_title="N° Homicidios"
    )
    return fig
