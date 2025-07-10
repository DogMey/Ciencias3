"""
Ejemplos de error para análisis léxico de bloques.
Incluye errores en tokens de estructuras de control.
"""

EJEMPLOS_ERROR_LEXER_BLOQUES = [
    {
        "codigo": """
int x = 5;
if (x > 0) @{
    x = x + 1;
}
        """,
        "descripcion": "Error: carácter inválido '@' antes de llave de apertura",
        "salida_esperada_lexica": False,
        "error_esperado": "carácter inválido"
    },
    {
        "codigo": """
int x = 5;
if (x > 0) {
    x = x #+ 1;
}
        """,
        "descripcion": "Error: carácter inválido '#' en expresión dentro de bloque",
        "salida_esperada_lexica": False,
        "error_esperado": "carácter inválido"
    },
    {
        "codigo": """
int x = 5;
wh¡le (x > 0) {
    x = x - 1;
}
        """,
        "descripcion": "Error: carácter inválido '¡' en palabra clave while",
        "salida_esperada_lexica": False,
        "error_esperado": "carácter inválido"
    },
    {
        "codigo": """
int x = 5;
if (x &>= 0) {
    x = x + 1;
} else {
    x = x - 1;
}
        """,
        "descripcion": "Error: operador inválido '&>=' en condición",
        "salida_esperada_lexica": False,
        "error_esperado": "operador inválido"
    },
    {
        "codigo": """
int x = 5;
if (x > 0) {
    x = x + 1;
}€
        """,
        "descripcion": "Error: carácter inválido '€' después de llave de cierre",
        "salida_esperada_lexica": False,
        "error_esperado": "carácter inválido"
    },
    {
        "codigo": """
int x = 5;
if (x != 0) {
    x = x + 1;
}
while (x > 0) {
    x = x - 1¿;
}
        """,
        "descripcion": "Error: carácter inválido '¿' en expresión",
        "salida_esperada_lexica": False,
        "error_esperado": "carácter inválido"
    }
]
