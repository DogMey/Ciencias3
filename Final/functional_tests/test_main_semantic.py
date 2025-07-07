import sys
import os
import importlib.util

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main_lexer import lexer
from main_parser import parser
from main_semantyc import semantic_analyze

def cargar_ejemplos(tipo, categoria):
    base = os.path.dirname(__file__)
    carpeta = f"ejemplos_{tipo}"
    modulo = f"{carpeta}.{categoria}"
    ruta = os.path.join(base, carpeta, f"{categoria}.py")
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No existe el archivo de ejemplos: {ruta}")
    spec = importlib.util.spec_from_file_location(modulo, ruta)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    nombre_lista = f"EJEMPLOS_{tipo.upper()}_{categoria.upper()}"
    return getattr(mod, nombre_lista)

def run_functional_semantic_tests(ejemplos):
    for i, ejemplo in enumerate(ejemplos, 1):
        print(f"\n=== Test {i}: {ejemplo['descripcion']} ===")
        print("Código fuente:")
        print(ejemplo['codigo'])
        try:
            tokens_completos = lexer(ejemplo['codigo'])
            ast = parser(tokens_completos)
            resultado = semantic_analyze(ast)
            print("Resultado semántico obtenido:", resultado)
            print("Resultado semántico esperado:", ejemplo.get('salida_esperada_semantica'))
            if resultado == ejemplo.get('salida_esperada_semantica'):
                print("✔️ Test exitoso")
            else:
                print("❌ Resultado semántico incorrecto")
        except Exception as e:
            print(f"❌ Error en análisis semántico: {e}")

if __name__ == "__main__":
    import argparse
    parser_arg = argparse.ArgumentParser(description="Test funcional semántico por tipo y categoría.")
    parser_arg.add_argument('--tipo', choices=['exitosos', 'error'], default='exitosos', help='Tipo de ejemplos a probar')
    parser_arg.add_argument('--categoria', choices=['variables', 'funciones', 'bloques'], default='variables', help='Categoría de ejemplos')
    args = parser_arg.parse_args()
    ejemplos = cargar_ejemplos(args.tipo, args.categoria)
    run_functional_semantic_tests(ejemplos)
