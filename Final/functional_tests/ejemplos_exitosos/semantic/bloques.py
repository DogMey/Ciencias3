"""
Ejemplos exitosos para análisis semántico de bloques.
Incluye bloques if, if-else, while, for y casos de shadowing y ámbitos anidados.
"""

EJEMPLOS_EXITOSOS_SEMANTIC_BLOQUES = [
    {
        "codigo": """
int x = 5;
if (x > 0) {
    int y = 10;
    x = x + y;
}
        """,
        "descripcion": "Bloque if con variable local - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
int x = 5;
if (x > 0) {
    x = x + 1;
} else {
    x = x - 1;
}
        """,
        "descripcion": "Bloque if-else con modificación de variable externa - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
int contador = 0;
while (contador < 3) {
    contador = contador + 1;
}
        """,
        "descripcion": "Bloque while con modificación de variable externa - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
int x = 10;
if (x > 5) {
    int x = 20;
    x = x + 5;
}
        """,
        "descripcion": "Shadowing - variable local con mismo nombre que externa - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
int suma = 0;
int i = 0;
while (i < 5) {
    suma = suma + i;
    i = i + 1;
}
        """,
        "descripcion": "Bucle while con acumulador - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
int x = 10;
if (x > 5) {
    if (x > 8) {
        int y = 20;
        x = x + y;
    }
}
        """,
        "descripcion": "Bloques if anidados con variable local - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
int nivel = 1;
if (nivel == 1) {
    int puntos = 100;
    if (puntos > 50) {
        int bonus = 25;
        puntos = puntos + bonus;
    }
    nivel = nivel + 1;
}
        """,
        "descripcion": "Múltiples niveles de anidación con variables locales - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
int x = 5;
int y = 10;
if (x < y) {
    int temp = x;
    x = y;
    y = temp;
}
        """,
        "descripcion": "Intercambio de variables con variable temporal local - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
bool activo = true;
if (activo) {
    int configuracion = 1;
    if (configuracion == 1) {
        int valor = 100;
        configuracion = valor;
    }
}
        """,
        "descripcion": "Bloques anidados con diferentes tipos de variables - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
int n = 5;
while (n > 0) {
    int factorial = 1;
    int i = 1;
    while (i <= n) {
        factorial = factorial * i;
        i = i + 1;
    }
    n = n - 1;
}
        """,
        "descripcion": "Bucles while anidados con variables locales - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
int x = 0;
if (x == 0) {
    int x = 1;
    if (x == 1) {
        int x = 2;
        x = x + 1;
    }
}
        """,
        "descripcion": "Shadowing múltiple en bloques anidados - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
int resultado = 0;
int base = 2;
int exponente = 3;
if (exponente > 0) {
    int temp = 1;
    while (exponente > 0) {
        temp = temp * base;
        exponente = exponente - 1;
    }
    resultado = temp;
}
        """,
        "descripcion": "Cálculo de potencia con bloques anidados - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
int array_size = 3;
int suma = 0;
int i = 0;
while (i < array_size) {
    int elemento = i * 2;
    suma = suma + elemento;
    i = i + 1;
}
        """,
        "descripcion": "Simulación de array con bucle y variable local - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
bool encontrado = false;
int objetivo = 7;
int actual = 1;
while (actual <= 10) {
    if (actual == objetivo) {
        encontrado = true;
        int posicion = actual;
        actual = 11;
    } else {
        actual = actual + 1;
    }
}
        """,
        "descripcion": "Búsqueda con bloques if-else anidados en while - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
int x = 10;
if (x > 0) {
    float y = 5.5;
    if (y > 0.0) {
        bool z = true;
        if (z) {
            int resultado = x + 1;
            x = resultado;
        }
    }
}
        """,
        "descripcion": "Bloques anidados con diferentes tipos de datos - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
int contador = 0;
while (contador < 2) {
    int i = 0;
    while (i < 3) {
        int j = 0;
        while (j < 2) {
            j = j + 1;
        }
        i = i + 1;
    }
    contador = contador + 1;
}
        """,
        "descripcion": "Bucles while triplemente anidados - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
int global_var = 100;
if (global_var > 50) {
    int local_var = 25;
    global_var = global_var - local_var;
    if (global_var > 60) {
        int another_local = 10;
        local_var = local_var + another_local;
        global_var = global_var - another_local;
    }
}
        """,
        "descripcion": "Interacción entre variables globales y locales en bloques anidados - análisis semántico exitoso",
        "salida_esperada_semantica": True
    }
]
