EJEMPLOS_EXITOSOS_VARIABLES = [
    # Declaración y uso correcto
    {
        "codigo": """
int x = 5;
x = x + 1;
        """,
        "descripcion": "Declaración y asignación válida",
        "salida_esperada_tokens": [
            ("KEYWORD", "int"),
            ("IDENTIFIER", "x"),
            ("OPERATOR", "="),
            ("NUMBER", "5"),
            ("SEMICOLON", ";"),
            ("IDENTIFIER", "x"),
            ("OPERATOR", "="),
            ("IDENTIFIER", "x"),
            ("OPERATOR", "+"),
            ("NUMBER", "1"),
            ("SEMICOLON", ";")
        ],
        "salida_esperada_ast": [
            ("DECLARATION", "int", "x", 5),
            ("ASSIGNMENT", "x", ("+", "x", 1))
        ],
        "salida_esperada_semantica": True
    },
        # Shadowing válido
    {
        "codigo": """
int x = 1;
while (x < 5) {
    int x = 2;
    x = x + 1;
}
""",
        "descripcion": "Shadowing de variable en bloque",
        "salida_esperada_tokens": [
            ("KEYWORD", "int"),
            ("IDENTIFIER", "x"),
            ("OPERATOR", "="),
            ("NUMBER", "1"),
            ("SEMICOLON", ";"),
            ("KEYWORD", "while"),
            ("LPAREN", "("),
            ("IDENTIFIER", "x"),
            ("LESS", "<"),
            ("NUMBER", "5"),
            ("RPAREN", ")"),
            ("LBRACE", "{"),
            ("KEYWORD", "int"),
            ("IDENTIFIER", "x"),
            ("OPERATOR", "="),
            ("NUMBER", "2"),
            ("SEMICOLON", ";"),
            ("IDENTIFIER", "x"),
            ("OPERATOR", "="),
            ("IDENTIFIER", "x"),
            ("OPERATOR", "+"),
            ("NUMBER", "1"),
            ("SEMICOLON", ";"),
            ("RBRACE", "}")
        ],
        "salida_esperada_ast": [
            ("DECLARATION", "int", "x", 1),
            ("WHILE", ("<", "x", 5), [
                ("DECLARATION", "int", "x", 2),
                ("ASSIGNMENT", "x", ("+", "x", 1))
            ])
        ],
        "salida_esperada_semantica": True
    },
    # Uso de variable en bloque
    {
        "codigo": """
int x = 1;
if (x > 0) {
    x = 2;
}
        """,
        "descripcion": "Uso de variable global en bloque",
        "salida_esperada_tokens": [
            ("KEYWORD", "int"),
            ("IDENTIFIER", "x"),
            ("OPERATOR", "="),
            ("NUMBER", "1"),
            ("SEMICOLON", ";"),
            ("KEYWORD", "if"),
            ("LPAREN", "("),
            ("IDENTIFIER", "x"),
            ("GREATER", ">"),
            ("NUMBER", "0"),
            ("RPAREN", ")"),
            ("LBRACE", "{"),
            ("IDENTIFIER", "x"),
            ("OPERATOR", "="),
            ("NUMBER", "2"),
            ("SEMICOLON", ";"),
            ("RBRACE", "}")
        ],
        "salida_esperada_ast": [
            ("DECLARATION", "int", "x", 1),
            ("IF", (">", "x", 0), [
                ("ASSIGNMENT", "x", 2)
            ])
        ],
        "salida_esperada_semantica": True
    },
]
