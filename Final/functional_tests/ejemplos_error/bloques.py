EJEMPLOS_ERROR_BLOQUES = [
    # Variable fuera de alcance
    {
        "codigo": """
if (2 > 1)
{
    int x = 1;
}
x = 2;
        """,
        "descripcion": "Uso de variable fuera de su bloque",
        "salida_esperada_semantica": "Error: Variable 'x' no declarada"
    },
    # Shadowing ilegal (si el lenguaje lo prohíbe en ciertos casos)
    {
        "codigo": """
int x = 1;
while (2 > 1)
{
    int x = 2;
    int x = 3;
}
        """,
        "descripcion": "Redeclaración en bloque anidado",
        "salida_esperada_semantica": "Error: Variable 'x' ya declarada en este ámbito"
    },
    # Aplicación incorrecta de condición con variable no declarada
    {
        "codigo": """
if (\"texto\") {
    int x = 5;
}
    """,
        "descripcion": "Aplicación incorrecta de condición con variable no declarada",
        "salida_esperada_semantica": "la condición del IF debe ser una expresión booleana, se encontró 'string'"
    },
]
