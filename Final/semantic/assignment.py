def check_assignment(node, scopes, infer_type):
    # node = ("ASSIGNMENT", nombre, expresión)
    nombre = node[1]
    
    # Verificar que la variable esté declarada
    if not scopes.is_declared(nombre):
        raise NameError(f"Variable '{nombre}' no declarada en el ámbito '{scopes.current_scope_name()}'")
    
    # Verificar que todas las variables en la expresión estén declaradas
    valor = node[2]
    _check_expression_variables(valor, scopes)
    
    # Verificar tipos (opcional, por ahora comentado)
    # tipo_var = scopes.get_type(nombre)
    # tipo_valor = infer_type(valor, scopes)
    # if tipo_var != tipo_valor:
    #     raise Exception(f"Tipos incompatibles en asignación a '{nombre}': {tipo_var} <- {tipo_valor}")

def _check_expression_variables(expr, scopes):
    """Verifica que todas las variables en una expresión estén declaradas."""
    if isinstance(expr, str):
        # Es un identificador - verificar si no es un literal numérico, booleano o string
        if not expr.isdigit() and not expr.replace('.', '').isdigit() and expr not in ['true', 'false'] and not expr.startswith('"') and not expr.startswith("'"):
            if not scopes.is_declared(expr):
                raise NameError(f"Variable '{expr}' no declarada en el ámbito '{scopes.current_scope_name()}'")
    elif isinstance(expr, tuple):
        # Es una expresión compuesta
        if len(expr) >= 3:
            # Formato: (operador, left, right)
            _check_expression_variables(expr[1], scopes)
            _check_expression_variables(expr[2], scopes)
        elif len(expr) == 2:
            # Formato: (operador, operando)
            _check_expression_variables(expr[1], scopes)
    # Para números e otros literales, no hacer nada
