"""
Ejemplos de error para análisis léxico de variables.
Incluye errores de tokens, caracteres inválidos y formato incorrecto.
"""

EJEMPLOS_ERROR_LEXER_VARIABLES = [
    {
        "codigo": """
int x = 5@;
        """,
        "descripcion": "Error: carácter inválido '@' en declaración",
        "salida_esperada_lexica": False,
        "error_esperado": "carácter inválido"
    },
    {
        "codigo": """
int x = 10.5.2;
        """,
        "descripcion": "Error: número decimal mal formado",
        "salida_esperada_lexica": False,
        "error_esperado": "número decimal inválido"
    },
    {
        "codigo": """
int x = 'abc';
        """,
        "descripcion": "Error: carácter literal con múltiples caracteres",
        "salida_esperada_lexica": False,
        "error_esperado": "carácter literal inválido"
    },
    {
        "codigo": """
int x = "cadena sin cerrar;
        """,
        "descripcion": "Error: cadena literal sin cerrar",
        "salida_esperada_lexica": False,
        "error_esperado": "cadena literal sin cerrar"
    },
    {
        "codigo": """
int x = 10 $ 5;
        """,
        "descripcion": "Error: operador inválido '$'",
        "salida_esperada_lexica": False,
        "error_esperado": "operador inválido"
    },
    {
        "codigo": """
int x = 10..5;
        """,
        "descripcion": "Error: operador punto doble inválido",
        "salida_esperada_lexica": False,
        "error_esperado": "operador inválido"
    },
    {
        "codigo": """
int x = #invalid;
        """,
        "descripcion": "Error: carácter especial inválido '#'",
        "salida_esperada_lexica": False,
        "error_esperado": "carácter inválido"
    },
    {
        "codigo": """
int variable% = 10;
        """,
        "descripcion": "Error: carácter inválido '%' en identificador",
        "salida_esperada_lexica": False,
        "error_esperado": "identificador inválido"
    }
]
