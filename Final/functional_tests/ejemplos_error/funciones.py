EJEMPLOS_ERROR_FUNCIONES = [
    # Llamada inválida a función sumar con aridad incorrecta
    {
        "codigo": "func int sumar(int a, int b) { return a + b; } sumar(2);",
        "descripcion": "Llamada inválida a función sumar con aridad incorrecta",
        "salida_esperada_semantica": "Aridad incorrecta en 'sumar'"
    },
    # Intento de modificar una constante
    {
        "codigo": "const PI = 3.14; PI = 3.1416;",
        "descripcion": "Intento de modificar una constante",
        "salida_esperada_semantica": "Error semántico: no se puede modificar la constante 'PI'."
    },
    # Llamada a función no declarada
    {
        "codigo": "int x = f(2);",
        "descripcion": "Llamada a función no declarada",
        "salida_esperada_semantica": "Error: Función 'f' no declarada"
    },
    # Return fuera de función
    {
        "codigo": "return 1;",
        "descripcion": "Return fuera de función",
        "salida_esperada_semantica": "Error: 'return' fuera de función"
    },
]
