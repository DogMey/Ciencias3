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
    {
        "codigo": """int n = 5;
while (n > 0) {
    n = n - 1;
}
""",
        "descripcion": "Bucle while simple",
        "salida_esperada_tokens": [
            ('KEYWORD', 'int'),
            ('IDENTIFIER', 'n'),
            ('OPERATOR', '='),
            ('NUMBER', '5'),
            ('SEMICOLON', ';'),
            ('KEYWORD', 'while'),
            ('LPAREN', '('),
            ('IDENTIFIER', 'n'),
            ('GREATER', '>'),
            ('NUMBER', '0'),
            ('RPAREN', ')'),
            ('LBRACE', '{'),
            ('IDENTIFIER', 'n'),
            ('OPERATOR', '='),
            ('IDENTIFIER', 'n'),
            ('OPERATOR', '-'),
            ('NUMBER', '1'),
            ('SEMICOLON', ';'),
            ('RBRACE', '}')
        ],
        "salida_esperada_ast": [
            ('DECLARATION', 'int', 'n', 5),
            ('WHILE', ('>', 'n', 0), [
                ('ASSIGNMENT', 'n', ('-', 'n', 1))
            ])
        ]
    },
    {
        "codigo": """int a = 1;
int b = 2;
int c = 3;
        """,
        "descripcion": "Declaraciones múltiples",
        "salida_esperada_tokens": [
            ('KEYWORD', 'int'),
            ('IDENTIFIER', 'a'),
            ('OPERATOR', '='),
            ('NUMBER', '1'),
            ('SEMICOLON', ';'),
            ('KEYWORD', 'int'),
            ('IDENTIFIER', 'b'),
            ('OPERATOR', '='),
            ('NUMBER', '2'),
            ('SEMICOLON', ';'),
            ('KEYWORD', 'int'),
            ('IDENTIFIER', 'c'),
            ('OPERATOR', '='),
            ('NUMBER', '3'),
            ('SEMICOLON', ';')
        ],
        "salida_esperada_ast": [
            ('DECLARATION', 'int', 'a', 1),
            ('DECLARATION', 'int', 'b', 2),
            ('DECLARATION', 'int', 'c', 3)
        ]
    },
    {
        "codigo": """func int suma(int a, int b) {
    return a + b;
}
int resultado = suma(2, 3);
""",
        "descripcion": "Declaración e invocación de función simple",
        "salida_esperada_tokens": [
            ('KEYWORD', 'func'),
            ('KEYWORD', 'int'),
            ('IDENTIFIER', 'suma'),
            ('LPAREN', '('),
            ('KEYWORD', 'int'),
            ('IDENTIFIER', 'a'),
            ('COMMA', ','),
            ('KEYWORD', 'int'),
            ('IDENTIFIER', 'b'),
            ('RPAREN', ')'),
            ('LBRACE', '{'),
            ('KEYWORD', 'return'),
            ('IDENTIFIER', 'a'),
            ('OPERATOR', '+'),
            ('IDENTIFIER', 'b'),
            ('SEMICOLON', ';'),
            ('RBRACE', '}'),
            ('KEYWORD', 'int'),
            ('IDENTIFIER', 'resultado'),
            ('OPERATOR', '='),
            ('IDENTIFIER', 'suma'),
            ('LPAREN', '('),
            ('NUMBER', '2'),
            ('COMMA', ','),
            ('NUMBER', '3'),
            ('RPAREN', ')'),
            ('SEMICOLON', ';')
        ],
        "salida_esperada_ast": [
            ('FUNC_DECL', 'suma', [('int', 'a'), ('int', 'b')], 'int', [
                ('RETURN', ('+', 'a', 'b'))
            ]),
            ('DECLARATION', 'int', 'resultado', ('FUNC_CALL', 'suma', [2, 3]))
        ]
    },
    {
        "codigo": """func void hola() {
    print(1);
}
hola();
        """,
        "descripcion": "Función sin parámetros y sin retorno, y llamada a la función",
        "salida_esperada_tokens": [
            ('KEYWORD', 'func'),
            ('KEYWORD', 'void'),
            ('IDENTIFIER', 'hola'),
            ('LPAREN', '('),
            ('RPAREN', ')'),
            ('LBRACE', '{'),
            ('IDENTIFIER', 'print'),
            ('LPAREN', '('),
            ('NUMBER', '1'),
            ('RPAREN', ')'),
            ('SEMICOLON', ';'),
            ('RBRACE', '}'),
            ('IDENTIFIER', 'hola'),
            ('LPAREN', '('),
            ('RPAREN', ')'),
            ('SEMICOLON', ';')
        ],
        "salida_esperada_ast": [
            ('FUNC_DECL', 'hola', [], 'void', [
                ('FUNC_CALL', 'print', [1])
            ]),
            ('FUNC_CALL', 'hola', [])
        ]
    }
]