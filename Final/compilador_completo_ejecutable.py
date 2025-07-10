"""
Compilador completo: Código fuente -> Código objeto ejecutable
Lexer -> Parser -> Generador de código intermedio -> Generador de código objeto -> Máquina virtual
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main_parser import parser
from main_lexer import lexer
from codegen import CodeGenerator, generate_declaration_code, generate_assignment_code
from objectcode.code_translator import CodeTranslator
from objectcode.stack_machine import StackMachine

def compile_and_execute(source_code, debug=False):
    """
    Compila y ejecuta código fuente completo.
    
    Args:
        source_code: Código fuente
        debug: Si mostrar información de depuración
    
    Returns:
        dict: Resultado de la ejecución
    """
    try:
        if debug:
            print("="*60)
            print("COMPILADOR COMPLETO - CÓDIGO FUENTE A EJECUCIÓN")
            print("="*60)
        
        # Paso 1: Análisis léxico
        if debug:
            print("\n=== PASO 1: ANÁLISIS LÉXICO ===")
        
        tokens = lexer(source_code)
        if debug:
            print(f"Tokens generados: {len(tokens)}")
        
        # Paso 2: Análisis sintáctico
        if debug:
            print("\n=== PASO 2: ANÁLISIS SINTÁCTICO ===")
        
        ast_nodes = parser(tokens)
        if debug:
            print(f"AST generado: {len(ast_nodes)} nodos")
            for i, node in enumerate(ast_nodes):
                print(f"  {i+1}: {node}")
        
        # Paso 3: Generación de código intermedio
        if debug:
            print("\n=== PASO 3: GENERACIÓN DE CÓDIGO INTERMEDIO ===")
        
        code_generator = CodeGenerator()
        
        for node in ast_nodes:
            if node[0] == 'DECLARATION':
                generate_declaration_code(node, code_generator)
            elif node[0] == 'ASSIGNMENT':
                generate_assignment_code(node, code_generator)
        
        intermediate_code = [instr for instr in code_generator.get_code()]
        
        if debug:
            print(f"Código intermedio generado: {len(intermediate_code)} instrucciones")
            for i, instr in enumerate(intermediate_code):
                print(f"  {i+1}: {instr}")
        
        # Paso 4: Generación de código objeto
        if debug:
            print("\n=== PASO 4: GENERACIÓN DE CÓDIGO OBJETO ===")
        
        translator = CodeTranslator()
        object_code = translator.translate_program(intermediate_code)
        
        if debug:
            print(f"Código objeto generado: {len(object_code)} instrucciones")
            var_info = translator.get_variable_info()
            print(f"Variables: {var_info['count']}")
            for var_name, address in var_info['variables'].items():
                print(f"  {var_name}: @{address}")
            print()
            translator.print_object_code()
        
        # Paso 5: Ejecución en máquina virtual
        if debug:
            print("\n=== PASO 5: EJECUCIÓN EN MÁQUINA VIRTUAL ===")
        
        vm = StackMachine()
        vm.load_program(object_code)
        vm.run(debug=debug)
        
        final_state = vm.get_state()
        
        if debug:
            print(f"\n=== RESULTADO FINAL ===")
            print(f"Estado de la máquina: {final_state}")
            print(f"Variables finales:")
            for var_name, address in var_info['variables'].items():
                if address in final_state['memory']:
                    print(f"  {var_name} = {final_state['memory'][address]}")
        
        return {
            'success': True,
            'tokens': len(tokens),
            'ast_nodes': len(ast_nodes),
            'intermediate_instructions': len(intermediate_code),
            'object_instructions': len(object_code),
            'variables': var_info['variables'],
            'final_state': final_state,
            'result': final_state['memory']
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'error_type': type(e).__name__
        }


def run_examples():
    """Ejecuta ejemplos predefinidos."""
    ejemplos = [
        {
            "nombre": "Declaración y asignación simple",
            "codigo": """
                int x = 5;
                int y = 10;
                x = x + y;
            """
        },
        {
            "nombre": "Expresión aritmética compleja",
            "codigo": """
                int a = 10;
                int b = 20;
                int c = 30;
                int resultado = a * b + c / 3;
            """
        }
    ]
    
    print("EJEMPLOS PREDEFINIDOS")
    print("="*50)
    
    for i, ejemplo in enumerate(ejemplos, 1):
        print(f"\n{'-'*40}")
        print(f"EJEMPLO {i}: {ejemplo['nombre']}")
        print(f"{'-'*40}")
        
        resultado = compile_and_execute(ejemplo['codigo'], debug=True)
        
        if resultado['success']:
            print("✓ COMPILACIÓN Y EJECUCIÓN EXITOSA")
        else:
            print(f"✗ ERROR: {resultado['error']}")


def interactive_mode():
    """Modo interactivo para ingresar código."""
    print("MODO INTERACTIVO")
    print("="*50)
    print("Ingrese código fuente tipo C (termine con una línea vacía)")
    print("Escriba 'salir' para terminar")
    print("Escriba 'ejemplos' para ver ejemplos predefinidos")
    print("Escriba 'ayuda' para ver sintaxis soportada")
    print()
    
    while True:
        print("Ingrese su código (línea vacía para compilar y ejecutar):")
        print("> ", end="")
        
        # Leer código fuente línea por línea
        lines = []
        while True:
            try:
                line = input()
                if line.strip() == "":
                    break
                elif line.strip().lower() == "salir":
                    print("¡Hasta luego!")
                    return
                elif line.strip().lower() == "ejemplos":
                    print()
                    run_examples()
                    print("\nIngrese su código:")
                    print("> ", end="")
                    continue
                elif line.strip().lower() == "ayuda":
                    print_help()
                    print("\nIngrese su código:")
                    print("> ", end="")
                    continue
                else:
                    lines.append(line)
                    print("> ", end="")
            except (EOFError, KeyboardInterrupt):
                print("\n¡Hasta luego!")
                return
        
        if not lines:
            continue
            
        source_code = "\n".join(lines)
        
        print("\n" + "="*60)
        print("COMPILANDO Y EJECUTANDO...")
        print("="*60)
        
        resultado = compile_and_execute(source_code, debug=True)
        
        if resultado['success']:
            print("\n✓ COMPILACIÓN Y EJECUCIÓN EXITOSA")
        else:
            print(f"\n✗ ERROR: {resultado['error']}")
        
        print("\n" + "="*60)
        print()


def print_help():
    """Muestra ayuda sobre la sintaxis soportada."""
    print("\nSINTAXIS SOPORTADA:")
    print("-" * 30)
    print("Declaraciones:")
    print("  int variable = valor;")
    print("  int x = 10;")
    print()
    print("Asignaciones:")
    print("  variable = expresión;")
    print("  x = y + 5;")
    print()
    print("Expresiones aritméticas:")
    print("  +, -, *, /, % (suma, resta, multiplicación, división, módulo)")
    print("  Paréntesis para precedencia: (a + b) * c")
    print()
    print("Ejemplos:")
    print("  int x = 5;")
    print("  int y = 10;")
    print("  int resultado = x * y + 3;")


def main():
    """Función principal con menú interactivo."""
    print("COMPILADOR COMPLETO - CÓDIGO FUENTE A EJECUCIÓN")
    print("="*60)
    print()
    print("Seleccione una opción:")
    print("1. Modo interactivo")
    print("2. Ejecutar ejemplos predefinidos")
    print("3. Salir")
    print()
    
    while True:
        try:
            opcion = input("Ingrese su opción (1-3): ").strip()
            
            if opcion == "1":
                print()
                interactive_mode()
                break
            elif opcion == "2":
                print()
                run_examples()
                break
            elif opcion == "3":
                print("¡Hasta luego!")
                break
            else:
                print("Opción inválida. Ingrese 1, 2 o 3.")
        except (EOFError, KeyboardInterrupt):
            print("\n¡Hasta luego!")
            break


if __name__ == "__main__":
    main()
