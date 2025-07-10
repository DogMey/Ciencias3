"""
Generador de código intermedio - Archivo principal.
Recorre el AST y genera código intermedio de tres direcciones.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from codegen import CodeGenerator, generate_declaration_code, generate_assignment_code

def generate_intermediate_code(ast_nodes):
    """
    Genera código intermedio completo a partir de una lista de nodos AST.
    
    Args:
        ast_nodes: Lista de nodos AST del programa
    
    Returns:
        CodeGenerator: Instancia con el código intermedio generado
    """
    code_generator = CodeGenerator()
    
    for node in ast_nodes:
        if node[0] == 'DECLARATION':
            generate_declaration_code(node, code_generator)
        elif node[0] == 'ASSIGNMENT':
            generate_assignment_code(node, code_generator)
        else:
            print(f"Advertencia: Tipo de nodo no soportado aún: {node[0]}")
    
    return code_generator


def main():
    """Función principal para pruebas."""
    # Ejemplo de AST simple
    ast_example = [
        ('DECLARATION', 'int', 'x', 5),
        ('DECLARATION', 'int', 'y', 10),
        ('ASSIGNMENT', 'x', ('+', 'x', 1)),
        ('ASSIGNMENT', 'y', ('*', 'x', 2))
    ]
    
    print("=== GENERADOR DE CÓDIGO INTERMEDIO ===")
    print("AST de entrada:")
    for i, node in enumerate(ast_example):
        print(f"  {i+1}: {node}")
    
    print("\nGenerando código intermedio...")
    code_generator = generate_intermediate_code(ast_example)
    
    print("\nTabla de símbolos:")
    for var_name, info in code_generator.symbol_table.items():
        print(f"  {var_name}: {info}")
    
    print()
    code_generator.print_code()


if __name__ == "__main__":
    main()
