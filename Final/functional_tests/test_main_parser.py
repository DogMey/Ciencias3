import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main_lexer import lexer
from main_parser import parser
from functional_tests.ejemplos import EJEMPLOS

def run_functional_parser_tests():
    for i, ejemplo in enumerate(EJEMPLOS, 1):
        print(f"\n=== Test {i}: {ejemplo['descripcion']} ===")
        print("Código fuente:")
        print(ejemplo['codigo'])
        try:
            tokens_completos = lexer(ejemplo['codigo'])
            ast = parser(tokens_completos)
            print("AST obtenido:", ast)
            print("AST esperado:", ejemplo.get('salida_esperada_ast'))
            if ast == ejemplo.get('salida_esperada_ast'):
                print("✔️ Test exitoso")
            else:
                print("❌ AST incorrecto")
        except Exception as e:
            print(f"❌ Error en análisis sintáctico: {e}")

if __name__ == "__main__":
    run_functional_parser_tests()