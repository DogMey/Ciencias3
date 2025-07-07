EJEMPLOS = [
    {
        "codigo": 'int x = 5;',
        "descripcion": "Declaración simple de variable entera",
        "salida_esperada_tokens": [
            ('KEYWORD', 'int'),
            ('IDENTIFIER', 'x'),
            ('OPERATOR', '='),
            ('NUMBER', '5'),
            ('SEMICOLON', ';')
        ],
        "salida_esperada_ast": [
            ('DECLARATION', 'int', 'x', 5)
        ]
    },
    {
        "codigo": 'if (a > 2) { b = 1; }',
        "descripcion": "Estructura condicional simple",
        "salida_esperada_tokens": [
            ('KEYWORD', 'if'),
            ('LPAREN', '('),
            ('IDENTIFIER', 'a'),
            ('GREATER', '>'),
            ('NUMBER', '2'),
            ('RPAREN', ')'),
            ('LBRACE', '{'),
            ('IDENTIFIER', 'b'),
            ('OPERATOR', '='),
            ('NUMBER', '1'),
            ('SEMICOLON', ';'),
            ('RBRACE', '}')
        ],
        "salida_esperada_ast": [
            ('IF', ('>', 'a', 2), [
                ('ASSIGNMENT', 'b', 1)
            ])
        ]
    },
    {
        "codigo": """int y = 10;
if (y < 20) 
{ 
    x = y; 
}
        """,
        "descripcion": "Estructura condicional con variable",
        "salida_esperada_tokens": [
            ('KEYWORD', 'int'),
            ('IDENTIFIER', 'y'),
            ('OPERATOR', '='),
            ('NUMBER', '10'),
            ('SEMICOLON', ';'),
            ('KEYWORD', 'if'),
            ('LPAREN', '('),
            ('IDENTIFIER', 'y'),
            ('LESS', '<'),
            ('NUMBER', '20'),
            ('RPAREN', ')'),
            ('LBRACE', '{'),
            ('IDENTIFIER', 'x'),
            ('OPERATOR', '='),
            ('IDENTIFIER', 'y'),
            ('SEMICOLON', ';'),
            ('RBRACE', '}')
        ],
        "salida_esperada_ast": [
            ('DECLARATION', 'int', 'y', 10),
            ('IF', ('<', 'y', 20), [
                ('ASSIGNMENT', 'x', 'y')
            ])
        ]
    },
    {
        "codigo": """int z = 3;
if (z == 3)
{
    z = z + 1;
}
        """,
        "descripcion": "Estructura condicional con comparación",
        "salida_esperada_tokens": [
            ('KEYWORD', 'int'),
            ('IDENTIFIER', 'z'),
            ('OPERATOR', '='),
            ('NUMBER', '3'),
            ('SEMICOLON', ';'),
            ('KEYWORD', 'if'),
            ('LPAREN', '('),
            ('IDENTIFIER', 'z'),
            ('EQUALS', '=='),
            ('NUMBER', '3'),
            ('RPAREN', ')'),
            ('LBRACE', '{'),
            ('IDENTIFIER', 'z'),
            ('OPERATOR', '='),
            ('IDENTIFIER', 'z'),
            ('OPERATOR', '+'),
            ('NUMBER', '1'),
            ('SEMICOLON', ';'),
            ('RBRACE', '}')
        ],
        "salida_esperada_ast": [
            ('DECLARATION', 'int', 'z', 3),
            ('IF', ('==', 'z', 3), [
                ('ASSIGNMENT', 'z', ('+', 'z', 1))
            ])
        ]
    },
    {        "codigo": """for (int i = 0; i < 10; i++) {
    print(i);
}""",
        "descripcion": "Bucle for simple",
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
            ('NUMBER', '10'),
            ('SEMICOLON', ';'),
            ('IDENTIFIER', 'i'),
            ('INCREMENT', '++'),
            ('RPAREN', ')'),
            ('LBRACE', '{'),
            ('IDENTIFIER', 'print'),
            ('LPAREN', '('),
            ('IDENTIFIER', 'i'),
            ('RPAREN', ')'),
            ('SEMICOLON', ';'),
            ('RBRACE', '}')
        ],
        "salida_esperada_ast": [
            ('FOR',
                ('DECLARATION', 'int', 'i', 0),   # inicialización
                ('<', 'i', 10),                   # condición
                ('INCREMENT', 'i'),               # incremento
                [
                    ('FUNC_CALL', 'print', ['i']) # cuerpo
                ]
            )
        ]
    },
]