EJEMPLOS_EXITOSOS_LEXER_BLOQUES = [
    {
        "codigo": """
if (x > 0) {
    int y = 1;
}
        """,
        "descripcion": "Bloque if con declaración de variable",
        "salida_esperada_tokens": [
            ('KEYWORD', 'if'),
            ('LPAREN', '('),
            ('IDENTIFIER', 'x'),
            ('GREATER', '>'),
            ('NUMBER', '0'),
            ('RPAREN', ')'),
            ('LBRACE', '{'),
            ('KEYWORD', 'int'),
            ('IDENTIFIER', 'y'),
            ('OPERATOR', '='),
            ('NUMBER', '1'),
            ('SEMICOLON', ';'),
            ('RBRACE', '}')
        ]
    },
    {
        "codigo": """
while (i < 10) {
    i = i + 1;
}
        """,
        "descripcion": "Bloque while con incremento",
        "salida_esperada_tokens": [
            ('KEYWORD', 'while'),
            ('LPAREN', '('),
            ('IDENTIFIER', 'i'),
            ('LESS', '<'),
            ('NUMBER', '10'),
            ('RPAREN', ')'),
            ('LBRACE', '{'),
            ('IDENTIFIER', 'i'),
            ('OPERATOR', '='),
            ('IDENTIFIER', 'i'),
            ('OPERATOR', '+'),
            ('NUMBER', '1'),
            ('SEMICOLON', ';'),
            ('RBRACE', '}')
        ]
    },
    {
        "codigo": """
for (int i = 0; i < 5; i = i + 1) {
    int temp = i * 2;
}
        """,
        "descripcion": "Bloque for con declaración e incremento",
        "salida_esperada_tokens": [
            ('KEYWORD', 'for'),
            ('LPAREN', '('),
            ('KEYWORD', 'int'),
            ('IDENTIFIER', 'i'),
            ('OPERATOR', '='),
            ('NUMBER', '0'),
            ('SEMICOLON', ';'),
            ('IDENTIFIER', 'i'),
            ('LESS', '<'),
            ('NUMBER', '5'),
            ('SEMICOLON', ';'),
            ('IDENTIFIER', 'i'),
            ('OPERATOR', '='),
            ('IDENTIFIER', 'i'),
            ('OPERATOR', '+'),
            ('NUMBER', '1'),
            ('RPAREN', ')'),
            ('LBRACE', '{'),
            ('KEYWORD', 'int'),
            ('IDENTIFIER', 'temp'),
            ('OPERATOR', '='),
            ('IDENTIFIER', 'i'),
            ('OPERATOR', '*'),
            ('NUMBER', '2'),
            ('SEMICOLON', ';'),
            ('RBRACE', '}')
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
        "salida_esperada_tokens": [
            ('KEYWORD', 'if'),
            ('LPAREN', '('),
            ('IDENTIFIER', 'a'),
            ('GREATER', '>'),
            ('IDENTIFIER', 'b'),
            ('RPAREN', ')'),
            ('LBRACE', '{'),
            ('KEYWORD', 'while'),
            ('LPAREN', '('),
            ('IDENTIFIER', 'c'),
            ('LESS', '<'),
            ('IDENTIFIER', 'd'),
            ('RPAREN', ')'),
            ('LBRACE', '{'),
            ('IDENTIFIER', 'c'),
            ('OPERATOR', '='),
            ('IDENTIFIER', 'c'),
            ('OPERATOR', '+'),
            ('NUMBER', '1'),
            ('SEMICOLON', ';'),
            ('RBRACE', '}'),
            ('RBRACE', '}')
        ]
    }
]
