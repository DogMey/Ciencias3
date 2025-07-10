"""
Ejemplos de error para análisis sintáctico de bloques.
Incluye errores de sintaxis en estructuras de control.
"""

EJEMPLOS_ERROR_PARSER_BLOQUES = [
    {
        "codigo": """
int x = 5;
if x > 0 {
    x = x + 1;
}
        """,
        "descripcion": "Error: falta paréntesis en condición de if",
        "salida_esperada_sintactica": False,
        "error_esperado": "se esperaba '('"
    },
    {
        "codigo": """
int x = 5;
if (x > 0) 
    x = x + 1;
        """,
        "descripcion": "Error: falta llaves en bloque de if",
        "salida_esperada_sintactica": False,
        "error_esperado": "se esperaba '{'"
    },
    {
        "codigo": """
int x = 5;
if (x > 0) {
    x = x + 1;
        """,
        "descripcion": "Error: falta llave de cierre en bloque",
        "salida_esperada_sintactica": False,
        "error_esperado": "se esperaba '}'"
    },
    {
        "codigo": """
int x = 5;
if () {
    x = x + 1;
}
        """,
        "descripcion": "Error: condición vacía en if",
        "salida_esperada_sintactica": False,
        "error_esperado": "condición vacía"
    },
    {
        "codigo": """
int x = 5;
while (x > 0 {
    x = x - 1;
}
        """,
        "descripcion": "Error: falta paréntesis de cierre en while",
        "salida_esperada_sintactica": False,
        "error_esperado": "se esperaba ')'"
    },
    {
        "codigo": """
int x = 5;
if (x > 0) {
    x = x + 1;
} else {
    x = x - 1;
        """,
        "descripcion": "Error: falta llave de cierre en else",
        "salida_esperada_sintactica": False,
        "error_esperado": "se esperaba '}'"
    },
    {
        "codigo": """
int x = 5;
if (x > 0) {
    x = x + 1;
} else if {
    x = x - 1;
}
        """,
        "descripcion": "Error: falta condición en else if",
        "salida_esperada_sintactica": False,
        "error_esperado": "se esperaba condición"
    },
    {
        "codigo": """
int x = 5;
if (x > 0) {
    x = x + 1;
} else if (x < 0) 
    x = x - 1;
}
        """,
        "descripcion": "Error: falta llave de apertura en else if",
        "salida_esperada_sintactica": False,
        "error_esperado": "se esperaba '{'"
    },
    {
        "codigo": """
int x = 5;
while () {
    x = x - 1;
}
        """,
        "descripcion": "Error: condición vacía en while",
        "salida_esperada_sintactica": False,
        "error_esperado": "condición vacía"
    },
    {
        "codigo": """
int x = 5;
if (x > 0) {
    x = x + 1
}
        """,
        "descripcion": "Error: falta punto y coma en statement dentro de bloque",
        "salida_esperada_sintactica": False,
        "error_esperado": "se esperaba ';'"
    }
]
