from lexer import lexer
from parser import parser
from semantic import semantic_analyze

def run_semantic_tests():
    ejemplos = [
        {
            "codigo": "int x = 5; print(x);",
            "descripcion": "Declaración y uso correcto de variable",
            "espera_error": False
        },
        {
            "codigo": "print(x);",
            "descripcion": "Uso de variable no declarada",
            "espera_error": True,
            "error_esperado": "Error semántico: la variable 'x' no ha sido declarada."
        },
                {
            "codigo": "int x = 2 + 3; print(x);",
            "descripcion": "Asignación válida de suma de enteros a variable entera",
            "espera_error": False
        },
        {
            "codigo": "int x = \"hola\";",
            "descripcion": "Asignación inválida de cadena a variable entera",
            "espera_error": True,
            "error_esperado": "Error semántico: no se puede asignar un valor de tipo 'string' a una variable de tipo 'int'."
        },
        {
            "codigo": "int x = int(\"5\"); print(x);",
            "descripcion": "Asignación válida de conversión de string a int",
            "espera_error": False
        },
        {
            "codigo": "int x = \"5\" + 2;",
            "descripcion": "Asignación inválida de suma de string y entero a variable entera",
            "espera_error": True,
            "error_esperado": "Error semántico: no se puede operar entre 'string' y tipo numérico sin conversión explícita."
        },
        {
            "codigo": "bool activo = !false; print(activo);",
            "descripcion": "Uso válido del operador de negación lógica sobre un booleano",
            "espera_error": False
        },
        {
            "codigo": "int x = !\"hola\";",
            "descripcion": "Uso inválido del operador de negación lógica sobre una cadena",
            "espera_error": True,
            "error_esperado": "Error semántico: el operador '!' solo puede aplicarse a valores booleanos, se encontró 'string'."
        },
        {
            "codigo": "int x = 5; if(x > 5) {print(x);}",
            "descripcion": "Aplicación correcta de condición con variable declarada",
            "espera_error": False,
        },
        {
            "codigo": "if (\"texto\") { int x = 5; }",
            "descripcion": "Aplicación incorrecta de condición con variable no declarada",
            "espera_error": True,
            "error_esperado": "la condición del IF debe ser una expresión booleana, se encontró 'string'"
        },
                {
            "codigo": "const PI = 3.14; print(PI);",
            "descripcion": "Declaración válida de constante",
            "espera_error": False
        },
        {
            "codigo": "const PI = 3.14; PI = 3.1416;",
            "descripcion": "Intento de modificar una constante",
            "espera_error": True,
            "error_esperado": "Error semántico: no se puede modificar la constante 'PI'."
        },
        {
            "codigo": "int edadUsuario; print(edadUsuario);",
            "descripcion": "Declaración válida de variable con identificador correcto",
            "espera_error": False
        },
        {
            "codigo": "int 2edad;",
            "descripcion": "Declaración inválida de variable: identificador no puede comenzar con un número",
            "espera_error": True,
            "error_esperado": "Error en línea 1, columna 5: se esperaba identificador, pero se encontró '2'"
        },
        {
            "codigo": "int x = 0;",
            "descripcion": "Declaración de variable no utilizada",
            "espera_error": True,
            "error_esperado": "Advertencia: la variable 'x' fue declarada pero nunca utilizada."
        },
        {
            "codigo": "int x = 0; x = x + 1;",
            "descripcion": "Asignación válida a variable inicializada",
            "espera_error": False
        },
        {
            "codigo": "x = x + 1;",
            "descripcion": "Uso de variable no inicializada",
            "espera_error": True,
            "error_esperado": "Error semántico: la variable 'x' no ha sido declarada."
        },
        {
            "codigo": "function sumar(int a, int b){print(a + b);}",
            "descripcion": "Creación de Función Correcta",
            "espera_error": False,
        },
         {
            "codigo": "function sumar(int a, int b){print(a + b);",
            "descripcion": "Creación de Función Correcta",
            "espera_error": True,
            "error_esperado": "Error en línea 1, columna 10: falta '}' de cierre en el bloque de la función 'sumar'"
        },
    ]

    for i, ejemplo in enumerate(ejemplos, 1):
        print(f"\n=== Test Semántico {i}: {ejemplo['descripcion']} ===")
        print("Código fuente:")
        print(ejemplo['codigo'])

        try:
            tokens = lexer(ejemplo['codigo'])
            ast = parser(tokens)
            semantic_analyze(ast)
            if ejemplo["espera_error"]:
                print("❌ Se esperaba un error semántico, pero no ocurrió.")
            else:
                print("✔️ Análisis semántico exitoso.")
        except Exception as e:
            if ejemplo["espera_error"]:
                if ejemplo.get("error_esperado") in str(e):
                    print("✔️ Error semántico esperado detectado:")
                    print(e)
                else:
                    print("❌ Error semántico detectado, pero no coincide con el esperado:")
                    print(e)
            else:
                print("❌ No se esperaba un error.")
                print(e)

if __name__ == "__main__":
    run_semantic_tests()