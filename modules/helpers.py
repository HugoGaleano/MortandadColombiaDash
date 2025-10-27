# Paleta de colores principal (tonos rojizos)
MAIN_COLOR = "#D73027"      # Rojo principal
ACCENT_COLOR = "#FC8D59"    # Naranja-rojizo para acentos
HEADER_COLOR = "#A50F15"    # Rojo oscuro para headers
LIGHT_RED = "#FEE0D2"       # Rojo muy claro para fondos
DARK_RED = "#67000D"        # Rojo muy oscuro
BG_CARD = "#FDFDFD"         # Fondo tarjetas
TEXT_COLOR = "#2C3E50"      # Texto principal

def get_grupos_edad_map():
    return {
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

def sexo_map():
    return {1: 'Masculino', 2: 'Femenino'}

def get_card_style():
    return {
        "backgroundColor": BG_CARD,
        "borderRadius": "15px",
        "boxShadow": "0 4px 15px rgba(215,48,39,0.1)",
        "padding": "20px",
        "border": f"1px solid {LIGHT_RED}",
        "marginBottom": "20px"
    }
