# semantic/functions.py
# Análisis semántico para funciones

def check_function(node, scopes, analyze_node):
    """
    Verifica que una función sea semánticamente correcta
    """
    _, func_name, params, return_type, body = node
    
    # Crear un nuevo ámbito para la función
    scopes.enter_scope_func(func_name)
    
    # Verificar parámetros duplicados
    param_names = set()
    for param_type, param_name in params:
        if param_name in param_names:
            raise ValueError(f"Parámetro '{param_name}' duplicado en función '{func_name}'")
        param_names.add(param_name)
        
        # Declarar el parámetro en el ámbito de la función
        scopes.declare(param_name, param_type)
    
    # Analizar el cuerpo de la función
    for stmt in body:
        analyze_node(stmt, scopes)
    
    # Salir del ámbito de la función
    scopes.exit_scope()
