import sys
import os
import importlib.util

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main_lexer import lexer

def cargar_ejemplos(tipo, categoria):
    """
    tipo: 'exitosos' o 'error'
    categoria: 'variables', 'funciones', 'bloques'
    """
    base = os.path.dirname(__file__)
    if tipo == 'exitosos':
        ruta = os.path.join(base, 'ejemplos_exitosos', 'lexer', f'{categoria}.py')
        modulo = f'ejemplos_exitosos.lexer.{categoria}'
        nombre_lista = f'EJEMPLOS_EXITOSOS_LEXER_{categoria.upper()}'
    else:
        ruta = os.path.join(base, 'ejemplos_error', 'lexer', f'{categoria}.py')
        modulo = f'ejemplos_error.lexer.{categoria}'
        nombre_lista = f'EJEMPLOS_ERROR_LEXER_{categoria.upper()}'
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No existe el archivo de ejemplos: {ruta}")
    spec = importlib.util.spec_from_file_location(modulo, ruta)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, nombre_lista)

def run_functional_lexer_tests(ejemplos, tipo):
    exitos = 0
    total = len(ejemplos)
    
    for i, ejemplo in enumerate(ejemplos, 1):
        print(f"\n=== Test {i}: {ejemplo['descripcion']} ===")
        print("Código fuente:")
        print(ejemplo['codigo'])
        
        try:
            tokens_completos = lexer(ejemplo['codigo'])
            tokens = [(t[0], t[1]) for t in tokens_completos]
            
            if tipo == 'exitosos':
                print("Tokens obtenidos:", tokens)
                print("Tokens esperados:", ejemplo.get('salida_esperada_tokens'))
                if tokens == ejemplo.get('salida_esperada_tokens'):
                    print("Test exitoso")
                    exitos += 1
                else:
                    print("❌ Tokens incorrectos")
            else:  # tipo == 'error'
                # Para casos de error, esperamos que el análisis léxico falle
                salida_esperada = ejemplo.get('salida_esperada_lexica', False)
                if salida_esperada == False:
                    print("❌ Se esperaba un error léxico, pero el análisis fue exitoso")
                    print("Tokens obtenidos:", tokens)
                else:
                    print("Test exitoso - análisis léxico completado correctamente")
                    exitos += 1
                    
        except Exception as e:
            if tipo == 'exitosos':
                print(f"ERROR inesperado en análisis léxico: {e}")
            else:  # tipo == 'error'
                salida_esperada = ejemplo.get('salida_esperada_lexica', False)
                if salida_esperada == False:
                    print(f"ERROR detectado correctamente: {e}")
                    print(f"Tipo de error esperado: {ejemplo.get('error_esperado', 'Error léxico')}")
                    exitos += 1
                else:
                    print(f"ERROR inesperado en análisis léxico: {e}")
    
    print(f"\n{'='*50}")
    print(f"Resultados: {exitos}/{total} pruebas exitosas")
    print(f"Porcentaje de éxito: {(exitos/total)*100:.1f}%")
    return exitos == total

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Test funcional lexer por tipo y categoría.")
    parser.add_argument('--tipo', choices=['exitosos', 'error'], default='exitosos', help='Tipo de ejemplos a probar')
    parser.add_argument('--categoria', choices=['variables', 'funciones', 'bloques'], default='variables', help='Categoría de ejemplos')
    args = parser.parse_args()
    ejemplos = cargar_ejemplos(args.tipo, args.categoria)
    print(f"Cargando ejemplos: {args.tipo} - {args.categoria}")
    print(f"Se cargaron {len(ejemplos)} ejemplos")
    run_functional_lexer_tests(ejemplos, args.tipo)