from lexer import lexer
from parser import parser

def run_tests(lexer_func, parser_func):
    ejemplos = [
        # Ejemplo 1 declaración con comentario al inicio
        {
            "codigo": """
            // Declaración con comentario
            int count = 0; // comentario sobre la linea de código
            """,
            "descripcion": "Declaración con comentario al inicio",
            "salida_esperada_tokens": [
                ('KEYWORD', 'int'),
                ('IDENTIFIER', 'count'),
                ('OPERATOR', '='),
                ('NUMBER', '0'),
                ('SEMICOLON', ';'),
            ],
            "salida_esperada_ast": [
                ('DECLARATION', 'int', 'count', 0)
            ]
        },
        # Ejemplo 2 expresion con paréntesis y multiplicación
        {
            "codigo": "result = (a + b) * 2;",
            "descripcion": "Expresión con paréntesis y multiplicación",
            "salida_esperada_tokens": [
                ('IDENTIFIER', 'result'),
                ('OPERATOR', '='),
                ('LPAREN', '('),         
                ('IDENTIFIER', 'a'),
                ('OPERATOR', '+'),
                ('IDENTIFIER', 'b'),
                ('RPAREN', ')'),         
                ('OPERATOR', '*'),
                ('NUMBER', '2'),
                ('SEMICOLON', ';')
            ],
            "salida_esperada_ast": [
                ('ASSIGNMENT', 'result', ('*', ('+', 'a', 'b'), 2))
            ]
        },
        # Ejemplo 3 condicional simple con igualdad y bloque
        {
            "codigo": """
            if (a == b) {
                c = 10;
            }
            """,
            "descripcion": "Condicional simple con igualdad y bloque",
            "salida_esperada_tokens": [
                ('KEYWORD', 'if'),
                ('LPAREN', '('),
                ('IDENTIFIER', 'a'),
                ('EQUALS', '=='),
                ('IDENTIFIER', 'b'),
                ('RPAREN', ')'),
                ('LBRACE', '{'),
                ('IDENTIFIER', 'c'),
                ('OPERATOR', '='),
                ('NUMBER', '10'),
                ('SEMICOLON', ';'),
                ('RBRACE', '}'),
            ],
            "salida_esperada_ast": [
                ('IF', ('==', 'a', 'b'), [
                    ('ASSIGNMENT', 'c', 10)
                ])
            ]
        },
        # Ejemplo 4 declaración y expresión con división
        {
            "codigo": """
            float x = 1.5;
            float y = 2.5;
            float z = x / y;
            """,
            "descripcion": "Declaraciones y expresión con división",
            "salida_esperada_tokens": [
                ('KEYWORD', 'float'),
                ('IDENTIFIER', 'x'),
                ('OPERATOR', '='),
                ('NUMBER', '1.5'),
                ('SEMICOLON', ';'),

                ('KEYWORD', 'float'),
                ('IDENTIFIER', 'y'),
                ('OPERATOR', '='),
                ('NUMBER', '2.5'),
                ('SEMICOLON', ';'),

                ('KEYWORD', 'float'),
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
        # Ejemplo 5 asignaciones con diferentes operaciones y paréntesis
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
                ('LPAREN', '('),
                ('IDENTIFIER', 'a'),
                ('OPERATOR', '+'),
                ('NUMBER', '2'),
                ('RPAREN', ')'),
                ('SEMICOLON', ';')
            ],
            "salida_esperada_ast": [
                ('ASSIGNMENT', 'a', 5),
                ('ASSIGNMENT', 'b', ('-', 'a', 3)),
                ('ASSIGNMENT', 'c', ('*', 'b', ('+', 'a', 2)))
            ]
        },
        # Ejemplo 6 expresión compleja con múltiples operaciones y paréntesis
        {
            "codigo": "result = a + b * c - 2 / 4;",
            "descripcion": "Expresión compleja con múltiples operaciones y paréntesis",
            "salida_esperada_tokens": [
                ("IDENTIFIER", "result"),
                ("OPERATOR", "="),
                ("IDENTIFIER", "a"),
                ("OPERATOR", "+"),
                ("IDENTIFIER", "b"),
                ("OPERATOR", "*"),
                ("IDENTIFIER", "c"),
                ("OPERATOR", "-"),
                ("NUMBER", "2"),
                ("OPERATOR", "/"),
                ("NUMBER", "4"),
                ("SEMICOLON", ";")
            ],

            "salida_esperada_ast": [
                ('ASSIGNMENT', 'result',
                    ('-',
                        ('+', 'a', ('*', 'b', 'c')),
                        ('/', 2, 4)
                    )
                )
            ]
        },
        # Ejemplo 7 inicialización de variable sin asignación de valor
        {
            "codigo": "int x;",
            "descripcion": "Inicialización de una variable sin asignación de valor",
            "salida_esperada_tokens": [
                ('KEYWORD', 'int'),
                ('IDENTIFIER', 'x'),
                ('SEMICOLON', ';')
            ],
            "salida_esperada_ast": [
                ('DECLARATION', 'int', 'x')
            ]
        },
        # Ejemplo 8 estructura if con llave de apertura en otra línea
        {
            "codigo": """
            if (x > y){
                z = 1;
            }""",
            "descripcion": "Estructura if con llave de apertura en otra línea",
            "salida_esperada_tokens": [
                ("KEYWORD", "if"),
                ("LPAREN", "("),
                ("IDENTIFIER", "x"),
                ("GREATER", ">"),
                ("IDENTIFIER", "y"),
                ("RPAREN", ")"),
                ("LBRACE", "{"),
                ("IDENTIFIER", "z"),
                ("OPERATOR", "="),
                ("NUMBER", "1"),
                ("SEMICOLON", ";"),
                ("RBRACE", "}")
            ],
            "salida_esperada_ast": [
                ('IF', ('>', 'x', 'y'), [
                    ('ASSIGNMENT', 'z', 1)
                ])
            ]
        },
        # Ejemplo 9 paréntesis no balanceados
        {
            "codigo": "a = (b + 2;",
            "descripcion": "Paréntesis no balanceados",
            "salida_esperada_tokens": [
                ('IDENTIFIER', 'a'),
                ('OPERATOR', '='),
                ('LPAREN', '('),
                ('IDENTIFIER', 'b'),
                ('OPERATOR', '+'),
                ('NUMBER', '2'),
                ('SEMICOLON', ';')
            ],
            "salida_esperada_ast": None,
            "error_esperado": "Error en línea 1, columna 11: se esperaba RPAREN ')' pero se encontró ';'"
        },
        # Ejemplo 10 llave de cierre faltante en if
        {
            "codigo": """
            if (x < 5) {
                y = 2;
            """,
            "descripcion": "Llave de cierre faltante en if",
            "salida_esperada_tokens": [
                ('KEYWORD', 'if'),
                ('LPAREN', '('),
                ('IDENTIFIER', 'x'),
                ('LESS', '<'),
                ('NUMBER', '5'),
                ('RPAREN', ')'),
                ('LBRACE', '{'),
                ('IDENTIFIER', 'y'),
                ('OPERATOR', '='),
                ('NUMBER', '2'),
                ('SEMICOLON', ';'),
            ],
            "salida_esperada_ast": None,
            "error_esperado": "Error en línea 2, columna 16: falta '}' de cierre en el bloque 'if'"
        },
        # Ejemplo 11 asignación sin punto y coma
        {
            "codigo": "int a = 5",
            "descripcion": "Asignación sin punto y coma",
            "salida_esperada_tokens": [
                ('KEYWORD', 'int'),
                ('IDENTIFIER', 'a'),
                ('OPERATOR', '='),
                ('NUMBER', '5')
            ],
            "salida_esperada_ast": None,
            "error_esperado": "Error: se esperaba ',' o ';' pero no se encontraron más tokens."
        },
        # Ejemplo 12 uso de operador inválido o mal formado
        {
            "codigo": "a = 3 + * 4;",
            "descripcion": "Uso de operador inválido o mal formado",
            "salida_esperada_tokens": [
                ('IDENTIFIER', 'a'),
                ('OPERATOR', '='),
                ('NUMBER', '3'),
                ('OPERATOR', '+'),
                ('OPERATOR', '*'),
                ('NUMBER', '4'),
                ('SEMICOLON', ';')
            ],
            "salida_esperada_ast": None,
            "error_esperado": "Error en línea 1, columna 9: token inesperado '*' en expresión"
        },
        # Ejemplo 13 asignación de string y carácter
        {
            "codigo": """
            a = "Hola Mundo";
            b = 'H';
            """,
            "descripcion": "Asignación de string y carácter",
            "salida_esperada_tokens": [
                ("IDENTIFIER", "a"),
                ("OPERATOR", "="),
                ("STRING", "\"Hola Mundo\""),
                ("SEMICOLON", ";"),
                ("IDENTIFIER", "b"),
                ("OPERATOR", "="),
                ("CHAR", "'H'"),
                ("SEMICOLON", ";")
            ],
            "salida_esperada_ast": [
                ("ASSIGNMENT", "a", "\"Hola Mundo\""),
                ("ASSIGNMENT", "b", "'H'")
            ]

        },
        # Ejemplo 14 declaración y asignación en la misma línea (válido)
        {
            "codigo": "int a = 1, b = 2;",
            "descripcion": "Declaración de múltiples variables con asignación en la misma línea",
            "salida_esperada_tokens": [
                ('KEYWORD', 'int'),
                ('IDENTIFIER', 'a'),
                ('OPERATOR', '='),
                ('NUMBER', '1'),
                ('COMMA', ','),
                ('IDENTIFIER', 'b'),
                ('OPERATOR', '='),
                ('NUMBER', '2'),
                ('SEMICOLON', ';')
            ],
            "salida_esperada_ast": [
                ('DECLARATION', 'int', 'a', 1),
                ('DECLARATION', 'int', 'b', 2)
            ]
        },
        # Ejemplo 15 error sintáctico: palabra reservada mal escrita
        {
            "codigo": "iff (x == 1) { y = 2; }",
            "descripcion": "Palabra reservada mal escrita (error sintáctico)",
            "salida_esperada_tokens": [
                ('IDENTIFIER', 'iff'),
                ('LPAREN', '('),
                ('IDENTIFIER', 'x'),
                ('EQUALS', '=='),
                ('NUMBER', '1'),
                ('RPAREN', ')'),
                ('LBRACE', '{'),
                ('IDENTIFIER', 'y'),
                ('OPERATOR', '='),
                ('NUMBER', '2'),
                ('SEMICOLON', ';'),
                ('RBRACE', '}')
            ],
            "salida_esperada_ast": None,
            "error_esperado": "Error en línea 1, columna 1: se esperaba 'if', pero se encontró 'iff'"
        },
        # Ejemplo 16 caso límite: expresión vacía entre paréntesis
        {
            "codigo": "a = ();",
            "descripcion": "Expresión vacía entre paréntesis (caso límite)",
            "salida_esperada_tokens": [
                ('IDENTIFIER', 'a'),
                ('OPERATOR', '='),
                ('LPAREN', '('),
                ('RPAREN', ')'),
                ('SEMICOLON', ';')
            ],
            "salida_esperada_ast": None,
            "error_esperado": "Error en línea 1, columna 6: token inesperado ')' en expresión"
        }
    ]
                              


    for i, ejemplo in enumerate(ejemplos, 1):
        print(f"\n=== Test {i}: {ejemplo['descripcion']} ===")
        print("Código fuente:")
        print(ejemplo['codigo'])

        # Análisis Léxico
        try:
            tokens_completos = lexer_func(ejemplo['codigo'])
            # Extraemos solo (token_type, token_value)
            tokens = [(t[0], t[1]) for t in tokens_completos]
            print("Tokens obtenidos (tipo, valor):")
            print(tokens)
            print("Tokens esperados:")
            print(ejemplo['salida_esperada_tokens'])
        except Exception as e:
            print(f"Error en análisis léxico: {e}")
            print("Test fallido ❌")
            continue

        if tokens == ejemplo['salida_esperada_tokens']:
            print("Tokens correctos ✔️")
        else:
            print("Tokens incorrectos ❌")
            print("Test fallido ❌")
            

        # Análisis Sintáctico
        error_esperado = ejemplo.get('error_esperado')
        try:
            ast = parser_func(tokens_completos)  # Pasamos tokens completos o los que tu parser espera

            if error_esperado:
                print("❌ Se esperaba un error, pero el parser devolvió un AST.")
                print("AST obtenido:")
                print(ast)
                print("Test fallido ❌")
                continue

            print("AST obtenido:")
            print(ast)
            print("AST esperado:")
            print(ejemplo['salida_esperada_ast'])

            if ast == ejemplo['salida_esperada_ast']:
                print("AST correcto ✔️")
                print("Test exitoso ✅")
            else:
                print("AST incorrecto ❌")
                print("Test fallido ❌")

        except Exception as e:
            print(f"Error en análisis sintáctico: {e}")
            print("No se pudo obtener AST.")

            if error_esperado:
                if error_esperado in str(e):
                    print("Error esperado correcto ✔️")
                    print("Test exitoso ✅")
                else:
                    print("❌ El error no coincide con el esperado.")
                    print("Error esperado:")
                    print(error_esperado)
                    print("Test fallido ❌")
            else:
                print("❌ No se esperaba un error.")
                print("Test fallido ❌")


if __name__ == "__main__":
    run_tests(lexer, parser)
