from dash import dash_table, html

def get_table(mortalidad, anexo2):
    mortalidad['COD3'] = mortalidad['COD_MUERTE'].astype(str).str[:3]
    mortalidad['COD4'] = mortalidad['COD_MUERTE'].astype(str).str[:4]
    top_causas = (
        mortalidad.groupby(['COD4', 'COD3'])
        .size().reset_index(name='TOTAL')
        .sort_values(by='TOTAL', ascending=False)
        .head(10)
    )
    tabla_10 = top_causas.merge(
        anexo2[['Código de la CIE-10 cuatro caracteres', 'Descripcion  de códigos mortalidad a cuatro caracteres']],
        left_on='COD4', right_on='Código de la CIE-10 cuatro caracteres', how='left'
    )
    tabla_10['Nombre de causa'] = tabla_10['Descripcion  de códigos mortalidad a cuatro caracteres']
    faltantes = tabla_10['Nombre de causa'].isnull()
    if faltantes.any():
        tabla_10.loc[faltantes, 'Nombre de causa'] = tabla_10.loc[faltantes].merge(
            anexo2[['Código de la CIE-10 tres caracteres', 'Descripción  de códigos mortalidad a tres caracteres']],
            left_on='COD3', right_on='Código de la CIE-10 tres caracteres', how='left'
        )['Descripción  de códigos mortalidad a tres caracteres'].values
    tabla_10 = tabla_10[['COD4', 'Nombre de causa', 'TOTAL']]
    tabla_10.rename(columns={'COD4': 'Código CIE-10', 'TOTAL': 'Total de casos'}, inplace=True)
    return html.Div([
        html.H4("Top 10 causas principales de muerte en Colombia (2019)", 
           style={'color': "#B71C1C", 'fontWeight': 'bold', 'marginBottom': '20px'}),
        dash_table.DataTable(
            data=tabla_10.to_dict('records'),
            columns=[
                {'name': 'Código CIE-10', 'id': 'Código CIE-10'},
                {'name': 'Nombre de causa', 'id': 'Nombre de causa'},
                {'name': 'Total de casos', 'id': 'Total de casos'},
            ],
            style_table={'overflowX': 'auto', 'margin': '0 auto', 'maxWidth': '900px'},
            style_cell={'padding': '10px', 'textAlign': 'left', 'fontFamily': 'Montserrat'},
            style_header={'backgroundColor': '#E57373', 'color': 'white', 'fontWeight': 'bold'},
            style_data={'backgroundColor': '#FFF', 'border': '1px solid #f5bdbd'}
        )
    ])
