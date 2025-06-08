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
            "codigo": "int x = 2 + 3;",
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
            "codigo": "int x = int(\"5\");",
            "descripcion": "Asignación válida de conversión de string a int",
            "espera_error": False
        },
        {
            "codigo": "int x = \"5\" + 2;",
            "descripcion": "Asignación inválida de suma de string y entero a variable entera",
            "espera_error": True,
            "error_esperado": "Error semántico: no se puede operar entre 'string' y tipo numérico sin conversión explícita."
        }
    ]

    for i, ejemplo in enumerate(ejemplos, 1):
        print(f"\n=== Test Semántico {i}: {ejemplo['descripcion']} ===")
        print("Código fuente:")
        print(ejemplo['codigo'])

        try:
            tokens = lexer(ejemplo['codigo'])
            print(tokens)
            ast = parser(tokens)
            print(ast)
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