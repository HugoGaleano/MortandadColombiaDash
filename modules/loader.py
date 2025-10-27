import pandas as pd
import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

def load_all_data():
    path_geojson = os.path.join(DATA_DIR, "colombia_departamentos.geojson")
    path_mortalidad = os.path.join(DATA_DIR, "Anexo1.NoFetal2019_CE_15-03-23.xlsx")
    path_anexo2 = os.path.join(DATA_DIR, "Anexo2.CodigosDeMuerte_CE_15-03-23.xlsx")
    path_divipola = os.path.join(DATA_DIR, "Divipola_CE_.xlsx")
    
    # GeoJSON departamentos (para mapa)
    with open(path_geojson, 'r', encoding='utf-8') as f:
        geojson_col = json.load(f)
    
    # Divipola
    divipola = pd.read_excel(path_divipola)
    divipola['DEPARTAMENTO'] = divipola['DEPARTAMENTO'].str.strip().str.title()
    replace_dict = {
        "Archipiélago De San Andrés, Providencia Y Santa Catalina": "San Andrés y Providencia",
        "Bogotá, D.C.": "Distrito Capital de Bogotá",
        "Valle Del Cauca": "Valle del Cauca",
        "Norte De Santander": "Norte de Santander"
    }
    divipola['DEPARTAMENTO'] = divipola['DEPARTAMENTO'].replace(replace_dict)
    divipola_clean = divipola.drop_duplicates(subset=["COD_DEPARTAMENTO", "COD_MUNICIPIO"])

    # Mortalidad
    mortalidad = pd.read_excel(path_mortalidad)
    mortalidad.columns = mortalidad.columns.str.strip().str.upper().str.replace(" ", "_")
    mortalidad = mortalidad[mortalidad["AÑO"] == 2019]

    # --- Mapa por departamento ---
    muertes_dep = mortalidad.groupby('COD_DEPARTAMENTO').size().reset_index(name='MUERTES')
    departamentos = divipola[['COD_DEPARTAMENTO', 'DEPARTAMENTO']].drop_duplicates()
    df_completo = pd.merge(departamentos, muertes_dep, on="COD_DEPARTAMENTO", how="left")
    df_completo['MUERTES'] = df_completo['MUERTES'].fillna(0)
    
    # --- Línea mensual (evolución) ---
    datos_mes = mortalidad.groupby(["MES"]).size().reset_index(name="MUERTES")
    datos_mes["MES"] = datos_mes["MES"].astype(int)
    meses_nombres = {
        1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio",
        7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"
    }
    datos_mes["MES_NOMBRE"] = datos_mes["MES"].map(meses_nombres)
    
    # --- Barras violencia ---
    top_homicidios = (
        mortalidad[mortalidad["MANERA_MUERTE"].str.lower() == "homicidio"]
        .groupby(["COD_DEPARTAMENTO", "COD_MUNICIPIO"])
        .size().reset_index(name="HOMICIDIOS")
        .sort_values("HOMICIDIOS", ascending=False).head(5)
    )
    top_homicidios = top_homicidios.merge(
        divipola_clean[["COD_DEPARTAMENTO", "COD_MUNICIPIO", "DEPARTAMENTO", "MUNICIPIO"]],
        on=["COD_DEPARTAMENTO", "COD_MUNICIPIO"], how="left"
    )
    top_homicidios["LABEL"] = (
        top_homicidios["MUNICIPIO"].fillna(top_homicidios["COD_MUNICIPIO"].astype(str)) +
        " (" + top_homicidios["DEPARTAMENTO"].fillna(top_homicidios["COD_DEPARTAMENTO"].astype(str)) + ")"
    )
    
    # --- Circular menor mortalidad ---
    muertes_mun = (
        mortalidad.groupby(["COD_DEPARTAMENTO", "COD_MUNICIPIO"])
        .size().reset_index(name="MUERTES")
    )
    muertes_mun = muertes_mun.merge(
        divipola_clean[["COD_DEPARTAMENTO", "COD_MUNICIPIO", "DEPARTAMENTO", "MUNICIPIO"]],
        on=["COD_DEPARTAMENTO", "COD_MUNICIPIO"], how="left"
    )
    muertes_mun["LABEL"] = (
        muertes_mun["MUNICIPIO"].fillna(muertes_mun["COD_MUNICIPIO"].astype(str)) +
        " (" + muertes_mun["DEPARTAMENTO"].fillna(muertes_mun["COD_DEPARTAMENTO"].astype(str)) + ")"
    )

    # --- Anexo2 y tabla causas principales ---
    anexo2 = pd.read_excel(path_anexo2, header=8)
    anexo2.columns = anexo2.columns.str.strip()
    
    # --- Retorno general para todos los módulos ---
    return {
        'geojson_col': geojson_col,
        'df_completo': df_completo,
        'datos_mes': datos_mes,
        'top_homicidios': top_homicidios,
        'muertes_mun': muertes_mun,
        'mortalidad': mortalidad,
        'anexo2': anexo2,
        'divipola': divipola,
        'divipola_clean': divipola_clean,
    }
