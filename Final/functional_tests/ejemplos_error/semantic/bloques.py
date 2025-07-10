"""
Ejemplos de error para análisis semántico de bloques.
Casos donde el análisis semántico debe fallar debido a errores de ámbito y acceso a variables.
"""

EJEMPLOS_ERROR_SEMANTIC_BLOQUES = [
    {
        "codigo": """
if (x > 0) {
    int y = 10;
}
        """,
        "descripcion": "Error: uso de variable no declarada en condición de if",
        "error_esperado": "NameError"
    },
    {
        "codigo": """
int x = 5;
if (x > 0) {
    int y = 10;
}
int z = y + 1;
        """,
        "descripcion": "Error: acceso a variable local fuera de su ámbito",
        "error_esperado": "NameError"
    },
    {
        "codigo": """
int contador = 0;
while (contador < limit) {
    contador = contador + 1;
}
        """,
        "descripcion": "Error: variable no declarada en condición de while",
        "error_esperado": "NameError"
    },
    {
        "codigo": """
int x = 10;
if (x > 5) {
    int temp = 20;
}
int resultado = temp * 2;
        """,
        "descripcion": "Error: uso de variable local después del bloque",
        "error_esperado": "NameError"
    },
    {
        "codigo": """
int x = 5;
if (x > 0) {
    int y = undefined_var + 1;
}
        """,
        "descripcion": "Error: variable no declarada en expresión dentro de bloque",
        "error_esperado": "NameError"
    },
    {
        "codigo": """
while (i < 10) {
    int suma = 0;
    i = i + 1;
}
        """,
        "descripcion": "Error: variable de bucle no declarada",
        "error_esperado": "NameError"
    },
    {
        "codigo": """
int x = 10;
if (x > 5) {
    int y = 20;
    if (y > 15) {
        int z = unknown + 5;
    }
}
        """,
        "descripcion": "Error: variable no declarada en bloque anidado",
        "error_esperado": "NameError"
    },
    {
        "codigo": """
int total = 0;
int i = 0;
while (i < 3) {
    total = total + value;
    i = i + 1;
}
        """,
        "descripcion": "Error: variable no declarada dentro de bucle",
        "error_esperado": "NameError"
    },
    {
        "codigo": """
int x = 5;
if (x > 0) {
    int y = 10;
    if (y > 5) {
        outer_var = 100;
    }
}
        """,
        "descripcion": "Error: asignación a variable no declarada en bloque anidado",
        "error_esperado": "NameError"
    },
    {
        "codigo": """
bool flag = true;
if (flag) {
    int contador = 0;
    while (contador < max) {
        contador = contador + 1;
    }
}
        """,
        "descripcion": "Error: variable no declarada en condición de while anidado",
        "error_esperado": "NameError"
    },
    {
        "codigo": """
int x = 10;
if (x > 5) {
    int y = 20;
}
else {
    int z = y + 10;
}
        """,
        "descripcion": "Error: acceso a variable de bloque if desde bloque else",
        "error_esperado": "NameError"
    },
    {
        "codigo": """
int a = 5;
while (a > 0) {
    int b = 10;
    a = a - 1;
}
int c = b * 2;
        """,
        "descripcion": "Error: uso de variable local de while fuera del bucle",
        "error_esperado": "NameError"
    },
    {
        "codigo": """
if (condition) {
    int result = 100;
}
        """,
        "descripcion": "Error: condición con variable no declarada",
        "error_esperado": "NameError"
    },
    {
        "codigo": """
int x = 10;
if (x > 0) {
    int y = 20;
    if (y > 15) {
        int z = 30;
    }
    int w = z + 5;
}
        """,
        "descripcion": "Error: acceso a variable de bloque anidado desde bloque padre",
        "error_esperado": "NameError"
    },
    {
        "codigo": """
int level = 1;
while (level < 3) {
    if (level == 1) {
        int points = 100;
    }
    int bonus = points * 2;
    level = level + 1;
}
        """,
        "descripcion": "Error: acceso a variable de bloque if desde bloque while padre",
        "error_esperado": "NameError"
    },
    {
        "codigo": """
int x = 5;
if (x > 0) {
    int x = 10;
    int x = 20;
}
        """,
        "descripcion": "Error: redeclaración de variable en el mismo bloque",
        "error_esperado": "ValueError"
    },
    {
        "codigo": """
int global_var = 100;
while (global_var > 0) {
    int local_var = 50;
    int local_var = 25;
    global_var = global_var - 10;
}
        """,
        "descripcion": "Error: redeclaración de variable local en while",
        "error_esperado": "ValueError"
    },
    {
        "codigo": """
int contador = 0;
while (contador < 5) {
    int temp = contador * 2;
    contador = contador + step;
}
        """,
        "descripcion": "Error: variable no declarada en incremento de bucle",
        "error_esperado": "NameError"
    }
]
