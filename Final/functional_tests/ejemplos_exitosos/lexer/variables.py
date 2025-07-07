EJEMPLOS_EXITOSOS_LEXER_VARIABLES = [
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
        ]
    },
    {
        "codigo": """
int x = 1;
int x = 2;
x = x + 1;
        """,
        "descripcion": "Shadowing de variable en bloque con while",
        "salida_esperada_tokens": [
            ('KEYWORD', 'int'),
            ('IDENTIFIER', 'x'),
            ('OPERATOR', '='),
            ('NUMBER', '1'),
            ('SEMICOLON', ';'),
            ('KEYWORD', 'int'),
            ('IDENTIFIER', 'x'),
            ('OPERATOR', '='),
            ('NUMBER', '2'),
            ('SEMICOLON', ';'),
            ('IDENTIFIER', 'x'),
            ('OPERATOR', '='),
            ('IDENTIFIER', 'x'),
            ('OPERATOR', '+'),
            ('NUMBER', '1'),
            ('SEMICOLON', ';')
        ]
    },
    {
        "codigo": """
int x = 1;
x = 2;
        """,
        "descripcion": "Uso de variable global en bloque if",
        "salida_esperada_tokens": [
            ('KEYWORD', 'int'),
            ('IDENTIFIER', 'x'),
            ('OPERATOR', '='),
            ('NUMBER', '1'),
            ('SEMICOLON', ';'),
            ('IDENTIFIER', 'x'),
            ('OPERATOR', '='),
            ('NUMBER', '2'),
            ('SEMICOLON', ';')
        ]
    }
]
