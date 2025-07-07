EJEMPLOS_EXITOSOS_FUNCIONES = [
    # Declaración y llamada correcta
    {
        "codigo": "int f(int a) { return a + 1; } int x = f(2);",
        "descripcion": "Declaración y llamada de función válida",
        "salida_esperada_semantica": "OK"
    },
    # Función sin parámetros
    {
        "codigo": "int f() { return 1; } int x = f();",
        "descripcion": "Función sin parámetros",
        "salida_esperada_semantica": "OK"
    },
    # Recursión simple
    {
        "codigo": "int f(int n) { if (n < 1) return 1; else return f(n-1); } int x = f(3);",
        "descripcion": "Función recursiva válida",
        "salida_esperada_semantica": "OK"
    },
]
