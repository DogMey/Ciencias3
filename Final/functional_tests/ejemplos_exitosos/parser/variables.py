EJEMPLOS_EXITOSOS_PARSER_VARIABLES = [
    {
        "codigo": """
int x = 5;
x = x + 1;
        """,
        "descripcion": "Declaración y asignación válida",
        "salida_esperada_ast": [
            ("DECLARATION", "int", "x", 5),
            ("ASSIGNMENT", "x", ("+", "x", 1))
        ]
    },
    {
        "codigo": """
int x = 1;
int y = 2;
x = y;
        """,
        "descripcion": "Múltiples declaraciones y asignación entre variables",
        "salida_esperada_ast": [
            ("DECLARATION", "int", "x", 1),
            ("DECLARATION", "int", "y", 2),
            ("ASSIGNMENT", "x", "y")
        ]
    },
    {
        "codigo": """
int resultado = x * 2 + y;
        """,
        "descripcion": "Declaración con expresión aritmética compleja",
        "salida_esperada_ast": [
            ("DECLARATION", "int", "resultado", ("+", ("*", "x", 2), "y"))
        ]
    },
    {
        "codigo": """
int a = 10;
int b = a - 5;
a = b * 2;
        """,
        "descripcion": "Secuencia de declaraciones y asignaciones con operaciones",
        "salida_esperada_ast": [
            ("DECLARATION", "int", "a", 10),
            ("DECLARATION", "int", "b", ("-", "a", 5)),
            ("ASSIGNMENT", "a", ("*", "b", 2))
        ]
    },
    {
        "codigo": """
int x = 0;
x = x + 1;
x = x * 2;
        """,
        "descripcion": "Incremento y multiplicación secuencial",
        "salida_esperada_ast": [
            ("DECLARATION", "int", "x", 0),
            ("ASSIGNMENT", "x", ("+", "x", 1)),
            ("ASSIGNMENT", "x", ("*", "x", 2))
        ]
    }
]
