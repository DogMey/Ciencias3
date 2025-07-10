"""
Generación de código intermedio para declaraciones de variables.
"""

def generate_declaration_code(ast_node, code_generator):
    """
    Genera código intermedio para declaraciones de variables.
    
    Args:
        ast_node: Nodo AST de la forma ('DECLARATION', tipo, nombre, valor)
        code_generator: Instancia de CodeGenerator
    
    Returns:
        str: Variable donde se almacena el resultado (el nombre de la variable declarada)
    """
    if ast_node[0] != 'DECLARATION':
        raise ValueError(f"Nodo AST esperado de tipo DECLARATION, recibido: {ast_node[0]}")
    
    _, var_type, var_name, initial_value = ast_node
    
    # Registrar la variable en la tabla de símbolos
    code_generator.declare_variable(var_type, var_name)
    
    # Generar instrucción de declaración
    code_generator.add_instruction(f"DECLARE {var_type} {var_name}")
    
    # Si tiene valor inicial, generar la asignación
    if initial_value is not None:
        from .expressions import generate_expression_code
        
        # Si el valor inicial es una expresión, generar su código
        if isinstance(initial_value, tuple):
            # Es una expresión compleja (ej: ('*', 'x', 2))
            result_var = generate_expression_code(initial_value, code_generator)
            code_generator.add_instruction(f"ASSIGN {var_name} = {result_var}")
        else:
            # Es un valor simple (número, variable, etc.)
            code_generator.add_instruction(f"ASSIGN {var_name} = {initial_value}")
    
    return var_name


def generate_declaration_list_code(ast_nodes, code_generator):
    """
    Genera código intermedio para una lista de declaraciones.
    
    Args:
        ast_nodes: Lista de nodos AST de declaraciones
        code_generator: Instancia de CodeGenerator
    
    Returns:
        list: Lista de nombres de variables declaradas
    """
    declared_vars = []
    
    for node in ast_nodes:
        if node[0] == 'DECLARATION':
            var_name = generate_declaration_code(node, code_generator)
            declared_vars.append(var_name)
    
    return declared_vars
