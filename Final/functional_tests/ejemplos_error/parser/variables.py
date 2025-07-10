"""
Ejemplos de error para análisis sintáctico de variables.
Incluye errores de sintaxis en declaraciones y asignaciones.
"""

EJEMPLOS_ERROR_PARSER_VARIABLES = [
    {
        "codigo": """
int x 5;
        """,
        "descripcion": "Error: falta operador de asignación '=' en declaración",
        "salida_esperada_sintactica": False,
        "error_esperado": "se esperaba '='"
    },
    {
        "codigo": """
int = 5;
        """,
        "descripcion": "Error: falta identificador en declaración",
        "salida_esperada_sintactica": False,
        "error_esperado": "se esperaba identificador"
    },
    {
        "codigo": """
int x = ;
        """,
        "descripcion": "Error: falta valor en asignación",
        "salida_esperada_sintactica": False,
        "error_esperado": "se esperaba expresión"
    },
    {
        "codigo": """
int int x = 5;
        """,
        "descripcion": "Error: tipo duplicado en declaración",
        "salida_esperada_sintactica": False,
        "error_esperado": "se esperaba identificador"
    },
    {
        "codigo": """
int x = 5 + ;
        """,
        "descripcion": "Error: expresión incompleta en asignación",
        "salida_esperada_sintactica": False,
        "error_esperado": "expresión incompleta"
    },
    {
        "codigo": """
int x = 5
        """,
        "descripcion": "Error: falta punto y coma al final",
        "salida_esperada_sintactica": False,
        "error_esperado": "se esperaba ';'"
    },
    {
        "codigo": """
int x = 5 +;
        """,
        "descripcion": "Error: operador sin operando derecho",
        "salida_esperada_sintactica": False,
        "error_esperado": "operando faltante"
    },
    {
        "codigo": """
int x = + 5;
        """,
        "descripcion": "Error: operador sin operando izquierdo",
        "salida_esperada_sintactica": False,
        "error_esperado": "operando faltante"
    },
    {
        "codigo": """
int x = 5 + * 3;
        """,
        "descripcion": "Error: operadores consecutivos sin operando",
        "salida_esperada_sintactica": False,
        "error_esperado": "operadores consecutivos"
    },
    {
        "codigo": """
int x = (5 + 3;
        """,
        "descripcion": "Error: paréntesis sin cerrar en expresión",
        "salida_esperada_sintactica": False,
        "error_esperado": "paréntesis sin cerrar"
    }
]
