EJEMPLOS_EXITOSOS_PARSER_BLOQUES = [
    {
        "codigo": """
if (x > 0) {
    int y = 1;
}
        """,
        "descripcion": "Bloque if con declaración de variable",
        "salida_esperada_ast": [
            ("IF", (">", "x", 0), [
                ("DECLARATION", "int", "y", 1)
            ])
        ]
    },
    {
        "codigo": """
while (i < 10) {
    i = i + 1;
}
        """,
        "descripcion": "Bloque while con incremento",
        "salida_esperada_ast": [
            ("WHILE", ("<", "i", 10), [
                ("ASSIGNMENT", "i", ("+", "i", 1))
            ])
        ]
    },
    {
        "codigo": """
for (int i = 0; i < 5; i = i + 1) {
    int temp = i * 2;
}
        """,
        "descripcion": "Bloque for con declaración e incremento",
        "salida_esperada_ast": [
            ("FOR", 
                ("DECLARATION", "int", "i", 0),
                ("<", "i", 5),
                ("ASSIGNMENT", "i", ("+", "i", 1)),
                [
                    ("DECLARATION", "int", "temp", ("*", "i", 2))
                ]
            )
        ]
    },
    {
        "codigo": """
if (a > b) {
    while (c < d) {
        c = c + 1;
    }
}
        """,
        "descripcion": "Bloques anidados if con while",
        "salida_esperada_ast": [
            ("IF", (">", "a", "b"), [
                ("WHILE", ("<", "c", "d"), [
                    ("ASSIGNMENT", "c", ("+", "c", 1))
                ])
            ])
        ]
    },
    {
        "codigo": """
int x = 5;
if (x == 5) {
    x = x * 2;
} else {
    x = x + 1;
}
        """,
        "descripcion": "Bloque if-else con operaciones",
        "salida_esperada_ast": [
            ("DECLARATION", "int", "x", 5),
            ("IF_ELSE", 
                ("==", "x", 5),
                [("ASSIGNMENT", "x", ("*", "x", 2))],
                [("ASSIGNMENT", "x", ("+", "x", 1))]
            )
        ]
    },
    {
        "codigo": """
int sum = 0;
for (int i = 1; i <= 3; i = i + 1) {
    sum = sum + i;
}
        """,
        "descripcion": "For loop con acumulador",
        "salida_esperada_ast": [
            ("DECLARATION", "int", "sum", 0),
            ("FOR",
                ("DECLARATION", "int", "i", 1),
                ("<=", "i", 3),
                ("ASSIGNMENT", "i", ("+", "i", 1)),
                [
                    ("ASSIGNMENT", "sum", ("+", "sum", "i"))
                ]
            )
        ]
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
        "descripcion": "Bloque if-else básico",
        "salida_esperada_ast": [
            ("DECLARATION", "int", "x", 5),
            ("IF_ELSE", 
                (">", "x", 0),
                [("ASSIGNMENT", "x", ("+", "x", 1))],
                [("ASSIGNMENT", "x", ("-", "x", 1))]
            )
        ]
    }
]
