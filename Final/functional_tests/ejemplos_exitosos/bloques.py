EJEMPLOS_EXITOSOS_BLOQUES = [
    # If y while válidos
    {
        "codigo": "int x = 0; if (x < 1) { x = 2; }",
        "descripcion": "If con bloque válido",
        "salida_esperada_semantica": "OK"
    },
    {
        "codigo": "int i = 0; while (i < 3) { i = i + 1; }",
        "descripcion": "While con incremento válido",
        "salida_esperada_semantica": "OK"
    },
    {
        "codigo": "int s = 0; for (int i = 0; i < 3; i = i + 1) { s = s + i; }",
        "descripcion": "For con declaración y uso de variable",
        "salida_esperada_semantica": "OK"
    },
]
