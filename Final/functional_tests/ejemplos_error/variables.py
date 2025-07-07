EJEMPLOS_ERROR_VARIABLES = [
    # Uso antes de declarar
    {
        "codigo": "print(x);",
        "descripcion": "Uso de variable no declarada",
        "salida_esperada_semantica": "Error semántico: la variable 'x' no ha sido declarada."
    },
    # Redeclaración en mismo ámbito
    {
        "codigo": """
int x = 1;
int x = 2;
        """,
        "descripcion": "Redeclaración de variable en mismo ámbito",
        "salida_esperada_semantica": "Error: Variable 'x' ya declarada en este ámbito"
    },
    # Asignación inválida de cadena a variable entera
    {
        "codigo": "int x = \"hola\";",
        "descripcion": "Asignación inválida de cadena a variable entera",
        "salida_esperada_semantica": "Error semántico: no se puede asignar un valor de tipo 'string' a una variable de tipo 'int'."
    },
    # Asignación inválida de suma de string y entero a variable entera
    {
        "codigo": "int x = \"5\" + 2;",
        "descripcion": "Asignación inválida de suma de string y entero a variable entera",
        "salida_esperada_semantica": "Error semántico: no se puede operar entre 'string' y tipo numérico sin conversión explícita."
    },
    # Uso de variable no inicializada
    {
        "codigo": "x = x + 1;",
        "descripcion": "Uso de variable no inicializada",
        "salida_esperada_semantica": "Error semántico: la variable 'x' no ha sido declarada."
    },
    # Declaración inválida de variable: identificador no puede comenzar con un número
    {
        "codigo": "int 2edad;",
        "descripcion": "Declaración inválida de variable: identificador no puede comenzar con un número",
        "salida_esperada_semantica": "Error en línea 1, columna 5: se esperaba identificador, pero se encontró '2'"
    },
    # Declaración de variable no utilizada
    {
        "codigo": "int x = 0;",
        "descripcion": "Declaración de variable no utilizada",
        "salida_esperada_semantica": "Advertencia: la variable 'x' fue declarada pero nunca utilizada."
    },
]
