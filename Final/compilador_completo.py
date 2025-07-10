"""
Integrador completo: Parser -> Generador de Código Intermedio
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main_parser import parser
from main_lexer import lexer
from codegen import CodeGenerator, generate_declaration_code, generate_assignment_code

def compile_to_intermediate_code(source_code):
    """
    Compila código fuente a código intermedio.
    
    Args:
        source_code: Código fuente en C
    
    Returns:
        tuple: (success, code_generator_or_error)
    """
    try:
        # Paso 1: Análisis léxico
        print("=== ANÁLISIS LÉXICO ===")
        tokens = lexer(source_code)
        print(f"Tokens generados: {len(tokens)}")
        
        # Paso 2: Análisis sintáctico
        print("\n=== ANÁLISIS SINTÁCTICO ===")
        print("Código fuente:")
        print(source_code)
        
        ast_nodes = parser(tokens)
        print(f"\nAST generado: {len(ast_nodes)} nodos")
        for i, node in enumerate(ast_nodes):
            print(f"  {i+1}: {node}")
        
        # Paso 3: Generación de código intermedio
        print("\n=== GENERACIÓN DE CÓDIGO INTERMEDIO ===")
        code_generator = CodeGenerator()
        
        for node in ast_nodes:
            if node[0] == 'DECLARATION':
                generate_declaration_code(node, code_generator)
            elif node[0] == 'ASSIGNMENT':
                generate_assignment_code(node, code_generator)
            else:
                print(f"Advertencia: Tipo de nodo no soportado: {node[0]}")
        
        print("\nTabla de símbolos:")
        for var_name, info in code_generator.symbol_table.items():
            print(f"  {var_name}: {info}")
        
        print()
        code_generator.print_code()
        
        return True, code_generator
        
    except Exception as e:
        print(f"Error en compilación: {e}")
        return False, str(e)


def main():
    """Función principal con ejemplos de prueba."""
    ejemplos = [
        {
            "nombre": "Declaraciones simples",
            "codigo": """
                int x = 5;
                int y = 10;
                x = x + 1;
            """
        },
        {
            "nombre": "Expresiones complejas",
            "codigo": """
                int a = 5;
                int b = 10;
                int resultado = a * 2 + b;
            """
        },
        {
            "nombre": "Secuencia de operaciones",
            "codigo": """
                int x = 1;
                x = x + 1;
                x = x * 2;
                x = x - 1;
            """
        }
    ]
    
    print("COMPILADOR COMPLETO: CÓDIGO FUENTE -> CÓDIGO INTERMEDIO")
    print("=" * 70)
    
    for i, ejemplo in enumerate(ejemplos, 1):
        print(f"\n{'-' * 50}")
        print(f"EJEMPLO {i}: {ejemplo['nombre']}")
        print(f"{'-' * 50}")
        
        success, result = compile_to_intermediate_code(ejemplo['codigo'])
        
        if success:
            print("✓ Compilación exitosa")
        else:
            print(f"✗ Error en compilación: {result}")
        
        print()


if __name__ == "__main__":
    main()
