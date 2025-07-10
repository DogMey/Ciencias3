"""
Ejemplos exitosos para análisis semántico de variables.
Cada ejemplo incluye código fuente y el resultado esperado del análisis semántico.
"""

EJEMPLOS_EXITOSOS_SEMANTIC_VARIABLES = [
    {
        "codigo": """
int x = 5;
x = x + 1;
        """,
        "descripcion": "Declaración y asignación válida - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
int x = 1;
int y = 2;
x = y;
        """,
        "descripcion": "Múltiples declaraciones y asignación entre variables - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
int a = 10;
int b = a - 5;
a = b * 2;
        """,
        "descripcion": "Secuencia de declaraciones y asignaciones con operaciones - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
int x = 0;
x = x + 1;
x = x * 2;
        """,
        "descripcion": "Incremento y multiplicación secuencial - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
float precio = 10.5;
float descuento = 0.15;
float total = precio * descuento;
        """,
        "descripcion": "Declaraciones con números flotantes - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
int contador = 0;
contador = contador + 1;
contador = contador + 1;
contador = contador + 1;
        """,
        "descripcion": "Múltiples asignaciones a la misma variable - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
int numero1 = 100;
int numero2 = 200;
int suma = numero1 + numero2;
int diferencia = numero2 - numero1;
int producto = numero1 * numero2;
        """,
        "descripcion": "Operaciones aritméticas con múltiples variables - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
int base = 5;
int exponente = 2;
int resultado = base * base;
        """,
        "descripcion": "Cálculo de potencia usando multiplicación - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
bool activo = true;
bool inactivo = false;
        """,
        "descripcion": "Declaraciones de variables booleanas - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
int x = 10;
float y = 20.5;
bool z = true;
        """,
        "descripcion": "Declaraciones de diferentes tipos de variables - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
int temp = 25;
temp = temp + 5;
temp = temp - 3;
temp = temp * 2;
temp = temp / 4;
        """,
        "descripcion": "Secuencia de operaciones aritméticas en la misma variable - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
int a = 1;
int b = 2;
int c = 3;
int suma_total = a + b + c;
        """,
        "descripcion": "Suma de múltiples variables - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
float radio = 5.0;
float area = radio * radio * 3.14;
        """,
        "descripcion": "Cálculo de área usando variable y constante - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
int edad = 25;
edad = edad + 1;
bool mayor_edad = true;
        """,
        "descripcion": "Combinación de tipos int y bool - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
int valor_inicial = 100;
int incremento = 10;
int valor_final = valor_inicial + incremento;
valor_inicial = valor_final;
        """,
        "descripcion": "Intercambio de valores entre variables - análisis semántico exitoso",
        "salida_esperada_semantica": True
    }
]
