def check_ifblock(node, scopes, analyze_node):
    # node = ("IF", condicion, cuerpo) o ("IF_ELSE", condicion, cuerpo_if, cuerpo_else)
    node_type = node[0]
    condicion = node[1]
    cuerpo_if = node[2]
    
    # Validar que todas las variables en la condición estén declaradas
    _check_condition_variables(condicion, scopes)
    
    # Analizar el bloque if en su propio ámbito
    scopes.enter_scope_if()
    for stmt in cuerpo_if:
        analyze_node(stmt, scopes)
    scopes.exit_scope()
    
    # Si hay un bloque else, analizarlo en su propio ámbito
    if node_type == "IF_ELSE" and len(node) > 3:
        cuerpo_else = node[3]
        scopes.enter_scope_if()  # Usar el mismo tipo de scope para else
        for stmt in cuerpo_else:
            analyze_node(stmt, scopes)
        scopes.exit_scope()

def _check_condition_variables(condition, scopes):
    """Verifica que todas las variables en una condición estén declaradas."""
    if isinstance(condition, str):
        # Es un identificador - verificar si no es un literal numérico, booleano o string
        if not condition.isdigit() and not condition.replace('.', '').isdigit() and condition not in ['true', 'false'] and not condition.startswith('"') and not condition.startswith("'"):
            if not scopes.is_declared(condition):
                raise NameError(f"Variable '{condition}' no declarada en el ámbito '{scopes.current_scope_name()}'")
    elif isinstance(condition, tuple):
        # Es una expresión compuesta
        if len(condition) >= 3:
            # Formato: (operador, left, right)
            _check_condition_variables(condition[1], scopes)
            _check_condition_variables(condition[2], scopes)
        elif len(condition) == 2:
            # Formato: (operador, operando)
            _check_condition_variables(condition[1], scopes)
    # Para números e otros literales, no hacer nada