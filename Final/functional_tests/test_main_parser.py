import sys
import os
import importlib.util

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main_lexer import lexer
from main_parser import parser

def cargar_ejemplos(tipo, categoria):
    """
    tipo: 'exitosos' o 'error'
    categoria: 'variables', 'funciones', 'bloques'
    """
    base = os.path.dirname(__file__)
    if tipo == 'exitosos':
        ruta = os.path.join(base, 'ejemplos_exitosos', 'parser', f'{categoria}.py')
        modulo = f'ejemplos_exitosos.parser.{categoria}'
        nombre_lista = f'EJEMPLOS_EXITOSOS_PARSER_{categoria.upper()}'
    else:
        ruta = os.path.join(base, 'ejemplos_error', 'parser', f'{categoria}.py')
        modulo = f'ejemplos_error.parser.{categoria}'
        nombre_lista = f'EJEMPLOS_ERROR_PARSER_{categoria.upper()}'
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No existe el archivo de ejemplos: {ruta}")
    spec = importlib.util.spec_from_file_location(modulo, ruta)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, nombre_lista)

def run_functional_parser_tests(ejemplos):
    for i, ejemplo in enumerate(ejemplos, 1):
        print(f"\n=== Test {i}: {ejemplo['descripcion']} ===")
        print("Código fuente:")
        print(ejemplo['codigo'])
        try:
            tokens_completos = lexer(ejemplo['codigo'])
            ast = parser(tokens_completos)
            print("AST obtenido:", ast)
            print("AST esperado:", ejemplo.get('salida_esperada_ast'))
            if ast == ejemplo.get('salida_esperada_ast'):
                print("Test exitoso")
            else:
                print("❌ AST incorrecto")
        except Exception as e:
            print(f"ERROR en análisis sintáctico: {e}")

if __name__ == "__main__":
    import argparse
    parser_arg = argparse.ArgumentParser(description="Test funcional parser por tipo y categoría.")
    parser_arg.add_argument('--tipo', choices=['exitosos', 'error'], default='exitosos', help='Tipo de ejemplos a probar')
    parser_arg.add_argument('--categoria', choices=['variables', 'funciones', 'bloques'], default='variables', help='Categoría de ejemplos')
    args = parser_arg.parse_args()
    ejemplos = cargar_ejemplos(args.tipo, args.categoria)
    run_functional_parser_tests(ejemplos)