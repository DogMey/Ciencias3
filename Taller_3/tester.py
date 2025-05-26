from lexer import lexer
from parser import parser

def run_tests(lexer_func, parser_func):
    ejemplos = [
        # Test 1: Declaración con comentario al inicio
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
        # Test 2: Expresión con paréntesis y multiplicación
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
        # Test 3: Condicional simple con igualdad y bloque
        {
            "codigo": """
            if (a == b) {
                c = 10;
            }
            """,
            "descripcion": "Condicional simple con igualdad y bloque",
            "salida_esperada_tokens": [
                ('IDENTIFIER', 'if'),
                ('LPAREN', '('),
                ('IDENTIFIER', 'a'),
                ('LOGICOPERATOR', '=='),
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
                ], None)
            ]
        },
        # Test 4: Declaración de variable y asignación
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
        # Test 5: Asignaciones con diferentes operaciones y paréntesis
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
        # Test 6: Expresión compleja con múltiples operaciones y paréntesis
        {
            "codigo": """
            a = 5;
            b = a - 3;
            c = b * (a + 2;
            """,
            "descripcion": "Expresión compleja con múltiples operaciones y paréntesis",
            "salida_esperada_tokens": [
                ("IDENTIFIER", 'result'),
                ('OPERATOR', '='),
                ('IDENTIFIER', 'a'),
                ('OPERATOR', '+'),
                ('IDENTIFIER', 'b'),
                ('OPERATOR', '*'),
                ('IDENTIFIER', 'c'),
                ('OPERATOR', '-'),
                ('NUMBER', '2'),
                ('OPERATOR', '/'),
                ('NUMBER', '4'),
                ('SEMICOLON', ';')
            ],
            'salida_esperada_ast': [
                ('ASSIGNMENT', 'result',
                    ('-',
                        ('+',
                            'a',
                            ('*', 'b', 'c')
                        ),
                        ('/', 2, 4)
                    )
                )
            ]
        },
        # Test 7: Declaración de variable sin asignación
        {
            "codigo": "int x = 1 + 2;",
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

    # Ejecutar cada test
    for i, ejemplo in enumerate(ejemplos, 1):
        print(f"\n=== Test {i}: {ejemplo['descripcion']} ===")
        print("Código fuente:")
        print(ejemplo['codigo'])

        # Análisis Léxico
        try:
            tokens_crudos = lexer_func(ejemplo['codigo'])   # Llamar al lexer
            tokens = normalizar_tokens(tokens_crudos)       # Normalizar tokens
            print("Tokens obtenidos:")
            print(tokens)
            print("Tokens esperados:")
            print(ejemplo['salida_esperada_tokens'])
        except Exception as e:
            print(f"Error en análisis léxico: {e}")
            continue

        if tokens == ejemplo['salida_esperada_tokens']:
            print("Tokens correctos ✔️")
        else:
            print("Tokens incorrectos ❌")

        # Análisis Sintáctico
        try:
            # Debug: mostrar formato de tokens antes de parsear
            print("Formato de tokens_crudos:", tokens_crudos[:3] if tokens_crudos else "Lista vacía")
            
            ast = parser_func(tokens_crudos)
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

# Normalizar tokens para comparación
def normalizar_tokens(tokens):
        """
        Convierte los tokens del nuevo lexer al formato ('TYPE', 'VALUE') para comparación.
        Ajusta aquí si los tokens vienen como objetos.
        """
        tokens_filtrados = []   # Lista para almacenar los tokens filtrados
        for tok in tokens:
            # Si el token es una tupla antigua, no hacer nada
            if isinstance(tok, tuple):
                tokens_filtrados.append(tok)    # Añadir el token tal cual
            else:
                # Si el token es un diccionario, extraer tipo y valor
                if tok["type"] and tok["value"]:
                    if tok["type"] not in {"COMMENT", "WHITESPACE"}: # Ignorar comentarios y espacios
                        tokens_filtrados.append((tok["type"], tok["value"])) # Añadir el token normalizado
        return tokens_filtrados # Retornar la lista de tokens filtrados

if __name__ == "__main__":
    run_tests(lexer, parser)