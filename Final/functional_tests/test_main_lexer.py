import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main_lexer import lexer
from functional_tests.ejemplos import EJEMPLOS

def run_functional_lexer_tests():
    for i, ejemplo in enumerate(EJEMPLOS, 1):
        print(f"\n=== Test {i}: {ejemplo['descripcion']} ===")
        print("Código fuente:")
        print(ejemplo['codigo'])
        try:
            tokens_completos = lexer(ejemplo['codigo'])
            tokens = [(t[0], t[1]) for t in tokens_completos]
            print("Tokens obtenidos:", tokens)
            print("Tokens esperados:", ejemplo['salida_esperada_tokens'])
            if tokens == ejemplo['salida_esperada_tokens']:
                print("✔️ Test exitoso")
            else:
                print("❌ Tokens incorrectos")
        except Exception as e:
            print(f"❌ Error en análisis léxico: {e}")

if __name__ == "__main__":
    run_functional_lexer_tests()