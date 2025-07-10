"""
Ejemplos exitosos de funciones para el parser.
Incluye declaraciones de funciones, llamadas a funciones y return statements.
"""

EJEMPLOS_EXITOSOS_PARSER_FUNCIONES = [
    {
        "codigo": """
func int suma(int a, int b) {
    return a + b;
}
        """,
        "descripcion": "Función simple con dos parámetros y return",
        "salida_esperada_ast": [
            ("FUNC_DECL", "suma", [("int", "a"), ("int", "b")], "int", [
                ("RETURN", ("+", "a", "b"))
            ])
        ]
    },
    {
        "codigo": """
func void saludo() {
    return;
}
        """,
        "descripcion": "Función sin parámetros ni valor de retorno",
        "salida_esperada_ast": [
            ("FUNC_DECL", "saludo", [], "void", [
                ("RETURN", None)
            ])
        ]
    },
    {
        "codigo": """
func int factorial(int n) {
    if (n <= 1) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}
        """,
        "descripcion": "Función recursiva con condicional",
        "salida_esperada_ast": [
            ("FUNC_DECL", "factorial", [("int", "n")], "int", [
                ("IF_ELSE", 
                    ("<=", "n", 1),
                    [("RETURN", 1)],
                    [("RETURN", ("*", "n", ("FUNC_CALL", "factorial", [("-", "n", 1)])))]
                )
            ])
        ]
    },
    {
        "codigo": """
func float promedio(int a, int b, int c) {
    int suma = a + b + c;
    return suma / 3;
}
        """,
        "descripcion": "Función con múltiples parámetros y variable local",
        "salida_esperada_ast": [
            ("FUNC_DECL", "promedio", [("int", "a"), ("int", "b"), ("int", "c")], "float", [
                ("DECLARATION", "int", "suma", ("+", ("+", "a", "b"), "c")),
                ("RETURN", ("/", "suma", 3))
            ])
        ]
    },
    {
        "codigo": """
func int maximo(int x, int y) {
    if (x > y) {
        return x;
    } else {
        return y;
    }
}
        """,
        "descripcion": "Función que retorna el máximo entre dos números",
        "salida_esperada_ast": [
            ("FUNC_DECL", "maximo", [("int", "x"), ("int", "y")], "int", [
                ("IF_ELSE", 
                    (">", "x", "y"),
                    [("RETURN", "x")],
                    [("RETURN", "y")]
                )
            ])
        ]
    },
    {
        "codigo": """
func void imprimirNumeros(int hasta) {
    int i = 1;
    while (i <= hasta) {
        i = i + 1;
    }
    return;
}
        """,
        "descripcion": "Función void con bucle while",
        "salida_esperada_ast": [
            ("FUNC_DECL", "imprimirNumeros", [("int", "hasta")], "void", [
                ("DECLARATION", "int", "i", 1),
                ("WHILE", ("<=", "i", "hasta"), [
                    ("ASSIGNMENT", "i", ("+", "i", 1))
                ]),
                ("RETURN", None)
            ])
        ]
    },
    {
        "codigo": """
func int cuadrado(int n) {
    return n * n;
}
int resultado = cuadrado(5);
        """,
        "descripcion": "Declaración de función y llamada a función",
        "salida_esperada_ast": [
            ("FUNC_DECL", "cuadrado", [("int", "n")], "int", [
                ("RETURN", ("*", "n", "n"))
            ]),
            ("DECLARATION", "int", "resultado", ("FUNC_CALL", "cuadrado", [5]))
        ]
    },
    {
        "codigo": """
func int operacion(int a, int b, int c) {
    int temp = a + b;
    temp = temp * c;
    return temp;
}
        """,
        "descripcion": "Función con múltiples operaciones y variable temporal",
        "salida_esperada_ast": [
            ("FUNC_DECL", "operacion", [("int", "a"), ("int", "b"), ("int", "c")], "int", [
                ("DECLARATION", "int", "temp", ("+", "a", "b")),
                ("ASSIGNMENT", "temp", ("*", "temp", "c")),
                ("RETURN", "temp")
            ])
        ]
    },
    {
        "codigo": """
func void procesarDatos(int x, float y) {
    int resultado = x * 2;
    if (resultado > 10) {
        resultado = resultado - 5;
    }
    return;
}
        """,
        "descripcion": "Función void con parámetros de diferentes tipos",
        "salida_esperada_ast": [
            ("FUNC_DECL", "procesarDatos", [("int", "x"), ("float", "y")], "void", [
                ("DECLARATION", "int", "resultado", ("*", "x", 2)),
                ("IF", (">", "resultado", 10), [
                    ("ASSIGNMENT", "resultado", ("-", "resultado", 5))
                ]),
                ("RETURN", None)
            ])
        ]
    },
    {
        "codigo": """
sumar(10, 20);
        """,
        "descripcion": "Llamada a función simple",
        "salida_esperada_ast": [
            ("FUNC_CALL", "sumar", [10, 20])
        ]
    },
    {
        "codigo": """
calcular(a + b, c * 2, 5);
        """,
        "descripcion": "Llamada a función con expresiones como argumentos",
        "salida_esperada_ast": [
            ("FUNC_CALL", "calcular", [("+", "a", "b"), ("*", "c", 2), 5])
        ]
    },
    {
        "codigo": """
func int fibonacci(int n) {
    if (n <= 1) {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}
        """,
        "descripcion": "Función recursiva de Fibonacci",
        "salida_esperada_ast": [
            ("FUNC_DECL", "fibonacci", [("int", "n")], "int", [
                ("IF", ("<=", "n", 1), [
                    ("RETURN", "n")
                ]),
                ("RETURN", ("+", 
                    ("FUNC_CALL", "fibonacci", [("-", "n", 1)]),
                    ("FUNC_CALL", "fibonacci", [("-", "n", 2)])
                ))
            ])
        ]
    },
    {
        "codigo": """
func bool esPositivo(int numero) {
    if (numero > 0) {
        return true;
    } else {
        return false;
    }
}
        """,
        "descripcion": "Función que retorna bool",
        "salida_esperada_ast": [
            ("FUNC_DECL", "esPositivo", [("int", "numero")], "bool", [
                ("IF_ELSE", 
                    (">", "numero", 0),
                    [("RETURN", "true")],
                    [("RETURN", "false")]
                )
            ])
        ]
    },
    {
        "codigo": """
func int multiplicar(int a, int b) {
    int resultado = 0;
    int i = 0;
    while (i < b) {
        resultado = resultado + a;
        i = i + 1;
    }
    return resultado;
}
        """,
        "descripcion": "Función que implementa multiplicación con bucle",
        "salida_esperada_ast": [
            ("FUNC_DECL", "multiplicar", [("int", "a"), ("int", "b")], "int", [
                ("DECLARATION", "int", "resultado", 0),
                ("DECLARATION", "int", "i", 0),
                ("WHILE", ("<", "i", "b"), [
                    ("ASSIGNMENT", "resultado", ("+", "resultado", "a")),
                    ("ASSIGNMENT", "i", ("+", "i", 1))
                ]),
                ("RETURN", "resultado")
            ])
        ]
    },
    {
        "codigo": """
func void configurar(int x, int y, int z) {
    int config = x + y + z;
    if (config > 50) {
        config = 50;
    }
    return;
}
configurar(10, 20, 30);
        """,
        "descripcion": "Función con configuración y su llamada",
        "salida_esperada_ast": [
            ("FUNC_DECL", "configurar", [("int", "x"), ("int", "y"), ("int", "z")], "void", [
                ("DECLARATION", "int", "config", ("+", ("+", "x", "y"), "z")),
                ("IF", (">", "config", 50), [
                    ("ASSIGNMENT", "config", 50)
                ]),
                ("RETURN", None)
            ]),
            ("FUNC_CALL", "configurar", [10, 20, 30])
        ]
    }
]
