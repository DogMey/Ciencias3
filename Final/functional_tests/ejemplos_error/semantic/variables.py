"""
Ejemplos de error para análisis semántico de variables.
Casos donde el análisis semántico debe fallar debido a errores semánticos.
"""

EJEMPLOS_ERROR_SEMANTIC_VARIABLES = [
    {
        "codigo": """
int x = 5;
y = x + 1;
        """,
        "descripcion": "Error: asignación a variable no declarada",
        "error_esperado": "NameError"
    },
    {
        "codigo": """
int x = 5;
int x = 10;
        """,
        "descripcion": "Error: redeclaración de variable en el mismo ámbito",
        "error_esperado": "ValueError"
    },
    {
        "codigo": """
x = 10;
        """,
        "descripcion": "Error: asignación a variable no declarada previamente",
        "error_esperado": "NameError"
    },
    {
        "codigo": """
int x = y + 1;
        """,
        "descripcion": "Error: uso de variable no declarada en expresión",
        "error_esperado": "NameError"
    },
    {
        "codigo": """
int x = 5;
z = x + y;
        """,
        "descripcion": "Error: uso de variable no declarada en expresión aritmética",
        "error_esperado": "NameError"
    },
    {
        "codigo": """
int resultado = a * b + c;
        """,
        "descripcion": "Error: múltiples variables no declaradas en expresión",
        "error_esperado": "NameError"
    },
    {
        "codigo": """
int x = 10;
int y = 20;
int x = 30;
        """,
        "descripcion": "Error: redeclaración de variable después de uso",
        "error_esperado": "ValueError"
    },
    {
        "codigo": """
float precio = 10.5;
float precio = 20.0;
        """,
        "descripcion": "Error: redeclaración de variable float",
        "error_esperado": "ValueError"
    },
    {
        "codigo": """
bool activo = true;
bool activo = false;
        """,
        "descripcion": "Error: redeclaración de variable booleana",
        "error_esperado": "ValueError"
    },
    {
        "codigo": """
int x = 5;
y = x;
int y = 10;
        """,
        "descripcion": "Error: uso de variable antes de declararla",
        "error_esperado": "NameError"
    },
    {
        "codigo": """
int suma = a + b + c + d;
        """,
        "descripcion": "Error: múltiples variables no declaradas en suma",
        "error_esperado": "NameError"
    },
    {
        "codigo": """
int x = 10;
resultado = x * 2;
        """,
        "descripcion": "Error: asignación a variable no declarada con expresión válida",
        "error_esperado": "NameError"
    },
    {
        "codigo": """
int base = 5;
int area = base * altura;
        """,
        "descripcion": "Error: uso de variable no declarada en cálculo",
        "error_esperado": "NameError"
    },
    {
        "codigo": """
int x = undefined_var;
        """,
        "descripcion": "Error: declaración con variable no definida",
        "error_esperado": "NameError"
    },
    {
        "codigo": """
int contador = 0;
int contador = contador + 1;
        """,
        "descripcion": "Error: redeclaración con referencia a sí misma",
        "error_esperado": "ValueError"
    }
]
