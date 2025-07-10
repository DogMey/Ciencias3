import sys
import os
import importlib.util

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main_lexer import lexer
from main_parser import parser
from main_semantyc import semantic_analyze

def cargar_ejemplos(tipo, categoria):
    """Carga ejemplos de la carpeta y archivo correspondiente."""
    base = os.path.dirname(__file__)
    
    if tipo == "exitosos":
        carpeta = "ejemplos_exitosos"
        subcarpeta = "semantic"
        archivo = f"{categoria}.py"
        nombre_lista = f"EJEMPLOS_EXITOSOS_SEMANTIC_{categoria.upper()}"
    elif tipo == "error":
        carpeta = "ejemplos_error"
        subcarpeta = "semantic"
        archivo = f"{categoria}.py"
        nombre_lista = f"EJEMPLOS_ERROR_SEMANTIC_{categoria.upper()}"
    else:
        raise ValueError(f"Tipo no válido: {tipo}")
    
    if subcarpeta:
        ruta = os.path.join(base, carpeta, subcarpeta, archivo)
    else:
        ruta = os.path.join(base, carpeta, archivo)
    
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No existe el archivo de ejemplos: {ruta}")
    
    # Cargar el módulo dinámicamente
    spec = importlib.util.spec_from_file_location(f"{carpeta}_{categoria}", ruta)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    return getattr(mod, nombre_lista)

def run_functional_semantic_tests(ejemplos, tipo):
    """Ejecuta las pruebas funcionales semánticas."""
    exitos = 0
    total = len(ejemplos)
    
    for i, ejemplo in enumerate(ejemplos, 1):
        print(f"\n=== Test {i}: {ejemplo['descripcion']} ===")
        print("Código fuente:")
        print(ejemplo['codigo'])
        
        try:
            # Análisis léxico
            tokens_completos = lexer(ejemplo['codigo'])
            
            # Análisis sintáctico
            ast = parser(tokens_completos)
            
            # Análisis semántico
            resultado = semantic_analyze(ast)
            
            if tipo == "exitosos":
                # Para casos exitosos, verificar que el resultado sea True
                esperado = ejemplo.get('salida_esperada_semantica', True)
                print(f"Resultado semántico obtenido: {resultado}")
                print(f"Resultado semántico esperado: {esperado}")
                
                if resultado == esperado:
                    print("Test exitoso")
                    exitos += 1
                else:
                    print("❌ Resultado semántico incorrecto")
            else:
                # Para casos de error, no debería llegar aquí
                print("❌ Se esperaba un error semántico, pero el análisis fue exitoso")
                
        except Exception as e:
            if tipo == "error":
                # Para casos de error, esto es esperado
                error_esperado = ejemplo.get('error_esperado', 'Error')
                print(f"ERROR semantico detectado correctamente: {e}")
                print(f"Tipo de error esperado: {error_esperado}")
                exitos += 1
            else:
                # Para casos exitosos, esto es un fallo
                print(f"ERROR inesperado en análisis semántico: {e}")
    
    print(f"\n{'='*50}")
    print(f"Resultados: {exitos}/{total} pruebas exitosas")
    print(f"Porcentaje de éxito: {(exitos/total)*100:.1f}%")
    
    return exitos == total

def listar_categorias_disponibles():
    """Lista las categorías disponibles para cada tipo."""
    base = os.path.dirname(__file__)
    
    # Categorías exitosas
    exitosos_path = os.path.join(base, "ejemplos_exitosos", "semantic")
    categorias_exitosas = []
    if os.path.exists(exitosos_path):
        for archivo in os.listdir(exitosos_path):
            if archivo.endswith('.py') and not archivo.startswith('__'):
                categorias_exitosas.append(archivo[:-3])  # Quitar .py
    
    # Categorías de error
    error_path = os.path.join(base, "ejemplos_error", "semantic")
    categorias_error = []
    if os.path.exists(error_path):
        for archivo in os.listdir(error_path):
            if archivo.endswith('.py') and not archivo.startswith('__'):
                categorias_error.append(archivo[:-3])  # Quitar .py
    
    return categorias_exitosas, categorias_error

if __name__ == "__main__":
    import argparse
    
    parser_arg = argparse.ArgumentParser(
        description="Test funcional semántico por tipo y categoría.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python test_main_semantic.py --tipo exitosos --categoria variables
  python test_main_semantic.py --tipo error --categoria variables
  python test_main_semantic.py --listar
        """
    )
    
    parser_arg.add_argument(
        '--tipo', 
        choices=['exitosos', 'error'], 
        default='exitosos', 
        help='Tipo de ejemplos a probar (exitosos o error)'
    )
    
    parser_arg.add_argument(
        '--categoria', 
        default='variables', 
        help='Categoría de ejemplos (variables, funciones, bloques, etc.)'
    )
    
    parser_arg.add_argument(
        '--listar', 
        action='store_true', 
        help='Listar todas las categorías disponibles'
    )
    
    args = parser_arg.parse_args()
    
    if args.listar:
        print("Categorías disponibles:")
        exitosas, error = listar_categorias_disponibles()
        print(f"\nCategorías exitosas: {exitosas}")
        print(f"Categorías de error: {error}")
        sys.exit(0)
    
    try:
        print(f"Cargando ejemplos: {args.tipo} - {args.categoria}")
        ejemplos = cargar_ejemplos(args.tipo, args.categoria)
        print(f"Se cargaron {len(ejemplos)} ejemplos")
        
        success = run_functional_semantic_tests(ejemplos, args.tipo)
        
        # Código de salida según el resultado
        sys.exit(0 if success else 1)
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Use --listar para ver las categorías disponibles")
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
