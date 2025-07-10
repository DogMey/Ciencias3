"""
Ejemplos de error para análisis semántico de funciones.
Incluye errores básicos que el analizador semántico actual puede detectar.
"""

EJEMPLOS_ERROR_SEMANTIC_FUNCIONES = [
    {
        "codigo": """
func int suma(int a, int a) {
    return a + a;
}
        """,
        "descripcion": "Error: parámetros duplicados en función",
        "salida_esperada_semantica": False,
        "error_esperado": "variable 'a' ya fue declarada"
    },
    {
        "codigo": """
func int calcular() {
    int x = 10;
    int x = 20;
    return x;
}
        """,
        "descripcion": "Error: variable redeclarada en función",
        "salida_esperada_semantica": False,
        "error_esperado": "variable 'x' ya fue declarada"
    },
    {
        "codigo": """
func int test() {
    int x = 5;
    y = x + 1;
    return y;
}
        """,
        "descripcion": "Error: asignación a variable no declarada en función",
        "salida_esperada_semantica": False,
        "error_esperado": "variable 'y' no ha sido declarada"
    },
    {
        "codigo": """
func int operacion() {
    int x = 10;
    int z = x + y;
    return z;
}
        """,
        "descripcion": "Error: variable 'y' no declarada en declaración",
        "salida_esperada_semantica": False,
        "error_esperado": "variable 'y' no ha sido declarada"
    },
    {
        "codigo": """
func int simple() {
    result = 42;
    return result;
}
        """,
        "descripcion": "Error: variable 'result' no declarada en función",
        "salida_esperada_semantica": False,
        "error_esperado": "variable 'result' no ha sido declarada"
    },
    {
        "codigo": """
func int suma(int a, int b) {
    int sum = a + b;
    int sum = sum + 1;
    return sum;
}
        """,
        "descripcion": "Error: redeclaración de variable local",
        "salida_esperada_semantica": False,
        "error_esperado": "variable 'sum' ya fue declarada"
    },
    {
        "codigo": """
func int calculo(int x) {
    int result = x * factor;
    return result;
}
        """,
        "descripcion": "Error: variable 'factor' no declarada en función",
        "salida_esperada_semantica": False,
        "error_esperado": "variable 'factor' no ha sido declarada"
    },
    {
        "codigo": """
func int test(int a) {
    int b = 10;
    int c = a + b;
    d = c + 1;
    return d;
}
        """,
        "descripcion": "Error: asignación a variable no declarada 'd'",
        "salida_esperada_semantica": False,
        "error_esperado": "variable 'd' no ha sido declarada"
    },
    {
        "codigo": """
func int multiplicar(int x, int y) {
    int producto = x * y;
    int producto = producto + 1;
    return producto;
}
        """,
        "descripcion": "Error: redeclaración de variable 'producto'",
        "salida_esperada_semantica": False,
        "error_esperado": "variable 'producto' ya fue declarada"
    },
    {
        "codigo": """
func int division(int a, int b) {
    int cociente = a / b;
    int resto = a - cociente * b;
    int resto = resto + 1;
    return resto;
}
        """,
        "descripcion": "Error: redeclaración de variable 'resto'",
        "salida_esperada_semantica": False,
        "error_esperado": "variable 'resto' ya fue declarada"
    }
]
