"""
Generación de código intermedio para asignaciones.
"""

def generate_assignment_code(ast_node, code_generator):
    """
    Genera código intermedio para asignaciones.
    
    Args:
        ast_node: Nodo AST de la forma ('ASSIGNMENT', variable, valor)
        code_generator: Instancia de CodeGenerator
    
    Returns:
        str: Variable asignada
    """
    if ast_node[0] != 'ASSIGNMENT':
        raise ValueError(f"Nodo AST esperado de tipo ASSIGNMENT, recibido: {ast_node[0]}")
    
    _, var_name, value = ast_node
    
    # Verificar que la variable esté declarada
    if not code_generator.is_variable_declared(var_name):
        raise ValueError(f"Variable '{var_name}' no declarada")
    
    # Generar código para el valor
    if isinstance(value, tuple):
        # Es una expresión compleja
        from .expressions import generate_expression_code
        result_var = generate_expression_code(value, code_generator)
        code_generator.add_instruction(f"ASSIGN {var_name} = {result_var}")
    else:
        # Es un valor simple
        code_generator.add_instruction(f"ASSIGN {var_name} = {value}")
    
    return var_name


def generate_assignment_list_code(ast_nodes, code_generator):
    """
    Genera código intermedio para una lista de asignaciones.
    
    Args:
        ast_nodes: Lista de nodos AST de asignaciones
        code_generator: Instancia de CodeGenerator
    
    Returns:
        list: Lista de variables asignadas
    """
    assigned_vars = []
    
    for node in ast_nodes:
        if node[0] == 'ASSIGNMENT':
            var_name = generate_assignment_code(node, code_generator)
            assigned_vars.append(var_name)
    
    return assigned_vars
