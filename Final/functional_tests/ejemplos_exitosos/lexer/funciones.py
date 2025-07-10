EJEMPLOS_EXITOSOS_LEXER_FUNCIONES = [
    {
        "codigo": """
int suma(int a, int b) {
    return a + b;
}
        """,
        "descripcion": "Declaración de función con parámetros y return",
        "salida_esperada_tokens": [
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
            ('RBRACE', '}')
        ]
    },
    {
        "codigo": """
int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}
        """,
        "descripcion": "Función recursiva con condicional",
        "salida_esperada_tokens": [
            ('KEYWORD', 'int'),
            ('IDENTIFIER', 'factorial'),
            ('LPAREN', '('),
            ('KEYWORD', 'int'),
            ('IDENTIFIER', 'n'),
            ('RPAREN', ')'),
            ('LBRACE', '{'),
            ('KEYWORD', 'if'),
            ('LPAREN', '('),
            ('IDENTIFIER', 'n'),
            ('LESSEQUAL', '<='),
            ('NUMBER', '1'),
            ('RPAREN', ')'),
            ('LBRACE', '{'),
            ('KEYWORD', 'return'),
            ('NUMBER', '1'),
            ('SEMICOLON', ';'),
            ('RBRACE', '}'),
            ('KEYWORD', 'return'),
            ('IDENTIFIER', 'n'),
            ('OPERATOR', '*'),
            ('IDENTIFIER', 'factorial'),
            ('LPAREN', '('),
            ('IDENTIFIER', 'n'),
            ('OPERATOR', '-'),
            ('NUMBER', '1'),
            ('RPAREN', ')'),
            ('SEMICOLON', ';'),
            ('RBRACE', '}')
        ]
    },
    {
        "codigo": """
void saludar() {
    print("Hola mundo");
}
        """,
        "descripcion": "Función sin parámetros que no retorna",
        "salida_esperada_tokens": [
            ('KEYWORD', 'void'),
            ('IDENTIFIER', 'saludar'),
            ('LPAREN', '('),
            ('RPAREN', ')'),
            ('LBRACE', '{'),
            ('IDENTIFIER', 'print'),
            ('LPAREN', '('),
            ('STRING', '"Hola mundo"'),
            ('RPAREN', ')'),
            ('SEMICOLON', ';'),
            ('RBRACE', '}')
        ]
    },
    {
        "codigo": """
int resultado = suma(5, 3);
        """,
        "descripcion": "Llamada a función con argumentos",
        "salida_esperada_tokens": [
            ('KEYWORD', 'int'),
            ('IDENTIFIER', 'resultado'),
            ('OPERATOR', '='),
            ('IDENTIFIER', 'suma'),
            ('LPAREN', '('),
            ('NUMBER', '5'),
            ('COMMA', ','),
            ('NUMBER', '3'),
            ('RPAREN', ')'),
            ('SEMICOLON', ';')
        ]
    },
    {
        "codigo": """
int calcular(int x, int y, int z) {
    int temp = x + y;
    return temp * z;
}
        """,
        "descripcion": "Función con múltiples parámetros y variables locales",
        "salida_esperada_tokens": [
            ('KEYWORD', 'int'),
            ('IDENTIFIER', 'calcular'),
            ('LPAREN', '('),
            ('KEYWORD', 'int'),
            ('IDENTIFIER', 'x'),
            ('COMMA', ','),
            ('KEYWORD', 'int'),
            ('IDENTIFIER', 'y'),
            ('COMMA', ','),
            ('KEYWORD', 'int'),
            ('IDENTIFIER', 'z'),
            ('RPAREN', ')'),
            ('LBRACE', '{'),
            ('KEYWORD', 'int'),
            ('IDENTIFIER', 'temp'),
            ('OPERATOR', '='),
            ('IDENTIFIER', 'x'),
            ('OPERATOR', '+'),
            ('IDENTIFIER', 'y'),
            ('SEMICOLON', ';'),
            ('KEYWORD', 'return'),
            ('IDENTIFIER', 'temp'),
            ('OPERATOR', '*'),
            ('IDENTIFIER', 'z'),
            ('SEMICOLON', ';'),
            ('RBRACE', '}')
        ]
    }
]
