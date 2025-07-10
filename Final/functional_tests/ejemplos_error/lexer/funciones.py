"""
Ejemplos de error para análisis léxico de funciones.
Incluye errores en tokens de declaración de funciones y parámetros.
"""

EJEMPLOS_ERROR_LEXER_FUNCIONES = [
    {
        "codigo": """
func int suma(int a, int b) {
    return a + b@;
}
        """,
        "descripcion": "Error: carácter inválido '@' en return",
        "salida_esperada_lexica": False,
        "error_esperado": "carácter inválido"
    },
    {
        "codigo": """
func int su#ma(int a, int b) {
    return a + b;
}
        """,
        "descripcion": "Error: carácter inválido '#' en nombre de función",
        "salida_esperada_lexica": False,
        "error_esperado": "carácter inválido"
    },
    {
        "codigo": """
func int suma(int a, int b) {
    return a + b;
}€
        """,
        "descripcion": "Error: carácter inválido '€' después de función",
        "salida_esperada_lexica": False,
        "error_esperado": "carácter inválido"
    },
    {
        "codigo": """
func int suma(int a¡, int b) {
    return a + b;
}
        """,
        "descripcion": "Error: carácter inválido '¡' en parámetro",
        "salida_esperada_lexica": False,
        "error_esperado": "carácter inválido"
    },
    {
        "codigo": """
func int suma(int a, int b) {
    return a &+ b;
}
        """,
        "descripcion": "Error: operador inválido '&+' en return",
        "salida_esperada_lexica": False,
        "error_esperado": "operador inválido"
    },
    {
        "codigo": """
func int suma(int a, int b) {
    return a + b;
}
int main() {
    int result = su$ma(5, 3);
}
        """,
        "descripcion": "Error: carácter inválido '$' en llamada a función",
        "salida_esperada_lexica": False,
        "error_esperado": "carácter inválido"
    },
    {
        "codigo": """
func int suma(int a, int b) {
    return a + "b;
}
        """,
        "descripcion": "Error: cadena literal sin cerrar en función",
        "salida_esperada_lexica": False,
        "error_esperado": "cadena sin cerrar"
    }
]
