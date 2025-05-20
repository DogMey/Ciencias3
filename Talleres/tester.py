from lexer import lexer
from parser import parser

def run_tests(lexer_func, parser_func):
    ejemplos = [
        {
            "codigo": """
            // Declaración con comentario
            int count = 0; // comentario sobre la linea de código
            """,
            "descripcion": "Declaración con comentario al inicio",
            "salida_esperada_tokens": [
                ('IDENTIFIER', 'int'),
                ('IDENTIFIER', 'count'),
                ('OPERATOR', '='),
                ('NUMBER', '0'),
                ('SEMICOLON', ';'),
            ],
            "salida_esperada_ast": [
                ('DECLARATION', 'int', 'count', 0)
            ]
        },
        {
            "codigo": "result = (a + b) * 2;",
            "descripcion": "Expresión con paréntesis y multiplicación",
            "salida_esperada_tokens": [
                ('IDENTIFIER', 'result'),
                ('OPERATOR', '='),
                ('PAREN', '('),
                ('IDENTIFIER', 'a'),
                ('OPERATOR', '+'),
                ('IDENTIFIER', 'b'),
                ('PAREN', ')'),
                ('OPERATOR', '*'),
                ('NUMBER', '2'),
                ('SEMICOLON', ';')
            ],
            "salida_esperada_ast": [
                ('ASSIGNMENT', 'result', ('*', ('+', 'a', 'b'), 2))
            ]
        },
        {
            "codigo": """
            if (a == b) {
                c = 10;
            }
            """,
            "descripcion": "Condicional simple con igualdad y bloque",
            "salida_esperada_tokens": [
                ('IDENTIFIER', 'if'),
                ('PAREN', '('),
                ('IDENTIFIER', 'a'),
                ('EQUALS', '=='),
                ('IDENTIFIER', 'b'),
                ('PAREN', ')'),
                ('BRACE', '{'),
                ('IDENTIFIER', 'c'),
                ('OPERATOR', '='),
                ('NUMBER', '10'),
                ('SEMICOLON', ';'),
                ('BRACE', '}'),
            ],
            "salida_esperada_ast": [
                ('IF', ('==', 'a', 'b'), [
                    ('ASSIGNMENT', 'c', 10)
                ])
            ]
        },
        {
            "codigo": """
            float x = 1.5;
            float y = 2.5;
            float z = x / y;
            """,
            "descripcion": "Declaraciones y expresión con división",
            "salida_esperada_tokens": [
                ('IDENTIFIER', 'float'),
                ('IDENTIFIER', 'x'),
                ('OPERATOR', '='),
                ('NUMBER', '1.5'),
                ('SEMICOLON', ';'),

                ('IDENTIFIER', 'float'),
                ('IDENTIFIER', 'y'),
                ('OPERATOR', '='),
                ('NUMBER', '2.5'),
                ('SEMICOLON', ';'),

                ('IDENTIFIER', 'float'),
                ('IDENTIFIER', 'z'),
                ('OPERATOR', '='),
                ('IDENTIFIER', 'x'),
                ('OPERATOR', '/'),
                ('IDENTIFIER', 'y'),
                ('SEMICOLON', ';')
            ],
            "salida_esperada_ast": [
                ('DECLARATION', 'float', 'x', 1.5),
                ('DECLARATION', 'float', 'y', 2.5),
                ('DECLARATION', 'float', 'z', ('/', 'x', 'y'))
            ]
        },
        {
            "codigo": """
            a = 5;
            b = a - 3;
            c = b * (a + 2);
            """,
            "descripcion": "Asignaciones con diferentes operaciones y paréntesis",
            "salida_esperada_tokens": [
                ('IDENTIFIER', 'a'),
                ('OPERATOR', '='),
                ('NUMBER', '5'),
                ('SEMICOLON', ';'),

                ('IDENTIFIER', 'b'),
                ('OPERATOR', '='),
                ('IDENTIFIER', 'a'),
                ('OPERATOR', '-'),
                ('NUMBER', '3'),
                ('SEMICOLON', ';'),

                ('IDENTIFIER', 'c'),
                ('OPERATOR', '='),
                ('IDENTIFIER', 'b'),
                ('OPERATOR', '*'),
                ('PAREN', '('),
                ('IDENTIFIER', 'a'),
                ('OPERATOR', '+'),
                ('NUMBER', '2'),
                ('PAREN', ')'),
                ('SEMICOLON', ';')
            ],
            "salida_esperada_ast": [
                ('ASSIGNMENT', 'a', 5),
                ('ASSIGNMENT', 'b', ('-', 'a', 3)),
                ('ASSIGNMENT', 'c', ('*', 'b', ('+', 'a', 2)))
            ]
        },

        {
            "codigo": "result = a + b * c - 2 / 4;",
            "descripcion": "Expresión compleja con múltiples operaciones y paréntesis",
            "salida_esperada_tokens": [
                ["IDENTIFIER", "result"],
                ["OPERATOR", "="],
                ["IDENTIFIER", "a"],
                ["OPERATOR", "+"],
                ["IDENTIFIER", "b"],
                ["OPERATOR", "*"],
                ["IDENTIFIER", "c"],
                ["OPERATOR", "-"],
                ["NUMBER", "2"],
                ["OPERATOR", "/"],
                ["NUMBER", "4"],
                ["SEMICOLON", ";"]
            ],
            "salida_esperada_ast": [
                ["ASSIGNMENT", "result",
                    ["-",
                        ["+",
                            "a",
                            ["*", "b", "c"]
                        ],
                        ["/", "2", "4"]
                    ]
                ]
            ]
        },

        {
            "codigo": "int x;",
            "descripcion": "Inicialización de una variable sin asignación de valor",
            "salida_esperada_tokens": [
                ('IDENTIFIER', 'int'),
                ('IDENTIFIER', 'x'),
                ('SEMICOLON', ';')
            ],
            "salida_esperada_ast": [
                ('DECLARATION', 'int', 'x')
            ]
        }



    ]


    for i, ejemplo in enumerate(ejemplos, 1):
        print(f"\n=== Test {i}: {ejemplo['descripcion']} ===")
        print("Código fuente:")
        print(ejemplo['codigo'])
        
        # Análisis Léxico
        try:
            tokens = lexer_func(ejemplo['codigo'])
            print("Tokens obtenidos:")
            print(tokens)
            print("Tokens esperados:")
            print(ejemplo['salida_esperada_tokens'])
        except Exception as e:
            print(f"Error en análisis léxico: {e}")
            continue
        
        # Comprobar tokens (simple comparación)
        if tokens == ejemplo['salida_esperada_tokens']:
            print("Tokens correctos ✔️")
        else:
            print("Tokens incorrectos ❌")
        
        # Análisis Sintáctico
        try:
            ast = parser_func(tokens)
            print("AST obtenido:")
            print(ast)
            print("AST esperado:")
            print(ejemplo['salida_esperada_ast'])
        except Exception as e:
            print(f"Error en análisis sintáctico: {e}")
            print("No se pudo obtener AST.")
            print("AST esperado:")
            print(ejemplo['salida_esperada_ast'])
            print("Test fallido ❌")
            continue

        if ast == ejemplo['salida_esperada_ast']:
            print("AST correcto ✔️")
        else:
            print("AST incorrecto ❌")



if __name__ == "__main__":
    run_tests(lexer, parser)