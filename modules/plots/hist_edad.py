import plotly.express as px
import pandas as pd

def get_fig(mortalidad):
    # Mapas de grupo de edad
    grupos_edad_map = {
        **dict.fromkeys([0,1,2,3,4], 'Mortalidad neonatal'),
        **dict.fromkeys([5,6], 'Mortalidad infantil'),
        **dict.fromkeys([7,8], 'Primera infancia'),
        **dict.fromkeys([9,10], 'Niñez'),
        11: 'Adolescencia',
        **dict.fromkeys([12,13], 'Juventud'),
        **dict.fromkeys([14,15,16], 'Adultez temprana'),
        **dict.fromkeys([17,18,19], 'Adultez intermedia'),
        **dict.fromkeys([20,21,22,23,24], 'Vejez'),
        **dict.fromkeys([25,26,27,28], 'Longevidad / Centenarios'),
        29: 'Edad desconocida'
    }
    edades = mortalidad['GRUPO_EDAD1'].map(grupos_edad_map)
    df_edades = edades.value_counts().reset_index()
    df_edades.columns = ['Grupo de Edad', 'Muertes']
    df_edades = df_edades[df_edades['Grupo de Edad'].notnull()]
    orden = [
        'Mortalidad neonatal', 'Mortalidad infantil', 'Primera infancia', 'Niñez', 'Adolescencia',
        'Juventud', 'Adultez temprana', 'Adultez intermedia', 'Vejez', 'Longevidad / Centenarios', 'Edad desconocida'
    ]
    df_edades['Grupo de Edad'] = pd.Categorical(df_edades['Grupo de Edad'], categories=orden, ordered=True)
    df_edades = df_edades.sort_values('Grupo de Edad')
    fig = px.bar(
        df_edades,
        x='Grupo de Edad',
        y='Muertes',
        title='<b style="color:#B71C1C;">Distribución de muertes por grupos de edad</b>',
        color_discrete_sequence=["#e57373"]
    )
    fig.update_layout(
        font_family="Montserrat",
        font_color="#810101",
        plot_bgcolor="#fff",
        xaxis_tickangle=30,
        xaxis_title="Grupo de edad",
        yaxis_title="Número de muertes"
    )
    return fig
