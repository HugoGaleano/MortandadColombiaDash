import plotly.express as px

def get_fig(mortalidad, divipola):
    # Mapea sexo
    sexo_map = {1: 'Masculino', 2: 'Femenino'}
    mortalidad_sexo = mortalidad.merge(
        divipola[['COD_DEPARTAMENTO', 'DEPARTAMENTO']].drop_duplicates(),
        on='COD_DEPARTAMENTO', how='left'
    )
    mortalidad_sexo['SEXO_NOMBRE'] = mortalidad_sexo['SEXO'].map(sexo_map)
    df_plot = (
        mortalidad_sexo
        .groupby(['DEPARTAMENTO', 'SEXO_NOMBRE'])
        .size()
        .reset_index(name='MUERTES')
    )
    fig = px.bar(
        df_plot,
        x='DEPARTAMENTO',
        y='MUERTES',
        color='SEXO_NOMBRE',
        title='<b style="color:#B71C1C;">Muertes por sexo en cada departamento (2019)</b>',
        labels={'DEPARTAMENTO': 'Departamento', 'MUERTES': 'Muertes', 'SEXO_NOMBRE': 'Sexo'},
        barmode='stack',
        color_discrete_map={'Masculino': '#e57373', 'Femenino': '#ffcdd2'}
    )
    fig.update_layout(
        font_family="Montserrat",
        font_color="#810101",
        plot_bgcolor="#fff",
        xaxis_tickangle=45,
        xaxis_title=None,
        yaxis_title="Número de muertes"
    )
    return fig
