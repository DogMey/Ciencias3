"""
Ejemplos de error para análisis sintáctico de funciones.
Incluye errores de sintaxis en declaraciones de funciones y parámetros.
"""

EJEMPLOS_ERROR_PARSER_FUNCIONES = [
    {
        "codigo": """
func suma(int a, int b) {
    return a + b;
}
        """,
        "descripcion": "Error: falta tipo de retorno en función",
        "salida_esperada_sintactica": False,
        "error_esperado": "se esperaba tipo de retorno"
    },
    {
        "codigo": """
func int (int a, int b) {
    return a + b;
}
        """,
        "descripcion": "Error: falta nombre de función",
        "salida_esperada_sintactica": False,
        "error_esperado": "se esperaba nombre de función"
    },
    {
        "codigo": """
func int suma int a, int b) {
    return a + b;
}
        """,
        "descripcion": "Error: falta paréntesis de apertura en parámetros",
        "salida_esperada_sintactica": False,
        "error_esperado": "se esperaba '('"
    },
    {
        "codigo": """
func int suma(int a, int b {
    return a + b;
}
        """,
        "descripcion": "Error: falta paréntesis de cierre en parámetros",
        "salida_esperada_sintactica": False,
        "error_esperado": "se esperaba ')'"
    },
    {
        "codigo": """
func int suma(int a, int b) 
    return a + b;
}
        """,
        "descripcion": "Error: falta llave de apertura en función",
        "salida_esperada_sintactica": False,
        "error_esperado": "se esperaba '{'"
    },
    {
        "codigo": """
func int suma(int a, int b) {
    return a + b;
        """,
        "descripcion": "Error: falta llave de cierre en función",
        "salida_esperada_sintactica": False,
        "error_esperado": "se esperaba '}'"
    },
    {
        "codigo": """
func int suma(int a,) {
    return a;
}
        """,
        "descripcion": "Error: coma al final de lista de parámetros",
        "salida_esperada_sintactica": False,
        "error_esperado": "parámetro esperado después de coma"
    },
    {
        "codigo": """
func int suma(int, int b) {
    return b;
}
        """,
        "descripcion": "Error: falta nombre de parámetro",
        "salida_esperada_sintactica": False,
        "error_esperado": "se esperaba nombre de parámetro"
    },
    {
        "codigo": """
func int suma(a, int b) {
    return a + b;
}
        """,
        "descripcion": "Error: falta tipo de parámetro",
        "salida_esperada_sintactica": False,
        "error_esperado": "se esperaba tipo de parámetro"
    },
    {
        "codigo": """
func int suma(int a int b) {
    return a + b;
}
        """,
        "descripcion": "Error: falta coma entre parámetros",
        "salida_esperada_sintactica": False,
        "error_esperado": "se esperaba ','"
    },
    {
        "codigo": """
func int suma(int a, int b) {
    return a + b
}
        """,
        "descripcion": "Error: falta punto y coma después de return",
        "salida_esperada_sintactica": False,
        "error_esperado": "se esperaba ';'"
    },
    {
        "codigo": """
func int suma(int a, int b) {
    return return a + b;
}
        """,
        "descripcion": "Error: return duplicado",
        "salida_esperada_sintactica": False,
        "error_esperado": "token inesperado"
    }
]
