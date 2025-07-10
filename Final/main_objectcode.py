"""
Generador de código objeto - Archivo principal.
Traduce código intermedio a código objeto ejecutable.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from objectcode import translate_intermediate_to_object, StackMachine
from objectcode.code_translator import CodeTranslator

def generate_object_code_example():
    """Ejemplo básico de generación de código objeto."""
    
    # Código intermedio de ejemplo
    intermediate_code = [
        "DECLARE int x",
        "ASSIGN x = 5",
        "DECLARE int y", 
        "ASSIGN y = 10",
        "t0 = x + y",
        "ASSIGN x = t0"
    ]
    
    print("=== GENERADOR DE CÓDIGO OBJETO ===")
    print("Código intermedio:")
    for i, instruction in enumerate(intermediate_code):
        print(f"  {i+1}: {instruction}")
    
    # Traducir a código objeto
    translator = CodeTranslator()
    object_code = translator.translate_program(intermediate_code)
    
    print("\nInformación de variables:")
    var_info = translator.get_variable_info()
    for var_name, address in var_info['variables'].items():
        print(f"  {var_name}: @{address}")
    
    print()
    translator.print_object_code()
    
    # Crear y ejecutar en la máquina virtual
    vm = StackMachine()
    vm.load_program(object_code)
    
    print("\n=== EJECUTANDO EN MÁQUINA VIRTUAL ===")
    vm.run(debug=True)
    
    return translator, vm


def test_complex_expression():
    """Prueba con expresión más compleja."""
    
    intermediate_code = [
        "DECLARE int a",
        "ASSIGN a = 10",
        "DECLARE int b",
        "ASSIGN b = 20", 
        "DECLARE int c",
        "ASSIGN c = 30",
        "t0 = a * b",
        "t1 = c / 3",
        "t2 = t0 + t1",
        "DECLARE int resultado",
        "ASSIGN resultado = t2"
    ]
    
    print("\n" + "="*50)
    print("PRUEBA CON EXPRESIÓN COMPLEJA")
    print("="*50)
    print("Código intermedio:")
    for i, instruction in enumerate(intermediate_code):
        print(f"  {i+1}: {instruction}")
    
    translator = CodeTranslator()
    object_code = translator.translate_program(intermediate_code)
    
    print("\nInformación de variables:")
    var_info = translator.get_variable_info()
    for var_name, address in var_info['variables'].items():
        print(f"  {var_name}: @{address}")
    
    print()
    translator.print_object_code()
    
    vm = StackMachine()
    vm.load_program(object_code)
    
    print("\n=== EJECUTANDO EN MÁQUINA VIRTUAL ===")
    vm.run(debug=True)
    
    return translator, vm


def main():
    """Función principal."""
    print("GENERADOR DE CÓDIGO OBJETO - DEMO")
    print("="*50)
    
    # Ejemplo básico
    translator1, vm1 = generate_object_code_example()
    
    # Ejemplo complejo
    translator2, vm2 = test_complex_expression()
    
    print("\n" + "="*50)
    print("RESUMEN DE RESULTADOS")
    print("="*50)
    
    print("Ejemplo básico:")
    print(f"  Variables: {translator1.get_variable_info()['count']}")
    print(f"  Instrucciones: {len(translator1.get_object_code())}")
    print(f"  Estado final: {vm1.get_state()}")
    
    print("\nEjemplo complejo:")
    print(f"  Variables: {translator2.get_variable_info()['count']}")
    print(f"  Instrucciones: {len(translator2.get_object_code())}")
    print(f"  Estado final: {vm2.get_state()}")


if __name__ == "__main__":
    main()
