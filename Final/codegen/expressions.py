"""
Generación de código intermedio para expresiones.
"""

def generate_expression_code(ast_node, code_generator):
    """
    Genera código intermedio para expresiones.
    
    Args:
        ast_node: Nodo AST de expresión
        code_generator: Instancia de CodeGenerator
    
    Returns:
        str: Variable temporal donde se almacena el resultado
    """
    # Si es un valor simple (número, variable)
    if not isinstance(ast_node, tuple):
        return str(ast_node)
    
    # Si es una expresión binaria (operador, operando1, operando2)
    if len(ast_node) == 3:
        operator, left, right = ast_node
        
        # Generar código para operandos
        left_var = generate_expression_code(left, code_generator)
        right_var = generate_expression_code(right, code_generator)
        
        # Generar variable temporal para el resultado
        result_var = code_generator.get_temp_var()
        
        # Generar instrucción
        code_generator.add_instruction(f"{result_var} = {left_var} {operator} {right_var}")
        
        return result_var
    
    # Si es una expresión unaria (operador, operando)
    elif len(ast_node) == 2:
        operator, operand = ast_node
        
        # Generar código para operando
        operand_var = generate_expression_code(operand, code_generator)
        
        # Generar variable temporal para el resultado
        result_var = code_generator.get_temp_var()
        
        # Generar instrucción
        code_generator.add_instruction(f"{result_var} = {operator} {operand_var}")
        
        return result_var
    
    else:
        raise ValueError(f"Expresión AST no reconocida: {ast_node}")


def generate_arithmetic_expression_code(ast_node, code_generator):
    """
    Genera código intermedio específicamente para expresiones aritméticas.
    
    Args:
        ast_node: Nodo AST de expresión aritmética
        code_generator: Instancia de CodeGenerator
    
    Returns:
        str: Variable temporal donde se almacena el resultado
    """
    return generate_expression_code(ast_node, code_generator)


def generate_logical_expression_code(ast_node, code_generator):
    """
    Genera código intermedio específicamente para expresiones lógicas.
    
    Args:
        ast_node: Nodo AST de expresión lógica
        code_generator: Instancia de CodeGenerator
    
    Returns:
        str: Variable temporal donde se almacena el resultado
    """
    return generate_expression_code(ast_node, code_generator)
